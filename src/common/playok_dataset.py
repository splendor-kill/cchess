import os
import re
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
from time import time

from kaggle_dataset import trans

pat = re.compile(r'^(RED|BLACK)\s+(\S+)\s+;\s+(\d+).*')
pat_move = re.compile(r'(\w[\d+-][.+-=]\d)')

piece_map = {'A': '士', 'C': '炮', 'E': '象', 'H': '马', 'K': '帅', 'P': '兵', 'R': '车'}
op_map = {'+': '进', '-': '退', '.': '平'}
digit_map = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}

pgn_dir = '.'
pgn_encoding = 'GB2312'
n_concur = 1


def get_name_elo(line):
    m = pat.match(line)
    if m:
        color, name, elo = m.group(1), m.group(2), m.group(3)
        return color, name, elo
    return None, None, None


def trans_move_ch(m, red_move):
    try:
        p1 = digit_map[m[1]] if red_move else m[1]
        p3 = digit_map[m[3]] if red_move else m[3]
    except Exception as e:
        print(m, e)
    return piece_map[m[0].upper()] + p1 + op_map[m[2]] + p3


def to_wushi_pgn(file):
    date_str = None
    red_name = None
    red_elo = None
    black_name = None
    black_elo = None
    result = None
    moves = []

    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith('FORMAT'):
            continue
        elif line.startswith('RED'):
            _, red_name, red_elo = get_name_elo(line)
        elif line.startswith('BLACK'):
            _, black_name, black_elo = get_name_elo(line)
        elif line.startswith('RESULT'):
            result = line.split()[-1]
            if result == '0.5-0.5':
                result = '1/2-1/2'
        elif line.startswith('DATE'):
            dt = datetime.fromisoformat(lines[4].strip()[4:].strip())
            date_str = dt.strftime("%Y年%-m月%-d日")
        elif line.startswith('EVENT'):
            pass
        elif line.startswith('START'):
            continue
        else:
            moves.extend(pat_move.findall(line))

    if result is None or not moves:
        return

    new_lines = [
        f'[Game "Chinese Chess"]',
        f'[Date "{date_str}"]',
        f'[Red "{red_name}"]',
        f'[RedElo "{red_elo}"]',
        f'[Black "{black_name}"]',
        f'[BlackElo "{black_elo}"]',
        f'[Result "{result}"]'
    ]

    parts = []
    for i, move in enumerate(moves):
        red_move = i % 2 == 0
        if red_move:
            parts.append(f'{i // 2 + 1}.')
        parts.append(trans(move))
        if i % 2 == 1:
            new_lines.append(' '.join(parts))
            parts.clear()
    if parts:  # maybe red win and end the game
        new_lines.append(f"{' '.join(parts)} {result}")
        parts.clear()
    else:
        new_lines.append(result)

    new_file = os.path.splitext(os.path.basename(file))[0]
    new_file = os.path.join(pgn_dir, f'{new_file}.pgn')
    with open(new_file, 'w', encoding=pgn_encoding) as f:
        f.write('\n'.join(new_lines))
        f.write('\n')


def convert_dir(data_dir):
    start_time = time()
    files = os.listdir(data_dir)
    if not files:
        return
    files = [os.path.join(data_dir, name) for name in files]
    with ProcessPoolExecutor(max_workers=args.n_concur) as executor:
        executor.map(to_wushi_pgn, files)
    print(f'convert {len(files)} spend {time() - start_time} sec.')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str)
    parser.add_argument('--data_dir', type=str, default='.')
    parser.add_argument('--pgn_dir', type=str, default='.')
    parser.add_argument('--pgn_encoding', type=str, default='GB2312')
    parser.add_argument('--n_concur', type=int, default=1, help='how many processes/threads')

    args = parser.parse_args()
    pgn_dir = args.pgn_dir
    pgn_encoding = args.pgn_encoding
    n_concur = args.n_concur
    if args.file:
        to_wushi_pgn(args.file)
    else:
        convert_dir(args.data_dir)
