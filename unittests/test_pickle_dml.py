import pathlib
import pytest
import doctree.pickle_dml as dml

FNAME = pathlib.Path('testfile.dtr')
testdata = [{'Application': 'DocTree'},
            [[(0, [(1, [])])]],
            {0: 'this is one text', 1: 'this is another'},
            {0: '0', 1: '0'}]


def _test_write_to_files():
    settings, views, itemdict, textpos = testdata
    dml.write_to_files(FNAME, settings, views, itemdict, textpos)


def _test_read_from_files():
    settings, views, itemdict, textpos = testdata
    dml.write_to_files(FNAME, settings, views, itemdict, textpos)
    data = dml.read_from_files('testfile')
    assert data == testdata
