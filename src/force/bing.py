from piece import Force
from piece import Piece


class Bing(Piece):
    def __init__(self, camp, col, row):
        super().__init__(camp, Force.BING, col, row)

    def traverse(self, col):
        col, row = self.with_my_view(col, self.row)
        assert abs(self.col - col) == 1
        assert 4 < row <= 9
        return col, self.row

    def advance(self, d):
        assert d == 1
        return self.col, self.row + self.heading * 1

    def retreat(self, d):
        raise ValueError('cannot do this')

    def is_cross_river(self):
        col, row = self.with_my_view()
        return row > 4

    def get_valid_pos(self, board_):
        test_pos = [(0, 1)]
        if self.is_cross_river():
            test_pos.extend([(1, 0), (-1, 0)])
        poses = []
        for pos in test_pos:
            col, row = self.col + pos[0], self.row + self.heading * pos[1]
            p = board_.piece_at(col, row)
            if p is None or p.camp != self.camp:
                if not self.will_cause_shuai_meet(board_, col, row):
                    poses.append((col, row))
        return poses


def test_can_move():
    from board import Board, N_COLS, N_ROWS
    from piece import Camp
    from force.shuai import Shuai
    col, row = 4, 8
    camp = Camp.BLACK
    p = Bing(camp, col, row)
    situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 4, 0), p]
    board = Board(situation)
    valid = []
    for c in range(N_COLS):
        for r in range(N_ROWS):
            yes = p.can_move(board, c, r)
            if yes:
                valid.append((c, r))
    print((col, row), valid)
    situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 4, 0), p]
    for c, r in valid:
        p = Bing(camp.opponent(), c, r)
        situation.append(p)
    board = Board(situation)
    print(board)


if __name__ == '__main__':
    test_can_move()
