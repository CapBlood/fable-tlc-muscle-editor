from collections import OrderedDict
from typing import Union, Tuple, List


class BncfgConfig:
    KEYS_MAPPER = {
        ('#Start_group_settings', '#End_group_settings'): "bones_group",
        ('#Start_Bone_data', '#End_bone_data'): "bones_data"
    }

    def __init__(self, group: OrderedDict) -> None:
        self.group: OrderedDict = self.__process(group)

    def __str__(self) -> str:
        return str(self.group)

    def __repr__(self) -> str:
        return repr(self.group)

    def __getitem__(self, key: str):
        return self.group[key]

    def __setitem__(self, key: str, value) -> None:
        self.group[key] = value

    def __process(self, group: OrderedDict) -> OrderedDict:
        processed_group = OrderedDict()

        for name, value in group.items():
            if isinstance(value, OrderedDict):
                if len(name) != 2:
                    raise Exception("Inner groups must have a tuple of str as keys")

                sub_group_name = self.KEYS_MAPPER.get(name, name)
                processed_group[sub_group_name] = TaggedBncfgGroup(value, name)
            else:
                processed_group[name] = value

        return processed_group

    def items(self) -> Tuple:
        return tuple(self.group.items())

    def to_bncfg(self, end_line="\r\n") -> str:
        text: str = ""

        for name, value in self.group.items():
            if isinstance(value, BncfgConfig):
                text += value.to_bncfg(end_line)
            else:
                text += "{}: {};{}".format(
                    name, ", ".join(map(str, value)),
                    end_line)
        
        return text


class TaggedBncfgGroup(BncfgConfig):
    def __init__(self, group: OrderedDict, tags: Tuple[str, str]) -> None:
        super().__init__(group)
        self.begin_tag = tags[0]
        self.end_tag = tags[1]

    def to_bncfg(self, end_line="\r\n") -> str:
        text: str = "{}{}".format(self.begin_tag, end_line)
        text += super().to_bncfg(end_line)
        text += "{}{}".format(self.end_tag, end_line)

        return text 