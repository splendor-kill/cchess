import re
from enum import IntEnum


PAT_OPTION = re.compile(r'\[(\w+)\s"(.*)"\]')
PAT_MOVE_MOVE = re.compile(r'\d+\.\s(.{4})\s(.{4})')
PAT_MOVE_RESULT = re.compile(r'\d+\.\s(.{4})\s(\d(/2)?-\d(/2)?)')
PAT_RESULT = re.compile(r'\d+\.\s(\d(/2)?-\d(/2)?)')


class State(IntEnum):
    IDLE = 1
    HEAD = 2
    BODY = 3
    POST = 4
    ERR = 5
    END = 6


def handle_head(line: str, game: dict):
    m = PAT_OPTION.match(line)
    if not m:
        return State.ERR
    k = m.group(1)
    if k in ('Result', 'RedElo', 'BlackElo'):
        game[k] = m.group(2)
    return State.HEAD


def handle_body(line: str, game: dict):
    parts = line.split()
    if not parts[0][:-1].isdigit():
        return State.ERR
    n_parts = len(parts)
    if n_parts == 2:
        if not PAT_RESULT.match(line):
            return State.ERR
        game['Result'] = parts[1]
        return State.BODY
    if n_parts == 3:
        m = PAT_MOVE_RESULT.match(line)
        if m:
            game['moves'].append(m.group(1))
            assert game['Result'] == m.group(2)
            return State.BODY
        game['moves'].append(parts[1])
        game['moves'].append(parts[2])
        return State.BODY
    return State.ERR


def get_games_from_file(filename):
    games = []

    with open(filename) as fp:
        state = State.IDLE
        game = None

        def handle_complete(games: list):
            nonlocal game
            if game is not None:
                games.append(game)
                game = None

        while state not in (State.ERR, State.END):
            try:
                line = next(fp)
            except StopIteration:
                state = State.END
                handle_complete(games)
                break
            line = line.strip()
            if state == State.IDLE:
                if line.startswith('['):
                    state = State.HEAD
                    game = {'moves': []}
                    state = handle_head(line, game)
                else:
                    # keep State.IDLE
                    continue
            elif state == State.HEAD:
                if line.startswith('['):
                    # keep State.HEAD
                    state = handle_head(line, game)
                elif line[0].isdigit():
                    state = State.BODY
                    state = handle_body(line, game)
                else:
                    state = State.ERR
            elif state == State.BODY:
                if not line:
                    state = State.IDLE
                    handle_complete(games)
                elif not line[0].isdigit():
                    state = State.POST
                else:
                    # keep State.BODY
                    state = handle_body(line, game)
            elif state == State.POST:
                if not line:
                    # keep State.POST
                    pass
                else:
                    state = State.IDLE
                    handle_complete(games)
    print(f'end with state: {state.name}, there are {len(games)} games in total.')
    return games


if __name__ == '__main__':
    file = './data/7eb106f1_utf8.pgn'
    # file = './data/merged.pgn'
    get_games_from_file(file)
