from board import Piece
from board import Force


class Pao(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.PAO)

    def can_move(self, board, dx, dy):
        return False

    def traverse(self, col):
        assert 1 <= col <= 9
        assert self.col != col
        self.col = col

    def advance(self, d):
        assert self.row + d < 9
        self.row += d

    def retreat(self, d):
        assert self.row - d > 0
        self.row -= d
