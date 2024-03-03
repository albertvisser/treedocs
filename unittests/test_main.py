"""unittests for ./doctree/main.py
"""
import datetime
from doctree import main as testee


def mock_ask_yn(*args):
    """stub for doctree.gui.ask_ynquestion: No answer
    """
    print('called gui.ask_ynquestion with args', args)
    return False


def mock_ask_yn_2(*args):
    """stub for doctree.gui.ask_ynquestion: Yes answer
    """
    print('called gui.ask_ynquestion with args', args)
    return True


def mock_ask_ync(*args):
    """stub for doctree.gui.ask_yncquestion: No answer
    """
    print('called gui.ask_yncquestion with args', args)
    return False, False


def mock_ask_ync_2(*args):
    """stub for doctree.gui.ask_yncquestion: Yes answer
    """
    print('called gui.ask_yncquestion with args', args)
    return True, False


def mock_ask_ync_3(*args):
    """stub for doctree.gui.ask_yncquestion: Cancel
    """
    print('called gui.ask_yncquestion with args', args)
    return False, True


def mock_get_filename(*args, **kwargs):
    """stub for Doctree.gui.get_filename: dialog was canceled
    """
    print('called gui.get_filename with args', args, kwargs)
    return False, ''


def mock_get_filename_2(*args, **kwargs):
    """stub for Doctree.gui.get_filename: dialog was accepted
    """
    print('called gui.get_filename with args', args, kwargs)
    return True, 'newname.trd'


def mock_get_text(*args, **kwargs):
    """stub for Doctree.gui.get_text: dialog was canceled
    """
    print('called gui.get_text with args', args, kwargs)
    return False, ''


def mock_get_text_2(*args, **kwargs):
    """stub for Doctree.gui.get_text: dialog was accepted
    """
    print('called gui.get_text with args', args, kwargs)
    return True, 'new text'


def mock_get_text_3(*args, **kwargs):
    """stub for Doctree.gui.get_text: dialog was accepted, input cas cleared
    """
    print('called gui.get_text with args', args, kwargs)
    return True, ''


def mock_get_choice(*args, **kwargs):
    """stub for Doctree.gui.get_choice: dialog was canceled
    """
    print('called gui.get_choice with args', args, kwargs)
    return False, ''


def mock_get_choice_2(*args, **kwargs):
    """stub for Doctree.gui.get_choice: dialog was accepted
    """
    print('called gui.get_choice with args', args, kwargs)
    return True, 'selection'


def mock_show_message(*args):
    """stub for doctree.gui.show_message
    """
    print('called gui.show_message with args', args)


def mock_show_nonmodal(*args):
    """stub for doctree.gui.show_nonmodal
    """
    print('called gui.show_nonmodal with args', args)


def mock_show_dialog(*args):
    """stub for doctree.gui.show_dialogi: dialog canceled
    """
    print('called gui.show_dialog with args', args)
    return False


def mock_show_dialog_2(*args):
    """stub for doctree.gui.show_dialog: dialog confirmed
    """
    print('called gui.show_dialog with args', args)
    return True


def mock_init_opts():
    """stub for main.init_opts
    """
    print('called init_opts')
    return {'ScreenSize': (200, 100), 'RootData': 'root data'}


class MockDateTime:
    def today():
        return datetime.datetime(2000, 1, 1)


class MockTree:
    """stub for doctree.gui.TreePanel
    """
    def getitemtitle(self, arg):
        print(f'called Tree.getitemtitle with arg `{arg}`')
        return 'item title'
    def setitemtitle(self, *args):
        print(f'called Tree.setitemtitle with args', args)
    def getitemkey(self, arg):
        print(f'called Tree.getitemkey with arg `{arg}`')
        return arg
    def getitemdata(self, arg):
        print(f'called Tree.getitemdata with arg `{arg}`')
        return 'item data'
    def getitemkids(self, arg):
        print(f'called Tree.getitemkids with arg `{arg}`')
        return ['child1', 'child2']
    def getselecteditem(self):
        print(f'called Tree.getselecteditem')
        return 'selected_item'
    def get_selected_item(self):
        print(f'called Tree.get_selected_item')
        return ['selected_item']
    def set_item_selected(self, arg):
        print(f'called Tree.set_item_selected with arg `{arg}`')
    def set_item_expanded(self, *args):
        print('called Tree.set_item_expanded with args', args)
    def set_item_collapsed(self, *args):
        print('called Tree.set_item_collapsed with args', args)


class MockEditor:
    """stub for doctree.gui.EditorPanel
    """
    def undo(self):
        print('called Editor.undo')
    def redo(self):
        print('called Editor.redo')
    def cut(self):
        print('called Editor.cut')
    def copy(self):
        print('called Editor.copy')
    def paste(self):
        print('called Editor.paste')
    def select_all (self):
        print('called Editor.select_all')
    def clear(self):
        print('called Editor.clear')
    def text_bold(self):
        print('called Editor.text_bold')
    def text_italic(self):
        print('called Editor.text.italic')
    def text_underline(self):
        print('called Editor.text_underline')
    def text_strikethrough(self):
        print('called Editor.text_strikethrough')
    def align_left(self):
        print('called Editor.align_left')
    def align_center(self):
        print('called Editor.align_center')
    def align_right(self):
        print('called Editor.align_right')
    def text_font(self):
        print('called Editor.text_font')
    def enlarge_text(self):
        print('called Editor.enlarge_text')
    def shrink_text(self):
        print('called Editor.shrink_text')
    def text_color(self):
        print('called Editor.text_color')
    def background_color(self):
        print('called Editor.backgound_color')
    def set_contents(self, arg):
        print(f"called Editor.set_contents with arg `{arg}'")
    def openup(self, value):
        print(f"called Editor.openup with arg '{value}'")
    def get_text_position(self):
        print('called Editor.get_text_position')
        return 9
    def search_from_start(self):
        print('called Editor.search_from_start')
        return False
    def find_next(self):
        print('called Editor.find_next')
    def find_prev(self):
        print('called Editor.find_prev')
    def check_dirty(self):
        print('called Editor.check_dirty')
        return False


class MockGui:
    """stub for doctree.gui.MainGui
    """
    def __init__(self, *args, **kwargs):
        print("called MainGui.__init__ with args", args, kwargs)
        self.tree = MockTree()
        self.editor = MockEditor()
    def setup_screen(self):
        print("called MainGui.setup_screen")
    def go(self):
        print("called MainGui.go")
    def set_windowtitle(self, *args):
        print('called MainGui.set_windowtitle with args', args)
    def set_version(self, *args):
        print('called MainGui.set_version with args', args)
    def set_window_dimensions(self, *args):
        print('called MainGui.set_window_dimensions with args', args)
    def disable_menu(self, value=True):
        extra = '' if value else f' with arg {value}'
        print("called MainGui.disable_menu" + extra)
    def init_app(self):
        print("called MainGui.init_app")
    def rebuild_root(self):
        print("called MainGui.rebuild_root")
    def reorder_items(self, *args, **kwargs):
        print("called MainGui.reorder_items with args", args, kwargs)
    def set_focus_to_tree(self):
        print("called MainGui.set_focus_to_tree")
    def tree_undo(self):
        print('called mainGui.tree_undo')
    def tree_redo(self):
        print('called MainGui.tree_redo')
    def close(self):
        print('called MainGui.close')
    def show_statusmessage(self, *args):
        print('called MainGui.show_statusmessage with args', args)
    def set_next_item(self, *args, **kwargs):
        print('called MainGui.set_next_item with args', args, kwargs)
    def set_prev_item(self, *args, **kwargs):
        print('called MainGui.set_prev_item with args', args, kwargs)
    def hide_me(self):
        print('called MainGui.hide_me')
    def set_focus_to_tree(self):
        print('called MainGui.set_focus_to_tree')
    def set_focus_to_editor(self):
        print('called MainGui.set_focus_to_editor')
    def clear_viewmenu(self):
        print("called MainGui.clear_viewmenu")
    def add_viewmenu_option(self, arg):
        print(f"called MainGui.add_viewmenu_option with arg '{arg}'")
        return 'An action'
    def rename_viewmenu_option(self, arg):
        print(f"called MainGui.rename_viewmenu_option with arg '{arg}'")
    def remove_viewmenu_option(self, arg):
        print(f"called MainGui.remove_viewmenu_option with arg '{arg}'")
        return 'An action'
    def uncheck_viewmenu_option(self):
        print("called MainGui.uncheck_viewmenu_option")
    def check_viewmenu_option(self, *args):
        if not args:
            print(f"called MainGui.check_viewmenu_option")
            return "A New view"
        else:
            print(f"called MainGui.check_viewmenu_option with arg '{args[0]}'")
    def check_next_viewmenu_option(self, **kwargs):
        if not kwargs:
            print(f"called MainGui.next_check_viewmenu_option")
        else:
            print(f"called MainGui.check_next_viewmenu_option with args", kwargs)
    def add_escape_action(self):
        print("called MainGui.add_escape_action")
    def remove_escape_action(self):
        print("called MainGui.remove_escape_action")


class MockMainWindow:
    """stub for doctree.main.MainWindow

    to be used for monkeypatching separate methods, not the class itself
    """
    def set_title(self):
        """stub for mainWindow.set_window_title
        """
        print('called MainWindow.set_window_title')

    def set_dirty(self, value):
        """stub for MainWindow.set_project_dirty
        """
        print(f'called MainWindow.set_project_dirty with arg {value}')

    def new(self, *args, **kwargs):
        """stub for MainWindow.new
        """
        print("called MainWindow.new with args", args, kwargs)

    def read(self):
        """stub for MainWindow.read
        """
        print("called MainWindow.read")

    def save(self):
        """stub for MainWindow.save
        """
        print("called MainWindow.save")

    def read_error(self):
        """stub for MainWindow.read - error on open or read
        """
        print("called MainWindow.read")
        return ('error',)

    def write(self, *args, **kwargs):
        """stub for MainWindow.write
        """
        print('called MainWindow.write with args', args, kwargs)

    def handle(self):
        """stub for MainWindow.handle_save_needed: break off current action
        """
        print("called MainWindow.handle_save_needed")
        return False

    def handle_2(self):
        """stub for MainWindow.handle_save_needed: carry on with current action
        """
        print("called MainWindow.handle_save_needed")
        return True

    def new_item(self, *args, **kwargs):
        """stub for MainWindow.new_item
        """
        print("called MainWindow.new_item with args", args, kwargs)

    def get_copy_item(self, *args, **kwargs):
        """stub for MainWindow.get_copy_item
        """
        print("called MainWindow.get_copy_item with args", args, kwargs)

    def put_paste_item(self, *args, **kwargs):
        """stub for MainWindow.put_paste_item
        """
        print("called MainWindow.put_paste_item with args", args, kwargs)

    def check(self):
        """stub for MainWindow.check_active
        """
        print("called MainWindow.check_active")

    def ask_title(self, *args):
        """stub for MainWindow.ask_title: canceled
        """
        print('called MainWindow.ask_title with args', args)
        return ()

    def ask_title_2(self, *args):
        """stub for MainWindow.ask_title: not canceled
        """
        print('called MainWindow.ask_title with args', args)
        return ('xx', ['yyy', 'zzz'])

    def reorder(self, *args, **kwargs):
        """stub for MainWindow.reorder
        """
        print('called MainWindow.reorder with args', args, kwargs)

    def confirm(self, *args, **kwargs):
        """stub for MainWindow.confirm
        """
        print('called MainWindow.confirm with args', args, kwargs)

    def set_escape_action(self):
        """stub for MainWindow.set_escape_action
        """
        print('called MainWindow.set_escape_action')

    def treetoview(self):
        """stub for MainWindow.treetoview
        """
        print("called MainWindow.treetoview")
        return 'A view'

    def viewtotree(self):
        """stub for MainWindow.viewtotree
        """
        print("called MainWindow.viewtotree")
        return 'An item'

    def goto_view(self, *args, **kwargs):
        """stub for MainWindow.goto_view
        """
        print("called MainWindow.goto_view with args", args, kwargs)

    def search_from(self, *args):
        """stub for MainWindow.search_from: canceled
        """
        print('called MainWindow.search_from with args', args)
        return []

    def search_from_2(self, *args):
        """stub for MainWindow.search_from: found stuff
        """
        print('called MainWindow.search_from with args', args)
        self.gui.srchlist = False
        return ['result', 'list']

    def search_from_3(self, *args):
        """stub for MainWindow.search_from: found stuff
        """
        print('called MainWindow.search_from with args', args)
        self.gui.srchlist = True
        return ['result', 'list']

    def go_to_result(self):
        """stub for MainWindow.go_to_result
        """
        print('called MainWindow.go_to_result')

    def search(self, **kwargs):
        """stub for MainWindow.search
        """
        print('called MainWindow.search with args', kwargs)


def test_init_opts(monkeypatch, capsys):
    """unittest for main.init_opts
    """
    assert testee.init_opts() == {
            "Application": "DocTree", "NotifyOnSave": True, 'NotifyOnLoad': True,
            "AskBeforeHide": True, "EscapeClosesApp": True, "SashPosition": 180,
            "ScreenSize": (800, 500), "ActiveItem": [0], "ActiveView": 0, "ViewNames": ["Default"],
            "RootTitle": "MyNotes", "RootData": "", "ImageCount": 0}


def test_add_newitems(monkeypatch, capsys):
    """unittest for main.add_newitems
    """
    def mock_replace(*args):
        print('called main.replace_keys with args', args)
        return 'copied-item-after-replace'
    copied_item = 'copied-item'
    cut_from_itemdict = [(2, ('2', 'xx')), (3, ('3', 'xxx'))]
    itemdict = {1: ('1', 'x'), 2: ('2', 'xx'), 4: ('4', 'xxxx')}
    monkeypatch.setattr(testee, 'replace_keys', mock_replace)
    assert testee.add_newitems(copied_item, cut_from_itemdict, itemdict) == (
            'copied-item-after-replace',
            {1: ('1', 'x'), 2: ('2', 'xx'), 4: ('4', 'xxxx'), 5: ('2', 'xx'), 6: ('3', 'xxx')},
            [5, 6])
    assert capsys.readouterr().out == (
            "called main.replace_keys with args ('copied-item', {2: 5, 3: 6})\n")
    itemdict = {}
    assert testee.add_newitems(copied_item, cut_from_itemdict, itemdict) == (
            'copied-item-after-replace', {0: ('2', 'xx'), 1: ('3', 'xxx')}, [0, 1])
    assert capsys.readouterr().out == (
            "called main.replace_keys with args ('copied-item', {2: 0, 3: 1})\n")


def test_replace_keys(monkeypatch, capsys):
    """unittest for main.replace_keys
    """
    assert testee.replace_keys((1, 1, [(2, 2, []), (3, 3, [])]), {1: 6, 2: 4, 3: 5}) == (
            (1, 6, [(2, 4, []), (3, 5, [])]))


def test_add_item_to_view(monkeypatch, capsys):
    """unittest for main.add_item_to_view
    """
    view = []
    testee.add_item_to_view((1, 1, [(2, 2, [(4, 4, [])]), (3, 3, [])]), view)
    assert view == [(1, [(2, [(4, [])]), (3, [])])]


def test_reset_toolkit_file_if_needed(monkeypatch, capsys, tmp_path):
    """unittest for main.reset_toolkit_file_if_needed
    """
    path = tmp_path / 'doctree'
    def mock_resolve(*args):
        print('called path.resolve with args', args)
        return path
    monkeypatch.setattr(testee.pathlib.Path, 'resolve', mock_resolve)
    path.mkdir()
    testee.reset_toolkit_file_if_needed()
    assert not (path / 'toolkit.py').exists()
    (path / 'toolkit-orig').touch()
    testee.reset_toolkit_file_if_needed()
    assert (path / 'toolkit.py').exists()

class TestMainWindow:
    """unittest for main.MainWindow
    """
    mocker = MockMainWindow()
    mocker.gui = MockGui()

    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.MainWindow object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MainWindow.__init__ with args', args)
        monkeypatch.setattr(testee.MainWindow, '__init__', mock_init)
        testobj = testee.MainWindow()
        testobj.gui = MockGui()
        assert capsys.readouterr().out == ("called MainWindow.__init__ with args ()\n"
                                           "called MainGui.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for MainWindow.__init__
        """
        def mock_reset():
            print('called reset_toolkit_file_if_needed')
        def mock_resolve(arg):
            print('called path.resolve with arg', arg)
            return testee.pathlib.Path('resolved')
        def mock_exists(arg):
            print('called path.exists with arg', arg)
            return False
        def mock_exists_2(arg):
            print('called path.exists with arg', arg)
            return True
        def mock_read_err(arr):
            print("called MainWindow.read")
            return 'error'
        monkeypatch.setattr(testee, 'reset_toolkit_file_if_needed', mock_reset)
        monkeypatch.setattr(testee.gui, 'MainGui', MockGui)
        monkeypatch.setattr(testee.gui, 'ask_ynquestion', mock_ask_yn)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        monkeypatch.setattr(testee.pathlib.Path, 'resolve', mock_resolve)
        monkeypatch.setattr(testee.pathlib.Path, 'exists', mock_exists)
        monkeypatch.setattr(testee.MainWindow, 'new', self.mocker.new)
        monkeypatch.setattr(testee.MainWindow, 'set_project_dirty', self.mocker.set_dirty)
        monkeypatch.setattr(testee.MainWindow, 'read', self.mocker.read)
        testee.gui.toolkit = 'qt'
        testobj = testee.MainWindow()
        assert not testobj.project_dirty
        assert not testobj.add_node_on_paste
        assert not testobj.has_treedata
        assert testobj.imagelist == []
        assert hasattr(testobj, 'temp_imagepath') and isinstance(testobj.temp_imagepath,
                                                                 testee.pathlib.Path)
        assert testobj.copied_item == ()
        assert testobj.cut_from_itemdict == []
        assert not testobj.images_embedded
        assert capsys.readouterr().out == (
                f"called MainGui.__init__ with args ({testobj},) {{'title': 'Doctree'}}\n"
                "called MainGui.setup_screen\n"
                "called MainWindow.new with args () {'ask_ok': False}\n"
                "called reset_toolkit_file_if_needed\n"
                "called MainGui.go\n")

        testee.gui.toolkit = 'wx'
        testobj = testee.MainWindow('test.trd')
        assert not testobj.project_dirty
        assert not testobj.add_node_on_paste
        assert not testobj.has_treedata
        assert testobj.imagelist == []
        assert hasattr(testobj, 'temp_imagepath') and isinstance(testobj.temp_imagepath,
                                                                 testee.pathlib.Path)
        assert testobj.copied_item == ()
        assert testobj.cut_from_itemdict == []
        assert testobj.images_embedded
        assert capsys.readouterr().out == (
                f"called MainGui.__init__ with args ({testobj},) {{'title': 'Doctree'}}\n"
                "called MainGui.setup_screen\n"
                "called path.resolve with arg test.trd\n"
                "called path.exists with arg resolved\n"
                "called gui.ask_ynquestion with args"
                f" ({testobj.gui}, 'test.trd does not exist, do you want to create it?')\n"
                "called MainGui.disable_menu\n"
                "called reset_toolkit_file_if_needed\n"
                "called MainGui.go\n")

        testee.gui.toolkit = 'qt'
        monkeypatch.setattr(testee.gui, 'ask_ynquestion', mock_ask_yn_2)
        testobj = testee.MainWindow('test.trd')
        assert not testobj.project_dirty
        assert not testobj.add_node_on_paste
        assert not testobj.has_treedata
        assert testobj.imagelist == []
        assert hasattr(testobj, 'temp_imagepath') and isinstance(testobj.temp_imagepath,
                                                                 testee.pathlib.Path)
        assert testobj.copied_item == ()
        assert testobj.cut_from_itemdict == []
        assert not testobj.images_embedded
        assert capsys.readouterr().out == (
                f"called MainGui.__init__ with args ({testobj},) {{'title': 'Doctree'}}\n"
                "called MainGui.setup_screen\n"
                "called path.resolve with arg test.trd\n"
                "called path.exists with arg resolved\n"
                "called gui.ask_ynquestion with args"
                f" ({testobj.gui}, 'test.trd does not exist, do you want to create it?')\n"
                "called MainWindow.new with args () {'filename': 'test.trd', 'ask_ok': False}\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called reset_toolkit_file_if_needed\n"
                "called MainGui.go\n")

        monkeypatch.setattr(testee.pathlib.Path, 'exists', mock_exists_2)
        testobj = testee.MainWindow('test.trd')
        assert not testobj.project_dirty
        assert not testobj.add_node_on_paste
        assert not testobj.has_treedata
        assert testobj.imagelist == []
        assert hasattr(testobj, 'temp_imagepath') and isinstance(testobj.temp_imagepath,
                                                                 testee.pathlib.Path)
        assert testobj.copied_item == ()
        assert testobj.cut_from_itemdict == []
        assert not testobj.images_embedded
        assert capsys.readouterr().out == (
                f"called MainGui.__init__ with args ({testobj},) {{'title': 'Doctree'}}\n"
                "called MainGui.setup_screen\n"
                "called path.resolve with arg test.trd\n"
                "called path.exists with arg resolved\n"
                "called MainWindow.read\n"
                "called reset_toolkit_file_if_needed\n"
                "called MainGui.go\n")

        monkeypatch.setattr(testee.pathlib.Path, 'exists', mock_exists_2)
        monkeypatch.setattr(testee.MainWindow, 'read', mock_read_err)
        testobj = testee.MainWindow('test.trd')
        assert not testobj.project_dirty
        assert not testobj.add_node_on_paste
        assert not testobj.has_treedata
        assert testobj.imagelist == []
        assert hasattr(testobj, 'temp_imagepath') and isinstance(testobj.temp_imagepath,
                                                                 testee.pathlib.Path)
        assert testobj.copied_item == ()
        assert testobj.cut_from_itemdict == []
        assert not testobj.images_embedded
        assert capsys.readouterr().out == (
                f"called MainGui.__init__ with args ({testobj},) {{'title': 'Doctree'}}\n"
                "called MainGui.setup_screen\n"
                "called path.resolve with arg test.trd\n"
                "called path.exists with arg resolved\n"
                "called MainWindow.read\n"
                f"called gui.show_message with args ({testobj.gui}, 'error')\n"
                "called reset_toolkit_file_if_needed\n"
                "called MainGui.go\n")

    def test_get_menu_data(self, monkeypatch, capsys):
        """unittest for MainWindow.get_menu_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        menudata = testobj.get_menu_data()
        assert len(menudata) == 8
        for name, items in menudata:
            for item in items:
                assert len(item) in (0, 5)

    def test_set_window_title(self, monkeypatch, capsys):
        """unittest for MainWindow.set_window_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {'ViewNames': ['xxx', 'yyy'], 'ActiveView': 1}
        testobj.project_file = testee.pathlib.Path('test.trd')
        testobj.gui.in_editor = False
        testobj.project_dirty = False
        testobj.set_window_title()
        assert capsys.readouterr().out == (
                "called MainGui.set_windowtitle with args ('test.trd (view: yyy) - Doctree',)\n")

        testobj.project_dirty = True
        testobj.set_window_title()
        assert capsys.readouterr().out == (
                "called MainGui.set_windowtitle with args ('test.trd* (view: yyy) - Doctree',)\n")

        testobj.gui.in_editor = True
        testobj.activeitem = None
        testobj.project_dirty = False
        testobj.set_window_title()
        assert capsys.readouterr().out == ""

        testobj.activeitem = 'active-item'
        testobj.set_window_title()
        assert capsys.readouterr().out == (
                "called Tree.getitemtitle with arg `active-item`\n"
                "called MainGui.set_windowtitle with args"
                " ('test.trd (title: item title) - Doctree',)\n")

        testobj.project_dirty = True
        testobj.set_window_title()
        assert capsys.readouterr().out == (
                "called Tree.getitemtitle with arg `active-item`\n"
                "called MainGui.set_windowtitle with args"
                " ('test.trd* (title: item title) - Doctree',)\n")

    def test_new(self, monkeypatch, capsys):
        """unittest for MainWindow.new
        """
        monkeypatch.setattr(testee.gui, 'ask_ynquestion', mock_ask_yn)
        monkeypatch.setattr(testee, 'init_opts', mock_init_opts)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_window_title = self.mocker.set_title
        testobj.set_project_dirty = self.mocker.set_dirty
        testobj.gui.menu_disabled = False
        testobj.new(filename='test.trd')
        assert capsys.readouterr().out == (
                f"called gui.ask_ynquestion with args ({testobj.gui}, 'Ok to initialize data?')\n")

        monkeypatch.setattr(testee.gui, 'ask_ynquestion', mock_ask_yn_2)
        testobj.new(filename='test.trd')
        assert testobj.project_file == testee.pathlib.Path('test.trd')
        assert testobj.views == [[]]
        assert testobj.viewcount == 1
        assert testobj.itemdict == {}
        assert testobj.text_positions == {}
        assert testobj.imagelist == []
        assert testobj.has_treedata
        assert capsys.readouterr().out == (
                f"called gui.ask_ynquestion with args ({testobj.gui}, 'Ok to initialize data?')\n"
                "called init_opts\n"
                "called MainWindow.set_window_title\n"
                "called MainWindow.set_project_dirty with arg False\n"
                "called MainGui.set_version with args ()\n"
                "called MainGui.set_window_dimensions with args (200, 100)\n"
                "called MainGui.clear_viewmenu\n"
                "called MainGui.add_viewmenu_option with arg '&1 Default'\n"
                "called MainGui.init_app\n"
                "called MainGui.rebuild_root\n"
                "called Editor.set_contents with arg `root data'\n"
                "called Editor.openup with arg 'False'\n"
                "called MainGui.set_focus_to_tree\n")

        testobj.gui.menu_disabled = True
        testobj.new(filename='test.trd', ask_ok=False)
        assert testobj.project_file == testee.pathlib.Path('test.trd')
        assert testobj.views == [[]]
        assert testobj.viewcount == 1
        assert testobj.itemdict == {}
        assert testobj.text_positions == {}
        assert testobj.imagelist == []
        assert testobj.has_treedata
        assert capsys.readouterr().out == (
                "called init_opts\n"
                "called MainWindow.set_window_title\n"
                "called MainWindow.set_project_dirty with arg False\n"
                "called MainGui.set_version with args ()\n"
                "called MainGui.set_window_dimensions with args (200, 100)\n"
                "called MainGui.disable_menu with arg False\n"
                "called MainGui.clear_viewmenu\n"
                "called MainGui.add_viewmenu_option with arg '&1 Default'\n"
                "called MainGui.init_app\n"
                "called MainGui.rebuild_root\n"
                "called Editor.set_contents with arg `root data'\n"
                "called Editor.openup with arg 'False'\n"
                "called MainGui.set_focus_to_tree\n")

    def test_open(self, monkeypatch, capsys):
        """unittest for MainWindow.open
        """
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        monkeypatch.setattr(testee.gui, 'get_filename', mock_get_filename)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = testee.pathlib.Path('test.trd')
        testobj.handle_save_needed = self.mocker.handle
        testobj.read = self.mocker.read
        testobj.gui.menu_disabled = False
        testobj.open()
        assert testobj.project_file == testee.pathlib.Path('test.trd')
        assert capsys.readouterr().out == "called MainWindow.handle_save_needed\n"

        testobj.handle_save_needed = self.mocker.handle_2
        testobj.open()
        assert testobj.project_file == testee.pathlib.Path('test.trd')
        assert capsys.readouterr().out == (
                "called MainWindow.handle_save_needed\n"
                "called gui.get_filename with args"
                f" ({testobj.gui}, 'DocTree - choose file to open', 'test.trd') {{}}\n")

        monkeypatch.setattr(testee.gui, 'get_filename', mock_get_filename_2)
        testobj.open()
        assert testobj.project_file == testee.pathlib.Path('newname.trd')
        assert capsys.readouterr().out == (
                "called MainWindow.handle_save_needed\n"
                "called gui.get_filename with args"
                f" ({testobj.gui}, 'DocTree - choose file to open', 'test.trd') {{}}\n"
                "called MainWindow.read\n"
                "called MainGui.show_statusmessage with args ('newname.trd gelezen',)\n")

        testobj.project_file = testee.pathlib.Path('test.trd')
        testobj.gui.menu_disabled = True
        testobj.open()
        assert testobj.project_file == testee.pathlib.Path('newname.trd')
        assert capsys.readouterr().out == (
                "called MainWindow.handle_save_needed\n"
                "called gui.get_filename with args"
                f" ({testobj.gui}, 'DocTree - choose file to open', 'test.trd') {{}}\n"
                "called MainWindow.read\n"
                "called MainGui.show_statusmessage with args ('newname.trd gelezen',)\n"
                "called MainGui.disable_menu with arg False\n")

        testobj.project_file = testee.pathlib.Path('test.trd')
        testobj.read = self.mocker.read_error
        testobj.open()
        assert testobj.project_file == testee.pathlib.Path('newname.trd')
        assert capsys.readouterr().out == (
                "called MainWindow.handle_save_needed\n"
                "called gui.get_filename with args"
                f" ({testobj.gui}, 'DocTree - choose file to open', 'test.trd') {{}}\n"
                "called MainWindow.read\n"
                f"called gui.show_message with args ({testobj.gui}, 'error')\n")

    def test_reread(self, monkeypatch, capsys):
        """unittest for MainWindow.reread
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = 'test.trd'
        testobj.handle_save_needed = self.mocker.handle
        testobj.read = self.mocker.read
        testobj.reread()
        assert capsys.readouterr().out == "called MainWindow.handle_save_needed\n"
        testobj.handle_save_needed = self.mocker.handle_2
        testobj.reread()
        assert capsys.readouterr().out == (
                "called MainWindow.handle_save_needed\n"
                "called MainWindow.read\n"
                "called MainGui.show_statusmessage with args ('test.trd herlezen',)\n")

    def test_save(self, monkeypatch, capsys):
        """unittest for MainWindow.save
        """
        def mock_saveas():
            print('called MainWindow.saveas')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.write = self.mocker.write
        testobj.saveas = mock_saveas
        testobj.project_file = None
        testobj.save()
        assert capsys.readouterr().out == "called MainWindow.saveas\n"
        testobj.project_file = testee.pathlib.Path('')
        testobj.save()
        assert capsys.readouterr().out == "called MainWindow.saveas\n"
        testobj.project_file = testee.pathlib.Path('test.trd')
        testobj.save()
        assert capsys.readouterr().out == "called MainWindow.write with args () {'meld': True}\n"

    def test_saveas(self, monkeypatch, capsys):
        """unittest for MainWindow.saveas
        """
        monkeypatch.setattr(testee.gui, 'get_filename', mock_get_filename)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = testee.pathlib.Path('test.trd')
        testobj.write = self.mocker.write
        testobj.set_window_title = self.mocker.set_title
        testobj.saveas()
        assert testobj.project_file == testee.pathlib.Path('test.trd')
        assert capsys.readouterr().out == (
                "called gui.get_filename with args"
                f" ({testobj.gui}, 'DocTree - save file as:', 'test.trd') {{'save': True}}\n")

        monkeypatch.setattr(testee.gui, 'get_filename', mock_get_filename_2)
        testobj.saveas()
        assert testobj.project_file == testee.pathlib.Path('newname.trd')
        assert capsys.readouterr().out == (
                "called gui.get_filename with args"
                f" ({testobj.gui}, 'DocTree - save file as:', 'test.trd') {{'save': True}}\n"
                "called MainWindow.write with args () {'meld': True}\n"
                "called MainWindow.set_window_title\n")

        testobj.project_file = testee.pathlib.Path('test.trd')
        monkeypatch.setattr(testee.shared, 'FILE_TYPE', ('x', '.txt'))
        testobj.saveas()
        assert testobj.project_file == testee.pathlib.Path('newname.txt')
        assert capsys.readouterr().out == (
                "called gui.get_filename with args"
                f" ({testobj.gui}, 'DocTree - save file as:', 'test.trd') {{'save': True}}\n"
                "called MainWindow.write with args () {'meld': True}\n"
                "called MainWindow.set_window_title\n")

    def test_rename_root(self, monkeypatch, capsys):
        """unittest for MainWindow.rename_root
        """
        monkeypatch.setattr(testee.gui, 'get_text', mock_get_text)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {'RootTitle': 'root title'}
        testobj.set_project_dirty = self.mocker.set_dirty
        testobj.gui.root = 'gui root'
        testobj.rename_root()
        assert testobj.opts == {'RootTitle': 'root title'}
        assert capsys.readouterr().out == (
                "called gui.get_text with args"
                f" ({testobj.gui}, 'Geef nieuwe titel voor het root item:', 'root title') {{}}\n")

        monkeypatch.setattr(testee.gui, 'get_text', mock_get_text_2)
        testobj.rename_root()
        assert testobj.opts == {'RootTitle': 'new text'}
        assert capsys.readouterr().out == (
                "called gui.get_text with args"
                f" ({testobj.gui}, 'Geef nieuwe titel voor het root item:', 'root title') {{}}\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called Tree.setitemtitle with args ('gui root', 'new text')\n")

    def test_add_item(self, monkeypatch, capsys):
        """unittest for MainWindow.add_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.new_item = self.mocker.new_item
        testobj.add_item()
        assert capsys.readouterr().out == "called MainWindow.new_item with args () {}\n"

    def test_root_item(self, monkeypatch, capsys):
        """unittest for MainWindow.root_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.new_item = self.mocker.new_item
        testobj.gui.root = 'gui root'
        testobj.root_item()
        assert capsys.readouterr().out == (
                "called MainWindow.new_item with args () {'root': 'gui root'}\n")

    def test_insert_item(self, monkeypatch, capsys):
        """unittest for MainWindow.insert_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.new_item = self.mocker.new_item
        testobj.insert_item()
        assert capsys.readouterr().out == (
                "called MainWindow.new_item with args () {'under': False}\n")

    def test_new_item(self, monkeypatch, capsys):
        """unittest for MainWindow.new_item
        """
        def mock_get():
            print('called MainWindow.get_item_title')
            return '', []
        def mock_get_2():
            print('called MainWindow.get_item_title')
            return 'title', ['extra', 'titles']
        def mock_start(*args, **kwargs):
            print('called MainGui.start_add with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_item_title = mock_get
        testobj.gui.start_add = mock_start
        testobj.new_item()
        assert capsys.readouterr().out == "called MainWindow.get_item_title\n"
        testobj.get_item_title = mock_get_2
        testobj.new_item()
        assert capsys.readouterr().out == (
            "called MainWindow.get_item_title\n"
            "called MainGui.start_add with args (None, True, 'title', ['extra', 'titles']) {}\n")
        testobj.new_item(root='a root', under=False)
        assert capsys.readouterr().out == (
            "called MainWindow.get_item_title\n"
            "called MainGui.start_add with args ('a root', False, 'title', ['extra', 'titles']) {}\n")

    def test_get_item_title(self, monkeypatch, capsys):
        """unittest for MainWindow.get_item_title
        """
        monkeypatch.setattr(testee, 'datetime', MockDateTime)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ask_title = self.mocker.ask_title
        testobj.check_active = self.mocker.check
        assert testobj.get_item_title() == (None, None)
        assert capsys.readouterr().out == (
                "called MainWindow.ask_title with args"
                " ('Geef een titel op voor het nieuwe item', '01-01-2000 00:00:00')\n")
        testobj.ask_title = self.mocker.ask_title_2
        assert testobj.get_item_title() == ('xx', ['yyy', 'zzz'])
        assert capsys.readouterr().out == (
                "called MainWindow.ask_title with args"
                " ('Geef een titel op voor het nieuwe item', '01-01-2000 00:00:00')\n"
                "called MainWindow.check_active\n")

    def _test_do_additem(self, monkeypatch, capsys):
        """unittest for MainWindow.do_additem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_additem(root, under, origpos, new_title, extra_titles) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_rename_item(self, monkeypatch, capsys):
        """unittest for MainWindow.rename_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.rename_item(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_ask_title(self, monkeypatch, capsys):
        """unittest for MainWindow.ask_title
        """
        monkeypatch.setattr(testee.gui, 'get_text', mock_get_text)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_title('title', 'text') == ()
        assert capsys.readouterr().out == (
                f"called gui.get_text with args ({testobj.gui}, 'title', 'text') {{}}\n")

        monkeypatch.setattr(testee.gui, 'get_text', mock_get_text_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_title('title', 'text') == ("new text", [])
        assert capsys.readouterr().out == (
                f"called gui.get_text with args ({testobj.gui}, 'title', 'text') {{}}\n")

        monkeypatch.setattr(testee.gui, 'get_text', mock_get_text_3)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_title('title', 'text') == ("(untitled)", [])
        assert capsys.readouterr().out == (
                f"called gui.get_text with args ({testobj.gui}, 'title', 'text') {{}}\n")

    def test_expand_item(self, monkeypatch, capsys):
        """unittest for MainWindow.expand_item
        """
        def mock_expand(*args, **kwargs):
            print('called MainWindow.expand with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.expand = mock_expand
        testobj.expand_item()
        assert capsys.readouterr().out == "called MainWindow.expand with args () {}\n"

    def test_collapse_item(self, monkeypatch, capsys):
        """unittest for MainWindow.collapse_item
        """
        def mock_collapse(*args, **kwargs):
            print('called MainWindow.collapse with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.collapse = mock_collapse
        testobj.collapse_item()
        assert capsys.readouterr().out == "called MainWindow.collapse with args () {}\n"

    def test_expand_all(self, monkeypatch, capsys):
        """unittest for MainWindow.expand_all
        """
        def mock_expand(*args, **kwargs):
            print('called MainWindow.expand with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.expand = mock_expand
        testobj.expand_all()
        assert capsys.readouterr().out == (
                "called MainWindow.expand with args () {'recursive': True}\n")

    def test_collapse_all(self, monkeypatch, capsys):
        """unittest for MainWindow.collapse_all
        """
        def mock_collapse(*args, **kwargs):
            print('called MainWindow.collapse with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.collapse = mock_collapse
        testobj.collapse_all()
        assert capsys.readouterr().out == (
                "called MainWindow.collapse with args () {'recursive': True}\n")

    def test_expand(self, monkeypatch, capsys):
        """unittest for MainWindow.expand
        """
        counter = 0
        def mock_getitemkids(arg):
            nonlocal counter
            print(f'called Tree.getitemkids with arg `{arg}`')
            counter += 1
            if counter == 1:
                return ['child1', 'child2']
            return []
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.getitemkids = mock_getitemkids
        testobj.expand()
        assert capsys.readouterr().out == (
                "called Tree.get_selected_item\n"
                "called Tree.set_item_expanded with args (['selected_item'],)\n")
        testobj.expand(recursive=True)
        assert capsys.readouterr().out == (
                "called Tree.get_selected_item\n"
                "called Tree.set_item_expanded with args (['selected_item'],)\n"
                "called Tree.getitemkids with arg `['selected_item']`\n"
                "called Tree.set_item_expanded with args ('child1',)\n"
                "called Tree.getitemkids with arg `child1`\n"
                "called Tree.set_item_expanded with args ('child2',)\n"
                "called Tree.getitemkids with arg `child2`\n")

    def test_collapse(self, monkeypatch, capsys):
        """unittest for MainWindow.collapse
        """
        counter = 0
        def mock_getitemkids(arg):
            nonlocal counter
            print(f'called Tree.getitemkids with arg `{arg}`')
            counter += 1
            if counter == 1:
                return ['child1', 'child2']
            return []
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.getitemkids = mock_getitemkids
        testobj.collapse()
        assert capsys.readouterr().out == (
                "called Tree.get_selected_item\n"
                "called Tree.set_item_collapsed with args (['selected_item'],)\n")
        testobj.collapse(recursive=True)
        assert capsys.readouterr().out == (
                "called Tree.get_selected_item\n"
                "called Tree.getitemkids with arg `['selected_item']`\n"
                "called Tree.getitemkids with arg `child1`\n"
                "called Tree.set_item_collapsed with args ('child1',)\n"
                "called Tree.getitemkids with arg `child2`\n"
                "called Tree.set_item_collapsed with args ('child2',)\n"
                "called Tree.set_item_collapsed with args (['selected_item'],)\n")

    def test_next_note(self, monkeypatch, capsys):
        """unittest for MainWindow.next_note
        """
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.next_note()
        assert capsys.readouterr().out == (
            "called MainGui.set_next_item with args () {}\n"
            f"called gui.show_message with args ({testobj.gui}, 'Geen volgend item op dit niveau')\n")

    def test_prev_note(self, monkeypatch, capsys):
        """unittest for MainWindow.prev_note
        """
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.prev_note()
        assert capsys.readouterr().out == (
            "called MainGui.set_prev_item with args () {}\n"
            f"called gui.show_message with args ({testobj.gui}, 'Geen vorig item op dit niveau')\n")

    def test_next_note_any(self, monkeypatch, capsys):
        """unittest for MainWindow.next_note_any
        """
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.next_note_any()
        assert capsys.readouterr().out == (
            "called MainGui.set_next_item with args () {'any_level': True}\n"
            f"called gui.show_message with args ({testobj.gui}, 'Geen volgend item')\n")

    def test_prev_note_any(self, monkeypatch, capsys):
        """unittest for MainWindow.prev_note_any
        """
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.prev_note_any()
        assert capsys.readouterr().out == (
            "called MainGui.set_prev_item with args () {'any_level': True}\n"
            f"called gui.show_message with args ({testobj.gui}, 'Geen vorig item')\n")

    def test_cut_item(self, monkeypatch, capsys):
        """unittest for MainWindow.cut_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_copy_item = self.mocker.get_copy_item
        testobj.cut_item()
        assert capsys.readouterr().out == (
                "called MainWindow.get_copy_item with args () {'cut': True}\n")

    def test_delete_item(self, monkeypatch, capsys):
        """unittest for MainWindow.delete_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_copy_item = self.mocker.get_copy_item
        testobj.delete_item()
        assert capsys.readouterr().out == (
                "called MainWindow.get_copy_item with args () {'cut': True, 'retain': False}\n")

    def test_copy_item(self, monkeypatch, capsys):
        """unittest for MainWindow.copy_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_copy_item = self.mocker.get_copy_item
        testobj.copy_item()
        assert capsys.readouterr().out == "called MainWindow.get_copy_item with args () {}\n"

    def test_get_copy_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_copy_item
        """
        def mock_get_source(*args):
            print('called MainWindow.get_copy_source with args', args)
        def mock_get_source_2(*args):
            print('called MainWindow.get_copy_source with args', args)
            return 'item'
        def mock_start(*args):
            print('called MainGui.start_copy with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_copy_source = mock_get_source
        testobj.gui.start_copy = mock_start
        testobj.get_copy_item()
        assert capsys.readouterr().out == (
                "called MainWindow.get_copy_source with args (False, True, None)\n")
        testobj.get_copy_source = mock_get_source_2
        testobj.get_copy_item()
        assert capsys.readouterr().out == (
                "called MainWindow.get_copy_source with args (False, True, None)\n"
                "called MainGui.start_copy with args (False, True, 'item')\n")
        testobj.get_copy_item(cut=True)
        assert capsys.readouterr().out == (
                "called MainWindow.get_copy_source with args (True, True, None)\n"
                "called MainGui.start_copy with args (True, True, 'item')\n")
        testobj.get_copy_item(retain=False)
        assert capsys.readouterr().out == (
                "called MainWindow.get_copy_source with args (False, False, None)\n"
                "called MainGui.start_copy with args (False, False, 'item')\n")
        testobj.get_copy_item(to_other_file='text.trd')
        assert capsys.readouterr().out == (
                "called MainWindow.get_copy_source with args (False, True, 'text.trd')\n"
                "called MainGui.start_copy with args (False, True, 'item')\n")

    def test_get_copy_source(self, monkeypatch, capsys):
        """unittest for MainWindow.get_copy_source
        """
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        monkeypatch.setattr(testee.gui, 'ask_ynquestion', mock_ask_yn)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = 'selected_item'
        assert testobj.get_copy_source(False, False, '') is None
        assert capsys.readouterr().out == (
                'called Tree.getselecteditem\n'
                f'called gui.show_message with args ({testobj.gui}, "Can\'t do this with root")\n')
        testobj.gui.root = 'gui root'
        assert testobj.get_copy_source(False, False, '') == "selected_item"
        assert capsys.readouterr().out == "called Tree.getselecteditem\n"
        assert testobj.get_copy_source(True, False, '') is None
        assert capsys.readouterr().out == (
                'called Tree.getselecteditem\n'
                "called gui.ask_ynquestion with args"
                f" ({testobj.gui}, 'Are you sure you want to remove this item?')\n")
        assert testobj.get_copy_source(False, True, '') == "selected_item"
        assert capsys.readouterr().out == "called Tree.getselecteditem\n"
        assert testobj.get_copy_source(True, True, '') == "selected_item"
        assert capsys.readouterr().out == "called Tree.getselecteditem\n"
        assert testobj.get_copy_source(False, False, 'xxx') == "xxx"
        assert capsys.readouterr().out == ("")
        assert testobj.get_copy_source(True, False, 'xxx') == "xxx"
        assert capsys.readouterr().out == ("")
        assert testobj.get_copy_source(False, True, 'xxx') == "xxx"
        assert capsys.readouterr().out == ("")
        assert testobj.get_copy_source(True, True, 'xxx') == "xxx"
        assert capsys.readouterr().out == ("")

    def _test_do_copyaction(self, monkeypatch, capsys):
        """unittest for MainWindow.do_copyaction
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_copyaction(cut, retain, current) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_popitems(self, monkeypatch, capsys):
        """unittest for MainWindow.popitems
        """
        counter = 0
        def mock_getitemkids(arg):
            nonlocal counter
            print(f'called Tree.getitemkids with arg `{arg}`')
            counter += 1
            if counter == 1:
                return ['child1', 'child2']
            return []
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.getitemkids = mock_getitemkids
        testobj.itemdict = {1: 'xxx', 'current': 'yyy', 2: 'zzz', 'child1': 'aaa', 3: 'bbb',
                            'child2': 'ccc', 4: 'ddd'}
        testobj.popitems('current', ['item', 'list'])
        assert testobj.itemdict == {1: 'xxx', 2: 'zzz', 3: 'bbb', 4: 'ddd'}
        assert capsys.readouterr().out == ("called Tree.getitemkey with arg `current`\n"
                                           "called Tree.getitemkids with arg `current`\n"
                                           "called Tree.getitemkey with arg `child1`\n"
                                           "called Tree.getitemkids with arg `child1`\n"
                                           "called Tree.getitemkey with arg `child2`\n"
                                           "called Tree.getitemkids with arg `child2`\n")

    def test_paste_item(self, monkeypatch, capsys):
        """unittest for MainWindow.paste_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.put_paste_item = self.mocker.put_paste_item
        testobj.paste_item()
        assert capsys.readouterr().out == "called MainWindow.put_paste_item with args () {}\n"

    def test_paste_item_after(self, monkeypatch, capsys):
        """unittest for MainWindow.paste_item_after
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.put_paste_item = self.mocker.put_paste_item
        testobj.paste_item_after()
        assert capsys.readouterr().out == (
                "called MainWindow.put_paste_item with args () {'before': False}\n")

    def test_paste_item_below(self, monkeypatch, capsys):
        """unittest for MainWindow.paste_item_below
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.put_paste_item = self.mocker.put_paste_item
        testobj.paste_item_below()
        assert capsys.readouterr().out == (
                "called MainWindow.put_paste_item with args () {'below': True}\n")

    def test_put_paste_item(self, monkeypatch, capsys):
        """unittest for MainWindow.put_paste_item
        """
        # testobj = self.setup_testobj(monkeypatch, capsys)
        # assert testobj.put_paste_item(before=True, below=False) == "expected_result"
        # assert capsys.readouterr().out == ("")
        def mock_get_dest(*args):
            print('called MainWindow.get_paste_dest with args', args)
        def mock_get_dest_2(*args):
            print('called MainWindow.get_paste_dest with args', args)
            return 'item'
        def mock_start(*args):
            print('called MainGui.start_paste with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_paste_dest = mock_get_dest
        testobj.gui.start_paste = mock_start
        testobj.put_paste_item()
        assert capsys.readouterr().out == (
                "called MainWindow.get_paste_dest with args (False,)\n")
        testobj.get_paste_dest = mock_get_dest_2
        testobj.put_paste_item()
        assert capsys.readouterr().out == (
                "called MainWindow.get_paste_dest with args (False,)\n"
                "called MainGui.start_paste with args (True, False, 'item')\n")
        testobj.put_paste_item(below=True)
        assert capsys.readouterr().out == (
                "called MainWindow.get_paste_dest with args (True,)\n"
                "called MainGui.start_paste with args (True, True, 'item')\n")
        testobj.put_paste_item(before=False)
        assert capsys.readouterr().out == (
                "called MainWindow.get_paste_dest with args (False,)\n"
                "called MainGui.start_paste with args (False, False, 'item')\n")

    def test_get_paste_dest(self, monkeypatch, capsys):
        """unittest for MainWindow.get_paste_dest
        """
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = 'selected_item'
        testobj.copied_item = None
        assert testobj.get_paste_dest(False) is None
        assert capsys.readouterr().out == ("called Tree.getselecteditem\n"
                                           "called gui.show_message with args"
                                           f" ({testobj.gui}, 'Can only copy *below* the root')\n")

        testobj.gui.root = 'selected_item'
        testobj.copied_item = 'copied item'
        assert testobj.get_paste_dest(False) is None
        assert capsys.readouterr().out == ("called Tree.getselecteditem\n"
                                           "called gui.show_message with args"
                                           f" ({testobj.gui}, 'Can only copy *below* the root')\n")

        testobj.gui.root = 'selected_item'
        testobj.copied_item = None
        assert testobj.get_paste_dest(True) is None
        assert capsys.readouterr().out == ("called Tree.getselecteditem\n"
                                           "called gui.show_message with args"
                                           f" ({testobj.gui}, 'Nothing to paste')\n")

        testobj.gui.root = 'selected_item'
        testobj.copied_item = 'copied item'
        assert testobj.get_paste_dest(True) == 'selected_item'
        assert capsys.readouterr().out == "called Tree.getselecteditem\n"

        testobj.gui.root = 'gui root'
        testobj.copied_item = None
        assert testobj.get_paste_dest(False) is None
        assert capsys.readouterr().out == ("called Tree.getselecteditem\n"
                                           "called gui.show_message with args"
                                           f" ({testobj.gui}, 'Nothing to paste')\n")

        testobj.gui.root = 'gui root'
        testobj.copied_item = 'copied item'
        assert testobj.get_paste_dest(True) == 'selected_item'
        assert capsys.readouterr().out == "called Tree.getselecteditem\n"

        testobj.gui.root = 'gui root'
        testobj.copied_item = None
        assert testobj.get_paste_dest(True) is None
        assert capsys.readouterr().out == ("called Tree.getselecteditem\n"
                                           "called gui.show_message with args"
                                           f" ({testobj.gui}, 'Nothing to paste')\n")

        testobj.gui.root = 'gui root'
        testobj.copied_item = 'copied item'
        assert testobj.get_paste_dest(True) == 'selected_item'
        assert capsys.readouterr().out == "called Tree.getselecteditem\n"

    def _test_do_pasteitem(self, monkeypatch, capsys):
        """unittest for MainWindow.do_pasteitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_pasteitem(before, below, current) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_add_items_back(self, monkeypatch, capsys):
        """unittest for MainWindow.add_items_back
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemdict = {1: ('x', 'xx')}
        testobj.cut_from_itemdict = [(2, ('y', 'yy'))]
        assert testobj.add_items_back() == [2]
        assert testobj.itemdict == {1: ('x', 'xx'), 2: ('y', 'yy')}

    def _test_move_to_file(self, monkeypatch, capsys):
        """unittest for MainWindow.move_to_file
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_to_file(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_order_top(self, monkeypatch, capsys):
        """unittest for MainWindow.order_top
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reorder = self.mocker.reorder
        testobj.gui.root = 'gui root'
        testobj.order_top()
        assert capsys.readouterr().out == "called MainWindow.reorder with args ('gui root',) {}\n"

    def test_order_all(self, monkeypatch, capsys):
        """unittest for MainWindow.order_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reorder = self.mocker.reorder
        testobj.gui.root = 'gui root'
        testobj.order_all()
        assert capsys.readouterr().out == (
                "called MainWindow.reorder with args ('gui root',) {'recursive': True}\n")

    def test_order_this(self, monkeypatch, capsys):
        """unittest for MainWindow.order_this
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reorder = self.mocker.reorder
        testobj.activeitem = 'active item'
        testobj.order_this()
        assert capsys.readouterr().out == "called MainWindow.reorder with args ('active item',) {}\n"

    def test_order_lower(self, monkeypatch, capsys):
        """unittest for MainWindow.order_lower
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reorder = self.mocker.reorder
        testobj.activeitem = 'active item'
        testobj.order_lower()
        assert capsys.readouterr().out == (
                "called MainWindow.reorder with args ('active item',) {'recursive': True}\n")

    def test_reorder(self, monkeypatch, capsys):
        """unittest for MainWindow.reorder
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_project_dirty = self.mocker.set_dirty
        testobj.reorder('root')
        assert capsys.readouterr().out == (
                "called MainGui.reorder_items with args ('root', False) {}\n"
                "called MainWindow.set_project_dirty with arg True\n")
        testobj.reorder('root', recursive=True)
        assert capsys.readouterr().out == (
                "called MainGui.reorder_items with args ('root', True) {}\n"
                "called MainWindow.set_project_dirty with arg True\n")

    def test_hide_me(self, monkeypatch, capsys):
        """unittest for MainWindow.hide_me
        """
        monkeypatch.setattr(testee.shared, 'HIDE_TEXT', 'xxx')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.confirm = self.mocker.confirm
        testobj.hide_me()
        assert capsys.readouterr().out == ("called MainWindow.confirm with args"
                                           " () {'setting': 'AskBeforeHide', 'textitem': 'xxx'}\n"
                                           "called MainGui.hide_me\n")

    def test_change_pane(self, monkeypatch, capsys):
        """unittest for MainWindow.change_pane
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.check_active = self.mocker.check
        testobj.gui.in_editor = False
        testobj.change_pane()
        assert capsys.readouterr().out == "called MainGui.set_focus_to_editor\n"
        testobj.gui.in_editor = True
        testobj.change_pane()
        assert capsys.readouterr().out == ("called MainWindow.check_active\n"
                                           "called MainGui.set_focus_to_tree\n")

    def test_set_options(self, monkeypatch, capsys):
        """unittest for MainWindow.set_options
        """
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_escape_action = self.mocker.set_escape_action
        testobj.set_options()
        assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj.gui},"
                                           " <class 'doctree.qtgui.OptionsDialog'>)\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog_2)
        testobj.set_options()
        assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj.gui},"
                                           " <class 'doctree.qtgui.OptionsDialog'>)\n"
                                           "called MainWindow.set_escape_action\n")

    def test_add_view(self, monkeypatch, capsys):
        """unittest for MainWindow.add_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.check_active = self.mocker.check
        testobj.treetoview = self.mocker.treetoview
        testobj.viewtotree = self.mocker.viewtotree
        testobj.set_project_dirty = self.mocker.set_dirty
        testobj.opts = {'ActiveItem': ['item0', 'item1'], 'ActiveView': 1,
                        'ViewNames': ['View0', 'View1']}
        testobj.views = ['', '']
        testobj.activeitem = 'active item'
        testobj.viewcount = 1
        testobj.gui.root = 'gui root'
        testobj.itemdict = {1: ('x', 'xx'), 2: ('y', 'yy')}
        testobj.add_view()
        assert testobj.opts == {'ActiveItem': ['item0', 'item data', 'item data'], 'ActiveView': 2,
                                'ViewNames': ['View0', 'View1', 'New View #2']}
        assert testobj.views == ['', 'A view', [(1, []), (2, [])]]
        assert testobj.viewcount == 2
        assert capsys.readouterr().out == (
                "called MainWindow.check_active\n"
                "called Tree.getitemdata with arg `active item`\n"
                "called MainWindow.treetoview\n"
                "called MainGui.uncheck_viewmenu_option\n"
                "called MainGui.add_viewmenu_option with arg '&2 New View #2'\n"
                "called MainGui.check_viewmenu_option with arg 'An action'\n"
                "called MainGui.rebuild_root\n"
                "called MainWindow.viewtotree\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called Tree.set_item_selected with arg `An item`\n")

    def test_rename_view(self, monkeypatch, capsys):
        """unittest for MainWindow.rename_view
        """
        def mock_get_text_2(*args, **kwargs):
            print('called gui.get_text with args', args, kwargs)
            return True, 'View1'
        def mock_get_text_3(*args, **kwargs):
            print('called gui.get_text with args', args, kwargs)
            return True, 'Other view'
        monkeypatch.setattr(testee.gui, 'get_text', mock_get_text)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {'ActiveItem': ['item0', 'item1'], 'ActiveView': 1,
                        'ViewNames': ['View0', 'View1']}
        testobj.set_project_dirty = self.mocker.set_dirty
        testobj.rename_view()
        assert testobj.opts == {'ActiveItem': ['item0', 'item1'], 'ActiveView': 1,
                                'ViewNames': ['View0', 'View1']}
        assert capsys.readouterr().out == (
                "called gui.get_text with args"
                f" ({testobj.gui}, 'Geef een nieuwe naam voor de huidige view', 'View1') {{}}\n")
        monkeypatch.setattr(testee.gui, 'get_text', mock_get_text_2)
        testobj.rename_view()
        assert testobj.opts == {'ActiveItem': ['item0', 'item1'], 'ActiveView': 1,
                                'ViewNames': ['View0', 'View1']}
        assert capsys.readouterr().out == (
                "called gui.get_text with args"
                f" ({testobj.gui}, 'Geef een nieuwe naam voor de huidige view', 'View1') {{}}\n")
        monkeypatch.setattr(testee.gui, 'get_text', mock_get_text_3)
        testobj.rename_view()
        assert testobj.opts == {'ActiveItem': ['item0', 'item1'], 'ActiveView': 1,
                                'ViewNames': ['View0', 'Other view']}
        assert capsys.readouterr().out == (
                "called gui.get_text with args"
                f" ({testobj.gui}, 'Geef een nieuwe naam voor de huidige view', 'View1') {{}}\n"
                "called MainGui.rename_viewmenu_option with arg 'Other view'\n"
                "called MainWindow.set_project_dirty with arg True\n")

    def test_remove_view(self, monkeypatch, capsys):
        """unittest for MainWindow.remove_view
        """
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        monkeypatch.setattr(testee.gui, 'ask_ynquestion', mock_ask_yn)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {'ActiveItem': ['item0', 'item1'], 'ActiveView': 1,
                        'ViewNames': ['View0', 'View1']}
        testobj.viewcount = 1
        testobj.viewtotree = self.mocker.viewtotree
        testobj.set_project_dirty = self.mocker.set_dirty
        testobj.remove_view()
        assert capsys.readouterr().out == (f'called gui.show_message with args ({testobj.gui},'
                                           ' "Can\'t delete the last (only) view")\n')

        testobj.viewcount = 2
        testobj.remove_view()
        assert capsys.readouterr().out == (f"called gui.ask_ynquestion with args ({testobj.gui},"
                                           " 'Are you sure you want to remove this view?')\n")

        monkeypatch.setattr(testee.gui, 'ask_ynquestion', mock_ask_yn_2)
        testobj.viewcount = 2
        testobj.views = [('view1',), ('view2',)]
        testobj.remove_view()
        assert testobj.viewcount == 1
        assert testobj.opts == {'ActiveItem': ['item0'], 'ActiveView': 0,
                                'ViewNames': ['View0']}
        assert capsys.readouterr().out == (
                f"called gui.ask_ynquestion with args ({testobj.gui},"
                " 'Are you sure you want to remove this view?')\n"
                "called MainGui.remove_viewmenu_option with arg 'View1'\n"
                "called MainGui.check_viewmenu_option with arg 'An action'\n"
                "called MainGui.rebuild_root\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called MainWindow.viewtotree\n"
                "called Tree.set_item_selected with arg `An item`\n")
        testobj.viewcount = 2
        testobj.opts = {'ActiveItem': ['item0', 'item1'], 'ActiveView': 0,
                        'ViewNames': ['View0', 'View1']}
        testobj.remove_view()
        assert testobj.viewcount == 1
        assert testobj.opts == {'ActiveItem': ['item1'], 'ActiveView': 0,
                                'ViewNames': ['View1']}
        assert capsys.readouterr().out == (
                f"called gui.ask_ynquestion with args ({testobj.gui},"
                " 'Are you sure you want to remove this view?')\n"
                "called MainGui.remove_viewmenu_option with arg 'View0'\n"
                "called MainGui.check_viewmenu_option with arg 'An action'\n"
                "called MainGui.rebuild_root\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called MainWindow.viewtotree\n"
                "called Tree.set_item_selected with arg `An item`\n")

    def test_next_view(self, monkeypatch, capsys):
        """unittest for MainWindow.next_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.goto_view = self.mocker.goto_view
        testobj.next_view()
        assert capsys.readouterr().out == (
                "called MainWindow.goto_view with args () {'goto_next': True}\n")

    def test_prev_view(self, monkeypatch, capsys):
        """unittest for MainWindow.prev_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.goto_view = self.mocker.goto_view
        testobj.prev_view()
        assert capsys.readouterr().out == (
                "called MainWindow.goto_view with args () {'goto_next': False}\n")

    def test_goto_view(self, monkeypatch, capsys):
        """unittest for MainWindow.goto_view
        """
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {'ActiveItem': ['item0', 'item1'], 'ActiveView': 1,
                        'ViewNames': ['View0', 'View1']}
        testobj.viewcount = 1
        testobj.goto_view()
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'This is the only view')\n")
        testobj.viewcount = 2
        testobj.views = [('view1',), ('view2',)]
        testobj.activeitem = 'active item'
        testobj.gui.root = 'gui root'
        testobj.check_active = self.mocker.check
        testobj.treetoview = self.mocker.treetoview
        testobj.viewtotree = self.mocker.viewtotree
        testobj.set_window_title = self.mocker.set_title
        testobj.opts["ActiveView"] = 0
        testobj.goto_view()
        assert capsys.readouterr().out == (
                "called MainWindow.check_active\n"
                "called MainWindow.treetoview\n"
                "called Editor.clear\n"
                "called MainGui.next_check_viewmenu_option\n"
                "called MainGui.rebuild_root\n"
                "called MainWindow.viewtotree\n"
                "called MainWindow.set_window_title\n"
                "called Tree.set_item_selected with arg `An item`\n")
        assert testobj.opts["ActiveView"] == 1
        assert testobj.activeitem == 'gui root'
        assert testobj.views == ['A view', ('view2',)]

        testobj.activeitem = 'active item'
        testobj.gui.root = 'gui root'
        testobj.views = [('view1',), ('view2',)]
        testobj.goto_view()
        assert capsys.readouterr().out == (
                "called MainWindow.check_active\n"
                "called MainWindow.treetoview\n"
                "called Editor.clear\n"
                "called MainGui.next_check_viewmenu_option\n"
                "called MainGui.rebuild_root\n"
                "called MainWindow.viewtotree\n"
                "called MainWindow.set_window_title\n"
                "called Tree.set_item_selected with arg `An item`\n")
        assert testobj.opts["ActiveView"] == 0
        assert testobj.activeitem == 'gui root'
        assert testobj.views == [('view1',), 'A view']

        testobj.opts["ActiveView"] = 1
        testobj.activeitem = 'active item'
        testobj.gui.root = 'gui root'
        testobj.views = [('view1',), ('view2',)]
        testobj.goto_view(goto_next=False)
        assert capsys.readouterr().out == (
                "called MainWindow.check_active\n"
                "called MainWindow.treetoview\n"
                "called Editor.clear\n"
                "called MainGui.check_next_viewmenu_option with args {'prev': True}\n"
                "called MainGui.rebuild_root\n"
                "called MainWindow.viewtotree\n"
                "called MainWindow.set_window_title\n"
                "called Tree.set_item_selected with arg `An item`\n")
        assert testobj.opts["ActiveView"] == 0
        assert testobj.activeitem == 'gui root'
        assert testobj.views == [('view1',), 'A view']

        testobj.activeitem = 'active item'
        testobj.gui.root = 'gui root'
        testobj.views = [('view1',), ('view2',)]
        testobj.goto_view(goto_next=False)
        assert capsys.readouterr().out == (
                "called MainWindow.check_active\n"
                "called MainWindow.treetoview\n"
                "called Editor.clear\n"
                "called MainGui.check_next_viewmenu_option with args {'prev': True}\n"
                "called MainGui.rebuild_root\n"
                "called MainWindow.viewtotree\n"
                "called MainWindow.set_window_title\n"
                "called Tree.set_item_selected with arg `An item`\n")
        assert testobj.opts["ActiveView"] == 1
        assert testobj.activeitem == 'gui root'
        assert testobj.views == ['A view', ('view2',)]

    def test_select_view_from_dropdown(self, monkeypatch, capsys):
        """unittest for MainWindow.select_view_from_dropdown
        """
        monkeypatch.setattr(testee.gui, 'get_choice', mock_get_choice)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {'ActiveItem': ['item0', 'item1'], 'ActiveView': 1,
                        'ViewNames': ['View0', 'selection']}
        testobj.views = [('view1',), ('view2',)]
        testobj.check_active = self.mocker.check
        testobj.treetoview = self.mocker.treetoview
        testobj.viewtotree = self.mocker.viewtotree
        testobj.set_window_title = self.mocker.set_title
        testobj.gui.root = 'gui root'
        testobj.select_view_from_dropdown()
        assert testobj.views == [('view1',), ('view2',)]
        assert capsys.readouterr().out == (
                "called gui.get_choice with args"
                f" ({testobj.gui}, 'Select a view:', ['View0', 'selection'], 1) {{}}\n")

        monkeypatch.setattr(testee.gui, 'get_choice', mock_get_choice_2)
        testobj.select_view_from_dropdown()
        assert capsys.readouterr().out == (
                "called gui.get_choice with args"
                f" ({testobj.gui}, 'Select a view:', ['View0', 'selection'], 1) {{}}\n"
                "called MainWindow.check_active\n"
                "called MainWindow.treetoview\n"
                "called Editor.clear\n"
                "called MainGui.rebuild_root\n"
                "called MainWindow.viewtotree\n"
                "called MainWindow.set_window_title\n"
                "called Tree.set_item_selected with arg `An item`\n")

    def test_select_view(self, monkeypatch, capsys):
        """unittest for MainWindow.select_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {'ActiveItem': ['item0', 'item1'], 'ActiveView': 1,
                        'ViewNames': ['New view', 'View1']}
        testobj.views = [('view1',), ('view2',)]
        testobj.viewnames = ['New view', '']
        testobj.check_active = self.mocker.check
        testobj.treetoview = self.mocker.treetoview
        testobj.viewtotree = self.mocker.viewtotree
        testobj.set_window_title = self.mocker.set_title
        testobj.gui.root = 'gui root'
        testobj.select_view()
        assert testobj.views == [('view1',), 'A view']
        assert testobj.opts["ActiveView"] == 0
        assert testobj.activeitem == 'gui root'
        assert capsys.readouterr().out == (
                "called MainWindow.check_active\n"
                "called MainWindow.treetoview\n"
                "called Editor.clear\n"
                "called MainGui.check_viewmenu_option\n"
                "called MainGui.rebuild_root\n"
                "called MainWindow.viewtotree\n"
                "called MainWindow.set_window_title\n"
                "called Tree.set_item_selected with arg `An item`\n")

    def test_search(self, monkeypatch, capsys):
        """unittest for MainWindow.search
        """
        def search_from_start_2():
            print('called Editor.search_from_start')
            return True
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
        monkeypatch.setattr(testee.gui, 'show_nonmodal', mock_show_nonmodal)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.go_to_result = self.mocker.go_to_result
        testobj.search_from = self.mocker.search_from
        testobj.gui.root = 'gui root'
        testobj.gui.srchlist = True
        testobj.search()
        assert capsys.readouterr().out == (
                "called gui.show_message with args"
                f" ({testobj.gui}, 'Cannot start new search while results screen is showing')\n")

        testobj.gui.srchlist = False
        testobj.search()
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" ({testobj.gui}, <class 'doctree.qtgui.SearchDialog'>)\n")

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog_2)
        testobj.gui.srchtype = 4
        testobj.search()
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" ({testobj.gui}, <class 'doctree.qtgui.SearchDialog'>)\n"
                f"called gui.show_message with args ({testobj.gui}, 'Wrong search type')\n")

        testobj.gui.srchtype = 0
        testobj.search()
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" ({testobj.gui}, <class 'doctree.qtgui.SearchDialog'>)\n"
                "called Editor.search_from_start\n"
                f"called gui.show_message with args ({testobj.gui}, 'Search string not found')\n")

        testobj.gui.editor.search_from_start = search_from_start_2
        testobj.search()
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" ({testobj.gui}, <class 'doctree.qtgui.SearchDialog'>)\n"
                "called Editor.search_from_start\n")

        testobj.gui.srchtype = 1
        testobj.search()
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" ({testobj.gui}, <class 'doctree.qtgui.SearchDialog'>)\n"
                "called MainWindow.search_from with args ('gui root',)\n"
                f"called gui.show_message with args ({testobj.gui}, 'Search string not found')\n")

        testobj.search_from = self.mocker.search_from_2
        testobj.search()
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" ({testobj.gui}, <class 'doctree.qtgui.SearchDialog'>)\n"
                "called MainWindow.search_from with args ('gui root',)\n"
                "called MainWindow.go_to_result\n")

        # mislukte poging om r. 1060 nog gecovered te krijgen
        testobj.search_from = self.mocker.search_from_3
        testobj.search()
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" ({testobj.gui}, <class 'doctree.qtgui.SearchDialog'>)\n"
                "called MainWindow.search_from with args ('gui root',)\n"
                "called MainWindow.go_to_result\n")

    def test_search_texts(self, monkeypatch, capsys):
        """unittest for MainWindow.search_texts
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search = self.mocker.search
        testobj.search_texts()
        assert capsys.readouterr().out == "called MainWindow.search with args {'mode': 2}\n"

    def test_search_titles(self, monkeypatch, capsys):
        """unittest for MainWindow.search_titles
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search = self.mocker.search
        testobj.search_titles()
        assert capsys.readouterr().out == "called MainWindow.search with args {'mode': 1}\n"

    def test_find_next(self, monkeypatch, capsys):
        """unittest for MainWindow.find_next
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.go_to_result = self.mocker.go_to_result
        testobj.gui.srchtext = ''
        testobj.gui.srchtype = 0
        testobj.srchno = 1
        testobj.find_next()
        assert capsys.readouterr().out == ""
        testobj.gui.srchtext = 'x'
        testobj.find_next()
        assert capsys.readouterr().out == "called Editor.find_next\n"
        testobj.gui.srchtype = 1
        testobj.find_next()
        assert testobj.srchno == 2
        assert capsys.readouterr().out == "called MainWindow.go_to_result\n"

    def test_find_prev(self, monkeypatch, capsys):
        """unittest for MainWindow.find_prev
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.go_to_result = self.mocker.go_to_result
        testobj.gui.srchtext = ''
        testobj.gui.srchtype = 0
        testobj.srchno = 1
        testobj.find_prev()
        assert capsys.readouterr().out == ""
        testobj.gui.srchtext = 'x'
        testobj.find_prev()
        assert capsys.readouterr().out == "called Editor.find_prev\n"
        testobj.gui.srchtype = 1
        testobj.find_prev()
        assert testobj.srchno == 0
        assert capsys.readouterr().out == "called MainWindow.go_to_result\n"

    def _test_search_from(self, monkeypatch, capsys):
        """unittest for MainWindow.search_from
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.search_from(parent, loc=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go_to_result(self, monkeypatch, capsys):
        """unittest for MainWindow.go_to_result
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go_to_result() == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_info_page(self, monkeypatch, capsys):
        """unittest for MainWindow.info_page
        """
        monkeypatch.setattr(testee, 'app_info', 'app info')
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.info_page()
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'app info')\n")

    def test_help_page(self, monkeypatch, capsys):
        """unittest for MainWindow.help_page
        """
        monkeypatch.setattr(testee, 'help_info', 'help info')
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.help_page()
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'help info')\n")

    def test_set_project_dirty(self, monkeypatch, capsys):
        """unittest for MainWindow.set_project_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_dirty = False
        testobj.set_window_title = self.mocker.set_title
        testobj.set_project_dirty(True)
        assert testobj.project_dirty
        assert capsys.readouterr().out == "called MainWindow.set_window_title\n"

    def test_handle_save_needed(self, monkeypatch, capsys):
        """unittest for MainWindow.handle_save_needed
        """
        def check_2():
            print('called Editor.check_dirty')
            return True
        monkeypatch.setattr(testee.gui, 'ask_yncquestion', mock_ask_ync)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.check_active = self.mocker.check
        testobj.save = self.mocker.save
        # allebei False en check_dirty ook
        testobj.has_treedata = False
        testobj.project_dirty = False
        testobj.gui.in_editor = False
        assert testobj.handle_save_needed()
        assert capsys.readouterr().out == "called Editor.check_dirty\n"
        assert testobj.handle_save_needed(always_check=False)
        assert capsys.readouterr().out == ""

        testobj.has_treedata = True
        testobj.gui.in_editor = False
        assert testobj.handle_save_needed()
        assert capsys.readouterr().out == "called Editor.check_dirty\n"
        assert testobj.handle_save_needed(always_check=False)
        assert capsys.readouterr().out == ""

        testobj.project_dirty = True
        testobj.gui.in_editor = False
        assert testobj.handle_save_needed()
        assert capsys.readouterr().out == (
                "called Editor.check_dirty\n"
                "called gui.ask_yncquestion with args"
                f" ({testobj.gui}, 'Data changed - save current file before continuing?')\n")
        assert testobj.handle_save_needed(always_check=False)
        assert capsys.readouterr().out == (
                "called gui.ask_yncquestion with args"
                f" ({testobj.gui}, 'Data changed - save current file before continuing?')\n")
        testobj.gui.in_editor = True
        assert testobj.handle_save_needed()
        assert capsys.readouterr().out == (
                "called Editor.check_dirty\n"
                "called MainWindow.check_active\n"
                "called gui.ask_yncquestion with args"
                f" ({testobj.gui}, 'Data changed - save current file before continuing?')\n")

        testobj.gui.editor.check_dirty = check_2
        testobj.project_dirty = False
        assert testobj.handle_save_needed()
        assert capsys.readouterr().out == (
                "called Editor.check_dirty\n"
                "called MainWindow.check_active\n"
                "called gui.ask_yncquestion with args"
                f" ({testobj.gui}, 'Data changed - save current file before continuing?')\n")
        assert testobj.handle_save_needed(always_check=False)
        assert capsys.readouterr().out == ''

        monkeypatch.setattr(testee.gui, 'ask_yncquestion', mock_ask_ync_2)
        testobj.project_dirty = True
        assert testobj.handle_save_needed()
        assert capsys.readouterr().out == (
                "called Editor.check_dirty\n"
                "called MainWindow.check_active\n"
                "called gui.ask_yncquestion with args"
                f" ({testobj.gui}, 'Data changed - save current file before continuing?')\n"
                "called MainWindow.save\n")

        monkeypatch.setattr(testee.gui, 'ask_yncquestion', mock_ask_ync_3)
        testobj.project_dirty = True
        assert not testobj.handle_save_needed()
        assert capsys.readouterr().out == (
                "called Editor.check_dirty\n"
                "called MainWindow.check_active\n"
                "called gui.ask_yncquestion with args"
                f" ({testobj.gui}, 'Data changed - save current file before continuing?')\n")

    def _test_treetoview(self, monkeypatch, capsys):
        """unittest for MainWindow.treetoview
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.treetoview() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_viewtotree(self, monkeypatch, capsys):
        """unittest for MainWindow.viewtotree
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.viewtotree() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_check_active(self, monkeypatch, capsys):
        """unittest for MainWindow.check_active
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.check_active() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_activate_item(self, monkeypatch, capsys):
        """unittest for MainWindow.activate_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.activate_item(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_cleanup_files(self, monkeypatch, capsys):
        """unittest for MainWindow.cleanup_files
        """
        def mock_remove(arg):
            print(f"called shutil.rmtree with arg '{arg}'")
        monkeypatch.setattr(testee.shutil, 'rmtree', mock_remove)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.temp_imagepath = 'path_to_images'
        testobj.cleanup_files()
        assert capsys.readouterr().out == "called shutil.rmtree with arg 'path_to_images'\n"

    def _test_read(self, monkeypatch, capsys):
        """unittest for MainWindow.read
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.read(other_file='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_set_escape_action(self, monkeypatch, capsys):
        """unittest for MainWindow.set_escape_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {'EscapeClosesApp': True}
        testobj.set_escape_action()
        assert capsys.readouterr().out == ("called MainGui.add_escape_action\n")
        testobj.opts = {'EscapeClosesApp': False}
        testobj.set_escape_action()
        assert capsys.readouterr().out == ("called MainGui.remove_escape_action\n")

    def _test_write(self, monkeypatch, capsys):
        """unittest for MainWindow.write
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.write(meld=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for MainWindow.confirm
        """
        def mock_write(*args, **kwargs):
            print('called dml.write_to_files with args', args, kwargs)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
        monkeypatch.setattr(testee.dml, 'write_to_files', mock_write)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = 'xx'
        testobj.opts = {'this': ''}
        testobj.views = ['view1']
        testobj.itemdict = {1: 'x'}
        testobj.text_positions = [2]
        testobj.temp_imagepath = 'yyy'
        testobj.confirm(setting='this')
        assert capsys.readouterr().out == ("")
        testobj.opts = {'this': 'that'}
        testobj.confirm(setting='this')
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj.gui},"
                " <class 'doctree.qtgui.CheckDialog'>, {'message': '', 'option': 'this'})\n"
                "called dml.write_to_files with args ('xx', {'this': 'that'}, ['view1'],"
                " {1: 'x'}, [2], 'yyy') {'backup': False, 'save_images': False}\n")
        testobj.confirm(setting='this', textitem='zzz')
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj.gui},"
                " <class 'doctree.qtgui.CheckDialog'>, {'message': 'zzz', 'option': 'this'})\n"
                "called dml.write_to_files with args ('xx', {'this': 'that'}, ['view1'],"
                " {1: 'x'}, [2], 'yyy') {'backup': False, 'save_images': False}\n")
