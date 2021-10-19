from board import Piece
from board import Force


class Ma(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.MA)

    def can_move(self, board_, col, row):
        from board import N_COLS, N_ROWS
        assert 0 <= col < N_COLS
        assert 0 <= row < N_ROWS

    def traverse(self, col):
        raise ValueError('cannot do this')

    def advance(self, col):
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 1 or d == 2
        return col, self.row + self.heading * (3 - d)

    def retreat(self, col):
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 1 or d == 2
        return col, self.row - self.heading * (3 - d)

    def get_valid_pos(self, board_):
        from board import N_COLS, N_ROWS
        test_pos = [(+2, +1), (+2, -1), (-2, +1), (-2, -1), (+1, +2), (+1, -2), (-1, +2), (-1, -2)]
        handicap = [(+1, 0), (+1, 0), (-1, 0), (-1, 0), (0, +1), (0, -1), (0, +1), (0, -1)]
        pos = []

        return pos
