# Filtered Deck Manager
Provides an interface to import and export filtered decks.

## Roadmap
### Short-Term Core Features
* Get the filter that makes the filtered deck, and write to file.
    * For writing to file, add newlines.
* Work on UI
    * Multi-selectable list of filtered decks (right now just writes out everything)
    * Toggle for appending `(is:new OR is:due)` to final command
* Ensure output file can actually be read in (while important, at least if it can be output, it can be manually copy-pasted in, so not quite as a big a priority as output for now)
* Implement creation of a filtered deck from a specified filter
    * Subsequently add checks for if deck exists prior to attempting

### Longer Term
* Merging filtered decks