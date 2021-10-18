from board import Piece
from board import Force


class Shi(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.SHI)

    def can_move(self, board_, action, act_param):
        return False

    def traverse(self, col):
        raise ValueError('cannot do this')

    def advance(self, col):
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 1
        return col, self.row + self.heading * 1

    def retreat(self, col):
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 1
        return col, self.row - self.heading * 1
