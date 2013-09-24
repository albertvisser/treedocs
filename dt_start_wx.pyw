#!/usr/bin/env python
import sys
from doctree.doctree_wx import main

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ini = sys.argv[1]
    else:
        ini = '' # 'MyMan.pck'
    main(ini)
