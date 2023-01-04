import numpy as np
from PySide6.QtWidgets import QDialog, QMessageBox

from body_changer.ui.setup_editor import Ui_Form
from body_changer.muscle_config import BncfgConfig
from body_changer.muscle_utils import non_proportional_mul_bones


class Editor(QDialog, Ui_Form):
    def __init__(self, config: BncfgConfig, *args, **kwargs) -> None:
        QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.__config = config
        self.update_config(config)
        self.__edited_config = self.__config
        self.is_save = False
        
        self.lineEdit.setText("1")
        self.lineEdit_2.setText("1")
        self.lineEdit_3.setText("1")
        self.pushButton.clicked.connect(self.change_bones)
        self.pushButton_2.clicked.connect(self.save_config)
        self.pushButton_4.clicked.connect(self.cancel_config)

    def update_config(self, config: BncfgConfig):
        self.set_text(config.to_bncfg())

    def config(self):
        return self.__config

    def cancel_config(self):
        self.__edited_config = self.__config
        self.update_config(self.__config)

    def save_config(self):
        self.__config = self.__edited_config
        self.is_save = True
        QMessageBox.information(self, "Save", "Config saved")
        self.close()

    def change_bones(self):
        height_text = self.lineEdit.text()
        direct_width_text = self.lineEdit_2.text()
        side_width_text = self.lineEdit_3.text()

        if not height_text or not direct_width_text or not side_width_text:
            QMessageBox.critical(self, "Error", "Incorrect multipliers")
            return

        height = float(height_text)
        direct_width = float(direct_width_text)
        side_width = float(side_width_text)

        new_config = non_proportional_mul_bones(
            self.__config, np.array([height, direct_width, side_width]))
        self.__edited_config = new_config
        self.update_config(self.__edited_config)

    def set_text(self, text: str) -> None:
        self.textBrowser.setText(text)

    @staticmethod
    def edit_config(config: BncfgConfig) -> BncfgConfig:
        editor = Editor(config)
        editor.exec()
        return editor.config(), editor.is_save

