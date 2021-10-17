from collections import defaultdict
from enum import IntEnum
import numpy as np

from constants import EMPTY_BOARD
from piece import *

N_ROWS = 10  # term: rank
N_COLS = 9  # term: file


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


class Board:
    """
         o ------- x(j)
         |
         |
    y(i) |
    """

    def __init__(self, situation):
        if isinstance(situation, str):
            situation = self._parse(situation)
        self.situation = situation
        assert isinstance(self.situation, list)

    def __str__(self):
        sit = {f'p{i}{j}': PLACE_CHARS[0] for i in range(N_ROWS) for j in range(N_ROWS)}
        for p in self.situation:
            k = f'p{p.row}{p.col}'
            sit[k] = str(p)
        return EMPTY_BOARD.format(**sit)

    def observe(self):
        plane = np.zeros((N_ROWS, N_COLS), np.int32)
        for p in self.situation:
            c = piece_2_char(p.camp, p.force)
            idx = PIECE_CHARS.index(c)
            plane[p.row, p.col] = idx
        return plane

    def get_valid_actions(self, camp):
        pass

    def can_move(self, x, y, dx, dy):
        return False

    def remove(self, x, y):
        pass

    @staticmethod
    def _parse(board):
        import force
        force_clz = {Force.JU: force.Ju,
                     Force.MA: force.Ma,
                     Force.XIANG: force.Xiang,
                     Force.SHI: force.Shi,
                     Force.SHUAI: force.Shuai,
                     Force.PAO: force.Pao,
                     Force.BING: force.Bing,
                     }
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
                    clz = force_clz[force]
                    sit.append(clz(i, j, camp))
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
        from board import Action
        d_fn = {Action.TRAVERSE: piece.traverse,
                Action.ADVANCE: piece.advance,
                Action.RETREAT: piece.retreat}
        fn = d_fn[action]
        return False, fn(param)


        piece_at_dst = None
        for p in self.situation:
            if p.col == dst[0] and p.row == dst[1]:
                piece_at_dst = p
                break

        if piece_at_dst is None:  # just move
            piece.col = dst[0]
            piece.row = dst[1]
        else:
            if piece_at_dst.camp != piece.camp:
                # TODO check if can move by rule
                self.situation.remove(piece_at_dst)
                print(f'capture the piece {piece_at_dst}')
            else:
                raise ValueError('illegal move')


def parse_action(cmd: str, camp: Camp, board: Board):
    """中式记法，参考 https://zh.wikipedia.org/wiki/%E8%B1%A1%E6%A3%8B

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
    cmds = [
        # '炮二平五',
        '马8进7',
        # '炮8平9',
    ]
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
    # situation = [Piece(0, 4, Camp.BLACK, Force.SHUAI),
    #              Piece(2, 3, Camp.BLACK, Force.SHI), Piece(2, 4, Camp.RED, Force.BING),
    #              Piece(2, 8, Camp.BLACK, Force.XIANG),
    #              Piece(3, 0, Camp.BLACK, Force.BING),
    #              Piece(5, 6, Camp.BLACK, Force.MA),
    #              Piece(6, 2, Camp.RED, Force.BING), Piece(6, 6, Camp.BLACK, Force.BING),
    #              Piece(7, 4, Camp.RED, Force.JU),
    #              Piece(8, 3, Camp.BLACK, Force.BING), Piece(8, 5, Camp.BLACK, Force.BING),
    #              Piece(9, 4, Camp.RED, Force.SHUAI),
    #              ]
    # board = Board(situation)
    # print(board)

    from constants import well_known_1, FULL_BOARD
    board = Board(FULL_BOARD)
    print(board)


if __name__ == '__main__':
    test()
    # test_parse_action()
