from piece import Camp, Force
from piece import Piece


class Shuai(Piece):
    def __init__(self, camp, col, row):
        super().__init__(camp, Force.SHUAI, col, row)

    def can_move(self, board_, col, row):
        from board import N_COLS, N_ROWS
        assert 0 <= col < N_COLS
        assert 0 <= row < N_ROWS
        pos = self.get_valid_pos(board_)
        return (col, row) in pos

    def traverse(self, col):
        assert col in (3, 4, 5)
        col, _ = self.with_my_view(col, None)
        d = abs(self.col - col)
        assert d == 1
        return col, self.row

    def advance(self, x):
        assert x == 1
        row = self.row + self.heading * 1
        _, row_in_my_view = self.with_my_view(None, row)
        assert 0 <= row_in_my_view <= 2
        return self.col, row

    def retreat(self, x):
        assert x == 1
        row = self.row - self.heading * 1
        _, row_in_my_view = self.with_my_view(None, row)
        assert 0 <= row_in_my_view <= 2
        return self.col, row

    def get_valid_pos(self, board_):
        black_palace = {(3, 0): [(3, 1), (4, 0)], (4, 0): [(3, 0), (5, 0), (4, 1)], (5, 0): [(4, 0), (5, 1)],
                        (3, 1): [(3, 0), (3, 2), (4, 1)], (4, 1): [(4, 0), (3, 1), (4, 2), (5, 1)],
                        (5, 1): [(5, 0), (5, 2), (4, 1)],
                        (3, 2): [(3, 1), (4, 2)], (4, 2): [(3, 2), (5, 2), (4, 1)], (5, 2): [(4, 2), (5, 1)]}
        red_palace = {(3, 9): [(4, 9), (3, 8)], (4, 9): [(3, 9), (5, 9), (4, 8)], (5, 9): [(4, 9), (5, 8)],
                      (3, 8): [(3, 9), (4, 8), (3, 7)], (4, 8): [(4, 9), (3, 8), (5, 8), (4, 7)],
                      (5, 8): [(5, 9), (4, 8), (5, 7)],
                      (3, 7): [(3, 8), (4, 7)], (4, 7): [(4, 8), (3, 7), (5, 7)], (5, 7): [(5, 8), (4, 7)]}
        palaces = {Camp.BLACK: black_palace, Camp.RED: red_palace}
        palace = palaces[self.camp]
        assert (self.col, self.row) in palace
        test_pos = palace[(self.col, self.row)]
        pos = []
        for c, r in test_pos:
            p = board_.piece_at(c, r)
            if p is None or p.camp != self.camp:
                if not self.meet_enemy_shuai(board_, c, r):
                    pos.append((c, r))
        return pos

    def meet_enemy_shuai(self, board_, col, row):
        enemy_shuai = board_.get_shuai(self.camp.opponent())
        assert enemy_shuai is not None
        if enemy_shuai.col != col:
            return False
        lb, ub = min(row, enemy_shuai.row), max(row, enemy_shuai.row)
        for r in range(lb + 1, ub - 1):  # have any piece in between
            p = board_.piece_at(col, r)
            if p is not None:
                return False
        return True


def test_can_move():
    from board import Board, N_COLS, N_ROWS
    from constants import FULL_BOARD
    col, row = 4, 8
    camp = Camp.RED
    p = Shuai(camp, col, row)
    situation = [p, Shuai(Camp.BLACK, 3, 0)]
    board = Board(situation)
    print(board)
    p = board.piece_at(col, row)
    assert p.camp == camp
    assert p.force == Force.SHUAI

    valid = []
    for c in range(N_COLS):
        for r in range(N_ROWS):
            yes = p.can_move(board, c, r)
            if yes:
                valid.append((c, r))
    print((col, row), valid)
    situation = [p]
    for c, r in valid:
        p = Shuai(camp.opponent(), c, r)
        situation.append(p)
    board = Board(situation)
    print(board)


if __name__ == '__main__':
    test_can_move()
