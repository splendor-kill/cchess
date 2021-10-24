from collections import defaultdict

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


def toggle_view(col=None, row=None):
    col = N_COLS - 1 - col if col is not None else None
    row = N_ROWS - 1 - row if row is not None else None
    return col, row


class Board:
    """
           cxj
     012345678
    0         9
    1         8
    2         7
    3         6
    4         5
    5         4
    6         3
  r 7         2
  y 8         1
  i 9         0
     876543210
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

    def piece_at(self, col, row):
        for p in self.situation:
            if p.col == col and p.row == row:
                return p
        return None

    def remove(self, c, r):
        pass

    def throw_away(self, piece):
        if piece in self.situation:
            self.situation.remove(piece)
        else:
            raise ValueError('piece not found')

    def get_shuai(self, camp):
        for p in self.situation:
            if p.camp == camp and p.force == Force.SHUAI:
                return p

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
                    sit.append(clz(camp, j, i))
        return sit

    def filter(self, camp, force):
        d = defaultdict(list)
        for p in self.situation:
            if p.camp == camp and p.force == force:
                d[p.col].append(p)
        return d

    def get_piece(self, camp, force_, col, row_indicator: RowIndicator = None):
        pieces = []
        for p in self.situation:
            if p.camp == camp and p.force == force_ and p.col == col:
                pieces.append(p)
        n_pieces = len(pieces)
        if n_pieces == 1:
            return pieces[0]

        rev = camp == Camp.BLACK
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
                piece.col = dst[0]
                piece.row = dst[1]
            else:
                raise ValueError('illegal move')

    def check_if_shuai_meet(self, shuai1_pos, shuai2_pos, ignore_piece=None):
        col1, row1 = shuai1_pos
        col2, row2 = shuai2_pos
        if col1 != col2:
            return False
        lb, ub = min(row1, row2), max(row1, row2)
        for r in range(lb + 1, ub - 1):  # have any piece in between
            p = self.piece_at(col1, r)
            if p is not None and p is not ignore_piece:
                return False
        return True


def parse_action(cmd: str, camp: Camp, board: Board):
    """中式记法，参考 https://zh.wikipedia.org/wiki/%E8%B1%A1%E6%A3%8B

    :param cmd: str, assume has normalized
    :param camp: which side
    :param board:
    :return: locations (src, dst)
    """

    cmd = cmd.strip()
    if len(cmd) == 3:
        if cmd[-1] in {ACTION_ALIAS[Action.ADVANCE], ACTION_ALIAS[Action.RETREAT]}:  # 处理如“兵七进”
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
        src_col -= 1  # to internal repr
        if camp == Camp.RED:  # from right to left
            src_col, _ = toggle_view(src_col, None)
    else:  # need ref board
        assert prefix is not None
        col2pieces = board.filter(camp, force)
        if len(col2pieces) == 1:
            (col, pieces), = col2pieces.items()
            sample = pieces[0]
            assert sample.force != Force.BING and prefix in (RowIndicator.FRONT, RowIndicator.REAR) \
                   or sample.force == Force.BING
            src_col = col
        else:
            assert force == Force.BING
            if prefix is None:
                raise ValueError('undistinguishable')
            if prefix in (RowIndicator.MID, RowIndicator.THIRD, RowIndicator.FORTH):
                src_col = max(col2pieces, key=lambda k: len(col2pieces[k]))
            else:
                raise ValueError('undistinguishable')

    piece = board.get_piece(camp, force, src_col, prefix)
    if piece is None:
        raise ValueError('piece not found')

    n = set(cmd).intersection(ACTION_ALIAS_INV)
    assert len(n) == 1
    (a), = n  # get the unique element
    action = ACTION_ALIAS_INV[a]
    i = cmd.index(a)
    act_param = cmd[i + 1] if i + 1 < len(cmd) else '1'
    if act_param not in COL_ALIAS_INV:
        raise ValueError('invalid action param')
    act_param = COL_ALIAS_INV[act_param]
    param_must_be_col = {(Force.JU, Action.TRAVERSE),
                         (Force.MA, Action.ADVANCE), (Force.MA, Action.RETREAT),
                         (Force.XIANG, Action.ADVANCE), (Force.XIANG, Action.RETREAT),
                         (Force.SHI, Action.ADVANCE), (Force.SHI, Action.RETREAT),
                         (Force.SHUAI, Action.TRAVERSE),
                         (Force.PAO, Action.TRAVERSE),
                         (Force.BING, Action.TRAVERSE)}
    if (piece.force, action) in param_must_be_col:
        act_param -= 1

    dst = piece.calc_dst(action, act_param)

    return force, action, act_param, piece, dst


def test():
    situation = [Shuai(Camp.BLACK, 4, 0),
                 Shi(Camp.BLACK, 3, 2), Bing(Camp.RED, 4, 2),
                 Xiang(Camp.BLACK, 8, 2),
                 Bing(Camp.BLACK, 0, 3),
                 Ma(Camp.BLACK, 6, 5),
                 Bing(Camp.RED, 2, 6), Bing(Camp.BLACK, 6, 6),
                 Ju(Camp.RED, 4, 7),
                 Bing(Camp.BLACK, 3, 8), Bing(Camp.BLACK, 5, 8),
                 Shuai(Camp.RED, 4, 9),
                 ]
    board = Board(situation)
    print(board)

    from constants import FULL_BOARD
    board = Board(FULL_BOARD)
    print(board)


if __name__ == '__main__':
    from force import *

    test()
