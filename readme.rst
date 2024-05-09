DocTree
=======

This is an elaboration on my Apropos application,
with a vertical rather than a horizontal organisation of notes,
and the possibility of nesting notes underneath each other.

For that purpose it uses a tree view on the left-hand side
and a text window on the right-hand side.
Another addition to Apropos is that it supports text formatting.

Some ideas are inspired by Lotus Notes, e.g. the possibility of
creating a sublevel by inserting a backslash surrounded by two spaces
in an item's title.
Another is visually organizing the same collection of notes in different
ways.

This application also supports saving and loading files under different names,
and reordering items by sorting or using drag 'n drop.

Another little extra is that you can copy pictures into the texts.

Usage
-----

cd to the top directory, and run ``python(3) start.py``.
If you know which file you are working with, you can add its name as an extra parameter.

The GUI toolkit used is controlled in toolkit.py in the program subdirectory; 
currently you can only specify `wx` or `qt`.

Requirements
------------

- Python
- PyQT(5) for the current GUI version
- wxPython (Phoenix) for a version of the GUI where I don't have the rich text field fully working yet.

Note that the current implementation uses *pickle* for storing the data. 
I'm in the process of providing an alternative data backend, because I already tried out json and 
sqlite for NoteTree, I thought MomgoDB might be a good choice. It's still a work in progress though.
