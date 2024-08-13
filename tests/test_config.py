import sys
from aqt import QApplication
import pytest
app = QApplication(sys.argv)
from FilteredDeckManager.Utilities import Configuration

def test_init_no_addon_path():
    config = Configuration.Configuration()
    assert "search_1" in config.rawData
    assert config.rawData["search_1"] == {}

def test_allow_empty_set():
    config = Configuration.Configuration()
    allowEmpty = True
    config.AllowEmpty = allowEmpty
    assert config.AllowEmpty == allowEmpty

def test_reschedule_set():
    config = Configuration.Configuration()
    reschedule = True
    config.Reschedule = reschedule
    assert config.Reschedule == config.Reschedule