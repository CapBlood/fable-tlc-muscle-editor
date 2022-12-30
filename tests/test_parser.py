import unittest
from unittest.mock import patch

from fs.tempfs import TempFS

from body_changer.muscle_changer import MuscleChanger


class TestParser(unittest.TestCase):
    def test_multiply(self):
        parser = MuscleChanger("bncfg_examples", "muscle.lark")
        tmp_fs = TempFS()
        
        tmp_fs.makedirs("data/bones/", recreate=True)
        with open("bncfg_examples/hero_strong.bncfg", "rb") as file:
            tmp_fs.writefile("data/bones/hero_strong.bncfg", file)

        with patch.object(parser, '_MuscleChanger__root_fs', tmp_fs):
            parser.multiply_file_bones([1.0, 1.0, 1.0])

        with tmp_fs.open("data/bones/hero_strong_new.bncfg") as file_1, tmp_fs.open("data/bones/hero_strong.bncfg") as file_2:
            self.assertEqual(
                file_1.read(), file_2.read())

        tmp_fs.close()
