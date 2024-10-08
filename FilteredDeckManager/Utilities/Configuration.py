from aqt import mw

class Configuration:
    """
    Manages configuration for FilteredDeckManager using the Anki add-on configuration API.
    """
    def __init__(self, addonPath: str = "") -> None:
        """
        Creates a new Configuration, reads in configuration file and loads data.

        Args:
            addonPath (str): Path to the Anki add-on, expected by the Anki API (typically just the add-on name).
        """
        self.addonPath = addonPath
        if addonPath:   # initializing global add-on config, so get add-on path from Anki add-on API
            if mw is not None:
                self.rawData = mw.addonManager.getConfig(self.addonPath)
            else:
                self.rawData = {}
        else:
            self.rawData = {}
            self.rawData["search_1"] = {}
        self.hasSecondSearchTerm = False
    
    def __eq__(self, other: object) -> bool:
        """
        Compares Configuration to another object instance by member variables.

        Args:
            other (object): The other object to compare to.

        Returns:
            bool: True if the member variables of self and other are equal, otherwise False.
        """
        if not isinstance(other, Configuration):
            return False
        if self.AllowEmpty != other.AllowEmpty:
            return False
        if self.Reschedule != other.Reschedule:
            return False
        # if self.IntervalAgain != other.IntervalAgain:
        #     return False
        # if self.IntervalHard != other.IntervalHard:
        #     return False
        # if self.IntervalGood != other.IntervalGood:
        #     return False
        if self.OrderBySearch1 != other.OrderBySearch1:
            return False
        if "search_2" in self.rawData and "search_2" in other.rawData:  # only run these tests if search_2 present in both
            if self.OrderBySearch2 != other.OrderBySearch2:
                return False
            if self.CardLimitSearch1 != other.CardLimitSearch1:
                return False
            if self.CardLimitSearch2 != other.CardLimitSearch2:
                return False
        else:
            if "search_2" in self.rawData != "search_2" in other.rawData:
                return False
        # if self.UseGlobalConfig != other.UseGlobalConfig:
        #     return False
        
        return True

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
        if mw is not None:
            mw.addonManager.writeConfig(self.addonPath, self.rawData)
    
    @property
    def IntervalAgain(self) -> int:
        """
        The value (in seconds) to use for the Again interval, if rescheduling is False.

        Raises:
            ValueError: If the value of this key in the configuration dictionary is None.

        Returns:
            int: The value for the Again interval, in seconds.
        """
        if self.rawData["intervals"]["again"] is not None:
            return self.rawData["intervals"]["again"]
        else:
            raise ValueError(f"Value for \"intervals\\again\" is unexpected value: {self.rawData['intervals']['again']}")
    
    @IntervalAgain.setter
    def IntervalAgain(self, againInterval: int) -> None:
        """
        Sets the value of the intervals/again key.

        Args:
            againInterval (int): The value (in seconds) to use for the Again interval.
        """
        self.rawData["intervals"]["again"] = againInterval
        self.WriteConfig()
    
    @property
    def IntervalHard(self) -> int:
        """
        The value (in seconds) to use for the Hard interval, if rescheduling is False.

        Raises:
            ValueError: If the value of this key in the configuration dictionary is None.

        Returns:
            int: The value for the Hard interval, in seconds.
        """
        if self.rawData["intervals"]["hard"] is not None:
            return self.rawData["intervals"]["hard"]
        else:
            raise ValueError(f"Value for \"intervals\\hard\" is unexpected value: {self.rawData['intervals']['hard']}")
    
    @IntervalHard.setter
    def IntervalHard(self, hardInterval: int) -> None:
        """
        Sets the value of the intervals/hard key.

        Args:
            hardInterval (int): The value (in seconds) to use for the Hard interval.
        """
        self.rawData["intervals"]["hard"] = hardInterval
        self.WriteConfig()
    
    @property
    def IntervalGood(self) -> int:
        """
        The value (in seconds) to use for the Good interval, if rescheduling is False.

        Raises:
            ValueError: If the value of this key in the configuration dictionary is None.

        Returns:
            int: The value for the Good interval, in seconds.
        """
        if self.rawData["intervals"]["good"] is not None:
            return self.rawData["intervals"]["good"]
        else:
            raise ValueError(f"Value for \"intervals\\good\" is unexpected value: {self.rawData['intervals']['good']}")
    
    @IntervalGood.setter
    def IntervalGood(self, goodInterval: int) -> None:
        """
        Sets the value of the intervals/good key.

        Args:
            goodInterval (int): The value (in seconds) to use for the Good interval.
        """
        self.rawData["intervals"]["good"] = goodInterval
        self.WriteConfig()
    
    @property
    def OrderBySearch1(self) -> int:
        """
        The enum value to use for card ordering in the filtered deck for the first search term.
        Enum name/values defined at https://github.com/ankitects/anki/blob/main/proto/anki/decks.proto#L91.

        Raises:
            ValueError: If the value of this key in the configuration dictionary is None.

        Returns:
            int: The integer representation of the enum value used for card ordering in the filtered deck.
        """
        if self.rawData["search_1"]["order"] is not None:
            return self.rawData["search_1"]["order"]
        else:
            raise ValueError(f"Value for \"search_1\\order\" is unexpected value: {self.rawData['search_1']['order']}")
    
    @OrderBySearch1.setter
    def OrderBySearch1(self, orderBy: int):
        """
        Sets the value of the search_1/order key.

        Args:
            orderBy (int): The integer representation of the Order enum value.
        """
        self.rawData["search_1"]["order"] = orderBy
        self.WriteConfig()
    
    @property
    def OrderBySearch2(self) -> int:
        """
        The enum value to use for card ordering in the filtered deck for the second search term.
        Enum name/values defined at https://github.com/ankitects/anki/blob/main/proto/anki/decks.proto#L91.

        Raises:
            ValueError: If the value of this key in the configuration dictionary is None.

        Returns:
            int: The integer representation of the enum value used for card ordering in the filtered deck.
        """
        if self.rawData["search_2"]["order"] is not None:
            return self.rawData["search_2"]["order"]
        else:
            raise ValueError(f"Value for \"search_2\\order\" is unexpected value: {self.rawData['search_2']['order']}")
    
    @OrderBySearch2.setter
    def OrderBySearch2(self, orderBy: int):
        """
        Sets the value of the search_2/order key.

        Args:
            orderBy (int): The integer representation of the Order enum value.
        """
        if "search_2" not in self.rawData:
            self.rawData["search_2"] = {}

        self.rawData["search_2"]["order"] = orderBy
        self.hasSecondSearchTerm = True
        self.WriteConfig()
    
    @property
    def CardLimitSearch1(self) -> int:
        """
        The maximum number of cards to include in a filtered deck on creation.
        If the number of matching cards for a search term exceeds this number, the number of cards in the resulting filtered deck will be capped by this number.
        If the number of matching cards is less than this number, the number of cards in the resulting filtered deck will equal the number of matched cards.

        Raises:
            ValueError: If the value of this key on the configuration dictionary is None.

        Returns:
            int: The maximum number of cards to include in the filtered deck.
        """
        if self.rawData["search_1"]["card_limit"] is not None:
            return self.rawData["search_1"]["card_limit"]
        else:
            raise ValueError(f"Value for \"search_1\\card_limit\" is unexpected value: {self.rawData['search_1']['card_limit']}")
    
    @CardLimitSearch1.setter
    def CardLimitSearch1(self, cardLimit: int) -> None:
        """
        Sets the value of the card_limit key.

        Args:
            cardLimit (int): The value for the maximum number of cards to include in the filtered deck on creation.
        """
        self.rawData["search_1"]["card_limit"] = cardLimit
        self.WriteConfig()
    
    @property
    def CardLimitSearch2(self) -> int:
        """
        The maximum number of cards to include in a filtered deck on creation.
        If the number of matching cards for a search term exceeds this number, the number of cards in the resulting filtered deck will be capped by this number.
        If the number of matching cards is less than this number, the number of cards in the resulting filtered deck will equal the number of matched cards.

        Raises:
            ValueError: If the value of this key on the configuration dictionary is None.

        Returns:
            int: The maximum number of cards to include in the filtered deck.
        """
        if self.rawData["search_2"]["card_limit"] is not None:
            return self.rawData["search_2"]["card_limit"]
        else:
            raise ValueError(f"Value for \"search_2\\card_limit\" is unexpected value: {self.rawData['search_2']['card_limit']}")
    
    @CardLimitSearch2.setter
    def CardLimitSearch2(self, cardLimit: int) -> None:
        """
        Sets the value of the card_limit key.

        Args:
            cardLimit (int): The value for the maximum number of cards to include in the filtered deck on creation.
        """
        self.rawData["search_2"]["card_limit"] = cardLimit
        self.WriteConfig()
    
    @property
    def UseGlobalConfig(self) -> bool:
        """
        Sets the value of the use_global_config key.
        This value will have imported filtered decks use global add-on settings instead of individual filtered deck settings.
        This key is not included in serialization (AsDict, FromDict), as those are used for per-deck configurations.

        Raises:
            ValueError: If the value in the data dictionary is invalid.

        Returns:
            bool: True if a newly-created filtered deck should use Anki add-on configuration instead of imported deck configuration, otherwise false.
        """
        if self.rawData["use_global_config"] is not None:
            return self.rawData["use_global_config"]
        else:
            raise ValueError(f"Value for \"use_global_config\" is unexpected value: {self.rawData['use_global_config']}.")
    
    @UseGlobalConfig.setter
    def UseGlobalConfig(self, useGlobalConfig: bool):
        """
        Sets the value of the use_global_config key.

        Args:
            useGlobalConfig (bool): The value to use for the use_global_config setting.
        """
        self.rawData["use_global_config"] = useGlobalConfig
        self.WriteConfig()
    
    def AsDict(self) -> dict:
        """
        Serialize current Configuration class to dict.

        Returns:
            dict: This Configuration class as a dict.
        """
        configAsDict = {}
        configAsDict["search_1"] = {}

        if self.AllowEmpty is not None:
            configAsDict["allow_empty"] = self.AllowEmpty
        if self.Reschedule is not None:
            configAsDict["reschedule"] = self.Reschedule
        if not self.Reschedule:
            if self.IntervalAgain is not None:
                configAsDict["intervals"]["again"] = self.IntervalAgain
            if self.IntervalHard is not None:
                configAsDict["intervals"]["hard"] = self.IntervalHard
            if self.IntervalGood is not None:
                configAsDict["intervals"]["good"] = self.IntervalGood
        if self.OrderBySearch1 is not None:
            configAsDict["search_1"]["order"] = self.OrderBySearch1
        if self.CardLimitSearch1 is not None:
            configAsDict["search_1"]["card_limit"] = self.CardLimitSearch1
        if self.hasSecondSearchTerm:
            if self.OrderBySearch2 is not None:
                configAsDict["search_2"]["order"] = self.OrderBySearch2
            if self.CardLimitSearch2 is not None:
                configAsDict["card_limit"]["card_limit"] = self.CardLimitSearch2
        
        return configAsDict

    def FromDict(self, configDict: dict) -> None:
        """
        Populates member variables of this Configuration class from a dictionary representation.

        Args:
            configDict (dict): Dictionary representation of a Configuration class.

        Raises:
            KeyError: _description_
        """
        if "allow_empty" in configDict:
            self.AllowEmpty = configDict["allow_empty"]
        else:
            raise KeyError("Missing key allow_empty.")
        if "reschedule" in configDict:
            self.Reschedule = configDict["reschedule"]
            if not self.Reschedule:
                if "again" in configDict["intervals"]:
                    self.IntervalAgain = configDict["intervals"]["again"]
                if "hard" in configDict["intervals"]:
                    self.IntervalHard = configDict["intervals"]["hard"]
                if "good" in configDict["intervals"]:
                    self.IntervalGood = configDict["intervals"]["good"]
        if "order" in configDict["search_1"]:
            self.OrderBySearch1 = configDict["search_1"]["order"]
        if "card_limit" in configDict["search_1"]:
            self.CardLimitSearch1 = configDict["search_1"]["card_limit"]
        if "search_2" in configDict:
            if "order" in configDict["search_1"]:
                self.OrderBySearch2 = configDict["search_2"]["order"]
            if "card_limit" in configDict["search_2"]:
                self.CardLimitSearch2 = configDict["search_2"]["card_limit"]

if __name__ == "__main__":
    pass