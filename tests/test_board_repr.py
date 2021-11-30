import unittest
import sys
sys.path.append('src')

from force import *
from board import Board
from constants import FULL_BOARD


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
        arr = np.array([[1500, 1410, 1320, 1230, 1140, 1250, 1360, 1470, 1580],
                        [0,    0,    0,    0,    0,    0,    0,    0,    0],
                        [0, 1612,    0,    0,    0,    0,    0, 1672,    0],
                        [1703,    0, 1723,    0, 1743,    0, 1763,    0, 1783],
                        [0,    0,    0,    0,    0,    0,    0,    0,    0],
                        [0,    0,    0,    0,    0,    0,    0,    0,    0],
                        [2706,    0, 2726,    0, 2746,    0, 2766,    0, 2786],
                        [0, 2617,    0,    0,    0,    0,    0, 2677,    0],
                        [0,    0,    0,    0,    0,    0,    0,    0,    0],
                        [2509, 2419, 2329, 2239, 2149, 2259, 2369, 2479, 2589]],
                       dtype=np.int32)
        board = Board(arr)
        arr1 = board.encode()
        self.assertTrue((arr == arr1).all())
