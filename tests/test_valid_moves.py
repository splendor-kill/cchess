import logging
import unittest

from board import Board, N_COLS, N_ROWS
from force import *
from piece import Camp, Force


class BingTest(unittest.TestCase):
    def test_can_move1(self):
        col, row = 4, 6
        camp = Camp.RED
        p = Bing(row, col, camp)
        situation = [p]
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
        p = Bing(row, col, camp)
        situation = [p]
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
        p = Bing(row, col, camp)
        situation = [p]
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
        p = Bing(row, col, camp)
        situation = [p]
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
        p = Bing(row, col, camp)
        situation = [p]
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
        p = Bing(row, col, camp)
        situation = [p]
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
        p = Bing(row, col, camp)
        situation = [p]
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
        p = Bing(row, col, camp)
        situation = [p]
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
        p = Bing(row, col, camp)
        situation = [p]
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
        p = Bing(row, col, camp)
        situation = [p]
        board = Board(situation)
        valid = []
        for c in range(N_COLS):
            for r in range(N_ROWS):
                yes = p.can_move(board, c, r)
                if yes:
                    valid.append((c, r))
        self.assertEqual(2, len(valid))
        self.assertSetEqual({(3, 9), (5, 9)}, set(valid))


class JuTest(unittest.TestCase):
    def test_can_move1(self):
        col, row = 4, 6
        camp = Camp.RED
        p = Ju(row, col, camp)
        situation = [p]
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
        p = Ju(row, col, camp)
        situation = [p]
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


if __name__ == '__main__':
    logging.basicConfig()
    unittest.main(verbosity=2)
