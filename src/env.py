from board import Board
from constants import FULL_BOARD
from piece import Camp


class Env:
    def __init__(self, opening=None):
        self.opening = opening if opening is not None else FULL_BOARD
        self.stats = {}
        self.board = None
        self.cur_player = Camp.RED

    def reset(self):
        self.cur_player = Camp.RED
        self.board = Board(self.opening)
        state = self.board.observe()
        valid_actions = self.board.get_valid_actions(self.cur_player)
        ob = {'next_player': self.cur_player,
              'board_state': state,
              'valid_actions': valid_actions,
              'board': self.board
              }
        return ob

    def render(self):
        print(self.board)

    def step(self, action):
        piece = action['piece']
        dx, dy = action['dst']
        self.board.move(piece.col, piece.row, dx, dy)
        self._switch_player()
        state = self.board.observe()
        done, reward = self._check_end()
        valid_actions = self.board.get_valid_actions(self.cur_player)
        ob = {'next_player': self.cur_player,
              'board_state': state,
              'valid_actions': valid_actions,
              'board': self.board
              }
        return ob, reward, done, None

    def close(self):
        self.board = None

    def _check_end(self):
        return False, 0

    def _switch_player(self):
        op = {Camp.RED: Camp.BLACK, Camp.BLACK: Camp.RED}
        self.cur_player = op[self.cur_player]
