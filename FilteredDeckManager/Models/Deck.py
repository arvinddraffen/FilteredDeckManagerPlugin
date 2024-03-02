class Deck:
    """Represents a Deck object as exposed by the Anki API."""
    def __init__(self) -> None:
        self.deckId: int
        self.name: str
        self.level: int
        self.reviewCount: int
        self.learnCount: int
        self.newCount: int
        self.intradayLearning: int
        self.interdayLearningUncapped: int
        self.newUncapped: int
        self.reviewUncapped: int
        self.totalInDeck: int
        self.totalIncludingChildren: int
        self.isFiltered: bool

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