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
    """stub for datetime.datetime
    """
    def today():
        return datetime.datetime(2000, 1, 1)


class MockTree:
    """stub for doctree.gui.TreePanel
    """
    def getitemtitle(self, arg):
        print(f'called Tree.getitemtitle with arg `{arg}`')
        return 'item title'
    def setitemtitle(self, *args):
        print('called Tree.setitemtitle with args', args)
    def getitemkey(self, arg):
        print(f'called Tree.getitemkey with arg `{arg}`')
        return arg
    def getitemparentpos(self, arg):
        print(f'called Tree.getitemparentpos with arg `{arg}`')
        return 'add_to', 1
    def setitemtext(self, *args):
        print('called Tree.setitemtext with args', args)
    def getitemdata(self, arg):
        print(f'called Tree.getitemdata with arg `{arg}`')
        return 'item data'
    def getitemuserdata(self, arg):
        print(f'called Tree.getitemdata with arg `{arg}`')
        return 'item data'
    def getitemkids(self, arg):
        print(f'called Tree.getitemkids with arg `{arg}`')
        return ['child1', 'child2']
    def getselecteditem(self):
        print('called Tree.getselecteditem')
        return 'selected_item'
    def get_selected_item(self):
        print('called Tree.get_selected_item')
        return ['selected_item']
    def set_item_selected(self, arg):
        print(f'called Tree.set_item_selected with arg `{arg}`')
    def set_item_expanded(self, *args):
        print('called Tree.set_item_expanded with args', args)
    def set_item_collapsed(self, *args):
        print('called Tree.set_item_collapsed with args', args)
    def add_to_parent(self, *args):
        print('called Tree.add_to_parent with args', args)
        return args[1]
    def putsubtree(self, *args, **kwargs):
        print('called Tree.putsubtree with args', args, kwargs)


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
    def select_all(self):
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
        print(f"called Editor.set_contents with arg '{arg}'")
    def get_contents(self):
        print("called Editor.get_contents")
        return 'editor contents'
    def openup(self, value):
        print(f"called Editor.openup with arg '{value}'")
    def get_text_position(self):
        print('called Editor.get_text_position')
        return 9
    def set_text_position(self, arg):
        print(f"called Editor.set_text_position with arg '{arg}'")
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
    def mark_dirty(self, value):
        print(f"called Editor.mark_dirty with arg '{value}'")


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
    def expand_root(self):
        print("called MainGui.expand_root")
    def rebuild_root(self):
        print("called MainGui.rebuild_root")
        return 'new root'
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
            print("called MainGui.check_viewmenu_option")
            return "A New view"
        print(f"called MainGui.check_viewmenu_option with arg '{args[0]}'")
        return None
    def check_next_viewmenu_option(self, **kwargs):
        if not kwargs:
            print("called MainGui.next_check_viewmenu_option")
        else:
            print("called MainGui.check_next_viewmenu_option with args", kwargs)
    def add_escape_action(self):
        print("called MainGui.add_escape_action")
    def remove_escape_action(self):
        print("called MainGui.remove_escape_action")
    def get_screensize(self):
        print("called MainGui.get_screensize")
        return 10, 20
    def get_splitterpos(self):
        print("called MainGui.get_splitterpos")
        return 100
    def find_needle(self, arg):
        print(f"called Gui.find_needle with arg '{arg}'")
        return 'needle'
    def goto_searchresult(self, arg):
        print(f"called Gui.goto_searchresult with arg '{arg}'")


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

    def get_add_dest(self, *args, **kwargs):
        """stub for MainWindow.get_add_dest
        """
        print("called MainWindow.get_add_dest with args", args, kwargs)
        return 'parent', 1

    def get_copy_item(self, *args, **kwargs):
        """stub for MainWindow.get_copy_item
        """
        print("called MainWindow.get_copy_item with args", args, kwargs)

    def put_paste_item(self, *args, **kwargs):
        """stub for MainWindow.put_paste_item
        """
        print("called MainWindow.put_paste_item with args", args, kwargs)

    def remove(self, *args):
        """stub for MainWindow.remove_item_from_view
        """
        print("called MainWindow.remove_item_from_view with args", args)

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

    def ask_title_3(self, *args):
        """stub for MainWindow.ask_title: not canceled
        """
        print('called MainWindow.ask_title with args', args)
        return ('xx', [])

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


def test_init_opts():
    """unittest for main.init_opts
    """
    assert testee.init_opts() == {
            "Application": "DocTree", "NotifyOnSave": True, 'NotifyOnLoad': True,
            "AskBeforeHide": True, "EscapeClosesApp": True, "SashPosition": (180, 0),
            "ScreenSize": (800, 500), "ActiveItem": [0], "ActiveView": 0, "ViewNames": ["Default"],
            "RootTitle": "MyNotes", "RootData": "", "ImageCount": 0}


def test_add_newitems():
    """unittest for main.add_newitems
    """
    cut_from_itemdict = [(2, ('2', 'xx')), (3, ('3', 'xxx'))]
    itemdict = {1: ('1', 'x'), 2: ('2', 'xx'), 4: ('4', 'xxxx')}
    assert testee.add_newitems(cut_from_itemdict, itemdict) == (
            {1: ('1', 'x'), 2: ('2', 'xx'), 4: ('4', 'xxxx'), 5: ('2', 'xx'), 6: ('3', 'xxx')},
            {2: 5, 3: 6})
    itemdict = {}
    assert testee.add_newitems(cut_from_itemdict, itemdict) == (
            {0: ('2', 'xx'), 1: ('3', 'xxx')}, {2: 0, 3: 1})


def test_replace_keys():
    """unittest for main.replace_keys
    """
    assert testee.replace_keys((1, 1, [(2, 2, []), (3, 3, [])]), {1: 6, 2: 4, 3: 5}) == (
            (1, 6, [(2, 4, []), (3, 5, [])]))


def test_add_item_to_view():
    """unittest for main.add_item_to_view
    """
    view = []
    testee.add_item_to_view((1, 1, [(2, 2, [(4, 4, [])]), (3, 3, [])]), view)
    assert view == [(1, [(2, [(4, [])]), (3, [])])]


def test_add_subitem_to_view():
    """unittest for main.add_subitem_to_view
    """
    view = [(1, [(2, [(4, [])]), (3, [])])]
    assert testee.add_subitem_to_view(view, 4, (5, [])) == 'Stop'
    assert view == [(1, [(2, [(4, [(5, [])])]), (3, [])])]


def test_remove_item_from_view():
    """unittest for main.remove_item_from_view
    """
    view = [(1, [(2, [(4, [])]), (3, [])])]
    assert testee.remove_item_from_view(view, (4, []))
    assert view == [(1, [(2, []), (3, [])])]
    view = [(1, [(2, [(4, [])]), (3, [])])]
    assert testee.remove_item_from_view(view, (2, []))
    assert view == [(1, [(4, []), (3, [])])]
    # dit klopt toch niet; 4 zou toch ook verwijderd moeten zijn?
    view = [(1, [(2, [(4, [])]), (3, [])])]
    assert testee.remove_item_from_view(view, (2, [(4, ())]))
    assert view == [(1, [(4, []), (3, [])])]


def test_reset_toolkit_file_if_needed(monkeypatch, tmp_path):
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
        monkeypatch.setattr(testee.MainWindow, 'read', self.mocker.read_error)
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
        for items in menudata:
            for item in items[1]:
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
                "called Editor.set_contents with arg 'root data'\n"
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
                "called Editor.set_contents with arg 'root data'\n"
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
        testobj.confirm = self.mocker.confirm
        testobj.reread()
        assert capsys.readouterr().out == "called MainWindow.handle_save_needed\n"
        testobj.handle_save_needed = self.mocker.handle_2
        testobj.reread()
        assert capsys.readouterr().out == (
                "called MainWindow.handle_save_needed\n"
                "called MainWindow.read\n"
                "called MainWindow.confirm with args"
                " () {'setting': 'NotifyOnLoad', 'textitem': 'test.trd herlezen'}\n"
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

    def test_do_addaction(self, monkeypatch, capsys):
        """unittest for MainWindow.do_addaction
        """
        monkeypatch.setattr(testee.MainWindow, 'set_project_dirty', self.mocker.set_dirty)
        monkeypatch.setattr(testee.MainWindow, 'get_add_dest', self.mocker.get_add_dest)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemdict = {0: 'x', 1: 'y', 3: 'z'}
        testobj.views = [[(0, [(1, []), (3, [])])], [(0, []), (1, []), (3, [])]]
        testobj.opts = {'ActiveView': 0}
        testobj.gui.root = 'gui root'
        assert testobj.do_addaction('root', 'under', 'origpos', 'new_title', []) == (
                4, [], 'new_title', [])
        assert capsys.readouterr().out == (
                "called MainWindow.get_add_dest with args ('root', 'under', 'origpos') {}\n"
                "called Tree.add_to_parent with args (4, 'new_title', 'parent', 1)\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called Tree.set_item_expanded with args ('parent',)\n"
                "called Tree.set_item_selected with arg `new_title`\n"
                "called MainGui.set_focus_to_editor\n")
        testobj.itemdict = {0: 'x', 1: 'y', 3: 'z'}
        testobj.views = [[(0, [(1, []), (3, [])])], [(0, []), (1, []), (3, [])]]
        assert testobj.do_addaction('root', 'under', 'origpos', 'new_title', ['extra', 'titles']) == (
                4, [5, 6], 'new_title', [(5, [(6, [])])])
        assert capsys.readouterr().out == (
                "called MainWindow.get_add_dest with args ('root', 'under', 'origpos') {}\n"
                "called Tree.add_to_parent with args (4, 'new_title', 'parent', 1)\n"
                "called Tree.add_to_parent with args (5, 'extra', 'new_title')\n"
                "called Tree.add_to_parent with args (6, 'titles', 'extra')\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called Tree.set_item_expanded with args ('parent',)\n"
                "called Tree.set_item_selected with arg `titles`\n"
                "called MainGui.set_focus_to_editor\n")

    def test_get_add_dest(self, monkeypatch, capsys):
        """unittest for MainWindow.get_add_dest
        """
        def mock_get_above(item):
            print(f'called item.getitemparentpos with arg {item}')
            return 'parent', 1
        def mock_get_above_2(item):
            print(f'called item.getitemparentpos with arg {item}')
            return 'parent', 2
        def mock_get_under(item):
            print(f'called item.getitemkids with arg {item}')
            return ['a', 'b']
        assert capsys.readouterr().out == ("")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.activeitem = None
        testobj.gui.root = 'gui_root'
        testobj.gui.tree.getitemparentpos = mock_get_above
        testobj.gui.tree.getitemkids = mock_get_under
        assert testobj.get_add_dest(None, True, 1) == ('gui_root', -1)
        assert capsys.readouterr().out == ("")
        testobj.activeitem = 'item_x'
        assert testobj.get_add_dest(None, False, -1) == ('parent', -1)
        assert capsys.readouterr().out == ("called item.getitemparentpos with arg item_x\n"
                                           "called item.getitemkids with arg parent\n")
        item = 'item_y'
        testobj.gui.tree.getitemparentpos = mock_get_above_2
        assert testobj.get_add_dest(item, False, -1) == ('parent', 3)
        assert capsys.readouterr().out == ("called item.getitemparentpos with arg item_y\n"
                                           "called item.getitemkids with arg parent\n")
        assert testobj.get_add_dest(item, False, 1) == ('parent', 1)
        assert capsys.readouterr().out == "called item.getitemparentpos with arg item_y\n"

    def test_rename_item(self, monkeypatch, capsys):
        """unittest fo?r MainWindow.rename_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemdict = {0: ('x', 'xxx'), 1: ('y', 'yyy'), 2: ('z', 'zzz')}
        testobj.views = [[(0, [(1, []), (2, [])])], [(0, []), (1, []), (2, [])]]
        testobj.opts = {'ActiveView': 0, 'RootTitle': '...'}
        testobj.gui.root = 'gui root'
        testobj.activeitem = 1
        testobj.check_active = self.mocker.check
        testobj.set_project_dirty = self.mocker.set_dirty
        testobj.ask_title = self.mocker.ask_title
        testobj.rename_item()
        assert testobj.opts['RootTitle'] == '...'
        assert capsys.readouterr().out == (
                "called MainWindow.check_active\n"
                "called Tree.getitemtitle with arg `1`\n"
                "called MainWindow.ask_title with args"
                " ('Nieuwe titel voor het huidige item:', 'item title')\n")

        testobj.ask_title = self.mocker.ask_title_3
        testobj.rename_item()
        assert testobj.opts['RootTitle'] == '...'
        assert capsys.readouterr().out == (
                "called MainWindow.check_active\n"
                "called Tree.getitemtitle with arg `1`\n"
                "called MainWindow.ask_title with args"
                " ('Nieuwe titel voor het huidige item:', 'item title')\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called Tree.setitemtitle with args (1, 'xx')\n"
                "called Tree.getitemkey with arg `1`\n"
                "called Tree.set_item_selected with arg `1`\n")

        testobj.ask_title = self.mocker.ask_title_3
        testobj.gui.root = 1
        testobj.rename_item()
        assert testobj.opts['RootTitle'] == 'xx'
        assert capsys.readouterr().out == (
                "called MainWindow.check_active\n"
                "called Tree.getitemtitle with arg `1`\n"
                "called MainWindow.ask_title with args"
                " ('Nieuwe titel voor het huidige item:', 'item title')\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called Tree.setitemtitle with args (1, 'xx')\n")

        testobj.ask_title = self.mocker.ask_title_2
        testobj.gui.root = 'gui root'
        testobj.rename_item()
        assert capsys.readouterr().out == (
                "called MainWindow.check_active\n"
                "called Tree.getitemtitle with arg `1`\n"
                "called MainWindow.ask_title with args"
                " ('Nieuwe titel voor het huidige item:', 'item title')\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called Tree.setitemtitle with args (1, 'xx')\n"
                "called Tree.getitemkey with arg `1`\n"
                "called Tree.add_to_parent with args (3, 'yyy', 1)\n"
                "called Tree.add_to_parent with args (4, 'zzz', 'yyy')\n"
                "called Tree.set_item_expanded with args (1,)\n"
                "called Tree.set_item_selected with arg `zzz`\n")

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

    def test_do_copyaction(self, monkeypatch, capsys):
        """unittest for MainWindow.do_copyaction
        """
        def mock_get(arg):
            print(f'called Tree.getsubtree with arg {arg}')
            return 'x', ['1', '2']
        def mock_remove(*args):
            print('called Tree.removeitem wth args', args)
            return 'old loc', 'prev'
        def mock_get_key(arg):
            print(f'called Tree.getitemkey with arg {arg}')
            return 'itemkey'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemdict = {1: ('y', 'yy'), 2: ('z', 'zz'), 3: ('q', 'qq')}
        testobj.gui.tree.getsubtree = mock_get
        testobj.set_project_dirty = self.mocker.set_dirty
        testobj.opts = {'ActiveItem': [1, 3], 'ActiveView': 1}
        testobj.views = [(0, [(1, [(2, [])]), (3, [])]), (0, [(1, []), (2, []), (3, [])])]
        testobj.copied_item = ''
        testobj.cut_from_itemdict = []
        testobj.activeitem = 'x'
        assert testobj.do_copyaction(False, True, 'current') == ('x', None, [(1, ('y', 'yy')),
                                                                             (2, ('z', 'zz'))])
        assert testobj.copied_item == 'x'
        assert testobj.cut_from_itemdict == [(1, ('y', 'yy')), (2, ('z', 'zz'))]
        assert testobj.add_node_on_paste
        assert testobj.activeitem == 'x'
        assert capsys.readouterr().out == "called Tree.getsubtree with arg current\n"

        testobj.copied_item = ''
        testobj.cut_from_itemdict = []
        testobj.activeitem = 'x'
        testobj.gui.tree.removeitem = mock_remove
        testobj.gui.tree.getitemkey = mock_get_key
        testee.remove_item_from_view = self.mocker.remove
        assert testobj.do_copyaction(True, False, 'current') == ('x', 'old loc', [(1, ('y', 'yy')),
                                                                                  (2, ('z', 'zz'))])
        assert testobj.copied_item == ''
        assert testobj.cut_from_itemdict == []
        assert not testobj.add_node_on_paste
        assert testobj.activeitem is None
        assert testobj.opts['ActiveItem'] == ['itemkey', 3]
        assert capsys.readouterr().out == ("called Tree.getsubtree with arg current\n"
                                           "called Tree.removeitem wth args"
                                           " ('current', [(1, ('y', 'yy')), (2, ('z', 'zz'))])\n"
                                           "called Tree.getitemkey with arg prev\n"
                                           "called MainWindow.remove_item_from_view with args"
                                           " ((0, [(1, [(2, [])]), (3, [])]), [1, 2])\n"
                                           "called MainWindow.set_project_dirty with arg True\n"
                                           "called Tree.set_item_selected with arg `prev`\n")

        testobj.copied_item = ''
        testobj.cut_from_itemdict = []
        testobj.activeitem = 'x'
        assert testobj.do_copyaction(True, True, 'current') == ('x', 'old loc', [(1, ('y', 'yy')),
                                                                                 (2, ('z', 'zz'))])
        assert testobj.copied_item == 'x'
        assert testobj.cut_from_itemdict == [(1, ('y', 'yy')), (2, ('z', 'zz'))]
        assert not testobj.add_node_on_paste
        assert testobj.activeitem is None
        assert testobj.opts['ActiveItem'] == ['itemkey', 3]
        assert capsys.readouterr().out == ("called Tree.getsubtree with arg current\n"
                                           "called Tree.removeitem wth args"
                                           " ('current', [(1, ('y', 'yy')), (2, ('z', 'zz'))])\n"
                                           "called MainWindow.remove_item_from_view with args"
                                           " ((0, [(1, [(2, [])]), (3, [])]), [1, 2])\n"
                                           "called MainWindow.set_project_dirty with arg True\n"
                                           "called Tree.set_item_selected with arg `prev`\n")

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

    def test_do_pasteaction(self, monkeypatch, capsys):
        """unittest for MainWindow.do_pasteitem
        """
        def mock_add_back():
            print('called MainWindow.add_items_back')
            return []
        def mock_add_new(*args):
            print('called add_newitems with args', args)
            return {}, {}
        def mock_replace(*args):
            print('called replace_keys with args', args)
            return ('pasted', 'item')
        def mock_add_item(*args):
            print('called add_item_to_view with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_node_on_paste = True
        testobj.copied_item = ''
        testobj.cut_from_itemdict = [(1, ('y', 'yy')), (2, ('z', 'zz'))]
        testobj.itemdict = {0: ('x', 'xx'), 1: ('y', 'yy'), 3: ('z', 'zz')}
        testobj.views = [[(0, [(1, []), (3, [])])], [(0, []), (1, []), (3, [])]]
        testobj.opts = {'ActiveView': 1}
        testobj.add_items_back = mock_add_back
        testobj.set_project_dirty = self.mocker.set_dirty
        monkeypatch.setattr(testee, 'add_newitems', mock_add_new)
        monkeypatch.setattr(testee, 'replace_keys', mock_replace)
        monkeypatch.setattr(testee, 'add_item_to_view', mock_add_item)
        assert testobj.do_pasteaction(True, False, 'current') == ([], ('add_to', 1))
        assert capsys.readouterr().out == (
                "called add_newitems with args ([(1, ('y', 'yy')), (2, ('z', 'zz'))],"
                " {0: ('x', 'xx'), 1: ('y', 'yy'), 3: ('z', 'zz')})\n"
                "called replace_keys with args ('', {})\n"
                "called Tree.getitemparentpos with arg `current`\n"
                "called Tree.putsubtree with args ('add_to', 'pasted', 'item') {'pos': 1}\n"
                "called add_item_to_view with args (('pasted', 'item'), [(0, [(1, []), (3, [])])])\n"
                "called MainWindow.set_project_dirty with arg True\n"
                "called Tree.set_item_expanded with args ('current',)\n"
                "called Tree.set_item_selected with arg `current`\n")

        testobj.add_node_on_paste = False
        assert testobj.do_pasteaction(False, True, 'current') == ([], ('current', -1))
        assert capsys.readouterr().out == ("called MainWindow.add_items_back\n"
                                           "called Tree.putsubtree with args ('current',) {}\n"
                                           "called MainWindow.set_project_dirty with arg True\n"
                                           "called Tree.set_item_expanded with args ('current',)\n"
                                           "called Tree.set_item_selected with arg `current`\n")

        testobj.add_node_on_paste = False
        assert testobj.do_pasteaction(True, True, 'current') == ([], ('current', -1))
        assert capsys.readouterr().out == ("called MainWindow.add_items_back\n"
                                           "called Tree.putsubtree with args ('current',) {}\n"
                                           "called MainWindow.set_project_dirty with arg True\n"
                                           "called Tree.set_item_expanded with args ('current',)\n"
                                           "called Tree.set_item_selected with arg `current`\n")

        testobj.add_node_on_paste = False
        assert testobj.do_pasteaction(False, False, 'current') == ([], ('add_to', 2))
        assert capsys.readouterr().out == ("called MainWindow.add_items_back\n"
                                           "called Tree.getitemparentpos with arg `current`\n"
                                           "called Tree.putsubtree with args ('add_to',) {'pos': 2}\n"
                                           "called MainWindow.set_project_dirty with arg True\n"
                                           "called Tree.set_item_expanded with args ('current',)\n"
                                           "called Tree.set_item_selected with arg `current`\n")

    def test_add_items_back(self, monkeypatch, capsys):
        """unittest for MainWindow.add_items_back
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemdict = {1: ('x', 'xx')}
        testobj.cut_from_itemdict = [(2, ('y', 'yy'))]
        assert testobj.add_items_back() == [2]
        assert testobj.itemdict == {1: ('x', 'xx'), 2: ('y', 'yy')}

    def test_move_to_file(self, monkeypatch, capsys):
        """unittest for MainWindow.move_to_file
        """
        def mock_get_same_filename(*args, **kwargs):
            """stub for Doctree.gui.get_filename: dialog was accepted
            """
            print('called gui.get_filename with args', args, kwargs)
            return True, 'path/to/data.trd'
        def mock_read(*args, **kwargs):
            print("called MainWindow.read with args", args, kwargs)
            return ('read error',)
        def mock_read_2(*args, **kwargs):
            print("called MainWindow.read with args", args, kwargs)
            return {'opts': 'dict'}, ['views', 'list'], {'item': 'dict'}, {'text': 'positions'}
        def mock_verify(*args, **kwargs):
            print('called dml.verify_imagenames with args', args, kwargs)
            return {'cut': ('from', 'itemdict')}, ['images']
        def mock_write(*args, **kwargs):
            print('called dml.write_to_files with args', args, kwargs)
        def mock_init():
            print('called Editor.init_opts')
            return {}
        def mock_add_newitems(*args):
            print('called add_newitems with args', args)
            return {'item': 'dict'}, {1: 4, 2: 5}
        def mock_replace(*args):
            print('called replace_keys with args', args)
            return ['new', 'copied', 'item']
        def mock_add_item(*args):
            print('called add_item_to_view with args', args)
        monkeypatch.setattr(testee, 'init_opts', mock_init)
        monkeypatch.setattr(testee, 'add_newitems', mock_add_newitems)
        monkeypatch.setattr(testee, 'replace_keys', mock_replace)
        monkeypatch.setattr(testee, 'add_item_to_view', mock_add_item)
        monkeypatch.setattr(testee.dml, 'verify_imagenames', mock_verify)
        monkeypatch.setattr(testee.dml, 'write_to_files', mock_write)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        monkeypatch.setattr(testee.gui, 'get_filename', mock_get_filename)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = testee.pathlib.Path('path/to/data.trd')
        testobj.temp_imagepath = testee.pathlib.Path('/tmp/path/to/imagefiles')
        testobj.images_embedded = False
        testobj.copied_item = 'copied item'
        testobj.opts = {'Version': 'xx'}
        testobj.cut_from_itemdict = [('copied', 'items')]
        testobj.text_positions = {1: 1, 2: 2}
        testobj.get_copy_item = self.mocker.get_copy_item
        testobj.read = mock_read

        testobj.gui.root = 'selected_item'
        testobj.move_to_file()
        assert capsys.readouterr().out == (
                "called Tree.getselecteditem\n"
                f'called gui.show_message with args ({testobj.gui}, "Can\'t do this with root")\n')

        testobj.gui.root = 'gui root'
        testobj.move_to_file()
        assert capsys.readouterr().out == (
                "called Tree.getselecteditem\n"
                f"called gui.get_filename with args ({testobj.gui},"
                " 'DocTree - choose file to move the item to', 'path/to') {}\n")

        monkeypatch.setattr(testee.gui, 'get_filename', mock_get_same_filename)
        testobj.move_to_file()
        assert capsys.readouterr().out == (
                "called Tree.getselecteditem\n"
                f"called gui.get_filename with args ({testobj.gui},"
                " 'DocTree - choose file to move the item to', 'path/to') {}\n"
                f"called gui.show_message with args ({testobj.gui},"
                " 'Destination file is the same as origin file')\n")

        monkeypatch.setattr(testee.gui, 'get_filename', mock_get_filename_2)
        monkeypatch.setattr(testee.pathlib.Path, 'exists', lambda x: False)
        testobj.move_to_file()
        assert capsys.readouterr().out == (
                "called Tree.getselecteditem\n"
                f"called gui.get_filename with args ({testobj.gui},"
                " 'DocTree - choose file to move the item to', 'path/to') {}\n"
                "called Editor.init_opts\n"
                "called MainWindow.get_copy_item with args"
                " () {'cut': True, 'to_other_file': 'selected_item'}\n"
                "called dml.verify_imagenames with args ([('copied', 'items')],"
                " PosixPath('/tmp/path/to/imagefiles'), PosixPath('newname.trd')) {}\n"
                "called add_newitems with args ({'cut': ('from', 'itemdict')}, {})\n"
                "called replace_keys with args ('copied item', {1: 4, 2: 5})\n"
                "called add_item_to_view with args (['new', 'copied', 'item'], [])\n"
                "called dml.write_to_files with args (PosixPath('newname.trd'),"
                " {'Version': 'xx'}, [[]], {'item': 'dict'}, {4: 1, 5: 2},"
                " PosixPath('/tmp/path/to/imagefiles'), ['images']) {'save_images': True}\n")

        monkeypatch.setattr(testee.gui, 'get_filename', mock_get_filename_2)
        monkeypatch.setattr(testee.pathlib.Path, 'exists', lambda x: True)
        testobj.images_embedded = True
        testobj.move_to_file()
        assert capsys.readouterr().out == (
                "called Tree.getselecteditem\n"
                f"called gui.get_filename with args ({testobj.gui},"
                " 'DocTree - choose file to move the item to', 'path/to') {}\n"
                "called MainWindow.read with args () {'other_file': PosixPath('newname.trd')}\n"
                f"called gui.show_message with args ({testobj.gui}, 'read error')\n")

        testobj.read = mock_read_2
        testobj.images_embedded = True
        testobj.text_positions = {1: 1, 2: 2}
        testobj.move_to_file()
        assert capsys.readouterr().out == (
                "called Tree.getselecteditem\n"
                f"called gui.get_filename with args ({testobj.gui},"
                " 'DocTree - choose file to move the item to', 'path/to') {}\n"
                "called MainWindow.read with args () {'other_file': PosixPath('newname.trd')}\n"
                "called MainWindow.get_copy_item with args"
                " () {'cut': True, 'to_other_file': 'selected_item'}\n"
                "called add_newitems with args ({'cut': ('from', 'itemdict')}, {'item': 'dict'})\n"
                "called replace_keys with args ('copied item', {1: 4, 2: 5})\n"
                "called add_item_to_view with args (['new', 'copied', 'item'], 'views')\n"
                "called add_item_to_view with args (['new', 'copied', 'item'], 'list')\n"
                "called dml.write_to_files with args (PosixPath('newname.trd'),"
                " {'opts': 'dict'}, ['views', 'list'], {'item': 'dict'}, {4: 1, 5: 2},"
                " PosixPath('/tmp/path/to/imagefiles'), []) {'save_images': False}\n")

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
        def mock_search_from_3(self, *args):
            print('called MainWindow.search_from with args', args)
            self.gui.srchlist = True
            return ['result', 'list']
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
        monkeypatch.setattr(testee.MainWindow, 'search_from', mock_search_from_3)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog_2)
        monkeypatch.setattr(testee.gui, 'show_nonmodal', mock_show_nonmodal)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = 'gui root'
        testobj.gui.srchlist = False
        testobj.gui.srchtype = 1
        testobj.search()
        assert testobj.gui.srchlist
        assert capsys.readouterr().out == (
                "called gui.show_dialog with args"
                f" ({testobj.gui}, <class 'doctree.qtgui.SearchDialog'>)\n"
                "called MainWindow.search_from with args ('gui root',)\n"
                f"called gui.show_nonmodal with args ({testobj.gui}, {testee.gui.ResultsDialog})\n")

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

    def test_search_from(self, monkeypatch, capsys):
        """unittest for MainWindow.search_from
        """
        def mock_getitemkids(arg):
            print(f"called Tree.getitemkids with arg '{arg}'")
            if arg == 'parent':
                return ['child1', 'child2']
            if arg == 'child1':
                return ['child3']
            return []
        def mock_getitemtitle(arg):
            print(f'called Tree.getitemtitle with arg `{arg}`')
            return f'{arg} title'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.getitemkids = mock_getitemkids
        testobj.gui.tree.getitemtitle = mock_getitemtitle
        # testobj.first_title = 'first'
        testobj.gui.srchtype = 1
        assert testobj.search_from('parent') == [([0], 'title', 'child1 title', 'child1 title'),
                                                 ([0, 0], 'title', 'child1 title', 'child3 title'),
                                                 ([1], 'title', 'child2 title', 'child2 title')]
        assert capsys.readouterr().out == ("called Tree.getitemkids with arg 'parent'\n"
                                           "called Tree.getitemtitle with arg `child1`\n"
                                           "called Tree.getitemdata with arg `child1`\n"
                                           "called Gui.find_needle with arg 'child1 title'\n"
                                           "called Tree.getitemkids with arg 'child1'\n"
                                           "called Tree.getitemtitle with arg `child3`\n"
                                           "called Tree.getitemdata with arg `child3`\n"
                                           "called Gui.find_needle with arg 'child3 title'\n"
                                           "called Tree.getitemkids with arg 'child3'\n"
                                           "called Tree.getitemtitle with arg `child2`\n"
                                           "called Tree.getitemdata with arg `child2`\n"
                                           "called Gui.find_needle with arg 'child2 title'\n"
                                           "called Tree.getitemkids with arg 'child2'\n")
        testobj.gui.srchtype = 2
        assert testobj.search_from('parent') == [([0], 'text', 'child1 title', 'child1 title'),
                                                 ([0, 0], 'text', 'child1 title', 'child3 title'),
                                                 ([1], 'text', 'child2 title', 'child2 title')]
        assert capsys.readouterr().out == ("called Tree.getitemkids with arg 'parent'\n"
                                           "called Tree.getitemtitle with arg `child1`\n"
                                           "called Tree.getitemdata with arg `child1`\n"
                                           "called Gui.find_needle with arg 'item data'\n"
                                           "called Tree.getitemkids with arg 'child1'\n"
                                           "called Tree.getitemtitle with arg `child3`\n"
                                           "called Tree.getitemdata with arg `child3`\n"
                                           "called Gui.find_needle with arg 'item data'\n"
                                           "called Tree.getitemkids with arg 'child3'\n"
                                           "called Tree.getitemtitle with arg `child2`\n"
                                           "called Tree.getitemdata with arg `child2`\n"
                                           "called Gui.find_needle with arg 'item data'\n"
                                           "called Tree.getitemkids with arg 'child2'\n")
        testobj.gui.srchtype = 3
        assert testobj.search_from('parent') == [([0], 'title', 'child1 title', 'child1 title'),
                                                 ([0], 'text', 'child1 title', 'child1 title'),
                                                 ([0, 0], 'title', 'child1 title', 'child3 title'),
                                                 ([0, 0], 'text', 'child1 title', 'child3 title'),
                                                 ([1], 'title', 'child2 title', 'child2 title'),
                                                 ([1], 'text', 'child2 title', 'child2 title')]
        assert capsys.readouterr().out == ("called Tree.getitemkids with arg 'parent'\n"
                                           "called Tree.getitemtitle with arg `child1`\n"
                                           "called Tree.getitemdata with arg `child1`\n"
                                           "called Gui.find_needle with arg 'child1 title'\n"
                                           "called Gui.find_needle with arg 'item data'\n"
                                           "called Tree.getitemkids with arg 'child1'\n"
                                           "called Tree.getitemtitle with arg `child3`\n"
                                           "called Tree.getitemdata with arg `child3`\n"
                                           "called Gui.find_needle with arg 'child3 title'\n"
                                           "called Gui.find_needle with arg 'item data'\n"
                                           "called Tree.getitemkids with arg 'child3'\n"
                                           "called Tree.getitemtitle with arg `child2`\n"
                                           "called Tree.getitemdata with arg `child2`\n"
                                           "called Gui.find_needle with arg 'child2 title'\n"
                                           "called Gui.find_needle with arg 'item data'\n"
                                           "called Tree.getitemkids with arg 'child2'\n")

    def test_go_to_result(self, monkeypatch, capsys):
        """unittest for MainWindow.go_to_result
        """
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.search_results = [['x'], ['y'], ['z']]
        testobj.gui.srchwrap = False
        testobj.srchno = 0
        testobj.go_to_result()
        assert testobj.srchno == 0
        assert capsys.readouterr().out == "called Gui.goto_searchresult with arg 'x'\n"
        testobj.srchno = -1
        testobj.go_to_result()
        assert testobj.srchno == 0
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'No prior result')\n")
        testobj.gui.srchwrap = True
        testobj.srchno = -1
        testobj.go_to_result()
        assert testobj.srchno == 2
        assert capsys.readouterr().out == "called Gui.goto_searchresult with arg 'z'\n"
        testobj.gui.srchwrap = False
        testobj.srchno = 2
        testobj.go_to_result()
        assert testobj.srchno == 2
        assert capsys.readouterr().out == ("called Gui.goto_searchresult with arg 'z'\n")
        testobj.srchno = 3
        testobj.go_to_result()
        assert testobj.srchno == 2
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'No next result')\n")
        testobj.gui.srchwrap = True
        testobj.srchno = 3
        testobj.go_to_result()
        assert testobj.srchno == 0
        assert capsys.readouterr().out == ("called Gui.goto_searchresult with arg 'x'\n")

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

    def test_treetoview(self, monkeypatch, capsys):
        """unittest for MainWindow.treetoview
        """
        counter = 0
        def mock_getitemkids(arg):
            nonlocal counter
            print(f"called Tree.getitemkids with arg '{arg}'")
            counter += 1
            if counter == 1:
                return ['child1', 'child2']
            return []
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.tree.getitemkids = mock_getitemkids
        testobj.opts = {'ActiveItem': ['', ''], 'ActiveView': 1}
        testobj.activeitem = 'child1'
        testobj.gui.root = 'xxx'
        assert testobj.treetoview() == [('child1', []), ('child2', [])]
        assert testobj.opts == {'ActiveItem': ['', 'child1'], 'ActiveView': 1}
        assert capsys.readouterr().out == ("called Tree.getitemkids with arg 'xxx'\n"
                                           "called Tree.getitemkey with arg `child1`\n"
                                           "called Tree.getitemkids with arg 'child1'\n"
                                           "called Tree.getitemkey with arg `child2`\n"
                                           "called Tree.getitemkids with arg 'child2'\n")

    def test_viewtotree(self, monkeypatch, capsys):
        """unittest for MainWindow.viewtotree
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemdict = {1: ('x', 'xxx'), 2: ('y', 'yyy'), 3: ('z', 'zzz')}
        testobj.gui.root = 'gui root'
        testobj.opts = {'ActiveItem': ['child1', ''], 'ActiveView': 1}
        testobj.views = [[(1,
                           [(2, None),
                            (3, [])])],
                         [(3,
                           [(1, []),
                            (2, None)])]]
        assert testobj.viewtotree() is None
        assert capsys.readouterr().out == (
                "called Tree.add_to_parent with args (3, 'z', 'gui root')\n"
                "called Tree.add_to_parent with args (1, 'x', 'z')\n"
                "called Tree.add_to_parent with args (2, 'y', 'z')\n")
        testobj.opts = {'ActiveItem': [2, 1], 'ActiveView': 1}
        assert testobj.viewtotree() == 'x'
        assert capsys.readouterr().out == (
                "called Tree.add_to_parent with args (3, 'z', 'gui root')\n"
                "called Tree.add_to_parent with args (1, 'x', 'z')\n"
                "called Tree.add_to_parent with args (2, 'y', 'z')\n")

    def test_check_active(self, monkeypatch, capsys):
        """unittest for MainWindow.check_active
        """
        def mock_getitemkey(arg):
            print(f'called Tree.getitemkey with arg `{arg}`')
            return 1
        def mock_getitemkey_2(arg):
            print(f'called Tree.getitemkey with arg `{arg}`')
            return -1
        def check_2():
            print('called Editor.check_dirty')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_project_dirty = self.mocker.set_dirty
        testobj.gui.tree.getitemkey = mock_getitemkey
        testobj.activeitem = None
        testobj.gui.root = 'gui root'
        testobj.check_active()
        assert capsys.readouterr().out == ""

        testobj.opts = {'RootData': 'root data'}
        testobj.itemdict = {1: ('item title', 'item text')}
        testobj.text_positions = [0, 1]
        testobj.activeitem = 'active item'
        testobj.check_active()
        assert capsys.readouterr().out == ("called Tree.getitemtitle with arg `active item`\n"
                                           "called Tree.getitemkey with arg `active item`\n"
                                           "called Editor.get_text_position\n"
                                           "called Editor.check_dirty\n")
        testobj.gui.editor.check_dirty = check_2
        testobj.check_active()
        assert capsys.readouterr().out == ("called Tree.getitemtitle with arg `active item`\n"
                                           "called Tree.getitemkey with arg `active item`\n"
                                           "called Editor.get_text_position\n"
                                           "called Editor.check_dirty\n"
                                           "called Editor.get_contents\n"
                                           "called Editor.mark_dirty with arg 'False'\n"
                                           "called MainWindow.set_project_dirty with arg True\n")
        testobj.gui.tree.getitemkey = mock_getitemkey_2
        testobj.check_active()
        assert testobj.opts['RootData'] == 'editor contents'
        assert capsys.readouterr().out == (
                "called Tree.getitemtitle with arg `active item`\n"
                "called Tree.getitemkey with arg `active item`\n"
                "called Editor.get_text_position\n"
                "called Editor.check_dirty\n"
                "called Editor.get_contents\n"
                "called Tree.setitemtext with args ('gui root', 'editor contents')\n"
                "called Editor.mark_dirty with arg 'False'\n"
                "called MainWindow.set_project_dirty with arg True\n")

    def test_activate_item(self, monkeypatch, capsys):
        """unittest for MainWindow.activate_item
        """
        def mock_getitemkey(arg):
            print(f'called Tree.getitemkey with arg `{arg}`')
            return 1
        def mock_getitemkey_2(arg):
            print(f'called Tree.getitemkey with arg `{arg}`')
            return -1
        def mock_set(arg):
            print(f"called Editor.set_text_position with arg '{arg}'")
            raise KeyError
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {'RootData': 'root data'}
        testobj.itemdict = {1: ('item title', 'item text')}
        testobj.text_positions = [0, 1]
        testobj.gui.tree.getitemkey = mock_getitemkey
        testobj.activate_item('item')
        assert capsys.readouterr().out == ("called Tree.getitemkey with arg `item`\n"
                                           "called Editor.set_text_position with arg '1'\n"
                                           "called Editor.set_contents with arg 'item text'\n"
                                           "called Editor.openup with arg 'True'\n")
        testobj.gui.tree.getitemkey = mock_getitemkey_2
        testobj.activate_item('item')
        assert capsys.readouterr().out == ("called Tree.getitemkey with arg `item`\n"
                                           "called Editor.set_contents with arg 'root data'\n"
                                           "called Editor.openup with arg 'True'\n")
        testobj.gui.tree.getitemkey = mock_getitemkey
        testobj.gui.editor.set_text_position = mock_set
        testobj.activate_item('item')
        assert capsys.readouterr().out == ("called Tree.getitemkey with arg `item`\n"
                                           "called Editor.set_text_position with arg '1'\n"
                                           "called Editor.get_text_position\n"
                                           "called Editor.set_contents with arg 'item text'\n"
                                           "called Editor.openup with arg 'True'\n")

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

    def test_read(self, monkeypatch, capsys):
        """unittest for MainWindow.read
        """
        def mock_init():
            print('called Editor.init_opts')
            return {'ImageCount': 0}
        def mock_set_split():
            print('called Editor.set_windowsplit')
        def mock_set_escape():
            print('called Editor.set_escape_action')
        def mock_setup_menu():
            print('called Editor.setup_viewmenu')
        def mock_viewtotree():
            print('called Editor.viewtotree')
            return 'item to activate'
        def mock_viewtotree_2():
            print('called Editor.viewtotree')
            return 'new root'
        def mock_set_dirty(value):
            print(f'called Editor.set_project_dirty with arg {value}')
        def mock_read(*args):
            print('called dml.read_from_files with args', args)
            return ('error',)
        def mock_read_2(*args):
            print('called dml.read_from_files with args', args)
            return ({'RootData': None, 'ScreenSize': (5, 10)}, ['views'], {'item': 'dict'},
                    {'text': 'positions'}, [])
        def mock_read_3(*args):
            print('called dml.read_from_files with args', args)
            return ({'RootData': 'asdf', 'ScreenSize': (5, 10)}, ['views'], {'item': 'dict'},
                    {'text': 'positions'}, ['00005.png'])
        monkeypatch.setattr(testee, 'init_opts', mock_init)
        monkeypatch.setattr(testee.dml, 'read_from_files', mock_read)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = 'xxxx'
        testobj.temp_imagepath = 'yyyy'
        testobj.set_windowsplit = mock_set_split
        testobj.set_escape_action = mock_set_escape
        testobj.setup_viewmenu = mock_setup_menu
        testobj.viewtotree = mock_viewtotree
        testobj.set_project_dirty = mock_set_dirty
        assert testobj.read() == ('error',)
        assert capsys.readouterr().out == (
                "called Editor.init_opts\n"
                "called dml.read_from_files with args ('xxxx', '', 'yyyy')\n")

        monkeypatch.setattr(testee.dml, 'read_from_files', mock_read_2)
        assert testobj.read(other_file='qqqq') == ({'RootData': None, 'ScreenSize': (5, 10)},
                                                   ['views'], {'item': 'dict'}, {'text': 'positions'})
        assert capsys.readouterr().out == (
                "called Editor.init_opts\n"
                "called dml.read_from_files with args ('xxxx', 'qqqq', 'yyyy')\n")

        assert testobj.read() == []
        assert testobj.opts['ImageCount'] == 0
        assert testobj.activeitem is not None
        assert testobj.has_treedata
        assert capsys.readouterr().out == (
                "called Editor.init_opts\n"
                "called dml.read_from_files with args ('xxxx', '', 'yyyy')\n"
                "called MainGui.set_version with args ()\n"
                "called MainGui.set_window_dimensions with args (5, 10)\n"
                "called Editor.set_windowsplit\n"
                "called Editor.set_escape_action\n"
                "called MainGui.rebuild_root\n"
                "called MainGui.init_app\n"
                "called Editor.set_contents with arg ''\n"
                "called Editor.setup_viewmenu\n"
                "called MainGui.set_focus_to_tree\n"
                "called Editor.viewtotree\n"
                "called Editor.set_project_dirty with arg False\n"
                "called MainGui.expand_root\n"
                "called Tree.set_item_selected with arg `item to activate`\n")

        monkeypatch.setattr(testee.dml, 'read_from_files', mock_read_3)
        testobj.viewtotree = mock_viewtotree_2
        assert testobj.read() == []
        assert testobj.opts['ImageCount'] == 5
        assert testobj.activeitem is not None
        assert testobj.has_treedata
        assert capsys.readouterr().out == (
                "called Editor.init_opts\n"
                "called dml.read_from_files with args ('xxxx', '', 'yyyy')\n"
                "called MainGui.set_version with args ()\n"
                "called MainGui.set_window_dimensions with args (5, 10)\n"
                "called Editor.set_windowsplit\n"
                "called Editor.set_escape_action\n"
                "called MainGui.rebuild_root\n"
                "called MainGui.init_app\n"
                "called Editor.set_contents with arg 'asdf'\n"
                "called Editor.setup_viewmenu\n"
                "called MainGui.set_focus_to_tree\n"
                "called Editor.viewtotree\n"
                "called Editor.set_project_dirty with arg False\n"
                "called MainGui.expand_root\n")

    def test_set_windowsplit(self, monkeypatch, capsys):
        """unittest for MainWindow.set_windowsplit
        """
        def mock_set_split(value):
            print(f'called EditorGui.set_window_split with arg {value}')
        def mock_set_split_2(value):
            print(f'called EditorGui.set_window_split with arg {value}')
            raise TypeError
        monkeypatch.setattr(testee.gui, 'show_message', mock_show_message)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.set_window_split = mock_set_split
        testobj.opts = {'SashPosition': 5, 'ScreenSize': (10, 10)}
        testobj.set_windowsplit()
        assert testobj.opts['SashPosition'] == (5, 5)
        assert capsys.readouterr().out == "called EditorGui.set_window_split with arg (5, 5)\n"

        testobj.opts = {'SashPosition': (5,), 'ScreenSize': (10, 10)}
        testobj.set_windowsplit()
        assert testobj.opts['SashPosition'] == (5, 5)
        assert capsys.readouterr().out == "called EditorGui.set_window_split with arg (5, 5)\n"

        testobj.opts = {'SashPosition': (5, 6), 'ScreenSize': (10, 10)}
        testobj.set_windowsplit()
        assert testobj.opts['SashPosition'] == (5, 6)
        assert capsys.readouterr().out == "called EditorGui.set_window_split with arg (5, 6)\n"

        testobj.opts = {'SashPosition': ()}
        testobj.gui.set_window_split = mock_set_split_2
        testobj.set_windowsplit()
        assert testobj.opts['SashPosition'] == ()
        assert capsys.readouterr().out == ("called EditorGui.set_window_split with arg ()\n"
                                           f"called gui.show_message with args ({testobj.gui},"
                                           " 'Ignoring incompatible sash position')\n")

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

    def test_setup_viewmenu(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_viewmenu
        """
        counter = 0
        def mock_add(arg):
            nonlocal counter
            print(f"called MainGui.add_viewmenu_option with arg '{arg}'")
            counter += 1
            return f'action-{counter}'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {'ViewNames': ['a view', 'also a view',], 'ActiveView': 1}
        testobj.gui.add_viewmenu_option = mock_add
        testobj.setup_viewmenu()
        assert capsys.readouterr().out == (
                "called MainGui.clear_viewmenu\n"
                "called MainGui.add_viewmenu_option with arg '&1 a view'\n"
                "called MainGui.add_viewmenu_option with arg '&2 also a view'\n"
                "called MainGui.check_viewmenu_option with arg 'action-2'\n")

    def test_write(self, monkeypatch, capsys):
        """unittest for MainWindow.write
        """
        def mock_write(*args, **kwargs):
            print('called dml.write_to_files with args', args, kwargs)
            return ['images']
        def mock_confirm(**kwargs):
            print("called MainWindow.confirm with args", kwargs)
        monkeypatch.setattr(testee.dml, 'write_to_files', mock_write)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = 'test.trd'
        testobj.opts = {'ActiveView': 1}
        testobj.views = ['', '']
        testobj.itemdict = {1: 'xxx'}
        testobj.text_positions = [1]
        testobj.temp_imagepath = 'path_to_images'
        testobj.images_embedded = False
        testobj.check_active = self.mocker.check
        testobj.treetoview = self.mocker.treetoview
        testobj.set_project_dirty = self.mocker.set_dirty
        testobj.confirm = mock_confirm
        testobj.write()
        assert testobj.opts == {'ActiveView': 1, 'ScreenSize': (10, 20), 'SashPosition': 100}
        assert testobj.views == ['', 'A view']
        assert testobj.imagelist == ['images']
        assert capsys.readouterr().out == (
                "called MainGui.get_screensize\n"
                "called MainGui.get_splitterpos\n"
                "called MainWindow.check_active\n"
                "called MainWindow.treetoview\n"
                "called dml.write_to_files with args"
                " ('test.trd', {'ActiveView': 1, 'ScreenSize': (10, 20), 'SashPosition': 100},"
                " ['', 'A view'], {1: 'xxx'}, [1], 'path_to_images') {'save_images': True}\n"
                "called MainWindow.set_project_dirty with arg False\n"
                "called MainWindow.confirm with args"
                " {'setting': 'NotifyOnSave', 'textitem': 'test.trd is opgeslagen'}\n"
                "called MainGui.show_statusmessage with args ('test.trd is opgeslagen',)\n")
        testobj.write(meld=False)
        assert testobj.opts == {'ActiveView': 1, 'ScreenSize': (10, 20), 'SashPosition': 100}
        assert testobj.views == ['', 'A view']
        assert testobj.imagelist == ['images']
        assert capsys.readouterr().out == (
                "called MainGui.get_screensize\n"
                "called MainGui.get_splitterpos\n"
                "called MainWindow.check_active\n"
                "called MainWindow.treetoview\n"
                "called dml.write_to_files with args"
                " ('test.trd', {'ActiveView': 1, 'ScreenSize': (10, 20), 'SashPosition': 100},"
                " ['', 'A view'], {1: 'xxx'}, [1], 'path_to_images') {'save_images': True}\n"
                "called MainWindow.set_project_dirty with arg False\n"
                "called MainGui.show_statusmessage with args ('test.trd is opgeslagen',)\n")

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
