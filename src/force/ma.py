from board import Piece
from board import Force


class Ma(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.MA)

    def can_move(self, board_, action, act_param):
        return False

    def traverse(self, col):
        raise ValueError('cannot do this')

    def advance(self, col):
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 1 or d == 2
        return col, self.row + self.heading * (3 - d)

    def retreat(self, col):
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 1 or d == 2
        return col, self.row - self.heading * (3 - d)
