"""
Various helper functions for working with the data used in this app
"""
import filecmp
import json
import os
import pathlib
from glob import glob
from logging import getLogger
from uuid import uuid4

logger = getLogger(__name__)


def find_pgn_files(directory, pattern='*.pgn'):
    dir_pattern = os.path.join(directory, pattern)
    files = list(sorted(glob(dir_pattern)))
    return files


def iter_pgn_files(directory, pattern='*.pgn'):
    return pathlib.Path(directory).glob(pattern)


def get_game_data_filenames(rc):
    pattern = os.path.join(rc.play_data_dir, rc.play_data_filename_tmpl % "*")
    files = list(sorted(glob(pattern)))
    return files


def get_next_gen_model_dirs(rc):
    dir_pattern = os.path.join(rc.next_gen_model_dir, rc.next_gen_model_dirname_tmpl % "*")
    dirs = list(sorted(glob(dir_pattern)))
    return dirs


def write_game_data_to_file(path, data, rc=None, **kwargs):
    try:
        with open(path, "wt") as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(e)

    if rc and rc.dist_play_data:
        from common.store_helper import get_store_util
        store_util = get_store_util(resource_config=rc)
        upload_replay_and_notify(store_util, rc, path, **kwargs)
        os.remove(path)


def read_game_data_from_file(path):
    try:
        with open(path, "rt") as f:
            return json.load(f)
    except Exception as e:
        logger.error('%s: %s', e, path)


def check_best_model_notifier(store_util, cfg):
    remote_path = os.path.join(cfg.s3_meta_dir, cfg.s3_best_model_notifier)
    local_path = os.path.join(cfg.data_dir, cfg.s3_best_model_notifier)
    local_path_new = local_path + '.new'
    try:
        store_util.load([(remote_path, local_path_new)])
        diff = not os.path.exists(local_path) or not filecmp.cmp(local_path, local_path_new)
        os.rename(local_path_new, local_path)
        with open(local_path) as f:
            content = json.load(f)
        return diff, content
    except Exception as e:
        logger.error(e)
        return False, None


def update_best_model_notifier(store_util, cfg, phase, did=0):
    notifier_local = os.path.join(cfg.data_dir, cfg.s3_best_model_notifier)
    content = {'phase': phase, 'id': did}
    with open(notifier_local, 'w') as f:
        json.dump(content, f)
    notifier_remote = os.path.join(cfg.s3_meta_dir, cfg.s3_best_model_notifier)
    store_util.save([(notifier_local, notifier_remote)])
    os.remove(notifier_local)


def check_play_data_notifier(store_util, cfg):
    remote_path = os.path.join(cfg.s3_meta_dir, cfg.s3_play_data_notifier)
    local_path = os.path.join(cfg.data_dir, cfg.s3_play_data_notifier)
    local_path_new = local_path + '.new'
    try:
        store_util.load([(remote_path, local_path_new)])
        if not os.path.exists(local_path):
            os.rename(local_path_new, local_path)
            return True
        eq = filecmp.cmp(local_path, local_path_new)
        os.rename(local_path_new, local_path)
        return not eq
    except Exception as e:
        logger.error(e)
        return None


def check_ng_model_notifier(store_util, cfg):
    remote_path = os.path.join(cfg.s3_meta_dir, cfg.s3_ng_model_notifier)
    local_path = os.path.join(cfg.data_dir, cfg.s3_ng_model_notifier)
    local_path_new = local_path + '.new'
    try:
        store_util.load([(remote_path, local_path_new)])
        if not os.path.exists(local_path):
            os.rename(local_path_new, local_path)
            return True
        eq = filecmp.cmp(local_path, local_path_new)
        os.rename(local_path_new, local_path)
        return not eq
    except Exception as e:
        logger.error(e)
        return None


def upload_replay_and_notify(store_util, cfg, path, did=None, time=None, digest=None, model_ver=None):
    logger.error('upload game replay')
    basename = os.path.basename(path)
    remote_path = os.path.join(cfg.play_data_dir_remote, basename)
    store_util.save([(path, remote_path)])

    info = {'file': basename, 'id': did, 'time': time,  # local time of sim, server time be better, but no API for it
            'digest': digest, 'based_model_version': model_ver}
    filename = f'{uuid4().hex}.json'
    path = os.path.join(cfg.data_dir, filename)
    with open(path, 'w') as f:
        json.dump(info, f)
    remote_path = os.path.join(cfg.s3_play_data_rec_dir, filename)
    store_util.save([(path, remote_path)])
    os.remove(path)

    notify = {'id': filename, 'time': time}
    path = os.path.join(cfg.data_dir, cfg.s3_play_data_notifier)
    with open(path, 'w') as f:
        json.dump(notify, f)
    notifier_remote = os.path.join(cfg.s3_meta_dir, cfg.s3_play_data_notifier)
    store_util.save([(path, notifier_remote)])
    # os.remove(path)  # potential bug, another proc is updating


def upload_ng_model_and_notify(store_util, cfg, path, time=None):
    info = {'model_dir': os.path.basename(path),
            'time': time,  # local time of sim, server time be better, but no API for it
            'digest': '', }
    filename = f'{uuid4().hex}.json'
    path = os.path.join(cfg.data_dir, filename)
    with open(path, 'w') as f:
        json.dump(info, f)
    remote_path = os.path.join(cfg.s3_model_rec_dir, filename)
    store_util.save([(path, remote_path)])
    os.remove(path)

    notify = {'id': filename, 'time': time}
    path = os.path.join(cfg.data_dir, cfg.s3_ng_model_notifier)
    with open(path, 'w') as f:
        json.dump(notify, f)
    notifier_remote = os.path.join(cfg.s3_meta_dir, cfg.s3_ng_model_notifier)
    store_util.save([(path, notifier_remote)])
    os.remove(path)
