from typing import List

from fs import open_fs
from fs.base import FS

from body_changer.muscle_config import BncfgConfig
from body_changer.muscle_parser import muscle_parser


class BncfgManager:
    def __init__(self, root_path: str) -> None:
        self.__root_fs: FS = open_fs(root_path)
        self.__init_env()

    def __init_env(self) -> None:
        if not self.__root_fs.exists("data/bones/configs"):
            self.__root_fs.makedir("data/bones/configs")

        if self.__root_fs.exists("data/bones/configs/default.bncfg"):
            return

        if not self.__root_fs.exists("data/bones/hero_strong.bncfg"):
            raise FileNotFoundError(
                "Не найден оригинальный конфигурационный файл hero_strong.bncfg")

        with self.__root_fs.open("data/bones/hero_strong.bncfg") as file:
            self.import_bncfg("default", muscle_parser.parse(file.read()))

    def get_available_configs(self) -> List[str]:
        return list(map(
            lambda config_name: config_name[:config_name.rindex(".")], 
            self.__root_fs.listdir("data/bones/configs")
        ))

    def get_config(self, name_config: str) -> BncfgConfig:
        with self.__root_fs.open(
            "data/bones/configs/{}.bncfg".format(name_config)) as file:
            file_content = file.read()

        return muscle_parser.parse(file_content)

    def activate_config(self, name_config: str) -> None:
        config = self.get_config(name_config)

        with self.__root_fs.open(
            "data/bones/hero_strong.bncfg", "w") as file:
            file.write(config.to_bncfg())

    def import_bncfg(self, name_config: str, config: BncfgConfig) -> None:
        with self.__root_fs.open(
            "data/bones/configs/{}.bncfg".format(name_config), "w") as file:
            file.write(config.to_bncfg())

    def export_bncfg(self, name_config: str, path: str) -> None:
        config = self.get_config(name_config)

        with open("{}/{}.bncfg".format(path, name_config), "w") as file:
            file.write(config.to_bncfg())


if __name__ == "__main__":
    manager = BncfgManager("tmp/")

    # with open("bncfg_examples/hero_strong.bncfg") as file:
    #     manager.import_bncfg("my", muscle_parser.parse(file.read()))

    print(manager.get_available_configs())
    manager.activate_config("my")
    # manager.export_bncfg("my", ".")
    # print(manager.get_config("default").to_bncfg())
