#  Filtered Deck Manager
Filtered Deck Manager is an Anki add-on providing support for importing and exporting filtered decks, with the primary motivation being for sharing filtered decks based on the same source deck. 
<br />

## Usage
### Exporting
To export a filtered deck, select the deck(s) for export using the checkboxes in the Select column, then press the Export Selected button. If exporting all filtered decks, the Export All button can be used.

The file exported is a `.json` file that is also readable in any text editor.

### Importing
To import filtered decks, first select the file containing the data to import using the Open File button. This will stage the filtered decks in a table, showing data including the Deck Name, estimated total number of cards, additional toggles (as described below), and the tags included in the deck.

#### Import Toggles
* Include Suspended Cards
    * By default, creation of a filtered deck will not include cards that are not suspended (as the purpose is to review cards that have been studied). However, if using a shared filtered deck to begin studying, cards contained within the filtered deck may not have been unsuspended yet and would otherwise be missed. This toggle will automatically unsuspend any suspended cards that match the search query in the filtered deck for their inclusion.
* Append `(is:new OR is:due)`
    * This option will only include either new cards or cards that are due to be studied based on the Anki scheduler at the time of filtered deck creation/rebuild.

#### Renaming Filtered Decks on Import
An option is provided for Filtered Decks to be renamed on import, which can be done by double-clicking on the filtered deck name in the table and entering the new name.

#### Detecting Duplicate Decks
On import, the add-on will check against existing filtered decks and other decks in the imported file to prevent import of a duplicate deck. The criteria used are an *exact match* of tags and the name of the deck.
* Note that this is an exact match of tags, and will not individually check tags (so therefore, the same set of tags in a different order would be considered a "different" deck). This behavior may be updated in the future, but this is the behavior on initial release.

### Configuration
For more detailed configuration options, `Filtered Deck Manager` has a overall add-on configuration as well as per-deck configuration. Add-on level configuration is modified through Anki Desktop, and deck configuration options are set on deck export and contained with the exported `.json` file.

In order to decide whether to use global add-on configurations, or accept the ones contained within a deck on import, modify the `use_global_config` option in the add-on settings.