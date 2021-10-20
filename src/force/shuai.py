from piece import Force
from piece import Piece


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

    def get_valid_pos(self, board_):
        black_palace = {(3, 0), (4, 0), (5, 0),
                        (3, 1), (4, 1), (5, 1),
                        (3, 2), (4, 2), (5, 2)}
        red_palace = [(3, 9), (4, 9), (5, 9),
                      (3, 8), (4, 8), (5, 8),
                      (3, 7), (4, 7), (5, 7)]
