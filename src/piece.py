import os
from enum import IntEnum
from board import Action

APPEAR_BLACK = ''
APPEAR_RED = ''
ENDC = ''

if os.name == 'posix':
    APPEAR_BLACK = '\033[1;30;47m'
    APPEAR_RED = '\033[1;31;47m'
    ENDC = '\033[0m'

PIECE_CHARS = '將士象馬車砲卒帥仕相傌俥炮兵'
PLACE_CHARS = '＋Ｘ'


class Camp(IntEnum):
    BLACK = 1
    RED = 2


class Force(IntEnum):
    SHUAI = 1
    SHI = 2
    XIANG = 3
    MA = 4
    JU = 5
    PAO = 6
    BING = 7


FORCE_ALIAS = {
    Force.SHUAI: tuple('将帅將帥'),
    Force.SHI: tuple('士仕'),
    Force.XIANG: tuple('象相'),
    Force.MA: tuple('马㐷馬傌'),
    Force.JU: tuple('车伡車俥'),
    Force.PAO: tuple('炮砲'),
    Force.BING: tuple('兵卒'),
}
FORCE_ALIAS_INV = {e: k for k, v in FORCE_ALIAS.items() for e in v}

COL_ALIAS = {
    1: tuple('1１一'),
    2: tuple('2２二'),
    3: tuple('3３三'),
    4: tuple('4４四'),
    5: tuple('5５五'),
    6: tuple('6６六'),
    7: tuple('7７七'),
    8: tuple('8８八'),
    9: tuple('9９九')
}
COL_ALIAS_INV = {e: k for k, v in COL_ALIAS.items() for e in v}


def piece_2_char(camp, force):
    index = 7 * (camp.value - 1) + force.value - 1
    return PIECE_CHARS[index]


def recog_piece(piece: str):
    assert piece in PIECE_CHARS
    assert len(piece) == 1
    idx = PIECE_CHARS.index(piece)
    q, r = divmod(idx, len(Force))
    camp = Camp(q + 1)
    force = Force(r + 1)
    return camp, force


class Piece:
    def __init__(self, row, col, camp, force):
        """xiangqi 术语参考 http://wxf.ca/xq/computer/XIANGQI_TERMS_IN_ENGLISH.pdf

        :param row: rank
        :param col: file
        :param camp: red or black
        :param force: piece type
        """
        self.row = row
        self.col = col
        self.camp = camp
        self.force = force

    def __str__(self):
        c = piece_2_char(self.camp, self.force)
        appear = APPEAR_RED if self.camp == Camp.RED else APPEAR_BLACK
        c = appear + c + ENDC
        return c

    def can_move(self, board, action, param):
        d_fn = {Action.TRAVERSE: self.traverse,
                Action.ADVANCE: self.advance,
                Action.RETREAT: self.retreat}
        fn = d_fn[action]
        return False, fn(param)

    def get_legal_moves(self):
        pass

    def traverse(self, col):
        pass

    def advance(self, d):
        pass

    def retreat(self, d):
        pass
