from re import search
from .Models import Deck

from .Utilities import AnkiApiHandler, Configuration, Constants, Logger
import logging

from anki.scheduler import FilteredDeckForUpdate

class FilteredDeckManager:
    """
    Data management and file handling for import/export of decks.

    Returns:
        _type_: _description_
    """
    from anki.collection import Collection
    
    def __init__(self, mw) -> None:
        """
        Initializes a FilteredDeckManager.

        Args:
            mw: Anki MainWindow
        """
        self.mainWindow = mw
        self.logger = Logger.Logger(mw)
        self.configuration = Configuration.Configuration(mw.addonManager.addonFromModule(__name__))
        self.ankiApiHandler = AnkiApiHandler.AnkiApiHandler()

    def _GetAllDecks(self):
        """
        Gets all decks from the deck due tree.
        """
        from google.protobuf import json_format
        self.allDecksList = []
        for deck in self.mainWindow.col.sched.deck_due_tree().children:
            serialized = json_format.MessageToDict(deck)
            newDeck = Deck.Deck()
            newDeck.FromDict(serialized, haveSearchTerms=False)
            newDeck.SearchTerms = []
            self.allDecksList.append(newDeck)
        self._InitializeFilteredDecksList()

    def CardCount(self) -> None:
        """
        Test function, returns the total card count.
        """
        return self.mainWindow.col.card_count()

    def _InitializeFilteredDecksList(self):
        """
        Iterates through all decks in the deck due tree and selects only the filtered decks.
        """
        self.filteredDecksList = []
        for deck in self.allDecksList:
            if deck.IsFiltered:
                deckConfig = self.mainWindow.col.sched.get_or_create_filtered_deck(deck_id=int(deck.DeckId)).config
                deck.Config.Reschedule = deckConfig.reschedule
                if not deckConfig.reschedule:
                    deck.Config.IntervalAgain = deckConfig.preview_again_secs
                    deck.Config.IntervalHard = deckConfig.preview_hard_secs
                    deck.Config.IntervalGood = deckConfig.preview_good_secs
                if len(deckConfig.search_terms) == 1 or len(deckConfig.search_terms) == 2:
                    for i, term in enumerate(deckConfig.search_terms):
                        deck.searchTerms.append(term.search)
                        if i == 0:
                            deck.Config.OrderBySearch1 = term.order
                            deck.Config.CardLimitSearch1 = term.limit
                        elif i == 1:
                            deck.Config.OrderBySearch2 = term.order
                            deck.Config.CardLimitSearch2 = term.limit
                        else:
                            pass
                deck.Config.AllowEmpty = self.mainWindow.col.sched.get_or_create_filtered_deck(deck_id=int(deck.DeckId)).allow_empty
                self.filteredDecksList.append(deck)

    @property
    def FilteredDecksList(self) -> list[Deck.Deck]:
        """
        Gets the list of filtered decks.

        Returns:
            list[Deck.Deck]: current list of filtered decks.
        """
        return self.filteredDecksList
    
    @property
    def StagedFilteredDecksList(self) -> list[Deck.Deck]:
        """
        Gets the list of filtered decks staged for import.

        Returns:
            list[Deck.Deck]: The current list of filtered decks staged for import.
        """
        return self.stagedFilteredDecksList
    
    @property
    def Configuration(self) -> Configuration.Configuration:
        """
        Gets the instance of the Configuration class, for reading add-on settings.

        Returns:
            Configuration.Configuration: instance of the Configuration class.
        """
        return self.configuration
    
    def WriteToFile(self, filepath: str, decks: list[Deck.Deck]) -> None:
        """
        Write list of filtered decks to file.

        Args:
            filepath (str): The absolute path of the output file to write the exported filtered decks file.
            decks (list[Deck.Deck]): The list of filtered decks to write to file.
        """
        import json
        with open(filepath, "w") as output:
            json.dump([deck.AsDict()for deck in decks], output, indent=2)
    
    def ReadFromFile(self, filepath: str) -> list[Deck.Deck]:
        """
        Reads list of filtered decks from file.

        Args:
            filepath (str): The absolute path of the input file to read from.

        Returns:
            list[Deck.Deck]: A list of filtered decks generated from the imported file.
        """
        import os.path
        if not os.path.exists(filepath):
            return  # invalid file
    
        import json
        importedDecks = []
        with open(filepath, "r") as inFile:
            data = json.load(inFile)
            for deckJson in data:
                deck = Deck.Deck()
                deck.FromDict(deckJson, haveSearchTerms=True)
                if self.logger.LoggingSupported: self.logger.Logger.debug(f"Imported deck: {deck.Name}")
                # will need to check for identical decks here
                importedDecks.append(deck)
        
        self.stagedFilteredDecksList = importedDecks
        return importedDecks

    def CreateFilteredDeck(self, deck: Deck.Deck, includeSuspended: bool, appendNewDue: bool) -> Constants.RETURN_CODES.UI_CODES:
        """
        Creates a filtered deck using the Anki backend based on the provided parameters.

        Args:
            deck (Deck.Deck): The Deck to use for Anki Filtered Deck creation.
            includeSuspended (bool): Set true if suspended cards should be unsuspended on deck creation.
            appendNewDue (bool): Set true if `(is:new OR is:due)` should be appended on filtered deck creation, useful for a filtered deck to be recreated daily.

        Returns:
            Constants.RETURN_CODES.UI_CODES: Enum value corresponding to success or failure state.
        """
        from aqt.operations.scheduling import add_or_update_filtered_deck
        if self.IsUnique(deck, self.StagedFilteredDecksList, importList=True):
            if self.IsUnique(deck, self.FilteredDecksList):
                if includeSuspended:
                    self.ankiApiHandler.UnsuspendCardsBySearchTerm(deck.SearchTerms[0])
                    if len(deck.SearchTerms) == 2:
                        self.ankiApiHandler.UnsuspendCardsBySearchTerm(deck.SearchTerms[1])
                
                newDeckConfig = self.Configuration if self.Configuration.UseGlobalConfig else deck.Config
                newDeck = self.ankiApiHandler.PrepareNewFilteredDeckForUpdate(deck, newDeckConfig, appendNewDue)
                
                add_or_update_filtered_deck(parent=self.mainWindow, deck=newDeck).run_in_background()
                return Constants.RETURN_CODES.UI_CODES.SUCCESS      
            else:
                return Constants.RETURN_CODES.UI_CODES.DECK_NOT_UNIQUE_EXISTING_LIST
        else:
            return Constants.RETURN_CODES.UI_CODES.DECK_NOT_UNIQUE_IMPORTED_LIST


    def IsUnique(self, deck: Deck.Deck, comparisonList: list[Deck.Deck], importList = False, checkNameOnly = False) -> bool:
        """
        Compares Deck name and Deck search terms to assess uniqueness. If both match, the deck is not considered unique.

        Args:
            deck (Deck.Deck): The Deck to compare.
            comparisonList (list[Deck.Deck]): The list of comparison decks to check against deck.
            importList (bool, optional): Flag to indicate whether comparisonList contains deck. Defaults to False.
            checkNameOnly (bool, optional): Flag to only check against deck names and not tags. Used for validating renaming of staged import decks. Defaults to False.

        Returns:
            bool: True if the deck is unique, otherwise False.
        """
        uniqueNameCheck = [x for x in comparisonList if (deck.Name == x.Name)]
        deckNameUnique = True
        searchQueryUnique = True
        if importList:
            deckNameUnique = len(uniqueNameCheck) <= 1     # will have one match of  if checking against the import list
        else:
            deckNameUnique = len(uniqueNameCheck) == 0
        
        if checkNameOnly:
            return deckNameUnique

        searchQueryUnique = True
        # now search through search queries to assess uniqueness
        # may not be the fastest approach
        deck1Terms = []
        if len(deck.SearchTerms) == 1:
            deck1Terms = deck.SearchTerms
        else:
            for term in deck.SearchTerms:
                deck1Terms += term
        
        numberOfMatches = 0
        for d in comparisonList:
            deck2Terms = []
            if len(d.SearchTerms) == 1:
                deck2Terms = d.SearchTerms
            else:
                for term in d.SearchTerms:
                    deck2Terms += term
            if sorted(deck1Terms) == sorted(deck2Terms):
                numberOfMatches += 1
        
        if importList:
            if numberOfMatches > 1:     # will have 1 match of itself
                searchQueryUnique = False
        else:
            if numberOfMatches > 0:
                searchQueryUnique = False

        return deckNameUnique and searchQueryUnique