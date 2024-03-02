class FilteredDeckManager:
    from anki.collection import Collection
    def __init__(self, mw) -> None:
        self.mainWindow = mw

    def CardCount(self) -> None:
        return self.mainWindow.col.card_count()

    def _InitializeFilteredDecksList(self):
        self._filteredDecks = self.mainWindow.col.sched.deck_due_tree()
        self.filteredDecksList = []
        for deck in self._filteredDecks.children:
            if deck.filtered:
                self.filteredDecksList.append(deck)

    @property
    def FilteredDecksList(self) -> list:
        return self.filteredDecksList
    
    def WriteToFile(self) -> None:
        import google.protobuf.internal.containers
        from google.protobuf import json_format
        import json
        outFile = "C:\\Users\\goat1\\Documents\\output.json"    # prompt from FileDialog
        with open(outFile, "w") as output:
            serialized = json_format.MessageToJson(self._filteredDecks)
            output.write(serialized)