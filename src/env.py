from logging import getLogger

from board import Board, Action, REWARD_DRAW, REWARD_WIN, REWARD_LOSE, REWARD_ILLEGAL, parse_action_iccs
from constants import FULL_BOARD
from piece import CAMP_ALIAS, Camp, Force, CAMP_ALIAS_INV
from player import infer_action_and_param

MAX_GAME_LENGTH = 200
LOWER_BOUND_SUE_DRAW = 25
N_STATES_TO_TEST_DRAW = 12

logger = getLogger(__name__)


class Env:
    def __init__(self, opening=None):
        self.opening = opening if opening is not None else FULL_BOARD
        self.board: Board = Board(self.opening)
        self.cur_player = Camp.RED
        self.sue_draw = False
        self.done = False
        self.winner: Camp = None
        self.n_steps = 0
        self.last_capture = 0
        self.last_n_states = []
        self.stats = {}

    def reset(self):
        self.cur_player = Camp.RED
        self.sue_draw = False
        self.done = False
        self.winner = None
        self.n_steps = 0
        self.last_capture = 0
        self.last_n_states = []
        self.stats = {}
        self.board = Board(self.opening)
        ob = self._make_observation()
        self._record_state(ob['board_state'])
        return ob

    def _make_observation(self, captured=None):
        state = self.board.observe()
        valid_actions = self.board.get_final_valid_actions(self.cur_player)
        ob = {'cur_player': self.cur_player,
              'board_state': state,
              'valid_actions': valid_actions,
              'sue_draw': self.sue_draw,
              'board': self.board,
              'captured': captured
              }
        return ob

    def render(self):
        print(self.board)

    def step(self, action):
        self.n_steps += 1
        if 'action' in action and action['action'] == Action.RESIGN:
            self.done = True
            self.winner = self.cur_player.opponent()
            return None, REWARD_LOSE, True, None
        if 'action' in action and action['action'] == Action.SUE_DRAW:
            if self.n_steps <= LOWER_BOUND_SUE_DRAW:
                self.done = True
                self.winner = self.cur_player.opponent()
                info = f'sue for peace only after {LOWER_BOUND_SUE_DRAW} turns'
                return None, REWARD_ILLEGAL, True, info
                
            if self.sue_draw:
                assert 'act_param' in action
                if action['act_param']:  # two camps agree with draw
                    self.done = True
                    self.winner = None
                    return None, REWARD_DRAW, True, None
                else:
                    self.sue_draw = False  # disagree
            else:
                self.sue_draw = True  # propose

            if self._opponent_no_way_out():
                self.done = True
                self.winner = self.cur_player
                return None, REWARD_WIN, True, None

            self._switch_player()
            ob = self._make_observation()
            self._record_state(ob['board_state'])
            assert len(ob['valid_actions']) != 0
            return ob, None, False, None

        piece = action['piece']
        dst = action['dst']
        if piece.camp != self.cur_player:
            info = "illegal move, you can't move opponent's piece"
            return None, REWARD_ILLEGAL, True, info

        try:
            captured = self.board.make_move(piece, dst)
            if captured is not None:
                self.last_capture = self.n_steps
                if captured.force == Force.SHUAI:
                    self.done = True
                    self.winner = self.cur_player
                    return None, REWARD_WIN, True, None
        except ValueError as e:
            logger.info(repr(e))
            self.done = True
            self.winner = self.cur_player.opponent()
            return None, REWARD_ILLEGAL, True, None

        if self.test_draw():
            self.done = True
            self.winner = None  # means DRAW
            return None, REWARD_DRAW, True, None

        if self._opponent_no_way_out():
            self.done = True
            self.winner = self.cur_player
            return None, REWARD_WIN, True, None

        self._switch_player()
        ob = self._make_observation(captured)
        self._record_state(ob['board_state'])
        assert len(ob['valid_actions']) != 0
        return ob, None, False, None

    def close(self):
        self.board = None

    def _switch_player(self):
        self.cur_player = self.cur_player.opponent()

    def canonical_input_planes(self):
        import numpy as np
        b = self.board.encode()
        planes = []
        order = (Camp.RED, Camp.BLACK) if self.cur_player == Camp.RED else (Camp.BLACK, Camp.RED)
        for c in order:
            for f in Force:
                v = c * 10 + f
                p = (b==v).astype(np.int32)
                planes.append(p)
        # TODO: add history
        planes = np.stack(planes, axis=0)
        logger.debug(f'input shape: {planes.shape}')
        return planes
    
    def test_draw(self):
        if self.n_steps > MAX_GAME_LENGTH:
            return True
        RULE_NO_CAPTURE_STEPS = 60
        if self.n_steps - self.last_capture >= RULE_NO_CAPTURE_STEPS:
            return True
        if self.does_history_repeat(self.last_n_states):
            return True
        if self.board.test_draw():
            return True

        return False

    def _record_state(self, state):
        self.last_n_states.append(state)
        if len(self.last_n_states) > N_STATES_TO_TEST_DRAW:
            self.last_n_states.pop(0)

    def _opponent_no_way_out(self):
        valid_actions = self.board.get_final_valid_actions(self.cur_player.opponent())
        return len(valid_actions) == 0

    @staticmethod
    def does_history_repeat(history):
        if len(history) < N_STATES_TO_TEST_DRAW:
            return False
        for i in range(4):
            hs = history[i::4]
            h0 = hs[0]
            for h in hs[1:]:
                if not (h0 == h).all():
                    return False
        return True

    @staticmethod
    def from_fen(fen: str):
        parts = fen.strip().split()
        n_parts = len(parts)
        assert n_parts >= 6
        opening = parts[0]
        color = parts[1]
        assert parts[2] == '-'
        assert parts[3] == '-'
        n_steps_since_last_kill = int(parts[4])
        n_turns = int(parts[5])

        env = Env(opening=opening)
        env.cur_player = CAMP_ALIAS_INV[color]
        env.n_steps = 2 * n_turns
        if n_parts == 6:
            return env

        assert parts[6] == 'moves'
        for m in parts[7:]:
            print(env.to_fen())
            piece, dst = parse_action_iccs(m, env.board)
            if piece.camp != env.cur_player:
                print(f'player {env.cur_player.name} want do action {m}, but {piece} is not own by him')
                break
            act, param = infer_action_and_param(piece, dst)
            action = {'action': act, 'act_param': param, 'piece': piece, 'dst': dst}
            env.step(action)
        print(env.to_fen())
        return env

    def to_fen(self):
        parts = []
        parts.append(self.board.board_to_fen1())
        parts.append(CAMP_ALIAS[self.cur_player])
        parts.append('-')
        parts.append('-')
        parts.append('0')
        parts.append(str(self.n_steps // 2))
        return ' '.join(parts)
