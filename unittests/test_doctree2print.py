"""unittests for ./doctree/doctree2print.py
"""
import types
from doctree import doctree2print as testee


def test_main(monkeypatch, capsys, tmp_path):
    """unittest for doctree2print.main
    """
    def mock_extract(*args):
        print(f"called extract_json_data with args ({args[0]!r}, temp_path)")
    def mock_extract_2(*args):
        print(f"called extract_json_data with args ({args[0]!r}, temp_path)")
        return tmp_path / 'o/data.json'
    orig_open = testee.pathlib.Path.open
    def mock_open(self, *args):
        print('called pathlib.open with args', self, args)
        return orig_open(self, *args)
    def mock_load(fname):
        print(f'called json.load with arg {fname}')
        return []  # 'garbage'  # 0             # geven TypeError
    def mock_load_2(fname):
        print(f'called json.load with arg {fname}')
        return {}           # geeft IndexError
    def mock_load_3(fname):
        print(f'called json.load with arg {fname}')
        return {'0': {'AskBeforeHide': True, 'RootTitle': 'title for root element',
                      'RootData': 'text for root element'}}
    def mock_load_4(fname):
        print(f'called json.load with arg {fname}')
        return {'0': {'AskBeforeHide': True, 'RootTitle': 'title for root element',
                      'RootData': 'text for root element'}, '1': []}
    def mock_load_5(fname):
        print(f'called json.load with arg {fname}')
        return {'0': {'AskBeforeHide': True, 'RootTitle': 'title for root element',
                      'RootData': 'text for root element'}, '1': [], '2': {}}
    def mock_load_6(fname):
        print(f'called json.load with arg {fname}')
        return {'0': {'AskBeforeHide': True, 'RootTitle': 'title for root element',
                      'RootData': 'text for root element'},
                '1': [(1, [])], '2': {1: ("title", "text 1")}, '3': {1: 5}}
    def mock_title(title):
        print(f'called title2filename with arg {title}')
        return title
    def mock_write(*args, **kwargs):
        print('called write_file with args', args, kwargs)
    def mock_filter(*args):
        print('called filter_html with args', args)
        return args[0]
    def mock_print(*args):
        print('called print_plain with args', args)
    monkeypatch.setattr(testee, 'extract_json_data', mock_extract)
    monkeypatch.setattr(testee.pathlib.Path, 'open', mock_open)
    monkeypatch.setattr(testee.json, 'load', mock_load)
    monkeypatch.setattr(testee, 'title2filename', mock_title)
    monkeypatch.setattr(testee, 'write_file', mock_write)
    monkeypatch.setattr(testee, 'filter_html', mock_filter)
    monkeypatch.setattr(testee, 'print_plain', mock_print)
    (tmp_path / 'i').mkdir()   # location of original file
    (tmp_path / 'o').mkdir()   # location of extracted data
    (tmp_path / 'o/data.json').touch()
    assert testee.main('fname') == "no data portion found in file"
    assert capsys.readouterr().out == (
            "donot-filter-html: False\n"
            "to-files: False\n"
            "called extract_json_data with args (PosixPath('fname'), temp_path)\n")
    monkeypatch.setattr(testee, 'extract_json_data', mock_extract_2)
    assert testee.main(str(tmp_path / 'i/fname')) == (
            f"{tmp_path / 'i/fname'} is not a valid Doctree data file")
    assert capsys.readouterr().out == (
            "donot-filter-html: False\n"
            "to-files: False\n"
            f"called extract_json_data with args (PosixPath('{tmp_path}/i/fname'), temp_path)\n"
            f"called pathlib.open with args {tmp_path}/o/data.json ('rb',)\n"
            f"called pathlib.open with args {tmp_path}/i/fname-text-only.out ('w',)\n"
            f"called json.load with arg <_io.BufferedReader name='{tmp_path}/o/data.json'>\n")
    monkeypatch.setattr(testee.json, 'load', mock_load_2)
    assert testee.main(str(tmp_path / 'i/fname')) == (
            f"{tmp_path / 'i/fname'} is not a valid Doctree data file")
    assert capsys.readouterr().out == (
            "donot-filter-html: False\n"
            "to-files: False\n"
            f"called extract_json_data with args (PosixPath('{tmp_path}/i/fname'), temp_path)\n"
            f"called pathlib.open with args {tmp_path}/o/data.json ('rb',)\n"
            f"called pathlib.open with args {tmp_path}/i/fname-text-only.out ('w',)\n"
            f"called json.load with arg <_io.BufferedReader name='{tmp_path}/o/data.json'>\n")
    monkeypatch.setattr(testee.json, 'load', mock_load_4)
    assert testee.main(str(tmp_path / 'i/fname')) == (
            f"{tmp_path / 'i/fname'} is not a valid Doctree data file")
    assert capsys.readouterr().out == (
            "donot-filter-html: False\n"
            "to-files: False\n"
            f"called extract_json_data with args (PosixPath('{tmp_path}/i/fname'), temp_path)\n"
            f"called pathlib.open with args {tmp_path}/o/data.json ('rb',)\n"
            f"called pathlib.open with args {tmp_path}/i/fname-text-only.out ('w',)\n"
            f"called json.load with arg <_io.BufferedReader name='{tmp_path}/o/data.json'>\n")
    monkeypatch.setattr(testee.json, 'load', mock_load_5)
    assert testee.main(str(tmp_path / 'i/fname')) == (
            f"{tmp_path / 'i/fname'} is not a valid Doctree data file")
    assert capsys.readouterr().out == (
            "donot-filter-html: False\n"
            "to-files: False\n"
            f"called extract_json_data with args (PosixPath('{tmp_path}/i/fname'), temp_path)\n"
            f"called pathlib.open with args {tmp_path}/o/data.json ('rb',)\n"
            f"called pathlib.open with args {tmp_path}/i/fname-text-only.out ('w',)\n"
            f"called json.load with arg <_io.BufferedReader name='{tmp_path}/o/data.json'>\n")
    monkeypatch.setattr(testee.json, 'load', mock_load_6)
    assert testee.main(str(tmp_path / 'i/fname')) == 'done.'
    assert capsys.readouterr().out == (
            "donot-filter-html: False\n"
            "to-files: False\n"
            f"called extract_json_data with args (PosixPath('{tmp_path}/i/fname'), temp_path)\n"
            f"called pathlib.open with args {tmp_path}/o/data.json ('rb',)\n"
            f"called pathlib.open with args {tmp_path}/i/fname-text-only.out ('w',)\n"
            f"called json.load with arg <_io.BufferedReader name='{tmp_path}/o/data.json'>\n"
            "called filter_html with args ('text for root element',)\n"
            "called print_plain with args ('options', {'AskBeforeHide': True,"
            " 'RootTitle': 'title for root element', 'RootData': 'text for root element'},"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-text-only.out'"
            " mode='w' encoding='UTF-8'>)\n"
            "called print_plain with args ('views', [(1, [])],"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-text-only.out'"
            " mode='w' encoding='UTF-8'>)\n"
            "called filter_html with args ('text 1',)\n"
            "called print_plain with args ('itemdict', {1: ('title', 'text 1')},"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-text-only.out'"
            " mode='w' encoding='UTF-8'>)\n"
            "called print_plain with args ('text positions', {1: 5},"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-text-only.out'"
            " mode='w' encoding='UTF-8'>)\n")
    assert testee.main(str(tmp_path / 'i/fname'), True) == "done."
    assert capsys.readouterr().out == (
            "donot-filter-html: True\n"
            "to-files: False\n"
            f"called extract_json_data with args (PosixPath('{tmp_path}/i/fname'), temp_path)\n"
            f"called pathlib.open with args {tmp_path}/o/data.json ('rb',)\n"
            f"called pathlib.open with args {tmp_path}/i/fname-as-saved.out ('w',)\n"
            f"called json.load with arg <_io.BufferedReader name='{tmp_path}/o/data.json'>\n"
            "called print_plain with args ('options', {'AskBeforeHide': True,"
            " 'RootTitle': 'title for root element', 'RootData': 'text for root element'},"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-as-saved.out'"
            " mode='w' encoding='UTF-8'>)\n"
            "called print_plain with args ('views', [(1, [])],"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-as-saved.out'"
            " mode='w' encoding='UTF-8'>)\n"
            "called print_plain with args ('itemdict', {1: ('title', 'text 1')},"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-as-saved.out'"
            " mode='w' encoding='UTF-8'>)\n"
            "called print_plain with args ('text positions', {1: 5},"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-as-saved.out'"
            " mode='w' encoding='UTF-8'>)\n")
    assert testee.main(str(tmp_path / 'i/fname'), to_files=True) == "done."
    assert capsys.readouterr().out == (
            "donot-filter-html: False\n"
            "to-files: True\n"
            f"called extract_json_data with args (PosixPath('{tmp_path}/i/fname'), temp_path)\n"
            f"called pathlib.open with args {tmp_path}/o/data.json ('rb',)\n"
            f"called pathlib.open with args {tmp_path}/i/fname-text-only_general.out ('w',)\n"
            f"called json.load with arg <_io.BufferedReader name='{tmp_path}/o/data.json'>\n"
            "called filter_html with args ('text for root element',)\n"
            "called print_plain with args ('options', {'AskBeforeHide': True,"
            " 'RootTitle': 'title for root element', 'RootData': 'text for root element'},"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-text-only_general.out'"
            " mode='w' encoding='UTF-8'>)\n"
            "called print_plain with args ('views', [(1, [])],"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-text-only_general.out'"
            " mode='w' encoding='UTF-8'>)\n"
            "called filter_html with args ('text 1',)\n"
            "called title2filename with arg 001 title\n"
            f"called write_file with args (PosixPath('{tmp_path}/i/fname-text-only.out'),"
            " '001 title', 'text 1', False) {}\n"
            "called print_plain with args ('text positions', {1: 5},"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-text-only_general.out'"
            " mode='w' encoding='UTF-8'>)\n")
    assert testee.main(str(tmp_path / 'i/fname'), donot_filter_html=True, to_files=True) == "done."
    assert capsys.readouterr().out == (
            "donot-filter-html: True\n"
            "to-files: True\n"
            f"called extract_json_data with args (PosixPath('{tmp_path}/i/fname'), temp_path)\n"
            f"called pathlib.open with args {tmp_path}/o/data.json ('rb',)\n"
            f"called pathlib.open with args {tmp_path}/i/fname-as-saved_general.out ('w',)\n"
            f"called json.load with arg <_io.BufferedReader name='{tmp_path}/o/data.json'>\n"
            "called title2filename with arg rootitem title for root element\n"
            f"called write_file with args (PosixPath('{tmp_path}/i/fname-as-saved.out'),"
            " 'rootitem title for root element', 'text for root element', True) {}\n"
            "called print_plain with args ('options', {'AskBeforeHide': True,"
            " 'RootTitle': 'title for root element', 'RootData': 'text for root element'},"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-as-saved_general.out'"
            " mode='w' encoding='UTF-8'>)\n"
            "called print_plain with args ('views', [(1, [])],"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-as-saved_general.out'"
            " mode='w' encoding='UTF-8'>)\n"
            "called title2filename with arg 001 title\n"
            f"called write_file with args (PosixPath('{tmp_path}/i/fname-as-saved.out'),"
            " '001 title', 'text 1', True) {}\n"
            "called print_plain with args ('text positions', {1: 5},"
            f" <_io.TextIOWrapper name='{tmp_path}/i/fname-as-saved_general.out'"
            " mode='w' encoding='UTF-8'>)\n")


def test_title2filename():
    """unittest for doctree2print.title2filename
    """
    assert testee.title2filename('title') == "title"
    assert testee.title2filename('path/to/title') == "path-to-title"


def test_write_file(tmp_path):
    """unittest for doctree2print.write_file
    """
    outfile = tmp_path / 'testfile.trd'
    testee.write_file(outfile, 'note_title', 'note_text', False)
    assert not outfile.exists()
    newfile = tmp_path / 'testfile_note_title.out'
    assert newfile.exists()
    assert newfile.read_text() == 'note_text'
    testee.write_file(outfile, 'note title', 'note_text', False)
    assert not outfile.exists()
    newfile = tmp_path / 'testfile_note-title.out'
    assert newfile.exists()
    assert newfile.read_text() == 'note_text'
    testee.write_file(outfile, 'note_title', 'note_text', True)
    assert not outfile.exists()
    newfile = tmp_path / 'testfile_note_title.html'
    assert newfile.exists()
    assert newfile.read_text() == 'note_text'


def test_filter_html(monkeypatch, capsys):
    """unittest for doctree2print.filter_html
    """
    def mock_get(*args):
        print('called get_text')
        return 'text'
    def mock_bs(*args):
        print('called BeautifoulSoup with args', args)
        return types.SimpleNamespace(html='')
    def mock_bs_2(*args):
        print('called BeautifoulSoup with args', args)
        return types.SimpleNamespace(html=types.SimpleNamespace(
            body=types.SimpleNamespace(get_text=mock_get)))

    monkeypatch.setattr(testee.bs, 'BeautifulSoup', mock_bs)
    assert testee.filter_html('data') == ""
    assert capsys.readouterr().out == "called BeautifoulSoup with args ('data', 'lxml')\n"

    monkeypatch.setattr(testee.bs, 'BeautifulSoup', mock_bs_2)
    assert testee.filter_html('data') == "text"
    assert capsys.readouterr().out == ("called BeautifoulSoup with args ('data', 'lxml')\n"
                                       "called get_text\n")


def test_extract_json_data(monkeypatch, capsys):
    """unittest for doctree2print.extract_json_data
    """
    class MockZipFile:
        """stub for zipfile.Zipfile
        """
        def __init__(self, *args):
            print('called ZipFile.__init__ with args', args)
            self._name = args[0]
        def namelist(self):
            print('called ZipFile.namelist')
            return ['name', 'list']
        def extract(self, *args, **kwargs):
            print('called ZipFile.extract with args', args, kwargs)
        def __enter__(self):
            print('called ZipFile.__enter__')
            return self
        def __exit__(self, *args):
            print('called ZipFile.__exit__')
            return True
    def mock_namelist(self):
        print('called ZipFile.namelist')
        return ['name', 'list.json']
    monkeypatch.setattr(testee.zpf, 'ZipFile', MockZipFile)
    assert not testee.extract_json_data('file.ntr', '/tmp/xxx')
    assert capsys.readouterr().out == (
            "called ZipFile.__init__ with args ('file.ntr',)\n"
            "called ZipFile.__enter__\n"
            "called ZipFile.namelist\n"
            "called ZipFile.__exit__\n")
    monkeypatch.setattr(MockZipFile, 'namelist', mock_namelist)
    outpath = testee.pathlib.Path('/tmp/xxx')
    result = testee.extract_json_data('file.ntr', outpath)
    assert isinstance(result, testee.pathlib.Path)
    assert str(result) == "/tmp/xxx/list.json"
    assert capsys.readouterr().out == (
            "called ZipFile.__init__ with args ('file.ntr',)\n"
            "called ZipFile.__enter__\n"
            "called ZipFile.namelist\n"
            f"called ZipFile.extract with args ('list.json',) {{'path': {outpath!r}}}\n"
            "called ZipFile.__exit__\n")


def test_print_plain(monkeypatch, capsys, tmp_path):
    """unittest for doctree2print.print_plai
    """
    def mock_print(*args, **kwargs):
        print('called pprint.pprint with args', args, kwargs)
    monkeypatch.setattr(testee.pprint, 'pprint', mock_print)
    with (tmp_path / 'testfile').open('w') as out:
        testee.print_plain('title', 'data', out)
    assert (tmp_path / 'testfile').read_text() == '----- title:\n'
    assert capsys.readouterr().out == (
            "called pprint.pprint with args ('data',) {'width': 200,"
            f" 'stream': <_io.TextIOWrapper name='{tmp_path}/testfile'"
            " mode='w' encoding='UTF-8'>}\n")
