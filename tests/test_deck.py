import sys
from aqt import QApplication
app = QApplication(sys.argv)
from FilteredDeckManager.Models import Deck


def test_deck_id_init():
    deck = Deck.Deck()
    assert deck.DeckId == None

def test_deck_id_set():
    deck = Deck.Deck()
    deckId = 5
    deck.DeckId = deckId
    assert deck.deckId == deckId
