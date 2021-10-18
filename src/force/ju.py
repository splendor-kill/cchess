from board import Piece
from board import Force


class Ju(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.JU)

    def can_move(self, board_, action, act_param):
        return False

    def traverse(self, col):
        assert 1 <= col <= 9
        col -= 1  # convert to 0-based
        assert self.col != col
        return col, self.row

    def advance(self, d):
        assert self.row + d < 9
        return self.col, self.row + self.heading * d

    def retreat(self, d):
        assert self.row - d > 0
        return self.col, self.row - self.heading * d
