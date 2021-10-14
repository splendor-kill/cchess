from board import Piece
from board import Force


class Shi(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.SHI)

    def can_move(self, board, dx, dy):
        return False

    def traverse(self, col):
        raise ValueError('cannot do this')

    def advance(self, col):
        d = abs(self.col - col)
        assert d == 1
        self.row += 1
        self.col = col

    def retreat(self, col):
        d = abs(self.col - col)
        assert d == 1
        self.row -= 1
        self.col = col
