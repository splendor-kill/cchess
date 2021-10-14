from board import Piece
from board import Force


class Ma(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.MA)

    def can_move(self, board, dx, dy):
        return False

    def traverse(self, col):
        raise ValueError('cannot do this')

    def advance(self, col):
        d = abs(self.col - col)
        assert d == 1 or d == 2
        self.row += 3 - d
        self.col = col

    def retreat(self, col):
        d = abs(self.col - col)
        assert d == 1 or d == 2
        self.row -= 3 - d
        self.col = col
