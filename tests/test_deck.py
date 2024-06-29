import sys
from aqt import QApplication
app = QApplication(sys.argv)
from FilteredDeckManager.Models import Deck


def test_deck_id_init():
    deck = Deck.Deck()
    assert deck.DeckId == None
