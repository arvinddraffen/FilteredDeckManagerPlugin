from .Models import Deck

class FilteredDeckManager:
    from anki.collection import Collection
    def __init__(self, mw) -> None:
        self.mainWindow = mw

    def _GetAllDecks(self):
        """Gets all decks from the deck due tree."""
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
        """Test function, returns the total card count."""
        return self.mainWindow.col.card_count()

    def _InitializeFilteredDecksList(self):
        """Iterates through all decks in the deck due tree and selects only the filtered decks."""
        self.filteredDecksList = []
        for deck in self.allDecksList:
            if deck.IsFiltered:
                deckConfig = self.mainWindow.col.sched.get_or_create_filtered_deck(deck_id=int(deck.DeckId)).config
                if len(deckConfig.search_terms) == 1 or len(deckConfig.search_terms) == 2:
                    for term in deckConfig.search_terms:
                        deck.searchTerms.append(term.search)
                self.filteredDecksList.append(deck)

    @property
    def FilteredDecksList(self) -> list:
        """Gets the list of filtered decks."""
        return self.filteredDecksList
    
    def WriteToFile(self) -> None:
        """Write list of filtered decks to file."""
        import json
        outFile = "C:\\Users\\goat1\\Documents\\output.json"    # prompt from FileDialog
        with open(outFile, "w") as output:
            json.dump([deck.AsDict()for deck in self.FilteredDecksList], output, indent=2)