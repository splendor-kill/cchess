from board import Piece
from board import Force


class Pao(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.PAO)

    def can_move(self, board, dx, dy):
        return False

    def traverse(self, col):
        assert 1 <= col <= 9
        col -= 1  # convert to 0-based
        assert self.col != col
        return col, self.row

    def advance(self, d):
        row = self.row + self.heading * d
        assert row < 9
        return self.col, row

    def retreat(self, d):
        row = self.row - self.heading * d
        assert row > 0
        return self.col, row
