import sys
from aqt import QApplication
import pytest
app = QApplication(sys.argv)
from FilteredDeckManager.Models import Deck
from FilteredDeckManager.Utilities import Configuration

@pytest.fixture(scope="session")
def populated_deck() -> Deck.Deck:
    deck = Deck.Deck()
    deck.DeckId = 33
    deck.Name = "Test Name"
    deck.ReviewCount = 20
    deck.TotalInDeck = 20
    deck.totalIncludingChildren = 20
    deck.IsFiltered = True
    deck.SearchTerms = ["tag:test_tag"]
    deck.Config = Configuration.Configuration()
    deck.Config.AllowEmpty = False
    deck.Config.OrderBySearch1 = 8
    deck.Config.CardLimitSearch1 = 100
    deck.Config.Reschedule = True
    return deck

@pytest.fixture(scope="session")
def populated_deck_as_dict() -> dict:
    return {
    "deckId": 33,
    "name": "Test Name",
    "reviewCount": 20,
    "totalInDeck": 20,
    "totalIncludingChildren": 20,
    "filtered": True,
    "search_terms": '["tag:test_tag"]',
    "config": '{"search_1": {"order": 8, "card_limit": 100}, "allow_empty": false, "reschedule": true}'
  }