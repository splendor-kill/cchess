import os
import shutil
import signal
from time import sleep

import yaml


def load_cfg(file):
    with open(file) as f:
        if hasattr(yaml, 'FullLoader'):
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        else:
            cfg = yaml.load(f)
    return cfg


def dump_yaml(data, file_handle):
    yaml.dump(data, file_handle, default_flow_style=False)


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
