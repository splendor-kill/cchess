from piece import Force
from piece import Piece


class Xiang(Piece):
    def __init__(self, camp, col, row):
        super().__init__(camp, Force.XIANG, col, row)

    def can_move(self, board_, col, row):
        from board import N_COLS, N_ROWS
        assert 0 <= col < N_COLS
        assert 0 <= row < N_ROWS
        pos = self.get_valid_pos(board_)
        return (col, row) in pos

    def traverse(self, col):
        raise ValueError('cannot do this')

    def advance(self, col):
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 2
        row = self.row + self.heading * 2
        assert row < 5
        return col, row

    def retreat(self, col):
        col -= 1  # convert to 0-based
        d = abs(self.col - col)
        assert d == 2
        row = self.row - self.heading * 2
        return col, row

    def get_valid_pos(self, board_):
        test_pos = [(+2, +2), (+2, -2), (-2, +2), (-2, -2)]
        handicap = [(+1, +1), (+1, -1), (-1, +1), (-1, -1)]
        poses = []

        for pos, handi in zip(test_pos, handicap):
            handi_p = board_.piece_at(self.col + handi[0], self.row + handi[1])
            if handi_p is not None:
                continue
            col, row = self.col + pos[0], self.row + pos[1]
            _, row_in_my_view = self.with_my_view(col, row)
            if row_in_my_view > 4:  # cannot cross river
                continue
            p = board_.piece_at(col, row)
            if p is None or p.camp != self.camp:
                poses.append((col, row))
        return poses


def test_can_move():
    from board import Board, N_COLS, N_ROWS
    from piece import Camp

    col, row = 6, 9
    camp = Camp.RED
    from constants import FULL_BOARD
    board = Board(FULL_BOARD)
    p = board.piece_at(7, 7)  # Pao
    p.move_to(board, 7, 8)
    print(board)
    p = board.piece_at(col, row)
    assert p.camp == camp
    assert p.force == Force.XIANG

    valid = []
    for c in range(N_COLS):
        for r in range(N_ROWS):
            yes = p.can_move(board, c, r)
            if yes:
                valid.append((c, r))
    print((col, row), valid)
    situation = [p]
    for c, r in valid:
        p = Xiang(camp.opponent(), c, r)
        situation.append(p)
    board = Board(situation)
    print(board)


if __name__ == '__main__':
    test_can_move()
