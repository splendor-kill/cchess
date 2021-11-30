import unittest
import sys
sys.path.append('src')

from force import *
from board import Board
from constants import FULL_BOARD


class FenTest(unittest.TestCase):
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
