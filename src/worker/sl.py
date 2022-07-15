"""
Contains the worker for training the model using recorded game data rather than self-play
"""
import os
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from itertools import repeat
from logging import getLogger
from threading import Thread
from time import time
from typing import Tuple

from xiangqi import Env, Camp

from common.data_helper import write_game_data_to_file, find_pgn_files
from common.pgn_parser_simple import get_games_from_file

logger = getLogger(__name__)


def start(cfg):
    return SupervisedLearningWorker(cfg).start()


class SupervisedLearningWorker:
    """
    Worker which performs supervised learning on recorded games.

    Attributes:
        :ivar Config config: config for this worker
        :ivar list((str,list(float)) buffer: buffer containing the data to use for training -
            each entry contains a FEN encoded game state and a list where every index corresponds
            to a chess move. The move that was taken in the actual game is given a value (based on
            the player elo), all other moves are given a 0.
    """

    def __init__(self, config):
        """
        :param config:
        """
        self.config = config
        os.makedirs(self.config.resource.play_data_dir, exist_ok=True)
        self.buffer = []

    def start(self):
        """
        Start the actual training.
        """
        self.buffer = []
        # noinspection PyAttributeOutsideInit
        game_idx = 0
        start_time = time()
        n_failed = 0
        with ProcessPoolExecutor(max_workers=7) as executor:
            games = self.get_games_from_all_files()

            for env, data in executor.map(get_buffer, repeat(self.config), games):
                game_idx += 1
                if not data:
                    n_failed += 1
                    continue
                self.buffer += data
                if (game_idx % self.config.playdata.sl_nb_game_in_file) == 0:
                    self.flush_buffer()
                end_time = time()
                winner = env.winner.name if env.winner is not None else str(env.winner)
                logger.debug(f'game {game_idx:4} time={(end_time - start_time):.3f}s '
                             f'n_steps={env.n_steps:3} {winner}')
                start_time = end_time

        print(f'failed: {n_failed}, total: {game_idx}, helpful: {1 - n_failed / game_idx}')
        if len(self.buffer) > 0:
            self.flush_buffer()

    def get_games_from_all_files(self):
        """
        Loads game data from pgn files
        :return list(chess.pgn.Game): the games
        """
        files = find_pgn_files(self.config.resource.pgn_dir)
        print(len(files))
        games = []
        for filename in files:
            games.extend(get_games_from_file(filename))
        print("done reading")
        return games

    def flush_buffer(self):
        """
        Clears out the moves loaded into the buffer and saves the to file.
        """
        rc = self.config.resource
        game_id = datetime.now().strftime("%Y%m%d-%H%M%S.%f")
        path = os.path.join(rc.play_data_dir, rc.play_data_filename_tmpl % game_id)
        logger.info(f"save play data to {path}")
        thread = Thread(target=write_game_data_to_file, args=(path, self.buffer))
        thread.start()
        self.buffer = []


def clip_elo_policy(config, elo):
    # 0 until min_elo, 1 after max_elo, linear in between
    return min(1, max(0, elo - config.playdata.min_elo_policy) / (
            config.playdata.max_elo_policy - config.playdata.min_elo_policy))


def get_buffer(config, game: dict) -> Tuple[Env, list]:
    """
    Gets data to load into the buffer by playing a game using PGN data.
    :param Config config: config to use to play the game
    :param pgn.Game game: game to play
    :return list(str,list(float)): data from this game for the SupervisedLearningWorker.buffer
    """
    from player import Playbook

    result = game['Result']
    moves = game['moves']
    red_elo, black_elo = int(game.get('RedElo', 100)), int(game.get('BlackElo', 100))
    red_weight = clip_elo_policy(config, red_elo)
    black_weight = clip_elo_policy(config, black_elo)

    players = {Camp.RED: Playbook(Camp.RED, moves[::2], result, config),
               Camp.BLACK: Playbook(Camp.BLACK, moves[1::2], result, config)}
    env = Env()
    for p in players.values():
        p.env = env

    ob = env.reset()
    while True:
        player = players[ob['cur_player']]
        try:
            action = player.make_decision(**ob)
            ob, reward, done, info = env.step(action)
        except Exception as e:
            logger.error(e)
            return env, []
        if done:
            print(f'player {player.id.name}, reward: {reward}')
            break

    player = players[env.cur_player]
    player.finish_game(reward)
    oppo = players[env.cur_player.opponent()]
    oppo.finish_game(-reward)

    data = []
    for i in range(len(player.sar)):
        data.append(player.sar[i])
        if i < len(oppo.sar):
            data.append(oppo.sar[i])
    return env, data
