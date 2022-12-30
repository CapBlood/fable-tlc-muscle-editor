import numpy as np
from fs import open_fs
from fs.base import FS

from body_changer.muscle_config import BncfgConfig
from body_changer.muscle_parser import MuscleParser
from body_changer.muscle_utils import non_proportional_mul_bones


class MuscleChanger:
    def __init__(self, root_path: str, lark_config_name: str, start_rule: str='main_group') -> None:
        self.__root_fs: FS = open_fs(root_path)
        self.__parser = MuscleParser(lark_config_name, start_rule)

    def set_root(self, root_path: str) -> None:
        self.__root_fs = open_fs(root_path)

    def multiply_file_bones(self, coefs: np.ndarray) -> None:
        with self.__root_fs.open("data/bones/hero_strong.bncfg") as file:
            config: BncfgConfig = self.__parser.parse(file.read())
            new_config: BncfgConfig = non_proportional_mul_bones(config, coefs)

        with self.__root_fs.open("data/bones/hero_strong_new.bncfg", "w") as file:
            file.write(new_config.to_bncfg())
