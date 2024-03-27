# Filtered Deck Manager
Provides an interface to import and export filtered decks.

## Roadmap
### Short-Term Core Features
* Work on UI
    * Toggle for appending `(is:new OR is:due)` to final command
* Ensure output file can actually be read in (while important, at least if it can be output, it can be manually copy-pasted in, so not quite as a big a priority as output for now)
* Implement creation of a filtered deck from a specified filter
    * Subsequently add checks for if deck exists prior to attempting

### Longer Term
* Toggle to unsuspend suspended cards (that would otherwise not be included) that are part of filtered deck tags
* Merging filtered decks