from env import Env
from piece import Camp
from player import Human, NoBrain


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
        format='##### %(processName)-15s %(filename)10s line %(lineno)-5d %(name)10s %(funcName)-10s: %(message)s',
        stream=sys.stderr,

    )
    # np.random.seed(0)
    s = time.perf_counter()

    n = 1
    play_a_game()

    elapsed = time.perf_counter() - s
    print(f'play {n} games spent {elapsed} seconds in total, mean time: {elapsed / n}')
