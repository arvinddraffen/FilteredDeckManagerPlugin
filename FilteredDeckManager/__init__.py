# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import qconnect
# import all of the Qt GUI library
from aqt.qt import *


from .UI import MainUI
dialogUI = MainUI.MainUI(mw)

def launch() -> None:
    dialogUI.InitializeData()
    dialogUI.exec()

action = QAction("Filtered Deck Manager", mw)
qconnect(action.triggered, launch)
# and add it to the tools menu
mw.form.menuTools.addAction(action)