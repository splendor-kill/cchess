import unittest
import sys
sys.path.append('src')

from board import Board
from force import *
from piece import Camp


class ShuaiMeetTest(unittest.TestCase):
    def test1(self):
        red = Shuai(Camp.RED, 4, 9)
        black = Shuai(Camp.BLACK, 4, 0)
        situation = [red, black]
        board = Board(situation)
        meet = board.test_shuai_meet((red.col, red.row), (black.col, black.row))
        self.assertTrue(meet)

    def test2(self):
        red = Shuai(Camp.RED, 4, 9)
        black = Shuai(Camp.BLACK, 4, 0)
        p = Ma(Camp.RED, 4, 4)
        situation = [red, black, p]
        board = Board(situation)
        meet = board.test_shuai_meet((red.col, red.row), (black.col, black.row))
        self.assertFalse(meet)
        meet = board.test_shuai_meet((red.col, red.row), (black.col, black.row), ignore_piece=p)
        self.assertTrue(meet)

    def test3(self):
        red = Shuai(Camp.RED, 4, 9)
        black = Shuai(Camp.BLACK, 4, 0)
        p = Ma(Camp.RED, 4, 4)
        p2 = Xiang(Camp.BLACK, 4, 2)
        situation = [red, black, p, p2]
        board = Board(situation)
        meet = board.test_shuai_meet((red.col, red.row), (black.col, black.row))
        self.assertFalse(meet)
        meet = board.test_shuai_meet((red.col, red.row), (black.col, black.row), ignore_piece=p)
        self.assertFalse(meet)

    def test4(self):
        red = Shuai(Camp.RED, 4, 9)
        black = Shuai(Camp.BLACK, 4, 0)
        p = Ma(Camp.RED, 3, 4)
        p2 = Pao(Camp.RED, 4, 7)
        situation = [red, black, p, p2]
        board = Board(situation)
        meet = board.test_shuai_meet((red.col, red.row), (black.col, black.row))
        self.assertFalse(meet)
        meet = board.test_shuai_meet((red.col, red.row), (black.col, black.row), ignore_piece=p)
        self.assertFalse(meet)
        meet = board.test_shuai_meet((red.col, red.row), (black.col, black.row), ignore_piece=p2)
        self.assertTrue(meet)

    def test5(self):
        situation = '''
        ＋－＋－＋－＋－將－＋－象－＋－＋
        ｜　｜　｜　｜＼｜／｜　｜　｜　｜
        ＋－＋－傌－＋－士－＋－＋－＋－＋
        ｜　｜　｜　｜／｜＼｜　｜　｜　｜
        ＋－＋－＋－＋－象－士－＋－＋－＋
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－＋－＋－＋－＋－＋－＋－＋
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－＋－＋－＋－＋－＋－＋－＋
        ＋－＋－相－＋－馬－＋－＋－＋－＋
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－＋－＋－＋－＋－＋－＋－＋
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－＋－＋－＋－＋－＋－＋－＋
        ｜　｜　｜　｜＼｜／｜　｜　｜　｜
        ＋－＋－＋－＋－＋－＋－＋－＋－＋
        ｜　｜　｜　｜／｜＼｜　｜　｜　｜
        ＋－＋－＋－帥－＋－＋－＋－＋－＋
        '''
        board = Board(situation)
        black_shuai = board.piece_at(4, 0)
        shuai1 = board.get_shuai(Camp.BLACK)
        self.assertIsNotNone(shuai1)
        self.assertTrue(shuai1 is black_shuai)


class CheckTest(unittest.TestCase):
    def test1(self):
        rshuai = Shuai(Camp.RED, 4, 9)
        rma = Ma(Camp.RED, 4, 4)
        rpao = Pao(Camp.RED, 4, 7)
        bshuai = Shuai(Camp.BLACK, 4, 0)
        bshi = Shi(Camp.BLACK, 4, 1)
        situation = [rshuai, rma, rpao, bshuai, bshi]
        board = Board(situation)
        check = board.test_check(Camp.RED)
        self.assertFalse(check)
        rma.move_to(board, 5, 2)
        check = board.test_check(Camp.RED)
        self.assertTrue(check)
        board.throw_away(rma)
        bshi.move_to(board, rma.col, rma.row)
        check = board.test_check(Camp.RED)
        self.assertFalse(check)


class FinalValidActionsTest(unittest.TestCase):
    def test1(self):
        rshuai = Shuai(Camp.RED, 4, 9)
        rma = Ma(Camp.RED, 4, 4)
        rpao = Pao(Camp.RED, 4, 7)
        bshuai = Shuai(Camp.BLACK, 4, 0)
        bshi = Shi(Camp.BLACK, 4, 1)
        bju = Ju(Camp.BLACK, 1, 9)
        situation = [rshuai, rma, rpao, bshuai, bshi, bju]
        board = Board(situation)
        board.checked[Camp.RED] = True
        actions = board.get_valid_actions(Camp.RED)
        self.assertEqual(23, len(actions))
        actions = board.get_final_valid_actions(Camp.RED)
        self.assertEqual(1, len(actions))

    def test2(self):
        rshuai = Shuai(Camp.RED, 4, 9)
        rma = Ma(Camp.RED, 4, 4)
        rpao = Pao(Camp.RED, 4, 7)
        rshi = Shi(Camp.RED, 4, 8)
        bshuai = Shuai(Camp.BLACK, 4, 0)
        bshi = Shi(Camp.BLACK, 4, 1)
        bju = Ju(Camp.BLACK, 1, 9)
        situation = [rshuai, rma, rpao, rshi, bshuai, bshi, bju]
        board = Board(situation)
        board.checked[Camp.RED] = True
        actions = board.get_valid_actions(Camp.RED)
        self.assertEqual(25, len(actions))
        actions = board.get_final_valid_actions(Camp.RED)
        self.assertEqual(1, len(actions))

    def test3(self):
        from constants import kaggle_1
        board = Board(kaggle_1)
        actions = board.get_valid_actions(Camp.BLACK)
        self.assertEqual(32, len(actions))


if __name__ == '__main__':
    unittest.main()
