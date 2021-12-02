import numpy as np


def flip_policy(pol, cfg):
    return np.asarray([pol[ind] for ind in cfg.unflipped_index])
