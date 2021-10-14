from board import Piece
from board import Force


class Bing(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.BING)

    def can_move(self, board, dx, dy):
        return False

    def traverse(self, col):
        assert abs(self.col - col) == 1
        self.col = col

    def advance(self, d):
        self.row += 1

    def retreat(self, d):
        raise ValueError('cannot do this')
