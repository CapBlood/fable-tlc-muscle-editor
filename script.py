import re
import os
from typing import List

# Original
# mapper = {
#     "Finger": "1.1, 1.35, 1.4;",
#     "Upper Arm": "1.0, 1.7, 1.65;",
#     "Toe": "1.0, 1.35, 1.35;",
#     "Hand": "1.1, 1.35, 1.4;",
#     "Foot": "1.0, 1.35, 1.35;",
#     "Calf": "1.0, 1.4, 1.55;",
#     "Thigh": "1.0, 1.65, 1.35;",
#     "Pelvis": "1.0, 1.35, 1.25;",
#     "Forearm": "1.0, 1.7, 1.7;",
#     "Clavicle": "1.35, 1.3, 1.6;",

#     "Spine": "1.0, 1.0, 1.45;",
#     "Spine1": "1.0, 1.25, 1.25;",
#     "Spine2": "1.0, 1.25, 1.25;",
#     "Spine3": "1.05, 1.4, 1.3;",

#     "Neck": "1.0, 1.0, 2.449999;",
#     "Neck1": "1.1, 1.5, 1.65;"
# }

# Modded
# mapper = {
#     "Finger": "1.05, 1.18, 1.2;",
#     "Upper Arm": "1.0, 1.18, 1.13;",
#     "Toe": "1.0, 1.15, 1.1;",
#     "Hand": "1.0, 1.0, 1.18;",
#     "Foot": "1.0, 1.05, 1.05;",

#     "Calf": "1.0, 1.1, 1.23;",
#     "Thigh": "1.0, 1.23, 1.28;",

#     "Pelvis": "1.0, 1.18, 1.18;",
#     "Forearm": "1.0, 1.28, 1.28;",
#     "Clavicle": "1.18, 1.05, 1.08;",

#     "Spine": "1.0, 1.0, 1.23;",
#     "Spine1": "1.0, 1.05, 1.05;",
#     "Spine2": "1.0, 1.05, 1.03;",
#     "Spine3": "1.0, 1.08, 1.1;",

#     "Neck": "1.0, 0.93, 1.65;",
#     "Neck1": "1.1, 1.5, 1.35;"
# }

# My
mapper = {
    "Finger": "1.05, 1.18, 1.2;",
    "Upper Arm": "1.0, 1.18, 1.13;",
    "Toe": "1.0, 1.15, 1.1;",
    "Hand": "1.0, 1.0, 1.18;",
    "Foot": "1.0, 1.05, 1.05;",

    "Calf": "1.0, 1.1, 1.23;",
    "Thigh": "1.0, 1.23, 1.28;",

    "Pelvis": "1.0, 1.18, 1.18;",
    "Forearm": "1.0, 1.28, 1.28;",
    "Clavicle": "1.18, 1.05, 1.08;",

    "Spine": "1.0, 1.0, 1.23;",
    "Spine1": "1.0, 1.05, 1.05;",
    "Spine2": "1.0, 1.05, 1.03;",
    "Spine3": "1.0, 1.08, 1.1;",

    "Neck": "1.0, 0.93, 1.65;",
    "Neck1": "1.1, 1.5, 1.35;"
}

patterns = {
    # Симметричные
    "Finger": "([ \w]+Finger[0-9]*: )([^;]+)",
    "Upper Arm": "([ \w]+UpperArm[0-9]*: )([^;]+)",
    "Hand": "([ \w]+Hand[0-9]*: )([^;]+)",
    "Foot": "([ \w]+Foot[0-9]*: )([^;]+)",
    "Forearm": "([ \w]+Forearm[0-9]*: )([^;]+)",
    "Toe": "([ \w]+Toe[0-9]*: )([^;]+)",
    "Calf": "([ \w]+Calf[0-9]*: )([^;]+)",
    "Clavicle": "([ \w]+Clavicle[0-9]*: )([^;]+)",
    "Thigh": "([ \w]+Thigh[0-9]*: )([^;]+)",

    # Несимметричные
    "Pelvis": "([ \w]+Pelvis[0-9]*: )([^;]+)",
    
    "Spine": "([ \w]+Spine: )([^;]+)",
    "Spine1": "([ \w]+Spine1: )([^;]+)",
    "Spine2": "([ \w]+Spine2: )([^;]+)",
    "Spine3": "([ \w]+Spine3: )([^;]+)",
    
    "Neck": "([ \w]+Neck: )([^;]+)",
    "Neck1": "([ \w]+Neck1: )([^;]+)"
}
# COEF = 0.9
# [высота ГГ, ширина тела в направлении взгляда, ширина тела вбок]
COEF = [1, 1.071, 1.071]

def parse_nums(line: str) -> List[float]:
    pattern = ";|,"
    nums = list(map(float, filter(None, re.split(pattern, line))))
    return nums

def render_nums(nums: List[float]) -> str:
    rendered_nums = ", ".join(map(str, nums)) + ";"
    return rendered_nums

def multiply_coef(nums: List[float]) -> List[float]:
    # return list(map(lambda x: x * COEF, nums))
    return list(map(lambda x, coef: x * coef, nums, COEF))

def change_value(line):
    return render_nums(multiply_coef(parse_nums(line)))


def replace(line):
    for name, pattern in patterns.items():
        result = re.search(pattern, line)
        
        if result:
            base_name = result.group(1)
            value = change_value(mapper[name])
            
            return base_name + value  + "\n"
    
    print(f"Не найден шаблон: {line}")
    return line


def process_file(file, offset_line, file_out):
    processed_text = ""
    for _ in range(offset_line):
        processed_text += next(file)
        # processed_text += "\n"

    for line in file:
        processed_text += replace(line)
        # processed_text += "\n"

    with open(file_out, "w") as file:
        file.write(processed_text)


os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("hero_strong.bncfg") as file:
    process_file(file, 12, "hero_strong.bncfg")
