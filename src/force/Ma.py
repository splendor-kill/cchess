from board import Piece
from board import Force


class Ma(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.MA)

    def can_move(self, board, dx, dy):
        return False
