# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

from .UI import MainUI
dialogUI = MainUI.MainUI(mw)

def testFunction() -> None:
    dialogUI.InitializeData()
    dialogUI.exec()

# create a new menu item, "test"
action = QAction("Filtered Deck Manager", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)