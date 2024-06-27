from aqt import mw
from anki.scheduler import FilteredDeckForUpdate
from anki.decks import FilteredDeckConfig

from FilteredDeckManager.Models import Deck
from FilteredDeckManager.Utilities import Configuration

class AnkiApiHandler:
    """
    Provides an interface between FilteredDeckManager and the Anki API.
    """
    def __init__(self) -> None:
        """
        Creates a new AnkiApiHandler.
        """
        pass


    def UnsuspendCardsBySearchTerm(self, searchTerm: str):
        """
        Unsuspends cards based on the provided search term.

        Args:
            searchTerm (str): The search term to use for unsuspending.
        """
        cardsToUnsuspend = mw.col.find_cards(searchTerm)
        mw.col.sched.unsuspend_cards(cardsToUnsuspend)


    def PrepareNewFilteredDeckForUpdate(self, deck: Deck.Deck, config: Configuration.Configuration, appendNewDue: bool) -> FilteredDeckForUpdate:
        """
        Converts a Deck into a anki.scheduler.FilteredDeckForUpdate for creation with the Anki API.

        Args:
            deck (Deck.Deck): The Deck to use for filtered deck creation.
            config (Configuration.Configuration): The associated Configuration options for the Deck.
            appendNewDue (bool): True if `(is:new OR is:due)` should be appended on filtered deck creation.

        Returns:
            FilteredDeckForUpdate: The created anki.scheduler.FilteredDeckForUpdate that can be used for creation of a filtered deck with the Anki API.
        """
        ankiDeck = FilteredDeckForUpdate()
        ankiDeck.name = deck.Name
        ankiDeck.allow_empty = config.AllowEmpty
        ankiDeck.config.reschedule = config.Reschedule
        
        if not config.Reschedule:
            ankiDeck.config.preview_again_secs = config.IntervalAgain
            ankiDeck.config.preview_hard_secs = config.IntervalHard
            ankiDeck.config.preview_good_secs = config.IntervalGood
        
        terms = [FilteredDeckConfig.SearchTerm(search=deck.searchTerms[0],limit=config.CardLimitSearch1,order=config.OrderBySearch1)]
        if appendNewDue:
            terms = [FilteredDeckConfig.SearchTerm(search=f"{deck.searchTerms[0]} (is:new OR is:due)",limit=config.CardLimitSearch1,order=config.OrderBySearch1)]
        else:
            terms = [FilteredDeckConfig.SearchTerm(search=deck.searchTerms[0],limit=config.CardLimitSearch1,order=config.OrderBySearch1)]

        if len(deck.SearchTerms) == 2:
            if appendNewDue:
                terms = [FilteredDeckConfig.SearchTerm(search=f"{deck.searchTerms[1]} (is:new OR is:due)",limit=config.CardLimitSearch2,order=config.OrderBySearch2)]
            else:
                terms = [FilteredDeckConfig.SearchTerm(search=deck.searchTerms[1],limit=config.CardLimitSearch2,order=config.OrderBySearch2)]
        
        ankiDeck.config.search_terms.extend(terms)

        return ankiDeck
