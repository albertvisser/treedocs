"""unittests for ./doctree/pickle_dml.py
"""
import pathlib
import doctree.pickle_dml as testee

testdata = [{'Application': 'DocTree'},
            [[(0, [(1, [])])]],
            {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
            {0: 0, 1: 0}]


class MockZipFileErr:
    """stub
    """
    def __init__(self, *args):
        print('called zipfile.ZipFile with args', args)
    def __enter__(self):
        """stub
        """
        print('called ZipFile.__enter__')
        return self
    def extractall(self, path):
        """stub
        """
        print(f'called ZipFile.extractall with arg `{path}`')
        raise FileNotFoundError
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
    def __exit__(self, *args):
        """stub
        """
        print('called ZipFile.__exit__')
        return True
    def namelist(self):
        """stub
        """
        print('called ZipFile.namelist')
        return ['name', 'list']
    def write(self, *args, **kwargs):
        """stub
        """
        print('called ZipFile.write with args', args, kwargs)


def test_read_from_files(monkeypatch, capsys, tmp_path):
    """unittest for pickle_dml.read_from_files
    """
    class NotASequence:
        """stub
        """
    def mock_open_err(*args):
        """stub
        """
        print('called path.open with args', args)
        raise OSError
    def mock_load_err(*args):
        """stub
        """
        print('called pickle.load')
        raise testee.pickle.UnpicklingError
    def mock_load_err_wrong_type(*args):
        """stub
        """
        return 'not-a-dict'
    def mock_load_err_not_an_iterable(*args):
        """stub
        """
        return NotASequence()
    def mock_load_err_1st_item(*args):
        """stub
        """
        return {}
    def mock_load_err_1st_item_2(*args):
        """stub
        """
        return {0: 'not-a-dict'}
    def mock_load_err_1st_item_3(*args):
        """stub
        """
        return {0: {}}
    def mock_load_err_1st_item_4(*args):
        """stub
        """
        return {0: {'Application': 'not DocTree'}}
    def mock_load_err_2nd_item(*args):
        """stub
        """
        return {0: testdata[0]}
    def mock_load_err_2nd_item_2(*args):
        """stub
        """
        return {0: testdata[0], 1: {}}
    def mock_load_err_2nd_item_3(*args):
        """stub
        """
        return {0: testdata[0], 1: NotASequence()}
    def mock_load_err_3rd_item(*args):
        """stub
        """
        return {0: testdata[0], 1: testdata[1]}
    def mock_load_err_3rd_item_2(*args):
        """stub
        """
        return {0: testdata[0], 1: testdata[1], 2: {}}
    def mock_load_err_3rd_item_3(*args):
        """stub
        """
        return {0: testdata[0], 1: testdata[1], 2: NotASequence()}
    def mock_load_err_3rd_item_4(*args):
        """stub
        """
        return {0: testdata[0], 1: testdata[1], 2: 'not-a-dict'}
    def mock_load_err_4th_item(*args):
        """stub
        """
        return {0: testdata[0], 1: testdata[1], 2: testdata[2]}
    def mock_load_err_4th_item_2(*args):
        """stub
        """
        return {0: testdata[0], 1: testdata[1], 2: testdata[2], 3: {}}
    def mock_load_err_4th_item_3(*args):
        """stub
        """
        return {0: testdata[0], 1: testdata[1], 2: testdata[2], 3: 'not-a-dict'}
    def mock_load_err_4th_item_4(*args):
        """stub
        """
        return {0: testdata[0], 1: testdata[1], 2: testdata[2], 3: NotASequence()}
    def mock_load_ok(*args):
        """stub
        """
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
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_not_an_iterable)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_1st_item)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_1st_item_2)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_1st_item_3)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_1st_item_4)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} is not a valid Doctree data file"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_2nd_item)
    assert testee.read_from_files(testfile, '', imagepath) == (
            {'Application': 'DocTree'}, [[]], {}, {}, [])
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_2nd_item_2)
    assert testee.read_from_files(testfile, '', imagepath) == (
            {'Application': 'DocTree'}, [], {}, {}, [])
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_2nd_item_3)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} contains invalid data for views"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_3rd_item)
    assert testee.read_from_files(testfile, '', imagepath) == (
            {'Application': 'DocTree'}, [[(0, [(1, [])])]], {}, {}, [])
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_3rd_item_2)
    assert testee.read_from_files(testfile, '', imagepath) == (
            {'Application': 'DocTree'}, [[(0, [(1, [])])]], {}, {}, [])
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_3rd_item_3)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} contains invalid data for itemdict"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_3rd_item_4)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} contains invalid data for itemdict"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_4th_item)
    assert testee.read_from_files(testfile, '', imagepath) == (
            {'Application': 'DocTree'}, [[(0, [(1, [])])]],
            {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')}, {0: 0, 1: 0}, [])
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_4th_item_2)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} contains invalid data for text positions"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_4th_item_3)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} contains invalid data for text positions"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_err_4th_item_4)
    assert testee.read_from_files(testfile, '', imagepath) == [
            f"{testfile} contains invalid data for text positions"]
    monkeypatch.setattr(testee.pickle, 'load', mock_load_ok)
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFileErr)
    assert testee.read_from_files(testfile, '', imagepath) == (
            {'Application': 'DocTree'}, [[(0, [(1, [])])]],
            {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')}, {0: 0, 1: 0}, [])
    assert capsys.readouterr().out == (
            'called pickle.load\n'
            f"called zipfile.ZipFile with args ('{testfile.with_suffix('.zip')}',)\n"
            'called ZipFile.__enter__\n'
            f'called ZipFile.extractall with arg `{imagepath}`\n'
            'called ZipFile.__exit__\n')
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFileOk)
    assert testee.read_from_files(testfile, '', imagepath) == (
            {'Application': 'DocTree'}, [[(0, [(1, [])])]],
            {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},
            {0: 0, 1: 0}, ['name', 'list'])
    assert capsys.readouterr().out == (
            'called pickle.load\n'
            f"called zipfile.ZipFile with args ('{testfile.with_suffix('.zip')}',) {{}}\n"
            'called ZipFile.__enter__\n'
            f'called ZipFile.extractall with arg `{imagepath}`\n'
            'called ZipFile.__exit__\n'
            'called ZipFile.namelist\n')

    # fout tijdens openen (aan het eind zodat ik de monkeypatch niet ongedaan hoef te maken)
    monkeypatch.setattr(pathlib.Path, 'open', mock_open_err)
    assert testee.read_from_files(testfile, '', imagepath) == [f"couldn't open {testfile}"]
    assert capsys.readouterr().out == f"called path.open with args ({testfile!r}, 'rb')\n"


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
    assert capsys.readouterr().out == ("called zipfile.ZipFile with args ('testfile.zip',) {}\n"
                                       "called ZipFile.__enter__\n"
                                       "called ZipFile.namelist\n"
                                       "called ZipFile.__exit__\n")
    monkeypatch.setattr(MockZipFileOk, 'namelist', mock_namelist_2)
    assert testee.determine_highest_in_zipfile(filename) == (['00005.png', '00001.png',
                                                              '00003.png'], 5)
    assert capsys.readouterr().out == ("called zipfile.ZipFile with args ('testfile.zip',) {}\n"
                                       "called ZipFile.__enter__\n"
                                       "called ZipFile.namelist\n"
                                       "called ZipFile.__exit__\n")


def test_write_to_files(monkeypatch, capsys, tmp_path):
    """unittest for pickle_dml.write_to_files
    """
    def mock_copy(*args):
        print('called shutil.copyfile with args', args)
        raise FileNotFoundError
    counter = 0
    def mock_copy_2(*args):
        nonlocal counter
        print('called shutil.copyfile with args', args, end="")
        counter += 1
        if counter > 1:
            print()
            raise FileNotFoundError
        print(' -- ok')
    def mock_copy_3(*args):
        print('called shutil.copyfile with args', args, end="")
        print(' -- ok')
    def mock_dump(*args):
        print('called pickle.dump with args', args)
    counter2 = 0
    def mock_exists(*args):
        nonlocal counter2
        print('called path.exists with args', args, end="")
        counter2 += 1
        if counter2 % 2 == 1:
            print(' gives False')
            return False
        print(' gives True')
        return True
    monkeypatch.setattr(testee.pickle, 'dump', mock_dump)
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFileOk)
    (tmp_path / 'test_write').mkdir(exist_ok=True)
    testfile = tmp_path / 'test_write' / 'testfile.dtr'
    bakfile = tmp_path / 'test_write' / 'testfile.dtr.bak'
    imgfile = testfile.with_suffix('.zip')
    imgtmppath = pathlib.Path('/tmp/path/to/images')
    imgbakfile = testfile.with_suffix('.zip.bak')
    settings, views, itemdict, textpos = testdata

    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    assert testee.write_to_files(testfile, settings, views, itemdict, textpos, imgtmppath) == []
    assert capsys.readouterr().out == (
            f"called shutil.copyfile with args ('{testfile}', '{bakfile}')\n"
            "called pickle.dump with args ({0: {'Application': 'DocTree'},"
            " 1: [[(0, [(1, [])])]],"
            " 2: {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},"
            f" 3: {{0: 0, 1: 0}}}}, <_io.BufferedWriter name='{testfile}'>)\n"
            f"called zipfile.ZipFile with args ('{imgfile}', 'w')"
            f" {{'compression': {testee.zpf.ZIP_DEFLATED}}}\n"
            "called ZipFile.__enter__\n"
            "called ZipFile.__exit__\n")

    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy_2)
    monkeypatch.setattr(pathlib.Path, 'exists', mock_exists)
    itemdict = {'text-1': ('title-1', '<html><body><img src="00002.png"/></body></html>'),
                'text-2': ('title-2', '<html><body><img src="00003.png"/></body></html>'),
                'text-3': ('title-3', '<html><body><img src="00006.png"/></body></html>')}
    assert testee.write_to_files(testfile, settings, views, itemdict, textpos,
                                 imgtmppath) == ['00003.png']
    assert capsys.readouterr().out == (
            f"called shutil.copyfile with args ('{testfile}', '{bakfile}') -- ok\n"
            f"called shutil.copyfile with args ('{imgfile}', '{imgbakfile}')\n"
            "called pickle.dump with args ({0: {'Application': 'DocTree'},"
            " 1: [[(0, [(1, [])])]],"
            """ 2: {'text-1': ('title-1', '<html><body><img src="00002.png"/></body></html>'),"""
            """ 'text-2': ('title-2', '<html><body><img src="00003.png"/></body></html>'),"""
            """ 'text-3': ('title-3', '<html><body><img src="00006.png"/></body></html>')},"""
            f" 3: {{0: 0, 1: 0}}}}, <_io.BufferedWriter name='{testfile}'>)\n"
            f"called zipfile.ZipFile with args ('{imgfile}', 'w')"
            f" {{'compression': {testee.zpf.ZIP_DEFLATED}}}\n"
            "called ZipFile.__enter__\n"
            "called path.exists with args (PosixPath(\'/tmp/path/to/images/00002.png\'),)"
            " gives False\n"
            "called path.exists with args (PosixPath(\'/tmp/path/to/images/00003.png\'),)"
            " gives True\n"
            "called ZipFile.write with args ('/tmp/path/to/images/00003.png',)"
            " {'arcname': '00003.png'}\n"
            "called path.exists with args (PosixPath(\'/tmp/path/to/images/00006.png\'),)"
            " gives False\n"
            "called ZipFile.__exit__\n")

    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy_3)
    itemdict = {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')}
    assert testee.write_to_files(testfile, settings, views, itemdict, textpos, imgtmppath,
                                 extra_images=['00001.png', '00002.png']) == ['00001.png']
    assert capsys.readouterr().out == (
            f"called shutil.copyfile with args ('{testfile}', '{bakfile}') -- ok\n"
            f"called shutil.copyfile with args ('{imgfile}', '{imgbakfile}') -- ok\n"
            "called pickle.dump with args ({0: {'Application': 'DocTree'},"
            " 1: [[(0, [(1, [])])]],"
            " 2: {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},"
            f" 3: {{0: 0, 1: 0}}}}, <_io.BufferedWriter name='{testfile}'>)\n"
            f"called zipfile.ZipFile with args ('{imgfile}', 'a')"
            f" {{'compression': {testee.zpf.ZIP_DEFLATED}}}\n"
            "called ZipFile.__enter__\n"
            "called path.exists with args (PosixPath(\'/tmp/path/to/images/00001.png\'),)"
            " gives True\n"
            "called ZipFile.write with args ('/tmp/path/to/images/00001.png',)"
            " {'arcname': '00001.png'}\n"
            "called path.exists with args (PosixPath(\'/tmp/path/to/images/00002.png\'),)"
            " gives False\n"
            "called ZipFile.__exit__\n")

    assert testee.write_to_files(testfile, settings, views, itemdict, textpos, imgtmppath,
                                 backup=False, save_images=False) == []
    assert capsys.readouterr().out == (
            "called pickle.dump with args ({0: {'Application': 'DocTree'},"
            " 1: [[(0, [(1, [])])]],"
            " 2: {0: ('text1', 'this is one text'), 1: ('text2', 'this is another')},"
            f" 3: {{0: 0, 1: 0}}}}, <_io.BufferedWriter name='{testfile}'>)\n")
