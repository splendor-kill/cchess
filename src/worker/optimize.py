"""
Encapsulates the worker which trains ChessModels using game data from recorded games from a file.
"""
import json
import os
import queue
import shutil
from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from glob import glob
from logging import getLogger
from multiprocessing import Process, Manager
from time import sleep

import numpy as np
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from xiangqi import Env, Camp

from agent.helper import flip_policy, testeval
from common.data_helper import get_game_data_filenames, read_game_data_from_file, upload_ng_model_and_notify, \
    check_play_data_notifier, check_best_model_notifier, untar
from common.store_helper import get_store_util
from common.utils import is_disk_enough, del_some_files
from model.helper import load_best_model_weight
from model.nn import NNModel

logger = getLogger(__name__)


def start(config):
    """
    Helper method which just kicks off the optimization using the specified config
    :param Config config: config to use
    """
    return OptimizeWorker(config).start()


class OptimizeWorker:
    """
    Worker which optimizes a ChessModel by training it on game data

    Attributes:
        :ivar Config config: config for this worker
        :ivar ChessModel model: model to train
        :ivar dequeue,dequeue,dequeue dataset: tuple of dequeues where each dequeue contains game states,
            target policy network values (calculated based on visit stats
                for each state during the game), and target value network values (calculated based on
                    who actually won the game after that state)
    """

    def __init__(self, config):
        self.config = config
        rc = self.config.resource
        os.makedirs(rc.model_dir, exist_ok=True)
        os.makedirs(rc.next_gen_model_dir, exist_ok=True)
        os.makedirs(rc.play_data_dir, exist_ok=True)
        self.store_util = get_store_util(resource_config=rc)
        self.model = None
        self.dataset = deque(), deque(), deque()
        self.m = Manager()
        self.filenames = self.m.Queue()
        self.handled_files = self.m.Queue()

    def start(self):
        """
        Load the next generation model from disk and start doing the training endlessly.
        """
        self.model = self.load_model()
        self.training()

    def training(self):
        """
        Does the actual training of the model, running it on game data. Endless.
        """
        self.compile_model()
        rc = self.config.resource

        files = get_game_data_filenames(rc) + self.get_zipped_filenames(rc)
        logger.info(f'there are {len(files)} sar files')
        for f in files:
            self.filenames.put_nowait(f)
        if rc.dist_play_data:
            controller = Process(target=wait_play_data_comming, args=(rc, self.filenames,), daemon=True)
            controller.start()

        total_steps = self.config.trainer.start_total_steps

        while True:
            self.fill_queue()
            steps = self.train_epoch(self.config.trainer.epoch_to_checkpoint)
            if steps == 0:
                sleep(1)
                continue
            total_steps += steps
            self.save_current_model()

            if rc.dist_play_data and not is_disk_enough(rc.disk_upper_limit):
                to_del = []
                while not self.handled_files.empty():
                    try:
                        to_del.append(self.handled_files.get_nowait())
                    except queue.Empty:
                        break
                del_some_files(to_del)

    def train_epoch(self, epochs):
        """
        Runs some number of epochs of training
        :param int epochs: number of epochs
        :return: number of datapoints that were trained on in total
        """
        tc = self.config.trainer
        state_ary, policy_ary, value_ary = self.collect_all_loaded_data()
        if state_ary.shape[0] == 0:
            return 0
        tensorboard_cb = TensorBoard(log_dir=self.config.resource.log_dir, batch_size=tc.batch_size, histogram_freq=1)
        self.model.model.fit(state_ary, [policy_ary, value_ary],
                             batch_size=tc.batch_size,
                             epochs=epochs,
                             shuffle=True,
                             validation_split=0.02,
                             callbacks=[tensorboard_cb])
        steps = (state_ary.shape[0] // tc.batch_size) * epochs
        return steps

    def compile_model(self):
        """
        Compiles the model to use optimizer and loss function tuned for supervised learning
        """
        opt = Adam()
        # avoid overfit for supervised
        losses = ['categorical_crossentropy', 'mean_squared_error']
        self.model.model.compile(optimizer=opt, loss=losses, loss_weights=self.config.trainer.loss_weights)

    def save_current_model(self):
        """
        Saves the current model as the next generation model to the appropriate directory
        """
        rc = self.config.resource
        model_id = datetime.now().strftime("%Y%m%d-%H%M%S.%f")
        model_dir = os.path.join(rc.next_gen_model_dir, rc.next_gen_model_dirname_tmpl % model_id)
        os.makedirs(model_dir, exist_ok=True)
        config_path = os.path.join(model_dir, rc.next_gen_model_config_filename)
        weight_path = os.path.join(model_dir, rc.next_gen_model_weight_filename)
        self.model.save(config_path, weight_path)
        if rc.dist_next_gen_model:
            self.model.upload(config_path, weight_path)
            upload_ng_model_and_notify(self.store_util, rc, path=model_dir, time=model_id)
            shutil.rmtree(model_dir)

    def fill_queue(self):
        """
        Fills the self.dataset queues with data from the training dataset.
        """
        n_workers = self.config.trainer.cleaning_processes
        with ProcessPoolExecutor(max_workers=n_workers) as executor:
            futures = []
            for _ in range(n_workers):
                if self.filenames.empty():
                    break
                try:
                    filename = self.filenames.get_nowait()
                except queue.Empty:
                    break
                futures.append(executor.submit(load_data_from_file, filename, self.handled_files, self.config))
            if not futures:
                for deq in self.dataset:
                    deq.clear()
                return
            while futures:
                future = next(as_completed(futures))
                futures.remove(future)
                if not self.filenames.empty():
                    try:
                        filename = self.filenames.get_nowait()
                    except queue.Empty:
                        pass
                    futures.append(executor.submit(load_data_from_file, filename, self.handled_files, self.config))
                sar = future.result()
                for x, y in zip(self.dataset, sar):
                    x.extend(y)
                del sar
                if len(self.dataset[0]) >= self.config.trainer.dataset_size:
                    break

    def collect_all_loaded_data(self):
        """
        :return: a tuple containing the data in self.dataset, split into
        (state, policy, and value).
        """
        state_ary, policy_ary, value_ary = self.dataset
        self.dataset = deque(), deque(), deque()
        state_ary1 = np.asarray(state_ary, dtype=np.float32)
        policy_ary1 = np.asarray(policy_ary, dtype=np.float32)
        value_ary1 = np.asarray(value_ary, dtype=np.float32)
        return state_ary1, policy_ary1, value_ary1

    def load_model(self):
        """
        Loads the next generation model from the appropriate directory. If not found, loads
        the best known model.
        """
        model = NNModel(self.config)
        rc = self.config.resource

        if self.config.model.distributed:
            while True:
                _, carrier = check_best_model_notifier(self.store_util, rc)
                if carrier is None:
                    logger.info('no model found')
                    sleep(1)
                    continue
                logger.debug(carrier)
                phase = carrier['phase']
                if phase in ('init_done', 'updated'):
                    logger.info('download model')
                    config_path = os.path.join(rc.model_dir, rc.model_best_config_path)
                    weight_path = os.path.join(rc.model_dir, rc.model_best_weight_path)
                    model.download(config_path, weight_path)
                    break
                else:  # in ('init', 'updating')
                    sleep(1)
                    continue

        if not load_best_model_weight(model):
            raise RuntimeError('load model failed.')
        return model

    def get_zipped_filenames(self, rc):
        pattern = os.path.join(rc.play_data_dir, '*.tar.gz')
        return glob(pattern)


def load_data_from_file(filename, handled_q, cfg):
    logger.debug(f"loading data from {filename}")
    suffix = '.tar.gz'
    is_tar = filename.endswith(suffix)
    if is_tar:
        untar(filename, cfg.resource.play_data_dir)
        filename_new = filename[:-len(suffix)] + '.json'
    data = read_game_data_from_file(filename_new)
    if is_tar:
        del_some_files([filename_new])
    handled_q.put_nowait(filename)
    if data is None:
        return np.array([], np.float32), np.array([], np.float32), np.array([], np.float32)
    return convert_to_cheating_data(data, cfg)


def convert_to_cheating_data(data, cfg):
    """
    :param data: format is SelfPlayWorker.buffer
    :return:
    """
    state_list = []
    policy_list = []
    value_list = []
    for state_fen, policy, value in data:
        env = Env(state_fen)
        state_planes = env.canonical_input_planes()

        if not env.cur_player == Camp.RED:
            policy = flip_policy(policy, cfg)

        move_number = int(state_fen.split(' ')[5])
        # reduces the noise of the opening... plz train faster
        value_certainty = min(5, move_number) / 5
        sl_value = value * value_certainty + testeval(state_fen, False) * (1 - value_certainty)

        state_list.append(state_planes)
        policy_list.append(policy)
        value_list.append(sl_value)

    return np.asarray(state_list, dtype=np.float32), \
           np.asarray(policy_list, dtype=np.float32), \
           np.asarray(value_list, dtype=np.float32)


def wait_play_data_comming(cfg, filename_q):
    from common.store_helper import get_store_util
    store_util = get_store_util(resource_config=cfg)
    all_files = set()
    while True:
        if not check_play_data_notifier(store_util, cfg):
            logger.info('check_play_data_notifier')
            sleep(1)
            continue
        proc = store_util.download_dirobj_async(cfg.s3_play_data_rec_dir, cfg.data_dir)
        proc.wait()
        files_at_now = set()
        path = os.path.join(cfg.data_dir, cfg.s3_play_data_rec_dir)
        files = os.listdir(path)
        for fn in files:
            with open(os.path.join(path, fn)) as f:
                content = json.load(f)
            files_at_now.add(content['file'])
        new_files = set(files_at_now).difference(all_files)
        logger.info(f'cur file num: {len(files_at_now)}, new: {len(new_files)}')

        downloads = [(os.path.join(cfg.play_data_dir_remote, f), os.path.join(cfg.play_data_dir, f)) for f in new_files]
        store_util.load(downloads)
        for rp, lp in downloads:
            filename_q.put_nowait(lp)
        all_files.update(new_files)
