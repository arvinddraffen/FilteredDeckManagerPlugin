#  Overview
Filtered Deck Manager is an Anki add-on providing support for importing and exporting filtered decks, with the primary motivation being for sharing filtered decks based on the same source deck. 
<br />

## Usage
### Exporting
To export a filtered deck, select the deck(s) for export using the checkboxes in the Select column, then press the Export Selected button. If exporting all filtered decks, the Export All button can be used.

The file exported is a `.json` file that is readable in any text editor.

### Importing
To import filtered decks, first select the file containing the data to import using the Open File button. This will stage the filtered decks in a table, showing data including the Deck Name, estimated total number of cards, additional toggles (as described below), and the tags included in the deck.

#### Import Toggles
* Include Suspended Cards
    * By default, creation of a filtered deck will not include cards that are not suspended (as the purpose is to review cards that have been studied). However, if using a shared filtered deck to begin studying, cards contained within the filtered deck may not have been unsuspended yet and would otherwise be missed. This toggle will automatically unsuspend any suspended cards that match the search query in the filtered deck for their inclusion.
* Append `(is:new OR is:due)`
    * This option will only include either new cards or cards that are due to be studied based on the Anki scheduler at the time of filtered deck creation/rebuild.