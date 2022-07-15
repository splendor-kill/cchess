import os

import pandas as pd

CH_POSES = '一二三四五六七八九'
EN_POSES = '123456789'
d_poses = dict(zip(EN_POSES, CH_POSES))
# PIECE_CHARS = '將士象馬車砲卒帥仕相傌俥炮兵'
PIECE_CHARS = '将士象马车炮卒帅仕相马车炮兵'
EN_PIECES = 'kaehrcpKAEHRCP'  # kabnrcpKABNRCP

D_FRONT_REAR = {'+': '前', '-': '后'}
D_ACTIONS = {'+': '进', '-': '退', '.': '平'}
d_pieces = dict(zip(EN_PIECES, PIECE_CHARS))


def to_pgn(info, moves, wxf=False, pgns_dir='.', pgn_encoding='GB2312'):
    game_id = info.iloc[0]['gameID']
    date = info.iloc[0]['game_datetime']
    black_id = info.iloc[0]['blackID']
    black_elo = info.iloc[0]['blackELO']
    red_id = info.iloc[0]['redID']
    red_elo = info.iloc[0]['redELO']
    winner = info.iloc[0]['winner']

    date = date.strftime('%Y年%m月%d日')
    d_results = {'red': '1-0', 'black': '0-1', 'tie': '1/2-1/2'}
    score = d_results[winner]

    wushi = {'e': 'b', 'h': 'n', 'E': 'B', 'H': 'N'}

    f_pgn = f'{game_id}.pgn'
    with open(os.path.join(pgns_dir, f_pgn), 'w', encoding=pgn_encoding) as fp:
        fp.write('[Game "Chinese Chess"]\n')
        fp.write(f'[Date "{date}"]\n')
        if wxf:
            fp.write(f'[Format "WXF"]\n')
        fp.write(f'[Red "{red_id}"]\n')
        fp.write(f'[RedElo "{red_elo}"]\n')
        fp.write(f'[Black "{black_id}"]\n')
        fp.write(f'[BlackElo "{black_elo}"]\n')
        fp.write(f'[Result "{score}"]\n')

        step = 1
        first = None
        track = {}
        for _, row in moves.iterrows():
            if first is None:
                first = track_ae(row.move, row.ch_move, wxf, track)
                if wxf and first[0] in wushi:
                    first = wushi[first[0]] + first[1:]
                continue
            second = track_ae(row.move, row.ch_move, wxf, track)
            if wxf and second[0] in wushi:
                second = wushi[second[0]] + second[1:]
            line = f'{step}. {first} {second}\n'
            fp.write(line)
            step += 1
            first = None

        line = f'{step}. {score}\n' if first is None else f'{step}. {first} {score}\n'
        fp.write(line)


def track_ae(en_move, ch_move, wxf, rec):
    """in Wushi, WXF A+-5 must be repr as A4-5 or A6-5, this case exists in Advisor & Elephant
    """
    first = en_move if wxf else ch_move
    c0, c1, c2, c3 = en_move
    if c0 in rec and c1 in '+-':
        if wxf:
            first = c0 + rec[c0] + c2 + c3
        else:
            col = d_poses[rec[c0]] if first[-1] in CH_POSES else rec[c0]
            first = first[1] + col + first[2:]
    if c0 in 'AEae':
        rec[c0] = c3
    return first


def trans(move):
    """
    [single-letter piece abbreviation]
    [former file]
    [operator indicating direction of movement]
    [new file, or in the case of purely vertical movement, number of ranks traversed]
    """
    assert len(move) == 4
    piece, ff, op, nfr = move
    # assert piece.upper() in 'RHEAKCP'
    # assert ff in '123456789+-'
    # assert op in '.+-'
    # assert nfr in '123456789'

    res_piece = d_pieces[piece]

    is_red = piece.isupper()

    prefix = ''
    res_ff = ''
    if ff in D_FRONT_REAR:
        prefix = D_FRONT_REAR[ff]
    else:
        res_ff = d_poses[ff] if is_red else ff
    res_nfr = d_poses[nfr] if is_red else nfr

    return f'{prefix}{res_piece}{res_ff}{D_ACTIONS[op]}{res_nfr}'


def main(data_dir, save_dir, pgn_encoding):
    info_file = os.path.join(data_dir, 'gameinfo.csv')
    moves_file = os.path.join(data_dir, 'moves.csv')
    df1 = pd.read_csv(info_file, parse_dates=['game_datetime'])
    print(df1.shape)
    df2 = pd.read_csv(moves_file)
    print(df2.shape)
    # df2['move'] = df2.apply(lambda row: row.move.upper() if row.side == 'red' else row.move.lower(), axis=1)
    df2['ch_move'] = df2.move.apply(trans)

    os.makedirs(save_dir, exist_ok=True)

    cnt = 0
    for n, g in df2.groupby('gameID'):
        dfx = g.sort_values(['turn', 'side'], ascending=[True, False])
        info = df1[df1.gameID == n]
        assert info.shape == (1, 7)
        print(n, dfx.shape[0], info.iloc[0]['winner'])
        to_pgn(info, dfx, pgns_dir=save_dir, pgn_encoding=pgn_encoding)
        cnt += 1
        # if cnt >= 1:
        #     break
    print(cnt)


if __name__ == '__main__':
    # dataset_url = 'https://www.kaggle.com/boyofans/onlinexiangqi'
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str)
    parser.add_argument('--pgn_dir', type=str, default='pgns')
    parser.add_argument('--pgn_encoding', type=str, default='GB2312')
    args = parser.parse_args()

    main(args.data_dir, args.pgn_dir, args.pgn_encoding)
