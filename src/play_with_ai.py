import multiprocessing as mp
from logging import DEBUG, StreamHandler, basicConfig, getLogger
from multiprocessing import Manager

from keras import backend as K

from agent.helper import flip_ucci_labels
from agent.player_mcts import MCTSPlayer
from board import get_iccs_action_space
from common.utils import load_cfg
from config import cfg
from env import Env
from model.nn import NNModel
from piece import Camp
from player import Human


def setup_logger(log_filename):
    format_str = '##### %(processName)-15s %(filename)10s line %(lineno)-5d %(name)10s %(funcName)-10s: %(message)s'
    # basicConfig(level=DEBUG, format=format_str, stream=sys.stderr)
    basicConfig(level=DEBUG, format=format_str, filename=log_filename)
    stream_handler = StreamHandler()
    getLogger().addHandler(stream_handler)


def load_ai_model(config, nn_model_config_path, nn_model_weight_path):
    model = NNModel(config)
    model.load(nn_model_config_path, nn_model_weight_path)
    model.session = K.get_session()
    model.graph = model.session.graph
    return model


def play_a_game(config, with_camp: Camp, nn_model_config_path, nn_model_weight_path, opening=None):
    play_config = config.play
    current_model = load_ai_model(config, nn_model_config_path, nn_model_weight_path)
    m = Manager()
    pipes_bundle = m.list([current_model.get_pipes(play_config.search_threads)
                           for _ in range(play_config.max_processes)])

    pipes_strand = pipes_bundle.pop()
    oppo_camp = with_camp.opponent()
    players = {with_camp: Human(with_camp),
               oppo_camp: MCTSPlayer(oppo_camp, config, pipes_strand=pipes_strand, play_config=play_config)
               }
    env = Env(opening)
    for p in players.values():
        p.env = env

    ob = env.reset()
    while True:
        env.render()
        player = players[ob['cur_player']]
        action = player.make_decision(**ob)
        ob, reward, done, info = env.step(action)
        if done:
            env.render()
            print(f'player {player.id.name}, reward: {reward}')
            break
    print('game over.')

    pipes_bundle.append(pipes_strand)


if __name__ == '__main__':
    import argparse
    import sys
    import time
    import warnings

    warnings.simplefilter(action='ignore', category=FutureWarning)

    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, default='config.yaml')
    parser.add_argument('--nn_model_config_path', type=str)
    parser.add_argument('--nn_model_weight_path', type=str)
    parser.add_argument('--human_color', default='red', choices=['red', 'black'], type=str)

    args = parser.parse_args()
    cfg.update(load_cfg(args.config))

    # setup_logger(cfg.resource.main_log_path)

    mp.set_start_method('spawn')
    sys.setrecursionlimit(10000)

    cfg.update(load_cfg(args.config))
    cfg.labels = get_iccs_action_space()
    cfg.n_labels = len(cfg.labels)
    print(f'action space size: {cfg.n_labels}')
    flipped = flip_ucci_labels(cfg.labels)
    cfg.unflipped_index = [cfg.labels.index(x) for x in flipped]
    # np.random.seed(0)
    s = time.perf_counter()

    camp = Camp.RED if args.human_color == 'red' else Camp.BLACK
    nn_model_config_path = cfg.resource.model_best_config_path if not args.nn_model_config_path else args.nn_model_config_path
    nn_model_weight_path = cfg.resource.model_best_weight_path if not args.nn_model_weight_path else args.nn_model_weight_path
    play_a_game(cfg, camp, nn_model_config_path, nn_model_weight_path)

    elapsed = time.perf_counter() - s
    print(f'spent {elapsed} seconds in total')
