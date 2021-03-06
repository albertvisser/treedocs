# -*- coding: utf-8 -*-
"""
Voor uitwisseling van Python2 naar Python3

lees een doctree file en sla het op zonder de sashposition vanuit de gui
to be run under Python 2
"""
import sys
import os
import shutil
try:
    import cPickle as pck
except ImportError:
    import pickle as pck

usage = """\
usage: [python] doctree_2to3.py <filename>
"""


def load(fname):
    """load the Python 2 created version
    """
    mld = ""
    try:
        f_in = open(fname, "rb")
    except IOError:
        return "couldn't open {}".format(fname)
    try:
        nt_data = pck.load(f_in)
    except EOFError:
        mld = "couldn't load data from {}".format(fname)
    finally:
        f_in.close()
    if mld:
        return mld
    try:
        test = nt_data[0]["AskBeforeHide"]
    except (ValueError, KeyError):
        return "{} is not a valid Doctree data file".format(fname)
    return nt_data


def save(fname, data):
    """Save in format suitable for Python 3
    """
    try:
        shutil.copyfile(fname, fname + ".py2")
    except IOError:
        pass
    with open(fname, "wb") as f_out:
        pck.dump(data, f_out, protocol=2)


def main(args):
    """Start processing
    """
    if sys.version >= '3':
        print('This script is not meant to be run using Python 3 or higher')
        return False
    if len(args) != 2:
        print("wrong number of arguments")
        return False
    fname = args[1]
    if not os.path.exists(fname):
        print("file does not exist")
        return False
    data = load(fname)
    if isinstance(data, str):
        print(data)
        return False
    for key, value in data[0].items():
        if key == "SashPosition":
            data[0][key] = 180
        elif key == "RootData":
            data[0][key] = unicode(value)
    for key, value in data[2].items():
        titel, text = value
        data[2][key] = (unicode(titel), unicode(text))
    save(fname, data)
    return True


if __name__ == '__main__':
    if not main(sys.argv):
        print(usage)
