"""
Encapsulates the worker which trains ChessModels using game data from recorded games from a file.
"""
import os
import shutil
import signal
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from logging import getLogger
from random import shuffle
from threading import Thread
from time import sleep

import numpy as np
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from xiangqi import Env, Camp

from agent.helper import flip_policy, testeval
from common.data_helper import get_game_data_filenames, read_game_data_from_file, get_next_generation_model_dirs
from common.store_helper import get_store_util
from model.helper import load_best_model_weight
from model.nn import NNModel

logger = getLogger(__name__)


def start(config):
    """
    Helper method which just kicks off the optimization using the specified config
    :param Config config: config to use
    """
    return OptimizeWorker(config).start()


def is_disk_enough(upper_limit):
    total, used, free = shutil.disk_usage('.')
    # print('disk usage:', used / total)
    return used / total < upper_limit


def check_disk_usage(pid, upper_limit):
    while True:
        sleep(1.)
        try:
            if not is_disk_enough(upper_limit):
                # print('download pause')
                os.kill(pid, signal.SIGSTOP)
            else:
                # print('download continue')
                os.kill(pid, signal.SIGCONT)
        except:
            pass


def del_some_files(obsolete_files):
    for file in obsolete_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


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
        :ivar ProcessPoolExecutor executor: executor for running all of the training processes
    """

    def __init__(self, config):
        self.config = config
        self.model = None
        self.dataset = deque(), deque(), deque()
        self.executor = ProcessPoolExecutor(max_workers=config.trainer.cleaning_processes)
        self.filenames = deque()

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
        if rc.dist_play_data:
            store_util = get_store_util(resource_config=rc)
            # put remote dir object under the parent dir, keep local name same as remote name in config
            local_path = os.path.dirname(rc.play_data_dir)
            os.makedirs(local_path, exist_ok=True)
            proc_download = store_util.download_dirobj_async(rc.play_data_dir_remote, local_path)
            controller = Thread(target=check_disk_usage, args=(proc_download.pid, rc.play_data_upper_limit))
            controller.start()

        files = get_game_data_filenames(rc)
        min_n = max(self.config.trainer.min_data_size_to_learn, 3)
        while rc.dist_play_data and len(files) < min_n:  # wait for download more files
            sleep(60)
            files = get_game_data_filenames(rc)

        downloaded_files = set(files)
        self.filenames.extend(files)
        shuffle(self.filenames)
        total_steps = self.config.trainer.start_total_steps

        while True:
            self.fill_queue()
            steps = self.train_epoch(self.config.trainer.epoch_to_checkpoint)
            total_steps += steps
            self.save_current_model()
            a, b, c = self.dataset
            while len(a) > self.config.trainer.dataset_size / 2:
                a.popleft()
                b.popleft()
                c.popleft()

            if rc.dist_play_data:
                files = get_game_data_filenames(rc)
                new_files = set(files).difference(downloaded_files)
                self.filenames.extend(new_files)
                downloaded_files.update(new_files)
                handled_files = downloaded_files.difference(set(self.filenames))
                if not is_disk_enough(rc.play_data_upper_limit):
                    del_some_files(handled_files)

    def train_epoch(self, epochs):
        """
        Runs some number of epochs of training
        :param int epochs: number of epochs
        :return: number of datapoints that were trained on in total
        """
        tc = self.config.trainer
        state_ary, policy_ary, value_ary = self.collect_all_loaded_data()
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
        model_dir = os.path.join(rc.next_generation_model_dir, rc.next_generation_model_dirname_tmpl % model_id)
        os.makedirs(model_dir, exist_ok=True)
        config_path = os.path.join(model_dir, rc.next_generation_model_config_filename)
        weight_path = os.path.join(model_dir, rc.next_generation_model_weight_filename)
        self.model.save(config_path, weight_path)

    def fill_queue(self):
        """
        Fills the self.dataset queues with data from the training dataset.
        """
        futures = deque()
        with ProcessPoolExecutor(max_workers=self.config.trainer.cleaning_processes) as executor:
            for _ in range(self.config.trainer.cleaning_processes):
                if len(self.filenames) == 0:
                    break
                filename = self.filenames.popleft()
                logger.debug(f"loading data from {filename}")
                futures.append(executor.submit(load_data_from_file, filename))
            while futures and len(self.dataset[0]) < self.config.trainer.dataset_size:
                for x, y in zip(self.dataset, futures.popleft().result()):
                    x.extend(y)
                if len(self.filenames) > 0:
                    filename = self.filenames.popleft()
                    logger.debug(f"loading data from {filename}")
                    futures.append(executor.submit(load_data_from_file, filename))

    def collect_all_loaded_data(self):
        """
        :return: a tuple containing the data in self.dataset, split into
        (state, policy, and value).
        """
        state_ary, policy_ary, value_ary = self.dataset

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

        dirs = get_next_generation_model_dirs(rc)
        if not dirs:
            logger.debug("loading best model")
            if not load_best_model_weight(model):
                raise RuntimeError("Best model can not loaded!")
        else:
            latest_dir = dirs[-1]
            logger.debug("loading latest model")
            config_path = os.path.join(latest_dir, rc.next_generation_model_config_filename)
            weight_path = os.path.join(latest_dir, rc.next_generation_model_weight_filename)
            model.load(config_path, weight_path)
        return model


def load_data_from_file(filename):
    data = read_game_data_from_file(filename)
    return convert_to_cheating_data(data)


def convert_to_cheating_data(data):
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
            policy = flip_policy(policy)

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
