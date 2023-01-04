import sys

from PySide6.QtWidgets import (
    QMainWindow, QApplication, QFileDialog, QMessageBox, QItemDelegate, QPushButton,
    QStyledItemDelegate, QStyleOptionButton, QStyle, QTreeWidgetItem, QAbstractItemView,
    QWidget, QHBoxLayout, QLineEdit, QToolButton, QInputDialog
)
from PySide6.QtCore import Signal, Qt, QEvent, QModelIndex, QRect, QPoint
from PySide6.QtGui import QBrush, QPen, QColor, QStandardItemModel, QStandardItem, QPalette


from body_changer.ui.setup_main_window import Ui_MainWindow
from body_changer.config_manager import BncfgManager
from body_changer.ui.editor import Editor


class Delegate(QStyledItemDelegate):
    activated = Signal(QModelIndex)

    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            painter.save()
            painter.setBrush(Qt.darkBlue)
            painter.fillRect(option.rect, painter.brush())
            painter.restore()

        widget = option.widget
        style = widget.style() if widget else QApplication.style()
        opt = QStyleOptionButton()
        opt.rect = option.rect
        opt.text = index.data()
        opt.state = option.state
        opt.state |= QStyle.State_On if index.data(Qt.CheckStateRole) == Qt.Checked else QStyle.State_Off
        style.drawControl(QStyle.CE_RadioButton, opt, painter, widget)


    def editorEvent(self, event, model, option, index):
        value = QStyledItemDelegate.editorEvent(self, event, model, option, index)
        if value:
            if event.type() == QEvent.MouseButtonRelease:
                parent = index.parent()
                for i in range(model.rowCount(parent)):
                    if i != index.row():
                        ix = model.index(i, 0, parent)
                        model.setData(ix, Qt.Unchecked, Qt.CheckStateRole)
                    else:
                        ix = model.index(i, 0, parent)
                        model.setData(ix, Qt.Checked, Qt.CheckStateRole)
                        self.activated.emit(ix)


        return value



class MainWindow(QMainWindow, Ui_MainWindow):
    manager = None
    selected_root = Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.select_root)
        self.selected_root.connect(self.update_profile_list)
        self.lineEdit.setEnabled(False)

        def set_selection(index: QModelIndex):
            self.listView.setCurrentIndex(index)

        self.delegate = Delegate()
        self.delegate.activated.connect(set_selection)
        self.delegate.activated.connect(self.activate_profile)
        self.listView.setModel(QStandardItemModel())
        self.listView.setItemDelegate(self.delegate)

        self.pushButton_5.clicked.connect(self.export_profile)
        self.pushButton_4.clicked.connect(self.update_profile_list)
        self.pushButton_2.clicked.connect(self.edit_profile)
        self.pushButton_3.clicked.connect(self.create_profile)
        self.pushButton_6.clicked.connect(self.delete_profile)
        
    def select_root(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Choose directory")
        
        if not path:
            return
        
        self.lineEdit.setText(path)
        self.selected_root.emit()

    def activate_profile(self, index: QModelIndex) -> None:
        profile_name = index.data(Qt.DisplayRole)
        self.manager.activate_config(profile_name)

    def create_profile(self) -> None:
        if self.manager is None:
            QMessageBox.critical(self, "Error", "Choose game directory")
            return 

        profile_name, success = QInputDialog.getText(self, "Create profile", "Enter a name")

        if not success:
            QMessageBox.critical(self, "Error", "Incorrect name")
            return 

        self.manager.set_config(
            profile_name, self.manager.get_config("default")
        )
        self.update_profile_list()

    def delete_profile(self) -> None:
        if self.manager is None:
            QMessageBox.critical(self, "Error", "Choose game directory")
            return 

        selected_indexes = self.listView.selectionModel().selectedIndexes()
        
        if len(selected_indexes) == 0:
            QMessageBox.critical(self, "Error", "Choose profile to edit")
            return

        selected_index = selected_indexes[0]
        profile_name = selected_index.data(Qt.DisplayRole)

        self.manager.delete_config(profile_name)
        self.update_profile_list()

    def edit_profile(self) -> None:
        selected_indexes = self.listView.selectionModel().selectedIndexes()
        
        if len(selected_indexes) == 0:
            QMessageBox.critical(self, "Error", "Choose profile to edit")
            return

        selected_index = selected_indexes[0]
        profile_name = selected_index.data(Qt.DisplayRole)
        config = self.manager.get_config(profile_name)
        edited_config, is_save = Editor.edit_config(config)
        if is_save:
            self.manager.set_config(profile_name, edited_config)
        self.update_profile_list()

    def export_profile(self) -> None:
        selected_indexes = self.listView.selectionModel().selectedIndexes()
        
        if len(selected_indexes) == 0:
            QMessageBox.critical(self, "Error", "Choose profile to export")
            return

        selected_index = selected_indexes[0]
        profile_name = selected_index.data(Qt.DisplayRole)
        
        path = QFileDialog.getExistingDirectory(self, "Choose directory to export")

        self.manager.export_bncfg(profile_name, path)

        QMessageBox.information(self, "Export", "Profile exported!")
        
    def update_profile_list(self) -> None:
        try:
            self.manager = BncfgManager(self.lineEdit.text())
        except:
            QMessageBox.critical(self, "Error", "Incorrect game directory")
            return

        profiles = self.manager.get_available_configs()
        model = self.listView.model()
        model.clear()
        for profile in profiles:
            item = QStandardItem(profile)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            model.appendRow(item)

    

def main() -> None:
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()