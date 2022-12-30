from copy import deepcopy

import numpy as np

from body_changer.muscle_config import BncfgConfig


def non_proportional_mul_bones(config: BncfgConfig, coefs: np.ndarray) -> BncfgConfig:
    config = deepcopy(config)

    for name, scales in config["bones_data"].items():
        config["bones_data"][name] = (np.array(scales) * coefs).tolist()

    return config
