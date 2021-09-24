from enum import IntEnum

from chessman.Bing import *
from chessman.Che import *
from chessman.Ma import *
from chessman.Pao import *
from chessman.Shi import *
from chessman.Shuai import *
from chessman.Xiang import *

APPEAR_BLACK = '\033[1;30;47m'
APPEAR_RED = '\033[1;31;47m'
ENDC = '\033[0m'


class Camp(IntEnum):
    BLACK = 1
    RED = 2


class Force(IntEnum):
    SHUAI = 1
    SHI = 2
    XIANG = 3
    MA = 4
    JU = 5
    PAO = 6
    BING = 7


PIECE_CHARS = '將士象馬車砲卒帥仕相傌俥炮兵'
PLACE_CHARS = '＋Ｘ'


def piece_2_char(camp, force):
    index = 7 * (camp.value - 1) + force.value - 1
    return PIECE_CHARS[index]


def recog_piece(piece: str):
    assert piece in PIECE_CHARS
    assert len(piece) == 1
    idx = PIECE_CHARS.index(piece)
    q, r = divmod(idx, len(Force))
    camp = Camp(q + 1)
    force = Force(r + 1)
    return camp, force


FULL_BOARD = '''
車－馬－象－士－將－士－象－馬－車
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
＋－砲－＋－＋－＋－＋－＋－砲－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
卒－＋－卒－＋－卒－＋－卒－＋－卒
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜　｜　｜　｜　｜　｜
兵－＋－兵－＋－兵－＋－兵－＋－兵
｜　｜　｜　｜　｜　｜　｜　｜　｜
＋－炮－＋－＋－＋－＋－＋－炮－＋
｜　｜　｜　｜＼｜／｜　｜　｜　｜
＋－＋－＋－＋－＋－＋－＋－＋－＋
｜　｜　｜　｜／｜＼｜　｜　｜　｜
俥－傌－相－仕－帥－仕－相－傌－俥
'''

EMPTY_BOARD = '''
{p00}－{p01}－{p02}－{p03}－{p04}－{p05}－{p06}－{p07}－{p08}
｜　｜　｜　｜＼｜／｜　｜　｜　｜
{p10}－{p11}－{p12}－{p13}－{p14}－{p15}－{p16}－{p17}－{p18}
｜　｜　｜　｜／｜＼｜　｜　｜　｜
{p20}－{p21}－{p22}－{p23}－{p24}－{p25}－{p26}－{p27}－{p28}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p30}－{p31}－{p32}－{p33}－{p34}－{p35}－{p36}－{p37}－{p38}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p40}－{p41}－{p42}－{p43}－{p44}－{p45}－{p46}－{p47}－{p48}
{p50}－{p51}－{p52}－{p53}－{p54}－{p55}－{p56}－{p57}－{p58}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p60}－{p61}－{p62}－{p63}－{p64}－{p65}－{p66}－{p67}－{p68}
｜　｜　｜　｜　｜　｜　｜　｜　｜
{p70}－{p71}－{p72}－{p73}－{p74}－{p75}－{p76}－{p77}－{p78}
｜　｜　｜　｜＼｜／｜　｜　｜　｜
{p80}－{p81}－{p82}－{p83}－{p84}－{p85}－{p86}－{p87}－{p88}
｜　｜　｜　｜／｜＼｜　｜　｜　｜
{p90}－{p91}－{p92}－{p93}－{p94}－{p95}－{p96}－{p97}－{p98}
'''


class ChessBoard:
    pieces = dict()

    selected_piece = None

    def __init__(self, north_is_red=True):
        # self.north_is_red = north_is_red
        # north area
        ChessBoard.pieces[4, 0] = Shuai(4, 0, north_is_red, "north")

        ChessBoard.pieces[0, 3] = Bing(0, 3, north_is_red, "north")
        ChessBoard.pieces[2, 3] = Bing(2, 3, north_is_red, "north")
        ChessBoard.pieces[4, 3] = Bing(4, 3, north_is_red, "north")
        ChessBoard.pieces[6, 3] = Bing(6, 3, north_is_red, "north")
        ChessBoard.pieces[8, 3] = Bing(8, 3, north_is_red, "north")

        ChessBoard.pieces[1, 2] = Pao(1, 2, north_is_red, "north")
        ChessBoard.pieces[7, 2] = Pao(7, 2, north_is_red, "north")

        ChessBoard.pieces[3, 0] = Shi(3, 0, north_is_red, "north")
        ChessBoard.pieces[5, 0] = Shi(5, 0, north_is_red, "north")

        ChessBoard.pieces[2, 0] = Xiang(2, 0, north_is_red, "north")
        ChessBoard.pieces[6, 0] = Xiang(6, 0, north_is_red, "north")

        ChessBoard.pieces[1, 0] = Ma(1, 0, north_is_red, "north")
        ChessBoard.pieces[7, 0] = Ma(7, 0, north_is_red, "north")

        ChessBoard.pieces[0, 0] = Che(0, 0, north_is_red, "north")
        ChessBoard.pieces[8, 0] = Che(8, 0, north_is_red, "north")

        # south area
        ChessBoard.pieces[4, 9] = Shuai(4, 9, not north_is_red, "south")

        ChessBoard.pieces[0, 6] = Bing(0, 6, not north_is_red, "south")
        ChessBoard.pieces[2, 6] = Bing(2, 6, not north_is_red, "south")
        ChessBoard.pieces[4, 6] = Bing(4, 6, not north_is_red, "south")
        ChessBoard.pieces[6, 6] = Bing(6, 6, not north_is_red, "south")
        ChessBoard.pieces[8, 6] = Bing(8, 6, not north_is_red, "south")

        ChessBoard.pieces[1, 7] = Pao(1, 7, not north_is_red, "south")
        ChessBoard.pieces[7, 7] = Pao(7, 7, not north_is_red, "south")

        ChessBoard.pieces[3, 9] = Shi(3, 9, not north_is_red, "south")
        ChessBoard.pieces[5, 9] = Shi(5, 9, not north_is_red, "south")

        ChessBoard.pieces[2, 9] = Xiang(2, 9, not north_is_red, "south")
        ChessBoard.pieces[6, 9] = Xiang(6, 9, not north_is_red, "south")

        ChessBoard.pieces[1, 9] = Ma(1, 9, not north_is_red, "south")
        ChessBoard.pieces[7, 9] = Ma(7, 9, not north_is_red, "south")

        ChessBoard.pieces[0, 9] = Che(0, 9, not north_is_red, "south")
        ChessBoard.pieces[8, 9] = Che(8, 9, not north_is_red, "south")

    def can_move(self, x, y, dx, dy):
        return self.pieces[x, y].can_move(self, dx, dy)

    def move(self, x, y, dx, dy):
        return self.pieces[x, y].move(self, dx, dy)

    def remove(self, x, y):
        del self.pieces[x, y]

    def select(self, x, y, player_is_red):
        # 选中棋子
        if not self.selected_piece:
            if (x, y) in self.pieces and self.pieces[x, y].is_red == player_is_red:
                self.pieces[x, y].selected = True
                self.selected_piece = self.pieces[x, y]
            return False, None

        # 移动棋子
        if not (x, y) in self.pieces:
            if self.selected_piece:
                ox, oy = self.selected_piece.x, self.selected_piece.y
                if self.can_move(ox, oy, x - ox, y - oy):
                    self.move(ox, oy, x - ox, y - oy)
                    self.pieces[x, y].selected = False
                    self.selected_piece = None
                    return True, (ox, oy, x, y)
            return False, None

        # 同一个棋子
        if self.pieces[x, y].selected:
            return False, None

        # 吃子
        if self.pieces[x, y].is_red != player_is_red:
            ox, oy = self.selected_piece.x, self.selected_piece.y
            if self.can_move(ox, oy, x - ox, y - oy):
                self.move(ox, oy, x - ox, y - oy)
                self.pieces[x, y].selected = False
                self.selected_piece = None
                return True, (ox, oy, x, y)
            return False, None

        # 取消选中
        for key in self.pieces.keys():
            self.pieces[key].selected = False
        # 选择棋子
        self.pieces[x, y].selected = True
        self.selected_piece = self.pieces[x, y]
        return False, None


class Board:
    def __init__(self, situation):
        if isinstance(situation, str):
            situation = self._parse(situation)
        self.situation = situation

    def __str__(self):
        sit = {f'p{i}{j}': PLACE_CHARS[0] for i in range(10) for j in range(9)}
        for p in self.situation:
            k = f'p{p.x}{p.y}'
            sit[k] = str(p)
        return EMPTY_BOARD.format(**sit)

    @staticmethod
    def _parse(board):
        board = board.strip()
        rows = board.splitlines()
        rows = rows[:9:2] + rows[-9::2]
        assert len(rows) == 10
        sit = []
        for i, r in enumerate(rows):
            r = r.strip()
            assert len(r) == 17
            r = r[::2]  # remove non-place chars
            for j, c in enumerate(r):
                if c in PIECE_CHARS:
                    camp, force = recog_piece(c)
                    sit.append(Piece(i, j, camp, force))
        return sit


class Piece:
    def __init__(self, x, y, camp, force):
        self.x = x
        self.y = y
        self.camp = camp
        self.force = force

    def __str__(self):
        c = piece_2_char(self.camp, self.force)
        appear = APPEAR_RED if self.camp == Camp.RED else APPEAR_BLACK
        c = appear + c + ENDC
        return c


def test():
    situation = [Piece(0, 4, Camp.BLACK, Force.SHUAI),
                 Piece(2, 3, Camp.BLACK, Force.SHI), Piece(2, 4, Camp.RED, Force.BING),
                 Piece(2, 8, Camp.BLACK, Force.XIANG),
                 Piece(3, 0, Camp.BLACK, Force.BING),
                 Piece(5, 6, Camp.BLACK, Force.MA),
                 Piece(6, 2, Camp.RED, Force.BING), Piece(6, 6, Camp.BLACK, Force.BING),
                 Piece(7, 4, Camp.RED, Force.JU),
                 Piece(8, 3, Camp.BLACK, Force.BING), Piece(8, 5, Camp.BLACK, Force.BING),
                 Piece(9, 4, Camp.RED, Force.SHUAI),
                 ]
    board = Board(situation)
    print(board)

    situation = '''
    ＋－＋－象－士－將－＋－＋－＋－＋
    ｜　｜　｜　｜＼｜／｜　｜　｜　｜
    ＋－＋－＋－＋－士－＋－＋－＋－＋
    ｜　｜　｜　｜／｜＼｜　｜　｜　｜
    ＋－＋－＋－＋－象－＋－＋－＋－＋
    ｜　｜　｜　｜　｜　｜　｜　｜　｜
    ＋－＋－＋－＋－＋－＋－＋－＋－＋
    ｜　｜　｜　｜　｜　｜　｜　｜　｜
    ＋－＋－＋－＋－＋－＋－傌－俥－俥
    ＋－＋－相－＋－＋－＋－＋－＋－＋
    ｜　｜　｜　｜　｜　｜　｜　｜　｜
    ＋－車－兵－＋－兵－＋－＋－＋－＋
    ｜　｜　｜　｜　｜　｜　｜　｜　｜
    ＋－＋－＋－卒－相－＋－＋－＋－＋
    ｜　｜　｜　｜＼｜／｜　｜　｜　｜
    ＋－＋－＋－＋－卒－＋－＋－＋－＋
    ｜　｜　｜　｜／｜＼｜　｜　｜　｜
    ＋－＋－＋－帥－＋－＋－＋－＋－＋
    '''
    board = Board(situation)
    print(board)


if __name__ == '__main__':
    test()
