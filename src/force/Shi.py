from board import Piece
from board import Force


class Shi(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.SHI)

    def can_move(self, board, dx, dy):
        return False
