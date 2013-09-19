DocTree
=======

This is an elaboration on my Apropos application,
with a vertical rather than a horizontal organisation of notes,
and the possibility of nesting notes underneath each other.

For that purpose it uses a tree view on the left-hand side
and a text window on the right-hand side.
Another addition to Apropos is that it supports text formatting.

Some ideas are inspired by Lotus Notes, e.g. the possibility of
`creating a sublevel by inserting a backslash surrounded by two spaces
in an item's title <wiki/create_sublevel>`_.
Another is `visually organizing the same collection of notes in different
ways <wiki/reorder_tree>`_.

This application also supports saving and loading files under different names,
and reordering items by sorting or using drag 'n drop.

Requirements
------------

- Python
- PyQT4 for the current GUI version
- wxPython for the older GUI version
