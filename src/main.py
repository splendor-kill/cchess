# https://www.unicode.org/charts/PDF/U2500.pdf
# http://www.unicode.org/wg2/docs/n4825-pdam2chart.pdf page 25

lt2, rt2, lb2, rb2 = '\u2554\u2557\u255A\u255D'
h2, v2 = '\u2550\u2551'
te = '\u2564'
ju1 = '\U0001FA64'


def show_board():
    print(ju1 + h2 + te + h2 + te + h2 + te + h2 + te + h2 + te + h2 + te + h2 + te + h2 + rt2)


if __name__ == '__main__':
    show_board()
