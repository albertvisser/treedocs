#!/usr/bin/env python
import sys
from doctree.doctree_wx import App

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ini = sys.argv[1]
    else:
        ini = 'MyMan.pck'
    app = App(ini)
    app.MainLoop()
