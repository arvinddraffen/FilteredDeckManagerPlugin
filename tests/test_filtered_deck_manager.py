import sys
from aqt import QApplication
from pathlib import Path
import pytest
app = QApplication(sys.argv)
from FilteredDeckManager import FilteredDeckManager

def test_read_from_file(populated_deck):
    manager = FilteredDeckManager.FilteredDeckManager()
    filepath = Path(__file__).parent.joinpath("data").joinpath("test_deck.json")
    deck = manager.ReadFromFile(str(filepath))[0]
    assert deck == populated_deck