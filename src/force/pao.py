from piece import Force
from piece import Piece


class Pao(Piece):
    def __init__(self, row, col, camp):
        super().__init__(row, col, camp, Force.PAO)

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
        row = self.row + self.heading * d
        assert row < 9
        return self.col, row

    def retreat(self, d):
        row = self.row - self.heading * d
        assert row > 0
        return self.col, row

    def get_valid_pos(self, board_):

        def op_at_row(p, x):
            return p.col, x

        def op_at_col(p, x):
            return x, p.row

        from board import N_COLS, N_ROWS
        poses = []
        ranges = [range(self.row + 1, N_ROWS),  # to bottom
                  range(self.row - 1, -1, -1),  # to top
                  range(self.col + 1, N_COLS),  # to right
                  range(self.col - 1, -1, -1)]  # to left
        ops = [op_at_row, op_at_row, op_at_col, op_at_col]
        for line, op in zip(ranges, ops):
            bed = False
            for x in line:
                c, r = op(self, x)
                p = board_.piece_at(c, r)
                if not bed:
                    if p is None:
                        poses.append((c, r))
                    else:
                        bed = True
                        continue
                else:
                    if p is None:
                        continue
                    if p.camp != self.camp:
                        poses.append((c, r))
                    break
                poses.append((c, r))
        return poses


def test_can_move():
    from board import Board, N_COLS, N_ROWS
    from piece import Camp

    col, row = 4, 5
    camp = Camp.BLACK
    from constants import well_known_5
    board = Board(well_known_5)
    print(board)
    p = board.piece_at(col, row)
    assert p.camp == camp
    assert p.force == Force.PAO

    valid = []
    for c in range(N_COLS):
        for r in range(N_ROWS):
            yes = p.can_move(board, c, r)
            if yes:
                valid.append((c, r))
    print((col, row), valid)
    situation = [p]
    for c, r in valid:
        p = Pao(r, c, camp.opponent())
        situation.append(p)
    board = Board(situation)
    print(board)


if __name__ == '__main__':
    test_can_move()
