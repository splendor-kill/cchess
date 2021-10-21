from piece import Camp, Force
from piece import Piece


class Shi(Piece):
    def __init__(self, camp, col, row):
        super().__init__(camp, Force.SHI, col, row)

    def can_move(self, board_, col, row):
        from board import N_COLS, N_ROWS
        assert 0 <= col < N_COLS
        assert 0 <= row < N_ROWS

        pos = self.get_valid_pos(board_)
        return (col, row) in pos

    def traverse(self, col):
        raise ValueError('cannot do this')

    def advance(self, col):
        col, _ = self.with_my_view(col, None)
        d = abs(self.col - col)
        assert d == 1
        return col, self.row + self.heading * 1

    def retreat(self, col):
        col, _ = self.with_my_view(col, None)
        d = abs(self.col - col)
        assert d == 1
        return col, self.row - self.heading * 1

    def get_valid_pos(self, board_):
        black_palace = {(3, 0): [(4, 1)], (5, 0): [(4, 1)],
                        (4, 1): [(3, 0), (5, 0), (3, 2), (5, 2)],
                        (3, 2): [(4, 1)], (5, 2): [(4, 1)]}
        red_palace = {(3, 9): [(4, 8)], (5, 9): [(4, 8)],
                      (4, 8): [(3, 9), (5, 9), (3, 7), (5, 7)],
                      (3, 7): [(4, 8)], (5, 7): [(4, 8)]}

        palaces = {Camp.BLACK: black_palace, Camp.RED: red_palace}
        palace = palaces[self.camp]
        assert (self.col, self.row) in palace
        test_pos = palace[(self.col, self.row)]
        pos = []
        for c, r in test_pos:
            p = board_.piece_at(c, r)
            if p is None or p.camp != self.camp:
                pos.append((c, r))
        return pos


def test_can_move():
    from board import Board, N_COLS, N_ROWS
    col, row = 3, 9
    camp = Camp.RED
    from constants import FULL_BOARD
    board = Board(FULL_BOARD)
    p = board.piece_at(col, row)
    assert p.camp == camp
    assert p.force == Force.SHI

    valid = []
    for c in range(N_COLS):
        for r in range(N_ROWS):
            yes = p.can_move(board, c, r)
            if yes:
                valid.append((c, r))
    print((col, row), valid)
    situation = [p]
    for c, r in valid:
        p = Shi(camp.opponent(), c, r)
        situation.append(p)
    board = Board(situation)
    print(board)


if __name__ == '__main__':
    test_can_move()
