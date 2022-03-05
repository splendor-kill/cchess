import sys
import unittest

sys.path.append('src')

from board import Board, parse_action, Action, parse_action_iccs, to_iccs_action, to_chinese_action
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
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        cmds = ['车9退2', '车9进9']
        for cmd in cmds:
            self.assertRaises(Exception, parse_action, cmd, camp, board)

    def test_parse_action2(self):
        cmds = ['车8平3', '车8进3', '车8退5']
        anss = [(6, 4), (1, 1), (1, 9)]
        camp = Camp.RED
        col, row = 1, 4
        p = Ju(camp, col, row)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)

    def test_parse_action3(self):
        cmds = ['前车进2', '前车退2', '前车平2', '后车进2', '后车退2', '后车平2']
        anss = [(3, 3), (3, 7), (7, 5), (3, 4), (3, 8), (7, 6)]
        camp = Camp.RED
        p1 = Ju(camp, 3, 6)
        p2 = Ju(camp, 3, 5)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:3], anss[:3]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[3:], anss[3:]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)

    def test_parse_action4(self):
        cmds = ['前车进2', '前车退2', '前车平2', '后车进2', '后车退2', '后车平2']
        anss = [(3, 8), (3, 4), (1, 6), (3, 7), (3, 3), (1, 5)]
        camp = Camp.BLACK
        p1 = Ju(camp, 3, 6)
        p2 = Ju(camp, 3, 5)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:3], anss[:3]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[3:], anss[3:]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)


class MaActionTest(unittest.TestCase):
    def test_parse_action1(self):
        cmd = '傌八进七'
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        piece, dst = parse_action(cmd, camp, board)
        self.assertEqual(camp, piece.camp)
        self.assertEqual(Force.MA, piece.force)
        self.assertEqual((1, 9), (piece.col, piece.row))
        self.assertEqual((2, 7), dst)

    def test_parse_action2(self):
        cmd = '马8进7'
        camp = Camp.BLACK
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        piece, dst = parse_action(cmd, camp, board)
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
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
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
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
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
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[2:], anss[2:]):
            piece, dst = parse_action(cmd, camp, board)
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
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[2:], anss[2:]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)


class XiangActionTest(unittest.TestCase):
    def test_parse_action1(self):
        cmds = ['相3进5', '相5进7', '相7退9', '相9退7', '相7进5', '相5进3', '相3退1', '相1退3']
        anss = [(4, 7), (2, 5), (0, 7), (2, 9), (4, 7), (6, 5), (8, 7), (6, 9)]
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        board.throw_away(board.piece_at(2, 9))  # left red Xiang
        col, row = 6, 9
        p = board.piece_at(col, row)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)
            piece.move_to(board, dst[0], dst[1])

    def test_parse_action2(self):
        cmds = ['相3进5', '相5进7', '相7退9', '相9退7', '相7进5', '相5进3', '相3退1', '相1退3']
        anss = [(4, 2), (6, 4), (8, 2), (6, 0), (4, 2), (2, 4), (0, 2), (2, 0)]
        camp = Camp.BLACK
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        board.throw_away(board.piece_at(6, 0))  # right black Xiang
        col, row = 2, 0
        p = board.piece_at(col, row)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)
            piece.move_to(board, dst[0], dst[1])

    def test_parse_action3(self):
        cmds = ['前相退5', '后相进9']
        anss = [(4, 7), (0, 7), (7, 5), (3, 4), (3, 8), (7, 6)]
        camp = Camp.RED
        p1 = Xiang(camp, 2, 9)
        p2 = Xiang(camp, 2, 5)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:1], anss[:1]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[1:], anss[1:]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)

    def test_parse_action4(self):
        cmds = ['前相退5', '后相进1']
        anss = [(4, 2), (0, 2)]
        camp = Camp.BLACK
        p1 = Xiang(camp, 2, 4)
        p2 = Xiang(camp, 2, 0)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:1], anss[:1]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[1:], anss[1:]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)

    def test_parse_action5(self):
        cmds = ['前相进5', '后相退5', '相5平3']
        camp = Camp.RED
        p1 = Xiang(camp, 2, 9)
        p2 = Xiang(camp, 2, 5)
        situation = [p1, p2]
        board = Board(situation)
        for cmd in cmds[:2]:
            self.assertRaises(Exception, parse_action, cmd, camp, board)
        p1 = Xiang(camp, 4, 7)
        situation = [p1]
        board = Board(situation)
        for cmd in cmds[2:]:
            self.assertRaises(Exception, parse_action, cmd, camp, board)

    def test_parse_action6(self):
        cmds = ['相3退5', '相3进1']
        anss = [(4, 2), (0, 2)]
        camp = Camp.BLACK
        p1 = Xiang(camp, 2, 4)
        p2 = Xiang(camp, 2, 0)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:1], anss[:1]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[1:], anss[1:]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)

    def test_parse_action7(self):
        from constants import kaggle_1
        cmds = ['象5退3']
        anss = [(2, 0)]
        camp = Camp.BLACK
        board = Board(kaggle_1)
        xiang = board.piece_at(4, 2)
        self.assertEqual(Force.XIANG, xiang.force)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is xiang)
            self.assertEqual(ans, dst)


class ShiActionTest(unittest.TestCase):
    def test_parse_action1(self):
        cmds = ['士4进5', '士5进6', '士6退5', '士5进4', '士4退5', '士5退6', '士6进5', '士5退4']
        anss = [(4, 8), (3, 7), (4, 8), (5, 7), (4, 8), (3, 9), (4, 8), (5, 9)]
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        board.throw_away(board.piece_at(3, 9))  # left red Shi
        col, row = 5, 9
        p = board.piece_at(col, row)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)
            piece.move_to(board, dst[0], dst[1])

    def test_parse_action2(self):
        cmds = ['士6进5', '士5进6', '士6退5', '士5进4', '士4退5', '士5退4', '士4进5', '士5退6']
        anss = [(4, 1), (5, 2), (4, 1), (3, 2), (4, 1), (3, 0), (4, 1), (5, 0)]
        camp = Camp.BLACK
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        board.throw_away(board.piece_at(3, 0))  # left black Shi
        col, row = 5, 0
        p = board.piece_at(col, row)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)
            piece.move_to(board, dst[0], dst[1])

    def test_parse_action3(self):
        cmds = ['前士退5', '后士进5']
        anss = [(4, 8), (4, 8)]
        camp = Camp.RED
        p1 = Shi(camp, 3, 9)
        p2 = Shi(camp, 3, 7)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:1], anss[:1]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[1:], anss[1:]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)

    def test_parse_action4(self):
        cmds = ['前士退5', '后士进5']
        anss = [(4, 1), (4, 1)]
        camp = Camp.BLACK
        p1 = Shi(camp, 3, 2)
        p2 = Shi(camp, 3, 0)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:1], anss[:1]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[1:], anss[1:]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)

    def test_parse_action5(self):
        cmds = ['前士进5', '后士退5', '士5平6']
        camp = Camp.RED
        p1 = Shi(camp, 3, 9)
        p2 = Shi(camp, 3, 7)
        situation = [p1, p2]
        board = Board(situation)
        for cmd in cmds[:2]:
            self.assertRaises(Exception, parse_action, cmd, camp, board)
        p1 = Shi(camp, 4, 8)
        situation = [p1]
        board = Board(situation)
        for cmd in cmds[2:]:
            self.assertRaises(Exception, parse_action, cmd, camp, board)


class ShuaiActionTest(unittest.TestCase):
    def test_parse_action1(self):
        cmds = ['帅5进', '帅5平6', '帅6退1', '帅6平5']
        anss = [(4, 8), (3, 8), (3, 9), (4, 9)]
        camp = Camp.RED
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        board.throw_away(board.piece_at(3, 9))  # left red Shi
        col, row = 4, 9
        p = board.piece_at(col, row)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)
            piece.move_to(board, dst[0], dst[1])

    def test_parse_action2(self):
        cmds = ['将5进', '将5平6', '将6退', '将6平5']
        anss = [(4, 1), (5, 1), (5, 0), (4, 0)]
        camp = Camp.BLACK
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        board.throw_away(board.piece_at(5, 0))  # right black Shi
        col, row = 4, 0
        p = board.piece_at(col, row)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)
            piece.move_to(board, dst[0], dst[1])

    def test_parse_action5(self):
        cmds = ['将5平3', '将5平7', '将5进2', '将5进3', '帅5退2']
        camp = Camp.RED
        p = Shuai(camp, 4, 8)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        for cmd in cmds:
            self.assertRaises(Exception, parse_action, cmd, camp, board)


class PaoActionTest(unittest.TestCase):
    def test_parse_action1(self):
        from board import toggle_view
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        cmds = ['炮2平5', '炮2进7', '炮2退1']
        anss = [(4, 7), (7, 0), (7, 8)]
        camp = Camp.RED
        col, row = 7, 7
        p = board.piece_at(col, row)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)
        camp = camp.opponent()
        anss = [toggle_view(c, r) for (c, r) in anss]
        col, row = toggle_view(col, row)
        p = board.piece_at(col, row)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)

    def test_parse_action2(self):
        cmds = ['炮8进8', '炮9平9', '炮9退1']
        camp = Camp.BLACK
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        for cmd in cmds:
            self.assertRaises(Exception, parse_action, cmd, camp, board)
        p = Pao(camp, 9, 1)
        situation = [Shuai(Camp.RED, 4, 9), Shuai(Camp.BLACK, 3, 0), p]
        board = Board(situation)
        cmds = ['炮9退2', '炮9进9']
        for cmd in cmds:
            self.assertRaises(Exception, parse_action, cmd, camp, board)

    def test_parse_action3(self):
        cmds = ['前炮进2', '前炮退2', '前炮平2', '后炮进2', '后炮退2', '后炮平2']
        anss = [(3, 3), (3, 7), (7, 5), (3, 4), (3, 8), (7, 6)]
        camp = Camp.RED
        p1 = Pao(camp, 3, 6)
        p2 = Pao(camp, 3, 5)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:3], anss[:3]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[3:], anss[3:]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)

    def test_parse_action4(self):
        cmds = ['前炮进2', '前炮退2', '前炮平2', '后炮进2', '后炮退2', '后炮平2']
        anss = [(3, 8), (3, 4), (1, 6), (3, 7), (3, 3), (1, 5)]
        camp = Camp.BLACK
        p1 = Pao(camp, 3, 6)
        p2 = Pao(camp, 3, 5)
        situation = [p1, p2]
        board = Board(situation)
        for cmd, ans in zip(cmds[:3], anss[:3]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p1)
            self.assertEqual(ans, dst)
        for cmd, ans in zip(cmds[3:], anss[3:]):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p2)
            self.assertEqual(ans, dst)


class BingActionTest(unittest.TestCase):
    def test_parse_action1(self):
        from board import toggle_view
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        cmds = ['兵3进', '兵3进', '兵3进', '兵3平4']
        anss = [(6, 5), (6, 4), (6, 3), (5, 3)]
        camp = Camp.RED
        col, row = 6, 6
        p = board.piece_at(col, row)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)
            e = board.piece_at(dst[0], dst[1])
            if e is not None:
                board.throw_away(e)
            piece.move_to(board, dst[0], dst[1])

        camp = camp.opponent()
        anss = [toggle_view(c, r) for (c, r) in anss]
        col, row = toggle_view(col, row)
        p = board.piece_at(col, row)
        for cmd, ans in zip(cmds, anss):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is p)
            self.assertEqual(ans, dst)
            e = board.piece_at(dst[0], dst[1])
            if e is not None:
                board.throw_away(e)
            piece.move_to(board, dst[0], dst[1])

    def test_parse_action2(self):
        cmds = ['兵9进2', '兵7平8', '兵5退1']
        camp = Camp.BLACK
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        for cmd in cmds:
            self.assertRaises(Exception, parse_action, cmd, camp, board)

    def test_parse_action3(self):
        cmds = ['前兵3进', '中兵3进', '后兵3进', '前兵平2', '中兵平4', '二兵平4', '三兵进', '中兵进', '二兵三平四']
        anss = [(6, 1), (6, 3), (6, 5), (7, 2), (5, 4), (5, 4), (6, 5), (6, 3), (5, 4)]
        camp = Camp.RED
        p1 = Bing(camp, 6, 6)
        p2 = Bing(camp, 6, 4)
        p3 = Bing(camp, 6, 2)
        situation = [p1, p2, p3]
        board = Board(situation)
        expected_p = [p3, p2, p1, p3, p2, p2]
        for cmd, ans, exp in zip(cmds, anss, expected_p):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is exp)
            self.assertEqual(ans, dst)

        from board import toggle_view
        camp = camp.opponent()
        anss = [toggle_view(c, r) for (c, r) in anss]
        p1 = Bing(camp, *toggle_view(p1.col, p1.row))
        p2 = Bing(camp, *toggle_view(p2.col, p2.row))
        p3 = Bing(camp, *toggle_view(p3.col, p3.row))
        situation = [p1, p2, p3]
        board = Board(situation)
        expected_p = [p3, p2, p1, p3, p2]
        for cmd, ans, exp in zip(cmds, anss, expected_p):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is exp)
            self.assertEqual(ans, dst)

    def test_parse_action4(self):
        cmds = ['前兵6进', '中兵6进', '后兵6进', '三兵进', '前兵8进', '后兵8进', '前兵6平7', '前兵8平7', ]
        anss = [(3, 1), (3, 2), (3, 3), (3, 3), (1, 2), (1, 3), (2, 2), (2, 3)]
        camp = Camp.RED
        p1 = Bing(camp, 3, 4)
        p2 = Bing(camp, 3, 3)
        p3 = Bing(camp, 3, 2)
        p4 = Bing(camp, 1, 3)
        p5 = Bing(camp, 1, 4)
        situation = [p1, p2, p3, p4, p5]
        board = Board(situation)
        expected_p = [p3, p2, p1, p1, p4, p5, p3, p4]
        for cmd, ans, exp in zip(cmds, anss, expected_p):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is exp)
            self.assertEqual(ans, dst)

        from board import toggle_view
        camp = camp.opponent()
        anss = [toggle_view(c, r) for (c, r) in anss]
        p1 = Bing(camp, *toggle_view(p1.col, p1.row))
        p2 = Bing(camp, *toggle_view(p2.col, p2.row))
        p3 = Bing(camp, *toggle_view(p3.col, p3.row))
        p4 = Bing(camp, *toggle_view(p4.col, p4.row))
        p5 = Bing(camp, *toggle_view(p5.col, p5.row))
        situation = [p1, p2, p3, p4, p5]
        board = Board(situation)
        expected_p = [p3, p2, p1, p1, p4, p5, p3, p4]
        for cmd, ans, exp in zip(cmds, anss, expected_p):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is exp)
            self.assertEqual(ans, dst)

    def test_parse_action5(self):
        cmds = ['前兵进', '后兵进', '前兵平4', '后兵平6', '四兵进', '五兵进']
        camp = Camp.RED
        p1 = Bing(camp, 4, 6)
        p2 = Bing(camp, 4, 4)
        p3 = Bing(camp, 4, 2)
        p4 = Bing(camp, 1, 3)
        p5 = Bing(camp, 1, 4)
        situation = [p1, p2, p3, p4, p5]
        board = Board(situation)
        for cmd in cmds:
            self.assertRaises(Exception, parse_action, cmd, camp, board)

    def test_parse_action6(self):
        cmds = ['前兵进一']
        anss = [(4, 3)]
        camp = Camp.RED
        situation = '''
        ＋－＋－＋－士－將－士－象－＋－＋
        ｜　｜　｜　｜＼｜／｜　｜　｜　｜
        ＋－＋－＋－＋－＋－＋－＋－＋－＋
        ｜　｜　｜　｜／｜＼｜　｜　｜　｜
        象－＋－馬－＋－砲－＋－砲－＋－馬
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－炮－＋－＋－＋－＋－＋－＋
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－卒－＋－兵－＋－＋－＋－卒
        兵－＋－＋－傌－＋－＋－＋－＋－＋
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－＋－＋－兵－＋－＋－＋－兵
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－＋－＋－相－＋－傌－＋－＋
        ｜　｜　｜　｜＼｜／｜　｜　｜　｜
        ＋－＋－＋－＋－仕－＋－＋－＋－＋
        ｜　｜　｜　｜／｜＼｜　｜　｜　｜
        ＋－＋－相－仕－帥－＋－＋－＋－＋
        '''
        board = Board(situation)
        p1 = board.piece_at(4, 4)
        p2 = board.piece_at(4, 6)
        expected_p = [p1]
        for cmd, ans, exp in zip(cmds, anss, expected_p):
            piece, dst = parse_action(cmd, camp, board)
            self.assertTrue(piece is exp)
            self.assertEqual(ans, dst)


class SpecialActionTest(unittest.TestCase):
    def test_parse_action_shu(self):
        opening = '''
        ＋－＋－＋－＋－＋－將－＋－＋－＋
        ｜　｜　｜　｜＼｜／｜　｜　｜　｜
        ＋－＋－＋－＋－俥－＋－＋－＋－＋
        ｜　｜　｜　｜／｜＼｜　｜　｜　｜
        ＋－＋－＋－＋－兵－兵－＋－＋－＋
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－＋－＋－＋－＋－＋－＋－＋
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－＋－＋－＋－＋－＋－＋－＋
        ＋－＋－＋－＋－＋－＋－＋－＋－＋
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－＋－＋－＋－車－＋－＋－＋
        ｜　｜　｜　｜　｜　｜　｜　｜　｜
        ＋－＋－＋－＋－相－＋－＋－＋－＋
        ｜　｜　｜　｜＼｜／｜　｜　｜　｜
        ＋－＋－＋－＋－仕－＋－＋－＋－＋
        ｜　｜　｜　｜／｜＼｜　｜　｜　｜
        ＋－＋－＋－＋－帥－仕－＋－＋－＋
        '''
        board = Board(opening)
        camp = Camp.BLACK
        from player import Human
        cmd = '认输'
        action = Human.flex_action_input(cmd, camp, board, sue_draw=False)
        self.assertEqual(Action.RESIGN, action['action'])


class ICCSActionTest(unittest.TestCase):
    def test_parse_action1(self):
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        cmds = ['h2e2', 'c3c4', 'i0i1', 'h0g2', 'c0a2', 'f0e1', 'e0e1']
        ans_forces = [Force.PAO, Force.BING, Force.JU, Force.MA, Force.XIANG, Force.SHI, Force.SHUAI]
        ans_srcs = [(7, 7), (2, 6), (8, 9), (7, 9), (2, 9), (5, 9), (4, 9)]
        ans_dsts = [(4, 7), (2, 5), (8, 8), (6, 7), (0, 7), (4, 8), (4, 8)]
        camp = Camp.RED

        for cmd, force, src, dst in zip(cmds, ans_forces, ans_srcs, ans_dsts):
            p = board.piece_at(*src)
            piece, dst1 = parse_action_iccs(cmd, board)
            self.assertTrue(piece is p)
            self.assertEqual(camp, p.camp)
            self.assertEqual(force, p.force)
            self.assertEqual(src[0], p.col)
            self.assertEqual(src[1], p.row)
            self.assertEqual(dst, dst1)

    def test_parse_action2(self):
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        cmds = ['b7b0']
        camp = Camp.RED
        for cmd in cmds:
            self.assertRaises(Exception, parse_action_iccs, cmd, camp, board)

    def test_to_iccs_action(self):
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        p = board.piece_at(7, 7)
        self.assertEqual(Force.PAO, p.force)
        self.assertEqual(Camp.RED, p.camp)
        dst = (4, 7)
        action = {'piece': p, 'dst': dst}
        a = to_iccs_action(action)
        self.assertEqual('h2e2', a)


class ActionToChineseTest(unittest.TestCase):
    def test_to_chinese1(self):
        from constants import FULL_BOARD
        board = Board(FULL_BOARD)
        srcs = [(2, 9), (2, 0), (1, 9), (7, 0), (5, 9), (5, 0), (8, 9), (8, 0), (7, 7), (7, 2)]
        dsts = [(4, 7), (4, 2), (0, 7), (8, 2), (4, 8), (4, 1), (8, 7), (8, 2), (7, 8), (7, 1)]
        anss = ['相七进五', '象3进5', '傌八进九', '馬8进9', '仕四进五', '士6进5', '俥一进二', '車9进2', '炮二退一', '砲8退1']
        for src, dst, ans in zip(srcs, dsts, anss):
            piece = board.piece_at(*src)
            s = to_chinese_action(piece, dst)
            s = s[10] + s[-3:]  # get rid of color codes
            self.assertEqual(ans, s)

    def test_to_chinese2(self):
        from constants import well_known_5
        board = Board(well_known_5)
        srcs = [(4, 8), (4, 1), (3, 6), (3, 4), (4, 2)]
        dsts = [(5, 9), (5, 0), (1, 7), (2, 2), (6, 0)]
        anss = ['仕五退四', '士5退6', '傌六退八', '馬4退3', '象5退7']
        for src, dst, ans in zip(srcs, dsts, anss):
            piece = board.piece_at(*src)
            s = to_chinese_action(piece, dst)
            s = s[10] + s[-3:]  # get rid of color codes
            self.assertEqual(ans, s)


if __name__ == '__main__':
    unittest.main()
