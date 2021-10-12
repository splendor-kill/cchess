from player import Human, NoBrain
from env import Env


def play_a_game():
    players = [Human(env, 0), NoBrain(env, 1)]
    env = Env(players[0])


    env.reset()

    env.run()


if __name__ == '__main__':
    import logging
    import sys
    import time
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--human_color', default='red', choices=['red', 'black'], type=str)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='##### PID %(process)-8d %(processName)-15s %(filename)10s line %(lineno)-5d %(name)10s %(funcName)-10s: %(message)s',
        stream=sys.stderr,

    )
    # np.random.seed(0)
    s = time.perf_counter()

    n = 1
    play_a_game()

    elapsed = time.perf_counter() - s
    print(f'play {n} games spent {elapsed} seconds in total, mean time: {elapsed / n}')
