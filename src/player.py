from piece import Camp, Force, piece_2_char
from board import parse_action, Action, ACTION_ALIAS, ROW_INDICATOR_ALIAS, RowIndicator


class Player:
    def __init__(self, id_):
        self._id_ = id_
        self._env = None

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, env):
        self._env = env

    def make_decision(self, **kwargs):
        raise NotImplementedError('leave the chance to successors')


class Human(Player):
    def __init__(self, id_, **kwargs):
        super().__init__(id_)

    def make_decision(self, **kwargs):
        valid_actions = kwargs['valid_actions']
        camp = kwargs['next_player']
        board = kwargs['board']

        while True:
            directive = input('what do you want? ')
            print(directive)

            try:
                action = self.flex_action_input(directive, camp, board)
                return action
            except Exception as e:
                print(e)

    @staticmethod
    def flex_action_input(directive: str, camp, board):
        pinyin = {
            'ju': piece_2_char(Camp.RED, Force.JU),
            'ma': piece_2_char(Camp.RED, Force.MA),
            'xiang': piece_2_char(Camp.RED, Force.XIANG),
            'shi': piece_2_char(Camp.RED, Force.SHI),
            'shuai': piece_2_char(Camp.RED, Force.SHUAI),
            'jiang': piece_2_char(Camp.BLACK, Force.SHUAI),
            'pao': piece_2_char(Camp.RED, Force.PAO),
            'bing': piece_2_char(Camp.RED, Force.BING),
            'zu': piece_2_char(Camp.BLACK, Force.BING),
            'ping': ACTION_ALIAS[Action.TRAVERSE],
            '=': ACTION_ALIAS[Action.TRAVERSE],
            'jin': ACTION_ALIAS[Action.ADVANCE],
            '+': ACTION_ALIAS[Action.ADVANCE],
            'tui': ACTION_ALIAS[Action.RETREAT],
            '-': ACTION_ALIAS[Action.RETREAT],
            'qian': ROW_INDICATOR_ALIAS[RowIndicator.FRONT],
            'zhong': ROW_INDICATOR_ALIAS[RowIndicator.MID],
            'hou': ROW_INDICATOR_ALIAS[RowIndicator.REAR],
            'er': ROW_INDICATOR_ALIAS[RowIndicator.SECOND],
            'san': ROW_INDICATOR_ALIAS[RowIndicator.THIRD],
            'si': ROW_INDICATOR_ALIAS[RowIndicator.FORTH],
            'wu': ROW_INDICATOR_ALIAS[RowIndicator.FIFTH],
            'front': ROW_INDICATOR_ALIAS[RowIndicator.FRONT],
            'mid': ROW_INDICATOR_ALIAS[RowIndicator.MID],
            'rear': ROW_INDICATOR_ALIAS[RowIndicator.REAR],
            'second': ROW_INDICATOR_ALIAS[RowIndicator.SECOND],
            'third': ROW_INDICATOR_ALIAS[RowIndicator.THIRD],
            'forth': ROW_INDICATOR_ALIAS[RowIndicator.FORTH],
            'fifth': ROW_INDICATOR_ALIAS[RowIndicator.FIFTH],
        }
        directive = directive.lower()
        for k, v in pinyin.items():
            directive = directive.replace(k, v)
        directive = directive.replace(' ', '')
        force, action, act_param, piece, dst = parse_action(directive, camp, board)
        print(force, action, act_param, piece, dst)
        return {'piece': piece, 'action': action, 'act_param': act_param, 'dst': dst}


class NoBrain(Player):
    def __init__(self, id_):
        super().__init__(id_)

    def make_decision(self, **kwargs):
        valid_actions = kwargs['valid_actions']
