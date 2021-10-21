from piece import Force
from piece import Piece


class Bing(Piece):
    def __init__(self, camp, col, row):
        super().__init__(camp, Force.BING, col, row)

    def can_move(self, board_, col, row):
        from board import N_COLS, N_ROWS
        assert 0 <= col < N_COLS
        assert 0 <= row < N_ROWS
        dst_p = board_.piece_at(col, row)
        if dst_p is not None and dst_p.camp == self.camp:
            return False
        mycol, myrow = self.with_my_view()
        col, row = self.with_my_view(col, row)

        if self.is_cross_river():
            if col == mycol and row - myrow == 1:
                return True
            if row == myrow and abs(col - mycol) == 1:
                return True
        else:
            return col == mycol and row - myrow == 1
        return False

    def traverse(self, col):
        col, _ = self.with_my_view(col, None)
        assert abs(self.col - col) == 1
        return col, self.row

    def advance(self, d):
        return self.col, self.row + self.heading * 1

    def retreat(self, d):
        raise ValueError('cannot do this')

    def is_cross_river(self):
        col, row = self.with_my_view()
        return row > 4


def test_can_move():
    from board import Board, N_COLS, N_ROWS
    from piece import Camp
    col, row = 4, 9
    camp = Camp.BLACK
    p = Bing(camp, col, row)
    situation = [p]
    board = Board(situation)
    valid = []
    for c in range(N_COLS):
        for r in range(N_ROWS):
            yes = p.can_move(board, c, r)
            if yes:
                valid.append((c, r))
    print((col, row), valid)
    situation = [p]
    for c, r in valid:
        p = Bing(camp.opponent(), c, r)
        situation.append(p)
    board = Board(situation)
    print(board)


if __name__ == '__main__':
    test_can_move()
