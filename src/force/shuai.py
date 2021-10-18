from board import Piece
from board import Force


class Shuai(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.SHUAI)

    def can_move(self, board_, action, act_param):
        return False

    def traverse(self, col):
        assert col in (4, 5, 6)
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 1
        return col, self.row

    def advance(self, x):
        assert self.row + 1 < 3
        return self.col, self.row + self.heading * 1

    def retreat(self, x):
        assert self.row - 1 > 0
        return self.col, self.row - self.heading * 1
