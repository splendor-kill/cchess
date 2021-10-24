import unittest

from board import Board, N_COLS, N_ROWS
from force import *
from piece import Camp, Force


class JuTest(unittest.TestCase):
    def test_can_move1(self):
        col, row = 3, 6
        camp = Camp.RED
        p = Ju(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(17, len(valid))

    def test_can_move2(self):
        col, row = 4, 6
        camp = Camp.BLACK
        p = Ju(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(17, len(valid))

    def test_can_move3(self):
        col, row = 8, 9
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.JU)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(2, len(valid))
        self.assertSetEqual({(8, 7), (8, 8)}, set(valid))

    def test_can_move4(self):
        col, row = 6, 9
        camp = Camp.BLACK
        from constants import well_known_2
        board = Board(well_known_2)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.JU)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(0, len(valid))

    def test_can_move5(self):
        col, row = 4, 1
        camp = Camp.RED
        from constants import well_known_3
        board = Board(well_known_3)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.JU)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(8, len(valid))
        self.assertSetEqual({(2, 1), (3, 1), (4, 0), (4, 2), (5, 1), (6, 1), (7, 1), (8, 1)}, set(valid))

    def test_can_move6(self):
        col, row = 5, 8
        camp = Camp.RED
        from constants import well_known_4
        board = Board(well_known_4)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.JU)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(6, len(valid))
        self.assertSetEqual({(5, 7), (5, 6), (5, 5), (6, 8), (7, 8), (8, 8)}, set(valid))

    def test_can_move7(self):
        col, row = 4, 6
        camp = Camp.RED
        p = Ju(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 4, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(8, len(valid))


class MaTest(unittest.TestCase):
    def test_can_move1(self):
        col, row = 4, 6
        camp = Camp.RED
        p = Ma(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(8, len(valid))

    def test_can_move2(self):
        col, row = 7, 9
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        p = board.piece_at(6, 9)  # Xiang
        board.throw_away(p)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.MA)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(3, len(valid))
        self.assertSetEqual({(6, 7), (8, 7), (5, 8)}, set(valid))

    def test_can_move3(self):
        col, row = 7, 9
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.MA)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(2, len(valid))
        self.assertSetEqual({(6, 7), (8, 7)}, set(valid))

    def test_can_move4(self):
        col, row = 4, 9
        camp = Camp.BLACK
        from constants import well_known_2
        board = Board(well_known_2)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.MA)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(0, len(valid))

    def test_can_move5(self):
        from constants import well_known_4
        col, row = 3, 4
        camp = Camp.RED
        board = Board(well_known_4)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.MA)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(5, len(valid))
        self.assertSetEqual({(1, 3), (1, 5), (2, 2), (4, 2), (4, 6)}, set(valid))

    def test_can_move6(self):
        from constants import well_known_4
        col, row = 5, 0
        camp = Camp.BLACK
        board = Board(well_known_4)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.MA)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(2, len(valid))
        self.assertSetEqual({(6, 2), (7, 1)}, set(valid))

    def test_can_move7(self):
        col, row = 4, 6
        camp = Camp.RED
        p = Ma(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 4, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(0, len(valid))


class XiangTest(unittest.TestCase):
    def test_can_move1(self):
        col, row = 4, 7
        camp = Camp.RED
        p = Xiang(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(4, len(valid))
        self.assertSetEqual({(6, 5), (2, 5), (2, 9), (6, 9)}, set(valid))

    def test_can_move2(self):
        col, row = 6, 9
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        p = board.piece_at(7, 7)  # Pao
        p.move_to(board, 7, 8)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.XIANG)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(1, len(valid))
        self.assertSetEqual({(4, 7)}, set(valid))

    def test_can_move3(self):
        col, row = 6, 9
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.XIANG)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(2, len(valid))
        self.assertSetEqual({(4, 7), (8, 7)}, set(valid))

    def test_can_move4(self):
        col, row = 6, 0
        camp = Camp.BLACK
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.XIANG)
        p.move_to(board, 6, 4)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(2, len(valid))
        self.assertSetEqual({(4, 2), (8, 2)}, set(valid))

    def test_can_move5(self):
        col, row = 8, 7
        camp = Camp.RED
        from constants import well_known_2
        board = Board(well_known_2)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.XIANG)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(1, len(valid))
        self.assertEqual((6, 5), valid[0])

    def test_can_move6(self):
        col, row = 8, 7
        camp = Camp.RED
        from constants import well_known_2
        board = Board(well_known_2)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.XIANG)
        board.throw_away(board.piece_at(7, 8))
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(2, len(valid))
        self.assertSetEqual({(6, 5), (6, 9)}, set(valid))

    def test_can_move7(self):
        col, row = 4, 7
        camp = Camp.RED
        p = Xiang(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 4, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(0, len(valid))


class ShiTest(unittest.TestCase):
    def test_can_move1(self):
        col, row = 3, 9
        camp = Camp.RED
        p = Shi(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(1, len(valid))
        self.assertSetEqual({(4, 8)}, set(valid))

    def test_can_move2(self):
        col, row = 4, 1
        camp = Camp.BLACK
        p = Shi(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(3, len(valid))
        self.assertSetEqual({(5, 0), (3, 2), (5, 2)}, set(valid))

    def test_can_move3(self):
        col, row = 5, 9
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        p = board.piece_at(4, 9)  # Shuai
        p.move_to(board, 4, 8)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.SHI)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(0, len(valid))

    def test_can_move4(self):
        col, row = 4, 8
        camp = Camp.RED
        p = Shi(camp, col, row)
        situation = [p, Pao(Camp.RED, 5, 7), Pao(Camp.BLACK, 5, 9), Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0)]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(3, len(valid))
        self.assertSetEqual({(3, 7), (3, 9), (5, 9)}, set(valid))

    def test_can_move5(self):
        col, row = 4, 8
        camp = Camp.RED
        p = Shi(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 4, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(0, len(valid))


class ShuaiTest(unittest.TestCase):
    def test_can_move1(self):
        col, row = 4, 9
        camp = Camp.RED
        p = Shuai(camp, col, row)
        situation = [p, Shuai(Camp.BLACK, 3, 0), Bing(Camp.RED, 3, 4)]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(3, len(valid))
        self.assertSetEqual({(4, 8), (3, 9), (5, 9)}, set(valid))

    def test_can_move2(self):
        col, row = 4, 8
        camp = Camp.RED
        p = Shuai(camp, col, row)
        situation = [p, Shuai(Camp.BLACK, 3, 0)]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(3, len(valid))
        self.assertSetEqual({(4, 9), (4, 7), (5, 8)}, set(valid))

    def test_can_move3(self):
        col, row = 4, 9
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        board.throw_away(board.piece_at(5, 0))  # black Shi
        p = board.piece_at(4, 0)  # black Shuai
        p.move_to(board, 5, 0)
        p = board.piece_at(5, 9)  # red Shi
        p.move_to(board, 4, 8)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.SHUAI)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(0, len(valid))

    def test_can_move4(self):
        col, row = 3, 9
        camp = Camp.RED
        p = Shuai(camp, col, row)
        situation = [p, Shuai(Camp.BLACK, 4, 0), Bing(Camp.RED, 3, 4)]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(1, len(valid))
        self.assertSetEqual({(3, 8)}, set(valid))


class PaoTest(unittest.TestCase):
    def test_can_move1(self):
        col, row = 4, 6
        camp = Camp.RED
        p = Pao(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(16, len(valid))

    def test_can_move2(self):
        col, row = 4, 6
        camp = Camp.BLACK
        p = Pao(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(16, len(valid))

    def test_can_move3(self):
        col, row = 7, 7
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.PAO)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(12, len(valid))
        self.assertSetEqual(
            {(2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 0), (7, 3), (7, 4), (7, 5), (7, 6), (7, 8), (8, 7)},
            set(valid))

    def test_can_move31(self):
        col, row = 7, 7
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.PAO)
        p.move_to(board, 4, 7)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(8, len(valid))
        self.assertSetEqual(
            {(2, 7), (3, 7), (4, 3), (4, 8), (5, 7), (6, 7), (7, 7), (8, 7)},
            set(valid))

    def test_can_move4(self):
        col, row = 5, 8
        camp = Camp.BLACK
        from constants import well_known_2
        board = Board(well_known_2)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.PAO)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(0, len(valid))

    def test_can_move5(self):
        col, row = 0, 0
        camp = Camp.BLACK
        from constants import well_known_3
        board = Board(well_known_3)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.PAO)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(10, len(valid))
        self.assertSetEqual({(1, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)},
                            set(valid))

    def test_can_move6(self):
        col, row = 4, 5
        camp = Camp.BLACK
        from constants import well_known_5
        board = Board(well_known_5)
        p = board.piece_at(col, row)
        self.assertEqual(p.camp, camp)
        self.assertEqual(p.force, Force.PAO)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(5, len(valid))
        self.assertSetEqual({(3, 5), (4, 4), (4, 6), (4, 8), (6, 5)}, set(valid))

    def test_can_move7(self):
        col, row = 4, 7
        camp = Camp.BLACK
        p = Pao(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 4, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(7, len(valid))


class BingTest(unittest.TestCase):
    def test_can_move1(self):
        col, row = 4, 6
        camp = Camp.RED
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(1, len(valid))
        self.assertEqual((4, 5), valid[0])

    def test_can_move2(self):
        col, row = 4, 4
        camp = Camp.RED
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(3, len(valid))
        self.assertSetEqual({(4, 3), (3, 4), (5, 4)}, set(valid))

    def test_can_move3(self):
        col, row = 0, 6
        camp = Camp.RED
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(1, len(valid))
        self.assertEqual((0, 5), valid[0])

    def test_can_move4(self):
        col, row = 0, 4
        camp = Camp.RED
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(2, len(valid))
        self.assertSetEqual({(0, 3), (1, 4)}, set(valid))

    def test_can_move5(self):
        col, row = 8, 0
        camp = Camp.RED
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(1, len(valid))
        self.assertEqual((7, 0), valid[0])

    def test_can_move6(self):
        col, row = 4, 6
        camp = Camp.BLACK
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(3, len(valid))
        self.assertSetEqual({(3, 6), (4, 7), (5, 6)}, set(valid))

    def test_can_move7(self):
        col, row = 4, 4
        camp = Camp.BLACK
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(1, len(valid))
        self.assertSetEqual({(4, 5)}, set(valid))

    def test_can_move8(self):
        col, row = 0, 6
        camp = Camp.BLACK
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(2, len(valid))
        self.assertSetEqual({(0, 7), (1, 6)}, set(valid))

    def test_can_move9(self):
        col, row = 0, 4
        camp = Camp.BLACK
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(1, len(valid))
        self.assertSetEqual({(0, 5)}, set(valid))

    def test_can_move10(self):
        col, row = 4, 9
        camp = Camp.BLACK
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(2, len(valid))
        self.assertSetEqual({(3, 9), (5, 9)}, set(valid))

    def test_can_move11(self):
        col, row = 4, 4
        camp = Camp.RED
        p = Bing(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 4, 0), p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(1, len(valid))
        self.assertSetEqual({(4, 3)}, set(valid))


if __name__ == '__main__':
    unittest.main()
