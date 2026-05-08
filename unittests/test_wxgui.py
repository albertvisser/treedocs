"""unittests for ./doctree/wxgui.py
"""
import pathlib
import types
import pytest
from mockgui import mockwxwidgets as mockwx
from doctree import wxgui as testee
# from output_fixture import expected_output


def test_show_message(monkeypatch, capsys):
    """unittest for wxgui.show_message
    """
    monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
    testee.show_message('win', 'text')
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'text', 'DocTree', 2052) {}\n"
            "called MessageDialog.ShowModal\n")


def test_ask_ynquestion(monkeypatch, capsys):
    """unittest for wxgui.ask_ynquestion
    """
    def mock_show(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_YES
    monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
    assert not testee.ask_ynquestion('win', 'text')
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'text', 'DocTree', 1034) {}\n"
            "called MessageDialog.ShowModal\n")
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show)
    assert testee.ask_ynquestion('win', 'text')
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'text', 'DocTree', 1034) {}\n"
            "called MessageDialog.ShowModal\n")


def test_ask_yncquestion(monkeypatch, capsys):
    """unittest for wxgui.ask_yncquestion
    """
    def mock_show(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_YES
    def mock_show_2(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_CANCEL
    monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
    assert testee.ask_yncquestion('win', 'text') == (False, False)
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'text', 'DocTree', 1050) {}\n"
            "called MessageDialog.ShowModal\n")
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show)
    assert testee.ask_yncquestion('win', 'text') == (True, False)
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'text', 'DocTree', 1050) {}\n"
            "called MessageDialog.ShowModal\n")
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show_2)
    assert testee.ask_yncquestion('win', 'text') == (False, True)
    assert capsys.readouterr().out == (
            "called MessageDialog.__init__ with args ('win', 'text', 'DocTree', 1050) {}\n"
            "called MessageDialog.ShowModal\n")


def test_get_text(monkeypatch, capsys):
    """unittest for wxgui.get_text_
    """
    def mock_show(self):
        print('called TextDialog.ShowModal')
        return testee.wx.ID_OK
    monkeypatch.setattr(testee.wx, 'TextEntryDialog', mockwx.MockTextDialog)
    assert testee.get_text('win', 'caption', 'oldtext') == (False, '')
    assert capsys.readouterr().out == (
            "called TextDialog.__init__ with args ('caption', 'DocTree', 'oldtext') {}\n"
            "called TextDialog.ShowModal\n"
            "called TextDialog.GetValue\n")
    monkeypatch.setattr(mockwx.MockTextDialog, 'ShowModal', mock_show)
    assert testee.get_text('win', 'caption', 'oldtext') == (True, '')
    assert capsys.readouterr().out == (
            "called TextDialog.__init__ with args ('caption', 'DocTree', 'oldtext') {}\n"
            "called TextDialog.ShowModal\n"
            "called TextDialog.GetValue\n")


def test_get_choice(monkeypatch, capsys):
    """unittest for wxgui.get_choice
    """
    def mock_show(self):
        print('called ChoiceDialog.ShowModal')
        return testee.wx.ID_OK
    monkeypatch.setattr(testee.wx, 'SingleChoiceDialog', mockwx.MockChoiceDialog)
    assert testee.get_choice('win', 'caption', ['opt', 'ions'], 'current') == (False,
                                                                               "selected value")
    assert capsys.readouterr().out == (
            "called ChoiceDialog.__init__ with args ('caption', 'DocTree', ['opt', 'ions'])\n"
            "called ChoiceDialog.SetSelection with arg 'current'\n"
            "called ChoiceDialog.ShowModal\n"
            "called ChoiceDialog.GetStringSelection\n")
    monkeypatch.setattr(mockwx.MockChoiceDialog, 'ShowModal', mock_show)
    assert testee.get_choice('win', 'caption', ['opt', 'ions'], 'current') == (True,
                                                                               "selected value")
    assert capsys.readouterr().out == (
            "called ChoiceDialog.__init__ with args ('caption', 'DocTree', ['opt', 'ions'])\n"
            "called ChoiceDialog.SetSelection with arg 'current'\n"
            "called ChoiceDialog.ShowModal\n"
            "called ChoiceDialog.GetStringSelection\n")


def test_get_filename(monkeypatch, capsys):
    """unittest for wxgui.get_filename
    """
    def mock_show(self):
        print('called FileDialog.ShowModal')
        return testee.wx.ID_CANCEL
    monkeypatch.setattr(testee.wx, 'FileDialog', mockwx.MockFileDialog)
    win = types.SimpleNamespace(master=types.SimpleNamespace(FILE_TYPE=('xxx', 'yy')))
    assert testee.get_filename(win, 'title', 'path/to/start') == (True, 'dirname/filename')
    assert capsys.readouterr().out == (
            "called FileDialog.__init__ with args ('title', 'path/to', '', 'xxx (*yy)|*yy', 1) {}\n"
            "called FileDialog.ShowModal\n"
            "called FileDialog.GetDirectory\n"
            "called FileDialog.GetFilename\n")
    assert testee.get_filename(win, 'title', 'path/to/start', save=True) == (True,
                                                                             'dirname/filename')
    assert capsys.readouterr().out == (
            "called FileDialog.__init__ with args ('title', 'path/to', '', 'xxx (*yy)|*yy', 6) {}\n"
            "called FileDialog.ShowModal\n"
            "called FileDialog.GetDirectory\n"
            "called FileDialog.GetFilename\n")
    monkeypatch.setattr(mockwx.MockFileDialog, 'ShowModal', mock_show)
    assert testee.get_filename(win, 'title', 'path/to/start') == (False, '')
    assert capsys.readouterr().out == (
            "called FileDialog.__init__ with args ('title', 'path/to', '', 'xxx (*yy)|*yy', 1) {}\n"
            "called FileDialog.ShowModal\n")


def test_show_dialog(monkeypatch, capsys):
    """unittest for wxgui.show_dialog
    """
    def mock_confirm():
        print('called DialogParent.confirm')
        return 'expected_result'
    def mock_show(self):
        print('called Dialog.ShowModal')
        return testee.wx.ID_CANCEL
    dlg = types.SimpleNamespace(gui=mockwx.MockDialog('parent'), confirm=mock_confirm)
    assert capsys.readouterr().out == "called Dialog.__init__ with args () {}\n"
    assert testee.show_dialog(dlg) == (True, "expected_result")
    assert capsys.readouterr().out == ("called Dialog.ShowModal\n"
                                       "called DialogParent.confirm\n")
    monkeypatch.setattr(mockwx.MockDialog, 'ShowModal', mock_show)
    assert testee.show_dialog(dlg) == (False, "expected_result")
    assert capsys.readouterr().out == ("called Dialog.ShowModal\n"
                                       "called DialogParent.confirm\n")


def test_show_nonmodal(monkeypatch, capsys):
    """unittest for wxgui.show_nonmodal
    """
    dlg = mockwx.MockDialog('parent')
    assert capsys.readouterr().out == "called Dialog.__init__ with args () {}\n"
    testee.show_nonmodal(dlg)
    assert capsys.readouterr().out == "called Dialog.Show\n"


def _test_get_hotkeys_from_text():  # monkeypatch, capsys):  # unused, so not finished
    """unittest for wxgui.get_hotkeys_from_text
    """
    breakpoint()
    assert testee.get_hotkeys_from_text('Quit\nCtrl+Q') == []
    assert testee.get_hotkeys_from_text('Help\nCtrl+Alt+Shift+F1') == []
    assert testee.get_hotkeys_from_text('Edit\nF2') == []
    assert testee.get_hotkeys_from_text('insert\nInsert') == []
    assert testee.get_hotkeys_from_text('Delete\nShift+Del') == []
    assert testee.get_hotkeys_from_text('Down\nShift+Ctrl+PgDn') == []
    assert testee.get_hotkeys_from_text('Up\nPgUp') == []
    assert testee.get_hotkeys_from_text('Cancel\nEsc') == []


class MockMainWindow:
    "stub for main.MainWindow object"
    def __init__(self, *args):
        self.project_dirty = False
        if args:
            self._parent = args[0]
    def set_project_dirty(self, value):
        print(f"called Editor.set_project_dirty with arg {value}")
    def check_active(self):
        print('called Editor.check_active')
    def activate_item(self, item):
        print(f'called Editor.activate_item with arg {item}')
    def set_window_title(self):
        print('called Editor.set_window_title')
    def putsubtree(self, *args, **kwargs):
        print('called Editor.putsubtree with args', args, kwargs)
    def getsubtree(self, *args, **kwargs):
        print('called Editor.getsubtree with args', args, kwargs)
        return []


class MockMainGui:
    "stub for qtgui.MainGui object"
    def __init__(self, *args):
        print('called MainGui.__init__ with args', args)


class MockTree:
    "stub for qtgui.TreePanel object"
    def __init__(self, *args, **kwargs):
        print('called TreePanel.__init__ with args', args, kwargs)

    def getitemparentpos(self, item):
        print(f"called TreePanel.getitemparentpos with arg '{item}'")
        return "parent", 0

    def getitemkey(self, item):
        print(f"called TreePanel.getitemkey with arg '{item}'")
        return "itemkey"

    def removeitem(self, *args):
        print("called TreePanel.removeitem with args", args)
        return 'title', 'text', 'subtree'


class MockEditorPanel:
    "stub for qtqui.EditorPanel object"
    def __init__(self, *args):
        print('called EditorPanel.__init__ with args', args)
    def set_text_position(self, pos):
        print(f'called Editor.set_text_position with arg {pos}')
    def search_from_start(self):
        print('called Editor.search_from_start')


class TestMainGui:
    """unittest for wxgui.MainGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.MainGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MainGui.__init__ with args', args)
        monkeypatch.setattr(testee.MainGui, '__init__', mock_init)
        testobj = testee.MainGui()
        # testobj.app = testee.wx.App()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        monkeypatch.setattr(testee.wx.Frame, '__init__', mockwx.MockFrame.__init__)
        monkeypatch.setattr(testee.wx.Frame, 'SetIcon', mockwx.MockFrame.SetIcon)
        monkeypatch.setattr(testee.wx, 'App', mockwx.MockApp)
        monkeypatch.setattr(testee.wx, 'Icon', mockwx.MockIcon)
        master = types.SimpleNamespace(HERE=pathlib.Path(__file__).parent.resolve(),
                                       opts={'ScreenSize': 'xy'})
        testobj = testee.MainGui(master, 'title')
        assert testobj.master == master
        assert testobj.title == 'title'
        assert isinstance(testobj.app, testee.wx.App)
        assert capsys.readouterr().out == (
                "called app.__init__ with args ()\n"
                "called frame.__init__ with args"
                " () {'parent': None, 'title': 'title', 'size': 'xy', 'style': 541072960}\n"
                f"called Icon.__init__ with args ('{testobj.master.HERE}/icons/doctree.ico', 3)\n"
                "called Frame.SetIcon with args"
                f" (Icon created from '{testobj.master.HERE}/icons/doctree.ico',)\n")

    def test_create_menu(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.create_menu
        """
        def mock_add(arg):
            print(f'called MainGui.addToolBar with arg {arg}')
            return toolbar
        monkeypatch.setattr(testee.wx,'ToolBar', mockwx.MockToolBar)
        monkeypatch.setattr(testee.wx,'MenuBar', mockwx.MockMenuBar)
        monkeypatch.setattr(testee.wx, 'Bitmap', mockwx.MockBitmap)
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(testee.wx.Frame, 'Bind', mockwx.MockFrame.Bind)
        monkeypatch.setattr(testee.wx.Frame, 'SetToolBar', mockwx.MockFrame.SetToolBar)
        monkeypatch.setattr(testee.wx.Frame, 'SetMenuBar', mockwx.MockFrame.SetMenuBar)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockMainWindow()
        testobj.master.HERE = pathlib.Path(__file__).parent.resolve()
        # testobj.menulist = []
        # testobj.mainactiondict = {}
        # testobj.styleactiondict = {}
        toolbar = mockwx.MockToolBar()
        assert capsys.readouterr().out == "called ToolBar.__init__ with args ()\n"
        testobj.addToolBar = mock_add
        menubar = mockwx.MockMenuBar()
        assert capsys.readouterr().out == "called MenuBar.__init__ with args ()\n"
        testobj.create_menu([])
        assert capsys.readouterr().out == (
                f"called ToolBar.__init__ with args ({testobj},)\n"
                "called Frame.SetToolBar with args (A ToolBar,)\n"
                "called MenuBar.__init__ with args ()\n"
                "called Frame.SetMenuBar with args (A MenuBar,)\n")
        callbacks = [f'callback{x}' for x in range(12)]
        menudata = [('aaa', [('aaaa', callbacks[0], '', 'aaa.ico', ''),
                             ('exit', callbacks[1], 'Ctrl+X,Esc', 'exit.ico', '')]),
                    ('xxx', [('LinE sPacINg', '', '', '', ''),
                             ('pARAgraph sPAcinG', '', '', '', '')]),
                    ('yyy', [('B', callbacks[2], '', '', 'CheckB'),
                             ('I', callbacks[3], '', '', 'CheckI'),
                             ('U', callbacks[4], '', '', 'CheckU'),
                             ('S', callbacks[5], '', '', 'CheckS'),
                             ('M', callbacks[11], '', '', 'CheckM'),
                             (),
                             (),
                             (' monospace ', '', '', '', ''),
                             (' justify', '', '', '', ''),
                             ('indent ', '', '', '', ''),
                             ('CtrlTab', 'callback', 'Ctrl+Tab', '', ''),
                             ('X', callbacks[6], '', '', 'Check'),
                             ()]),
                    ('zzz', [('&Undo', callbacks[7], 'Ctrl+Z', '', 'undo'),
                             ('&Redo', callbacks[8], 'Ctrl+Y', '', 'redo'),
                             ('', callbacks[0], '', '', 'xxx')]),
                    ('bbb', [('bbbb', callbacks[9], '', '', '')]),
                    ('ccc', [('cccc', callbacks[10], '', '', '')])]
        testobj.create_menu(menudata)
        assert capsys.readouterr().out == expected_output['create_menu'].format(testobj=testobj,
                                                                                testee=testee)

        # assert len(testobj.menulist) == 6
        assert isinstance(testobj.viewmenu, testee.wx.Menu)  # mockqtw.MockMenu)
        assert isinstance(testobj.notemenu, testee.wx.Menu)  # mockqtw.MockMenu)
        assert isinstance(testobj.treemenu, testee.wx.Menu)  # mockqtw.MockMenu)
        # assert testobj.menulist[1] == testobj.notemenu
        # assert testobj.menulist[2] == testobj.viewmenu
        # assert testobj.menulist[3] == testobj.treemenu
        # assert len(testobj.menulist[0].MenuItemCount()) == 2
        # assert capsys.readouterr().out == 'called Menu.MenuItemCount\n'
        # assert len(testobj.menulist[1].MenuItemCount()) == 0
        # assert capsys.readouterr().out == 'called Menu.MenuItemCount\n'
        # assert len(testobj.menulist[2].MenuItemCount()) == 8
        # assert capsys.readouterr().out == 'called Menu.MenuItemCount\n'
        # assert len(testobj.menulist[3].MenuItemCount()) == 2
        # assert capsys.readouterr().out == 'called Menu.MenuItemCount\n'
        # assert len(testobj.menulist[4].MenuItemCount()) == 1
        # assert capsys.readouterr().out == 'called Menu.MenuItemCount\n'
        # assert len(testobj.menulist[5].MenuItemCount()) == 1
        # assert capsys.readouterr().out == 'called Menu.MenuItemCount\n'
        assert isinstance(testobj.undo_item, testee.wx.MenuItem)
        assert testobj.undo_item.GetItemLabel() == '&Undo'
        assert capsys.readouterr().out == 'called menuitem.GetItemLabel\n'
        # assert testobj.undo_item.shortcuts() == ['Ctrl+Z']
        # assert capsys.readouterr().out == 'called Action.shortcuts\n'
        assert isinstance(testobj.redo_item, testee.wx.MenuItem)
        assert testobj.redo_item.GetItemLabel() == '&Redo'
        assert capsys.readouterr().out == 'called menuitem.GetItemLabel\n'
        # assert testobj.redo_item.shortcuts() == ['Ctrl+Y']
        # assert capsys.readouterr().out == 'called Action.shortcuts\n'
        # assert isinstance(testobj.quit_action, testee.wx.MenuItem)
        # assert testobj.quit_action.GetItemLabel() == 'exit'
        # assert capsys.readouterr().out == 'called Action.GetItemLabel\n'
        # assert testobj.quit_action.shortcuts() == ['Ctrl+X', 'Esc']
        # assert capsys.readouterr().out == 'called menuitem.shortcuts\n'
        # assert testobj.mainactiondict == {'aaa': callback0, 'exit': callback99}
        # assert len(testobj.mainactiondict) == 2
        # assert testobj.styleactiondict == {'ccc': callback7}
        # assert len(testobj.styleactiondict) == 1

    def test_create_splitter(self, monkeypatch, capsys):
        """unittest for MainGui.create_splitter
        """
        monkeypatch.setattr(testee.wx, 'SplitterWindow', mockwx.MockSplitter)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_splitter()
        # assert testobj.splitter.parent == testobj
        assert isinstance(testobj.splitter, testee.wx.SplitterWindow)
        assert capsys.readouterr().out == (
                f"called Splitter.__init__ with args ({testobj}, -1) {{}}\n"
                "called splitter.SetMinimumPaneSize with args (1,)\n")

    def test_create_tree_on_left(self, monkeypatch, capsys):
        """unittest for MainGui.tree_on_left
        """
        def mock_bind(*args):
            print('called MainGui.Bind with args', args)
        monkeypatch.setattr(testee, 'TreePanel', mockwx.MockTree)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = 'Editor'
        testobj.Bind = mock_bind
        testobj.splitter = mockwx.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__ with args () {}\n"
        testobj.create_tree_on_left()
        assert testobj.tree.controller == 'Editor'  # testobj
        assert isinstance(testobj.tree, testee.TreePanel)
        assert testobj.root == 'The Root'
        assert capsys.readouterr().out == (
                f"called Tree.__init__ with args ({testobj.splitter},) {{'style': 1}}\n"
                "called tree.AddRoot with args ('MyNotes',)\n"
                f"called MainGui.Bind with args"
                f" ({testee.wx.EVT_TREE_SEL_CHANGED}, {testobj.OnSelChanged}, {testobj.tree})\n"
                f"called tree.Bind with args ({testee.wx.EVT_KEY_DOWN}, {testobj.on_key})\n")

    def test_create_editor_on_right(self, monkeypatch, capsys):
        """unittest for MainGui.editor_on_right
        """
        monkeypatch.setattr(testee, 'EditorPanel', mockwx.MockEditor)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.splitter = mockwx.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__ with args () {}\n"
        testobj.create_editor_on_right()
        assert isinstance(testobj.editor, testee.EditorPanel)
        assert capsys.readouterr().out == (
                f"called Editor.__init__ with args ({testobj.splitter},) {{}}\n"
                "called editor.Enable with args (False,)\n"
                f"called editor.Bind with args ({testee.wx.EVT_KEY_DOWN}, {testobj.on_key})\n")

    def test_create_statusbar_at_bottom(self, monkeypatch, capsys):
        """unittest for MainGui.statusbar_at_bottom
        """
        monkeypatch.setattr(testee.wx.Frame, 'CreateStatusBar', mockwx.MockFrame.CreateStatusBar)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_statusbar_at_bottom()
        assert isinstance(testobj.statbar, mockwx.MockStatusBar)
        assert capsys.readouterr().out == ("called Frame.CreateStatusBar\n"
                                           "called StatusBar.__init__ with args ()\n")

    def test_finalize_display(self, monkeypatch, capsys):
        """unittest for MainGui.finalize_display
        """
        def mock_create(tbar):
            print(f'called MainGui.create_stylestoolbar with arg {tbar}')
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Frame, 'GetToolBar', mockwx.MockFrame.GetToolBar)
        monkeypatch.setattr(testee.wx.Frame, 'SetSizer', mockwx.MockFrame.SetSizer)
        monkeypatch.setattr(testee.wx.Frame, 'SetAutoLayout', mockwx.MockFrame.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Frame, 'SetSize', mockwx.MockFrame.SetSize)
        monkeypatch.setattr(testee.wx.Frame, 'Layout', mockwx.MockFrame.Layout)
        monkeypatch.setattr(testee.wx.Frame, 'Bind', mockwx.MockFrame.Bind)
        monkeypatch.setattr(testee.wx.Frame, 'Show', mockwx.MockFrame.Show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(opts={'SashPosition': 10, 'ScreenSize': (100, 200)})
        testobj.splitter = mockwx.MockSplitter()
        testobj.tree = mockwx.MockTree()
        testobj.editor = mockwx.MockEditor()
        assert capsys.readouterr().out == ("called Splitter.__init__ with args () {}\n"
                                           "called Tree.__init__ with args () {}\n"
                                           "called Editor.__init__ with args () {}\n")
        testobj.create_stylestoolbar = mock_create
        testobj.finalize_display()
        assert testobj.menu_disabled
        assert not testobj.in_editor
        assert capsys.readouterr().out == (
                "called Frame.GetToolBar with args ()\n"
                "called ToolBar.__init__ with args ()\n"
                "called MainGui.create_stylestoolbar with arg A ToolBar\n"
                "called Toolbar.Realize with args ()\n"
                f"called splitter.SplitVertically with args ({testobj.tree}, {testobj.editor})\n"
                "called splitter.SetSashPosition with args (10, True)\n"
                f"called Frame.Bind with args ({testee.wx.EVT_CLOSE}, {testobj.afsl})\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called vert sizer.Add with args MockSplitter (1, 8192)\n"
                "called Frame.SetSizer with args (vert sizer,)\n"
                "called Frame.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                "called Frame.SetSize with args ((100, 200),)\n"
                "called Frame.Layout with args ()\n"
                "called frame.Show with args (True,)\n")
        testobj.master.opts['SashPosition'] = (10, 100)
        testobj.finalize_display()
        assert testobj.menu_disabled
        assert not testobj.in_editor
        assert capsys.readouterr().out == (
                "called Frame.GetToolBar with args ()\n"
                "called ToolBar.__init__ with args ()\n"
                "called MainGui.create_stylestoolbar with arg A ToolBar\n"
                "called Toolbar.Realize with args ()\n"
                f"called splitter.SplitVertically with args ({testobj.tree}, {testobj.editor})\n"
                "called splitter.SetSashPosition with args ((10, 100), True)\n"
                "called splitter.SetSashPosition with args (10, True)\n"
                f"called Frame.Bind with args ({testee.wx.EVT_CLOSE}, {testobj.afsl})\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called vert sizer.Add with args MockSplitter (1, 8192)\n"
                "called Frame.SetSizer with args (vert sizer,)\n"
                "called Frame.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                "called Frame.SetSize with args ((100, 200),)\n"
                "called Frame.Layout with args ()\n"
                "called frame.Show with args (True,)\n")

    def test_disable_menu(self, monkeypatch, capsys):
        """unittest for MainGui.disable_menu
        """
        def mock_get(self):
            print('called MainGui.GetMenuBar')
            return mockwx.MockMenuBar()
        def mock_getmenus(self, *args):
            print('called menubar.GetMenus with args', args)
            return []
        def mock_getitems(self):
            print('called menu.GetMenuItems')
            return [MockMenuItem(0), MockMenuItem(1), MockMenuItem(2), MockMenuItem(3)]
        class MockMenuItem:
            def __init__(self, count):
                print('called MenuItem.__init__')
                self._id = count + 1
                self._text = ['Open', 'Init', 'eXit', 'qqqq'][count]
            def GetId(self):  # , *args):
                print('called menuitem.GetId')  #  with args', args)
                return self._id
            def GetItemLabelText(self):
                print('called menuitem.GetItemLabelText')
                return self._text
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.MainGui, 'GetMenuBar',  mock_get)
        testobj.disable_menu()
        assert testobj.menu_disabled
        assert capsys.readouterr().out == ("called MainGui.GetMenuBar\n"
                                           "called MenuBar.__init__ with args ()\n"
                                           "called menubar.GetMenus\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called menubar.EnableTop with args (1, False)\n"
                                           "called menubar.GetMenus with args (0,)\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called menu.GetMenuItems\n")
        monkeypatch.setattr(mockwx.MockMenuBar, 'GetMenus', mock_getmenus)
        monkeypatch.setattr(mockwx.MockMenu, 'GetMenuItems', mock_getitems)
        testobj.disable_menu(value=False)
        assert not testobj.menu_disabled
        assert capsys.readouterr().out == ("called MainGui.GetMenuBar\n"
                                           "called MenuBar.__init__ with args ()\n"
                                           "called menubar.GetMenus with args ()\n"
                                           "called menubar.GetMenus with args (0,)\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called menu.GetMenuItems\n"
                                           "called MenuItem.__init__\n"
                                           "called MenuItem.__init__\n"
                                           "called MenuItem.__init__\n"
                                           "called MenuItem.__init__\n"
                                           "called menuitem.GetItemLabelText\n"
                                           "called menuitem.GetItemLabelText\n"
                                           "called menuitem.GetItemLabelText\n"
                                           "called menuitem.GetItemLabelText\n"
                                           "called menuitem.GetId\n"
                                           "called menu.Enable with args (4, True)\n")

    def test_create_stylestoolbar(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.create_stylestoolbar
        """
        class MockEditor:  #
            def select_text_color(self):
                print('called EditorPanel.select_text_color')
            def set_text_color(self):
                print('called EditorPanel.set_text_color')
            def select_background_color(self):
                print('called EditorPanel.select_background_color')
            def set_background_color(self):
                print('called EditorPanel.set_background_color')
        def mock_change(*args):
            print('called maingui.changebitmapbuttoncolour with args', args)
        monkeypatch.setattr(testee.wx, 'Bitmap', mockwx.MockBitmap)
        monkeypatch.setattr(testee.csel, 'ColourSelect', mockwx.MockColourSelect)
        monkeypatch.setattr(testee.wxlb, 'GenBitmapButton', mockwx.MockButton)
        toolbar = mockwx.MockToolBar()
        assert capsys.readouterr().out == "called ToolBar.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.changebitmapbuttoncolour = mock_change
        testobj.editor = MockEditor()
        testobj.create_stylestoolbar(toolbar)
        assert testobj.textcolour == testee.wx.BLACK
        assert testobj.backgroundcolour == testee.wx.WHITE
        assert isinstance(testobj.fgcselect, testee.csel.ColourSelect)
        assert isinstance(testobj.fgcset, testee.wxlb.GenBitmapButton)
        assert isinstance(testobj.bgcselect, testee.csel.ColourSelect)
        assert isinstance(testobj.bgcset, testee.wxlb.GenBitmapButton)
        assert capsys.readouterr().out == expected_output['stylestoolbar'].format(testobj=testobj,
                                                                                  testee=testee)

    def test_changebitmapbuttoncolour(self, monkeypatch, capsys):
        """unittest for MainGui.changebitmapbuttoncolour
        """
        bitmapbutton = mockwx.MockBitmapButton()
        assert capsys.readouterr().out == "called BitmapButton.__init__ with args () {}\n"
        monkeypatch.setattr(testee.wx, 'MemoryDC', mockwx.MockMemoryDC)
        monkeypatch.setattr(testee.wx, 'Brush', mockwx.MockBrush)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.changebitmapbuttoncolour(bitmapbutton, 'colour')
        assert capsys.readouterr().out == (
                "called BitmapButton.GetBitmapLabel\n"
                "called memorydc.SelectObject with arg bitmap\n"
                "called brush.__init__ with args ('colour',)\n"
                "called memorydc.SetBackground with arg <<brush from color colour>>\n"
                "called memorydc.Clear\n"
                f"called memorydc.SelectObject with arg {testee.wx.NullBitmap}\n"
                "called BitmapButton.SetBitmapLabel with args ('bitmap',)\n")

    def test_show_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.show_statusmessage
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.statbar = mockwx.MockStatusBar()
        assert capsys.readouterr().out == "called StatusBar.__init__ with args ()\n"
        testobj.show_statusmessage('text')
        assert capsys.readouterr().out == "called statusbar.SetStatusText with args ('text',)\n"

    def test_set_version(self, monkeypatch, capsys):
        """unittest for MainGui.set_version
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(opts={})
        testobj.set_version()
        assert testobj.master.opts['Version'] == 'Wx'
        assert capsys.readouterr().out == ""

    def test_set_window_dimensions(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_dimensions
        """
        monkeypatch.setattr(testee.wx.Frame, 'SetSize', mockwx.MockFrame.SetSize)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_window_dimensions('x', 'y')
        assert capsys.readouterr().out == ("called Frame.SetSize with args ('x', 'y')\n")

    def test_get_screensize(self, monkeypatch, capsys):
        """unittest for MainGui.get_screensize
        """
        monkeypatch.setattr(testee.wx.Frame, 'GetSize', mockwx.MockFrame.GetSize)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_screensize() == (100, 10)
        assert capsys.readouterr().out == ("called Frame.GetSize\n"
                                           "called Size.__init__ with args (100, 10)\n")

    def test_set_windowtitle(self, monkeypatch, capsys):
        """unittest for MainGui.set_windowtitle
        """
        monkeypatch.setattr(testee.wx.Frame, 'SetTitle', mockwx.MockFrame.SetTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_windowtitle('title')
        assert capsys.readouterr().out == "called Frame.SetTitle with args ('title',)\n"

    def test_set_window_split(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_split
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.splitter = mockwx.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__ with args () {}\n"
        testobj.set_window_split((10, 100))
        assert capsys.readouterr().out == "called splitter.SetSashPosition with args (10, True)\n"
        with pytest.raises(TypeError):
            testobj.set_window_split(10)

    def test_get_splitterpos(self, monkeypatch, capsys):
        """unittest for MainGui.get_splitterpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.splitter = mockwx.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__ with args () {}\n"
        assert testobj.get_splitterpos() == (55,)
        assert capsys.readouterr().out == "called splitter.SetSashPosition\n"

    def _test_init_app(self, monkeypatch, capsys):
        """unittest for MainGui.init_app
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_app() == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def test_set_focus_to_tree(self, monkeypatch, capsys):
        """unittest for MainGui.set_focus_to_tree
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.set_focus_to_tree()
        assert not testobj.in_editor
        assert capsys.readouterr().out == "called tree.SetFocus\n"

    def test_set_focus_to_editor(self, monkeypatch, capsys):
        """unittest for MainGui.set_focus_to_editor
        """
        def mock_get(*args):
            print('called tree.getitemkey with args', args)
            return keyref
        def mock_set(*args):
            print('called editor.set_text_position with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(activeitem='xxx', text_positions={'xxx': 'pos'})
        testobj.tree = mockwx.MockTree()
        testobj.editor = mockwx.MockEditor()
        assert capsys.readouterr().out == ("called Tree.__init__ with args () {}\n"
                                           "called Editor.__init__ with args () {}\n")
        testobj.tree.getitemkey = mock_get
        testobj.editor.set_text_position = mock_set
        keyref = 'yyy'
        testobj.set_focus_to_editor()
        assert testobj.in_editor
        assert capsys.readouterr().out == ("called editor.SetFocus\n"
                                           "called tree.getitemkey with args ('xxx',)\n")
        keyref = 'xxx'
        testobj.set_focus_to_editor()
        assert testobj.in_editor
        assert capsys.readouterr().out == ("called editor.SetFocus\n"
                                           "called tree.getitemkey with args ('xxx',)\n"
                                           "called editor.set_text_position with args ('pos',)\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for MainGui.go
        """
        def mock_loop():
            print('called Application.MainLoop')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = types.SimpleNamespace(MainLoop=mock_loop)
        testobj.go()
        assert capsys.readouterr().out == "called Application.MainLoop\n"

    def test_close(self, monkeypatch, capsys):
        """unittest for MainGui.close
        """
        monkeypatch.setattr(testee.wx.Frame, 'Close', mockwx.MockFrame.Close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close()
        assert capsys.readouterr().out == "called Frame.Close with arg False\n"

    def test_afsl(self, monkeypatch, capsys):
        """unittest for MainGui.afsl
        """
        def mock_handle():
            print('called Doctree.handle_save_needed')
            return False
        def mock_handle_2():
            print('called DocTree.handle_save_needed')
            return True
        def mock_cleanup():
            print('called DocTree.cleanup_files')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(handle_save_needed=mock_handle,
                                               cleanup_files=mock_cleanup)
        testobj.afsl()
        assert capsys.readouterr().out == "called Doctree.handle_save_needed\n"
        testobj.master.handle_save_needed = mock_handle_2
        testobj.afsl()
        assert capsys.readouterr().out == ("called DocTree.handle_save_needed\n"
                                           "called DocTree.cleanup_files\n")
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj.afsl(event)
        assert capsys.readouterr().out == ("called DocTree.handle_save_needed\n"
                                           "called DocTree.cleanup_files\n"
                                           "called event.Skip\n")

    def test_hide_me(self, monkeypatch, capsys):
        """unittest for MainGui.hide_me
        """
        class MockIcon:
            def __init__(self, *args):
                print('called TaskbarIcon.__init__ with args', args)
        monkeypatch.setattr(testee, 'TaskbarIcon', MockIcon)
        monkeypatch.setattr(testee.wx.Frame, 'Hide', mockwx.MockFrame.Hide)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hide_me()
        assert capsys.readouterr().out == (f"called TaskbarIcon.__init__ with args ({testobj},)\n"
                                           "called frame.Hide\n")

    def test_revive(self, monkeypatch, capsys):
        """unittest for MainGui.revive
        """
        class MockIcon:
            def Destroy(self, *args):
                print('called TaskbarIcon.Destroy')
        monkeypatch.setattr(testee.wx.Frame, 'Show', mockwx.MockFrame.Show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tbi = MockIcon()
        testobj.revive()
        assert capsys.readouterr().out == ("called frame.Show\n"
                                           "called TaskbarIcon.Destroy\n")

    def _test_expand_root(self, monkeypatch, capsys):
        """unittest for MainGui.expand_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.expand_root() == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def test_start_add(self, monkeypatch, capsys):
        """unittest for MainGui.start_add
        """
        def mock_do(*args):
            print('called TreeDocs.do_addaction with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(do_addaction=mock_do)
        testobj.start_add()
        assert capsys.readouterr().out == (
                "called TreeDocs.do_addaction with args (None, True, -1, ['', '', []])\n")
        testobj.start_add(root='root', under=False, new_title='xxx', extra_titles=[])
        assert capsys.readouterr().out == (
                "called TreeDocs.do_addaction with args ('root', False, -1, ['xxx', '', []])\n")
        testobj.start_add(root='root', under=False, new_title='xxx', extra_titles=['yyy', 'zzz'])
        assert capsys.readouterr().out == (
                "called TreeDocs.do_addaction with args"
                " ('root', False, -1, ['xxx', '', ['yyy', '', ['zzz', '', []]]])\n")

    def test_set_next_item(self, monkeypatch, capsys):
        """unittest for MainGui.set_next_item
        """
        def mock_getnext(*args):
            print('called tree.GetNextSibling')  #  with args', args)
            return mockwx.MockTreeItem('not ok')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(activeitem='activeitem')
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.set_next_item()
        assert capsys.readouterr().out == (
                "called tree.GetNextSibling\n"
                "called TreeItem.__init__ with args ('next treeitem',)\n"
                "called TreeItem.IsOk\n"
                "called tree.SelectItem with args (next treeitem,)\n")
        testobj.tree.GetNextSibling = mock_getnext
        assert not testobj.set_next_item()
        assert capsys.readouterr().out == (
                "called tree.GetNextSibling\n"
                "called TreeItem.__init__ with args ('not ok',)\n"
                "called TreeItem.IsOk\n")
        assert not testobj.set_next_item(any_level=True)
        assert capsys.readouterr().out == (
                "called tree.GetNextSibling\n"
                "called TreeItem.__init__ with args ('not ok',)\n"
                "called TreeItem.IsOk\n")

    def test_set_prev_item(self, monkeypatch, capsys):
        """unittest for MainGui.set_prev_item
        """
        def mock_getprev(*args):
            print('called tree.GetPrevSibling')  #  with args', args)
            return mockwx.MockTreeItem('not ok')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(activeitem='activeitem')
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.set_prev_item()
        assert capsys.readouterr().out == (
                "called tree.GetPrevSibling\n"
                "called TreeItem.__init__ with args ('previous treeitem',)\n"
                "called TreeItem.IsOk\n"
                "called tree.SelectItem with args (previous treeitem,)\n")
        testobj.tree.GetPrevSibling = mock_getprev
        assert not testobj.set_prev_item()
        assert capsys.readouterr().out == (
                "called tree.GetPrevSibling\n"
                "called TreeItem.__init__ with args ('not ok',)\n"
                "called TreeItem.IsOk\n")
        assert not testobj.set_prev_item(any_level=True)
        assert capsys.readouterr().out == (
                "called tree.GetPrevSibling\n"
                "called TreeItem.__init__ with args ('not ok',)\n"
                "called TreeItem.IsOk\n")

    def test_start_copy(self, monkeypatch, capsys):
        """unittest for MainGui.start_copy
        """
        def mock_do(*args):
            print('called TreeDocs.do_copyaction with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(do_copyaction=mock_do)
        testobj.start_copy()
        assert capsys.readouterr().out == (
                "called TreeDocs.do_copyaction with args (False, True, None)\n")
        testobj.start_copy(cut=True, retain=False, current='current')
        assert capsys.readouterr().out == (
                "called TreeDocs.do_copyaction with args (True, False, 'current')\n")

    def test_start_paste(self, monkeypatch, capsys):
        """unittest for MainGui.start_paste
        """
        def mock_do(*args):
            print('called TreeDocs.do_pasteaction with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(do_pasteaction=mock_do)
        testobj.start_paste()
        assert capsys.readouterr().out == (
                "called TreeDocs.do_pasteaction with args (True, False, None)\n")
        testobj.start_paste(before=False, below=True, dest='dest')
        assert capsys.readouterr().out == (
                "called TreeDocs.do_pasteaction with args (False, True, 'dest')\n")

    def test_reorder_items(self, monkeypatch, capsys):
        """unittest for MainGui.reorder_items
        """
        def mock_getfirst(*args):
            print('called tree.GetFirstChild with args', args)
            if args[0] == 'root':
                return mockwx.MockTreeItem('first'), 0
            return mockwx.MockTreeItem('not ok'), -1

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.tree.GetFirstChild = mock_getfirst
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.reorder_items('root')
        assert capsys.readouterr().out == "called tree.SortChildren with args ('root',)\n"
        # breakpoint()
        testobj.reorder_items('root', recursive=True)
        assert capsys.readouterr().out == ("called tree.SortChildren with args ('root',)\n"
                                           "called tree.GetFirstChild with args ('root',)\n"
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called tree.SortChildren with args (first,)\n"
                                           "called tree.GetFirstChild with args (first,)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called tree.GetNextChild with args ('root', 0)\n"
                                           "called TreeItem.__init__ with args ('next',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called tree.SortChildren with args (next,)\n"
                                           "called tree.GetFirstChild with args (next,)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called tree.GetNextChild with args ('root', 1)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.IsOk\n")

    def test_rebuild_root(self, monkeypatch, capsys):
        """unittest for MainGui.rebuild_root
        """
        def mock_set_title(*args):
            print('called tree.setitemtitle with args', args)
        def mock_set_key(*args):
            print('called tree.setitemkey with args', args)
        def mock_set_text(*args):
            print('called tree.setitemtext with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(project_file=types.SimpleNamespace(stem='xxx'),
                                               opts={'RootTitle': 'qqq', 'RootData': 'rrr'})
        testobj.tree = mockwx.MockTree()
        testobj.tree.setitemtitle = mock_set_title
        testobj.tree.setitemkey = mock_set_key
        testobj.tree.setitemtext = mock_set_text
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.rebuild_root() == "appended item"
        assert capsys.readouterr().out == (
                "called tree.DeleteAllItems\n"
                "called tree.AddRoot with args ('hidden_root',)\n"
                "called tree.SetItemData() with args ('The Root', '')\n"
                "called tree.AppendItem with args ('The Root', 'xxx')\n"
                "called tree.setitemtitle with args ('appended item', 'qqq')\n"
                "called tree.setitemkey with args ('appended item', -1)\n"
                "called tree.setitemtext with args ('appended item', 'rrr')\n")

    def _test_clear_viewmenu(self, monkeypatch, capsys):
        """unittest for MainGui.clear_viewmenu
        """
        def mock_get():
            print('called menu.GetMenuItems')
            return ['x', 'y', 'z', 'a', 'b', 'c', 'd']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu = mockwx.MockMenu()
        testobj.viewmenu.GetMenuItems = mock_get
        testobj.clear_viewmenu()
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called menu.GetMenuItems\n"
                                           "called menu.Delete with args ('b',)\n"
                                           "called menu.Delete with args ('c',)\n"
                                           "called menu.Delete with args ('d',)\n")

    def test_add_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.add_viewmenu_option
        """
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(testee.wx.Frame, 'Bind', mockwx.MockFrame.Bind)
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.master = types.SimpleNamespace(select_view='select_view')
        testobj.viewmenu = mockwx.MockMenu()
        result = testobj.add_viewmenu_option('optiontext', 'callback')
        assert isinstance(result, testee.wx.MenuItem)
        assert capsys.readouterr().out == (
                "called Menu.__init__ with args ()\n"
                "called MenuItem.__init__ with args (A Menu, -1, 'optiontext',"
                " 'Switch to this view') {'kind': 1}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback')\n"
                "called menu.Append with args MockMenuItem\n")

    # def _test_check_viewmenu_option(self, monkeypatch, capsys):
    #     """unittest for MainGui.check_viewmenu_option
    #     """
    #     def mock_get():
    #         print('called viewmenu.GetMenuItems')
    #         return ('0', '1', '2', '3', '4', '5', '6', menuitem1, menuitem2, menuitem3)
    #     class MockMenuItem:
    #         def __init__(self, *args):
    #             if args:
    #                 self._text = args[0]
    #         def GetId(self):
    #             print('called menuitem.GetId')
    #             return self._text[0]
    #         def GetItemLabelText(self):
    #             print('called menuitem.GetItemLabelText')
    #             return self._text[1:]
    #         def IsChecked(self):
    #             print('called menuitem.IsChecked')
    #             return self._text == '1one'
    #         def Check(self, value=True):
    #             print(f'called menuitem.check with arg {value}')
    #     class MockEvent:
    #         def GetId(self):
    #             print('called event.GetId')
    #             return eventid
    #     monkeypatch.setattr(testee.wx, 'MenuItem', MockMenuItem)
    #     menu_item = testee.wx.MenuItem()
    #     menuitem1 = MockMenuItem('1one')
    #     menuitem2 = MockMenuItem('2two')
    #     menuitem3 = MockMenuItem('3three')
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     # testobj,viewmenu = mockwx.MockMenu()
    #     testobj.viewmenu = types.SimpleNamespace(GetMenuItems=mock_get)
    #     assert testobj.check_viewmenu_option(menu_item) == ""
    #     assert capsys.readouterr().out == "called menuitem.check with arg True\n"

    #     event = MockEvent()
    #     eventid = '1'
    #     assert testobj.check_viewmenu_option(event) == "one"
    #     assert capsys.readouterr().out == ("called event.GetId\n"
    #                                        "called viewmenu.GetMenuItems\n"
    #                                        "called menuitem.GetId\n"
    #                                        "called menuitem.GetItemLabelText\n"
    #                                        "called menuitem.check with arg True\n"
    #                                        "called menuitem.GetId\n"
    #                                        "called menuitem.IsChecked\n"
    #                                        "called menuitem.GetId\n"
    #                                        "called menuitem.IsChecked\n")
    #     eventid = '2'
    #     assert testobj.check_viewmenu_option(event) == "two"
    #     assert capsys.readouterr().out == ("called event.GetId\n"
    #                                        "called viewmenu.GetMenuItems\n"
    #                                        "called menuitem.GetId\n"
    #                                        "called menuitem.IsChecked\n"
    #                                        "called menuitem.check with arg False\n"
    #                                        "called menuitem.GetId\n"
    #                                        "called menuitem.GetItemLabelText\n"
    #                                        "called menuitem.check with arg True\n"
    #                                        "called menuitem.GetId\n"
    #                                        "called menuitem.IsChecked\n")

    def test_check_menuitem_option(self, monkeypatch, capsys):
        """unittest for MainGui.check_menuitem_option
        """
        item = mockwx.MockMenuItem()
        assert capsys.readouterr().out == "called MenuItem.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.check_menuitem_option(item, 'value')
        assert capsys.readouterr().out == "called menuitem.Check with arg value\n"

    def test_determine_viewmenuitem(self, monkeypatch, capsys):
        """unittest for MainGui.determine_viewmenuitem
        """
        def mock_getid():
            print('called event.GetId')
            return 'yy'
        def mock_getid1():
            print('called menuitem1.getId')
            return 'xx'
        def mock_getid2():
            print('called menuitem2.getId')
            return 'yy'
        def mock_get():
            print('called menu.GetMenuItems')
            return ()
        def mock_get_2():
            print('called menu.GetMenuItems')
            return menuitem1, menuitem2
        event = types.SimpleNamespace(GetId=mock_getid)
        menuitem1 = types.SimpleNamespace(GetId=mock_getid1)
        menuitem2 = types.SimpleNamespace(GetId=mock_getid2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu = mockwx.MockMenu()
        assert capsys.readouterr().out == "called Menu.__init__ with args ()\n"
        testobj.viewmenu.GetMenuItems = mock_get
        assert testobj.determine_viewmenuitem(event, '') is None
        assert capsys.readouterr().out == "called menu.GetMenuItems\n"
        testobj.viewmenu.GetMenuItems = mock_get_2
        assert testobj.determine_viewmenuitem(event, '') == menuitem2
        assert capsys.readouterr().out == ("called menu.GetMenuItems\n"
                                           "called menuitem1.getId\n"
                                           "called event.GetId\n"
                                           "called menuitem2.getId\n"
                                           "called event.GetId\n")

    # def _test_uncheck_viewmenu_option(self, monkeypatch, capsys):
    #     """unittest for MainGui.uncheck_viewmenu_option
    #     """
    #     def mock_get():
    #         print('called viewmenu.GetMenuItems')
    #         return ()
    #     def mock_get_2():
    #         print('called viewmenu.GetMenuItems')
    #         return ('0', '1', '2', '3', '4', '5', '6', menuitem1, menuitem2, menuitem3)
    #     menuitem1 = mockwx.MockMenuItem('1one')
    #     menuitem2 = mockwx.MockMenuItem('2two')
    #     menuitem3 = mockwx.MockMenuItem('3three')
    #     assert capsys.readouterr().out == ("called MenuItem.__init__ with args ('1one',) {}\n"
    #                                        "called MenuItem.__init__ with args ('2two',) {}\n"
    #                                        "called MenuItem.__init__ with args ('3three',) {}\n")
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.master = types.SimpleNamespace(opts={'ActiveView': 2})
    #     testobj.viewmenu = types.SimpleNamespace(GetMenuItems=mock_get)
    #     testobj.uncheck_viewmenu_option()
    #     assert capsys.readouterr().out == "called viewmenu.GetMenuItems\n"
    #     testobj.viewmenu = types.SimpleNamespace(GetMenuItems=mock_get_2)
    #     testobj.uncheck_viewmenu_option()
    #     assert capsys.readouterr().out == ("called viewmenu.GetMenuItems\n"
    #                                        "called menuitem.Check with arg False\n")
    #     # maar hoe weet ik nu dat-ie de juiste gedaan heeft?

    # def _test_rename_viewmenu_option(self, monkeypatch, capsys):
    #     """unittest for MainGui.rename_viewmenu_option
    #     """
    #     def mock_get():
    #         print('called viewmenu.GetMenuItems')
    #         return ()
    #     def mock_get_2():
    #         print('called viewmenu.GetMenuItems')
    #         return ('0', '1', '2', '3', '4', '5', '6', menuitem1, menuitem2, menuitem3)
    #     menuitem1 = mockwx.MockMenuItem('1one')
    #     menuitem2 = mockwx.MockMenuItem('2two')
    #     menuitem3 = mockwx.MockMenuItem('3three')
    #     assert capsys.readouterr().out == ("called MenuItem.__init__ with args ('1one',) {}\n"
    #                                        "called MenuItem.__init__ with args ('2two',) {}\n"
    #                                        "called MenuItem.__init__ with args ('3three',) {}\n")
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.master = types.SimpleNamespace(opts={'ActiveView': 2})
    #     testobj.viewmenu = types.SimpleNamespace(GetMenuItems=mock_get)
    #     testobj.rename_viewmenu_option('newname')
    #     assert capsys.readouterr().out == "called viewmenu.GetMenuItems\n"
    #     testobj.viewmenu = types.SimpleNamespace(GetMenuItems=mock_get_2)
    #     testobj.rename_viewmenu_option('newname')
    #     assert capsys.readouterr().out == ("called viewmenu.GetMenuItems\n"
    #                                        "called menuitem.SetItemLabel with arg 'newname'\n")
    #     # maar hoe weet ik nu dat-ie de juiste gedaan heeft?

    # def _test_check_next_viewmenu_option(self, monkeypatch, capsys):
    #     """unittest for MainGui.check_next_viewmenu_option
    #     """
    #     def mock_get():
    #         return ('0', '1', '2', '3', '4', '5', '6', menuitem1, menuitem2, menuitem3)
    #     class MockMenuItem:
    #         def __init__(self, *args):
    #             if args:
    #                 self._text = args[0]
    #         def GetId(self):
    #             print('called menuitem.GetId')
    #             return self._text[0]
    #         def GetItemLabelText(self):
    #             print('called menuitem.GetItemLabelText')
    #             return self._text[1:]
    #         def IsChecked(self):
    #             print('called menuitem.IsChecked')
    #             return self._text == '1one'
    #         def Check(self, value=True):
    #             print(f'called menuitem.check with arg {value}')
    #     menuitem1 = MockMenuItem('1one')
    #     menuitem2 = MockMenuItem('2two')
    #     menuitem3 = MockMenuItem('3three')
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.viewmenu = types.SimpleNamespace(actions=mock_get)
    #     testobj.check_next_viewmenu_option()
    #     assert capsys.readouterr().out == ("called menuitem.IsChecked\n"
    #                                        "called menuitem.check with arg False\n"
    #                                        "called menuitem.IsChecked\n"
    #                                        "called menuitem.check with arg True\n")
    #     testobj.check_next_viewmenu_option(prev=True)
    #     assert capsys.readouterr().out == ("called menuitem.IsChecked\n"
    #                                        "called menuitem.IsChecked\n"
    #                                        "called menuitem.IsChecked\n"
    #                                        "called menuitem.check with arg False\n"
    #                                        "called menuitem.check with arg True\n")

    # def _test_remove_viewmenu_option(self, monkeypatch, capsys):
    #     """unittest for MainGui.update_removedview
    #     """
    #     def mock_get():
    #         return ('0', '1', '2', '3', '4', '5', '6', menuitem1, menuitem2, menuitem3)
    #     class MockMenuItem:
    #         def __init__(self, *args):
    #             if args:
    #                 self._text = args[0]
    #         def GetId(self):
    #             print('called menuitem.GetId')
    #             return self._text[0]
    #         def GetItemLabelText(self):
    #             print('called menuitem.GetItemLabelText')
    #             return self._text[1:]
    #         def IsChecked(self):
    #             print('called menuitem.IsChecked')
    #             return self._text == '1one'
    #         def Check(self, value=True):
    #             print(f'called menuitem.check with arg {value}')
    #     menuitem1 = MockMenuItem('1one')
    #     menuitem2 = MockMenuItem('2two')
    #     menuitem3 = MockMenuItem('3three')
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.viewmenu = types.SimpleNamespace(actions=mock_get)
    #     assert testobj.remove_viewmenu_option(viewname) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_get_viewmenu_get(self, monkeypatch, capsys):
        """unittest for MainGui.get_viewmenu_options
        """
        def mock_get():
            print('called menu.actions')
            return ('xxx', 'yyy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu = types.SimpleNamespace(GetMenuItems=mock_get)
        assert testobj.get_viewmenu_options() == ['xxx', 'yyy']
        assert capsys.readouterr().out == "called menu.actions\n"

    def test_get_viewmenuoption_state(self, monkeypatch, capsys):
        """unittest for MainGui.get_viewmenuoption_state
        """
        item = mockwx.MockMenuItem()
        assert capsys.readouterr().out == "called MenuItem.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_viewmenuoption_state(item) == 'value'
        assert capsys.readouterr().out == "called menuitem.IsChecked\n"

    def test_get_menuitem_text(self, monkeypatch, capsys):
        """unittest for MainGui.get_menuitem_text
        """
        def mock_get():
            print('called menuitem.GetItemLabelText')
            return 'xxx'
        item = mockwx.MockMenuItem()
        assert capsys.readouterr().out == "called MenuItem.__init__ with args () {}\n"
        item.GetItemLabelText = mock_get
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_menuitem_text(item) == 'xxx'
        assert capsys.readouterr().out == "called menuitem.GetItemLabelText\n"

    def test_set_menuitem_text(self, monkeypatch, capsys):
        """unittest for MainGui.set_menuitem_text
        """
        item = mockwx.MockMenuItem()
        assert capsys.readouterr().out == "called MenuItem.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_menuitem_text(item, 'naam')
        assert capsys.readouterr().out == "called menuitem.SetItemLabel with arg 'naam'\n"

    def test_remove_menuoption(self, monkeypatch, capsys):
        """unittest for MainGui.remove_menuoption
        """
        menu = mockwx.MockMenu()
        item = mockwx.MockMenuItem()
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called MenuItem.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_menuoption(menu, item)
        assert capsys.readouterr().out == f"called menu.Delete with args ({item},)\n"

    def _test_tree_undo(self, monkeypatch, capsys):
        """unittest for MainGui.tree_undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.tree_undo() == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def _test_tree_redo(self, monkeypatch, capsys):
        """unittest for MainGui.tree_redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.tree_redo() == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def _test_find_needle(self, monkeypatch, capsys):
        """unittest for MainGui.find_needle
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_needle(haystack) == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def _test_goto_searchresult(self, monkeypatch, capsys):
        """unittest for MainGui.goto_searchresult
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.goto_searchresult(loc) == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def _test_forward_event(self, monkeypatch, capsys):
        """unittest for MainGui.forward_event
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.forward_event(evt) == "expected_result"
        assert capsys.readouterr().out == ("")
        # disabled

    def test_on_key(self, monkeypatch, capsys):
        """unittest for MainGui.on_key
        """
        def mock_close():
            print('called MainGui.close')
        def mock_delete():
            print('called MainGui.delete_item')
        class MockEvent:
            def GetKeyCode(self):
                print('called event.GetKeyCode')
                return event_key
            def GetEventObject(self):
                print('called event.GetEventObject')
                return event_obj
            def Skip(self):
                print('called event.Skip')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close = mock_close
        testobj.delete_item = mock_delete
        testobj.master = types.SimpleNamespace(opts={'EscapeClosesApp': False})
        testobj.tree = 'tree'
        event = MockEvent()
        event_key = testee.wx.WXK_ESCAPE
        event_obj = 'editor'
        testobj.on_key(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called event.GetEventObject\n"
                                           "called event.Skip\n")
        testobj.master.opts['EscapeClosesApp'] = True
        testobj.on_key(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called event.GetEventObject\n"
                                           "called MainGui.close\n"
                                           "called event.Skip\n")
        event_key = testee.wx.WXK_DELETE
        testobj.on_key(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called event.GetEventObject\n"
                                           "called event.Skip\n")
        event_obj = 'tree'
        testobj.on_key(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called event.GetEventObject\n"
                                           "called MainGui.delete_item\n")
        event_key = 'something else'
        testobj.on_key(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called event.GetEventObject\n"
                                           "called event.Skip\n")

    def test_OnSelChanged(self, monkeypatch, capsys):
        """unittest for MainGui.OnSelChanged
        """
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockMainWindow()
        testobj.OnSelChanged(event)
        assert capsys.readouterr().out == ("called event.GetItem\n"
                                           "called Editor.check_active\n"
                                           "called Editor.activate_item with arg treeitem\n"
                                           "called event.Skip\n")

    def _test_add_escape_action(self, monkeypatch, capsys):
        """unittest for MainGui.add_escape_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_escape_action() == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def _test_remove_escape_action(self, monkeypatch, capsys):
        """unittest for MainGui.remove_escape_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_escape_action() == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented


class TestTreePanel:
    """unittest for wxgui.TreePanel
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.TreePanel object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TreePanel.__init__ with args', args)
        monkeypatch.setattr(testee.TreePanel, '__init__', mock_init)
        testobj = testee.TreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()\n'
        return testobj

    def test_OnDrop(self, monkeypatch, capsys):
        """unittest for TreePanel.OnDrop
        """
        monkeypatch.setattr(testee.wx.TreeCtrl, 'GetRootItem', mockwx.MockTree.GetRootItem)
        monkeypatch.setattr(testee.wx.TreeCtrl, 'Delete', mockwx.MockTree.Delete)
        monkeypatch.setattr(testee.wx.TreeCtrl, 'Expand', mockwx.MockTree.Expand)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = 'root'
        testobj.controller = MockMainWindow()
        testobj.OnDrop('rootitem', 'dragitem')
        assert capsys.readouterr().out == "called tree.GetRootItem\n"
        testobj.OnDrop(None, 'dragitem')
        assert capsys.readouterr().out == (
                "called tree.GetRootItem\n"
                f"called Editor.getsubtree with args ({testobj}, 'dragitem') {{}}\n"
                "called tree.Delete with args ('dragitem',)\n"
                f"called Editor.putsubtree with args ({testobj}, 'root') {{}}\n"
                "called tree.Expand with args ('root',)\n")
        testobj.OnDrop('dropitem', 'dragitem')
        assert capsys.readouterr().out == (
                "called tree.GetRootItem\n"
                f"called Editor.getsubtree with args ({testobj}, 'dragitem') {{}}\n"
                "called tree.Delete with args ('dragitem',)\n"
                f"called Editor.putsubtree with args ({testobj}, 'dropitem') {{}}\n"
                "called tree.Expand with args ('dropitem',)\n")

    def _test_create_popupmenu(self, monkeypatch, capsys):
        """unittest for TreePanel.create_popupmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_popupmenu(item) == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def test_add_to_parent(self, monkeypatch, capsys):
        """unittest for TreePanel.add_to_parent
        """
        def mock_append(*args):
            print('called TreePanel.AppendItem with arg', args)
            return 'appended'
        def mock_insert(*args):
            print('called TreePanel.InsertItem with arg', args)
            return 'inserted'
        def mock_setkey(*args):
            print('called TreePanel.setitemkey with args', args)
        def mock_settext(*args):
            print('called TreePanel.setitemtext with args', args)
        monkeypatch.setattr(testee.wx, 'TreeCtrl', mockwx.MockTree)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.AppendItem = mock_append
        testobj.InsertItem = mock_insert
        testobj.setitemkey = mock_setkey
        testobj.setitemtext = mock_settext
        assert testobj.add_to_parent('itemkey', 'titel', 'parent') == "appended"
        assert capsys.readouterr().out == (
                "called TreePanel.AppendItem with arg ('parent', 'titel')\n"
                "called TreePanel.setitemkey with args ('appended', 'itemkey')\n"
                "called TreePanel.setitemtext with args ('appended', '')\n")
        assert testobj.add_to_parent('itemkey', 'titel', 'parent', pos=2) == "inserted"
        assert capsys.readouterr().out == (
                "called TreePanel.InsertItem with arg ('parent', 2, 'titel')\n"
                "called TreePanel.setitemkey with args ('inserted', 'itemkey')\n"
                "called TreePanel.setitemtext with args ('inserted', '')\n")

    def test_getitemdata(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemdata
        """
        def mock_getkey(*args):
            print('called TreePanel.getitemkey with args', args)
            return 'item key'
        def mock_gettitle(*args):
            print('called TreePanel.getitemtitle with args', args)
            return 'item title'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getitemkey = mock_getkey
        testobj.getitemtitle = mock_gettitle
        assert testobj.getitemdata('item') == ('item title', 'item key')
        assert capsys.readouterr().out == ("called TreePanel.getitemtitle with args ('item',)\n"
                                           "called TreePanel.getitemkey with args ('item',)\n")

    def test_getitemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemtext
        """
        def mock_get(*args):
            print('called TreePanel.GetItemData with args', args)
            return 'xx', 'yy'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetItemData = mock_get
        assert testobj.getitemtext('item') == "yy"
        assert capsys.readouterr().out == "called TreePanel.GetItemData with args ('item',)\n"

    def test_getitemtitle(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemtitle
        """
        def mock_get(*args):
            print('called TreePanel.GetItemText with args', args)
            return 'qq'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetItemText = mock_get
        assert testobj.getitemtitle('item') == "qq"
        assert capsys.readouterr().out == "called TreePanel.GetItemText with args ('item',)\n"

    def test_getitemkey(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemkey
        """
        def mock_get(*args):
            print('called TreePanel.GetItemData with args', args)
            return ''
        def mock_get_2(*args):
            print('called TreePanel.GetItemData with args', args)
            return 'xx', 'yy'
        def mock_get_3(*args):
            print('called TreePanel.GetItemData with args', args)
            return '1', 'yy'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetItemData = mock_get
        assert testobj.getitemkey('item') is None
        assert capsys.readouterr().out == "called TreePanel.GetItemData with args ('item',)\n"
        testobj.GetItemData = mock_get_2
        assert testobj.getitemkey('item') == -1
        assert capsys.readouterr().out == "called TreePanel.GetItemData with args ('item',)\n"
        testobj.GetItemData = mock_get_3
        assert testobj.getitemkey('item') == 1
        assert capsys.readouterr().out == "called TreePanel.GetItemData with args ('item',)\n"

    def test_setitemkey(self, monkeypatch, capsys):
        """unittest for TreePanel.setitemkey
        """
        def mock_get(*args):
            print('called TreePanel.GetItemData with args', args)
            return 'xx', 'yy'
        def mock_set(*args):
            print('called TreePanel.SetItemData with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetItemData = mock_get
        testobj.SetItemData = mock_set
        testobj.setitemkey('item', 'key')
        assert capsys.readouterr().out == (
                "called TreePanel.GetItemData with args ('item',)\n"
                "called TreePanel.SetItemData with args ('item', ('key', 'yy'))\n")

    def test_setitemtitle(self, monkeypatch, capsys):
        """unittest for TreePanel.setitemtitle
        """
        def mock_set(*args):
            print('called TreePanel.SetItemText with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.SetItemText = mock_set
        testobj.setitemtitle('item', 'title')
        assert capsys.readouterr().out == (
                "called TreePanel.SetItemText with args ('item', 'title')\n")

    def test_setitemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.setitemtext
        """
        def mock_get(*args):
            print('called TreePanel.GetItemData with args', args)
            return 'xx', 'yy'
        def mock_set(*args):
            print('called TreePanel.SetItemData with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetItemData = mock_get
        testobj.SetItemData = mock_set
        testobj.setitemtext('item', 'text')
        assert capsys.readouterr().out == (
                "called TreePanel.GetItemData with args ('item',)\n"
                "called TreePanel.SetItemData with args ('item', ('xx', 'text'))\n")

    def test_getitemkids(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemkids
        """
        def mock_getfirst(*args):
            print('called TreePanel.GetFirstChild with args', args)
            return no_item, -1
        def mock_getfirst_2(*args):
            print('called TreePanel.GetFirstChild with args', args)
            return first_item, 0
        def mock_getnext(*args):
            print('called TreePanel.GetNextChild with args', args)
            if args[1] == 0:
                return next_item, 1
            return no_item, -1
        no_item = mockwx.MockTreeItem('not ok')
        first_item = mockwx.MockTreeItem('first')
        next_item = mockwx.MockTreeItem('next')
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.__init__ with args ('next',)\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetFirstChild = mock_getfirst
        testobj.GetNextChild = mock_getnext
        assert testobj.getitemkids('item') == []
        assert capsys.readouterr().out == ("called TreePanel.GetFirstChild with args ('item',)\n"
                                           "called TreeItem.IsOk\n")
        testobj.GetFirstChild = mock_getfirst_2
        assert testobj.getitemkids('item') == [first_item, next_item]
        assert capsys.readouterr().out == ("called TreePanel.GetFirstChild with args ('item',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called TreePanel.GetNextChild with args ('item', 0)\n"
                                           "called TreeItem.IsOk\n"
                                           "called TreePanel.GetNextChild with args ('item', 1)\n"
                                           "called TreeItem.IsOk\n")

    def test_getitemparentpos(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemparentpos
        """
        def mock_get(*args):
            print('called TreePanel.GetItemParent with args', args)
            return no_item
        def mock_get_2(*args):
            print('called TreePanel.GetItemParent with args', args)
            return parent
        def mock_getfirst(*args):
            print('called TreePanel.GetFirstChild with args', args)
            return no_item, -1
        def mock_getfirst_2(*args):
            print('called TreePanel.GetFirstChild with args', args)
            return first_item, 0
        def mock_getnext(*args):
            print('called TreePanel.GetNextChild with args', args)
            if args[1] == 0:
                return next_item, 1
            return no_item, -1
        no_item = mockwx.MockTreeItem('not ok')
        parent = mockwx.MockTreeItem('parent')
        first_item = mockwx.MockTreeItem('first')
        next_item = mockwx.MockTreeItem('next')
        last_item = mockwx.MockTreeItem('last')
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.__init__ with args ('parent',)\n"
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.__init__ with args ('next',)\n"
                                           "called TreeItem.__init__ with args ('last',)\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetItemParent = mock_get
        testobj.GetFirstChild = mock_getfirst
        testobj.GetNextChild = mock_getnext
        assert testobj.getitemparentpos('item') == ('item', -1)      # root, no parent
        assert capsys.readouterr().out == ("called TreePanel.GetItemParent with args ('item',)\n"
                                           "called TreeItem.IsOk\n")
        testobj.GetItemParent = mock_get_2
        # impossible: if we can get to the parent, the parent must have children
        assert testobj.getitemparentpos('item') == (parent, 0)  # parent has no children
        assert capsys.readouterr().out == ("called TreePanel.GetItemParent with args ('item',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called TreePanel.GetFirstChild with args (parent,)\n"
                                           "called TreeItem.IsOk\n")
        testobj.GetFirstChild = mock_getfirst_2
        # impossible: if we can get the parent, "this" item must be one of its children
        assert testobj.getitemparentpos('item') == (parent, 2)  # parent has no child "item"
        assert capsys.readouterr().out == ("called TreePanel.GetItemParent with args ('item',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called TreePanel.GetFirstChild with args (parent,)\n"
                                           "called TreeItem.IsOk\n"
                                           "called TreePanel.GetNextChild with args (parent, 0)\n"
                                           "called TreeItem.IsOk\n"
                                           "called TreePanel.GetNextChild with args (parent, 1)\n"
                                           "called TreeItem.IsOk\n")
        assert testobj.getitemparentpos(first_item) == (parent, 0)  # first child
        assert capsys.readouterr().out == (
                f"called TreePanel.GetItemParent with args ({first_item},)\n"
                "called TreeItem.IsOk\n"
                "called TreePanel.GetFirstChild with args (parent,)\n"
                "called TreeItem.IsOk\n")
        assert testobj.getitemparentpos(next_item) == (parent, 1)  # next child
        assert capsys.readouterr().out == (
                f"called TreePanel.GetItemParent with args ({next_item},)\n"
                "called TreeItem.IsOk\n"
                "called TreePanel.GetFirstChild with args (parent,)\n"
                "called TreeItem.IsOk\n"
                "called TreePanel.GetNextChild with args (parent, 0)\n"
                "called TreeItem.IsOk\n")
        assert testobj.getitemparentpos(last_item) == (parent, 2)  # last child
        assert capsys.readouterr().out == (
                f"called TreePanel.GetItemParent with args ({last_item},)\n"
                "called TreeItem.IsOk\n"
                "called TreePanel.GetFirstChild with args (parent,)\n"
                "called TreeItem.IsOk\n"
                "called TreePanel.GetNextChild with args (parent, 0)\n"
                "called TreeItem.IsOk\n"
                "called TreePanel.GetNextChild with args (parent, 1)\n"
                "called TreeItem.IsOk\n")

    def test_getselecteditem(self, monkeypatch, capsys):
        """unittest for TreePanel.getselecteditem
        """
        def mock_get():
            print('called tree.GetSelection')
            return 'selection'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetSelection = mock_get
        assert testobj.getselecteditem() == "selection"
        assert capsys.readouterr().out == "called tree.GetSelection\n"

    def test_set_item_expanded(self, monkeypatch, capsys):
        """unittest for TreePanel.set_item_expanded
        """
        def mock_expand(*args):
            print('called tree.Expand with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.Expand = mock_expand
        testobj.set_item_expanded('item')
        assert capsys.readouterr().out == "called tree.Expand with args ('item',)\n"

    def test_set_item_collapsed(self, monkeypatch, capsys):
        """unittest for TreePanel.set_item_collapsed
        """
        def mock_collapse(*args):
            print('called tree.Collapse with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.Collapse = mock_collapse
        testobj.set_item_collapsed('item')
        assert capsys.readouterr().out == "called tree.Collapse with args ('item',)\n"

    def test_set_item_selected(self, monkeypatch, capsys):
        """unittest for TreePanel.set_item_selected
        """
        def mock_set(*args):
            print('called tree.SetFocusedItem with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.SetFocusedItem = mock_set
        testobj.set_item_selected('item')
        assert capsys.readouterr().out == "called tree.SetFocusedItem with args ('item',)\n"

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for TreePanel.get_selected_item
        """
        def mock_get(*args):
            print('called tree.GetFocusedItem')
            return 'focusitem'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetFocusedItem = mock_get
        assert testobj.get_selected_item() == "focusitem"
        assert capsys.readouterr().out == "called tree.GetFocusedItem\n"

    def test_removeitem(self, monkeypatch, capsys):
        """unittest for TreePanel.removeitem
        """
        def mock_pop(*args):
            print('called MainWindow.popitems with args', args)
        def mock_getpp(*args):
            print('called treepanel.getitemparentpos with args', args)
            return parent, 'pos'
        def mock_get_prev(*args):
            print('called treepanel.GetPrevSibling with args', args)
            return previtem
        def mock_get_next(*args):
            print('called treepanel.GetNextSibling with args', args)
            return nextitem
        def mock_delete(*args):
            print('called treepanel.Delete with args', args)
        def mock_isok(self):
            print('called TreeItem.IsOk')
            return False
        previtem = mockwx.MockTreeItem('prev')
        nextitem = mockwx.MockTreeItem('next')
        parentitem = mockwx.MockTreeItem('parent')
        rootitem = mockwx.MockTreeItem('root')
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('prev',)\n"
                                           "called TreeItem.__init__ with args ('next',)\n"
                                           "called TreeItem.__init__ with args ('parent',)\n"
                                           "called TreeItem.__init__ with args ('root',)\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(master=types.SimpleNamespace(popitems=mock_pop))
        testobj.getitemparentpos = mock_getpp
        testobj.GetPrevSibling = mock_get_prev
        testobj.GetNextSibling = mock_get_next
        testobj.Delete = mock_delete
        testobj.root = rootitem
        parent = parentitem
        assert testobj.removeitem('item', 'cut_from_itemdict') == ((parent, 'pos'), previtem)
        assert capsys.readouterr().out == (
                "called treepanel.getitemparentpos with args ('item',)\n"
                "called treepanel.GetPrevSibling with args ('item',)\n"
                "called TreeItem.IsOk\n"
                "called MainWindow.popitems with args ('item', 'cut_from_itemdict')\n"
                "called treepanel.Delete with args ('item',)\n")
        monkeypatch.setattr(mockwx.MockTreeItem, 'IsOk', mock_isok)
        assert testobj.removeitem('item', 'cut_from_itemdict') == ((parent, 'pos'), parent)
        assert capsys.readouterr().out == (
                "called treepanel.getitemparentpos with args ('item',)\n"
                "called treepanel.GetPrevSibling with args ('item',)\n"
                "called TreeItem.IsOk\n"
                "called MainWindow.popitems with args ('item', 'cut_from_itemdict')\n"
                "called treepanel.Delete with args ('item',)\n")
        parent = rootitem
        assert testobj.removeitem('item', 'cut_from_itemdict') == ((rootitem, 'pos'), nextitem)
        assert capsys.readouterr().out == (
                "called treepanel.getitemparentpos with args ('item',)\n"
                "called treepanel.GetPrevSibling with args ('item',)\n"
                "called TreeItem.IsOk\n"
                "called treepanel.GetNextSibling with args ('item',)\n"
                "called MainWindow.popitems with args ('item', 'cut_from_itemdict')\n"
                "called treepanel.Delete with args ('item',)\n")

    # def _test_getsubtree(self, monkeypatch, capsys):
    #     """unittest for TreePanel.getsubtree
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.getsubtree(item, itemlist=None) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    # def _test_putsubtree(self, monkeypatch, capsys):
    #     """unittest for TreePanel.putsubtree
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.putsubtree(parent, titel, key, subtree=None, pos=-1) == "expected_result"
    #     assert capsys.readouterr().out == ("")


class TestEditorPanel:
    """unittest for wxgui.EditorPanel
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.EditorPanel object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EditorPanel.__init__ with args', args)
        monkeypatch.setattr(testee.EditorPanel, '__init__', mock_init)
        testobj = testee.EditorPanel()
        assert capsys.readouterr().out == 'called EditorPanel.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EditorPanel.__init__
        """
        def mock_mark(self, value):
            print('called EditorPanel.mark_sirty with arg {value}')
        monkeypatch.setattr(testee.rt, 'RichTextCtrl', mockwx.MockEditor)
        monkeypatch.setattr(testee.rt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.EditorPanel, 'mark_dirty', mock_mark)
        parent = types.SimpleNamespace(parent=types.SimpleNamespace())
        testobj = testee.EditorPanel(parent)
        assert testobj.parent_ == parent
        assert testobj.paragraph_indent == 100
        assert testobj.parspace_increment == 20
        assert capsys.readouterr().out == (
                f"called Editor.__init__ with args ({parent},) {{'style': -1071644672}}\n"
                "called RichTextAttr.__init__\n"
                "called EditorPanel.mark_sirty with arg {value}\n")

    def test_set_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_contents
        """
        monkeypatch.setattr(testee.rt, 'RichTextXMLHandler', mockwx.MockHandler)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'Clear', mockwx.MockTextCtrl.Clear)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetValue', mockwx.MockTextCtrl.SetValue)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'Refresh', mockwx.MockTextCtrl.Refresh)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetBuffer', mockwx.MockTextCtrl.GetBuffer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_contents('data')
        assert capsys.readouterr().out == ("called text.Clear\n"
                                           "called text.SetValue with args ('data',)\n"
                                           "called text.Refresh\n")
        testobj.set_contents("<?xml data")
        handler, buffer, tmpfilename = testobj.teststuff
        assert capsys.readouterr().out == (
                "called text.Clear\n"
                "called RichTextXMLHandler.__init__\n"
                "called text.GetBuffer\n"
                "called RichTextBuffer.__init__\n"
                f"called RichTextBuffer.AddHandler with args ({handler},)\n"
                f"called RichTextXMLHandler.LoadFile with args ({buffer}, '{tmpfilename}')\n"
                "called text.Refresh\n")

    def test_get_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.get_contents
        """
        def mock_save(self, *args):
            print('called RichTextXMLHandler.SaveFile with args', args)
            with open(args[1], 'w') as out:
                out.write('value from textctrl')
        monkeypatch.setattr(testee.rt, 'RichTextXMLHandler', mockwx.MockHandler)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetBuffer', mockwx.MockTextCtrl.GetBuffer)
        monkeypatch.setattr(mockwx.MockHandler, 'SaveFile', mock_save)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_contents() == "value from textctrl"
        handler, buffer, tmpfilename = testobj.teststuff
        assert capsys.readouterr().out == (
                "called RichTextXMLHandler.__init__\n"
                "called text.GetBuffer\n"
                "called RichTextBuffer.__init__\n"
                f"called RichTextBuffer.AddHandler with args ({handler},)\n"
                f"called RichTextXMLHandler.SaveFile with args ({buffer}, '{tmpfilename}')\n")

    def test_get_text_position(self, monkeypatch, capsys):
        """unittest for EditorPanel.get_text_position
        """
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetInsertionPoint',
                            mockwx.MockEditor.GetInsertionPoint)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_text_position() == "insert here"
        assert capsys.readouterr().out == "called editor.GetInsertionPoint\n"

    def test_set_text_position(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_text_position
        """
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetInsertionPoint',
                            mockwx.MockEditor.SetInsertionPoint)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'ScrollIntoView',
                            mockwx.MockEditor.ScrollIntoView)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_text_position('pos')
        assert capsys.readouterr().out == ("called editor.SetInsertionPoint with args ('pos',)\n"
                                           "called editor.ScrollIntoView with args ('pos', 0)\n")

    def test_undo(self, monkeypatch, capsys):
        """unittest for EditorPanel.undo
        """
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'Undo', mockwx.MockEditor.Undo)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo('evt')
        assert capsys.readouterr().out == "called editor.Undo\n"

    def test_redo(self, monkeypatch, capsys):
        """unittest for EditorPanel.redo
        """
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'Redo', mockwx.MockEditor.Redo)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.redo('evt')
        assert capsys.readouterr().out == "called editor.Redo\n"

    def test_cut(self, monkeypatch, capsys):
        """unittest for EditorPanel.cut
        """
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'Cut', mockwx.MockEditor.Cut)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cut('evt')
        assert capsys.readouterr().out == "called editor.Cut\n"

    def test_copy(self, monkeypatch, capsys):
        """unittest for EditorPanel.copy
        """
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'Copy', mockwx.MockEditor.Copy)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.copy('evt')
        assert capsys.readouterr().out == "called editor.Copy\n"

    def test_paste(self, monkeypatch, capsys):
        """unittest for EditorPanel.paste
        """
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'Paste', mockwx.MockEditor.Paste)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.paste('evt')
        assert capsys.readouterr().out == "called editor.Paste\n"

    def test_select_all(self, monkeypatch, capsys):
        """unittest for EditorPanel.select_all
        """
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SelectAll', mockwx.MockEditor.SelectAll)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_all()
        assert capsys.readouterr().out == "called editor.SelectAll\n"

    def test_clear(self, monkeypatch, capsys):
        """unittest for EditorPanel.clear
        """
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'Clear', mockwx.MockEditor.Clear)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear()
        assert capsys.readouterr().out == "called editor.Clear\n"

    def test_text_bold(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_bold
        """
        def mock_apply():
            print('called Editor.ApplyBoldToSelection')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ApplyBoldToSelection = mock_apply
        testobj.text_bold('evt')
        assert capsys.readouterr().out == "called Editor.ApplyBoldToSelection\n"

    def test_text_italic(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_italic
        """
        def mock_apply():
            print('called Editor.ApplyItalicToSelection')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ApplyItalicToSelection = mock_apply
        testobj.text_italic('evt')
        assert capsys.readouterr().out == "called Editor.ApplyItalicToSelection\n"

    def test_text_underline(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_underline
        """
        def mock_apply():
            print('called Editor.ApplyUnderlineToSelection')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ApplyUnderlineToSelection = mock_apply
        testobj.text_underline('evt')
        assert capsys.readouterr().out == "called Editor.ApplyUnderlineToSelection\n"

    def test_text_strikethrough(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_strikethrough
        """
        def mock_has():
            print('called Editor.HasSelection')
            return False
        def mock_has_2():
            print('called Editor.HasSelection')
            return True
        monkeypatch.setattr(testee.rt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetStyle', mockwx.MockEditor.SetStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'BeginStyle', mockwx.MockEditor.BeginStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetSelectionRange',
                            mockwx.MockEditor.GetSelectionRange)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HasSelection = mock_has
        testobj.text_strikethrough('evt')
        assert capsys.readouterr().out == ("called RichTextAttr.__init__\n"
                                           "called RichTextAttr.SetFlags with args (134217728,)\n"
                                           "called Editor.HasSelection\n"
                                           "called editor.BeginStyle with args (richtextattr,)\n")
        testobj.HasSelection = mock_has_2
        testobj.text_strikethrough('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (134217728,)\n"
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called editor.SetStyle with args ('range', richtextattr)\n")

    def test_align_left(self, monkeypatch, capsys):
        """unittest for EditorPanel.align_left
        """
        def mock_apply(arg):
            print(f'called Editor.ApplyAlignmentToSelection with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ApplyAlignmentToSelection = mock_apply
        testobj.align_left('evt')
        assert capsys.readouterr().out == "called Editor.ApplyAlignmentToSelection with arg 1\n"

    def test_align_center(self, monkeypatch, capsys):
        """unittest for EditorPanel.align_center
        """
        def mock_apply(arg):
            print(f'called Editor.ApplyAlignmentToSelection with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ApplyAlignmentToSelection = mock_apply
        testobj.align_center('evt')
        assert capsys.readouterr().out == "called Editor.ApplyAlignmentToSelection with arg 2\n"

    def test_align_right(self, monkeypatch, capsys):
        """unittest for EditorPanel.align_right
        """
        def mock_apply(arg):
            print(f'called Editor.ApplyAlignmentToSelection with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ApplyAlignmentToSelection = mock_apply
        testobj.align_right('evt')
        assert capsys.readouterr().out == "called Editor.ApplyAlignmentToSelection with arg 3\n"

    def test_text_justify(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_justify
        """
        def mock_show(*args):
            print('called show_message with args', args)
        monkeypatch.setattr(testee, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = 'parent'
        testobj.text_justify('evt')
        assert capsys.readouterr().out == (
                "called show_message with args"
                " ('parent', 'Sorry, Not possible in WxPython at this time')\n")

    def test_indent_more(self, monkeypatch, capsys):
        """unittest for EditorPanel.indent_more
        """
        def mock_get(*args):
            print('called Editor.GetStyle with args', args)
            return False
        def mock_get_2(*args):
            print('called Editor.GetStyle with args', args)
            return True
        def mock_has():
            print('called Editor.HasSelection')
            return False
        def mock_has_2():
            print('called Editor.HasSelection')
            return True
        def mock_indent(self):
            print('called RichTextAttr.GetLeftIndent')
            return 100
        monkeypatch.setattr(testee.rt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.rt.RichTextAttr, 'GetLeftIndent', mock_indent)
        monkeypatch.setattr(testee.rt, 'RichTextRange', mockwx.MockTextRange)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetStyle', mockwx.MockEditor.SetStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetInsertionPoint',
                            mockwx.MockEditor.GetInsertionPoint)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetSelectionRange',
                            mockwx.MockEditor.GetSelectionRange)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetStyle = mock_get
        testobj.HasSelection = mock_has
        testobj.paragraph_indent = 20
        testobj.indent_more('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n")
        testobj.GetStyle = mock_get_2
        testobj.paragraph_indent = 20
        testobj.indent_more('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called RichTextAttr.GetLeftIndent\n"
                "called RichTextAttr.SetLeftIndent with args (120,)\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.SetStyle with args (richtextrange, richtextattr)\n")
        testobj.HasSelection = mock_has_2
        testobj.paragraph_indent = 20
        testobj.indent_more('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called RichTextAttr.GetLeftIndent\n"
                "called RichTextAttr.SetLeftIndent with args (120,)\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.SetStyle with args ('range', richtextattr)\n")

    def test_indent_less(self, monkeypatch, capsys):
        """unittest for EditorPanel.indent_less
        """
        def mock_get(*args):
            print('called Editor.GetStyle with args', args)
            return False
        def mock_get_2(*args):
            print('called Editor.GetStyle with args', args)
            return True
        def mock_has():
            print('called Editor.HasSelection')
            return False
        def mock_has_2():
            print('called Editor.HasSelection')
            return True
        def mock_indent(self):
            print('called RichTextAttr.GetLeftIndent')
            return 100
        monkeypatch.setattr(testee.rt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.rt.RichTextAttr, 'GetLeftIndent', mock_indent)
        monkeypatch.setattr(testee.rt, 'RichTextRange', mockwx.MockTextRange)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetStyle', mockwx.MockEditor.SetStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetInsertionPoint',
                            mockwx.MockEditor.GetInsertionPoint)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetSelectionRange',
                            mockwx.MockEditor.GetSelectionRange)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetStyle = mock_get
        testobj.HasSelection = mock_has
        testobj.paragraph_indent = 20
        testobj.indent_less('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n")
        testobj.GetStyle = mock_get_2
        testobj.indent_less('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called RichTextAttr.GetLeftIndent\n"
                "called RichTextAttr.SetLeftIndent with args (80,)\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.SetStyle with args (richtextrange, richtextattr)\n")
        testobj.HasSelection = mock_has_2
        testobj.indent_less('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called RichTextAttr.GetLeftIndent\n"
                "called RichTextAttr.SetLeftIndent with args (80,)\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.SetStyle with args ('range', richtextattr)\n")
        testobj.paragraph_indent = 120
        testobj.indent_less('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (256,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called RichTextAttr.GetLeftIndent\n")

    def test_increase_parspacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.increase_parspacing_more
        """
        def mock_get(*args):
            print('called Editor.GetStyle with args', args)
            return False
        def mock_get_2(*args):
            print('called Editor.GetStyle with args', args)
            return True
        def mock_has():
            print('called Editor.HasSelection')
            return False
        def mock_has_2():
            print('called Editor.HasSelection')
            return True
        def mock_spacing(self):
            print('called RichTextAttr.GetParagraphSpacingAfter')
            return 100
        monkeypatch.setattr(testee.rt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.rt.RichTextAttr, 'GetParagraphSpacingAfter', mock_spacing)
        monkeypatch.setattr(testee.rt, 'RichTextRange', mockwx.MockTextRange)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetStyle', mockwx.MockEditor.SetStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetInsertionPoint',
                            mockwx.MockEditor.GetInsertionPoint)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetSelectionRange',
                            mockwx.MockEditor.GetSelectionRange)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetStyle = mock_get
        testobj.HasSelection = mock_has
        testobj.parspace_increment = 20
        testobj.increase_parspacing('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n")
        testobj.GetStyle = mock_get_2
        testobj.increase_parspacing('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.SetParagraphSpacingAfter with args (120,)\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.SetStyle with args (richtextrange, richtextattr)\n")
        testobj.HasSelection = mock_has_2
        testobj.increase_parspacing('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.SetParagraphSpacingAfter with args (120,)\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.SetStyle with args ('range', richtextattr)\n")

    def test_decrease_parspacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.decrease_parspacing_less
        """
        def mock_get(*args):
            print('called Editor.GetStyle with args', args)
            return False
        def mock_get_2(*args):
            print('called Editor.GetStyle with args', args)
            return True
        def mock_has():
            print('called Editor.HasSelection')
            return False
        def mock_has_2():
            print('called Editor.HasSelection')
            return True
        def mock_spacing(self):
            print('called RichTextAttr.GetParagraphSpacingAfter')
            return 100
        monkeypatch.setattr(testee.rt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.rt.RichTextAttr, 'GetParagraphSpacingAfter', mock_spacing)
        monkeypatch.setattr(testee.rt, 'RichTextRange', mockwx.MockTextRange)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetStyle', mockwx.MockEditor.SetStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetInsertionPoint',
                            mockwx.MockEditor.GetInsertionPoint)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetSelectionRange',
                            mockwx.MockEditor.GetSelectionRange)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetStyle = mock_get
        testobj.HasSelection = mock_has
        testobj.parspace_increment = 20
        testobj.decrease_parspacing('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n")
        testobj.GetStyle = mock_get_2
        testobj.decrease_parspacing('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.SetParagraphSpacingAfter with args (80,)\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.SetStyle with args (richtextrange, richtextattr)\n")
        testobj.HasSelection = mock_has_2
        testobj.decrease_parspacing('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n"
                "called RichTextAttr.SetParagraphSpacingAfter with args (80,)\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.SetStyle with args ('range', richtextattr)\n")
        testobj.parspace_increment = 120
        testobj.decrease_parspacing('evt')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (2048,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called RichTextAttr.GetParagraphSpacingAfter\n")

    def test_set_linespacing_10(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_linespacing_10
        """
        def mock_set(*args):
            print('called Editor.set_linespacing with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_linespacing = mock_set
        testobj.set_linespacing_10('evt')
        assert capsys.readouterr().out == "called Editor.set_linespacing with args (10,)\n"

    def test_set_linespacing_15(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_linespacing_15
        """
        def mock_set(*args):
            print('called Editor.set_linespacing with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_linespacing = mock_set
        testobj.set_linespacing_15('evt')
        assert capsys.readouterr().out == "called Editor.set_linespacing with args (15,)\n"

    def test_set_linespacing_20(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_linespacing_20
        """
        def mock_set(*args):
            print('called Editor.set_linespacing with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_linespacing = mock_set
        testobj.set_linespacing_20('evt')
        assert capsys.readouterr().out == "called Editor.set_linespacing with args (20,)\n"

    def test_set_linespacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_linespacing_10
        """
        def mock_get(*args):
            print('called Editor.GetStyle with args', args)
            return False
        def mock_get_2(*args):
            print('called Editor.GetStyle with args', args)
            return True
        def mock_has():
            print('called Editor.HasSelection')
            return False
        def mock_has_2():
            print('called Editor.HasSelection')
            return True
        monkeypatch.setattr(testee.rt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.rt, 'RichTextRange', mockwx.MockTextRange)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetStyle', mockwx.MockEditor.SetStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetInsertionPoint',
                            mockwx.MockEditor.GetInsertionPoint)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetSelectionRange',
                            mockwx.MockEditor.GetSelectionRange)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.GetStyle = mock_get
        testobj.HasSelection = mock_has
        testobj.set_linespacing('value')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (8192,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n")
        testobj.GetStyle = mock_get_2
        testobj.set_linespacing('value')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (8192,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called RichTextAttr.SetFlags with args (8192,)\n"
                "called RichTextAttr.SetLineSpacing with args ('value',)\n"
                "called editor.SetStyle with args (richtextrange, richtextattr)\n")
        testobj.HasSelection = mock_has_2
        testobj.set_linespacing('value')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (8192,)\n"
                "called editor.GetInsertionPoint\n"
                "called Editor.GetStyle with args ('insert here', richtextattr)\n"
                "called RichTextRange.__init__ with args ('insert here', 'insert here')\n"
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called RichTextAttr.SetFlags with args (8192,)\n"
                "called RichTextAttr.SetLineSpacing with args ('value',)\n"
                "called editor.SetStyle with args ('range', richtextattr)\n")

    def test_text_font(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_font
        """
        def mock_get():
            print('called event.GetFont')
            return testfont
        def mock_has():
            print('called Editor.HasSelection')
            return False
        def mock_has_2():
            print('called Editor.HasSelection')
            return True
        monkeypatch.setattr(testee.rt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetStyle', mockwx.MockEditor.SetStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'BeginFont', mockwx.MockEditor.BeginFont)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetSelectionRange',
                            mockwx.MockEditor.GetSelectionRange)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetFocus', mockwx.MockEditor.SetFocus)
        evt = types.SimpleNamespace(GetFont=mock_get)
        assert capsys.readouterr().out == ""
        testfont = None
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HasSelection = mock_has
        testobj.text_font(evt)
        assert capsys.readouterr().out == ("called event.GetFont\n"
                                           "called RichTextAttr.__init__\n"
                                           "called editor.SetFocus\n")
        testfont = 'xxx'
        testobj.text_font(evt)
        assert capsys.readouterr().out == ("called event.GetFont\n"
                                           "called RichTextAttr.__init__\n"
                                           "called Editor.HasSelection\n"
                                           "called editor.BeginFont with args ('xxx',)\n"
                                           "called editor.SetFocus\n")
        testobj.HasSelection = mock_has_2
        testobj.text_font(evt)
        assert capsys.readouterr().out == (
                "called event.GetFont\n"
                "called RichTextAttr.__init__\n"
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called RichTextAttr.SetFlags with args (503316604,)\n"
                "called RichTextAttr.SetFont with args ('xxx',)\n"
                "called editor.SetStyle with args ('range', richtextattr)\n"
                "called editor.SetFocus\n")

    def _test_enlarge_text(self, monkeypatch, capsys):
        """unittest for EditorPanel.enlarge_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enlarge_text(evt) == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def _test_shrink_text(self, monkeypatch, capsys):
        """unittest for EditorPanel.shrink_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.shrink_text(evt) == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def test_select_text_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.select_text_color
        """
        def mock_getv():
            print('called eventobject.GetValue')
            return colourvalue
        def mock_get():
            print('called event.GetEventObject')
            return types.SimpleNamespace(GetValue=mock_getv)
        def mock_apply(*args):
            print('called editor.applyfgcolour with args', args)
        def mock_change(*args):
            print('called editor.changebitmapbuttoncolour with args', args)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetFocus', mockwx.MockEditor.SetFocus)
        event = types.SimpleNamespace(GetEventObject=mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.applyfgcolour = mock_apply
        testobj.parent_ = types.SimpleNamespace(changebitmapbuttoncolour=mock_change,
                                                fgcset='fgcset')
        colourvalue = ''
        testobj.select_text_color(event)
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called eventobject.GetValue\n"
                                           "called editor.SetFocus\n")
        colourvalue = 'xxx'
        testobj.select_text_color(event)
        assert testobj.parent_.textcolour == 'xxx'
        assert capsys.readouterr().out == (
                "called event.GetEventObject\n"
                "called eventobject.GetValue\n"
                "called editor.applyfgcolour with args ('xxx',)\n"
                "called editor.changebitmapbuttoncolour with args ('fgcset', 'xxx')\n"
                "called editor.SetFocus\n")

    def test_set_text_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_text_color
        """
        def mock_apply(*args):
            print('called editor.applyfgcolour with args', args)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetFocus', mockwx.MockEditor.SetFocus)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.applyfgcolour = mock_apply
        testobj.parent_ = types.SimpleNamespace(textcolour='xxx')
        testobj.set_text_color('evt')
        assert capsys.readouterr().out == ("called editor.applyfgcolour with args ('xxx',)\n"
                                           "called editor.SetFocus\n")

    def test_applyfgcolour(self, monkeypatch, capsys):
        """unittest for EditorPanel.applyfgcolour
        """
        def mock_has():
            print('called Editor.HasSelection')
            return False
        def mock_has_2():
            print('called Editor.HasSelection')
            return True
        monkeypatch.setattr(testee.rt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetStyle', mockwx.MockEditor.SetStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'BeginTextColour',
                            mockwx.MockEditor.BeginTextColour)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetSelectionRange',
                            mockwx.MockEditor.GetSelectionRange)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HasSelection = mock_has
        testobj.applyfgcolour('colour')
        assert capsys.readouterr().out == ("called Editor.HasSelection\n"
                                           "called editor.BeginTextColour with args ('colour',)\n")
        testobj.HasSelection = mock_has_2
        testobj.applyfgcolour('colour')
        assert capsys.readouterr().out == (
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (1,)\n"
                "called RichTextAttr.SetTextColour with args ('colour',)\n"
                "called editor.SetStyle with args ('range', richtextattr)\n")

    def test_background_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.background_color
        """
        def mock_getv():
            print('called eventobject.GetValue')
            return colourvalue
        def mock_get():
            print('called event.GetEventObject')
            return types.SimpleNamespace(GetValue=mock_getv)
        def mock_apply(*args):
            print('called editor.applybgcolour with args', args)
        def mock_change(*args):
            print('called editor.changebitmapbuttoncolour with args', args)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetFocus', mockwx.MockEditor.SetFocus)
        event = types.SimpleNamespace(GetEventObject=mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.applybgcolour = mock_apply
        testobj.parent_ = types.SimpleNamespace(changebitmapbuttoncolour=mock_change,
                                                bgcset='bgcset')
        colourvalue = ''
        testobj.select_background_color(event)
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called eventobject.GetValue\n"
                                           "called editor.SetFocus\n")
        colourvalue = 'xxx'
        testobj.select_background_color(event)
        assert testobj.parent_.backgroundcolour == 'xxx'
        assert capsys.readouterr().out == (
                "called event.GetEventObject\n"
                "called eventobject.GetValue\n"
                "called editor.applybgcolour with args ('xxx',)\n"
                "called editor.changebitmapbuttoncolour with args ('bgcset', 'xxx')\n"
                "called editor.SetFocus\n")

    def test_set_background_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_background_color
        """
        def mock_apply(*args):
            print('called editor.applybgcolour with args', args)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetFocus', mockwx.MockEditor.SetFocus)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.applybgcolour = mock_apply
        testobj.parent_ = types.SimpleNamespace(backgroundcolour='xxx')
        testobj.set_background_color('evt')
        assert capsys.readouterr().out == ("called editor.applybgcolour with args ('xxx',)\n"
                                           "called editor.SetFocus\n")

    def test_applybgcolour(self, monkeypatch, capsys):
        """unittest for EditorPanel.applybgcolour
        """
        def mock_has():
            print('called Editor.HasSelection')
            return False
        def mock_has_2():
            print('called Editor.HasSelection')
            return True
        monkeypatch.setattr(testee.rt, 'RichTextAttr', mockwx.MockTextAttr)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'SetStyle', mockwx.MockEditor.SetStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'BeginStyle', mockwx.MockEditor.BeginStyle)
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'GetSelectionRange',
                            mockwx.MockEditor.GetSelectionRange)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.HasSelection = mock_has
        testobj.applybgcolour('colour')
        assert capsys.readouterr().out == (
            "called RichTextAttr.__init__\n"
            "called RichTextAttr.SetFlags with args (2,)\n"
            "called RichTextAttr.SetBackgroundColour with args ('colour',)\n"
            "called Editor.HasSelection\n"
            "called editor.BeginStyle with args (richtextattr,)\n")
        testobj.HasSelection = mock_has_2
        testobj.applybgcolour('colour')
        assert capsys.readouterr().out == (
                "called RichTextAttr.__init__\n"
                "called RichTextAttr.SetFlags with args (2,)\n"
                "called RichTextAttr.SetBackgroundColour with args ('colour',)\n"
                "called Editor.HasSelection\n"
                "called editor.GetSelectionRange with args ()\n"
                "called editor.SetStyle with args ('range', richtextattr)\n")

    # def test_update_bold(self, monkeypatch, capsys):
    #     """unittest for EditorPanel.update_bold
    #     """
    #     def mock_is():
    #         print('called editor.IsSelectionBold')
    #         return True
    #     evt = mockwx.MockEvent()
    #     assert capsys.readouterr().out == "called event.__init__ with args ()\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.IsSelectionBold = mock_is
    #     testobj.update_bold(evt)
    #     assert capsys.readouterr().out == ("called editor.IsSelectionBold\n"
    #                                        "called event.Check with args (True,)\n")

    # def test_update_italic(self, monkeypatch, capsys):
    #     """unittest for EditorPanel.update_italic
    #     """
    #     def mock_is():
    #         print('called editor.IsSelectionItalics')
    #         return True
    #     evt = mockwx.MockEvent()
    #     assert capsys.readouterr().out == "called event.__init__ with args ()\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.IsSelectionItalics = mock_is
    #     testobj.update_italic(evt)
    #     assert capsys.readouterr().out == ("called editor.IsSelectionItalics\n"
    #                                        "called event.Check with args (True,)\n")

    # def test_update_underline(self, monkeypatch, capsys):
    #     """unittest for EditorPanel.update_underline
    #     """
    #     def mock_is():
    #         print('called editor.IsSelectionUnderlined')
    #         return True
    #     evt = mockwx.MockEvent()
    #     assert capsys.readouterr().out == "called event.__init__ with args ()\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.IsSelectionUnderlined = mock_is
    #     testobj.update_underline(evt)
    #     assert capsys.readouterr().out == ("called editor.IsSelectionUnderlined\n"
    #                                        "called event.Check with args (True,)\n")

    # def _test_update_strikethrough(self, monkeypatch, capsys):
    #     """unittest for EditorPanel.update_strikethrough
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.update_strikethrough(evt) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    # def test_update_alignleft(self, monkeypatch, capsys):
    #     """unittest for EditorPanel.update_alignleft
    #     """
    #     def mock_is(*args):
    #         print('called editor.IsSelectionAligned with args', args)
    #         return True
    #     evt = mockwx.MockEvent()
    #     assert capsys.readouterr().out == "called event.__init__ with args ()\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.IsSelectionAligned = mock_is
    #     testobj.update_alignleft(evt)
    #     assert capsys.readouterr().out == ("called editor.IsSelectionAligned with args (1,)\n"
    #                                        "called event.Check with args (True,)\n")

    # def test_update_center(self, monkeypatch, capsys):
    #     """unittest for EditorPanel.update_center
    #     """
    #     def mock_is(*args):
    #         print('called editor.IsSelectionAligned with args', args)
    #         return True
    #     evt = mockwx.MockEvent()
    #     assert capsys.readouterr().out == "called event.__init__ with args ()\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.IsSelectionAligned = mock_is
    #     testobj.update_center(evt)
    #     assert capsys.readouterr().out == ("called editor.IsSelectionAligned with args (2,)\n"
    #                                        "called event.Check with args (True,)\n")

    # def test_update_alignright(self, monkeypatch, capsys):
    #     """unittest for EditorPanel.update_alignright
    #     """
    #     def mock_is(*args):
    #         print('called editor.IsSelectionAligned with args', args)
    #         return True
    #     evt = mockwx.MockEvent()
    #     assert capsys.readouterr().out == "called event.__init__ with args ()\n"
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.IsSelectionAligned = mock_is
    #     testobj.update_alignright(evt)
    #     assert capsys.readouterr().out == ("called editor.IsSelectionAligned with args (3,)\n"
    #                                        "called event.Check with args (True,)\n")

    def test_check_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel.check_dirty
        """
        def mock_is():
            print('called editor.IsModified')
            return 'modified'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.IsModified = mock_is
        assert testobj.check_dirty() == "modified"
        assert capsys.readouterr().out == "called editor.IsModified\n"

    def test_mark_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel.mark_dirty
        """
        def mock_set(value):
            print('called editor.SetModified with value `value`')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.SetModified = mock_set
        testobj.mark_dirty('value')
        assert capsys.readouterr().out == "called editor.SetModified with value `value`\n"

    def test_openup(self, monkeypatch, capsys):
        """unittest for EditorPanel.openup
        """
        monkeypatch.setattr(testee.rt.RichTextCtrl, 'Enable', mockwx.MockEditor.Enable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.openup('value')
        assert capsys.readouterr().out == "called editor.Enable with args ('value',)\n"

    def _test_search_from_start(self, monkeypatch, capsys):
        """unittest for EditorPanel.search_from_start
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.search_from_start() == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def _test_find_next(self, monkeypatch, capsys):
        """unittest for EditorPanel.find_next
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_next() == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented

    def _test_find_prev(self, monkeypatch, capsys):
        """unittest for EditorPanel.find_prev
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_prev() == "expected_result"
        assert capsys.readouterr().out == ("")
        # not implemented


class TestCheckDialog:
    """unittest for wxgui.CheckDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.CheckDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CheckDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CheckDialog, '__init__', mock_init)
        testobj = testee.CheckDialog()
        assert capsys.readouterr().out == 'called CheckDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for CheckDialog.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        parent = types.SimpleNamespace(app_icon='icon')
        testobj = testee.CheckDialog('master', parent, 'title')
        assert isinstance(testobj.vsizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title', 'size': (-1, 120)}\n"
                "called Dialog.SetIcon with args ('icon',)\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_label
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_label('xxx')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                "called  sizer.Add with args MockStaticText (1, 240, 5)\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_checkbox
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        result = testobj.add_checkbox('xxx')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
            "called BoxSizer.__init__ with args (4,)\n"
            f"called CheckBox.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
            "called hori sizer.Add with args MockCheckBox (0, 8192)\n"
            "called  sizer.Add with args MockBoxSizer (0, 256)\n")

    def test_add_ok_buttonbox(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_ok_buttonbox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_ok_buttonbox()
        assert capsys.readouterr().out == ("called dialog.CreateButtonSizer with args (4,)\n"
                                           "called BoxSizer.__init__ with args ()\n"
                                           "called  sizer.Add with args MockBoxSizer (0, 256)\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for CheckDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == "called checkbox.GetValue\n"


class TestOptionsDialog:
    """unittest for wxgui.OptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.OptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called OptionsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.OptionsDialog, '__init__', mock_init)
        testobj = testee.OptionsDialog()
        assert capsys.readouterr().out == 'called OptionsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for OptionsDialog.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'FlexGridSizer', mockwx.MockFlexGridSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        parent = types.SimpleNamespace(app_icon='icon')
        testobj = testee.OptionsDialog('master', parent, 'title')
        assert isinstance(testobj.vsizer, testee.wx.BoxSizer)
        assert isinstance(testobj.vsizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args ('title',) {}\n"
                # "called Dialog.SetIcon with args ('icon',)\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called FlexGridSizer.__init__ with args () {'cols': 2}\n"
                "called vert sizer.Add with args MockFlexGridSizer (0, 2544, 5)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")

    def test_add_checkbox_line_to_grid(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_checkbox
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_checkbox_line_to_grid('row', 'labeltext', 'value')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                # "called BoxSizer.__init__ with args (4,)\n"
            f"called StaticText.__init__ with args ({testobj},) {{'label': 'labeltext'}}\n"
            "called GridSizer.Add with args MockStaticText (1, 240, 5)\n"
            f"called CheckBox.__init__ with args ({testobj},) {{}}\n"
            "called checkbox.SetValue with args ('value',)\n"
            "called GridSizer.Add with args MockCheckBox (1, 240, 5)\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_buttonbox
        """
        def mock_set(*args):
            print('called CheckDialog.SetEscapeId with args', args)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.SetEscapeId = mock_set
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_buttonbox('okvalue', 'cancelvalue')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called Button.__init__ with args"
                f" ({testobj},) {{'id': 5100, 'label': 'okvalue'}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                "called Button.__init__ with args"
                f" ({testobj},) {{'id': 5001, 'label': 'cancelvalue'}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                "called CheckDialog.SetEscapeId with args (5001,)\n"
                "called  sizer.Add with args MockBoxSizer (0, 2544, 5)\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for CheckDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == "called checkbox.GetValue\n"


class TestSearchDialog:
    """unittest for wxgui.SearchDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.SearchDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SearchDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SearchDialog, '__init__', mock_init)
        testobj = testee.SearchDialog()
        assert capsys.readouterr().out == 'called SearchDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SearchDialog.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        parent = types.SimpleNamespace(app_icon='icon')
        testobj = testee.SearchDialog('master', parent)
        assert isinstance(testobj.vsizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args ('Search Results',) {}\n"
                "called Dialog.SetIcon with args ('icon',)\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for SearchDialog.add_label
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_label('text')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called hori sizer.Add with args MockStaticText ()\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_testentry(self, monkeypatch, capsys):
        """unittest for SearchDialog.add_testentry
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert isinstance(testobj.add_textentry(), testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called TextCtrl.__init__ with args ({testobj},) {{}}\n"
                "called hori sizer.Add with args MockTextCtrl ()\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_build_search_selector(self, monkeypatch, capsys):
        """unittest for SearchDialog.build_search_selector
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert testobj.build_search_selector([], '') == []
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddStretchSpacer\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called vert sizer.AddSpacer with args (3,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'In: '}}\n"
                "called vert sizer.Add with args MockStaticText ()\n"
                "called vert sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args MockBoxSizer ()\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called hori sizer.Add with args MockBoxSizer ()\n"
                "called hori sizer.AddStretchSpacer\n"
                "called  sizer.Add with args MockBoxSizer ()\n")
        searchdefs = ['search', 'for']
        result = testobj.build_search_selector(searchdefs, 'callback')
        assert len(result) == len(searchdefs)
        for item in result:
            assert isinstance(item, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddStretchSpacer\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called vert sizer.AddSpacer with args (3,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'In: '}}\n"
                "called vert sizer.Add with args MockStaticText ()\n"
                "called vert sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args MockBoxSizer ()\n"
                "called BoxSizer.__init__ with args (8,)\n"
                f"called CheckBox.__init__ with args ('search', {testobj}) {{}}\n"
                f"called CheckBox.Bind with args ({testee.wx.EVT_CHECKBOX}, 'callback') {{}}\n"
                "called vert sizer.Add with args MockCheckBox ()\n"
                f"called CheckBox.__init__ with args ('for', {testobj}) {{}}\n"
                f"called CheckBox.Bind with args ({testee.wx.EVT_CHECKBOX}, 'callback') {{}}\n"
                "called vert sizer.Add with args MockCheckBox ()\n"
                "called hori sizer.Add with args MockBoxSizer ()\n"
                "called hori sizer.AddStretchSpacer\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_build_options_selector(self, monkeypatch, capsys):
        """unittest for SearchDialog.build_options_selector
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert testobj.build_options_selector([]) == []
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args (4,)\n"
                                           "called BoxSizer.__init__ with args (8,)\n"
                                           "called hori sizer.Add with args MockBoxSizer ()\n"
                                           "called hori sizer.AddStretchSpacer\n"
                                           "called  sizer.Add with args MockBoxSizer ()\n")
        optiondefs = ['option1', 'option2']
        result = testobj.build_options_selector(optiondefs)
        assert len(result) == len(optiondefs)
        for item in result:
            assert isinstance(item, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called BoxSizer.__init__ with args (8,)\n"
                f"called CheckBox.__init__ with args ('option1', {testobj}) {{}}\n"
                "called vert sizer.Add with args MockCheckBox ()\n"
                f"called CheckBox.__init__ with args ('option2', {testobj}) {{}}\n"
                "called vert sizer.Add with args MockCheckBox ()\n"
                "called hori sizer.Add with args MockBoxSizer ()\n"
                "called hori sizer.AddStretchSpacer\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_vertical_space(self, monkeypatch, capsys):
        """unittest for SearchDialog.add_vertical_space
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_vertical_space('height')
        assert capsys.readouterr().out == "called  sizer.AddSpacer with args ('height',)\n"

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for SearchDialog.add_checkbox
        """
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert isinstance(testobj.add_checkbox('text'), testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('text', {testobj}) {{}}\n"
                "called  sizer.Add with args MockCheckBox ()\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for SearchDialog.add_buttons
        """
        def mock_set(*args):
            print('called CheckDialog.SetEscapeId with args', args)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.SetEscapeId = mock_set
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_buttons()
        assert capsys.readouterr().out == (
            "called BoxSizer.__init__ with args (4,)\n"
            "called hori sizer.AddStretchSpacer\n"
            f"called Button.__init__ with args ({testobj},) {{'id': 5100, 'label': '&Ok'}}\n"
            "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
            f"called Button.__init__ with args ({testobj},) {{'id': 5001, 'label': '&Cancel'}}\n"
            "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
            "called CheckDialog.SetEscapeId with args (5001,)\n"
            "called hori sizer.AddStretchSpacer\n"
            "called  sizer.Add with args MockBoxSizer ()\n")

    def test_set_checkbox_value(self, monkeypatch, capsys):
        """unittest for SearchDialog.set_checkbox_value
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_checkbox_value(cb, 'value')
        assert capsys.readouterr().out == "called checkbox.SetValue with args ('value',)\n"

    def test_set_textentry_value(self, monkeypatch, capsys):
        """unittest for SearchDialog.set_textentry_value
        """
        txt = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textentry_value(txt, 'text')
        assert capsys.readouterr().out == "called text.SetValue with args ('text',)\n"

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for SearchDialog.set_focus_to
        """
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Control.SetFocus\n"

    def _test_set_modechecks(self, monkeypatch, capsys):
        """unittest for SearchDialog.set_modechecks
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_modechecks() == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_get_textentry_value(self, monkeypatch, capsys):
        """unittest for SearchDialog.get_textentry_value
        """
        txt = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textentry_value(txt) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SearchDialog.get_checkbox_value
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_value(cb) == "value from checkbox"
        assert capsys.readouterr().out == "called checkbox.IsChecked\n"


class TestResultsDialog:
    """unittest for wxgui.ResultsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.ResultsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ResultsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ResultsDialog, '__init__', mock_init)
        testobj = testee.ResultsDialog()
        assert capsys.readouterr().out == 'called ResultsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ResultsDialog.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        parent = types.SimpleNamespace(app_icon='icon')
        testobj = testee.ResultsDialog('master', parent)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'Search Results'}\n"
                "called Dialog.SetIcon with args ('icon',)\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args (vert sizer,)\n")

    def test_set_toptext(self, monkeypatch, capsys):
        """unittest for ResultsDialog.set_toptext
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.set_toptext('text')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called hori sizer.Add with args MockStaticText ()\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_results_list(self, monkeypatch, capsys):
        """unittest for ResultsDialog.add_results_list
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee, 'MyListCtrl', mockwx.MockListCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert isinstance(testobj.add_results_list([], ''), testee.MyListCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called ListCtrl.__init__ with args ({testobj},) {{'style': 32}}\n"
                f"called ListCtrl.Bind with args ({testee.wx.EVT_LIST_ITEM_ACTIVATED}, '')\n"
                "called hori sizer.Add with args MockListCtrl (1, 8432, 5)\n"
                "called  sizer.Add with args MockBoxSizer ()\n")
        assert isinstance(testobj.add_results_list(['lbl1', 'lbl2'], 'callback'), testee.MyListCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called ListCtrl.__init__ with args ({testobj},) {{'style': 32}}\n"
                "called ListCtrl.InsertColumn with args (0, 'lbl1')\n"
                "called ListCtrl.InsertColumn with args (1, 'lbl2')\n"
                f"called ListCtrl.Bind with args ({testee.wx.EVT_LIST_ITEM_ACTIVATED}, 'callback')\n"
                "called hori sizer.Add with args MockListCtrl (1, 8432, 5)\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for ResultsDialog.add_buttons
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert testobj.add_buttons([]) == []
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddStretchSpacer\n"
                "called hori sizer.AddStretchSpacer\n"
                "called  sizer.Add with args MockBoxSizer ()\n")
        buttondefs = [('button', 'callback1'), ('defs', 'callback2')]
        result = testobj.add_buttons(buttondefs)
        assert len(result) == len(buttondefs)
        for item in result:
            assert isinstance(item, testee.wx.Button)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddStretchSpacer\n"
                f"called Button.__init__ with args ('button', {testobj}) {{}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback1') {{}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ('defs', {testobj}) {{}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback2') {{}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called hori sizer.AddStretchSpacer\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_item_to_list(self, monkeypatch, capsys):
        """unittest for ResultsDialog.add_item_to_list
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_item_to_list(listbox, 'loc', 'root', 'title')
        assert capsys.readouterr().out == (
                "called ListCtrl.InsertItem with args (9223372036854775807, 'root')\n"
                "called ListCtrl.SetItem with args ('itemindex', 0, 'root')\n"
                "called ListCtrl.SetItem with args ('itemindex', 1, 'title')\n"
                "called ListCtrl.SetItemData with args ('itemindex', 'loc')\n")

    def test_get_next_item(self, monkeypatch, capsys):
        """unittest for ResultsDialog.get_next_item
        """
        def mock_get(*args):
            print('called list.GetNextItem with args', args)
            return -1
        def mock_get_2(*args):
            print('called list.GetNextItem with args', args)
            return 'xx'
        listbox = types.SimpleNamespace(GetNextItem=mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_next_item(listbox) is None
        assert capsys.readouterr().out == "called list.GetNextItem with args (2,)\n"
        listbox.GetNextItem = mock_get_2
        assert testobj.get_next_item(listbox) == "xx"
        assert capsys.readouterr().out == "called list.GetNextItem with args (2,)\n"

    def test_get_prev_item(self, monkeypatch, capsys):
        """unittest for ResultsDialog.get_prev_item
        """
        def mock_get(*args):
            print('called list.GetNextItem with args', args)
            return -1
        def mock_get_2(*args):
            print('called list.GetNextItem with args', args)
            return 'xx'
        listbox = types.SimpleNamespace(GetNextItem=mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_prev_item(listbox) is None
        assert capsys.readouterr().out == "called list.GetNextItem with args (0,)\n"
        listbox.GetNextItem = mock_get_2
        assert testobj.get_prev_item(listbox) == "xx"
        assert capsys.readouterr().out == "called list.GetNextItem with args (0,)\n"

    def test_getselection(self, monkeypatch, capsys):
        """unittest for ResultsDialog.get_selection
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getselection(listbox) == -1
        assert capsys.readouterr().out == "called ListCtrl.GetFirstSelected\n"

    def test_setselection(self, monkeypatch, capsys):
        """unittest for ResultsDialog.set_selection
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setselection(listbox, 'sel')
        assert capsys.readouterr().out == "called ListCtrl.Select with args ('sel',)\n"

    def test_disable_widget(self, monkeypatch, capsys):
        """unittest for ResultsDialog.disable_widget
        """
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.disable_widget(widget)
        assert capsys.readouterr().out == "called Control.Enable with arg False\n"

    def test_enable_button_if_disabled(self, monkeypatch, capsys):
        """unittest for ResultsDialog.enable_button_if_disabled
        """
        def mock_is():
            print('called Button.IsEnabled')
            return True
        def mock_is_2():
            print('called Button.IsEnabled')
            return False
        button = mockwx.MockButton()
        assert capsys.readouterr().out == "called Button.__init__ with args () {}\n"
        button.IsEnabled = mock_is
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_button_if_disabled(button)
        assert capsys.readouterr().out == "called Button.IsEnabled\n"
        button.IsEnabled = mock_is_2
        testobj.enable_button_if_disabled(button)
        assert capsys.readouterr().out == ("called Button.IsEnabled\n"
                                           "called Button.Enable with arg True\n")

    def test_get_item_data(self, monkeypatch, capsys):
        """unittest for ResultsDialog.get_item_data
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_data(listbox, 'item') == "item"
        assert capsys.readouterr().out == ("called ListCtrl.GetItemData with args ('item',)\n")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for ResultsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_reject(self, monkeypatch, capsys):
        """unittest for ResultsDialog.reject
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.reject() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestMyListCtrl:
    """unittests for gui_wx.MyListCtrl
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for MyListCtrl.__init__
        """
        monkeypatch.setattr(testee.wx.ListCtrl, '__init__', mockwx.MockListCtrl.__init__)
        monkeypatch.setattr(testee.listmix.ListCtrlAutoWidthMixin, '__init__',
                            mockwx.MockListCtrlAutoWidthMixin.__init__)
        parent = 'parent'
        testobj = testee.MyListCtrl(parent)
        assert capsys.readouterr().out == (
                "called ListCtrl.__init__ with args"
                " ('parent',) {'pos': wx.Point(-1, -1), 'size': wx.Size(-1, -1), 'style': 0}\n"
                "called ListCtrlAutoWidthMixin.__init__ with args () {}\n")
        testobj = testee.MyListCtrl(parent, pos="pos", size="size", style="style")
        assert capsys.readouterr().out == (
                "called ListCtrl.__init__ with args"
                " ('parent',) {'pos': 'pos', 'size': 'size', 'style': 'style'}\n"
                "called ListCtrlAutoWidthMixin.__init__ with args () {}\n")


class TestTaskbarIcon:
    """unittest for wxgui.TaskbarIcon
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.TaskbarIcon object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TaskbarIcon.__init__ with args', args)
        monkeypatch.setattr(testee.TaskbarIcon, '__init__', mock_init)
        testobj = testee.TaskbarIcon()
        assert capsys.readouterr().out == 'called TaskbarIcon.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for TaskbarIcon.__init__
        """
        def mock_init(self):
            print("called taskbaricon.__init__")
        def mock_set(self, *args):
            print("called taskbaricon.SetIcon with args", args)
        def mock_bind(self, *args, **kwargs):
            print("called taskbaricon.Bind with args", args, kwargs)
        parent = types.SimpleNamespace(app_icon='appicon', revive='revive')
        monkeypatch.setattr(testee.wx.adv.TaskBarIcon, '__init__', mock_init)
        monkeypatch.setattr(testee.wx.adv.TaskBarIcon, 'SetIcon', mock_set)
        monkeypatch.setattr(testee.wx.adv.TaskBarIcon, 'Bind', mock_bind)
        testobj = testee.TaskbarIcon(parent)
        assert capsys.readouterr().out == (
            "called taskbaricon.__init__\n"
            "called taskbaricon.SetIcon with args ('appicon', 'Click to revive DocTree')\n"
            "called taskbaricon.Bind with args"
            f" ({testee.wx.adv.EVT_TASKBAR_LEFT_DCLICK}, 'revive') {{}}\n"
            f"called taskbaricon.Bind with args ({testee.wx.EVT_MENU}, 'revive') {{'id': -1}}\n")

    def test_CreatePopupMenu(self, monkeypatch, capsys):
        """unittest for TaskbarIcon.CreatePopupMenu
        """
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.revive = 'xxx'
        assert isinstance(testobj.CreatePopupMenu(), testee.wx.Menu)
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called menu.Append with args (-1, 'Revive Doctree')\n")


create_menu = """\
called ToolBar.__init__ with args ({testobj},)
called Frame.SetToolBar with args (A ToolBar,)
called MenuBar.__init__ with args ()
called Frame.SetMenuBar with args (A MenuBar,)
called Menu.__init__ with args ()
called MenuItem.__init__ with args (A Menu, -1, 'aaaa', '') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback0')
called Bitmap.__init__ with args ('{testobj.master.HERE}/aaa.ico', 15)
called menuitem.SetBitmap with args (Bitmap created from '{testobj.master.HERE}/aaa.ico',)
called Toolbar.AddTool with args (-1, 'aaaa', Bitmap created from '{testobj.master.HERE}/aaa.ico') {{}}
called Frame.Bind with args ({testee.wx.EVT_TOOL}, 'callback0')
called menu.Append with args MockMenuItem
called MenuItem.__init__ with args (A Menu, -1, 'exit\\tCtrl+X', '') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback1')
called Bitmap.__init__ with args ('{testobj.master.HERE}/exit.ico', 15)
called menuitem.SetBitmap with args (Bitmap created from '{testobj.master.HERE}/exit.ico',)
called Toolbar.AddTool with args (-1, 'exit', Bitmap created from '{testobj.master.HERE}/exit.ico') {{}}
called Frame.Bind with args ({testee.wx.EVT_TOOL}, 'callback1')
called menu.Append with args MockMenuItem
called menubar.Append with args (A Menu, 'aaa')
called Menu.__init__ with args ()
called MenuItem.__init__ with args (A Menu, -1, 'LinE sPacINg', '') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, '')
called menu.Append with args MockMenuItem
called MenuItem.__init__ with args (A Menu, -1, 'pARAgraph sPAcinG', '') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, '')
called menu.Append with args MockMenuItem
called menubar.Append with args (A Menu, 'xxx')
called Menu.__init__ with args ()
called MenuItem.__init__ with args (A Menu, -1, 'B', 'CheckB') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback2')
called menu.Append with args MockMenuItem
called MenuItem.__init__ with args (A Menu, -1, 'I', 'CheckI') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback3')
called menu.Append with args MockMenuItem
called MenuItem.__init__ with args (A Menu, -1, 'U', 'CheckU') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback4')
called menu.Append with args MockMenuItem
called MenuItem.__init__ with args (A Menu, -1, 'S', 'CheckS') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback5')
called menu.Append with args MockMenuItem
called MenuItem.__init__ with args (A Menu, -1, 'M', 'CheckM') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback11')
called menu.Append with args MockMenuItem
called menu.AppendSeparator with args ()
called MenuItem.__init__ with args (A Menu, -1, 'CtrlTab', '') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback')
called menu.Append with args MockMenuItem
called MenuItem.__init__ with args (A Menu, -1, 'X', 'Check') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback6')
called menu.Append with args MockMenuItem
called menu.AppendSeparator with args ()
called menubar.Append with args (A Menu, 'yyy')
called Menu.__init__ with args ()
called Toolbar.AddSeparator with args ()
called MenuItem.__init__ with args (A Menu, -1, '&Undo\\tCtrl+Z', 'undo') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback7')
called menu.Append with args MockMenuItem
called MenuItem.__init__ with args (A Menu, -1, '&Redo\\tCtrl+Y', 'redo') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback8')
called menu.Append with args MockMenuItem
called MenuItem.__init__ with args (A Menu, -1, '', 'xxx') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback0')
called menu.Append with args MockMenuItem
called menubar.Append with args (A Menu, 'zzz')
called Menu.__init__ with args ()
called Toolbar.AddSeparator with args ()
called MenuItem.__init__ with args (A Menu, -1, 'bbbb', '') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback9')
called menu.Append with args MockMenuItem
called menubar.Append with args (A Menu, 'bbb')
called Menu.__init__ with args ()
called Toolbar.AddSeparator with args ()
called MenuItem.__init__ with args (A Menu, -1, 'cccc', '') {{}}
called Frame.Bind with args ({testee.wx.EVT_MENU}, 'callback10')
called menu.Append with args MockMenuItem
called menubar.Append with args (A Menu, 'ccc')
"""

toolbar = """\
called colourselect.__init__ with args (A ToolBar,) {{'colour': wx.Colour(-1, -1, -1, 255)}}
called colourselect.Bind with args ({testee.csel.EVT_COLOURSELECT}, {testobj.editor.select_text_color}) {{}}
called Toolbar.AddControl with args ({testobj.fgcselect},)
called Bitmap.__init__ with args (14, 14)
called Button.__init__ with args (A ToolBar,) {{'bitmap': Bitmap created from '14', 'size': (22, 22)}}
called maingui.changebitmapbuttoncolour with args ({testobj.fgcset}, wx.Colour(-1, -1, -1, 255))
called Button.Bind with args ({testee.wx.EVT_BUTTON}, {testobj.editor.set_text_color}) {{}}
called Toolbar.AddControl with args ({testobj.fgcset},)
called colourselect.__init__ with args (A ToolBar,) {{'colour': wx.Colour(-1, -1, -1, 255), 'size': (24, 24)}}
called colourselect.Bind with args ({testee.csel.EVT_COLOURSELECT}, {testobj.editor.select_background_color}) {{}}
called Toolbar.AddControl with args ({testobj.bgcselect},)
called Bitmap.__init__ with args (16, 16)
called Button.__init__ with args (A ToolBar,) {{'bitmap': Bitmap created from '16', 'size': (24, 24)}}
called maingui.changebitmapbuttoncolour with args ({testobj.bgcset}, wx.Colour(-1, -1, -1, 255))
called Button.Bind with args ({testee.wx.EVT_BUTTON}, {testobj.editor.set_background_color}) {{}}
called Toolbar.AddControl with args ({testobj.bgcset},)
"""

@pytest.fixture
def expected_output():
    """uitvoervoorspellingen
    """
    return {'create_menu': create_menu, 'stylestoolbar': toolbar}
