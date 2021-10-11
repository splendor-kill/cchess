import os
from collections import defaultdict
from enum import IntEnum

from chessman.Bing import *
from chessman.Che import *
from chessman.Ma import *
from chessman.Pao import *
from chessman.Shi import *
from chessman.Shuai import *
from chessman.Xiang import *

APPEAR_BLACK = ''
APPEAR_RED = ''
ENDC = ''
if os.name == 'posix':
    APPEAR_BLACK = '\033[1;30;47m'
    APPEAR_RED = '\033[1;31;47m'
    ENDC = '\033[0m'

PIECE_CHARS = '將士象馬車砲卒帥仕相傌俥炮兵'
PLACE_CHARS = '＋Ｘ'
N_ROWS = 10  # term: rank
N_COLS = 9  # term: file


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


class Action(IntEnum):
    ADVANCE = 1
    RETREAT = 2
    TRAVERSE = 3


ACTION_ALIAS = {
    Action.ADVANCE: '进',
    Action.RETREAT: '退',
    Action.TRAVERSE: '平'
}
ACTION_ALIAS_INV = {v: k for k, v in ACTION_ALIAS.items()}


class RowIndicator(IntEnum):
    FRONT = 1
    MID = 2
    REAR = 3
    SECOND = 4
    THIRD = 5
    FORTH = 6
    FIFTH = 7


ROW_INDICATOR_ALIAS = {
    RowIndicator.FRONT: '前',
    RowIndicator.REAR: '后',
    RowIndicator.MID: '中',
    RowIndicator.SECOND: '二',
    RowIndicator.THIRD: '三',
    RowIndicator.FORTH: '四',
    RowIndicator.FIFTH: '五',
}
ROW_INDICATOR_ALIAS_INV = {v: k for k, v in ROW_INDICATOR_ALIAS.items()}


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


EMPTY_BOARD = '''
１　２　３　４　５　６　７　８　９
{p00}－{p01}－{p02}－{p03}－{p04}－{p05}－{p06}－{p07}－{p08}
｜　｜　｜　｜＼｜／｜　｜　｜　｜
{p10}－{p11}－{p12}－{p13}－{p14}－{p15}－{p16}－{p17}－{p18}
｜　｜　｜　｜／｜＼｜　｜　｜　｜
{p20}－{p21}－{p22}－{p23}－{p24}－{p25}－{p26}－{p27}－{p28}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p30}－{p31}－{p32}－{p33}－{p34}－{p35}－{p36}－{p37}－{p38}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p40}－{p41}－{p42}－{p43}－{p44}－{p45}－{p46}－{p47}－{p48}
{p50}－{p51}－{p52}－{p53}－{p54}－{p55}－{p56}－{p57}－{p58}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p60}－{p61}－{p62}－{p63}－{p64}－{p65}－{p66}－{p67}－{p68}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p70}－{p71}－{p72}－{p73}－{p74}－{p75}－{p76}－{p77}－{p78}
｜　｜　｜　｜＼｜／｜　｜　｜　｜
{p80}－{p81}－{p82}－{p83}－{p84}－{p85}－{p86}－{p87}－{p88}
｜　｜　｜　｜／｜＼｜　｜　｜　｜
{p90}－{p91}－{p92}－{p93}－{p94}－{p95}－{p96}－{p97}－{p98}
九　八　七　六　五　四　三　二　一
'''


class ChessBoard:
    pieces = dict()

    selected_piece = None

    def __init__(self, north_is_red=True):
        # self.north_is_red = north_is_red
        # north area
        ChessBoard.pieces[4, 0] = Shuai(4, 0, north_is_red, "north")

        ChessBoard.pieces[0, 3] = Bing(0, 3, north_is_red, "north")
        ChessBoard.pieces[2, 3] = Bing(2, 3, north_is_red, "north")
        ChessBoard.pieces[4, 3] = Bing(4, 3, north_is_red, "north")
        ChessBoard.pieces[6, 3] = Bing(6, 3, north_is_red, "north")
        ChessBoard.pieces[8, 3] = Bing(8, 3, north_is_red, "north")

        ChessBoard.pieces[1, 2] = Pao(1, 2, north_is_red, "north")
        ChessBoard.pieces[7, 2] = Pao(7, 2, north_is_red, "north")

        ChessBoard.pieces[3, 0] = Shi(3, 0, north_is_red, "north")
        ChessBoard.pieces[5, 0] = Shi(5, 0, north_is_red, "north")

        ChessBoard.pieces[2, 0] = Xiang(2, 0, north_is_red, "north")
        ChessBoard.pieces[6, 0] = Xiang(6, 0, north_is_red, "north")

        ChessBoard.pieces[1, 0] = Ma(1, 0, north_is_red, "north")
        ChessBoard.pieces[7, 0] = Ma(7, 0, north_is_red, "north")

        ChessBoard.pieces[0, 0] = Che(0, 0, north_is_red, "north")
        ChessBoard.pieces[8, 0] = Che(8, 0, north_is_red, "north")

        # south area
        ChessBoard.pieces[4, 9] = Shuai(4, 9, not north_is_red, "south")

        ChessBoard.pieces[0, 6] = Bing(0, 6, not north_is_red, "south")
        ChessBoard.pieces[2, 6] = Bing(2, 6, not north_is_red, "south")
        ChessBoard.pieces[4, 6] = Bing(4, 6, not north_is_red, "south")
        ChessBoard.pieces[6, 6] = Bing(6, 6, not north_is_red, "south")
        ChessBoard.pieces[8, 6] = Bing(8, 6, not north_is_red, "south")

        ChessBoard.pieces[1, 7] = Pao(1, 7, not north_is_red, "south")
        ChessBoard.pieces[7, 7] = Pao(7, 7, not north_is_red, "south")

        ChessBoard.pieces[3, 9] = Shi(3, 9, not north_is_red, "south")
        ChessBoard.pieces[5, 9] = Shi(5, 9, not north_is_red, "south")

        ChessBoard.pieces[2, 9] = Xiang(2, 9, not north_is_red, "south")
        ChessBoard.pieces[6, 9] = Xiang(6, 9, not north_is_red, "south")

        ChessBoard.pieces[1, 9] = Ma(1, 9, not north_is_red, "south")
        ChessBoard.pieces[7, 9] = Ma(7, 9, not north_is_red, "south")

        ChessBoard.pieces[0, 9] = Che(0, 9, not north_is_red, "south")
        ChessBoard.pieces[8, 9] = Che(8, 9, not north_is_red, "south")

    def can_move(self, x, y, dx, dy):
        return self.pieces[x, y].can_move(self, dx, dy)

    def move(self, x, y, dx, dy):
        return self.pieces[x, y].move(self, dx, dy)

    def remove(self, x, y):
        del self.pieces[x, y]

    def select(self, x, y, player_is_red):
        # 选中棋子
        if not self.selected_piece:
            if (x, y) in self.pieces and self.pieces[x, y].is_red == player_is_red:
                self.pieces[x, y].selected = True
                self.selected_piece = self.pieces[x, y]
            return False, None

        # 移动棋子
        if not (x, y) in self.pieces:
            if self.selected_piece:
                ox, oy = self.selected_piece.x, self.selected_piece.y
                if self.can_move(ox, oy, x - ox, y - oy):
                    self.move(ox, oy, x - ox, y - oy)
                    self.pieces[x, y].selected = False
                    self.selected_piece = None
                    return True, (ox, oy, x, y)
            return False, None

        # 同一个棋子
        if self.pieces[x, y].selected:
            return False, None

        # 吃子
        if self.pieces[x, y].is_red != player_is_red:
            ox, oy = self.selected_piece.x, self.selected_piece.y
            if self.can_move(ox, oy, x - ox, y - oy):
                self.move(ox, oy, x - ox, y - oy)
                self.pieces[x, y].selected = False
                self.selected_piece = None
                return True, (ox, oy, x, y)
            return False, None

        # 取消选中
        for key in self.pieces.keys():
            self.pieces[key].selected = False
        # 选择棋子
        self.pieces[x, y].selected = True
        self.selected_piece = self.pieces[x, y]
        return False, None


class Board:
    """
         -------- x(j)
         |
         |
    y(i) |
    """

    def __init__(self, situation):
        if isinstance(situation, str):
            situation = self._parse(situation)
        self.situation = situation
        assert isinstance(self.situation, list)
        self.pieces_in_col = self.indexing_by_col()

    def __str__(self):
        sit = {f'p{i}{j}': PLACE_CHARS[0] for i in range(N_ROWS) for j in range(N_ROWS)}
        for p in self.situation:
            k = f'p{p.row}{p.col}'
            sit[k] = str(p)
        return EMPTY_BOARD.format(**sit)

    def get_col(self, col):
        pass

    def indexing_by_col(self):
        d = defaultdict(list)
        for p in self.situation:
            d[p.col].append(p)
        return d

    @staticmethod
    def _parse(board):
        board = board.strip()
        rows = board.splitlines()
        rows = rows[:9:2] + rows[-9::2]
        assert len(rows) == N_ROWS
        sit = []
        for i, r in enumerate(rows):
            r = r.strip()
            assert len(r) == 17
            r = r[::2]  # remove non-place chars
            for j, c in enumerate(r):
                if c in PIECE_CHARS:
                    camp, force = recog_piece(c)
                    sit.append(Piece(i, j, camp, force))
        return sit

    def filter(self, camp, force):
        d = defaultdict(list)
        for p in self.situation:
            if p.camp == camp and p.force == force:
                d[p.col].append(p)
        return d

    def get_piece(self, camp, force, col, row_indicator: RowIndicator = None):
        """

        :param camp:
        :param force:
        :param col: relative to camp self perspective, in [1..9]
        :param row_indicator:
        :return: piece
        """

        col -= 1
        if camp == Camp.RED:  # from right to left
            col = N_COLS - 1 - col
        pieces = []
        for p in self.situation:
            if p.camp == camp and p.force == force and p.col == col:
                pieces.append(p)
        n_pieces = len(pieces)
        if n_pieces == 1:
            return pieces[0]

        rev = camp == Camp.RED
        pieces.sort(key=lambda p: p.row, reverse=rev)
        if row_indicator == RowIndicator.FRONT:
            assert n_pieces > 1
            return pieces[0]
        elif row_indicator == RowIndicator.MID:
            assert n_pieces == 3
            return pieces[1]
        elif row_indicator == RowIndicator.REAR:
            assert n_pieces > 1
            return pieces[-1]
        elif row_indicator == RowIndicator.SECOND:
            assert n_pieces >= 2
            return pieces[1]
        elif row_indicator == RowIndicator.THIRD:
            assert n_pieces >= 3
            return pieces[2]
        elif row_indicator == RowIndicator.FORTH:
            assert n_pieces >= 4
            return pieces[3]
        elif row_indicator == RowIndicator.FIFTH:
            assert n_pieces == 5
            return pieces[4]

    def make_move(self, piece, dst):
        to_remove = None
        for p in self.situation:
            if p.col == dst[0] and p.row == dst[1] and p.camp != piece.camp:
                to_remove = p


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


def normalize_action(cmd):
    pass


def parse_action(cmd: str, camp: Camp, board: Board):
    """中式记法，参考 https://zh.wikipedia.org/wiki/%E8%B1%A1%E6%A3%8B
    参考2 http://wxf.ca/xq/computer/wxf_notation.html ;
    参考3 http://wxf.ca/xq/computer/XIANGQI_TERMS_IN_ENGLISH.pdf

    :param cmd: str, assume has normalized
    :param camp: which side
    :param board:
    :return: locations (src, dst)
    """

    cmd = cmd.strip()
    if len(cmd) == 3:
        if cmd[-1] == ACTION_ALIAS[Action.ADVANCE]:  # 处理如“兵七进”
            cmd = cmd + '1'
    assert len(cmd) in (4, 5)
    n = set(cmd).intersection(FORCE_ALIAS_INV)
    assert len(n) == 1
    (p), = n  # get the unique element
    force = FORCE_ALIAS_INV[p]
    i = cmd.index(p)
    assert i in (0, 1)
    prefix = cmd[i - 1] if i > 0 else None
    if prefix is not None:
        assert prefix in ROW_INDICATOR_ALIAS_INV
        prefix = ROW_INDICATOR_ALIAS_INV[prefix]
    src_col = cmd[i + 1]
    if src_col in COL_ALIAS_INV:
        src_col = COL_ALIAS_INV[src_col]
    else:  # need ref board
        assert prefix is not None
        col2pieces = board.filter(camp, force)
        if len(col2pieces) == 1:
            (col, piece), = col2pieces.items()
            assert piece != Force.BING and prefix in (RowIndicator.FRONT, RowIndicator.REAR) or piece == Force.BING
            src_col = col
        else:
            assert force == Force.BING
            if prefix is None:
                raise ValueError('undistinguishable')
            prefix = ROW_INDICATOR_ALIAS_INV[prefix]
            if prefix in (RowIndicator.MID, RowIndicator.THIRD, RowIndicator.FORTH):
                src_col = max(col2pieces, key=lambda k: len(col2pieces[k]))
            else:
                raise ValueError('undistinguishable')

    piece = board.get_piece(camp, force, src_col, prefix)

    n = set(cmd).intersection(ACTION_ALIAS_INV)
    assert len(n) == 1
    (a), = n  # get the unique element
    action = ACTION_ALIAS_INV[a]
    i = cmd.index(a)
    act_param = cmd[i + 1]
    assert act_param in COL_ALIAS_INV
    act_param = COL_ALIAS_INV[act_param]

    dst = calc_dst(piece, action, act_param)

    return force, action, act_param, piece, dst


def calc_dst(piece, action, act_param):
    dir_ = -1 if piece.camp == Camp.RED else 1
    if action == Action.TRAVERSE:
        dst_col = act_param - 1
        dst_row = piece.row
    elif action == Action.ADVANCE:
        dst_col = piece.col
        dst_row = piece.row + dir_ * act_param
    else:  # Action.RETREAT
        dst_col = piece.col
        dst_row = piece.row - dir_ * act_param
    return dst_col, dst_row


def test_parse_action():
    cmds = ['炮二平五']  # , '马8进7', '炮8平9', ]
    # '前㐷退六', '后炮平4', '卒3进1', '车9进1',
    # '兵七进', '中兵进', '三兵平四', '三兵三平四', '前兵九平八']

    from constants import FULL_BOARD
    board = Board(FULL_BOARD)
    for cmd in cmds:
        force, action, act_param, piece, dst = parse_action(cmd, Camp.RED, board)
        print(force, action, act_param, piece, dst)
        board.make_move(piece, dst)
        print(board)


def test():
    situation = [Piece(0, 4, Camp.BLACK, Force.SHUAI),
                 Piece(2, 3, Camp.BLACK, Force.SHI), Piece(2, 4, Camp.RED, Force.BING),
                 Piece(2, 8, Camp.BLACK, Force.XIANG),
                 Piece(3, 0, Camp.BLACK, Force.BING),
                 Piece(5, 6, Camp.BLACK, Force.MA),
                 Piece(6, 2, Camp.RED, Force.BING), Piece(6, 6, Camp.BLACK, Force.BING),
                 Piece(7, 4, Camp.RED, Force.JU),
                 Piece(8, 3, Camp.BLACK, Force.BING), Piece(8, 5, Camp.BLACK, Force.BING),
                 Piece(9, 4, Camp.RED, Force.SHUAI),
                 ]
    board = Board(situation)
    print(board)

    from constants import well_known_1
    board = Board(well_known_1)
    print(board)


if __name__ == '__main__':
    # test()
    test_parse_action()
