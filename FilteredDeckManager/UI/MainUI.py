from aqt import QCheckBox, QTableWidget
from .ui_form import Ui_Dialog
from ..FilteredDeckManager import FilteredDeckManager
from ..Models import Deck
from ..Utilities import Constants

from aqt.qt import QDialog
from aqt.qt import QTableWidgetItem
from aqt.qt import QAbstractItemView
from aqt.qt import QFileDialog
from aqt.qt import QMessageBox
from aqt.qt import QAbstractItemView
from aqt.qt import Qt
from aqt.qt import QUrl

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
        self.SetupAboutTab()
    
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
            checkboxSelected = QCheckBox(self.ui.tableWidgetFilteredDecks)
            self.ui.tableWidgetFilteredDecks.setCellWidget(i, Constants.UI_CONSTANTS.FilteredDeckTableWidgetColumns.SELECT_CHECKBOX.value, checkboxSelected)
            self.ui.tableWidgetFilteredDecks.setItem(i, Constants.UI_CONSTANTS.FilteredDeckTableWidgetColumns.DECK_NAME.value, QTableWidgetItem(filteredDeck.Name))
            self.ui.tableWidgetFilteredDecks.setItem(i, Constants.UI_CONSTANTS.FilteredDeckTableWidgetColumns.DECK_ID.value, QTableWidgetItem(filteredDeck.DeckId))
            i += 1
        self.ui.tableWidgetFilteredDecks.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
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
        qconnect(self.rejected, self.ExitDialog)
    
    def SetupAboutTab(self) -> None:
        import datetime
        from pathlib import Path
        self.ui.labelWrittenBy.setText(f"{self.ui.labelWrittenBy.text()} Arvind Draffen, {datetime.date.today().year}.")
        readmePath = (Path(__file__).parent.parent).joinpath('Utilities').joinpath('Data').joinpath('AboutText.md')
        self.ui.textBrowser.setSource(QUrl.fromLocalFile(f"{readmePath}"))

    def ImportFromFile(self) -> None:
        """
        Import filtered decks from file and populate in UI.
        """
        filepath = QFileDialog.getOpenFileName(self, caption="Import", filter="JSON (*.json)")[0]
        print(filepath)
        importedFilteredDecksList = self.manager.ReadFromFile(filepath)
        self.PopulateImportedFilteredDecks(importedFilteredDecksList)
    
    def PopulateImportedFilteredDecks(self, importedFilteredDecksList: list[Deck.Deck]) -> None:
        """
        Populates imported filtered decks into the corresponding QTableWidget.
        """
        self.ui.tableWidgetStagedForImportFilteredDecks.setRowCount(len(importedFilteredDecksList))
        i = 0
        for importedFilteredDeck in importedFilteredDecksList:
            print(f"Adding: {importedFilteredDeck.Name}")
            checkboxSelected = QCheckBox(self.ui.tableWidgetStagedForImportFilteredDecks)
            checkboxUnsuspended = QCheckBox(self.ui.tableWidgetStagedForImportFilteredDecks)
            checkboxAppendNewDue = QCheckBox(self.ui.tableWidgetStagedForImportFilteredDecks)
            qconnect(checkboxUnsuspended.stateChanged, self.UpdateImportedFilteredDecks)
            qconnect(checkboxAppendNewDue.stateChanged, self.UpdateImportedFilteredDecks)
            numberOfCards = self.CalculateCardCount(importedFilteredDeck.SearchTermsAsString, False, False)
            searchTermsItem = QTableWidgetItem(importedFilteredDeck.SearchTerms[0])
            searchTermsItem.setFlags(searchTermsItem.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidgetStagedForImportFilteredDecks.setCellWidget(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.SELECT_CHECKBOX.value, checkboxSelected)
            self.ui.tableWidgetStagedForImportFilteredDecks.setItem(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.DECK_NAME.value, QTableWidgetItem(importedFilteredDeck.Name))
            self.ui.tableWidgetStagedForImportFilteredDecks.setItem(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.TOTAL_CARD_NUMBER.value, QTableWidgetItem(str(numberOfCards)))
            self.ui.tableWidgetStagedForImportFilteredDecks.setCellWidget(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.INCLUDE_SUSPENDED_CHECKBOX.value, checkboxUnsuspended)
            self.ui.tableWidgetStagedForImportFilteredDecks.setCellWidget(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.APPEND_NEW_DUE_CHECKBOX.value, checkboxAppendNewDue)
            self.ui.tableWidgetStagedForImportFilteredDecks.setItem(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.TAGS.value, searchTermsItem)
            i += 1
        qconnect(self.ui.tableWidgetStagedForImportFilteredDecks.cellChanged, self.UpdateFilteredDeckName)
        self.ui.tableWidgetStagedForImportFilteredDecks.update()
        self.ui.tableWidgetStagedForImportFilteredDecks.show()
    
    def CreateFilteredDecksFromImported(self) -> None:
        """
        Creates a filtered deck from the imported decks list.
        """
        importedFilteredDecksList = self.manager.StagedFilteredDecksList
        selectedDecks = self.GetSelectedStagedFilteredDecks()
        i = 0
        for deck in importedFilteredDecksList:
            print(f"Assessing Deck #{i}. Selected Decks: {selectedDecks}")
            if i in selectedDecks:
                if self.manager.IsUnique(deck, importedFilteredDecksList, importList=True):
                    if self.manager.IsUnique(deck, self.manager.FilteredDecksList):
                        searchTerm = deck.searchTerms[0]
                        if len(deck.SearchTerms) == 2:
                            searchTerm = f"{searchTerm} {deck.SearchTerms[1]}"
                        if self.ui.tableWidgetStagedForImportFilteredDecks.cellWidget(i,Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.INCLUDE_SUSPENDED_CHECKBOX.value).isChecked():
                            cardsToUnsuspend = self.mainWindow.col.find_cards(deck.SearchTerms[0])
                            self.mainWindow.col.sched.unsuspend_cards(cardsToUnsuspend)
                        if self.ui.tableWidgetStagedForImportFilteredDecks.cellWidget(i,Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.APPEND_NEW_DUE_CHECKBOX.value).isChecked():
                            searchTerm = f"{searchTerm} (is:new OR is:due)"
                        newDeckId = self.mainWindow.col.decks.new_filtered(deck.Name)
                        newDeck = self.mainWindow.col.decks.get(newDeckId)
                        newDeck["terms"] = [[searchTerm, 9999, 6]]
                        self.mainWindow.col.decks.save(newDeck)
                        self.mainWindow.col.sched.rebuildDyn(newDeckId)
                    else:
                        QMessageBox.warning(self, "Failed Uniqueness Check", f"The deck {deck.Name} already exists and will be skipped.")
                else:
                    QMessageBox.warning(self, "Failed Uniqueness Check", f"The deck {deck.Name} already exists and will be skipped.")
            i += 1
        self.CleanupAndExit()
    
    def UpdateImportedFilteredDecks(self):
        """
        Slot for updating data in the staged filtered decks table on toggle of option checkboxes.
        """
        for row in range(self.ui.tableWidgetStagedForImportFilteredDecks.rowCount()):
            query = self.manager.StagedFilteredDecksList[row].SearchTermsAsString
            includeSuspended = self.ui.tableWidgetStagedForImportFilteredDecks.cellWidget(row,Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.INCLUDE_SUSPENDED_CHECKBOX.value).isChecked()
            includeNewDue = self.ui.tableWidgetStagedForImportFilteredDecks.cellWidget(row,Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.APPEND_NEW_DUE_CHECKBOX.value).isChecked()
            updatedCardCount = self.CalculateCardCount(query, includeSuspended, includeNewDue)
            self.ui.tableWidgetStagedForImportFilteredDecks.item(row,Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.TOTAL_CARD_NUMBER.value).setText(str(updatedCardCount))

    def CalculateCardCount(self, query: str, includeSuspended: bool, includeNewDue: bool) -> int:
        """
        Calculates the card count based on a given search term and additional modifiers of suspended or only new/due cards.
        """
        if not includeSuspended:
            query = f"{query} (-is:suspended)"
        if includeNewDue:
            query = f"{query} (is:new OR is:due)"
        
        return len(self.mainWindow.col.find_cards(query))

    def UpdateFilteredDeckName(self, row: int, column: int) -> None:
        """
        Slot for updating the name of a filtered deck based on user input into the Deck Name column.
        """
        if column == Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.DECK_NAME:
            print(f"Filtered deck name set to: {self.ui.tableWidgetStagedForImportFilteredDecks.item(row,column).text()}")
            tempDeck = Deck.Deck()
            tempDeck.Name = self.ui.tableWidgetStagedForImportFilteredDecks.item(row,column).text()
            if self.manager.IsUnique(tempDeck, self.manager.FilteredDecksList, False, True) and self.manager.IsUnique(tempDeck, self.manager.StagedFilteredDecksList, True, True):
                self.manager.StagedFilteredDecksList[row].Name = self.ui.tableWidgetStagedForImportFilteredDecks.item(row,column).text()
            else:
                QMessageBox.warning(self, "Failed Uniqueness Check", f"The deck name {tempDeck.Name} is not unique.")
                self.ui.tableWidgetStagedForImportFilteredDecks.item(row,column).setText(self.manager.StagedFilteredDecksList[row].Name)
                print(f"Updating filtered deck name to: {self.manager.StagedFilteredDecksList[row].Name}")

    def GetSelectedFilteredDecks(self) -> list[int]:
        """
        Returns list of indices where the "Select" column of a QTableWidget is selected.
        """
        selectedDecks = []
        for row in range(self.ui.tableWidgetFilteredDecks.rowCount()):
            if self.ui.tableWidgetFilteredDecks.cellWidget(row, Constants.UI_CONSTANTS.FilteredDeckTableWidgetColumns.SELECT_CHECKBOX.value).isChecked():
                selectedDecks.append(row)
        return selectedDecks
    
    def GetSelectedStagedFilteredDecks(self) -> list[int]:
        """
        Returns list of indices where the "Select" column of a QTableWidget is selected.
        """
        selectedDecks = []
        for row in range(self.ui.tableWidgetStagedForImportFilteredDecks.rowCount()):
            if self.ui.tableWidgetStagedForImportFilteredDecks.cellWidget(row, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.SELECT_CHECKBOX.value).isChecked():
                selectedDecks.append(row)
        return selectedDecks
    

    def CleanupAndExit(self) -> None:
        """
        After filtered deck import, update MainWindow and FilteredDecks list for add-on.
        """
        self.mainWindow.reset()
        self.InitializeData()
        self.ExitDialog()

    def ExitDialog(self) -> None:
        """
        Closes the Filtered Deck Manager window.
        """
        self.ui.tableWidgetFilteredDecks.clearContents()
        self.ui.tableWidgetFilteredDecks.setRowCount(0)
        self.ui.tableWidgetStagedForImportFilteredDecks.clearContents()
        self.ui.tableWidgetStagedForImportFilteredDecks.setRowCount(0)
        self.ui.tableWidgetStagedForImportFilteredDecks.hide()
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
        selectedItems = self.GetSelectedFilteredDecks()
        selectedDeckIds = [int(self.ui.tableWidgetFilteredDecks.item(deckIndex, Constants.UI_CONSTANTS.FilteredDeckTableWidgetColumns.DECK_ID.value).text()) for deckIndex in selectedItems]
        selectedDecks = []
        for deckId in selectedDeckIds:
            decks = [deck for deck in self.manager.FilteredDecksList if (int(deck.DeckId) == int(deckId))]
            selectedDecks.append(decks[0])
        filepath = QFileDialog.getSaveFileName(filter="JSON (*.json)")[0]
        self.manager.WriteToFile(filepath, selectedDecks)
        

if __name__ == "__main__":
    pass



# from aqt.qt import QTabWidget, QVBoxLayout, QLabel, QWidget, QFont, QGroupBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QCoreApplication, QMetaObject, QAbstractItemView, QTextBrowser