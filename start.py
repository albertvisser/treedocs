#! /usr/bin/env python3
"""startup script voor DocTree
"""
import sys
from doctree.main import MainWindow

if __name__ == '__main__':
    if len(sys.argv) > 1:
        MainWindow(sys.argv[1])
    else:
        MainWindow()
