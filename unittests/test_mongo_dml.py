import types
import pytest
import doctree.mongo_dml as dml

testdata = [{'Application': 'DocTree'},
            # [[(0, [(1, []), (2, [])])]],  # MongoDB ver-list de tuples
            [[[0, [[1, []], [2, []]]]]],
            {0: 'this is one text', 1: 'this is another'},
            {0: '0', 1: '0'}]

# ik weet niet of ik _add_doc en _update_doc nodig ga hebben
def test_add_doc(monkeypatch, capsys):
    def mock_insert_one(*args):
        print('called database.insert_one() with args', args)
        return types.SimpleNamespace(inserted_id='x')
    mycoll = dml.db['test']
    monkeypatch.setattr(dml.Collection, 'insert_one', mock_insert_one)
    assert dml._add_doc('test', 'doc') == 'x'
    assert capsys.readouterr().out == f"called database.insert_one() with args ({mycoll}, 'doc')\n"


def test_update_doc(monkeypatch, capsys):
    def mock_update(*args):
        print('called database.update_one() with args', args)
    mycoll = dml.db['test']
    monkeypatch.setattr(dml.Collection, 'update_one', mock_update)
    dml._update_doc('test', '1', 'doc')
    assert capsys.readouterr().out == (f"called database.update_one() with args ({mycoll},"
                                       " {'_id': '1'}, 'doc')\n")


def test_list_dtrees(monkeypatch, capsys):
    def mock_list():
        print('called db.list_collection_names()')
        return 'names'
    monkeypatch.setattr(dml.db, 'list_collection_names', mock_list)
    assert dml.list_dtrees() == 'names'
    assert capsys.readouterr().out == 'called db.list_collection_names()\n'


def test_create_new_dtree(monkeypatch, capsys):
    def mock_find_one_exc(*args):
        return True
    def mock_find_one(*args):
        print('called database.find_one() with args', args)
    def mock_insert_one(*args):
        print('called database.insert_one() with args', args)
    monkeypatch.setattr(dml.Collection, 'find_one', mock_find_one_exc)
    with pytest.raises(FileExistsError):
        dml.create_new_dtree('test')
    monkeypatch.setattr(dml.Collection, 'find_one', mock_find_one)
    monkeypatch.setattr(dml.Collection, 'insert_one', mock_insert_one)
    mycoll = dml.db['test']
    dml.create_new_dtree('test')
    assert capsys.readouterr().out == (
            f"called database.find_one() with args ({mycoll}, {{'type': 'settings'}})\n"
            f"called database.insert_one() with args ({mycoll}, {{'type': 'settings'}})\n"
            f"called database.insert_one() with args ({mycoll}, {{'type': 'imagelist'}})\n")


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


def test_clear_dtree(monkeypatch, capsys):
    def mock_find_one_not(*args):
        return False
    def mock_find_one(*args):
        print('called database.find_one() with args', args)
        return True
    def mock_drop(*args):
        print('called database.drop() with args', args)
    def mock_create_new_dtree(*args):
        print('called dml.create_new_tree() with args', args)
    monkeypatch.setattr(dml.Collection, 'find_one', mock_find_one_not)
    with pytest.raises(FileNotFoundError):
        dml.clear_dtree('test')
    mycoll = dml.db['test']
    monkeypatch.setattr(dml.Collection, 'find_one', mock_find_one)
    monkeypatch.setattr(dml.Collection, 'drop', mock_drop)
    monkeypatch.setattr(dml, 'create_new_dtree', mock_create_new_dtree)
    dml.clear_dtree('test')
    assert capsys.readouterr().out == (
        f"called database.find_one() with args ({mycoll}, {{'type': 'settings'}})\n"
        f"called database.drop() with args ({mycoll},)\n")
    dml.clear_dtree('test', recreate=True)
    assert capsys.readouterr().out == (
        f"called database.find_one() with args ({mycoll}, {{'type': 'settings'}})\n"
        f"called database.drop() with args ({mycoll},)\n"
        "called dml.create_new_tree() with args ('test',)\n")


def test_rename_dtree(monkeypatch, capsys):
    def mock_find_one(*args):
        return True
    def mock_find_none(*args):
        print('called database.find_one() with args', args)
        return None
    def mock_rename(*args):
        print('called database.rename() with args', args)
    monkeypatch.setattr(dml.Collection, 'find_one', mock_find_one)
    with pytest.raises(FileExistsError) as exc:
        dml.rename_dtree('test', 'new')
    assert str(exc.value) == 'new_name_taken'
    monkeypatch.setattr(dml.Collection, 'find_one', mock_find_none)
    monkeypatch.setattr(dml.Collection, 'rename', mock_rename)
    mycoll = dml.db['test']
    newcoll = dml.db['other']
    dml.rename_dtree('test', 'other')
    assert capsys.readouterr().out == (
            f"called database.find_one() with args ({newcoll}, {{'type': 'settings'}})\n"
            f"called database.rename() with args ({mycoll}, 'other')\n")


def _test_rename_dtree():
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


def _test_write_to_files():  # testee moet nog aangepast worden
    filename = 'testfile'
    if filename in dml.list_dtrees():
        dml.clear_dtree(filename, recreate=True)
    else:
        dml.create_new_dtree(filename)
    settings, views, itemdict, textpos = testdata
    dml.write_to_files(filename, settings, views, itemdict, textpos, '')
    return_data = dml.read_dtree(filename, readable=True)
    assert list(return_data) == testdata


def _test_read_from_files():  # testee moet nog aangepast worden
    filename = 'testfile'
    if filename in dml.list_dtrees():
        dml.clear_dtree(filename, recreate=True)
    else:
        dml.create_new_dtree(filename)
    # settings, views, itemdict, textpos = testdata
    dml.write_to_files(filename, *testdata)  # settings, views, itemdict, textpos)
    opts, view, viewcount, itemdict, textpos = dml.read_from_files('testfile')
    assert [opts, view, itemdict, textpos] == testdata
