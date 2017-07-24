"""DocTree startup program
"""
from __future__ import absolute_import
## from doctree_wx import main
## from doctree.doctree_qt4 import main
from doctree.doctree_qt import main

if __name__ == "__main__":
    main('data/qt_tree.pck')
    ## main('data/wx_tree.pck')
