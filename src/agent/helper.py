import numpy as np

from config import cfg


def flip_policy(pol):
    return np.asarray([pol[ind] for ind in cfg.unflipped_index])
