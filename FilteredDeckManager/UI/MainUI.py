from .ui_form import Ui_Dialog

from aqt.qt import QDialog

class MainUI(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)