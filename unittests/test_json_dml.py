"""unittests for ./doctree/pickle_dml.py
"""
import pathlib
import pytest
import doctree.json_dml as testee

testdata = [{'Application': 'DocTree'},
            [[(0, [(1, [])])]],
            {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
            {0: 0, 1: 0}]


class MockZipFileBad:
    """stub
    """
    def __init__(self, *args, **kwargs):
        print('called zipfile.ZipFile with args', args, kwargs)
        raise testee.zpf.BadZipFile('File is not a zip file')


class MockZipFileErr:
    """stub
    """
    def __init__(self, *args, **kwargs):
        print('called zipfile.ZipFile with args', args, kwargs)
    def __enter__(self):
        """stub
        """
        print('called ZipFile.__enter__')
        return self
    def namelist(self):
        """stub
        """
        print('called ZipFile.namelist')
        return ["name", "list"]
    def extractall(self, path):
        """stub
        """
        print(f'called ZipFile.extractall with arg `{path}`')
        raise FileNotFoundError('No data file found')
    def __exit__(self, *args):
        """stub
        """
        print('called ZipFile.__exit__')
        return False


class MockZipFileOk:
    """stub
    """
    def __init__(self, *args, **kwargs):
        print('called zipfile.ZipFile with args', args, kwargs)
    def __enter__(self):
        """stub
        """
        print('called ZipFile.__enter__')
        return self
    def extractall(self, path):
        """stub
        """
        print(f'called ZipFile.extractall with arg `{path}`')
        path.mkdir()
        (path / '00000.json').touch()
    def __exit__(self, *args):
        """stub
        """
        print('called ZipFile.__exit__')
        return True
    def namelist(self):
        """stub
        """
        print('called ZipFile.namelist')
        return []
    def write(self, *args, **kwargs):
        """stub
        """
        print('called ZipFile.write with args', args, kwargs)


def test_read_from_files(monkeypatch, capsys, tmp_path):
    """unittest for pickle_dml.read_from_files
    """
    def mock_load_err(*args):
        """stub
        """
        print('called json.load with args', args)
        raise UnicodeDecodeError('XXX', b'xxx', 1, 3, 'Not Unicode encoded')
    def mock_load_err2(*args):
        """stub
        """
        print('called json.load with args', args)
        raise testee.json.JSONDecodeError('Not JSON encoded', '00000.json', 1)
    def mock_load(*args):
        """stub
        """
        print('called json.load with args', args)
        return testdata  # {0: testdata[0], 1: testdata[1], 2: testdata[2], 3: testdata[3]}
    def mock_namelist(self):
        """stub
        """
        print('called ZipFile.namelist')
        return ['00001.png', '00004.png']
    def mock_namelist_2(self):
        """stub
        """
        print('called ZipFile.namelist')
        return ['00000.json', '00001.png', '00004.png']
    (tmp_path / 'test_read').mkdir(exist_ok=True)
    testfile = tmp_path / 'test_read' / 'testfile.dtr'
    imagepath = tmp_path / 'temp_path_for_images'

    # geen filenaam
    assert testee.read_from_files('', '', imagepath) == ['missing filename']
    assert capsys.readouterr().out == ""
    # 19-64
    # file bestaat niet
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"[Errno 2] No such file or directory: '{testfile}'"]
    assert capsys.readouterr().out == ""
    # 21-22, 24-64
    testfile.touch()
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFileBad)
    assert testee.read_from_files(testfile, '', imagepath) == ["File is not a zip file"]
    assert capsys.readouterr().out == f"called zipfile.ZipFile with args ({testfile!r},) {{}}\n"
    # 21-22, 25-64
    read_zipfile = (f"called zipfile.ZipFile with args ({testfile!r},) {{}}\n"
                    "called ZipFile.__enter__\n"
                    "called ZipFile.namelist\n"
                    f"called ZipFile.extractall with arg `{imagepath}`\n"
                    "called ZipFile.__exit__\n")
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFileErr)
    assert testee.read_from_files(testfile, '', imagepath) == ["No data file found"]
    assert capsys.readouterr().out == read_zipfile

    # 25-64
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFileOk)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile} appears to be empty"]
    assert capsys.readouterr().out == read_zipfile
    # 26-29, 34-64
    monkeypatch.setattr(MockZipFileOk, 'namelist', mock_namelist)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} does not contain a data portion"]
    assert capsys.readouterr().out == read_zipfile
    # 27-29, 36-64
    monkeypatch.setattr(MockZipFileOk, 'namelist', mock_namelist_2)
    assert testee.read_from_files(testfile, '', imagepath) == [
            "Expecting value: line 1 column 1 (char 0)"]
    assert capsys.readouterr().out == read_zipfile
    # 47-64
    # json.load gemocked
    read_zip_json = read_zipfile + ("called json.load with args (<_io.TextIOWrapper"
                                    f" name='{imagepath / "00000.json"}'"
                                    " mode='r' encoding='UTF-8'>,)\n")
    monkeypatch.setattr(testee.json, 'load', mock_load_err)
    assert testee.read_from_files(testfile, '', imagepath) == [
            "'XXX' codec can't decode bytes in position 1-2: Not Unicode encoded"]
    assert capsys.readouterr().out == read_zip_json
    # 47-64
    monkeypatch.setattr(testee.json, 'load', mock_load_err2)
    assert testee.read_from_files(testfile, '', imagepath) == [
            "Not JSON encoded: line 1 column 2 (char 1)"]
    assert capsys.readouterr().out == read_zip_json
    # 47-64
    monkeypatch.setattr(testee.json, 'load', mock_load)
    testdata = {}
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} is not a valid DocTree data file"]
    assert capsys.readouterr().out == read_zip_json
    # 53-64
    testdata = {0: {}}
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} is not a valid DocTree data file"]
    assert capsys.readouterr().out == read_zip_json
    # 53-64
    testdata = {0: {'Application': 'Not Doctree'}}
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} is not a valid DocTree data file"]
    assert capsys.readouterr().out == read_zip_json
    # 53-64
    testdata = {0: {'Application': 'DocTree'}}
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'},
                                                               [[]], {}, {},
                                                               ['00001.png', '00004.png'])
    assert capsys.readouterr().out == read_zip_json
    # 62
    testdata = {0: {'Application': 'DocTree'}, 1: []}
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'},
                                                               [], {}, {},
                                                               ['00001.png', '00004.png'])
    assert capsys.readouterr().out == read_zip_json
    # 62
    testdata = {0: {'Application': 'DocTree'}, 1: [['x']]}
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'},
                                                               [['x']], {}, {},
                                                               ['00001.png', '00004.png'])
    assert capsys.readouterr().out == read_zip_json
    # 62
    testdata = {0: {'Application': 'DocTree'}, 1: [[(0, [(1, [])])]]}
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'},
                                                               [[(0, [(1, [])])]], {}, {},
                                                               ['00001.png', '00004.png'])
    assert capsys.readouterr().out == read_zip_json
    # 62
    testdata = {0: {'Application': 'DocTree'}, 1: [[(0, [(1, [])])]], 2: {}}
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'},
                                                               [[(0, [(1, [])])]], {}, {},
                                                               ['00001.png', '00004.png'])
    assert capsys.readouterr().out == read_zip_json
    # 62
    testdata = {0: {'Application': 'DocTree'}, 1: [[(0, [(1, [])])]], 2: {'x': 'y'}}
    with pytest.raises(ValueError) as e:
        testee.read_from_files(testfile, '', imagepath)
    assert str(e.value) == "invalid literal for int() with base 10: 'x'"
    assert capsys.readouterr().out == read_zip_json
    # 62
    testdata = {0: {'Application': 'DocTree'}, 1: [[(0, [(1, [])])]],
                2: {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')}}
    assert testee.read_from_files(testfile, '', imagepath) == (
            {'Application': 'DocTree'}, [[(0, [(1, [])])]],
            {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
            {}, ['00001.png', '00004.png'])
    assert capsys.readouterr().out == read_zip_json
    # 62
    testdata = {0: {'Application': 'DocTree'}, 1: [[(0, [(1, [])])]],
                2: {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')}, 3: {}}
    assert testee.read_from_files(testfile, '', imagepath) == (
            {'Application': 'DocTree'}, [[(0, [(1, [])])]],
            {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
            {}, ['00001.png', '00004.png'])
    assert capsys.readouterr().out == read_zip_json
    # 62
    testdata = {0: {'Application': 'DocTree'}, 1: [[(0, [(1, [])])]],
                2: {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
                3: {'x': 'y'}}
    with pytest.raises(ValueError) as e:
        testee.read_from_files(testfile, '', imagepath)
    assert str(e.value) == "invalid literal for int() with base 10: 'x'"
    assert capsys.readouterr().out == read_zip_json
    # 62
    testdata = {0: {'Application': 'DocTree'}, 1: [[(0, [(1, [])])]],
                2: {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
                3: {0: 0, 1: 0}}
    assert testee.read_from_files(testfile, '', imagepath) == (
            {'Application': 'DocTree'}, [[(0, [(1, [])])]],
            {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
            {0: 0, 1: 0}, ['00001.png', '00004.png'])
    assert capsys.readouterr().out == read_zip_json
    # 62
    testdata = {0: {'Application': 'DocTree'}, 1: [[(0, [(1, [])])]],
                2: {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
                3: {0: 0, 1: 0}}
    assert testee.read_from_files('', testfile, imagepath) == (
            {'Application': 'DocTree'}, [[(0, [(1, [])])]],
            {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
            {0: 0, 1: 0}, [])
    assert capsys.readouterr().out == read_zip_json


def test_verify_imagenames(monkeypatch, capsys):
    """unittest for pickle_dml.verify_imagenames
    """
    def mock_determine(filename):
        print(f"called determine_highest_in_zipfile with arg '{filename}'")
        return ['00005.png', '00001.png', '00003.png'], 5
    def mock_rename(*args):
        print('called path.rename with args', args)
    monkeypatch.setattr(testee, 'determine_highest_in_zipfile', mock_determine)
    monkeypatch.setattr(pathlib.Path, 'rename', mock_rename)
    other_file = pathlib.Path('testfile.trd')
    temp_imagepath = pathlib.Path('/tmp/path/to/images')
    items_to_move = [('text-1', ('title-1', '<html><body><img src="00002.png"/></body></html>')),
                     ('text-2', ('title-2', '<html><body><img src="00003.png"/></body></html>')),
                     ('text-3', ('title-3', '<html><body><img src="00006.png"/></body></html>'))]
    # breakpoint()
    new_items, imagelist = testee.verify_imagenames(items_to_move, temp_imagepath, other_file)
    assert new_items == [('text-1', ('title-1', '<html><body><img src="00002.png"/></body></html>')),
                         ('text-2', ('title-2', '<html><body><img src="00006.png"/></body></html>')),
                         ('text-3', ('title-3', '<html><body><img src="00007.png"/></body></html>'))]
    assert imagelist == ['00002.png', '00006.png', '00007.png']
    assert capsys.readouterr().out == (
            "called determine_highest_in_zipfile with arg 'testfile.trd'\n"
            "called path.rename with args (PosixPath('/tmp/path/to/images/00003.png'),"
            " PosixPath('/tmp/path/to/images/00006.png'))\n"
            "called path.rename with args (PosixPath('/tmp/path/to/images/00006.png'),"
            " PosixPath('/tmp/path/to/images/00007.png'))\n")


def test_determine_highest_in_zipfile(monkeypatch, capsys):
    """unittest for pickle_dml.determine_highest_in_zipfile
    """
    def mock_namelist(self):
        print('called ZipFile.namelist')
        return []
    def mock_namelist_2(self):
        print('called ZipFile.namelist')
        return ['00005.png', '00001.png', '00003.png']
    monkeypatch.setattr(MockZipFileOk, 'namelist', mock_namelist)
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFileOk)
    filename = pathlib.Path('testfile.trd')
    monkeypatch.setattr(MockZipFileOk, 'namelist', mock_namelist)
    assert testee.determine_highest_in_zipfile(filename) == ([], 0)
    assert capsys.readouterr().out == ("called zipfile.ZipFile with args ('testfile.trd',) {}\n"
                                       "called ZipFile.__enter__\n"
                                       "called ZipFile.namelist\n"
                                       "called ZipFile.__exit__\n")
    monkeypatch.setattr(MockZipFileOk, 'namelist', mock_namelist_2)
    assert testee.determine_highest_in_zipfile(filename) == (['00005.png', '00001.png',
                                                              '00003.png'], 5)
    assert capsys.readouterr().out == ("called zipfile.ZipFile with args ('testfile.trd',) {}\n"
                                       "called ZipFile.__enter__\n"
                                       "called ZipFile.namelist\n"
                                       "called ZipFile.__exit__\n")


def test_write_to_files(monkeypatch, capsys, tmp_path):
    """unittest for pickle_dml.write_to_files
    """
    def mock_copy(*args):
        print('called shutil.copyfile with args', args)
        raise FileNotFoundError
    def mock_copy_2(*args):
        print('called shutil.copyfile with args', args)
    def mock_dump(*args):
        print('called json.dump with args', args)
    monkeypatch.setattr(testee.json, 'dump', mock_dump)
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFileOk)
    temp_imagepath = tmp_path / 'images'
    temp_imagepath.mkdir()
    filename = tmp_path / 'testfile.trd'
    backupname = tmp_path / 'testfile.trd.bak'
    dataname = temp_imagepath / '00000.json'
    opts = {'opts': 'dict'}
    views = [[(1, []), (2, [])], [(1, [(2, [])])]]
    itemdict = {1: ('titel1', 'tekst1'), 2: ('titel2', 'tekst2')}
    textpositions = {0: 0, 1: 0}
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    assert testee.write_to_files(filename, opts, views, itemdict, textpositions,
                                 temp_imagepath) == []
    assert capsys.readouterr().out == (
            f"called json.dump with args ({{0: {opts}, 1: {views}, 2: {itemdict},"
            f" 3: {textpositions}}},"
            f" <_io.TextIOWrapper name='{dataname}' mode='w' encoding='UTF-8'>)\n"
            f"called shutil.copyfile with args ('{filename}', '{backupname}')\n"
            f"called zipfile.ZipFile with args ('{filename}', 'w')"
            f" {{'compression': {testee.zpf.ZIP_DEFLATED}}}\n"
            "called ZipFile.__enter__\n"
            f"called ZipFile.write with args ('{dataname}',) {{'arcname': '00000.json'}}\n"
            "called ZipFile.__exit__\n")
    itemdict = {'text-1': ('title-1', '<html><body><img src="00002.png"/></body></html>'),
                'text-2': ('title-2', '<html><body><img src="00003.png"/></body></html>'),
                'text-3': ('title-3', '<html><body><img src="00006.png"/></body></html>')}
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy_2)
    assert testee.write_to_files(filename, opts, views, itemdict, textpositions,
                                 temp_imagepath, backup=False) == []
    assert capsys.readouterr().out == (
            f"called json.dump with args ({{0: {opts}, 1: {views}, 2: {itemdict},"
            f" 3: {textpositions}}},"
            f" <_io.TextIOWrapper name='{dataname}' mode='w' encoding='UTF-8'>)\n"
            f"called zipfile.ZipFile with args ('{filename}', 'w')"
            f" {{'compression': {testee.zpf.ZIP_DEFLATED}}}\n"
            "called ZipFile.__enter__\n"
            f"called ZipFile.write with args ('{dataname}',) {{'arcname': '00000.json'}}\n"
            "called ZipFile.__exit__\n")
    (temp_imagepath / '00002.png').touch()
    (temp_imagepath / '00003.png').touch()
    (temp_imagepath / '00006.png').touch()
    assert testee.write_to_files(filename, opts, views, itemdict, textpositions,
                                 temp_imagepath, backup=False) == ['00002.png', '00003.png',
                                                                   '00006.png']
    assert capsys.readouterr().out == (
            f"called json.dump with args ({{0: {opts}, 1: {views}, 2: {itemdict},"
            f" 3: {textpositions}}},"
            f" <_io.TextIOWrapper name='{dataname}' mode='w' encoding='UTF-8'>)\n"
            f"called zipfile.ZipFile with args ('{filename}', 'w')"
            f" {{'compression': {testee.zpf.ZIP_DEFLATED}}}\n"
            "called ZipFile.__enter__\n"
            f"called ZipFile.write with args ('{dataname}',) {{'arcname': '00000.json'}}\n"
            f"called ZipFile.write with args ('{temp_imagepath / "00002.png"}',)"
            " {'arcname': '00002.png'}\n"
            f"called ZipFile.write with args ('{temp_imagepath / "00003.png"}',)"
            " {'arcname': '00003.png'}\n"
            f"called ZipFile.write with args ('{temp_imagepath / "00006.png"}',)"
            " {'arcname': '00006.png'}\n"
            "called ZipFile.__exit__\n")
    assert testee.write_to_files(filename, opts, views, itemdict, textpositions,
                                 temp_imagepath, save_images=False) == []
    assert capsys.readouterr().out == (
            f"called json.dump with args ({{0: {opts}, 1: {views}, 2: {itemdict},"
            f" 3: {textpositions}}},"
            f" <_io.TextIOWrapper name='{dataname}' mode='w' encoding='UTF-8'>)\n"
            f"called shutil.copyfile with args ('{filename}', '{backupname}')\n"
            f"called zipfile.ZipFile with args ('{filename}', 'w')"
            f" {{'compression': {testee.zpf.ZIP_DEFLATED}}}\n"
            "called ZipFile.__enter__\n"
            f"called ZipFile.write with args ('{dataname}',) {{'arcname': '00000.json'}}\n"
            "called ZipFile.__exit__\n")
