from board import Board
from constants import FULL_BOARD
from piece import Camp


class Env:
    def __init__(self, red_player, black_player, opening=None):
        self.players = {Camp.RED: red_player, Camp.BLACK: black_player}
        self.opening = opening if opening is not None else FULL_BOARD
        self.stats = {}
        self.board = None

    def reset(self):
        self.board = Board(self.opening)
        return self.board.observe()

    def render(self):
        pass

    def step(self, action):
        ob = self.board.observe()
        done, reward = self._check_end()
        return ob, reward, done, None

    def close(self):
        self.players.clear()
        self.board = None

    def _check_end(self):
        return False, 0


if __name__ == '__main__':
    env = Env()
    observation = env.reset()
    for _ in range(1):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)

        if done:
            observation = env.reset()

    env.close()
