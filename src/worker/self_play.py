from logging import getLogger
import os
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from multiprocessing import Manager
from threading import Thread
from time import time

from env import Env
from model.nn import NNModel
from keras import backend as K

from common.data_helper import get_game_data_filenames, write_game_data_to_file, pretty_print
from model.helper import load_best_model_weight, save_as_best_model, \
    reload_best_model_weight_if_changed

logger = getLogger(__name__)


def start(cfg):
    return SelfPlayWorker(cfg).start()


class SelfPlayWorker:
    def __init__(self, config):
        self.config = config
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
                print(f'game {game_idx:3} time={time() - start_time:5.1f}s n_steps={env.n_steps:3} {str(env.winner):12}, data: {len(data)}') self.buffer += data
                if (game_idx % self.config.playdata.nb_game_in_file) == 0:
                    self.flush_buffer()
                    reload_best_model_weight_if_changed(self.current_model)
                futures.append(executor.submit(self_play_buffer, self.config, self.pipes_bundle))  # Keep it going

    def load_model(self):
        model = NNModel(self.config)
        if self.config.opts.new or not load_best_model_weight(model):
            model.build()
            save_as_best_model(model)
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
        thread = Thread(target=write_game_data_to_file, args=(path, self.buffer))
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
    from piece import Camp
    from agent.player_mcts import MCTSPlayer

    players = {Camp.RED: MCTSPlayer(Camp.RED, config, pipes_strand=pipes_strand),
               Camp.BLACK: MCTSPlayer(Camp.BLACK, config, pipes_strand=pipes_strand)}
    env = Env()
    for p in players.values():
        p.env = env

    ob = env.reset()
    while True:
        # env.render()
        player = players[ob['next_player']]
        action = player.make_decision(**ob)
        ob, reward, done, info = env.step(action)
        if done:
            print(f'player {player.id.name}, reward: {reward}')
            break

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
