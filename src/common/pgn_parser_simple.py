import re
import sys
from enum import IntEnum

PAT_OPTION = re.compile(r'\[(\w+)\s"(.*)"\]')
PAT_MOVE_MOVE = re.compile(r'\d+\.\s(.{4})\s(.{4})')
PAT_MOVE_RESULT = re.compile(r'\d+\.\s(.{4})\s(\d(/2)?-\d(/2)?)')
PAT_RESULT = re.compile(r'(\d+\.\s)?(\d(/2)?-\d(/2)?)')


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
    m = PAT_RESULT.match(line)
    if m:
        game['Result'] = m.group(2)
        return State.BODY
    parts = line.split()
    if not parts[0][:-1].isdigit():
        return State.ERR
    n_parts = len(parts)
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

        line_consumed = True
        while state not in (State.ERR, State.END):
            if line_consumed:
                try:
                    line = next(fp)
                except StopIteration:
                    state = State.END
                    handle_complete(games)
                    break
                line = line.strip()

            if state == State.IDLE:
                line_consumed = True
                if line.startswith('['):
                    state = State.HEAD
                    game = {'moves': []}
                    state = handle_head(line, game)
                else:
                    # keep State.IDLE
                    continue
            elif state == State.HEAD:
                line_consumed = True
                if line.startswith('['):
                    # keep State.HEAD
                    state = handle_head(line, game)
                elif line[0].isdigit():
                    state = State.BODY
                    state = handle_body(line, game)
                else:
                    state = State.ERR
            elif state == State.BODY:
                line_consumed = True
                if not line:
                    state = State.IDLE
                    handle_complete(games)
                elif not line[0].isdigit():
                    state = State.POST
                    line_consumed = False  # this is the first line under POST
                else:
                    # keep State.BODY
                    state = handle_body(line, game)
            elif state == State.POST:
                if game is not None:
                    handle_complete(games)
                    game = None
                line_consumed = True
                if not line:
                    state = State.IDLE
                elif line.startswith('['):
                    state = State.IDLE
                    line_consumed = False  # start a new game replay directly
                else:
                    # keep State.POST
                    pass

    print(f'end with state: {state.name}, there are {len(games)} games in {filename}.')
    return games


if __name__ == '__main__':
    file = sys.argv[1]
    get_games_from_file(file)
