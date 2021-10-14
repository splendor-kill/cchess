from board import Piece
from board import Force


class Xiang(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.XIANG)

    def can_move(self, board, dx, dy):
        return False

    def traverse(self, col):
        raise ValueError('cannot do this')

    def advance(self, col):
        d = abs(self.col - col)
        assert d == 2
        self.row += 2
        assert self.row < 5
        self.col = col

    def retreat(self, col):
        d = abs(self.col - col)
        assert d == 2
        self.row -= 2
        self.col = col
