import logging
from .Constants import BACKEND_CONSTANTS

from anki import utils

class Logger:
    """
    Handles logging for FilteredDeckManager. Support for add-on logging was added in Anki desktop version 240400.
    """
    def __init__(self, mw) -> None:
        self.logger = getattr(mw.addonManager, "getLogger", logging.getLogger)(__name__.split('.', 1)[0])
        self.currentAnkiVersion = utils.int_version()
    
    @property
    def Logger(self) -> logging.Logger:
        """
        Returns the logger object.

        Returns:
            logging.Logger: The logger object.
        """
        return self.logger

    @property
    def CurrentAnkiVersion(self) -> int:
        """
        Returns the current version of Anki desktop as an integer.

        Returns:
            int: The current Anki desktop version.
        """
        return self.currentAnkiVersion

    @property
    def LoggingSupported(self) -> bool:
        """
        Returns whether the current Anki desktop version supports add-on logging. This was added in version 240400.

        Returns:
            bool: True if the current Anki desktop is equal to or later than the version supporting add-on logging, otherwise false.
        """
        return self.CurrentAnkiVersion >= BACKEND_CONSTANTS.ANKI_VERSION_LOGGING_SUPPORT

if __name__ == "__main__":
    pass