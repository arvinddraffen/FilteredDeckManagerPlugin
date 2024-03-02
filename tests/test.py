import sys
print(sys.path)
from FilteredDeckManager import FilteredDeckManager

if __name__ == "__main__":
    from aqt import mw
    manager = FilteredDeckManager.FilteredDeckManagerSrc(mw)