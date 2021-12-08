"""
Contains the worker for training the model using recorded game data rather than self-play
"""
import os
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from logging import getLogger
from threading import Thread
from time import time
from typing import Tuple

from env import Env
from common.pgn_parser_simple import get_games_from_file


from common.data_helper import write_game_data_to_file, find_pgn_files

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
        self.buffer = []

    def start(self):
        """
        Start the actual training.
        """
        self.buffer = []
        # noinspection PyAttributeOutsideInit
        self.idx = 0
        start_time = time()
        with ProcessPoolExecutor(max_workers=7) as executor:
            games = self.get_games_from_all_files()
            for res in as_completed([executor.submit(get_buffer, self.config, game) for game in games]): #poisoned reference (memleak)
                self.idx += 1
                env, data = res.result()
                self.save_data(data)
                end_time = time()
                logger.debug(f'game {self.idx:4} time={(end_time - start_time):.3f}s '
                             f'n_steps={env.n_steps:3} {env.winner:12}')
                start_time = end_time

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

    def save_data(self, data):
        """

        :param (str,list(float)) data: a FEN encoded game state and a list where every index corresponds
            to a chess move. The move that was taken in the actual game is given a value (based on
            the player elo), all other moves are given a 0.
        """
        self.buffer += data
        if self.idx % self.config.playdata.sl_nb_game_in_file == 0:
            self.flush_buffer()

    def flush_buffer(self):
        """
        Clears out the moves loaded into the buffer and saves the to file.
        """
        rc = self.config.resource
        game_id = datetime.now().strftime("%Y%m%d-%H%M%S.%f")
        path = os.path.join(rc.play_data_dir, rc.play_data_filename_tmpl % game_id)
        logger.info(f"save play data to {path}")
        thread = Thread(target = write_game_data_to_file, args=(path, self.buffer))
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
    from piece import Camp
    from player import Playbook
    
    result = game['Result']
    moves = game['moves']
    red_elo, black_elo = int(game.get('RedElo', 100)), int(game.get('BlackElo', 100))
    red_weight = clip_elo_policy(config, red_elo)
    black_weight = clip_elo_policy(config, black_elo)
    
    players = {Camp.RED: Playbook(Camp.RED, moves[::2], result), Camp.BLACK: Playbook(Camp.BLACK, moves[1::2], result)}
    env = Env()
    for p in players.values():
        p.env = env

    ob = env.reset()
    while True:
        player = players[ob['next_player']]
        action = player.make_decision(**ob)
        ob, reward, done, info = env.step(action)
        if done:
            print(f'player {player.id.name}, reward: {reward}')
            break

    player = players[env.cur_player]
    player.finish_game(reward)
    oppo = players[env.cur_player.opponent()]
    oppo.finish_game(-reward)

    data = []
    for i in range(len(player.moves)):
        data.append(player.moves[i])
        if i < len(oppo.moves):
            data.append(oppo.moves[i])

    return env, data
