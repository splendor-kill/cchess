import unittest

from board import Board, parse_action
from force import *
from piece import Camp, Force


class JuActionTest(unittest.TestCase):
    def test_parse_action1(self):
        cmds = ['车8进8', '车9平9', '车9退1']
        camp = Camp.BLACK
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        for cmd in cmds:
            self.assertRaises(Exception, parse_action, cmd, camp, board)
        p = Ju(camp, 9, 1)
        situation = [p]
        board = Board(situation)
        cmds = ['车9退2', '车9进9']
        for cmd in cmds:
            self.assertRaises(Exception, parse_action, cmd, camp, board)

    def test_parse_action4(self):
        cmds = ['车8平3', '车8进3', '车8退5']
        anss = [(6, 4), (1, 1), (1, 9)]
        camp = Camp.RED
        col, row = 1, 4
        p = Ju(camp, col, row)
        situation = [p]
        board = Board(situation)
        for cmd, ans in zip(cmds, anss):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)

    def test_parse_action6(self):
        cmds = ['前车进2', '前车退2', '前车平2', '后车进2', '后车退2', '后车平2']
        anss = [(3, 3), (3, 7), (7, 5), (3, 4), (3, 8), (7, 6)]
        camp = Camp.RED
        p1 = Ju(camp, 3, 6)
        p2 = Ju(camp, 3, 5)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:3], anss[:3]):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[3:], anss[3:]):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)

    def test_parse_action7(self):
        cmds = ['前车进2', '前车退2', '前车平2', '后车进2', '后车退2', '后车平2']
        anss = [(3, 8), (3, 4), (1, 6), (3, 7), (3, 3), (1, 5)]
        camp = Camp.BLACK
        p1 = Ju(camp, 3, 6)
        p2 = Ju(camp, 3, 5)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:3], anss[:3]):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[3:], anss[3:]):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)


class MaActionTest(unittest.TestCase):
    def test_parse_action1(self):
        cmd = '傌八进七'
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        force, action, act_param, piece, dst = parse_action(cmd, camp, board)
        self.assertEqual(camp, piece.camp)
        self.assertEqual(Force.MA, piece.force)
        self.assertEqual((1, 9), (piece.col, piece.row))
        self.assertEqual((2, 7), dst)

    def test_parse_action2(self):
        cmd = '马8进7'
        camp = Camp.BLACK
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        force, action, act_param, piece, dst = parse_action(cmd, camp, board)
        self.assertEqual(camp, piece.camp)
        self.assertEqual(Force.MA, piece.force)
        self.assertEqual((7, 0), (piece.col, piece.row))
        self.assertEqual((6, 2), dst)

    def test_parse_action3(self):
        cmd = '马8进8'
        camp = Camp.BLACK
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        self.assertRaises(Exception, parse_action, cmd, camp, board)

    def test_parse_action4(self):
        cmds = ['傌六进四', '傌六进五', '傌六进七', '傌六进八', '傌六退四', '傌六退五', '傌六退七', '傌六退八']
        anss = [(5, 5), (4, 4), (2, 4), (1, 5), (5, 7), (4, 8), (2, 8), (1, 7)]
        camp = Camp.RED
        col, row = 3, 6
        p = Ma(camp, col, row)
        situation = [p]
        board = Board(situation)
        for cmd, ans in zip(cmds, anss):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertEqual(camp, piece.camp)
            self.assertEqual(Force.MA, piece.force)
            self.assertEqual((col, row), (piece.col, piece.row))
            self.assertEqual(ans, dst)

    def test_parse_action5(self):
        cmds = ['马5进3', '马5进4', '马5进6', '马5进7', '马5退3', '马5退4', '马5退6', '马5退7']
        anss = [(2, 7), (3, 8), (5, 8), (6, 7), (2, 5), (3, 4), (5, 4), (6, 5)]
        camp = Camp.BLACK
        col, row = 4, 6
        p = Ma(camp, col, row)
        situation = [p]
        board = Board(situation)
        for cmd, ans in zip(cmds, anss):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertEqual(camp, piece.camp)
            self.assertEqual(Force.MA, piece.force)
            self.assertEqual((col, row), (piece.col, piece.row))
            self.assertEqual(ans, dst)

    def test_parse_action6(self):
        cmds = ['前马进5', '前马退8', '后马退7', '后马进5']
        anss = [(4, 3), (1, 6), (2, 8), (4, 4)]
        camp = Camp.RED
        p1 = Ma(camp, 3, 6)
        p2 = Ma(camp, 3, 5)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:2], anss[:2]):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[2:], anss[2:]):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)

    def test_parse_action7(self):
        cmds = ['前马进5', '前马退2', '后马退2', '后马进3']
        anss = [(4, 8), (1, 5), (1, 4), (2, 7)]
        camp = Camp.BLACK
        p1 = Ma(camp, 3, 6)
        p2 = Ma(camp, 3, 5)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:2], anss[:2]):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[2:], anss[2:]):
            force, action, act_param, piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)


if __name__ == '__main__':
    unittest.main()
