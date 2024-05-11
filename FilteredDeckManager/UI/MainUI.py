from aqt import QCheckBox, QTableWidget
from .ui_form import Ui_Dialog
from ..FilteredDeckManager import FilteredDeckManager
from ..Models import Deck
from ..Utilities import Constants, Logger

import logging

from aqt.qt import QDialog
from aqt.qt import QTableWidgetItem
from aqt.qt import QAbstractItemView
from aqt.qt import QFileDialog
from aqt.qt import QMessageBox
from aqt.qt import QAbstractItemView
from aqt.qt import Qt
from aqt.qt import QUrl

from anki.scheduler import FilteredDeckForUpdate
from aqt.operations.scheduling import add_or_update_filtered_deck
from anki.decks import FilteredDeckConfig

from aqt.utils import qconnect

class MainUI(QDialog):
    """
    Dialog UI data preparation and additional UI setup.
    UI initially defined using Qt designer, imported as ui_form.py. Qt designer file located in Designer/form.ui.
    """
    def __init__(self, mw, parent=None) -> None:
        """
        Initializes MainUI class.
        Initializes data of QTableWidget for existing filtered decks, populates the About tab, and defines Qt signal/slots.

        Args:
            mw: Anki MainWindow
            parent (optional): Parent for MainUI. Defaults to None.
        """
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tabWidget.setCurrentIndex(0)    # ensure the first tab is the active tab on load
        self.ui.tableWidgetFilteredDecks.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.tableWidgetStagedForImportFilteredDecks.hide()
        self.mainWindow = mw
        self.manager = FilteredDeckManager(self.mainWindow)
        self.logger = Logger.Logger(mw)
        self.SetupSignalsSlots()
        self.SetupAboutTab()
    
    def InitializeData(self) -> None:
        """
        Triggers query of filtered decks from the Anki API using the `FilteredDeckManager`.
        """
        self.manager._GetAllDecks()
        self.PopulateDecks(self.manager.FilteredDecksList)

    def PopulateDecks(self, filteredDecksList: list[Deck.Deck]) ->None:
        """
        Populates the central table with a list of filtered decks (Deck Name and Deck Id).

        Args:
            filteredDecksList (list[Deck.Deck]): The list of current filtered decks.
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
        Sets up Qt signals/slots for `MainUI`, primarily for button presses.
        """
        qconnect(self.ui.pushButtonExportAll.clicked, self.WriteAllToFile)
        qconnect(self.ui.buttonExportSelected.clicked, self.WriteSelectedToFile)
        qconnect(self.ui.buttonImport.clicked, self.ImportFromFile)
        qconnect(self.ui.buttonOkay.clicked, self.CreateFilteredDecksFromImported)
        qconnect(self.ui.buttonExit.clicked, self.ExitDialog)
        qconnect(self.rejected, self.ExitDialog)
    
    def SetupAboutTab(self) -> None:
        """
        Populates information in the About tab.
        """
        import datetime
        from pathlib import Path
        self.ui.labelWrittenBy.setText(f"{self.ui.labelWrittenBy.text()} Arvind Draffen, {datetime.date.today().year}.\nAdd-on version: {Constants.BACKEND_CONSTANTS.ADD_ON_VERSION}")
        readmePath = (Path(__file__).parent.parent).joinpath('Utilities').joinpath('Data').joinpath('AboutText.md')
        self.ui.textBrowser.setSource(QUrl.fromLocalFile(f"{readmePath}"))

    def ImportFromFile(self) -> None:
        """
        Import filtered decks from file and populate in UI.
        """
        filepath = QFileDialog.getOpenFileName(self, caption="Import", filter="JSON (*.json)")[0]
        importedFilteredDecksList = self.manager.ReadFromFile(filepath)
        self.PopulateImportedFilteredDecks(importedFilteredDecksList)
    
    def PopulateImportedFilteredDecks(self, importedFilteredDecksList: list[Deck.Deck]) -> None:
        """
        Populates imported filtered decks into the corresponding QTableWidget.

        Args:
            importedFilteredDecksList (list[Deck.Deck]): The list of filtered decks read in from the imported file.
        """
        self.ui.tableWidgetStagedForImportFilteredDecks.setRowCount(len(importedFilteredDecksList))
        i = 0
        for importedFilteredDeck in importedFilteredDecksList:
            if self.logger.LoggingSupported: self.logger.Logger.debug(f"Adding: {importedFilteredDeck.Name}")
            checkboxSelected = QCheckBox(self.ui.tableWidgetStagedForImportFilteredDecks)
            checkboxUnsuspended = QCheckBox(self.ui.tableWidgetStagedForImportFilteredDecks)
            checkboxAppendNewDue = QCheckBox(self.ui.tableWidgetStagedForImportFilteredDecks)
            qconnect(checkboxUnsuspended.stateChanged, self.UpdateImportedFilteredDecks)
            qconnect(checkboxAppendNewDue.stateChanged, self.UpdateImportedFilteredDecks)
            numberOfCards = self.CalculateCardCount(importedFilteredDeck.SearchTermsAsString, False, False)
            searchTerms1Item = QTableWidgetItem(importedFilteredDeck.SearchTerms[0])
            searchTerms1Item.setFlags(searchTerms1Item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidgetStagedForImportFilteredDecks.setCellWidget(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.SELECT_CHECKBOX.value, checkboxSelected)
            self.ui.tableWidgetStagedForImportFilteredDecks.setItem(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.DECK_NAME.value, QTableWidgetItem(importedFilteredDeck.Name))
            self.ui.tableWidgetStagedForImportFilteredDecks.setItem(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.TOTAL_CARD_NUMBER.value, QTableWidgetItem(str(numberOfCards)))
            self.ui.tableWidgetStagedForImportFilteredDecks.setCellWidget(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.INCLUDE_SUSPENDED_CHECKBOX.value, checkboxUnsuspended)
            self.ui.tableWidgetStagedForImportFilteredDecks.setCellWidget(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.APPEND_NEW_DUE_CHECKBOX.value, checkboxAppendNewDue)
            self.ui.tableWidgetStagedForImportFilteredDecks.setItem(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.SEARCH_1.value, searchTerms1Item)
            if len(importedFilteredDeck.SearchTerms) > 1:
                searchTerms2Item = QTableWidgetItem(importedFilteredDeck.SearchTerms[1])
                searchTerms2Item.setFlags(searchTerms2Item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.ui.tableWidgetStagedForImportFilteredDecks.setItem(i, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.SEARCH_2.value, searchTerms2Item)
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
            if self.logger.LoggingSupported: self.logger.Logger.debug(f"Assessing Deck #{i}. Selected Decks: {selectedDecks}")
            if i in selectedDecks:
                if self.manager.IsUnique(deck, importedFilteredDecksList, importList=True):
                    if self.manager.IsUnique(deck, self.manager.FilteredDecksList):
                        if self.ui.tableWidgetStagedForImportFilteredDecks.cellWidget(i,Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.INCLUDE_SUSPENDED_CHECKBOX.value).isChecked():
                            cardsToUnsuspend = self.mainWindow.col.find_cards(deck.SearchTerms[0])
                            self.mainWindow.col.sched.unsuspend_cards(cardsToUnsuspend)

                        newFilteredDeck = FilteredDeckForUpdate()
                        newFilteredDeck.name = deck.Name
                        newFilteredDeck.config.reschedule = True    # add option in later versions, but explicitly set for now
                        newFilteredDeck.allow_empty = True
                        
                        terms = [FilteredDeckConfig.SearchTerm(search=deck.searchTerms[0],limit=9999)]
                        if self.ui.tableWidgetStagedForImportFilteredDecks.cellWidget(i,Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.APPEND_NEW_DUE_CHECKBOX.value).isChecked():
                            terms = [FilteredDeckConfig.SearchTerm(search=f"{deck.searchTerms[0]} (is:new OR is:due)",limit=9999)]
                        else:
                            terms = [FilteredDeckConfig.SearchTerm(search=deck.searchTerms[0],limit=9999)]

                        if len(deck.SearchTerms) == 2:
                            if self.ui.tableWidgetStagedForImportFilteredDecks.cellWidget(i,Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.APPEND_NEW_DUE_CHECKBOX.value).isChecked():
                                terms = [FilteredDeckConfig.SearchTerm(search=f"{deck.searchTerms[1]} (is:new OR is:due)",limit=9999)]
                            else:
                                terms = [FilteredDeckConfig.SearchTerm(search=deck.searchTerms[1],limit=9999)]

                        newFilteredDeck.config.search_terms.extend(terms)
                        print(newFilteredDeck.config.search_terms)
                        add_or_update_filtered_deck(parent=self.mainWindow, deck=newFilteredDeck).run_in_background()
                    else:
                        QMessageBox.warning(self, "Failed Uniqueness Check", f"The deck {deck.Name} already exists and will be skipped.")
                else:
                    QMessageBox.warning(self, "Failed Uniqueness Check", f"The deck {deck.Name} already exists and will be skipped.")
            i += 1
        self.CleanupAndExit()
    
    def UpdateImportedFilteredDecks(self) -> None:
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

        Args:
            query (str): The search string to use to query the Anki database for selecting cards.
            includeSuspended (bool): Whether or not to include suspended cards in the card count.
            includeNewDue (bool): Whether to restrict the card count to cards that are new or due to studying at the time of deck creation.

        Returns:
            int: The number of cards matching the search criteria.
        """
        if not includeSuspended:
            query = f"{query} (-is:suspended)"
        if includeNewDue:
            query = f"{query} (is:new OR is:due)"
        
        return len(self.mainWindow.col.find_cards(query))

    def UpdateFilteredDeckName(self, row: int, column: int) -> None:
        """
        Slot for updating the name of a filtered deck based on user input into the Deck Name column.

        Args:
            row (int): The row in the QTableWidget corresponding to the deck to update.
            column (int): The column in the QTableWidget corresponding to the deck to update.
        """
        if column == Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.DECK_NAME:
            if self.logger.LoggingSupported: self.logger.Logger.debug(f"Filtered deck name set to: {self.ui.tableWidgetStagedForImportFilteredDecks.item(row,column).text()}")
            tempDeck = Deck.Deck()
            tempDeck.Name = self.ui.tableWidgetStagedForImportFilteredDecks.item(row,column).text()
            if self.manager.IsUnique(tempDeck, self.manager.FilteredDecksList, False, True) and self.manager.IsUnique(tempDeck, self.manager.StagedFilteredDecksList, True, True):
                self.manager.StagedFilteredDecksList[row].Name = self.ui.tableWidgetStagedForImportFilteredDecks.item(row,column).text()
            else:
                QMessageBox.warning(self, "Failed Uniqueness Check", f"The deck name {tempDeck.Name} is not unique.")
                self.ui.tableWidgetStagedForImportFilteredDecks.item(row,column).setText(self.manager.StagedFilteredDecksList[row].Name)
                if self.logger.LoggingSupported: self.logger.Logger.debug(f"Updating filtered deck name to: {self.manager.StagedFilteredDecksList[row].Name}")

    def GetSelectedFilteredDecks(self) -> list[int]:
        """
        Returns list of indices where the "Select" column of a filtered decks QTableWidget is selected.

        Returns:
            list[int]: The list of indices from the filtered decks QTableWidget that are selected.
        """
        selectedDecks = []
        for row in range(self.ui.tableWidgetFilteredDecks.rowCount()):
            if self.ui.tableWidgetFilteredDecks.cellWidget(row, Constants.UI_CONSTANTS.FilteredDeckTableWidgetColumns.SELECT_CHECKBOX.value).isChecked():
                selectedDecks.append(row)
        return selectedDecks
    
    def GetSelectedStagedFilteredDecks(self) -> list[int]:
        """
        Returns list of indices where the "Select" column of the staged filtered decks QTableWidget is selected.

        Returns:
            list[int]: The list of indices from the staged filtered decks QTableWidget that are selected.
        """
        selectedDecks = []
        for row in range(self.ui.tableWidgetStagedForImportFilteredDecks.rowCount()):
            if self.ui.tableWidgetStagedForImportFilteredDecks.cellWidget(row, Constants.UI_CONSTANTS.ImportedFilteredDeckTableWidgetColumns.SELECT_CHECKBOX.value).isChecked():
                selectedDecks.append(row)
        return selectedDecks
    

    def CleanupAndExit(self) -> None:
        """
        After filtered deck import, update MainWindow and FilteredDecks list for add-on, then cleanup prior to exiting.
        """
        self.mainWindow.reset()
        self.InitializeData()
        self.ExitDialog()

    def ExitDialog(self) -> None:
        """
        Closes the Filtered Deck Manager window. Resets data and restores UI to initial state.
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