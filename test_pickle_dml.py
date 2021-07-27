import doctree.mongo_dml as dml

testdata = [{'Application': 'DocTree'},
            [[(0, [(1, [])])]],
            {0: 'this is one text', 1: 'this is another'},
            {0: '0', 1: '0'}]

def test_write_to_files():
    filename = 'testfile'
    settings, views, itemdict, textpos = testdata
    dml.write_to_files(filename, settings, views, itemdict, textpos)
    data_read = '', [], {}, {}
    for item in dml.read_dtree('testfile'):
        if item['type'] == 'settings':
            data[0] = item['data']
        elif item['type'] == 'view':
            data[1].append(item['data'])
        elif item['type'] == 'textitem':
            data[2][item['textid']] = item['data']
            data[3][item['textid']] = item['textpos']

def test_read_from_files():
    filename = 'testfile'
    if filename in dml.list_dtrees():
        dml.clear_dtree(filename, recreate=True)
    else:
        dml.create_new_dtree(filename)
    settings, views, itemdict, textpos = testdata
    dml.write_to_files(filename, settings, views, itemdict, textpos)
    data = dml.read_from_files('testfile')
    assert data == testdata


print(test_write_to_files())
test_read_from_files()
