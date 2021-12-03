import numpy as np


def flip_policy(pol, cfg):
    return np.asarray([pol[ind] for ind in cfg.unflipped_index])


def flip_ucci_labels(labels):
    def repl(x):
        return "".join([(str(9 - int(a)) if a.isdigit() else a) for a in x])
    return [repl(x) for x in labels]
