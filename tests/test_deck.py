import sys
from aqt import QApplication
import pytest
app = QApplication(sys.argv)
from FilteredDeckManager.Models import Deck
from FilteredDeckManager.Utilities import Configuration

def test_init():
    deck = Deck.Deck()
    assert deck.DeckId == None
    assert deck.Name == None
    assert deck.Level == None
    assert deck.ReviewCount == None
    assert deck.LearnCount == None
    assert deck.NewCount == None
    assert deck.IntradayLearning == None
    assert deck.InterdayLearningUncapped == None
    assert deck.NewUncapped == None
    assert deck.ReviewUncapped == None
    assert deck.TotalInDeck == None
    assert deck.TotalIncludingChildren == None
    assert deck.IsFiltered == None
    assert deck.SearchTerms == None
    assert isinstance(deck.Config, Configuration.Configuration)

def test_id_set():
    deck = Deck.Deck()
    deckId = 5
    deck.DeckId = deckId
    assert deck.deckId == deckId

def test_name_set():
    deck = Deck.Deck()
    name = "Test Name"
    deck.Name = name
    assert deck.Name == name

def test_level_set():
    deck = Deck.Deck()
    level = 2
    deck.Level = level
    assert deck.Level == level

def test_review_count_set():
    deck = Deck.Deck()
    reviewCount = 555
    deck.ReviewCount = reviewCount
    assert deck.ReviewCount == reviewCount

def test_learn_count_set():
    deck = Deck.Deck()
    learnCount = 456
    deck.LearnCount = learnCount
    assert deck.LearnCount == learnCount

def test_new_count_set():
    deck = Deck.Deck()
    newCount = 785
    deck.NewCount = newCount
    assert deck.NewCount == newCount

def test_intraday_learning_set():
    deck = Deck.Deck()
    intradayLearning = 35
    deck.IntradayLearning = intradayLearning
    assert deck.IntradayLearning == intradayLearning

def test_interday_learning_uncapped_set():
    deck = Deck.Deck()
    interdayLearningUncapped = 684
    deck.InterdayLearningUncapped = interdayLearningUncapped
    assert deck.InterdayLearningUncapped == interdayLearningUncapped

def test_new_uncapped_set():
    deck = Deck.Deck()
    newUncapped = 95
    deck.NewUncapped = newUncapped
    assert deck.NewUncapped == newUncapped

def test_review_uncapped_set():
    deck = Deck.Deck()
    reviewUncapped = 926
    deck.ReviewUncapped = reviewUncapped
    assert deck.ReviewUncapped == reviewUncapped

def test_total_indeck_set():
    deck = Deck.Deck()
    totalInDeck = 637
    deck.TotalInDeck = totalInDeck
    assert deck.TotalInDeck == totalInDeck

def test_total_including_children_set():
    deck = Deck.Deck()
    totalIncludingChildren = 908
    deck.TotalIncludingChildren = totalIncludingChildren
    assert deck.TotalIncludingChildren == totalIncludingChildren

def test_is_filtered_set():
    deck = Deck.Deck()
    isFiltered = True
    deck.IsFiltered = isFiltered
    assert deck.IsFiltered == isFiltered

def test_search_terms_set():
    deck = Deck.Deck()
    searchTerms = ["tag:#AK\\_Step1\\_v12::#B&B::14\\_MSK::02\\_Cell\\_Biology::03\\_Smooth\\_Muscle"]
    deck.SearchTerms = searchTerms
    assert deck.SearchTerms == searchTerms

def test_search_terms_as_string_one_term():
    deck = Deck.Deck()
    searchTerms = ["tag:#AK\\_Step1\\_v12::#B&B::14\\_MSK::02\\_Cell\\_Biology::03\\_Smooth\\_Muscle"]
    deck.SearchTerms = searchTerms
    searchTermsAsString = f"{searchTerms[0]}"
    assert deck.SearchTermsAsString == searchTermsAsString

def test_search_terms_as_string_two_terms():
    deck = Deck.Deck()
    searchTerms = ["tag:#AK\\_Step1\\_v12::#B&B::14\\_MSK::02\\_Cell\\_Biology::03\\_Smooth\\_Muscle", "tag:#AK\\_Step1\\_v12::#B&B::09\\_GI::01\\_Anatomy::03\\_Gastrointestinal\\_Blood\\_Supply"]
    deck.SearchTerms = searchTerms
    searchTermsAsString = f"{searchTerms[0]} {searchTerms[1]}"
    assert deck.SearchTermsAsString == searchTermsAsString

def test_as_dict(populated_deck, populated_deck_as_dict):
    deck = populated_deck
    assert deck.AsDict() == populated_deck_as_dict

def test_from_dict(populated_deck, populated_deck_as_dict):
    deck = Deck.Deck()
    deck_dict = populated_deck_as_dict
    deck.FromDict(deck_dict)
    assert populated_deck == deck