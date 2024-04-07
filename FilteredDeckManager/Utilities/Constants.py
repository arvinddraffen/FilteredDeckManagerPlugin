"""
Provides constants used in the UI.
"""

from enum import Enum

class UI_CONSTANTS:
    """
    Constants used in the add-on UI.
    """
    class FilteredDeckTableWidgetColumns(Enum):
        """Defines constants to use instead of column index numbers for tableWidgetFilteredDecks."""
        SELECT_CHECKBOX = 0
        DECK_NAME = 1
        DECK_ID = 2

    class ImportedFilteredDeckTableWidgetColumns(Enum):
        """Defines constants to use instead of column index numbers for tableWidgetStagedForImportFilteredDecks."""
        SELECT_CHECKBOX = 0
        DECK_NAME = 1
        TOTAL_CARD_NUMBER = 2
        INCLUDE_SUSPENDED_CHECKBOX = 3
        APPEND_NEW_DUE_CHECKBOX = 4
        TAGS = 5

class BACKEND_CONSTANTS:
    """
    Constants used in back-end logic.
    """

    ANKI_VERSION_LOGGING_SUPPORT = 240400

if __name__ == "__main__":
    pass