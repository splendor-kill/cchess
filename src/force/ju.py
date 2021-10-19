from board import Piece
from board import Force


class Ju(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.JU)

    def can_move(self, board_, col, row):
        from board import N_COLS, N_ROWS
        assert 0 <= col < N_COLS
        assert 0 <= row < N_ROWS

        pos = self.get_valid_pos(board_)
        return (col, row) in pos

    def traverse(self, col):
        assert 1 <= col <= 9
        col -= 1  # convert to 0-based
        assert self.col != col
        return col, self.row

    def advance(self, d):
        assert self.row + d < 9
        return self.col, self.row + self.heading * d

    def retreat(self, d):
        assert self.row - d > 0
        return self.col, self.row - self.heading * d

    def get_valid_pos(self, board_):
        from board import N_COLS, N_ROWS
        pos = []
        for r in range(self.row + 1, N_ROWS):  # to bottom
            p = board_.piece_at(self.col, r)
            if p is not None:
                if p.camp != self.camp:
                    pos.append((self.col, r))
                break
            pos.append((self.col, r))
        for r in range(self.row - 1, -1, -1):  # to top
            p = board_.piece_at(self.col, r)
            if p is not None:
                if p.camp != self.camp:
                    pos.append((self.col, r))
                break
            pos.append((self.col, r))
        for c in range(self.col + 1, N_COLS):  # to right
            p = board_.piece_at(c, self.row)
            if p is not None:
                if p.camp != self.camp:
                    pos.append((self.col, r))
                break
            pos.append((c, self.row))
        for c in range(self.col - 1, -1, -1):  # to left
            p = board_.piece_at(c, self.row)
            if p is not None:
                if p.camp != self.camp:
                    pos.append((self.col, r))
                break
            pos.append((c, self.row))
        return pos


def test_can_move():
    from board import Board, N_COLS, N_ROWS
    from piece import Camp
    col, row = 4, 1
    camp = Camp.RED
    from constants import well_known_3
    board = Board(well_known_3)
    p = board.piece_at(col, row)
    assert p.camp == camp
    assert p.force == Force.JU

    valid = []
    for c in range(N_COLS):
        for r in range(N_ROWS):
            yes = p.can_move(board, c, r)
            if yes:
                valid.append((c, r))
    print((col, row), valid)
    situation = [p]
    for c, r in valid:
        p = Ju(r, c, camp.opponent())
        situation.append(p)
    board = Board(situation)
    print(board)


if __name__ == '__main__':
    test_can_move()
