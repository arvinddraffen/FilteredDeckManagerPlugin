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
        qconnect(self.ui.pushButtonExportAll.clicked, self.WriteToFile)

    def WriteToFile(self):
        filepath = QFileDialog.getSaveFileName(filter="JSON (*.json)")[0]
        self.manager.WriteToFile(filepath, self.manager.FilteredDecksList)

if __name__ == "__main__":
    pass



# from aqt.qt import QTabWidget, QVBoxLayout, QLabel, QWidget, QFont, QGroupBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QCoreApplication, QMetaObject, QAbstractItemView