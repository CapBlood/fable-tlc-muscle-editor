import os
from collections import OrderedDict

from lark import Lark, Transformer

from body_changer.muscle_config import BncfgConfig


class MuscleTreeToConfig(Transformer):
    def string(self, s):
        (s,) = s
        return str(s)
    
    def number(self, n):
        (n,) = n
        return float(n)
    
    def assign(self, n):
        return dict({
            n[0]: [*n[1:]]
        })

    def tag(self, n):
        return self.string(n)

    def tag_group(self, n):
        settings = OrderedDict()
        settings[(n[0], n[-1])] = OrderedDict()

        for line in n[1:-1]:
            settings[(n[0], n[-1])].update(line)

        return settings
    
    def main_group(self, lines):
        settings = OrderedDict()

        for line in lines:
            settings.update(line)

        return BncfgConfig(settings)


class MuscleParser:
    def __init__(self, lark_config_name: str, start_rule: str) -> None:
        root_file_path: str = os.path.dirname(os.path.realpath(__file__))
        lark_config_name: str = os.path.join(root_file_path, lark_config_name)

        with open(lark_config_name) as file:
            self.__parser: Lark = Lark(
                file.read(), start=start_rule)

    def parse(self, text: str) -> BncfgConfig:
        tree = self.__parser.parse(text)

        return MuscleTreeToConfig().transform(tree)


import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


muscle_parser = MuscleParser(resource_path("muscle.lark"), "main_group")
