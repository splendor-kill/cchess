import os
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from logging import getLogger
from multiprocessing import Manager
from random import random
from threading import Thread
from time import time, sleep
from uuid import uuid4

from keras import backend as K
from xiangqi import Env, Camp

from common.data_helper import get_game_data_filenames, write_game_data_to_file, check_best_model_notifier, \
    update_best_model_notifier
from common.store_helper import get_store_util
from model.helper import load_best_model_weight, save_as_best_model, \
    reload_best_model_weight_if_changed
from model.nn import NNModel

logger = getLogger(__name__)


def start(cfg):
    return SelfPlayWorker(cfg).start()


class SelfPlayWorker:
    def __init__(self, config):
        self.dist_id = uuid4().hex
        self.config = config
        rc = self.config.resource
        os.makedirs(rc.model_dir, exist_ok=True)
        os.makedirs(rc.play_data_dir, exist_ok=True)
        self.store_util = get_store_util(resource_config=rc)
        self.current_model = self.load_model()
        self.m = Manager()
        self.pipes_bundle = self.m.list([self.current_model.get_pipes(self.config.play.search_threads) for _ in
                                         range(self.config.play.max_processes)])
        self.buffer = []

    def start(self):
        self.buffer.clear()

        futures = deque()
        with ProcessPoolExecutor(max_workers=self.config.play.max_processes) as executor:
            for game_idx in range(self.config.play.max_processes * 2):
                futures.append(executor.submit(self_play_buffer, self.config, self.pipes_bundle))
            game_idx = 0
            while True:
                game_idx += 1
                start_time = time()
                x = futures.popleft()
                env, data = x.result()
                time_cost = time() - start_time
                winner = env.winner.name if env.winner is not None else str(env.winner)
                print(f'game: {game_idx}, time: {time_cost:.3f}, n_steps: {env.n_steps}, '
                      f'winner: {winner}, data len: {len(data)}')
                self.buffer += data
                if (game_idx % self.config.playdata.nb_game_in_file) == 0:
                    self.flush_buffer()
                    reload_best_model_weight_if_changed(self.current_model, self.store_util)
                futures.append(executor.submit(self_play_buffer, self.config, self.pipes_bundle))  # Keep it going

    def load_model(self):
        model = NNModel(self.config)
        rc = self.config.resource
        self.wait_best_model_notifier(rc, model)

        if self.config.opts.new or not load_best_model_weight(model):
            model.build()
            save_as_best_model(model)
            model_config_path = os.path.join(rc.model_dir, rc.model_best_config_path)
            model_weight_path = os.path.join(rc.model_dir, rc.model_best_weight_path)
            logger.info(f'upload model {model_weight_path}')
            model.upload(model_config_path, model_weight_path)
            update_best_model_notifier(self.store_util, rc, phase='init_done', did=self.dist_id)

        model.session = K.get_session()
        model.graph = model.session.graph
        return model

    def flush_buffer(self):
        """
        Flush the play data buffer and write the data to the appropriate location
        """
        rc = self.config.resource
        game_id = datetime.now().strftime("%Y%m%d-%H%M%S.%f")
        path = os.path.join(rc.play_data_dir, rc.play_data_filename_tmpl % game_id)
        logger.info(f"save play data to {path}")
        thread = Thread(target=write_game_data_to_file, args=(path, self.buffer, rc),
                        kwargs={'did': self.dist_id, 'time': game_id})
        thread.start()
        self.buffer = []

    def remove_play_data(self):
        """
        Delete the play data from disk
        """
        files = get_game_data_filenames(self.config.resource)
        if len(files) < self.config.playdata.max_file_num:
            return
        for i in range(len(files) - self.config.playdata.max_file_num):
            os.remove(files[i])

    def wait_best_model_notifier(self, cfg, model):
        start_time = time()
        while True:
            _, carrier = check_best_model_notifier(self.store_util, cfg)
            if carrier is None:
                update_best_model_notifier(self.store_util, cfg, phase='init', did=self.dist_id)
            else:
                logger.debug(carrier)
                phase = carrier['phase']
                if phase in ('init_done', 'updated'):
                    if carrier['id'] != self.dist_id:
                        logger.info('download model')
                        config_path = os.path.join(cfg.model_dir, cfg.model_best_config_path)
                        weight_path = os.path.join(cfg.model_dir, cfg.model_best_weight_path)
                        model.download(config_path, weight_path)
                        # model.load() should be successful
                    else:
                        path = os.path.join(cfg.model_dir, cfg.model_best_weight_path)
                        assert os.path.exists(path)
                    break
                elif phase in ('init', 'updating'):
                    if carrier['id'] != self.dist_id:
                        # wait someone upload model
                        sleep(random())
                        elapse = time() - start_time
                        if elapse < 1 * 60:
                            continue
                        else:
                            break  # may someone failed to upload model
                    else:
                        # get the chance to upload model
                        break


def self_play_buffer(config, pipes_bundle):
    """
    Play one game and add the play data to the buffer
    :param Config config: config for how to play
    :param list(Connection) cur: list of pipes to use to get a pipe to send observations to for getting
        predictions. One will be removed from this list during the game, then added back
    :return (ChessEnv,list((str,list(float)): a tuple containing the final ChessEnv state and then a list
        of data to be appended to the SelfPlayWorker.buffer
    """
    pipes_strand = pipes_bundle.pop()  # borrow
    from agent.player_mcts import MCTSPlayer

    players = {Camp.RED: MCTSPlayer(Camp.RED, config, pipes_strand=pipes_strand),
               Camp.BLACK: MCTSPlayer(Camp.BLACK, config, pipes_strand=pipes_strand)}
    env = Env()
    for p in players.values():
        p.env = env

    ob = env.reset()
    cnt, cost = 0, 0
    while True:
        # env.render()
        player = players[ob['cur_player']]
        start_time = time()
        action = player.make_decision(**ob)
        time_cost = time() - start_time
        cnt += 1
        cost += time_cost
        logger.debug(f'step: {cnt}, time cost(sec.): {time_cost:.3f}, average: {cost / cnt:.3f}')
        ob, reward, done, info = env.step(action)
        if done:
            extra = '' if info is None else f', info: {info}'
            logger.debug(f'player {player.id.name}, reward: {reward}{extra}')
            break
    logger.info(f'average cost(sec.): {cost / cnt:.3f}')
    player = players[env.cur_player]
    player.finish_game(reward)
    oppo = players[env.cur_player.opponent()]
    oppo.finish_game(-reward)

    data = []
    for i in range(len(player.moves)):
        data.append(player.moves[i])
        if i < len(oppo.moves):
            data.append(oppo.moves[i])

    pipes_bundle.append(pipes_strand)
    return env, data
