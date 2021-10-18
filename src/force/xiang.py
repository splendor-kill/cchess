from board import Piece
from board import Force


class Xiang(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.XIANG)

    def can_move(self, board_, action, act_param):
        return False

    def traverse(self, col):
        raise ValueError('cannot do this')

    def advance(self, col):
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 2
        row = self.row + self.heading * 2
        assert row < 5
        return col, row

    def retreat(self, col):
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 2
        row = self.row - self.heading * 2
        return col, row
