#!/usr/bin/env python
import sys
## from doctree.doctree_qt import main
from doctree.doctree import main

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ini = sys.argv[1]
    else:
        ini = 'MyMan.ini'
    main(ini)
