from .ui_form import Ui_Dialog
from ..FilteredDeckManager import FilteredDeckManager

from aqt.qt import QDialog
from aqt.qt import QTableWidgetItem
from aqt.qt import QAbstractItemView
from aqt.qt import QFileDialog

from aqt.utils import qconnect

class MainUI(QDialog):
    def __init__(self, mw, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tableWidgetFilteredDecks.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.mainWindow = mw
        self.manager = FilteredDeckManager(self.mainWindow)
        self.SetupSignalsSlots()
    
    def InitializeData(self):
        self.manager._GetAllDecks()
        # self.manager.WriteToFile("C:\\Users\\goat1\\Documents\\output.json")
        self.PopulateDecks(self.manager.FilteredDecksList)

    def PopulateDecks(self, filteredDecksList):
        self.ui.tableWidgetFilteredDecks.setRowCount(len(filteredDecksList))
        i = 0
        for filteredDeck in filteredDecksList:
            self.ui.tableWidgetFilteredDecks.setItem(i, 0, QTableWidgetItem(filteredDeck.Name))
            self.ui.tableWidgetFilteredDecks.setItem(i, 1, QTableWidgetItem(filteredDeck.DeckId))
            i += 1
        self.ui.tableWidgetFilteredDecks.update()
    
    def SetupSignalsSlots(self):
        # self.ui.pushButtonExportAll.clicked.connect(self.WriteToFile)
        qconnect(self.ui.pushButtonExportAll.clicked, self.WriteAllToFile)
        qconnect(self.ui.buttonExportSelected.clicked, self.WriteSelectedToFile)

    def WriteAllToFile(self):
        filepath = QFileDialog.getSaveFileName(filter="JSON (*.json)")[0]
        self.manager.WriteToFile(filepath, self.manager.FilteredDecksList)
    
    def WriteSelectedToFile(self):
        """
        Writes the filtered decks selected in the filtered decks table to the file specified by the user.
        """
        selectedItems = self.ui.tableWidgetFilteredDecks.selectedIndexes()
        selectedItemsList = [x.row() for x in selectedItems]    # list format of every row, column selected
        selectedItemsListNonDuplicated = selectedItemsList[::2] # we only care about the row, so get every other element (since we have entire-row selection, where each row represents a Deck)
        selectedDeckIds = [int(self.ui.tableWidgetFilteredDecks.item(deckIndex, 1).text()) for deckIndex in selectedItemsListNonDuplicated]
        selectedDecks = []
        for deckId in selectedDeckIds:
            decks = [deck for deck in self.manager.FilteredDecksList if (int(deck.DeckId) == int(deckId))]
            selectedDecks.append(decks[0])
        filepath = QFileDialog.getSaveFileName(filter="JSON (*.json)")[0]
        self.manager.WriteToFile(filepath, selectedDecks)
        

if __name__ == "__main__":
    pass



# from aqt.qt import QTabWidget, QVBoxLayout, QLabel, QWidget, QFont, QGroupBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QCoreApplication, QMetaObject, QAbstractItemView