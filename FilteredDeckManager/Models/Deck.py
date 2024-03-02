class Deck:
    """Represents a Deck object as exposed by the Anki API."""
    def __init__(self) -> None:
        self.deckId: int = None
        self.name: str = None
        self.level: int = None
        self.reviewCount: int = None
        self.learnCount: int = None
        self.newCount: int = None
        self.intradayLearning: int = None
        self.interdayLearningUncapped: int = None
        self.newUncapped: int = None
        self.reviewUncapped: int = None
        self.totalInDeck: int = None
        self.totalIncludingChildren: int = None
        self.isFiltered: bool = None

    @property
    def DeckId(self) -> int:
        """The unique ID of this `Deck`."""
        return self.deckId
    
    @DeckId.setter
    def DeckId(self, deckId: int) -> None:
        """Sets the unique ID of this `Deck`."""
        self.deckId = deckId
    
    @property
    def Name(self) -> str:
        """The name of this `Deck`."""
        return self.name

    @Name.setter
    def Name(self, name: str) -> None:
        """Sets the name of this `Deck`."""
        self.name = name
    
    @property
    def Level(self) -> int:
        """The indentation level of this `Deck`.""" 
        return self.level

    @Level.setter
    def Level(self, level: int) -> None:
        """Sets the level of this `Deck."""
        self.level = level
    
    @property
    def ReviewCount(self) -> int:
        """The number of cards up for review in this `Deck`."""
        return self.reviewCount
    
    @ReviewCount.setter
    def ReviewCount(self, reviewCount: int) -> None:
        """Sets the review count of this `Deck`."""
        self.reviewCount = reviewCount
    
    @property
    def LearnCount(self) -> int:
        """The number of cards in the learn state in this `Deck`."""
        return self.learnCount
    
    @LearnCount.setter
    def LearnCount(self, learnCount: int) -> None:
        """Sets the learn count of this `Deck`."""
        self.learnCount = learnCount
    
    @property
    def NewCount(self) -> int:
        """The number of new (unreviewed) cards in this `Deck`."""
        return self.newCount
    
    @NewCount.setter
    def NewCount(self, newCount: int) -> None:
        """Sets the new count of this `Deck`."""
        self.newCount = newCount
    
    @property
    def IntradayLearning(self) -> int:
        """The number of intraday learning cards for this `Deck`."""
        return self.intradayLearning

    @IntradayLearning.setter
    def IntradayLearning(self, intradayLearning: int) -> None:
        """Sets the number of intraday learning cards for this `Deck`."""
        self.intradayLearning = intradayLearning
    
    @property
    def InterdayLearningUncapped(self) -> int:
        """The number of interday learning uncapped cards for this `Deck`."""
        return self.interdayLearningUncapped

    @InterdayLearningUncapped.setter
    def InterdayLearningUncapped(self, interdayLearningUncapped: int) -> None:
        """Sets the number of interday learning uncapped cards for this `Deck`."""
        self.interdayLearningUncapped = interdayLearningUncapped
    
    @property
    def NewUncapped(self) -> int:
        """The uncapped number of new (unreviewed) cards for this `Deck`."""
        return self.newUncapped
    
    @NewUncapped.setter
    def NewUncapped(self, newUncapped: int) -> None:
        """Sets the uncapped number of new (unreviewed) cards for this `Deck`."""
        self.newUncapped = newUncapped
    
    @property
    def ReviewUncapped(self) -> int:
        """Gets the uncapped number of cards up for review for this `Deck`."""
        return self.reviewUncapped

    @ReviewUncapped.setter
    def ReviewUncapped(self, reviewUncapped: int) -> None:
        """Sets the uncapped number of cards up for review for this `Deck`."""
        self.reviewUncapped = reviewUncapped
    
    @property
    def TotalInDeck(self) -> int:
        """The total number of cards in this `Deck`."""
        return self.totalInDeck
    
    @TotalInDeck.setter
    def TotalInDeck(self, totalInDeck: int) -> None:
        """Sets the total number of cards in this `Deck`."""
        self.totalInDeck = totalInDeck
    
    @property
    def TotalIncludingChildren(self) -> int:
        """The total number of cards, including children cards, in this `Deck`."""
        return self.totalIncludingChildren
    
    @TotalIncludingChildren.setter
    def TotalIncludingChildren(self, totalIncludingChildren: int) -> None:
        """Sets the total number of cards, including children cards, in this `Deck`."""
        self.totalIncludingChildren = totalIncludingChildren
    
    @property
    def IsFiltered(self) -> bool:
        """Represents whether this `Deck` is a filtered deck."""
        return self.isFiltered
    
    @IsFiltered.setter
    def IsFiltered(self, isFiltered: bool) -> None:
        self.isFiltered = isFiltered
    
    def AsDict(self) -> dict:
        """
        Serializes this `Deck` as a dictionary.
        """
        deckAsDict = {}

        if self.DeckId is not None:
            deckAsDict["deckId"] = self.DeckId
        if self.Name is not None:
            deckAsDict["name"] = self.Name
        if self.Level is not None:
            deckAsDict["name"] = self.Name
        if self.ReviewCount is not None:
            deckAsDict["reviewCount"] = self.ReviewCount
        if self.LearnCount is not None:
            deckAsDict["reviewCount"] = self.ReviewCount
        if self.NewCount is not None:
            deckAsDict["newCount"] = self.NewCount
        if self.IntradayLearning is not None:
            deckAsDict["intradayLearning"] = self.IntradayLearning
        if self.InterdayLearningUncapped is not None:
            deckAsDict["interdayLearningUncapped"] = self.InterdayLearningUncapped
        if self.NewUncapped is not None:
            deckAsDict["newUncapped"] = self.NewUncapped
        if self.totalInDeck is not None:
            deckAsDict["totalInDeck"] = self.TotalInDeck
        if self.TotalIncludingChildren is not None:
            deckAsDict["totalIncludingChildren"] = self.TotalIncludingChildren

        # is only included if the deck is filtered (aka not present but as "False")
        if self.IsFiltered:
            deckAsDict["filtered"] = self.IsFiltered
        
        return deckAsDict
    
    def FromDict(self, deck: dict) -> None:
        """
        Reads in a `Deck` serialized as a dictionary and populates corresponding properties.
        Each deck does not necessarily contain every property when serialized by Anki, so validate existence before assignment.
        """
        if "deckId" in deck:
            self.DeckId = deck["deckId"]
        if "name" in deck:
            self.Name = deck["name"]
        if "level" in deck:
            self.Level = deck["level"]
        if "reviewCount" in deck:
            self.ReviewCount = deck["reviewCount"]
        if "learnCount" in deck:
            self.LearnCount = deck["learnCount"]
        if "newCount" in deck:
            self.NewCount = deck["newCount"]
        if "intradayLearning" in deck:
            self.IntradayLearning = deck["intradayLearning"]
        if "interdayLearningUncapped" in deck:
            self.InterdayLearningUncapped = deck["interdayLearningUncapped"]
        if "newUncapped" in deck:
            self.NewUncapped = deck["newUncapped"]
        if "reviewUncapped" in deck:
            self.ReviewUncapped = deck["reviewUncapped"]
        if "totalInDeck" in deck:
            self.TotalInDeck = deck["totalInDeck"]
        if "totalIncludingChildren" in deck:
            self.TotalIncludingChildren = deck["totalIncludingChildren"]
        if "filtered" in deck:
            self.IsFiltered = deck["filtered"]
        else:
            self.IsFiltered = False


if __name__ == "__main__":
    pass