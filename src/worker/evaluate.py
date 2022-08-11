"""
Encapsulates the worker which evaluates newly-trained models and picks the best one
"""
import json
import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from logging import getLogger
from multiprocessing import Manager
from random import random
from time import sleep
from typing import Tuple
from uuid import uuid4

from keras import backend as K
from xiangqi import Env, Camp

from agent.player_mcts import MCTSPlayer
from common.data_helper import check_ng_model_notifier, update_best_model_notifier, \
    check_best_model_notifier, get_next_gen_model_dirs
from common.store_helper import get_store_util
from model.helper import load_best_model_weight, save_as_best_model
from model.nn import NNModel

logger = getLogger(__name__)


def start(config):
    return EvaluateWorker(config).start()


class EvaluateWorker:
    """
    Worker which evaluates trained models and keeps track of the best one

    Attributes:
        :ivar Config config: config to use for evaluation
        :ivar PlayConfig config: PlayConfig to use to determine how to play, taken from config.eval.play_config
        :ivar ChessModel current_model: currently chosen best model
        :ivar Manager m: multiprocessing manager
        :ivar list(Connection) pipes_bundle: pipes on which the current best ChessModel is listening which will be used to
            make predictions while playing a game.
    """

    def __init__(self, config):
        """
        :param config: Config to use to control how evaluation should work
        """
        self.dist_id = uuid4().hex
        self.config = config
        rc = self.config.resource
        self.store_util = get_store_util(resource_config=rc)
        self.play_config = config.eval.play_config
        self.current_model = self.load_current_model()
        self.m = Manager()
        self.pipes_bundle = self.m.list([self.current_model.get_pipes(self.play_config.search_threads) for _ in
                                         range(self.play_config.max_processes)])

    def start(self):
        """
        Start evaluation, endlessly loading the latest models from the directory which stores them and
        checking if they do better than the current model, saving the result in self.current_model
        """
        model_walk = iter(self.load_next_generation_model())
        while True:
            try:
                ng_model, model_dir = next(model_walk)
            except StopIteration:
                sleep(1)
                model_walk = iter(self.load_next_generation_model())
                continue

            logger.info(f"start evaluate model {model_dir}")
            try:
                ng_is_great = self.evaluate_model(ng_model)
                if ng_is_great:
                    logger.info(f"New Model become best model: {model_dir}")
                    save_as_best_model(ng_model)
                    self.current_model = ng_model

                    rc = self.config.resource
                    update_best_model_notifier(self.store_util, rc, phase='updating', did=self.dist_id)
                    model_config_path = os.path.join(rc.model_dir, rc.model_best_config_path)
                    model_weight_path = os.path.join(rc.model_dir, rc.model_best_weight_path)
                    ng_model.upload(model_config_path, model_weight_path)
                    update_best_model_notifier(self.store_util, rc, phase='updated', did=self.dist_id)
                self.move_model(model_dir)
            except Exception as e:
                logger.error(e)

    def evaluate_model(self, ng_model):
        """
        Given a model, evaluates it by playing a bunch of games against the current model.

        :param ChessModel ng_model: model to evaluate
        :return: true iff this model is better than the current_model
        """
        ng_pipes = self.m.list(
            [ng_model.get_pipes(self.play_config.search_threads) for _ in range(self.play_config.max_processes)])

        futures = []
        with ProcessPoolExecutor(max_workers=self.play_config.max_processes) as executor:
            for game_idx in range(self.config.eval.game_num):
                fut = executor.submit(play_game, self.config, cur=self.pipes_bundle, ng=ng_pipes,
                                      cur_red=(game_idx % 2 == 0))
                futures.append(fut)

            results = []
            for fut in as_completed(futures):
                # ng_score := if ng_model win -> 1, lose -> 0, draw -> 0.5
                ng_score, env, cur_red = fut.result()
                results.append(ng_score)
                win_rate = sum(results) / len(results)
                game_idx = len(results)
                logger.debug(f"game {game_idx:3}: ng_score={ng_score:.1f} as {'black' if cur_red else 'red'} "
                             f"win_rate={win_rate * 100:5.1f}% ")

                if len(results) - sum(results) >= self.config.eval.game_num * (1 - self.config.eval.replace_rate):
                    logger.debug(f"lose count reach {results.count(0)} so give up challenge")
                    return False
                if sum(results) >= self.config.eval.game_num * self.config.eval.replace_rate:
                    logger.debug(f"win count reach {results.count(1)} so change best model")
                    return True

        win_rate = sum(results) / len(results)
        logger.debug(f"winning rate {win_rate * 100:.1f}%")
        return win_rate >= self.config.eval.replace_rate

    def move_model(self, model_dir):
        """
        Moves the newest model to the specified directory

        :param file model_dir: directory where model should be moved
        """
        rc = self.config.resource
        # new_dir = os.path.join(rc.next_gen_model_dir, "copies", os.path.basename(model_dir))
        # os.makedirs(os.path.dirname(new_dir), exist_ok=True)
        # os.rename(model_dir, new_dir)]
        shutil.rmtree(model_dir)

    def load_current_model(self):
        """
        Loads the best model from the standard directory.
        :return ChessModel: the model
        """

        model = NNModel(self.config)
        if self.config.model.distributed:
            self.wait_best_model_notifier(self.config.resource, model)
        load_best_model_weight(model)
        model.session = K.get_session()
        model.graph = model.session.graph
        return model

    def load_next_generation_model(self):
        """
        Loads the next generation model from the standard directory
        :return (ChessModel, file): the model and the directory that it was in
        """
        rc = self.config.resource
        next_gen_model_iterable = self.wait_next_gen_model_comming(
            rc) if rc.dist_next_gen_model else get_next_gen_model_dirs(rc)
        for model_dir in next_gen_model_iterable:
            config_path = os.path.join(model_dir, rc.next_gen_model_config_filename)
            weight_path = os.path.join(model_dir, rc.next_gen_model_weight_filename)
            model = NNModel(self.config)
            try:
                model.load(config_path, weight_path)
            except Exception as e:
                logger.error(e)
                continue
            model.session = K.get_session()
            model.graph = model.session.graph
            yield model, model_dir

    def wait_best_model_notifier(self, cfg, model):
        while True:
            _, carrier = check_best_model_notifier(self.store_util, cfg)
            if carrier is None:
                sleep(1)
            else:
                logger.debug(carrier)
                phase = carrier['phase']
                if phase == 'init':
                    sleep(1)
                    continue
                elif phase in ('init_done', 'updated'):
                    if carrier['id'] != self.dist_id:
                        logger.debug('download model')
                        config_path = os.path.join(cfg.model_dir, cfg.model_best_config_path)
                        weight_path = os.path.join(cfg.model_dir, cfg.model_best_weight_path)
                        model.download(config_path, weight_path)
                        # model.load() should be successful
                    else:
                        path = os.path.join(cfg.model_dir, cfg.model_best_weight_path)
                        assert os.path.exists(path)
                    break
                elif phase == 'updating':
                    if carrier['id'] != self.dist_id:
                        # wait someone upload model
                        sleep(random())
                        continue
                    else:
                        # get the chance to upload model
                        break

    def wait_next_gen_model_comming(self, cfg):
        from common.store_helper import get_store_util
        store_util = get_store_util(resource_config=cfg)
        all_models = set()
        while True:
            if not check_ng_model_notifier(store_util, cfg):
                sleep(1)
                continue
            proc = store_util.download_dirobj_async(cfg.s3_model_rec_dir, cfg.data_dir)
            proc.wait()
            models_at_now = set()
            path = os.path.join(cfg.data_dir, cfg.s3_model_rec_dir)
            files = os.listdir(path)
            for fn in files:
                with open(os.path.join(path, fn)) as f:
                    content = json.load(f)
                models_at_now.add(os.path.basename(content['model_dir']))
            logger.debug(f'n models at now: {len(models_at_now)}, {list(models_at_now)[0]}')
            new_models = set(models_at_now).difference(all_models)
            for f in new_models:
                model_name = os.path.basename(f)
                remote_path = os.path.join(cfg.next_gen_model_dir_remote, model_name)
                proc = store_util.download_dirobj_async(remote_path, cfg.next_gen_model_dir)
                proc.wait()
                logger.info(f'download_dirobj {remote_path} retcode: {proc.returncode}')
                if proc.returncode != 0:
                    continue
                all_models.add(f)
                model_path = os.path.join(cfg.next_gen_model_dir, model_name)
                yield model_path
            break


def play_game(config, cur, ng, cur_red: bool) -> Tuple[float, Env, bool]:
    """
    Plays a game against models cur and ng and reports the results.

    :param Config config: config for how to play the game
    :param ChessModel cur: should be the current model
    :param ChessModel ng: should be the next generation model
    :param bool cur_red: whether cur should play red or black
    :return (float, ChessEnv, bool): the score for the ng model
        (0 for loss, .5 for draw, 1 for win), the env after the game is finished, and a bool
        which is true iff cur played as red in that game.
    """
    cur_pipes = cur.pop()
    ng_pipes = ng.pop()

    cur_model_camp = Camp.RED if cur_red else Camp.BLACK
    ng_model_camp = cur_model_camp.opponent()

    players = {
        cur_model_camp: MCTSPlayer(cur_model_camp, config, pipes_strand=cur_pipes, play_config=config.eval.play_config),
        ng_model_camp: MCTSPlayer(ng_model_camp, config, pipes_strand=ng_pipes, play_config=config.eval.play_config)}
    env = Env()
    for p in players.values():
        p.env = env

    ob = env.reset()
    while True:
        # env.render()
        player = players[ob['cur_player']]
        action = player.make_decision(**ob)
        ob, reward, done, info = env.step(action)
        if done:
            logger.debug(f'player {player.id.name}, reward: {reward}')
            break

    if env.winner == ng_model_camp:
        ng_score = 1
    elif env.winner == cur_model_camp:
        ng_score = 0
    else:
        ng_score = 0.5

    cur.append(cur_pipes)
    ng.append(ng_pipes)

    return ng_score, env, cur_red
