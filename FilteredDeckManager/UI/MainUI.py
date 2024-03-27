from .ui_form import Ui_Dialog
from ..FilteredDeckManager import FilteredDeckManager
from ..Models import Deck

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
        self.ui.tableWidgetStagedForImportFilteredDecks.hide()
        self.mainWindow = mw
        self.manager = FilteredDeckManager(self.mainWindow)
        self.SetupSignalsSlots()
    
    def InitializeData(self) -> None:
        """
        Triggers query of filtered decks from the Anki API using the `FilteredDeckManager`.
        """
        self.manager._GetAllDecks()
        self.PopulateDecks(self.manager.FilteredDecksList)

    def PopulateDecks(self, filteredDecksList: list) ->None:
        """
        Populates the central table with a list of filtered decks (Deck Name and Deck Id).
        """
        self.ui.tableWidgetFilteredDecks.setRowCount(len(filteredDecksList))
        i = 0
        for filteredDeck in filteredDecksList:
            self.ui.tableWidgetFilteredDecks.setItem(i, 0, QTableWidgetItem(filteredDeck.Name))
            self.ui.tableWidgetFilteredDecks.setItem(i, 1, QTableWidgetItem(filteredDeck.DeckId))
            i += 1
        self.ui.tableWidgetFilteredDecks.update()
    
    def SetupSignalsSlots(self) -> None:
        """
        Sets up Qt signals/slots for `MainUI`, primarily for button presses..
        """
        qconnect(self.ui.pushButtonExportAll.clicked, self.WriteAllToFile)
        qconnect(self.ui.buttonExportSelected.clicked, self.WriteSelectedToFile)
        qconnect(self.ui.buttonImport.clicked, self.ImportFromFile)
        qconnect(self.ui.buttonOkay.clicked, self.CreateFilteredDecksFromImported)
        qconnect(self.ui.buttonExit.clicked, self.ExitDialog)
    
    def ImportFromFile(self) -> None:
        """
        Import filtered decks from file and populate in UI.
        """
        filepath = QFileDialog.getOpenFileName(self, caption="Import", filter="JSON (*.json)")[0]
        print(filepath)
        importedFilteredDecksList = self.manager.ReadFromFile(filepath)
        self.PopulateImportedFilteredDecks(importedFilteredDecksList)
    
    def PopulateImportedFilteredDecks(self, importedFilteredDecksList: list) -> None:
        """
        Populates imported filtered decks into the corresponding QTableWidget.
        """
        self.ui.tableWidgetStagedForImportFilteredDecks.setRowCount(len(importedFilteredDecksList))
        i = 0
        for importedFilteredDeck in importedFilteredDecksList:
            print(f"Adding: {importedFilteredDeck.Name}")
            self.ui.tableWidgetStagedForImportFilteredDecks.setItem(i, 0, QTableWidgetItem(importedFilteredDeck.Name))
            self.ui.tableWidgetStagedForImportFilteredDecks.setItem(i, 1, QTableWidgetItem(str(20)))
            self.ui.tableWidgetStagedForImportFilteredDecks.setItem(i, 2, QTableWidgetItem(importedFilteredDeck.SearchTerms[0]))
            i += 1
        self.ui.tableWidgetStagedForImportFilteredDecks.update()
        self.ui.tableWidgetStagedForImportFilteredDecks.show()
    
    def CreateFilteredDecksFromImported(self) -> None:
        from anki.collection import SearchNode
        from anki.decks import FilteredDeckConfig
        from anki.scheduler import FilteredDeckForUpdate
        from aqt.operations.scheduling import add_or_update_filtered_deck
        importedFilteredDecksList = self.manager.StagedFilteredDecksList
        for deck in importedFilteredDecksList:
            newDeckId = self.mainWindow.col.decks.new_filtered(deck.Name)
            newDeck = self.mainWindow.col.decks.get(newDeckId)
            newDeck["terms"] = [[deck.SearchTerms[0], 9999, 6]]
            self.mainWindow.col.decks.save(newDeck)
            self.mainWindow.col.sched.rebuildDyn(newDeckId)
        self.mainWindow.reset()
        self.ExitDialog()
                

    def ExitDialog(self) -> None:
        self.close()

    def WriteAllToFile(self) -> None:
        """
        Writes all filtered decks in the filtered decks table to the file specified by the user.
        """
        filepath = QFileDialog.getSaveFileName(filter="JSON (*.json)")[0]
        self.manager.WriteToFile(filepath, self.manager.FilteredDecksList)
    
    def WriteSelectedToFile(self) -> None:
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