import doctree.pickle_dml as dml

FNAME = 'testfile.dtr'
testdata = [{'Application': 'DocTree'},
            [[(0, [(1, [])])]],
            {0: 'this is one text', 1: 'this is another'},
            {0: '0', 1: '0'}]


def test_write_to_files():
    settings, views, itemdict, textpos = testdata
    dml.write_to_files(FNAME, settings, views, itemdict, textpos)


def test_read_from_files():
    settings, views, itemdict, textpos = testdata
    dml.write_to_files(FNAME, settings, views, itemdict, textpos)
    data = dml.read_from_files('testfile')
    assert data == testdata


print(test_write_to_files())
test_read_from_files()
