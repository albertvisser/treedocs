#! /usr/bin/env python3
"""startup script voor DocTree
"""
import sys
from doctree.doctree import main

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ini = sys.argv[1]
    else:
        ini = ''  # 'MyMan.pck'
    main(ini)
