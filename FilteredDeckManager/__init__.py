# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

from .FilteredDeckManager import FilteredDeckManager
manager = FilteredDeckManager(mw)

def testFunction() -> None:
    # show a message box
    # showInfo("Card count: %d" % manager.CardCount())
    manager._GetAllDecks()
    manager.WriteToFile()
    import json
    decks = "Filtered Decks List:\n"
    for deck in manager.FilteredDecksList:
        decks = f"{decks}\n{deck.Name}"
    showInfo(decks)

# create a new menu item, "test"
action = QAction("Filtered Deck Manager", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)