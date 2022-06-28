"""
Various helper functions for working with the data used in this app
"""

import json
import os
from glob import glob
from logging import getLogger

logger = getLogger(__name__)


def find_pgn_files(directory, pattern='*.pgn'):
    dir_pattern = os.path.join(directory, pattern)
    files = list(sorted(glob(dir_pattern)))
    return files


def get_game_data_filenames(rc):
    pattern = os.path.join(rc.play_data_dir, rc.play_data_filename_tmpl % "*")
    files = list(sorted(glob(pattern)))
    return files


def get_next_generation_model_dirs(rc):
    dir_pattern = os.path.join(rc.next_generation_model_dir, rc.next_generation_model_dirname_tmpl % "*")
    dirs = list(sorted(glob(dir_pattern)))
    return dirs


def write_game_data_to_file(path, data, rc=None):
    try:
        with open(path, "wt") as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(e)

    if rc and rc.dist_play_data:
        from common.store_helper import get_store_util
        store_util = get_store_util(resource_config=rc)
        remote_path = path.replace(rc.play_data_dir, rc.play_data_dir_remote)
        try:
            store_util.save([(path, remote_path)])
        except Exception as e:
            logger.error(e)


def read_game_data_from_file(path):
    try:
        with open(path, "rt") as f:
            return json.load(f)
    except Exception as e:
        logger.error(e)
