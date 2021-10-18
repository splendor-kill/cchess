from board import Piece
from board import Force


class Bing(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.BING)

    def can_move(self, board_, col, row):
        dst_p = board_.piece_at(col, row)
        if dst_p is not None and dst_p.camp == self.camp:
            return False

        return False

    def traverse(self, col):
        col -= 1  # convert to 0-based
        assert abs(self.col - col) == 1
        return col, self.row

    def advance(self, d):
        return self.col, self.row + self.heading * 1

    def retreat(self, d):
        raise ValueError('cannot do this')

    def is_cross_river(self):