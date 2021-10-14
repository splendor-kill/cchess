from board import Piece
from board import Force


class Shuai(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.SHUAI)

    def can_move(self, board, dx, dy):
        return False

    def traverse(self, col):
        assert col in (4, 5, 6)
        d = abs(self.col - col)
        assert d == 1
        self.col = col

    def advance(self, x):
        assert self.row + 1 < 3
        self.row += 1

    def retreat(self, x):
        assert self.row - 1 > 0
        self.row -= 1
