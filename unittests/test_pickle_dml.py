import pathlib
import doctree.pickle_dml as testee

testdata = [{'Application': 'DocTree'},
            [[(0, [(1, [])])]],
            {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
            {0: 0, 1: 0}]


def test_write_to_files(tmp_path):
    (tmp_path / 'test_write').mkdir(exist_ok=True)
    testfile = tmp_path / 'test_write' / 'testfile.dtr'
    imgfile = testfile.with_suffix('.zip')
    settings, views, itemdict, textpos = testdata
    testee.write_to_files(testfile, settings, views, itemdict, textpos, imgfile)
    assert testfile.exists()
    # nog vergelijken met van hieruit pickle maken


def test_read_from_files(monkeypatch, capsys, tmp_path):
    class NotASequence:
        pass
    class MockZipFileErr:
        def __init__(self, *args):
            print('called zipfile.ZipFile with args', args)
        def __enter__(self):
            print('called ZipFile.__enter__')
            return self
        def extractall(self, path):
            print(f'called ZipFile.extractall with arg `{path}`')
            raise FileNotFoundError
        def __exit__(self, *args):
            print('called ZipFile.__exit__')
            return False
    class MockZipFileOk:
        def __init__(self, *args):
            print('called zipfile.ZipFile with args', args)
        def __enter__(self):
            print('called ZipFile.__enter__')
            return self
        def extractall(self, path):
            print(f'called ZipFile.extractall with arg `{path}`')
        def __exit__(self, *args):
            print('called ZipFile.__exit__')
            return True
        def namelist(self):
            print('called ZipFile.namelist')
            return ['name', 'list']
    def mock_open_err(*args):
        print('called path.open with args', args)
        raise OSError
    def mock_open_ok(*args):
        print('called path.open with args', args)
        return args[0].open(args[1])
    def mock_load_err(*args):
        print('called pickle.load')
        raise testee.pickle.UnpicklingError
    def mock_load_err_wrong_type(*args):
        return 'not-a-dict'
    def mock_load_err_not_an_iterable(*args):
        return NotASequence()
    def mock_load_err_1st_item(*args):
        return {}
    def mock_load_err_1st_item_2(*args):
        return {0: 'not-a-dict'}
    def mock_load_err_1st_item_3(*args):
        return {0: {}}
    def mock_load_err_1st_item_4(*args):
        return {0: {'Application': 'not DocTree'}}
    def mock_load_err_2nd_item(*args):
        return {0: testdata[0]}
    def mock_load_err_2nd_item_2(*args):
        return {0: testdata[0], 1: {}}
    def mock_load_err_2nd_item_3(*args):
        return {0: testdata[0], 1: NotASequence()}
    def mock_load_err_3rd_item(*args):
        return {0: testdata[0], 1: testdata[1]}
    def mock_load_err_3rd_item_2(*args):
        return {0: testdata[0], 1: testdata[1], 2: {}}
    def mock_load_err_3rd_item_3(*args):
        return {0: testdata[0], 1: testdata[1], 2: NotASequence}
    def mock_load_err_3rd_item_4(*args):
        return {0: testdata[0], 1: testdata[1], 2: 'not-a-dict'}
    def mock_load_err_4th_item(*args):
        return {0: testdata[0], 1: testdata[1], 2: testdata[2]}
    def mock_load_err_4th_item_2(*args):
        return {0: testdata[0], 1: testdata[1], 2: testdata[2], 3: {}}
    def mock_load_err_4th_item_3(*args):
        return {0: testdata[0], 1: testdata[1], 2: testdata[2], 3: 'not-a-dict'}
    def mock_load_ok(*args):
        print('called pickle.load')
        return {0: testdata[0], 1: testdata[1], 2: testdata[2], 3: testdata[3]}
    (tmp_path / 'test_read').mkdir(exist_ok=True)
    testfile = tmp_path / 'test_read' / 'testfile.dtr'
    imagepath = 'temp_path_for_images'  # # testfile.with_suffix('.zip')

    # geen filenaam
    assert testee.read_from_files('', '', imagepath) == ['no file name given']
    # file bestaat niet
    assert testee.read_from_files(testfile, '', imagepath) == [f"couldn't open {testfile}"]
    # fout tijdens lezen leeg file (geeft EOFError?)
    testfile.touch()
    assert testee.read_from_files(testfile, '', imagepath) == [f"couldn't load data from {testfile}"]
    # fout tijdens unpicklen
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err)
    assert testee.read_from_files(testfile, '', imagepath) == [f"couldn't load data from {testfile}"]
    assert capsys.readouterr().out == 'called pickle.load\n'
    # mogelijke fouten in data
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_wrong_type)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile}"
                                                             " is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_not_an_iterable)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile}"
                                                             " is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_1st_item)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile}"
                                                             " is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_1st_item_2)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile}"
                                                             " is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_1st_item_3)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile}"
                                                             " is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_1st_item_4)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile}"
                                                             " is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_2nd_item)
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'}, [[]], {},
                                                             {}, [])
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_2nd_item_2)
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'}, [], {},
                                                             {}, [])
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_2nd_item_3)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile}"
                                                             " contains invalid data for views"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_3rd_item)
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'},
                                                             [[(0, [(1, [])])]], {}, {}, [])
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_3rd_item_2)
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'},
                                                             [[(0, [(1, [])])]], {}, {}, [])
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_3rd_item_3)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile}"
                                                             " contains invalid data for itemdict"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_4th_item)
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'},
                                                             [[(0, [(1, [])])]],
                                                             {0: ('text1', 'this is one text'),
                                                              1: ('text2', 'this is another')},
                                                             {0: 0, 1: 0}, [])
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_4th_item_2)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile} contains"
                                                             " invalid data for text positions"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_4th_item_3)
    assert testee.read_from_files(testfile, '', imagepath) == [f"{testfile} contains"
                                                             " invalid data for text positions"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_ok)
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFileErr)
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'},
                                                             [[(0, [(1, [])])]],
                                                             {0: ('text1', 'this is one text'),
                                                              1: ('text2', 'this is another')},
                                                             {0: 0, 1: 0}, [])
    assert capsys.readouterr().out == ('called pickle.load\n'
            f"called zipfile.ZipFile with args ('{testfile.with_suffix('.zip')}',)\n"
            'called ZipFile.__enter__\n'
            f'called ZipFile.extractall with arg `{imagepath}`\n'
            'called ZipFile.__exit__\n')
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFileOk)
    assert testee.read_from_files(testfile, '', imagepath) == ({'Application': 'DocTree'},
                                                             [[(0, [(1, [])])]],
                                                             {0: ('text1', 'this is one text'),
                                                              1: ('text2', 'this is another')},
                                                             {0: 0, 1: 0}, ['name', 'list'])
    assert capsys.readouterr().out == ('called pickle.load\n'
            f"called zipfile.ZipFile with args ('{testfile.with_suffix('.zip')}',)\n"
            'called ZipFile.__enter__\n'
            f'called ZipFile.extractall with arg `{imagepath}`\n'
            'called ZipFile.__exit__\n'
            'called ZipFile.namelist\n')

    # fout tijdens openen
    monkeypatch.setattr(pathlib.Path, 'open', mock_open_err)
    assert testee.read_from_files(testfile, '', imagepath) == [f"couldn't open {testfile}"]
    assert capsys.readouterr().out == f"called path.open with args ({testfile!r}, 'rb')\n"
