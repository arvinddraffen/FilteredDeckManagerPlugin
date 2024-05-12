from aqt import mw

class Configuration:
    """
    Manages configuration for FilteredDeckManager using the Anki add-on configuration API.
    """
    def __init__(self, addonPath: str) -> None:
        """
        Creates a new Configuration, reads in configuration file and loads data.

        Args:
            addonPath (str): Path to the Anki add-on, expected by the Anki API (typically just the add-on name).
        """
        self.addonPath = addonPath
        self.rawData = mw.addonManager.getConfig(self.addonPath)

    @property
    def AllowEmpty(self) -> bool:
        """
        Whether the add-on should allow creation of a filtered deck if the search returns 0 cards.

        Raises:
            ValueError: If the value of this key in the configuration dictionary is None.

        Returns:
            bool: True if the add-on should allow creation of filtered decks with no matching cards, otherwise False.
        """
        if self.rawData["allow_empty"] is not None:
            return self.rawData["allow_empty"]
        else:
            raise ValueError(f"Value for \"allow_empty\" is unexpected value: {self.rawData['allow_empty']}")
    
    @AllowEmpty.setter
    def AllowEmpty(self, allow_empty: bool) -> None:
        """
        Sets the value of the allow_empty key.

        Args:
            allow_empty (bool): Set to True if the add-on should allow creation of filtered decks with no matching cards, otherwise False.
        """
        self.rawData["allow_empty"] = allow_empty
        self.WriteConfig()
    
    @property
    def Reschedule(self) -> bool:
        """
        Whether the add-on should enable the Reschedule option for filtered decks.

        Raises:
            ValueError: If the value of this key in the configuration dictionary is None.

        Returns:
            bool: True if the add-on should enable the Reschedule option on filtered deck creation, otherwise False.
        """
        if self.rawData["reschedule"] is not None:
            return self.rawData["reschedule"]
        else:
            raise ValueError(f"Value for \"reschedule\" is unexpected value: {self.rawData['reschedule']}")
    
    @Reschedule.setter
    def Reschedule(self, reschedule: bool) -> None:
        """
        Sets the value of the reschedule key.

        Args:
            reschedule (bool): Set to True if the add-on should enable the Reschedule option on filtered deck creation, otherwise False.
        """
        self.rawData["reschedule"] = reschedule
        self.WriteConfig()
    
    def WriteConfig(self) -> None:
        """
        Writes the configuration dictionary to the corresponding settings file.
        """
        mw.addonManager.writeConfig(self.addonPath, self.rawData)


if __name__ == "__main__":
    pass