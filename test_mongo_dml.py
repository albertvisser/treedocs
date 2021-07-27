import doctree.mongo_dml as dml

testdata = [{'Application': 'DocTree'},
            # [[(0, [(1, []), (2, [])])]],  # MongoDB ver-list de tuples
            [[[0, [[1, []], [2, []]]]]],
            {0: 'this is one text', 1: 'this is another'},
            {0: '0', 1: '0'}]
# ik weet niet of ik _add_doc en _update_doc nodig ga hebben

def test_list_dtrees():
    print('output van list_dtrees:', dml.list_dtrees())

def test_create_new_dtree():
    info = dml.list_dtrees()
    if 'test' not in info:
        data = dml.create_new_dtree('test')
        print('data indien nog niet aanwezig:', data)
        info = dml.list_dtrees()
    assert 'test' in info
    try:
        dml.create_new_dtree('test')
    except FileExistsError:
        pass  # verwacht
    else:
        print('test_create_new_dtree failed: bij 2e keer aanmaken werd een exception verwacht')

def test_read_dtree():
    info = dml.list_dtrees()
    if 'test' not in info:
        dml.create_new_dtree('test')
    # print([x for x in dml.read_dtree('test')])
    data = list(dml.read_dtree('test'))
    assert len(data) == 2
    assert data[0]['type'] == 'settings'
    # assert data[1]['type'] == 'textpos'
    assert data[1]['type'] == 'imagelist'

def test_clear_dtree():
    info = dml.list_dtrees()
    if 'test' not in info:
        dml.create_new_dtree('test')
    assert 'test' in dml.list_dtrees()
    dml.clear_dtree('test')
    assert 'test' not in dml.list_dtrees()
    try:
        dml.clear_dtree('test')
    except FileNotFoundError:
        pass  # verwacht
    else:
        print('test_clear_dtree failed: bij 2e keer leegmaken werd een exception verwacht')
    assert 'test' not in dml.list_dtrees()
    dml.create_new_dtree('test')
    assert 'test' in dml.list_dtrees()
    dml.clear_dtree('test', recreate=True)
    assert 'test' in dml.list_dtrees()

def test_rename_dtree():
    info = dml.list_dtrees()
    if 'test' not in info:
        dml.create_new_dtree('test')
    if 'new' not in info:
        dml.create_new_dtree('new')
    if 'newer' in info:
        dml.clear_dtree('newer')
    info = dml.list_dtrees()
    assert 'test' in info and 'new' in info and 'newer' not in info
    try:
        dml.rename_dtree('test', 'new')
    except FileExistsError:
        pass  # verwacht
    else:
        print('test_rename_dtree failed: bij hernoemen naar bestaand wordt een exception verwacht')
    dml.rename_dtree('test', 'newer')
    info = dml.list_dtrees()
    assert 'new' in info and 'newer' in info

def test_write_to_files():
    filename = 'testfile'
    if filename in dml.list_dtrees():
        dml.clear_dtree(filename, recreate=True)
    else:
        dml.create_new_dtree(filename)
    settings, views, itemdict, textpos = testdata
    dml.write_to_files(filename, settings, views, itemdict, textpos)
    return_data = dml.read_dtree(filename, readable=True)
    assert list(return_data) == testdata

def test_read_from_files():
    filename = 'testfile'
    if filename in dml.list_dtrees():
        dml.clear_dtree(filename, recreate=True)
    else:
        dml.create_new_dtree(filename)
    # settings, views, itemdict, textpos = testdata
    dml.write_to_files(filename, *testdata)  # settings, views, itemdict, textpos)
    opts, view, viewcount, itemdict, textpos = dml.read_from_files('testfile')
    assert [opts, view, itemdict, textpos] == testdata


test_list_dtrees()
test_read_dtree()
test_create_new_dtree()
test_clear_dtree()
test_rename_dtree()
test_write_to_files()
test_read_from_files()
