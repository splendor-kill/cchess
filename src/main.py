from env import Env
from piece import Camp
from board import get_iccs_action_space
from player import Human, NoBrain, Playbook
from common.utils import load_cfg
from config import cfg
import multiprocessing as mp

def flip_ucci_labels(labels):
    def repl(x):
        return "".join([(str(9 - int(a)) if a.isdigit() else a) for a in x])
    return [repl(x) for x in labels]


def play_a_game(opening=None):
    players = {Camp.RED: Human(Camp.RED), Camp.BLACK: Human(Camp.BLACK)}
    env = Env(opening)
    for p in players.values():
        p.env = env

    ob = env.reset()
    while True:
        env.render()
        player = players[ob['next_player']]
        action = player.make_decision(**ob)
        ob, reward, done, info = env.step(action)
        if done:
            env.render()
            print(f'player {player.id.name}, reward: {reward}')
            break
    print('game over.')


def demo(pgn):
    from common.pgn_parser import get_moves_and_result
    moves, result = get_moves_and_result(pgn)

    players = {Camp.RED: Playbook(Camp.RED, moves[::2], result), Camp.BLACK: Playbook(Camp.BLACK, moves[1::2], result)}
    env = Env()
    for p in players.values():
        p.env = env

    ob = env.reset()
    while True:
        env.render()
        player = players[ob['next_player']]
        action = player.make_decision(**ob)
        ob, reward, done, info = env.step(action)
        if done:
            env.render()
            print(f'player {player.id.name}, reward: {reward}')
            break
    print('game over.')


if __name__ == '__main__':
    import logging
    import sys
    import time
    import argparse
    import warnings

    warnings.simplefilter(action='ignore', category=FutureWarning)

    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, default='config.yaml')
    parser.add_argument('--human_color', default='red', choices=['red', 'black'], type=str)
    parser.add_argument('--cmd', help='what to do', choices=['self', 'opt', 'eval', 'demo'])
    parser.add_argument('--pgn_file', help='demo by pgn')

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG,
        format='##### %(processName)-15s %(filename)10s line %(lineno)-5d %(name)10s %(funcName)-10s: %(message)s',
        stream=sys.stderr
    )

    mp.set_start_method('spawn')
    sys.setrecursionlimit(10000)

    cfg.update(load_cfg(args.config))
    cfg.labels = get_iccs_action_space()
    cfg.n_labels = len(cfg.labels)
    flipped = flip_ucci_labels(cfg.labels)
    cfg.unflipped_index = [cfg.labels.index(x) for x in flipped]
    # np.random.seed(0)
    s = time.perf_counter()

    if args.cmd == 'self':
        from worker import self_play

        self_play.start(cfg)
        sys.exit(0)
    elif args.cmd == 'opt':
        from worker import optimize

        optimize.start(cfg)
        sys.exit(0)
    elif args.cmd == 'eval':
        from worker import evaluate

        evaluate.start(cfg)
        sys.exit(0)
    elif args.cmd == 'demo':
        demo(args.pgn_file)
        sys.exit(0)

    n = 1
    play_a_game()

    elapsed = time.perf_counter() - s
    print(f'play {n} games spent {elapsed} seconds in total, mean time: {elapsed / n}')
