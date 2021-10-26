from board import Board, Action, REWARD_DRAW, REWARD_WIN, REWARD_LOSE
from constants import FULL_BOARD
from piece import Camp


class Env:
    def __init__(self, opening=None):
        self.opening = opening if opening is not None else FULL_BOARD
        self.stats = {}
        self.board = None
        self.cur_player = Camp.RED
        self.sue_draw = False

    def reset(self):
        self.cur_player = Camp.RED
        self.board = Board(self.opening)
        return self._make_observation()

    def _make_observation(self):
        state = self.board.observe()
        valid_actions = self.board.get_final_valid_actions(self.cur_player)
        ob = {'next_player': self.cur_player,
              'board_state': state,
              'valid_actions': valid_actions,
              'board': self.board,
              'sue_draw': self.sue_draw
              }
        return ob

    def render(self):
        print(self.board)

    def step(self, action):
        if action['action'] == Action.RESIGN:
            return None, REWARD_LOSE, True, None
        if action['action'] == Action.SUE_DRAW:
            assert 'act_param' in action
            if self.sue_draw:
                if action['act_param']:  # two camps agree with draw
                    return None, REWARD_DRAW, True, None
                else:
                    self.sue_draw = False  # disagree
            else:
                self.sue_draw = True  # propose

            self._switch_player()
            ob = self._make_observation()
            if len(ob['valid_actions']) == 0:
                return ob, REWARD_WIN, True, None  # note: no way out, opponent win
            return ob, None, False, None

        piece = action['piece']
        dst = action['dst']

        try:
            capture_enemy_shuai = self.board.make_move(piece, dst)
            if capture_enemy_shuai:
                return None, REWARD_WIN, True, None
        except ValueError as e:
            print(e)
            return None, REWARD_LOSE, True, None

        done = self.board.test_draw()
        if done:
            return None, REWARD_DRAW, True, None

        self._switch_player()
        ob = self._make_observation()
        if len(ob['valid_actions']) == 0:
            return ob, REWARD_WIN, True, None  # note: no way out, opponent win
        return ob, None, False, None

    def close(self):
        self.board = None

    def _switch_player(self):
        self.cur_player = self.cur_player.opponent()
