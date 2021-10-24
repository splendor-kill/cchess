import unittest

from board import Board
from force import *
from piece import Camp


class ShuaiMeetTest(unittest.TestCase):
    def test1(self):
        red = Shuai(Camp.RED, 4, 9)
        black = Shuai(Camp.BLACK, 4, 0)
        situation = [red, black]
        board = Board(situation)
        meet = board.check_if_shuai_meet((red.col, red.row), (black.col, black.row))
        self.assertTrue(meet)

    def test2(self):
        red = Shuai(Camp.RED, 4, 9)
        black = Shuai(Camp.BLACK, 4, 0)
        p = Ma(Camp.RED, 4, 4)
        situation = [red, black, p]
        board = Board(situation)
        meet = board.check_if_shuai_meet((red.col, red.row), (black.col, black.row))
        self.assertFalse(meet)
        meet = board.check_if_shuai_meet((red.col, red.row), (black.col, black.row), ignore_piece=p)
        self.assertTrue(meet)

    def test3(self):
        red = Shuai(Camp.RED, 4, 9)
        black = Shuai(Camp.BLACK, 4, 0)
        p = Ma(Camp.RED, 4, 4)
        p2 = Xiang(Camp.BLACK, 4, 2)
        situation = [red, black, p, p2]
        board = Board(situation)
        meet = board.check_if_shuai_meet((red.col, red.row), (black.col, black.row))
        self.assertFalse(meet)
        meet = board.check_if_shuai_meet((red.col, red.row), (black.col, black.row), ignore_piece=p)
        self.assertFalse(meet)

    def test4(self):
        red = Shuai(Camp.RED, 4, 9)
        black = Shuai(Camp.BLACK, 4, 0)
        p = Ma(Camp.RED, 3, 4)
        p2 = Pao(Camp.RED, 4, 7)
        situation = [red, black, p, p2]
        board = Board(situation)
        meet = board.check_if_shuai_meet((red.col, red.row), (black.col, black.row))
        self.assertFalse(meet)
        meet = board.check_if_shuai_meet((red.col, red.row), (black.col, black.row), ignore_piece=p)
        self.assertFalse(meet)
        meet = board.check_if_shuai_meet((red.col, red.row), (black.col, black.row), ignore_piece=p2)
        self.assertTrue(meet)


if __name__ == '__main__':
    unittest.main()
