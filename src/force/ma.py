from piece import Force
from piece import Piece


class Ma(Piece):
    def __init__(self, camp, col, row):
        super().__init__(camp, Force.MA, col, row)

    def can_move(self, board_, col, row):
        from board import N_COLS, N_ROWS
        assert 0 <= col < N_COLS
        assert 0 <= row < N_ROWS
        pos = self.get_valid_pos(board_)
        return (col, row) in pos

    def traverse(self, col):
        raise ValueError('cannot do this')

    def advance(self, col):
        col, _ = self.with_my_view(col, None)
        d = abs(self.col - col)
        assert d == 1 or d == 2
        return col, self.row + self.heading * (3 - d)

    def retreat(self, col):
        col, _ = self.with_my_view(col, None)
        d = abs(self.col - col)
        assert d == 1 or d == 2
        return col, self.row - self.heading * (3 - d)

    def get_valid_pos(self, board_):
        test_pos = [(+2, +1), (+2, -1), (-2, +1), (-2, -1), (+1, +2), (+1, -2), (-1, +2), (-1, -2)]
        handicap = [(+1, 0), (+1, 0), (-1, 0), (-1, 0), (0, +1), (0, -1), (0, +1), (0, -1)]
        poses = []
        for pos, handi in zip(test_pos, handicap):
            handi_p = board_.piece_at(self.col + handi[0], self.row + handi[1])
            if handi_p is not None:
                continue
            col, row = self.col + pos[0], self.row + pos[1]
            p = board_.piece_at(col, row)
            if p is None or p.camp != self.camp:
                poses.append((col, row))
        return poses


def test_can_move():
    from board import Board, N_COLS, N_ROWS
    from piece import Camp
    from constants import well_known_4

    col, row = 3, 4
    camp = Camp.RED
    board = Board(well_known_4)
    print(board)
    p = board.piece_at(col, row)
    assert p.camp == camp
    assert p.force == Force.MA

    valid = []
    for c in range(N_COLS):
        for r in range(N_ROWS):
            yes = p.can_move(board, c, r)
            if yes:
                valid.append((c, r))
    print((col, row), valid)
    situation = [p]
    for c, r in valid:
        p = Ma(camp.opponent(), c, r)
        situation.append(p)
    board = Board(situation)
    print(board)


if __name__ == '__main__':
    test_can_move()