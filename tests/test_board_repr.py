import unittest
import sys
sys.path.append('src')

from force import *
from board import Board
from constants import FULL_BOARD
from env import Env


class ReprFenTest(unittest.TestCase):
    def test1(self):
        fen1 = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'
        board = Board(fen1)
        fen1_ = board.board_to_fen1()
        self.assertEqual(fen1, fen1_)
        board1 = Board(FULL_BOARD)
        self.assertEqual(str(board1), str(board))

    def test2(self):
        fen1 = '9/9/3k5/9/9/9/4R4/3A5/8r/4K4'
        board = Board(fen1)
        fen1_ = board.board_to_fen1()
        self.assertEqual(fen1, fen1_)


class ReprNumpyArrayTest(unittest.TestCase):
    def test1(self):
        import numpy as np
        arr = np.array([[15, 14, 13, 12, 11, 12, 13, 14, 15],
                        [0,  0,  0,  0,  0,  0,  0,  0,  0],
                        [0, 16,  0,  0,  0,  0,  0, 16,  0],
                        [17,  0, 17,  0, 17,  0, 17,  0, 17],
                        [0,  0,  0,  0,  0,  0,  0,  0,  0],
                        [0,  0,  0,  0,  0,  0,  0,  0,  0],
                        [27,  0, 27,  0, 27,  0, 27,  0, 27],
                        [0, 26,  0,  0,  0,  0,  0, 26,  0],
                        [0,  0,  0,  0,  0,  0,  0,  0,  0],
                        [25, 24, 23, 22, 21, 22, 23, 24, 25]],
                       dtype=np.int32)
        board = Board(arr)
        arr1 = board.encode()
        self.assertTrue((arr == arr1).all())


class EnvFenTest(unittest.TestCase):
    def test1(self):
        fen = '9/9/3k5/9/9/9/4R4/3A5/8r/4K4 b - - 0 1'
        env = Env.from_fen(fen)
        fen1 = env.to_fen()
        self.assertEqual(fen, fen1)

    def test2(self):
        fen = '9/9/3k5/9/9/9/4R4/3A5/4K4/8r b - - 0 1 moves i0i1 e1e0 i1i0 e0e1 i0i1 e1e0 i1i0 e0e1 i0i1 e1e0'
        env = Env.from_fen(fen)
        fen1 = env.to_fen()
        parts = fen1.split()
        eres = '9/9/3k5/9/9/9/4R4/3A5/8r/4K4'
        self.assertEqual(eres, parts[0])
