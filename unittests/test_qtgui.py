"""unittests for ./doctree/qtgui.py
"""
import types
from doctree import qtgui as testee
import pytest
from mockgui import mockqtwidgets as mockqtw
from output_fixture import expected_output

def test_show_message(monkeypatch, capsys):
    """unittest for qtgui.show_message
    """
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testee.show_message('win', 'text')
    assert capsys.readouterr().out == (
            "called MessageBox.information with args `win` `DocTree` `text`\n")


def test_ask_ynquestion(monkeypatch, capsys):
    """unittest for qtgui.ask_ynquestion
    """
    def mock_ask(parent, caption, message, buttons, defaultButton=None):
        if defaultButton:
            print('called MessageBox.question with args'
                  f' `{parent}` `{caption}` `{message}` `{buttons}` `{defaultButton}`')
        else:
            print('called MessageBox.question with args'
                  f' `{parent}` `{caption}` `{message}` `{buttons}`')
        return testee.qtw.QMessageBox.Yes
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    assert not testee.ask_ynquestion('win', 'text')
    assert capsys.readouterr().out == (
            "called MessageBox.question with args `win` `DocTree` `text` `12` `4`\n")
    monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_ask)
    assert testee.ask_ynquestion('win', 'text')
    assert capsys.readouterr().out == (
            "called MessageBox.question with args `win` `DocTree` `text` `12` `4`\n")


def test_ask_yncquestion(monkeypatch, capsys):
    """unittest for qtgui.ask_yncquestion
    """
    def mock_ask(parent, caption, message, buttons, defaultButton=None):
        if defaultButton:
            print('called MessageBox.question with args'
                  f' `{parent}` `{caption}` `{message}` `{buttons}` `{defaultButton}`')
        else:
            print('called MessageBox.question with args'
                  f' `{parent}` `{caption}` `{message}` `{buttons}`')
        return testee.qtw.QMessageBox.Yes
    def mock_ask_2(parent, caption, message, buttons, defaultButton=None):
        if defaultButton:
            print('called MessageBox.question with args'
                  f' `{parent}` `{caption}` `{message}` `{buttons}` `{defaultButton}`')
        else:
            print('called MessageBox.question with args'
                  f' `{parent}` `{caption}` `{message}` `{buttons}`')
        return testee.qtw.QMessageBox.Cancel
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    assert testee.ask_yncquestion('win', 'text') == (False, False)
    assert capsys.readouterr().out == (
            "called MessageBox.question with args `win` `DocTree` `text` `14` `4`\n")
    monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_ask)
    assert testee.ask_yncquestion('win', 'text') == (True, False)
    assert capsys.readouterr().out == (
            "called MessageBox.question with args `win` `DocTree` `text` `14` `4`\n")
    monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_ask_2)
    assert testee.ask_yncquestion('win', 'text') == (False, True)
    assert capsys.readouterr().out == (
            "called MessageBox.question with args `win` `DocTree` `text` `14` `4`\n")


def test_get_text(monkeypatch, capsys):
    """unittest for qtgui.get_text
    """
    def mock_get(parent, *args, **kwargs):
        print('called InputDialog.getText with args', parent, args, kwargs)
        return 'text', True
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    assert testee.get_text('win', 'caption', 'oldtext') == (False, 'oldtext')
    assert capsys.readouterr().out == (
            "called InputDialog.getText with args win ('DocTree', 'caption') {'text': 'oldtext'}\n")
    monkeypatch.setattr(mockqtw.MockInputDialog, 'getText', mock_get)
    assert testee.get_text('win', 'caption', 'oldtext') == (True, 'text')
    assert capsys.readouterr().out == (
            "called InputDialog.getText with args win ('DocTree', 'caption') {'text': 'oldtext'}\n")


def test_get_choice(monkeypatch, capsys):
    """unittest for qtgui.get_choice
    """
    def mock_get(parent, *args, **kwargs):
        print('called InputDialog.getItem with args', parent, args, kwargs)
        return 'text', True
    monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
    assert testee.get_choice('win', 'caption', 'options', 'current') == (False, '')
    assert capsys.readouterr().out == (
            "called InputDialog.getItem with args win ('DocTree', 'caption', 'options', 'current')"
            " {'editable': False}\n")
    monkeypatch.setattr(mockqtw.MockInputDialog, 'getItem', mock_get)
    assert testee.get_choice('win', 'caption', 'options', 'current') == (True, "text")
    assert capsys.readouterr().out == (
            "called InputDialog.getItem with args win ('DocTree', 'caption', 'options', 'current')"
            " {'editable': False}\n")


def test_get_filename(monkeypatch, capsys):
    """unittest for qtgui.get_filename
    """
    def mock_open(parent, *args, **kwargs):
        print('called FileDialog.getOpenFileName with args', parent, args, kwargs)
        return 'xxxxx', True
    def mock_save(parent, *args, **kwargs):
        print('called FileDialog.getSaveFileName with args', parent, args, kwargs)
        return 'xxxxx', True
    monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
    assert testee.get_filename('win', 'title', 'start') == (False, '')
    assert capsys.readouterr().out == ("called FileDialog.getOpenFileName with args"
                                       " win ('title', 'start', 'Doctree Files (*.trd)') {}\n")
    monkeypatch.setattr(mockqtw.MockFileDialog, 'getOpenFileName', mock_open)
    assert testee.get_filename('win', 'title', 'start') == (True, 'xxxxx')
    assert capsys.readouterr().out == ("called FileDialog.getOpenFileName with args"
                                       " win ('title', 'start', 'Doctree Files (*.trd)') {}\n")
    assert testee.get_filename('win', 'title', 'start', True) == (False, '')
    assert capsys.readouterr().out == ("called FileDialog.getSaveFileName with args"
                                       " win ('title', 'start', 'Doctree Files (*.trd)') {}\n")
    monkeypatch.setattr(mockqtw.MockFileDialog, 'getSaveFileName', mock_save)
    assert testee.get_filename('win', 'title', 'start', True) == (True, 'xxxxx')
    assert capsys.readouterr().out == ("called FileDialog.getSaveFileName with args"
                                       " win ('title', 'start', 'Doctree Files (*.trd)') {}\n")


def test_show_dialog(monkeypatch, capsys):
    """unittest for qtgui.show_dialog
    """
    def mock_exec(self):
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Accepted
    # monkeypatch.setattr(testee.qtw, 'QDialog', mockqtw.MockDialog)
    # cls = testee.qtw.QDialog
    cls = mockqtw.MockDialog
    assert not testee.show_dialog('win', cls)
    assert capsys.readouterr().out == ("called Dialog.__init__ with args win () {}\n"
                                       "called Dialog.exec\n")
    monkeypatch.setattr(mockqtw.MockDialog, 'exec_', mock_exec)
    assert not testee.show_dialog('win', cls, {'greet': 'hello'})
    assert capsys.readouterr().out == ("called Dialog.__init__ with args win () {'greet': 'hello'}\n"
                                       "called Dialog.exec\n")


def test_show_nonmodal(monkeypatch, capsys):
    """unittest for qtgui.show_nonmodal
    """
    cls = mockqtw.MockDialog
    testee.show_nonmodal('win', cls)
    assert capsys.readouterr().out == ("called Dialog.__init__ with args win () {}\n"
                                       "called Dialog.show\n")


class MockMainWindow:
    "stub for main.MainWindow object"


class MockEditor:
    "stub for main.Editor object"
    def __init__(self, *args):
        self.project_dirty = False
        if args:
            self._parent = args[0]
    def set_project_dirty(self, value):
        print(f"called Editor.set_project_dirty with arg {value}")
    def check_active(self):
        print('called Editor.check_active')
    def activate_item(self, item):
        print('called Editor.activate_item with arg {item}')
    def set_window_title(self):
        print('called Editor.set_window_title')
    def set_text_position(self, pos):
        print(f'called Editor.set_text_position with arg {pos}')
    def ensureCursorVisible(self):
        print('called Editor.ensureCursorVisible')
    def setFocus(self):
        print('called Editor.setFocus')
    def do_addaction(self, *args):
        print("called Editor.do_addaction with args", args)
        return 'data'
    def do_pasteaction(self, *args):
        print("called Editor.do_pasteaction with args", args)
        return 'keys', 'parent'
    def do_copyaction(self, *args):
        print("called Editor.do_addaction with args", args)
        return 'opts', 'views'
    def setReadOnly(self, value):
        print(f'called Editor.setReadOnly with arg {value}')


class MockMainGui:
    "stub for qtgui.MainGui object"
    undo_item = mockqtw.MockAction()
    redo_item = mockqtw.MockAction()
    # assert capsys.readouterr().out == ("called Action.__init__ with args ()\n"
    #                                    "called Action.__init__ with args ()\n")


class MockTree:
    "stub for qtgui.TreePanel object"
    def __init__(self, *args):
        print('called TreePanel.__init__ with args', args)

    def getitemparentpos(self, item):
        print(f"called TreePanel.getitemparentpos with arg '{item}'")
        return "parent", 0

    def getitemkey(self, item):
        print(f"called TreePanel.getitemkey with arg '{item}'")
        return "itemkey"

    def removeitem(self, *args):
        print("called TreePanel.removeitem with args", args)
        return 'title', 'text', 'subtree'


class MockStack:
    "stub for qtgui.UndoRedoStack object"
    def __init__(self, parent):
        print(f'called gui.UndoRedoStack.__init__ with arg {parent}')


class TestCheckDialog:
    """unittest for qtgui.CheckDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.CheckDialog object

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
        testobj.parent = MockMainGui()
        testobj.parent.master = MockEditor()
        assert capsys.readouterr().out == 'called CheckDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for CheckDialog.__init__
        """
        def mock_klaar(self):
            "stub for CheckDialog.klaar method"
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.CheckDialog, 'klaar', mock_klaar)
        parent = MockMainGui()
        parent.nt_icon = 'Icon'
        testobj = testee.CheckDialog(parent)
        assert testobj.parent == parent
        assert testobj.option == ''
        assert isinstance(testobj.check, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['checkdialog'].format(testobj=testobj,
                                                                                message='')
        message = 'Do something'
        testobj = testee.CheckDialog(parent, message, 'this')
        assert testobj.parent == parent
        assert testobj.option == 'this'
        assert isinstance(testobj.check, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['checkdialog'].format(testobj=testobj,
                                                                                message=message)

    def test_klaar(self, monkeypatch, capsys):
        """unittest for CheckDialog.klaar
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'done', mockqtw.MockDialog.done)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.option = 'something'
        testobj.parent.master.opts = {}
        testobj.check = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj.klaar()
        assert testobj.parent.master.opts == {}
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called Dialog.done with arg `0`\n")
        testobj.check.setChecked(True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"
        testobj.klaar()
        assert testobj.parent.master.opts == {'something': False}
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called Dialog.done with arg `0`\n")


class TestOptionsDialog:
    """unittest for qtgui.OptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.OptionsDialog object

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
        testobj.parent = MockMainGui()
        testobj.parent.master = MockEditor()
        assert capsys.readouterr().out == 'called OptionsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for OptionsDialog.__init__
        """
        def mock_get():
            print('called shared.get_setttexts')
            return {'xxx': 'xxxxxxxxxxxxxx', 'yyy': 'yyyyyyyyyyyyyyy'}
        monkeypatch.setattr(testee.shared, 'get_setttexts', mock_get)
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        parent = MockMainGui()
        parent.master = MockEditor()
        parent.master.opts = {'xxx': True, 'yyy': False, 'zzz': False}
        testobj = testee.OptionsDialog(parent)
        assert len(testobj.controls) == len(['xxx', 'yyy'])
        assert isinstance(testobj.controls[0][1], testee.qtw.QCheckBox)
        assert isinstance(testobj.controls[1][1], testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['optionsdialog'].format(testobj=testobj)

    def test_accept(self, monkeypatch, capsys):
        """unittest for OptionsDialog.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.opts = {}
        checkbox1 = mockqtw.MockCheckBox()
        checkbox1.setChecked(True)
        checkbox2 = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.__init__\n")
        testobj.controls = [('xxx', checkbox1), ('yyy', checkbox2)]
        testobj.accept()
        assert testobj.parent.master.opts == {'xxx': True, 'yyy': False}
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called Dialog.accept\n")


class TestSearchDialog:
    """unittest for qtgui.SearchDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SearchDialog object

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
        testobj.parent = MockMainGui()
        testobj.parent.master = MockEditor()
        assert capsys.readouterr().out == 'called SearchDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SearchDialog.__init__
        """
        def mock_check(self):
            "stub"
            print('SearchDialog.check_modes')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.SearchDialog, 'check_modes', mock_check)
        parent = MockMainGui()
        parent.title = 'Title'
        parent.nt_icon = 'Icon'
        parent.srchtext = ''
        parent.srchflags = testee.gui.QTextDocument.FindFlag
        parent.srchlist = False
        parent.srchwrap = False
        parent.master = MockEditor()
        testobj = testee.SearchDialog(parent)
        assert capsys.readouterr().out == expected_output['searchdialog'].format(testobj=testobj)
        assert isinstance(testobj.t_zoek, testee.qtw.QLineEdit)
        assert isinstance(testobj.c_titl, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_text, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_curr, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_hlett, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_woord, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_wrap, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_lijst, testee.qtw.QCheckBox)
        assert testobj.c_curr.isChecked()
        assert not testobj.c_titl.isChecked()
        assert not testobj.c_text.isChecked()
        assert testobj.t_zoek.text() == ''
        assert not testobj.c_hlett.isChecked()
        assert not testobj.c_woord.isChecked()
        assert not testobj.c_lijst.isChecked()
        assert not testobj.c_wrap.isChecked()
        assert capsys.readouterr().out == ("called CheckBox.isChecked\ncalled CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\ncalled LineEdit.text\n"
                                           "called CheckBox.isChecked\ncalled CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\ncalled CheckBox.isChecked\n")

        parent.srchtext = 'Find'
        parent.srchflags = testee.gui.QTextDocument.FindFlag.FindBackward
        parent.srchlist = True
        parent.srchwrap = True
        testobj = testee.SearchDialog(parent, mode=1)
        assert capsys.readouterr().out == expected_output['searchdialog1'].format(testobj=testobj)
        assert isinstance(testobj.t_zoek, testee.qtw.QLineEdit)
        assert isinstance(testobj.c_titl, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_text, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_curr, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_hlett, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_woord, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_wrap, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_lijst, testee.qtw.QCheckBox)
        assert not testobj.c_curr.isChecked()
        assert testobj.c_titl.isChecked()
        assert not testobj.c_text.isChecked()
        assert testobj.t_zoek.text() == 'Find'
        assert not testobj.c_hlett.isChecked()
        assert not testobj.c_woord.isChecked()
        assert testobj.c_lijst.isChecked()
        assert testobj.c_wrap.isChecked()
        assert capsys.readouterr().out == ("called CheckBox.isChecked\ncalled CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\ncalled LineEdit.text\n"
                                           "called CheckBox.isChecked\ncalled CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\ncalled CheckBox.isChecked\n")

        parent.srchflags = (testee.gui.QTextDocument.FindFlag.FindCaseSensitively
                            | testee.gui.QTextDocument.FindFlag.FindWholeWords)
        testobj = testee.SearchDialog(parent, mode=2)
        assert capsys.readouterr().out == expected_output['searchdialog2'].format(testobj=testobj)
        assert isinstance(testobj.t_zoek, testee.qtw.QLineEdit)
        assert isinstance(testobj.c_titl, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_text, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_curr, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_hlett, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_woord, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_wrap, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_lijst, testee.qtw.QCheckBox)
        assert not testobj.c_curr.isChecked()
        assert not testobj.c_titl.isChecked()
        assert testobj.c_text.isChecked()
        assert testobj.t_zoek.text() == 'Find'
        assert testobj.c_hlett.isChecked()
        assert testobj.c_woord.isChecked()
        assert testobj.c_lijst.isChecked()
        assert testobj.c_wrap.isChecked()
        assert capsys.readouterr().out == ("called CheckBox.isChecked\ncalled CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\ncalled LineEdit.text\n"
                                           "called CheckBox.isChecked\ncalled CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\ncalled CheckBox.isChecked\n")

    def test_check_modes(self, monkeypatch, capsys):
        """unittest for SearchDialog.check_modes
        """
        c_curr = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        def mock_sender():
            print('called SearchDialog.sender')
            return c_curr
        def mock_sender_2():
            print('called SearchDialog.sender')
            return None
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.c_curr = c_curr
        testobj.c_titl = mockqtw.MockCheckBox()
        testobj.c_text = mockqtw.MockCheckBox()
        testobj.c_lijst = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n")
        testobj.sender = mock_sender
        testobj.check_modes()
        assert capsys.readouterr().out == ("called SearchDialog.sender\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setEnabled with arg False\n")
        testobj.sender = mock_sender_2
        testobj.check_modes()
        assert capsys.readouterr().out == ("called SearchDialog.sender\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setEnabled with arg True\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SearchDialog.accept
        """
        def mock_show(*args):
            print('called show_message with args', args)
        # def mock_find():
        #     print("called TextDocument.FindFlags")
        #     return 0
        monkeypatch.setattr(testee, 'show_message', mock_show)
        # monkeypatch.setattr(testee.gui.QTextDocument, 'FindFlags', mock_find)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj.t_zoek = mockqtw.MockLineEdit()
        testobj.c_curr = mockqtw.MockCheckBox()
        testobj.c_titl = mockqtw.MockCheckBox()
        testobj.c_text = mockqtw.MockCheckBox()
        testobj.c_hlett = mockqtw.MockCheckBox()
        testobj.c_woord = mockqtw.MockCheckBox()
        testobj.c_lijst = mockqtw.MockCheckBox()
        testobj.c_wrap = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n")
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                f"called show_message with args ({testobj}, 'Wel iets te zoeken opgeven')\n")
        testobj.t_zoek.setText('Zoek')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `Zoek`\n"
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                f"called show_message with args ({testobj}, 'Wel een zoek modus kiezen')\n")
        testobj.c_titl.setChecked(True)
        testobj.c_text.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n")
        testobj.accept()
        assert testobj.parent.srchtext == 'Zoek'
        assert testobj.parent.srchtype == 3
        assert testobj.parent.srchflags == testee.gui.QTextDocument.FindFlag
        assert not testobj.parent.srchlist
        assert not testobj.parent.srchwrap
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called Dialog.accept\n")
        testobj.c_titl.setChecked(False)
        testobj.c_text.setChecked(False)
        testobj.c_curr.setChecked(True)
        testobj.c_woord.setChecked(True)
        testobj.c_lijst.setChecked(True)
        testobj.c_wrap.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n")
        testobj.accept()
        assert testobj.parent.srchtext == 'Zoek'
        assert testobj.parent.srchtype == 0
        assert testobj.parent.srchflags.value == 4
        assert testobj.parent.srchlist
        assert testobj.parent.srchwrap
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called Dialog.accept\n")
        testobj.c_hlett.setChecked(True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"
        testobj.accept()
        assert testobj.parent.srchtext == 'Zoek'
        assert testobj.parent.srchtype == 0
        assert testobj.parent.srchflags.value == 6
        assert testobj.parent.srchlist
        assert testobj.parent.srchwrap
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called Dialog.accept\n")

        testobj.parent.srchflags = testee.gui.QTextDocument.FindFlag
        testobj.c_woord.setChecked(False)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg False\n"
        testobj.accept()
        assert testobj.parent.srchtext == 'Zoek'
        assert testobj.parent.srchtype == 0
        assert testobj.parent.srchflags.value == 2
        assert testobj.parent.srchlist
        assert testobj.parent.srchwrap
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called Dialog.accept\n")


class TestResultsDialog:
    """unittest for qtgui.ResultsDialog

    wordt alleen gestuurd als er resultaten zijn voor zoeken in titels en/of teksten
    dus current_text (mode 0) en geen zoekresultaten hoeven niet getest worden
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.ResultsDialog object

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
        testobj.parent = MockMainGui()
        testobj.parent.master = MockEditor()
        assert capsys.readouterr().out == 'called ResultsDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ResultsDialog.__init__
        """
        def mock_populate(self):
            print('called ResultsDialog.populate_list')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTreeWidget)
        monkeypatch.setattr(testee.ResultsDialog, 'populate_list', mock_populate)
        parent = MockMainGui()
        parent.title = 'Title'
        parent.nt_icon = 'Icon'
        parent.srchtype = 0  # hoeft eigenlijk niet
        parent.srchtext = 'Find'
        testobj = testee.ResultsDialog(parent)
        assert isinstance(testobj.result_list, testee.qtw.QTreeWidget)
        assert isinstance(testobj.next_button, testee.qtw.QPushButton)
        assert isinstance(testobj.prev_button, testee.qtw.QPushButton)
        assert capsys.readouterr().out == expected_output['resultsdialog'].format(testobj=testobj,
                                                                                  where='')
        parent.srchtype = 1
        testobj = testee.ResultsDialog(parent)
        assert capsys.readouterr().out == expected_output['resultsdialog'].format(testobj=testobj,
                                                                                  where='titles')
        parent.srchtype = 2
        testobj = testee.ResultsDialog(parent)
        assert capsys.readouterr().out == expected_output['resultsdialog'].format(testobj=testobj,
                                                                                  where='texts')
        parent.srchtype = 3
        testobj = testee.ResultsDialog(parent)
        assert capsys.readouterr().out == expected_output['resultsdialog'].format(
                testobj=testobj, where='titles and texts')

    def test_populate_list(self, monkeypatch, capsys):
        """unittest for ResultsDialog.populate_list
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.search_results = [(1, 'title', 'xxx', 'yyy'),
                                                (1, 'text', 'xxx', 'yyy'),
                                                (2, 'text', 'aaa', 'bbb'),
                                                (3, 'title', 'qqq', 'rrr')]
        testobj.result_list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.populate_list()
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with arg `xxx` for col 0\n"
                                           "called TreeItem.setData to `1` with role 256 for col 0\n"
                                           "called TreeItem.setText with arg `yyy` for col 1\n"
                                           "called TreeItem.setData to `1` with role 256 for col 1\n"
                                           "called Tree.addTopLevelItem\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with arg `aaa` for col 0\n"
                                           "called TreeItem.setData to `2` with role 256 for col 0\n"
                                           "called TreeItem.setText with arg `bbb` for col 1\n"
                                           "called TreeItem.setData to `2` with role 256 for col 1\n"
                                           "called Tree.addTopLevelItem\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with arg `qqq` for col 0\n"
                                           "called TreeItem.setData to `3` with role 256 for col 0\n"
                                           "called TreeItem.setText with arg `rrr` for col 1\n"
                                           "called TreeItem.setData to `3` with role 256 for col 1\n"
                                           "called Tree.addTopLevelItem\n")

    def test_goto_next(self, monkeypatch, capsys):
        """unittest for ResultsDialog.goto_next
        """
        def mock_goto():
            print('called ResultsDialog.goto_selected')
        def mock_below(arg):
            print(f'called Tree.itemBelow with arg {arg}')
            return None
        def mock_show(*args):
            print('called show_message with args', args)
        monkeypatch.setattr(testee, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.goto_selected = mock_goto
        testobj.next_button = mockqtw.MockPushButton()
        testobj.result_list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called Tree.__init__\n")
        testobj.goto_next()
        assert capsys.readouterr().out == ("called Tree.itemBelow with arg called Tree.currentItem\n"
                                           "called Tree.setCurrentItem with arg `x`\n"
                                           "called ResultsDialog.goto_selected\n")
        testobj.result_list.itemBelow = mock_below
        testobj.goto_next()
        assert capsys.readouterr().out == ("called Tree.itemBelow with arg called Tree.currentItem\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           f"called show_message with args ({testobj},"
                                           " 'This is the last one')\n")

    def test_goto_prev(self, monkeypatch, capsys):
        """unittest for ResultsDialog.goto_prev
        """
        def mock_goto():
            print('called ResultsDialog.goto_selected')
        def mock_above(arg):
            print(f'called Tree.itemAbove with arg {arg}')
            return None
        def mock_show(*args):
            print('called show_message with args', args)
        monkeypatch.setattr(testee, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.goto_selected = mock_goto
        testobj.prev_button = mockqtw.MockPushButton()
        testobj.result_list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called Tree.__init__\n")
        testobj.goto_prev()
        assert capsys.readouterr().out == ("called Tree.itemAbove with arg called Tree.currentItem\n"
                                           "called Tree.setCurrentItem with arg `x`\n"
                                           "called ResultsDialog.goto_selected\n")
        testobj.result_list.itemAbove = mock_above
        testobj.goto_prev()
        assert capsys.readouterr().out == ("called Tree.itemAbove with arg called Tree.currentItem\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           f"called show_message with args ({testobj},"
                                           " 'This is the first one')\n")

    def test_goto_selected(self, monkeypatch, capsys):
        """unittest for ResultsDialog.goto_selected
        """
        def mock_goto():
            print('called Editor.go_to_result')
        def mock_current():
            print('called Tree.currentItem')
            return resultitem
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.go_to_result = mock_goto
        testobj.next_button = mockqtw.MockPushButton()
        testobj.prev_button = mockqtw.MockPushButton()
        testobj.result_list = mockqtw.MockTreeWidget()
        resultitem = mockqtw.MockTreeItem()
        resultitem.setData(0, testee.core.Qt.ItemDataRole.UserRole, 'xxx')
        assert capsys.readouterr().out == (
                "called PushButton.__init__ with args () {}\n"
                "called PushButton.__init__ with args () {}\n"
                "called Tree.__init__\n"
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setData to `xxx` with role 256 for col 0\n")
        testobj.result_list.currentItem = mock_current
        testobj.goto_selected()
        assert testobj.parent.master.srchno == "xxx"
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called Tree.currentItem\n"
                                           "called TreeItem.data for col 0 role 256\n"
                                           "called Editor.go_to_result\n")
        testobj.goto_selected()
        assert testobj.parent.master.srchno == "xxx"
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           "called TreeItem.data for col 0 role 256\n"
                                           "called Editor.go_to_result\n")

    def test_goto_and_close(self, monkeypatch, capsys):
        """unittest for ResultsDialog.goto_and_close
        """
        def mock_goto():
            print('called ResultsDialog.goto_selected')
        def mock_accept():
            print('called ResultsDialog.accept')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.goto_selected = mock_goto
        testobj.accept = mock_accept
        testobj.goto_and_close()
        assert capsys.readouterr().out == ("called ResultsDialog.goto_selected\n"
                                           "called ResultsDialog.accept\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for ResultsDialog.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.accept()
        assert not testobj.parent.srchlist
        assert capsys.readouterr().out == "called Dialog.accept\n"

    def test_reject(self, monkeypatch, capsys):
        """unittest for ResultsDialog.reject
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reject()
        assert not testobj.parent.srchlist
        assert capsys.readouterr().out == "called Dialog.reject\n"


class TestUndoRedoStack:
    """unittest for qtgui.UndoRedoStack
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.UndoRedoStack object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called UndoRedoStack.__init__ with args', args)
        monkeypatch.setattr(testee.UndoRedoStack, '__init__', mock_init)
        testobj = testee.UndoRedoStack()
        testobj._parent = MockMainGui()
        testobj.parent = lambda *x: testobj._parent
        assert capsys.readouterr().out == 'called UndoRedoStack.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for UndoRedoStack.__init__
        """
        # monkeypatch.setattr(testee.qtw, 'QUndoStack', mockqtw.MockUndoStack)
        monkeypatch.setattr(testee.gui.QUndoStack, '__init__', mockqtw.MockUndoStack.__init__)
        monkeypatch.setattr(testee.gui.QUndoStack, 'parent', mockqtw.MockUndoStack.parent)
        monkeypatch.setattr(testee.gui.QUndoStack, 'cleanChanged', mockqtw.MockUndoStack.cleanChanged)
        monkeypatch.setattr(testee.gui.QUndoStack, 'indexChanged', mockqtw.MockUndoStack.indexChanged)
        monkeypatch.setattr(testee.gui.QUndoStack, 'setUndoLimit', mockqtw.MockUndoStack.setUndoLimit)
        parent = MockMainGui()
        testobj = testee.UndoRedoStack(parent)
        assert capsys.readouterr().out == (
                f"called UndoStack.__init__ with args ({parent},)\n"
                f"called Signal.connect with args ({testobj.clean_changed},)\n"
                f"called Signal.connect with args ({testobj.index_changed},)\n"
                "called UndoRedoStack.setUndoLimit with arg 1\n"
                "called Action.setText with arg `Nothing to undo`\n"
                "called Action.setText with arg `Nothing to redo`\n"
                "called Action.setDisabled with arg `True`\n"
                "called Action.setDisabled with arg `True`\n")

    def test_clean_changed(self, monkeypatch, capsys):
        """unittest for UndoRedoStack.clean_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clean_changed(False)
        assert capsys.readouterr().out == "called Action.setDisabled with arg `False`\n"
        testobj.clean_changed(True)
        assert capsys.readouterr().out == ("called Action.setText with arg `Nothing to undo`\n"
                                           "called Action.setText with arg `Nothing to redo`\n"
                                           "called Action.setDisabled with arg `True`\n")

    def test_index_changed(self, monkeypatch, capsys):
        """unittest for UndoRedoStack.index_changed
        """
        def mock_undotext():
            print('called UndoRedoStack.undotext')
            return ''
        def mock_undotext_2():
            print('called UndoRedoStack.undotext')
            return 'xxx'
        def mock_redotext():
            print('called UndoRedoStack.redotext')
            return ''
        def mock_redotext_2():
            print('called UndoRedoStack.redotext')
            return 'yyy'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undoText = mock_undotext
        testobj.redoText = mock_redotext
        testobj.index_changed(1)
        assert capsys.readouterr().out == ("called UndoRedoStack.undotext\n"
                                           "called Action.setText with arg `Nothing to undo`\n"
                                           "called Action.setDisabled with arg `True`\n"
                                           "called UndoRedoStack.redotext\n"
                                           "called Action.setText with arg `Nothing to redo`\n"
                                           "called Action.setDisabled with arg `True`\n")
        testobj.undoText = mock_undotext_2
        testobj.redoText = mock_redotext_2
        testobj.index_changed(1)
        assert capsys.readouterr().out == ("called UndoRedoStack.undotext\n"
                                           "called Action.setText with arg `&Undo xxx`\n"
                                           "called Action.setEnabled with arg `True`\n"
                                           "called UndoRedoStack.redotext\n"
                                           "called Action.setText with arg `&Redo yyy`\n"
                                           "called Action.setEnabled with arg `True`\n")


class TestAddCommand:
    """unittest for qtgui.AddCommand
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.AddCommand object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called AddCommand.__init__ with args', args)
        monkeypatch.setattr(testee.AddCommand, '__init__', mock_init)
        testobj = testee.AddCommand()
        testobj.win = MockMainGui()
        testobj.win.master = MockEditor()
        testobj.win.tree = MockTree()
        assert capsys.readouterr().out == ('called AddCommand.__init__ with args ()\n'
                                           "called TreePanel.__init__ with args ()\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for AddCommand.__init__
        """
        def mock_init(self, *args):
            print('called QUndoCommand with args', args)
        monkeypatch.setattr(testee.gui.QUndoCommand, '__init__', mock_init)
        win = MockMainGui()
        win.master = MockEditor()
        win.tree = MockTree()
        win.root = mockqtw.MockTreeItem()
        win.master.activeitem = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called TreePanel.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n")
        testobj = testee.AddCommand(win, None, False, 'new_title', ['extra', 'titles'])
        assert testobj.win == win
        assert testobj.root == win.master.activeitem  # win.root
        assert not testobj.under
        assert testobj.pos == 1
        assert testobj.add_to_itemdict == ['new_title', '', ['extra', '', ['titles', '', []]]]
        assert testobj.is_first_edit
        assert capsys.readouterr().out == (
                f"called TreePanel.getitemparentpos with arg '{testobj.root}'\n"
                "called QUndoCommand with args ('Add',)\n")
        testobj = testee.AddCommand(win, win.root, True, 'new_title', [], 'AddCommand')
        assert testobj.win == win
        assert testobj.root == win.root
        assert testobj.under
        assert testobj.pos == -1
        assert testobj.add_to_itemdict == ['new_title', '', []]
        assert testobj.is_first_edit
        assert capsys.readouterr().out == (
                "called QUndoCommand with args ('AddCommand top level item',)\n")

    def test_redo(self, monkeypatch, capsys):
        """unittest for AddCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = 'root'
        testobj.under = 'under'
        testobj.pos = -1
        testobj.add_to_itemdict = ['new_title', 'text', []]
        testobj.redo()
        assert testobj.data == "data"
        assert capsys.readouterr().out == ("called Editor.do_addaction with args ('root', 'under',"
                                           " -1, ['new_title', 'text', []])\n")

    def test_undo(self, monkeypatch, capsys):
        """unittest for AddCommand.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.data = ['1', ['2'], '3', '4', '5', '6']
        testobj.is_first_edit = False
        testobj.win.master.itemdict = {'1': 'x', '2': 'y'}
        testobj.win.master.views = [['view1', 'q'], ['view2', 'q'], ['view3', 'q']]
        testobj.win.master.opts = {'ActiveView': 1}
        testobj.undo()
        # assert testobj.win.master.views == [['view1'], ['view2', 'q'], ['view3']]
        assert testobj.win.master.views == [['view1', 'q'], ['view2', 'q'], ['view3', 'q']]
        assert capsys.readouterr().out == (
                # "called TreePanel.removeitem with args ('3', [('1', 'x'), ('2', 'y')])\n")
                "called TreePanel.removeitem with args (['1', ['2'], '3', '4', '5', '6'],)\n")
        testobj.data = ['1', [], '3', '4', '6']
        testobj.is_first_edit = True
        testobj.win.master.views = [['view1', 'q']]
        testobj.win.master.opts = {'ActiveView': 0}
        testobj.undo()
        assert testobj.win.master.views == [['view1', 'q']]
        assert capsys.readouterr().out == (
                # "called TreePanel.removeitem with args ('3', [('1', 'x')])\n"
                "called TreePanel.removeitem with args (['1', [], '3', '4', '6'],)\n"
                "called Editor.set_project_dirty with arg False\n")


class TestPasteCommand:
    """unittest for qtgui.PasteCommand
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.PasteCommand object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called PasteCommand.__init__ with args', args)
        monkeypatch.setattr(testee.PasteCommand, '__init__', mock_init)
        testobj = testee.PasteCommand()
        testobj.win = MockMainGui()
        testobj.win.statusbar = mockqtw.MockStatusBar()
        testobj.win.master = MockEditor()
        testobj.win.tree = MockTree()
        assert capsys.readouterr().out == ('called PasteCommand.__init__ with args ()\n'
                                           'called StatusBar.__init__ with args ()\n'
                                           'called TreePanel.__init__ with args ()\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for PasteCommand.__init__
        """
        def mock_init(self, *args):
            print('called QUndoCommand with args', args)
        monkeypatch.setattr(testee.gui.QUndoCommand, '__init__', mock_init)
        win = MockMainGui()
        win.master = MockEditor()
        win.tree = MockTree()
        win.master.project_dirty = False
        item = mockqtw.MockTreeItem('xxx', '111')
        assert capsys.readouterr().out == ("called TreePanel.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ('xxx', '111')\n")
        testobj = testee.PasteCommand(win, False, False, item, description="Paste")
        assert not testobj.before
        assert not testobj.below
        assert testobj.item == item
        assert testobj.first_edit
        assert testobj.replaced is None
        assert capsys.readouterr().out == "called QUndoCommand with args ('Paste After',)\n"
        win.master.project_dirty = True
        testobj = testee.PasteCommand(win, False, True, item, description="Paste")
        assert not testobj.before
        assert testobj.below
        assert testobj.item == item
        assert not testobj.first_edit
        assert testobj.replaced is None
        assert capsys.readouterr().out == "called QUndoCommand with args ('Paste Under',)\n"
        testobj = testee.PasteCommand(win, True, False, item, description="Paste")
        assert testobj.before
        assert not testobj.below
        assert testobj.item == item
        assert not testobj.first_edit
        assert testobj.replaced is None
        assert capsys.readouterr().out == "called QUndoCommand with args ('Paste Before',)\n"
        testobj = testee.PasteCommand(win, True, True, item, description="Paste")
        assert testobj.before
        assert testobj.below
        assert testobj.item == item
        assert not testobj.first_edit
        assert testobj.replaced is None
        assert capsys.readouterr().out == "called QUndoCommand with args ('Paste Under',)\n"

    def test_redo(self, monkeypatch, capsys):
        """unittest for PasteCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.win.master.views = ['views']
        testobj.before = 'before'
        testobj.below = 'below'
        testobj.item = 'item'
        testobj.redo()
        assert testobj.views == testobj.win.master.views
        assert testobj.used_keys == 'keys'
        assert testobj.used_parent == 'parent'
        assert capsys.readouterr().out == (
                "called Editor.do_pasteaction with args ('before', 'below', 'item')\n")

    def test_undo(self, monkeypatch, capsys):
        """unittest for PasteCommand.undo
        """
        def mock_text():
            print('called PasteCommand.text')
            return 'Paste action'
        parent = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.used_keys = []
        testobj.win.master.itemdict = {'xx': 'xxxx', 'yy': 'yyyy'}
        testobj.used_parent = (parent, 2)
        testobj.views = ['views']
        testobj.first_edit = False
        testobj.text = mock_text
        testobj.undo()
        assert testobj.win.master.itemdict == {'xx': 'xxxx', 'yy': 'yyyy'}
        assert testobj.win.master.views == ['views']
        assert capsys.readouterr().out == (
                "called TreeItem.takeChild\n"
                "called PasteCommand.text\n"
                "called StatusBar.showMessage with arg `Paste action undone`\n")

        testobj.win.master.views = []
        testobj.used_keys = ['xx']
        testobj.used_parent = (parent, -1)
        testobj.first_edit = True
        testobj.undo()
        assert testobj.win.master.itemdict == {'yy': 'yyyy'}
        assert testobj.win.master.views == ['views']
        assert capsys.readouterr().out == (
                "called TreeItem.childCount\n"
                "called TreeItem.takeChild\n"
                "called Editor.set_project_dirty with arg False\n"
                "called PasteCommand.text\n"
                "called StatusBar.showMessage with arg `Paste action undone`\n")


class TestCopyCommand:
    """unittest for qtgui.CopyCommand
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.CopyCommand object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CopyCommand.__init__ with args', args)
        monkeypatch.setattr(testee.CopyCommand, '__init__', mock_init)
        testobj = testee.CopyCommand()
        testobj.win = MockMainGui()
        testobj.win.master = MockEditor()
        testobj.win.statusbar = mockqtw.MockStatusBar()
        testobj.win.tree = MockTree()
        assert capsys.readouterr().out == ('called CopyCommand.__init__ with args ()\n'
                                           'called StatusBar.__init__ with args ()\n'
                                           'called TreePanel.__init__ with args ()\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for CopyCommand.__init__
        """
        def mock_init(self, *args):
            print('called QUndoCommand with args', args)
        monkeypatch.setattr(testee.gui.QUndoCommand, '__init__', mock_init)
        win = MockMainGui()
        win.master = MockEditor()
        win.tree = MockTree()
        win.master.project_dirty = False
        item = mockqtw.MockTreeItem('xxx', '111')
        assert capsys.readouterr().out == ("called TreePanel.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ('xxx', '111')\n")
        testobj = testee.CopyCommand(win, False, False, item)
        assert testobj.undodata is None
        assert testobj.win == win
        assert testobj.item == item
        assert testobj.first_edit
        assert not testobj.cut
        assert not testobj.retain
        assert capsys.readouterr().out == "called QUndoCommand with args ('Copy',)\n"
        win.master.project_dirty = True
        testobj = testee.CopyCommand(win, False, True, item)
        assert testobj.undodata is None
        assert testobj.win == win
        assert testobj.item == item
        assert not testobj.first_edit
        assert not testobj.cut
        assert testobj.retain
        assert capsys.readouterr().out == "called QUndoCommand with args ('Copy',)\n"
        testobj = testee.CopyCommand(win, True, False, item)
        assert testobj.undodata is None
        assert testobj.win == win
        assert testobj.item == item
        assert not testobj.first_edit
        assert testobj.cut
        assert not testobj.retain
        assert capsys.readouterr().out == "called QUndoCommand with args ('Delete',)\n"
        testobj = testee.CopyCommand(win, True, True, item)
        assert testobj.undodata is None
        assert testobj.win == win
        assert testobj.item == item
        assert not testobj.first_edit
        assert testobj.cut
        assert testobj.retain
        assert capsys.readouterr().out == "called QUndoCommand with args ('Cut',)\n"

    def test_redo(self, monkeypatch, capsys):
        """unittest for CopyCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.key = 'xx'
        testobj.cut = 'cut'
        testobj.retain = 'retain'
        testobj.item = 'item'
        # testobj.win.master.itemdict = {'xx': 'xxxx'}
        testobj.win.master.views = ['yyy']
        testobj.win.master.opts = {'ActiveItem': 'q'}
        testobj.redo()
        assert testobj.oldstate == ('q', ['yyy'])
        assert testobj.newstate == ('opts', 'views')
        assert capsys.readouterr().out == (
                "called Editor.do_addaction with args ('cut', 'retain', 'item')\n")

    def test_undo(self, monkeypatch, capsys):
        """unittest for CopyCommand.undo
        """
        def mock_text():
            print('called CopyCommand.text')
            return 'Copy action'
        def mock_put(*args, **kwargs):
            print('called Tree.putsubtree with args', args, kwargs)
            return 'yy'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.newstate = (['copied', 'items'], ('oldloc', 2), [('cut', 'from'), ('item', 'dict')])
        testobj.oldstate = ('xx', ['views'])
        testobj.cut = False
        testobj.win.master.itemdict = {}
        testobj.item = ''
        testobj.win.master.activeitem = ''
        testobj.win.master.opts = {}
        testobj.win.tree.putsubtree = mock_put
        testobj.first_edit = False
        testobj.text = mock_text
        testobj.undo()
        assert testobj.win.master.itemdict == {}
        assert testobj.win.master.activeitem == ''
        assert testobj.item == ''
        assert testobj.win.master.opts["ActiveItem"] == 'xx'
        assert testobj.win.master.views == ['views']
        assert capsys.readouterr().out == (
                "called CopyCommand.text\n"
                "called StatusBar.showMessage with arg `Copy action undone`\n")
        testobj.cut = True
        testobj.first_edit = True
        testobj.undo()
        assert testobj.win.master.itemdict == {'cut': 'from', 'item': 'dict'}
        assert testobj.win.master.activeitem == 'yy'
        assert testobj.item == 'yy'
        assert testobj.win.master.opts["ActiveItem"] == 'xx'
        assert testobj.win.master.views == ['views']
        assert capsys.readouterr().out == (
                "called Tree.putsubtree with args ('oldloc', 'copied', 'items') {'pos': 1}\n"
                "called Editor.set_project_dirty with arg False\n"
                "called CopyCommand.text\n"
                "called StatusBar.showMessage with arg `Copy action undone`\n")


class TestTreePanel:
    """unittest for qtgui.TreePanel
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.TreePanel object

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
        testobj.parent = MockMainGui()
        testobj.parent.master = MockEditor()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for TreePanel.__init__
        """
        monkeypatch.setattr(testee.qtw.QTreeWidget, '__init__', mockqtw.MockTreeWidget.__init__)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setColumnCount',
                            mockqtw.MockTreeWidget.setColumnCount)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'hideColumn', mockqtw.MockTreeWidget.hideColumn)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'headerItem', mockqtw.MockTreeWidget.headerItem)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setAcceptDrops',
                            mockqtw.MockTreeWidget.setAcceptDrops)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setDragEnabled',
                            mockqtw.MockTreeWidget.setDragEnabled)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setSelectionMode',
                            mockqtw.MockTreeWidget.setSelectionMode)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setDragDropMode',
                            mockqtw.MockTreeWidget.setDragDropMode)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setDropIndicatorShown',
                            mockqtw.MockTreeWidget.setDropIndicatorShown)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setUniformRowHeights',
                            mockqtw.MockTreeWidget.setUniformRowHeights)
        # monkeypatch.setattr(testee.qtw.QTreeWidget, 'SingleSelection',
        #                     mockqtw.MockTreeWidget.SingleSelection)
        # monkeypatch.setattr(testee.qtw.QTreeWidget, 'InternalMove',
        #                     mockqtw.MockTreeWidget.InternalMove)
        parent = MockEditor()
        testobj = testee.TreePanel(parent)
        assert capsys.readouterr().out == (
                "called Tree.__init__\n"
                "called Tree.setColumnCount with arg `2`\n"
                "called Tree.hideColumn\n"
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setHidden with arg `True`\n"
                "called Tree.setAcceptDrops with arg True\n"
                "called Tree.setDragEnabled with arg True\n"
                "called Tree.setSelectionMode\n"
                "called Tree.setDragDropMode with arg DragDropMode.InternalMove\n"
                "called Tree.setDropIndicatorShown with arg True\n"
                "called Tree.setUniformRowHeights with arg `True`\n")

    def test_selectionChanged(self, monkeypatch, capsys):
        """unittest for TreePanel.selectionChanged
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'currentItem',
                            mockqtw.MockTreeWidget.currentItem)
        testobj.selectionChanged('newsel', ' oldsel')
        assert capsys.readouterr().out == ("called Editor.check_active\n"
                                           "called Editor.activate_item with arg {item}\n"
                                           "called Editor.set_window_title\n")

    def test_dropEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.dropEvent
        """
        def mock_selected():
            print('called Tree.selectedItems')
            return ['xxx', 'yyy']
        def mock_itemat(linecol):
            print(f'called Tree.itemAt with arg ({linecol})')
            return None
        def mock_itemat_2(linecol):
            print(f'called Tree.itemAt with arg ({linecol})')
            return dropitem
        def mock_count():
            print('called Tree.topLevelItemCount')
            return 1
        def mock_count_2():
            print('called Tree.topLevelItemCount')
            return 2
        def mock_item(number):
            print(f'called Tree.topLevelItem with arg {number}')
            if number == 0:
                return None
            return 'xxx'
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'dropEvent',
                            mockqtw.MockTreeWidget.dropEvent)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setCurrentItem',
                            mockqtw.MockTreeWidget.setCurrentItem)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'takeTopLevelItem',
                            mockqtw.MockTreeWidget.takeTopLevelItem)
        monkeypatch.setattr(testee.qtw.QTreeWidgetItem, 'insertChild',
                            mockqtw.MockTreeItem.insertChild)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.selectedItems = mock_selected
        testobj.itemAt = mock_itemat
        event = mockqtw.MockEvent()
        assert capsys.readouterr().out == ""
        testobj.dropEvent(event)
        assert capsys.readouterr().out == ("called Tree.selectedItems\n"
                                           "called Tree.itemAt with arg ((1, 2))\n")

        testobj.itemAt = mock_itemat_2
        dropitem = mockqtw.MockTreeItem()
        testobj.oldparent = mockqtw.MockTreeItem()
        testobj.oldpos = 1
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n")
        testobj.topLevelItemCount = mock_count
        testobj.topLevelItem = mock_item
        testobj.dropEvent(event)
        assert capsys.readouterr().out == ("called Tree.selectedItems\n"
                                           "called Tree.itemAt with arg ((1, 2))\n"
                                           f"called Tree.dropEvent with arg {event}\n"
                                           "called Tree.topLevelItemCount\n"
                                           "called Editor.set_project_dirty with arg True\n"
                                           "called Tree.setCurrentItem with arg `xxx`\n"
                                           "called TreeItem.setExpanded with arg `True`\n")

        testobj.topLevelItemCount = mock_count_2
        testobj.dropEvent(event)
        assert capsys.readouterr().out == ("called Tree.selectedItems\n"
                                           "called Tree.itemAt with arg ((1, 2))\n"
                                           f"called Tree.dropEvent with arg {event}\n"
                                           "called Tree.topLevelItemCount\n"
                                           "called Tree.topLevelItem with arg 0\n"
                                           "called Tree.topLevelItem with arg 1\n"
                                           "called Tree.takeTopLevelItem with arg `1`\n"
                                           "called TreeItem.insertChild at pos 1\n"
                                           "called Tree.setCurrentItem with arg `xxx`\n")

    def test_mousePressEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mousePressEvent
        """
        def mock_itemat(pos):
            print(f'called Tree.itemAt with args {pos}')
            return ''
        def mock_get(item):
            print(f'called Tree.getitemparentpos with arg `{item}`')
            return 'parent', 'pos'
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'mousePressEvent',
                            mockqtw.MockTreeWidget.mousePressEvent)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'itemAt',
                            mockqtw.MockTreeWidget.itemAt)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getitemparentpos = mock_get
        event = mockqtw.MockEvent()
        testobj.mousePressEvent(event)
        assert capsys.readouterr().out == ("called Tree.itemAt with args ((1, 2),)\n"
                                           "called Tree.getitemparentpos with arg `item at (1, 2)`\n"
                                           f"called Tree.mousePressEvent with arg {event}\n")
        testobj.itemAt = mock_itemat
        testobj.mousePressEvent(event)
        assert capsys.readouterr().out == ("called Tree.itemAt with args (1, 2)\n"
                                           f"called Tree.mousePressEvent with arg {event}\n")

    def test_mouseReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mouseReleaseEvent
        """
        def mock_itemat(pos):
            print(f'called Tree.itemAt with args {pos}')
            return ''
        def mock_create(item):
            print(f"called Tree.create_popupmenu with arg '{item}'")
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'mouseReleaseEvent',
                            mockqtw.MockTreeWidget.mouseReleaseEvent)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'itemAt',
                            mockqtw.MockTreeWidget.itemAt)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_popupmenu = mock_create
        event = mockqtw.MockEvent()
        testobj.mouseReleaseEvent(event)
        assert capsys.readouterr().out == (f"called Tree.mouseReleaseEvent with arg {event}\n")

        event.button = lambda *x: testee.core.Qt.MouseButton.RightButton
        testobj.mouseReleaseEvent(event)
        assert capsys.readouterr().out == (
                "called Tree.itemAt with args ((1, 2),)\n"
                "called Tree.create_popupmenu with arg 'item at (1, 2)'\n")

        testobj.itemAt = mock_itemat
        testobj.mouseReleaseEvent(event)
        assert capsys.readouterr().out == (
                "called Tree.itemAt with args (1, 2)\n"
                f"called Tree.mouseReleaseEvent with arg {event}\n")

    def test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.keyReleaseEvent
        """
        def mock_create(item):
            print(f"called Tree.create_popupmenu with arg '{item}'")
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'keyReleaseEvent',
                            mockqtw.MockTreeWidget.keyReleaseEvent)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'currentItem',
                            mockqtw.MockTreeWidget.currentItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_popupmenu = mock_create
        event = mockqtw.MockEvent()
        testobj.keyReleaseEvent(event)
        assert capsys.readouterr().out == f"called Tree.keyReleaseEvent with arg {event}\n"

        event.key = lambda *x: testee.core.Qt.Key.Key_Menu
        testobj.keyReleaseEvent(event)
        assert capsys.readouterr().out == (
                "called Tree.create_popupmenu with arg 'called Tree.currentItem'\n")

    def test_create_popupmenu(self, monkeypatch, capsys):
        """unittest for TreePanel.create_popupmenu
        """
        monkeypatch.setattr(testee.qtw, 'QMenu', mockqtw.MockMenu)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'mapToGlobal',
                            mockqtw.MockTreeWidget.mapToGlobal)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'visualItemRect',
                            mockqtw.MockTreeWidget.visualItemRect)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.notemenu = mockqtw.MockMenu()
        testobj.parent.treemenu = mockqtw.MockMenu()
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called Menu.__init__ with args ()\n")
        testobj.parent.root = 'root'
        testobj.create_popupmenu('item')
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Tree.visualItemRect with arg item\n"
                                           "called Tree.mapToGlobal with arg center\n"
                                           "called Menu.exec with args ('mapped-to-global',) {}\n")
        testobj.create_popupmenu('root')
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Tree.visualItemRect with arg root\n"
                                           "called Tree.mapToGlobal with arg center\n"
                                           "called Menu.exec with args ('mapped-to-global',) {}\n")
        testobj.parent.notemenu.addAction(mockqtw.MockAction('&Add', ''))
        testobj.parent.notemenu.addAction(mockqtw.MockAction('&Delete', ''))
        testobj.parent.notemenu.addAction(mockqtw.MockAction('&Forward', ''))
        testobj.parent.notemenu.addAction(mockqtw.MockAction('&Back', ''))
        testobj.parent.notemenu.addAction(mockqtw.MockAction('Other', ''))
        testobj.parent.treemenu.addAction(mockqtw.MockAction('Anything', ''))
        assert capsys.readouterr().out == ("called Action.__init__ with args ('&Add', '')\n"
                                           "called Menu.addAction\n"
                                           "called Action.__init__ with args ('&Delete', '')\n"
                                           "called Menu.addAction\n"
                                           "called Action.__init__ with args ('&Forward', '')\n"
                                           "called Menu.addAction\n"
                                           "called Action.__init__ with args ('&Back', '')\n"
                                           "called Menu.addAction\n"
                                           "called Action.__init__ with args ('Other', '')\n"
                                           "called Menu.addAction\n"
                                           "called Action.__init__ with args ('Anything', '')\n"
                                           "called Menu.addAction\n")
        testobj.create_popupmenu('item')
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction\n"
                                           "called Tree.visualItemRect with arg item\n"
                                           "called Tree.mapToGlobal with arg center\n"
                                           "called Menu.exec with args ('mapped-to-global',) {}\n")
        testobj.create_popupmenu('root')
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called Menu.addAction\n"
                                           "called Action.text\n"
                                           "called Action.setEnabled with arg `False`\n"
                                           "called Menu.addAction\n"
                                           "called Action.text\n"
                                           "called Action.setEnabled with arg `False`\n"
                                           "called Menu.addAction\n"
                                           "called Action.text\n"
                                           "called Action.setEnabled with arg `False`\n"
                                           "called Menu.addAction\n"
                                           "called Action.text\n"
                                           "called Action.setEnabled with arg `False`\n"
                                           "called Menu.addAction\n"
                                           "called Action.text\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction\n"
                                           "called Action.setEnabled with arg `False`\n"
                                           "called Tree.visualItemRect with arg root\n"
                                           "called Tree.mapToGlobal with arg center\n"
                                           "called Menu.exec with args ('mapped-to-global',) {}\n"
                                           "called Action.text\n"
                                           "called Action.setEnabled with arg `True`\n"
                                           "called Action.text\n"
                                           "called Action.setEnabled with arg `True`\n"
                                           "called Action.text\n"
                                           "called Action.setEnabled with arg `True`\n"
                                           "called Action.text\n"
                                           "called Action.setEnabled with arg `True`\n"
                                           "called Action.text\n"
                                           "called Action.setEnabled with arg `True`\n")

    def test_add_to_parent(self, monkeypatch, capsys):
        """unittest for TreePanel.add_to_parent
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        monkeypatch.setattr(testee.gui, 'QTextDocument', mockqtw.MockTextDocument)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.itemdict = {'itemkey': ['title', 'And this is the text']}
        parent = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.add_to_parent('itemkey', 'titel', parent)
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setText with arg `titel` for col 0\n"
                "called TextDocument.__init__ with args ()\n"
                "called TextDocument.setHtml with arg 'And this is the text'\n"
                "called TextDocument.toPlainText\n"
                "called TreeItem.setData to `plain text` with role 256 for col 0\n"
                "called TreeItem.setText with arg `itemkey` for col 1\n"
                "called TreeItem.setTooltip with args (0, 'titel')\n"
                "called TreeItem.addChild\n")
        testobj.add_to_parent('itemkey', 'titel', parent, pos=1)
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setText with arg `titel` for col 0\n"
                "called TextDocument.__init__ with args ()\n"
                "called TextDocument.setHtml with arg 'And this is the text'\n"
                "called TextDocument.toPlainText\n"
                "called TreeItem.setData to `plain text` with role 256 for col 0\n"
                "called TreeItem.setText with arg `itemkey` for col 1\n"
                "called TreeItem.setTooltip with args (0, 'titel')\n"
                "called TreeItem.insertChild at pos 1\n")

    def test_getitemdata(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemdata
        """
        def mock_get_title(arg):
            print(f"called Tree.getitemtitle with arg '{arg}'")
            return 'title'
        def mock_get_key(arg):
            print(f"called Tree.getitemkey with arg '{arg}'")
            return 'key'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getitemtitle = mock_get_title
        testobj.getitemkey = mock_get_key
        assert testobj.getitemdata('item') == ('title', 'key')
        assert capsys.readouterr().out == ("called Tree.getitemtitle with arg 'item'\n"
                                           "called Tree.getitemkey with arg 'item'\n")

    def test_getitemuserdata(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemuserdata
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        item.setData(0, testee.core.Qt.ItemDataRole.UserRole, 'data')
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setData to `data` with role"
                f" {testee.core.Qt.ItemDataRole.UserRole} for col 0\n")
        assert testobj.getitemuserdata(item) == "data"
        assert capsys.readouterr().out == (
                f"called TreeItem.data for col 0 role {testee.core.Qt.ItemDataRole.UserRole}\n")

    def test_getitemtitle(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemtitle
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem('xxx')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx',)\n"
        assert testobj.getitemtitle(item) == "xxx"
        assert capsys.readouterr().out == "called TreeItem.text for col 0\n"

    def test_getitemkey(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemkey
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem('xxx', 'yyy')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx', 'yyy')\n"
        assert testobj.getitemkey(item) == -1
        assert capsys.readouterr().out == "called TreeItem.text for col 1\n"
        item = mockqtw.MockTreeItem('xxx', '111')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx', '111')\n"
        assert testobj.getitemkey(item) == 111
        assert capsys.readouterr().out == "called TreeItem.text for col 1\n"

    def test_setitemtitle(self, monkeypatch, capsys):
        """unittest for TreePanel.setitemtitle
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.setitemtitle(item, 'title')
        assert capsys.readouterr().out == ("called TreeItem.setText with arg `title` for col 0\n"
                                           "called TreeItem.setTooltip with args (0, 'title')\n")

    def test_setitemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.setitemtext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.setitemtext(item, 'text')
        assert capsys.readouterr().out == "called TreeItem.setText with arg `text` for col 1\n"

    def test_getitemkids(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemkids
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        item2 = mockqtw.MockTreeItem()
        item3 = mockqtw.MockTreeItem()
        item.addChild(item2)
        item.addChild(item3)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.addChild\n")
        assert testobj.getitemkids(item) == [item2, item3]
        assert capsys.readouterr().out == ("called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.child with arg 1\n")

    def test_getitemparentpos(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemparentpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        parent = mockqtw.MockTreeItem()
        parent.addChild(mockqtw.MockTreeItem())
        item = mockqtw.MockTreeItem()
        parent.addChild(item)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n")
        assert testobj.getitemparentpos(item) == (parent, 1)
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.indexOfChild\n")

    def test_getselecteditem(self, monkeypatch, capsys):
        """unittest for TreePanel.getselecteditem
        """
        def mock_selected():
            print('called Tree.selectedItems')
            return ['xxx', 'yyy']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.selectedItems = mock_selected
        assert testobj.getselecteditem() == "xxx"
        assert capsys.readouterr().out == "called Tree.selectedItems\n"

    def test_set_item_expanded(self, monkeypatch, capsys):
        """unittest for TreePanel.set_item_expanded
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_item_expanded(item)
        assert capsys.readouterr().out == "called TreeItem.setExpanded with arg `True`\n"

    def test_set_item_collapsed(self, monkeypatch, capsys):
        """unittest for TreePanel.set_item_collapsed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_item_collapsed(item)
        assert capsys.readouterr().out == "called TreeItem.setExpanded with arg `False`\n"

    def test_set_item_selected(self, monkeypatch, capsys):
        """unittest for TreePanel.set_item_selected
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setCurrentItem',
                            mockqtw.MockTreeWidget.setCurrentItem)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_item_selected(item)
        assert capsys.readouterr().out == f"called Tree.setCurrentItem with arg `{item}`\n"

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for TreePanel.get_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'currentItem',
                            mockqtw.MockTreeWidget.currentItem)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        assert testobj.get_selected_item() == "called Tree.currentItem"

    def test_removeitem(self, monkeypatch, capsys):
        """unittest for treepanel.removeitem
        """
        def mock_parentpos(arg):
            print(f'called Tree.getparentpos with arg {arg}')
            return parent, 1
        def mock_pop(*args):
            print('called mainwindow.popitems with args', args)
            return ['popped', 'items']
        root = mockqtw.MockTreeItem()
        parent = mockqtw.MockTreeItem()
        child1 = mockqtw.MockTreeItem()
        child2 = mockqtw.MockTreeItem()
        parent.addChild(child1)
        parent.addChild(child2)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.addChild\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getitemparentpos = mock_parentpos
        testobj.parent.root = root
        testobj.parent.master.popitems = mock_pop
        assert testobj.removeitem(child2) == ((parent, 1), child1, ['popped', 'items'])
        assert capsys.readouterr().out == (f"called Tree.getparentpos with arg {child2}\n"
                                           "called TreeItem.child with arg 0\n"
                                           f"called mainwindow.popitems with args ({child2}, [])\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.takeChild\n")

    def test_removeitem_2(self, monkeypatch, capsys):
        """unittest for treepanel.removeitem
        """
        def mock_parentpos(arg):
            print(f'called Tree.getparentpos with arg {arg}')
            return parent, 1
        def mock_pop(*args):
            print('called MainWindow.popitems with args', args)
            return ['popped', 'items']
        root = mockqtw.MockTreeItem()
        parent = mockqtw.MockTreeItem()
        child1 = mockqtw.MockTreeItem()
        child2 = mockqtw.MockTreeItem()
        child3 = mockqtw.MockTreeItem()
        parent.addChild(child1)
        parent.addChild(child2)
        child2.addChild(child3)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.addChild\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getitemparentpos = mock_parentpos
        testobj.parent.root = root
        testobj.parent.master.popitems = mock_pop
        assert testobj.removeitem(child2) == ((parent, 1), child1, ['popped', 'items'])
        assert capsys.readouterr().out == (f"called Tree.getparentpos with arg {child2}\n"
                                           "called TreeItem.child with arg 0\n"
                                           f"called MainWindow.popitems with args ({child2}, [])\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.takeChild\n"
                                           "called TreeItem.takeChild\n")

    def test_removeitem_3(self, monkeypatch, capsys):
        """unittest for treepanel.removeitem
        """
        def mock_parentpos(arg):
            print(f'called Tree.getparentpos with arg {arg}')
            return parent, 0
        def mock_pop(*args):
            print('called MainWindow.popitems with args', args)
            return ['popped', 'items']
        root = mockqtw.MockTreeItem()
        parent = mockqtw.MockTreeItem()
        child1 = mockqtw.MockTreeItem()
        child2 = mockqtw.MockTreeItem()
        parent.addChild(child1)
        parent.addChild(child2)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.addChild\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getitemparentpos = mock_parentpos
        testobj.parent.root = root
        testobj.parent.master.popitems = mock_pop
        assert testobj.removeitem(child1) == ((parent, 0), parent, ['popped', 'items'])
        assert capsys.readouterr().out == (f"called Tree.getparentpos with arg {child1}\n"
                                           f"called MainWindow.popitems with args ({child1}, [])\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.takeChild\n")

    def test_removeitem_4(self, monkeypatch, capsys):
        """unittest for treepanel.removeitem
        """
        def mock_parentpos(arg):
            print(f'called Tree.getparentpos with arg {arg}')
            return parent, 0
        def mock_pop(*args):
            print('called MainWindow.popitems with args', args)
            return ['popped', 'items']
        root = mockqtw.MockTreeItem()
        parent = mockqtw.MockTreeItem()
        child1 = mockqtw.MockTreeItem()
        child2 = mockqtw.MockTreeItem()
        parent.addChild(child1)
        parent.addChild(child2)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.addChild\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getitemparentpos = mock_parentpos
        testobj.parent.root = parent
        testobj.parent.master.popitems = mock_pop
        assert testobj.removeitem(child1) == ((parent, 0), child2, ['popped', 'items'])
        assert capsys.readouterr().out == (f"called Tree.getparentpos with arg {child1}\n"
                                           "called TreeItem.child with arg 1\n"
                                           f"called MainWindow.popitems with args ({child1}, [])\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.takeChild\n")

    def test_removeitem_5(self, monkeypatch, capsys):
        """unittest for treepanel.removeitem
        """
        def mock_parentpos(arg):
            print(f'called Tree.getparentpos with arg {arg}')
            return parent, 0
        def mock_pop(*args):
            print('called MainWindow.popitems with args', args)
            return ['popped', 'items']
        root = mockqtw.MockTreeItem()
        parent = None
        item1 = mockqtw.MockTreeItem()
        item2 = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           )
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getitemparentpos = mock_parentpos
        testobj.parent.root = root
        testobj.parent.master.popitems = mock_pop
        assert testobj.removeitem(item1) == ((None, 0), root, ['popped', 'items'])
        assert capsys.readouterr().out == (f"called Tree.getparentpos with arg {item1}\n"
                                           f"called MainWindow.popitems with args ({item1}, [])\n"
                                           "called TreeItem.childCount\n")

    def test_getsubtree(self, monkeypatch, capsys):
        """unittest for TreePanel.getsubtree
        """
        def mock_get(self, *args, **kwargs):
            print('called shared.getsubtree with args', args, kwargs)
            return 'subtree'
        monkeypatch.setattr(testee.shared, 'getsubtree', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getsubtree('item') == "subtree"
        assert capsys.readouterr().out == (
                "called shared.getsubtree with args ('item', None) {}\n")
        assert testobj.getsubtree('item', itemlist=['item', 'list']) == "subtree"
        assert capsys.readouterr().out == (
                "called shared.getsubtree with args ('item', ['item', 'list']) {}\n")

    def test_putsubtree(self, monkeypatch, capsys):
        """unittest for TreePanel.putsubtree
        """
        def mock_put(self, *args, **kwargs):
            print('called shared.putsubtree with args', args, kwargs)
            return 'subtree'
        monkeypatch.setattr(testee.shared, 'putsubtree', mock_put)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.putsubtree('parent', 'titel', 'key') == "subtree"
        assert capsys.readouterr().out == (
                "called shared.putsubtree with args ('parent', 'titel', 'key', None, -1) {}\n")
        assert testobj.putsubtree('parent', 'titel', 'key', subtree='xxx', pos=1) == "subtree"
        assert capsys.readouterr().out == (
                "called shared.putsubtree with args ('parent', 'titel', 'key', 'xxx', 1) {}\n")


def test_tabsize(monkeypatch, capsys):
    """unittest for qtgui.tabsize
    """
    assert testee.tabsize(1) == 4
    assert testee.tabsize(2) == 8
    assert testee.tabsize(3) == 8
    assert testee.tabsize(4) == 12
    assert testee.tabsize(5) == 16


class TestEditorPanel:
    """unittest for qtgui.EditorPanel
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.EditorPanel object

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
        testobj.parent = MockMainGui()
        testobj.parent.master = MockEditor()
        assert capsys.readouterr().out == 'called EditorPanel.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EditorPanel.__init__
        """
        def mock_charformat(self):
            "stub for reference"
        def mock_cursorposition(self):
            "stub for reference"
        def mock_tabsize(arg):
            print('called tabsize')
            return arg
        monkeypatch.setattr(testee.qtw.QTextEdit, '__init__', mockqtw.MockEditorWidget.__init__)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setAcceptRichText',
                            mockqtw.MockEditorWidget.setAcceptRichText)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setAutoFormatting',
                            mockqtw.MockEditorWidget.setAutoFormatting)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'currentCharFormatChanged',
                            mockqtw.MockEditorWidget.currentCharFormatChanged)
        monkeypatch.setattr(testee.EditorPanel, 'charformat_changed', mock_charformat)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'cursorPositionChanged',
                            mockqtw.MockEditorWidget.cursorPositionChanged)
        monkeypatch.setattr(testee.EditorPanel, 'cursorposition_changed', mock_cursorposition)
        monkeypatch.setattr(testee, 'tabsize', mock_tabsize)
        monkeypatch.setattr(testee.gui, 'QFont', mockqtw.MockFont)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'currentFont',
                            mockqtw.MockEditorWidget.currentFont)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setTabStopDistance',
                            mockqtw.MockEditorWidget.setTabStopDistance)
        testobj = testee.EditorPanel('parent')
        assert testobj.parent == 'parent'
        assert testobj.paragraph_increment == 1  # 100
        assert capsys.readouterr().out == (
                "called Editor.__init__\n"
                "called Editor.setAcceptRichText with arg `True`\n"
                "called Editor.setAutoFormatting with arg `AutoFormattingFlag.AutoAll`\n"
                f"called Signal.connect with args ({testobj.charformat_changed},)\n"
                f"called Signal.connect with args ({testobj.cursorposition_changed},)\n"
                "called Editor.currentFont\n"
                "called Font.__init__\n"
                "called Font.pointSize\n"
                "called tabsize\n"
                "called Editor.setTabStopDistance with arg fontsize\n")

    def test_canInsertFromMimeData(self, monkeypatch, capsys):
        """unittest for EditorPanel.canInsertFromMimeData
        """
        def mock_can(self, arg):
            print(f'called TreePanel.canInsertFromMimeData with arg {arg}')
            return 'can'
        monkeypatch.setattr(testee.qtw.QTextEdit, 'canInsertFromMimeData', mock_can)
        testobj = self.setup_testobj(monkeypatch, capsys)
        source = types.SimpleNamespace(hasImage=lambda *x: True)
        assert testobj.canInsertFromMimeData(source)
        assert capsys.readouterr().out == ""
        source = types.SimpleNamespace(hasImage=lambda *x: False)
        assert testobj.canInsertFromMimeData(source) == 'can'
        assert capsys.readouterr().out == (
                f"called TreePanel.canInsertFromMimeData with arg {source}\n")

    def test_insertFromMimeData(self, monkeypatch, capsys):
        """unittest for EditorPanel.insertFromMimeData
        """
        def mock_save(arg):
            print(f"called Image.save with arg '{arg}'")
        monkeypatch.setattr(testee.gui, 'QImage', mockqtw.MockImage)
        monkeypatch.setattr(testee.core, 'QUrl', mockqtw.MockUrl)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'insertFromMimeData',
                            mockqtw.MockEditorWidget.insertFromMimeData)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'textCursor', mockqtw.MockEditorWidget.textCursor)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'document', mockqtw.MockEditorWidget.document)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.opts = {'ImageCount': 1}
        testobj.parent.master.temp_imagepath = testee.shared.pathlib.Path('xxx')
        source = types.SimpleNamespace(hasImage=lambda *x: False)
        testobj.insertFromMimeData(source)
        assert capsys.readouterr().out == (
                f"called Editor.insertFromMimeData with args ({source},)\n")
        source = types.SimpleNamespace(hasImage=lambda *x: True,
                                       imageData=lambda: types.SimpleNamespace(save=mock_save))
        testobj.insertFromMimeData(source)
        assert capsys.readouterr().out == (
                "called Editor.textCursor\n"
                "called TextCursor.__init__\n"
                "called TextDocument.__init__ with args ()\n"
                "called Image.save with arg 'xxx/00002.png'\n"
                "called Url.__init__ with args ('xxx/00002.png',)\n"
                "called TextDocument.addResource with args"
                " (2, <class 'mockgui.mockqtwidgets.MockUrl'>, <class 'types.SimpleNamespace'>)\n"
                "called Cursor.insertImage with arg xxx/00002.png\n")

    def test_set_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_contents
        """
        def mock_set(data):
            print(f'called EditorPanel.setHtml with arg {data}')
        def mock_char(arg):
            print('called EditorPanel.charformat_changed')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.temp_imagepath = 'xxx'
        testobj.setHtml = mock_set
        testobj.charformat_changed = mock_char
        testobj.set_contents('img src="yyy"')
        assert testobj.oldtext == 'img src="xxx/yyy"'
        assert capsys.readouterr().out == 'called EditorPanel.setHtml with arg img src="xxx/yyy"\n'

    def test_get_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.get_contents
        """
        def mock_to_text():
            print('called EditorPanel.toPlainText')
            return 'plaintext'
        def mock_to_html():
            print('called EditorPanel.toHtml')
            return f'img src="{testobj.parent.master.temp_imagepath}/yyy"'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.temp_imagepath = 'xxx'
        testobj.parent.tree = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        testobj.parent.tree.currentItem = lambda: item
        testobj.toHtml = mock_to_html
        testobj.toPlainText = mock_to_text
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n")
        assert testobj.get_contents() == 'img src="yyy"'
        assert capsys.readouterr().out == ("called EditorPanel.toPlainText\n"
                                           "called TreeItem.setData to `plaintext` with role"
                                           f" {testee.core.Qt.ItemDataRole.UserRole} for col 0\n"
                                           "called EditorPanel.toHtml\n")

    def test_get_text_position(self, monkeypatch, capsys):
        """unittest for EditorPanel.get_text_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.textCursor = lambda: mockqtw.MockTextCursor()
        assert testobj.get_text_position() == "position"
        assert capsys.readouterr().out == ("called TextCursor.__init__\n"
                                           "called TextCursor.position\n")

    def test_set_text_position(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_text_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._text_cursor = mockqtw.MockTextCursor()
        testobj.textCursor = lambda: testobj._text_cursor
        monkeypatch.setattr(testee.EditorPanel, 'setTextCursor',
                            mockqtw.MockEditorWidget.setTextCursor)
        monkeypatch.setattr(testee.EditorPanel, 'ensureCursorVisible',
                            mockqtw.MockEditorWidget.ensureCursorVisible)
        testobj.set_text_position('pos')
        assert capsys.readouterr().out == ("called TextCursor.__init__\n"
                                           "called TextCursor.setPosition with arg pos\n"
                                           "called Editor.setTextCursor\n"
                                           "called Editor.ensureCursorVisible\n")

    def test_select_all(self, monkeypatch, capsys):
        """unittest for EditorPanel.select_all
        """
        monkeypatch.setattr(testee.EditorPanel, 'selectAll', mockqtw.MockEditorWidget.selectAll)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.select_all()
        assert capsys.readouterr().out == ("called Editor.selectAll\n")

    def test_text_bold(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_bold
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.parent.styleactiondict = {'&Bold': mockqtw.MockCheckBox()}
        assert capsys.readouterr().out == ("called CheckBox.__init__\n")
        testobj.text_bold()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.text_bold()
        assert capsys.readouterr().out == (
                "called Editor.hasFocus\n"
                "called TextCharFormat.__init__ with args ()\n"
                "called CheckBox.isChecked\n"
                f"called TextCharFormat.setFontWeight with arg {testee.gui.QFont.Weight.Normal}\n"
                "called EditorPanel.mergeCurrentCharformat\n")
        testobj.parent.styleactiondict['&Bold'].setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n")
        testobj.text_bold()
        assert capsys.readouterr().out == (
                "called Editor.hasFocus\n"
                "called TextCharFormat.__init__ with args ()\n"
                "called CheckBox.isChecked\n"
                f"called TextCharFormat.setFontWeight with arg {testee.gui.QFont.Weight.Bold}\n"
                "called EditorPanel.mergeCurrentCharformat\n")

    def test_text_italic(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_italic
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.parent.styleactiondict = {'&Italic': mockqtw.MockCheckBox()}
        assert capsys.readouterr().out == ("called CheckBox.__init__\n")
        testobj.text_italic()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.text_italic()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called TextCharFormat.__init__ with args ()\n"
                                           "called CheckBox.isChecked\n"
                                           "called TextCharFormat.setFontItalic with arg False\n"
                                           "called EditorPanel.mergeCurrentCharformat\n")
        testobj.parent.styleactiondict['&Italic'].setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n")
        testobj.text_italic()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called TextCharFormat.__init__ with args ()\n"
                                           "called CheckBox.isChecked\n"
                                           "called TextCharFormat.setFontItalic with arg True\n"
                                           "called EditorPanel.mergeCurrentCharformat\n")

    def test_text_underline(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_underline
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.parent.styleactiondict = {'&Underline': mockqtw.MockCheckBox()}
        assert capsys.readouterr().out == ("called CheckBox.__init__\n")
        testobj.text_underline()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.text_underline()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called TextCharFormat.__init__ with args ()\n"
                                           "called CheckBox.isChecked\n"
                                           "called TextCharFormat.setFontUnderline with arg False\n"
                                           "called EditorPanel.mergeCurrentCharformat\n")
        testobj.parent.styleactiondict['&Underline'].setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n")
        testobj.text_underline()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called TextCharFormat.__init__ with args ()\n"
                                           "called CheckBox.isChecked\n"
                                           "called TextCharFormat.setFontUnderline with arg True\n"
                                           "called EditorPanel.mergeCurrentCharformat\n")

    def test_text_strikethrough(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_strikethrough
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.parent.styleactiondict = {'Strike&through': mockqtw.MockCheckBox()}
        assert capsys.readouterr().out == ("called CheckBox.__init__\n")
        testobj.text_strikethrough()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.text_strikethrough()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called TextCharFormat.__init__ with args ()\n"
                                           "called CheckBox.isChecked\n"
                                           "called TextCharFormat.setFontStrikeOut with arg False\n"
                                           "called EditorPanel.mergeCurrentCharformat\n")
        testobj.parent.styleactiondict['Strike&through'].setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n")
        testobj.text_strikethrough()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called TextCharFormat.__init__ with args ()\n"
                                           "called CheckBox.isChecked\n"
                                           "called TextCharFormat.setFontStrikeOut with arg True\n"
                                           "called EditorPanel.mergeCurrentCharformat\n")

    def test_align_left(self, monkeypatch, capsys):
        """unittest for EditorPanel.align_left
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.EditorPanel, 'setAlignment',
                            mockqtw.MockEditorWidget.setAlignment)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.styleactiondict = {'Align &Left': mockqtw.MockCheckBox(),
                                          'C&enter': mockqtw.MockCheckBox(),
                                          'Align &Right': mockqtw.MockCheckBox(),
                                          '&Justify': mockqtw.MockCheckBox()}
        testobj.parent.styleactiondict['Align &Left'].setChecked(True)
        testobj.parent.styleactiondict['C&enter'].setChecked(True)
        testobj.parent.styleactiondict['Align &Right'].setChecked(True)
        testobj.parent.styleactiondict['&Justify'].setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n")
        testobj.align_left()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.align_left()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called Editor.setAlignment with arg 17\n")

    def test_align_center(self, monkeypatch, capsys):
        """unittest for EditorPanel.align_center
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.EditorPanel, 'setAlignment',
                            mockqtw.MockEditorWidget.setAlignment)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.styleactiondict = {'Align &Left': mockqtw.MockCheckBox(),
                                          'C&enter': mockqtw.MockCheckBox(),
                                          'Align &Right': mockqtw.MockCheckBox(),
                                          '&Justify': mockqtw.MockCheckBox()}
        testobj.parent.styleactiondict['Align &Left'].setChecked(True)
        testobj.parent.styleactiondict['C&enter'].setChecked(True)
        testobj.parent.styleactiondict['Align &Right'].setChecked(True)
        testobj.parent.styleactiondict['&Justify'].setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n")
        testobj.align_center()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.align_center()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called Editor.setAlignment with arg 4\n")

    def test_align_right(self, monkeypatch, capsys):
        """unittest for EditorPanel.align_right
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.EditorPanel, 'setAlignment',
                            mockqtw.MockEditorWidget.setAlignment)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.styleactiondict = {'Align &Left': mockqtw.MockCheckBox(),
                                          'C&enter': mockqtw.MockCheckBox(),
                                          'Align &Right': mockqtw.MockCheckBox(),
                                          '&Justify': mockqtw.MockCheckBox()}
        testobj.parent.styleactiondict['Align &Left'].setChecked(True)
        testobj.parent.styleactiondict['C&enter'].setChecked(True)
        testobj.parent.styleactiondict['Align &Right'].setChecked(True)
        testobj.parent.styleactiondict['&Justify'].setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n")
        testobj.align_right()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.align_right()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called Editor.setAlignment with arg 18\n")

    def test_text_justify(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_justify
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.EditorPanel, 'setAlignment',
                            mockqtw.MockEditorWidget.setAlignment)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.styleactiondict = {'Align &Left': mockqtw.MockCheckBox(),
                                          'C&enter': mockqtw.MockCheckBox(),
                                          'Align &Right': mockqtw.MockCheckBox(),
                                          '&Justify': mockqtw.MockCheckBox()}
        testobj.parent.styleactiondict['Align &Left'].setChecked(True)
        testobj.parent.styleactiondict['C&enter'].setChecked(True)
        testobj.parent.styleactiondict['Align &Right'].setChecked(True)
        testobj.parent.styleactiondict['&Justify'].setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg True\n")
        testobj.text_justify()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.text_justify()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called Editor.setAlignment with arg 8\n")

    def test_indent_more(self, monkeypatch, capsys):
        """unittest for EditorPanel.indent_more
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        # def mock_blockFormat(self):
        #     print('called TextCursor.blockFormat')
        #     return mockqtw.MockTextBlockFormat()
        # def mock_setBlockFormat(self, arg):
        #     print('called TextCursor.setBlockFormat')
        # def mock_indent(self):
        #     print("called TextBlockCursor.indent")
        #     return 1
        # def mock_setIndent(self, value):
        #     print(f"called TextBlockCursor.setIndent with arg {value}")
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.EditorPanel, 'textCursor', mockqtw.MockEditorWidget.textCursor)
        monkeypatch.setattr(testee.EditorPanel, 'setTextCursor',
                            mockqtw.MockEditorWidget.setTextCursor)
        # monkeypatch.setattr(mockqtw.MockTextCursor, 'blockFormat', mock_blockFormat)
        # monkeypatch.setattr(mockqtw.MockTextCursor, 'setBlockFormat', mock_setBlockFormat)
        # monkeypatch.setattr(mockqtw.MockTextBlockFormat, 'indent', mock_indent)
        # monkeypatch.setattr(mockqtw.MockTextBlockFormat, 'setIndent', mock_setIndent)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.paragraph_increment = 5
        testobj.indent_more()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.indent_more()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called Editor.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.blockFormat\n"
                                           "called TextBlockFormat.__init__ with args ()\n"
                                           "called TextBlockFormat.indent\n"
                                           "called TextBlockFormat.setIndent with arg"
                                           f" {1 + testobj.paragraph_increment}\n"
                                           "called TextCursor.setBlockFormat\n"
                                           "called Editor.setTextCursor\n")

    def test_indent_less(self, monkeypatch, capsys):
        """unittest for EditorPanel.indent_less
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        def mock_blockFormat(self):
            print('called TextCursor.blockFormat')
            return mockqtw.MockTextBlockFormat()
        def mock_setBlockFormat(self, arg):
            print('called TextCursor.setBlockFormat')
        def mock_indent(self):
            print("called TextBlockCursor.indent")
            return 1
        def mock_indent_2(self):
            print("called TextBlockCursor.indent")
            return 5
        def mock_setIndent(self, value):
            print(f"called TextBlockCursor.setIndent with arg {value}")
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.EditorPanel, 'textCursor', mockqtw.MockEditorWidget.textCursor)
        monkeypatch.setattr(testee.EditorPanel, 'setTextCursor',
                            mockqtw.MockEditorWidget.setTextCursor)
        monkeypatch.setattr(mockqtw.MockTextCursor, 'blockFormat', mock_blockFormat)
        monkeypatch.setattr(mockqtw.MockTextCursor, 'setBlockFormat', mock_setBlockFormat)
        monkeypatch.setattr(mockqtw.MockTextBlockFormat, 'indent', mock_indent)
        monkeypatch.setattr(mockqtw.MockTextBlockFormat, 'setIndent', mock_setIndent)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.paragraph_increment = 5
        testobj.indent_less()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.indent_less()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called Editor.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.blockFormat\n"
                                           "called TextBlockFormat.__init__ with args ()\n"
                                           "called TextBlockCursor.indent\n"
                                           "called TextCursor.setBlockFormat\n"
                                           "called Editor.setTextCursor\n")
        monkeypatch.setattr(mockqtw.MockTextBlockFormat, 'indent', mock_indent_2)
        testobj.indent_less()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called Editor.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.blockFormat\n"
                                           "called TextBlockFormat.__init__ with args ()\n"
                                           "called TextBlockCursor.indent\n"
                                           "called TextBlockCursor.setIndent with arg"
                                           f" {5 - testobj.paragraph_increment}\n"
                                           "called TextCursor.setBlockFormat\n"
                                           "called Editor.setTextCursor\n")

    def _test_increase_parspacing(self, monkeypatch, capsys):  # not implemented in testee
        """unittest for EditorPanel.increase_parspacing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.increase_parspacing() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_decrease_parspacing(self, monkeypatch, capsys):  # not implemented in testee
        """unittest for EditorPanel.decrease_parspacing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.decrease_parspacing() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_linespacing_10(self, monkeypatch, capsys):  # not implemented in testee
        """unittest for EditorPanel.set_linespacing_10
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_linespacing_10() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_linespacing_15(self, monkeypatch, capsys):  # not implemented in testee
        """unittest for EditorPanel.set_linespacing_15
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_linespacing_15() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_linespacing_20(self, monkeypatch, capsys):  # not implemented in testee
        """unittest for EditorPanel.set_linespacing_20
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_linespacing_20() == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_text_font(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_font
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        def mock_getfont(self, *args):
            print('called FontDialog.getFont with args', args)
            return mockqtw.MockFont(), True
        def mock_tabsize(arg):
            print('called tabsize')
            return arg
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        monkeypatch.setattr(testee.qtw, 'QFontDialog', mockqtw.MockFontDialog)
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        monkeypatch.setattr(testee.gui, 'QFont', mockqtw.MockFont)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'currentFont',
                            mockqtw.MockEditorWidget.currentFont)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setTabStopDistance',
                            mockqtw.MockEditorWidget.setTabStopDistance)
        monkeypatch.setattr(testee, 'tabsize', mock_tabsize)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.text_font()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n")
        testobj.hasFocus = mock_has_focus
        testobj.text_font()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called Editor.currentFont\n"
                                           "called Font.__init__\n"
                                           f"called FontDialog.getFont with args {testobj}\n")
        monkeypatch.setattr(mockqtw.MockFontDialog, 'getFont', mock_getfont)
        testobj.text_font()
        assert capsys.readouterr().out == ("called Editor.hasFocus\n"
                                           "called Editor.currentFont\n"
                                           "called Font.__init__\n"
                                           f"called FontDialog.getFont with args ({testobj},)\n"
                                           "called Font.__init__\n"
                                           "called TextCharFormat.__init__ with args ()\n"
                                           "called TextCharFormat.setFont\n"
                                           "called Font.pointSize\n"
                                           "called tabsize\n"
                                           "called Editor.setTabStopDistance with arg fontsize\n"
                                           "called EditorPanel.mergeCurrentCharformat\n")

    def test_text_family(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_family
        """
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setFocus', mockqtw.MockEditorWidget.setFocus)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.text_family('family')
        assert capsys.readouterr().out == ("called TextCharFormat.__init__ with args ()\n"
                                           "called TextCharFormat.setFontFamily with arg family\n"
                                           "called EditorPanel.mergeCurrentCharformat\n"
                                           "called Editor.setFocus\n")

    def test_enlarge_text(self, monkeypatch, capsys):
        """unittest for EditorPanel.enlarge_text
        """
        def mock_size(arg):
            print(f'called EditorPanel.text_size with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.combo_size = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.parent.fontsizes = ['10', '20', '30']
        testobj.parent.combo_size.currentText = lambda: '20'
        testobj.text_size = mock_size
        testobj.enlarge_text()
        assert capsys.readouterr().out == "called EditorPanel.text_size with arg 30\n"
        testobj.parent.combo_size.currentText = lambda: '30'
        testobj.enlarge_text()
        assert capsys.readouterr().out == ""

    def test_shrink_text(self, monkeypatch, capsys):
        """unittest for EditorPanel.shrink_text
        """
        def mock_size(arg):
            print(f'called EditorPanel.text_size with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.combo_size = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.parent.fontsizes = ['10', '20', '30']
        testobj.parent.combo_size.currentText = lambda: '20'
        testobj.text_size = mock_size
        testobj.shrink_text()
        assert capsys.readouterr().out == "called EditorPanel.text_size with arg 10\n"
        testobj.parent.combo_size.currentText = lambda: '10'
        testobj.shrink_text()
        assert capsys.readouterr().out == ("")

    def test_text_size(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_size
        """
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setFocus', mockqtw.MockEditorWidget.setFocus)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        testobj.text_size(0)
        assert capsys.readouterr().out == ""
        testobj.text_size(10)
        assert capsys.readouterr().out == ("called TextCharFormat.__init__ with args ()\n"
                                           "called TextCharFormat.setFontPointSize with arg 10.0\n"
                                           "called EditorPanel.mergeCurrentCharformat\n"
                                           "called Editor.setFocus\n")

    def test_select_text_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_color
        """
        def mock_message(*args):
            print('called show_message with args', args)
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        def mock_get(*args):
            print('called ColorDialog.getColor with args', args)
            return color1
        def mock_get_2(*args):
            print('called ColorDialog.getColor with args', args)
            return color2
        def mock_changed(arg):
            print(f'called EditorPanel.color_changed with arg {arg}')
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        def mock_icon(self, arg):
            print(f'called Icon.__init__ with arg of type {type(arg)}')
        def mock_seticon(self, arg):
            print('called Action.setIcon')
        monkeypatch.setattr(testee, 'show_message', mock_message)
        monkeypatch.setattr(testee.qtw.QColorDialog, 'getColor', mock_get)
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        monkeypatch.setattr(testee.gui.QIcon, '__init__', mock_icon)
        monkeypatch.setattr(mockqtw.MockAction, 'setIcon', mock_seticon)
        monkeypatch.setattr(testee.gui, 'QPixmap', mockqtw.MockPixmap)
        color1 = mockqtw.MockColor('1')
        color1.isValid = lambda: False
        color2 = mockqtw.MockColor('2')
        color2.isValid = lambda: True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        color0 = mockqtw.MockColor('0')
        testobj.textColor = lambda: color0
        testobj.color_changed = mock_changed
        testobj.parent.setcolor_action = mockqtw.MockAction()
        assert capsys.readouterr().out == ('called Action.__init__ with args ()\n')
        testobj.select_text_color()
        assert capsys.readouterr().out == (
                'called Editor.hasFocus\n'
                f'called show_message with args ({testobj}, "Can\'t do this outside text field")\n')
        testobj.hasFocus = mock_has_focus
        testobj.select_text_color()
        assert capsys.readouterr().out == (
                'called Editor.hasFocus\n'
                f'called ColorDialog.getColor with args ({color0!r}, {testobj})\n')
        monkeypatch.setattr(testee.qtw.QColorDialog, 'getColor', mock_get_2)
        testobj.select_text_color()
        assert testobj.parent.setcoloraction_color == color2
        assert capsys.readouterr().out == (
                'called Editor.hasFocus\n'
                f'called ColorDialog.getColor with args ({color0!r}, {testobj})\n'
                'called TextCharFormat.__init__ with args ()\n'
                "called TextCharFormat.setForeground with arg 'color 2'\n"
                "called EditorPanel.mergeCurrentCharformat\n"
                "called EditorPanel.color_changed with arg 'color 2'\n"
                "called Pixmap.__init__\n"
                "called Pixmap.fill with arg 'color 2'\n"
                "called Icon.__init__ with arg of type <class 'mockgui.mockqtwidgets.MockPixmap'>\n"
                'called Action.setIcon\n')

    def test_set_text_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_text_color
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        def mock_message(*args):
            print('called show_message with args', args)
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        monkeypatch.setattr(testee, 'show_message', mock_message)
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        color0 = mockqtw.MockColor('0')
        testobj.parent.setcoloraction_color = color0
        testobj.set_text_color()
        assert capsys.readouterr().out == (
                'called Editor.hasFocus\n'
                f'called show_message with args ({testobj}, "Can\'t do this outside text field")\n')
        testobj.hasFocus = mock_has_focus
        testobj.set_text_color()
        assert capsys.readouterr().out == (
                "called Editor.hasFocus\n"
                "called TextCharFormat.__init__ with args ()\n"
                "called TextCharFormat.setForeground with arg 'color 0'\n"
                "called EditorPanel.mergeCurrentCharformat\n")

    def test_select_background_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.background_color
        """
        def mock_message(*args):
            print('called show_message with args', args)
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        def mock_get(*args):
            print('called ColorDialog.getColor with args', args)
            return color1
        def mock_get_2(*args):
            print('called ColorDialog.getColor with args', args)
            return color2
        def mock_changed(arg):
            print(f'called EditorPanel.color_changed with arg {arg}')
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        def mock_icon(self, arg):
            print(f'called Icon.__init__ with arg of type {type(arg)}')
        def mock_seticon(self, arg):
            print('called Action.setIcon')
        monkeypatch.setattr(testee, 'show_message', mock_message)
        monkeypatch.setattr(testee.qtw.QColorDialog, 'getColor', mock_get)
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        monkeypatch.setattr(testee.gui.QIcon, '__init__', mock_icon)
        monkeypatch.setattr(mockqtw.MockAction, 'setIcon', mock_seticon)
        monkeypatch.setattr(testee.gui, 'QPixmap', mockqtw.MockPixmap)
        color1 = mockqtw.MockColor('1')
        color1.isValid = lambda: False
        color2 = mockqtw.MockColor('2')
        color2.isValid = lambda: True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        color0 = mockqtw.MockColor('0')
        testobj.textBackgroundColor = lambda: color0
        testobj.background_changed = mock_changed
        testobj.parent.setbackgroundcolor_action = mockqtw.MockAction()
        assert capsys.readouterr().out == ('called Action.__init__ with args ()\n')
        testobj.select_background_color()
        assert capsys.readouterr().out == (
                'called Editor.hasFocus\n'
                f'called show_message with args ({testobj}, "Can\'t do this outside text field")\n')
        testobj.hasFocus = mock_has_focus
        testobj.select_background_color()
        assert capsys.readouterr().out == (
                'called Editor.hasFocus\n'
                f'called ColorDialog.getColor with args ({color0!r}, {testobj})\n')
        monkeypatch.setattr(testee.qtw.QColorDialog, 'getColor', mock_get_2)
        testobj.select_background_color()
        assert testobj.parent.setbackgroundcoloraction_color == color2
        assert capsys.readouterr().out == (
                'called Editor.hasFocus\n'
                f'called ColorDialog.getColor with args ({color0!r}, {testobj})\n'
                'called TextCharFormat.__init__ with args ()\n'
                "called TextCharFormat.setBackground with arg 'color 2'\n"
                "called EditorPanel.mergeCurrentCharformat\n"
                "called EditorPanel.color_changed with arg 'color 2'\n"
                "called Pixmap.__init__\n"
                "called Pixmap.fill with arg 'color 2'\n"
                "called Icon.__init__ with arg of type <class 'mockgui.mockqtwidgets.MockPixmap'>\n"
                'called Action.setIcon\n')

    def test_set_background_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_background_color
        """
        def mock_has_focus():
            print('called Editor.hasFocus')
            return True
        def mock_message(*args):
            print('called show_message with args', args)
        def mock_merge(arg):
            print('called EditorPanel.mergeCurrentCharformat')
        monkeypatch.setattr(testee, 'show_message', mock_message)
        monkeypatch.setattr(testee.EditorPanel, 'hasFocus', mockqtw.MockEditorWidget.hasFocus)
        monkeypatch.setattr(testee.gui, 'QTextCharFormat', mockqtw.MockTextCharFormat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat = mock_merge
        color0 = mockqtw.MockColor('0')
        testobj.parent.setbackgroundcoloraction_color = color0
        testobj.set_background_color()
        assert capsys.readouterr().out == (
                'called Editor.hasFocus\n'
                f'called show_message with args ({testobj}, "Can\'t do this outside text field")\n')
        testobj.hasFocus = mock_has_focus
        testobj.set_background_color()
        assert capsys.readouterr().out == (
                "called Editor.hasFocus\n"
                "called TextCharFormat.__init__ with args ()\n"
                "called TextCharFormat.setBackground with arg 'color 0'\n"
                "called EditorPanel.mergeCurrentCharformat\n")
        assert capsys.readouterr().out == ("")

    def test_charformat_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.charformat_changed
        """
        def mock_font(arg):
            print(f"called EditorPanel.font_changed with arg '{arg}'")
        def mock_color(arg):
            print(f"called EditorPanel.color_changed with arg '{arg}'")
        def mock_background(arg):
            print(f"called EditorPanel.background_changed with arg '{arg}'")
        def mock_style(self):
            return testee.core.Qt.BrushStyle.NoBrush
        def mock_style_2(self):
            return testee.core.Qt.BrushStyle.SolidPattern
        monkeypatch.setattr(mockqtw.MockBrush, 'style', mock_style)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.font_changed = mock_font
        testobj.color_changed = mock_color
        testobj.background_changed = mock_background
        fmt = mockqtw.MockTextCharFormat()
        assert capsys.readouterr().out == 'called TextCharFormat.__init__ with args ()\n'
        testobj.charformat_changed(fmt)
        assert capsys.readouterr().out == ("called TextCharFormat.font\n"
                                           "called EditorPanel.font_changed with arg 'a font'\n"
                                           "called TextCharFormat.foreground\n"
                                           "called EditorPanel.color_changed with arg 'fg color'\n"
                                           "called TextCharFormat.background\n"
                                           "called EditorPanel.background_changed with arg"
                                           f" '{testee.core.Qt.GlobalColor.white}'\n")
        monkeypatch.setattr(mockqtw.MockBrush, 'style', mock_style_2)
        testobj.charformat_changed(fmt)
        assert capsys.readouterr().out == ("called TextCharFormat.font\n"
                                           "called EditorPanel.font_changed with arg 'a font'\n"
                                           "called TextCharFormat.foreground\n"
                                           "called EditorPanel.color_changed with arg 'fg color'\n"
                                           "called TextCharFormat.background\n"
                                           "called EditorPanel.background_changed with arg"
                                           " 'bg color'\n")

    def test_cursorposition_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.cursorposition_changed
        """
        def mock_align():
            return 'alignment'
        def mock_changed(arg):
            print(f"called EditorPanel.alignment_changed with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.alignment = mock_align
        testobj.alignment_changed = mock_changed
        testobj.cursorposition_changed()
        assert capsys.readouterr().out == (
                "called EditorPanel.alignment_changed with arg 'alignment'\n")

    def test_font_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.font_changed
        """
        monkeypatch.setattr(testee.gui, 'QFontInfo', mockqtw.MockFontInfo)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.combo_font = mockqtw.MockComboBox()
        testobj.parent.combo_size = mockqtw.MockComboBox()
        testobj.parent.styleactiondict = {'&Bold': mockqtw.MockCheckBox(),
                                          '&Italic': mockqtw.MockCheckBox(),
                                          '&Underline': mockqtw.MockCheckBox(),
                                          'Strike&through': mockqtw.MockCheckBox()}
        font = mockqtw.MockFont()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called Font.__init__\n")
        testobj.font_changed(font)
        assert capsys.readouterr().out == (f"called FontInfo.__init__ with arg {font}\n"
                                           "called Font.family\n"
                                           "called ComboBox.findText with args ('family name',)\n"
                                           "called ComboBox.setCurrentIndex with arg `1`\n"
                                           "called Font.pointSize\n"
                                           "called ComboBox.findText with args ('fontsize',)\n"
                                           "called ComboBox.setCurrentIndex with arg `1`\n"
                                           "called Font.bold\n"
                                           "called CheckBox.setChecked with arg bold\n"
                                           "called Font.italic\n"
                                           "called CheckBox.setChecked with arg italic\n"
                                           "called Font.underline\n"
                                           "called CheckBox.setChecked with arg underline\n"
                                           "called Font.strikeOut\n"
                                           "called CheckBox.setChecked with arg strikeOut\n")

    def test_color_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.color_changed
        """
        def mock_icon(self, arg):
            print(f'called Icon.__init__ with arg of type {type(arg)}')
        def mock_seticon(self, arg):
            print('called Action.setIcon')
        monkeypatch.setattr(testee.gui, 'QPixmap', mockqtw.MockPixmap)
        monkeypatch.setattr(testee.gui.QIcon, '__init__', mock_icon)
        monkeypatch.setattr(mockqtw.MockAction, 'setIcon', mock_seticon)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.styleactiondict = {"&Color...": mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.color_changed('color')
        assert capsys.readouterr().out == (
                "called Pixmap.__init__\n"
                "called Pixmap.fill with arg color\n"
                "called Icon.__init__ with arg of type <class 'mockgui.mockqtwidgets.MockPixmap'>\n"
                "called Action.setIcon\n")

    def test_background_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.background_changed
        """
        def mock_icon(self, arg):
            print(f'called Icon.__init__ with arg of type {type(arg)}')
        def mock_seticon(self, arg):
            print('called Action.setIcon')
        monkeypatch.setattr(testee.gui, 'QPixmap', mockqtw.MockPixmap)
        monkeypatch.setattr(testee.gui.QIcon, '__init__', mock_icon)
        monkeypatch.setattr(mockqtw.MockAction, 'setIcon', mock_seticon)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.styleactiondict = {"&Background...": mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.background_changed('color')
        assert capsys.readouterr().out == (
                "called Pixmap.__init__\n"
                "called Pixmap.fill with arg color\n"
                "called Icon.__init__ with arg of type <class 'mockgui.mockqtwidgets.MockPixmap'>\n"
                "called Action.setIcon\n")

    def test_alignment_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.alignment_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.styleactiondict = {'Align &Left': mockqtw.MockCheckBox(),
                                          'C&enter': mockqtw.MockCheckBox(),
                                          'Align &Right': mockqtw.MockCheckBox(),
                                          '&Justify': mockqtw.MockCheckBox()}
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n")
        align = 0
        testobj.alignment_changed(align)
        assert not testobj.parent.styleactiondict["Align &Left"].isChecked()
        assert not testobj.parent.styleactiondict["C&enter"].isChecked()
        assert not testobj.parent.styleactiondict["Align &Right"].isChecked()
        assert not testobj.parent.styleactiondict["&Justify"].isChecked()
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n")
        align = testee.core.Qt.AlignmentFlag.AlignLeft
        testobj.alignment_changed(align)
        assert testobj.parent.styleactiondict["Align &Left"].isChecked()
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.isChecked\n")
        align = testee.core.Qt.AlignmentFlag.AlignHCenter
        testobj.alignment_changed(align)
        assert testobj.parent.styleactiondict["C&enter"].isChecked()
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.isChecked\n")
        align = testee.core.Qt.AlignmentFlag.AlignRight
        testobj.alignment_changed(align)
        assert testobj.parent.styleactiondict["Align &Right"].isChecked()
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.isChecked\n")
        align = testee.core.Qt.AlignmentFlag.AlignJustify
        testobj.alignment_changed(align)
        assert testobj.parent.styleactiondict["&Justify"].isChecked()
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.isChecked\n")

    def test_mergeCurrentCharFormat(self, monkeypatch, capsys):
        """unittest for EditorPanel.mergeCurrentCharFormat
        """
        def mock_sel(self):
            print('called TextCursor.hasSelection')
            return True
        monkeypatch.setattr(testee.qtw.QTextEdit, 'mergeCurrentCharFormat',
                            mockqtw.MockEditorWidget.mergeCurrentCharFormat)
        monkeypatch.setattr(testee.qtw.QTextEdit, 'textCursor',
                            mockqtw.MockEditorWidget.textCursor)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mergeCurrentCharFormat('fmt')
        assert capsys.readouterr().out == (
                "called Editor.textCursor\n"
                "called TextCursor.__init__\n"
                "called TextCursor.hasSelection\n"
                "called TextCursor.select with arg SelectionType.WordUnderCursor\n"
                "called TextCursor.mergeCharFormat with arg fmt\n"
                "called Editor.mergeCurrentCharFormat with arg fmt\n")
        monkeypatch.setattr(mockqtw.MockTextCursor, 'hasSelection', mock_sel)
        testobj.mergeCurrentCharFormat('fmt')
        assert capsys.readouterr().out == ("called Editor.textCursor\n"
                                           "called TextCursor.__init__\n"
                                           "called TextCursor.hasSelection\n"
                                           "called TextCursor.mergeCharFormat with arg fmt\n"
                                           "called Editor.mergeCurrentCharFormat with arg fmt\n")

    def test_check_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel.check_dirty
        """
        monkeypatch.setattr(testee.qtw.QTextEdit, 'document', mockqtw.MockEditorWidget.document)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.check_dirty() == "modified"
        assert capsys.readouterr().out == ("called TextDocument.__init__ with args ()\n"
                                           "called textDocument.isModified\n")

    def test_mark_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel.mark_dirty
        """
        monkeypatch.setattr(testee.qtw.QTextEdit, 'document', mockqtw.MockEditorWidget.document)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mark_dirty('value')
        assert capsys.readouterr().out == ("called TextDocument.__init__ with args ()\n"
                                           "called TextDocument.setModified with arg value\n")

    def test_openup(self, monkeypatch, capsys):
        """unittest for EditorPanel.openup
        """
        monkeypatch.setattr(testee.qtw.QTextEdit, 'setReadOnly',
                            mockqtw.MockEditorWidget.setReadOnly)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.openup(False)
        assert capsys.readouterr().out == ("called Editor.setReadOnly with arg `True`\n")
        testobj.openup(True)
        assert capsys.readouterr().out == ("called Editor.setReadOnly with arg `False`\n")

    def test_focusInEvent(self, monkeypatch, capsys):
        """unittest for EditorPanel.focusInEvent
        """
        def mock_set():
            print('called Editor.set_window_title')
        monkeypatch.setattr(testee.qtw.QTextEdit, 'focusInEvent',
                            mockqtw.MockEditorWidget.focusInEvent)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.set_window_title = mock_set
        testobj.focusInEvent()
        assert testobj.parent.in_editor
        assert capsys.readouterr().out == ("called Editor.set_window_title\n"
                                           "called Editor.focusInEvent with args ()\n")
        testobj.focusInEvent('x', 'y')
        assert testobj.parent.in_editor
        assert capsys.readouterr().out == ("called Editor.set_window_title\n"
                                           "called Editor.focusInEvent with args ('x', 'y')\n")

    def test_focusOutEvent(self, monkeypatch, capsys):
        """unittest for EditorPanel.focusOutEvent
        """
        def mock_set():
            print('called Editor.set_window_title')
        monkeypatch.setattr(testee.qtw.QTextEdit, 'focusOutEvent',
                            mockqtw.MockEditorWidget.focusOutEvent)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.set_window_title = mock_set
        testobj.focusOutEvent()
        assert not testobj.parent.in_editor
        assert capsys.readouterr().out == ("called Editor.set_window_title\n"
                                           "called Editor.focusOutEvent with args ()\n")
        testobj.focusOutEvent('x', 'y')
        assert not testobj.parent.in_editor
        assert capsys.readouterr().out == ("called Editor.set_window_title\n"
                                           "called Editor.focusOutEvent with args ('x', 'y')\n")

    def test_search_from_start(self, monkeypatch, capsys):
        """unittest for EditorPanel.search_from_start
        """
        def mock_find(*args):
            print('called Editor.find with args', args)
            return True
        monkeypatch.setattr(testee.EditorPanel, 'moveCursor', mockqtw.MockEditorWidget.moveCursor)
        monkeypatch.setattr(testee.EditorPanel, 'find', mockqtw.MockEditorWidget.find)
        monkeypatch.setattr(testee.EditorPanel, 'ensureCursorVisible',
                            mockqtw.MockEditorWidget.ensureCursorVisible)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.srchtext = 'search'
        testobj.parent.srchflags = 'flags'
        assert not testobj.search_from_start()
        assert capsys.readouterr().out == (
                "called Editor.moveCursor with args"
                f" ({testee.gui.QTextCursor.MoveOperation.Start!r},)\n"
                "called Editor.find with args ('search', 'flags')\n")
        testobj.find = mock_find
        assert testobj.search_from_start()
        assert capsys.readouterr().out == (
                f"called Editor.moveCursor with args"
                f" ({testee.gui.QTextCursor.MoveOperation.Start!r},)\n"
                "called Editor.find with args ('search', 'flags')\n"
                "called Editor.ensureCursorVisible\n")

    def test_find_next(self, monkeypatch, capsys):
        """unittest for EditorPanel.find_next
        """
        def mock_find(what, how):
            print(f"called Editor.find with args '{what}', {how}")
            return False
        def mock_find_2(what, how):
            print(f"called Editor.find with args '{what}', {how}")
            return True
        monkeypatch.setattr(testee.EditorPanel, 'ensureCursorVisible',
                            mockqtw.MockEditorWidget.ensureCursorVisible)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.srchtext = 'search'
        testobj.parent.srchflags = (testee.gui.QTextDocument.FindFlag.FindCaseSensitively
                                    | testee.gui.QTextDocument.FindFlag.FindWholeWords)
        testobj.find = mock_find
        testobj.find_next()
        assert capsys.readouterr().out == ("called Editor.find with args 'search',"
                                           " FindFlag.FindCaseSensitively|FindWholeWords\n")
        testobj.find = mock_find_2
        testobj.find_next()
        assert capsys.readouterr().out == ("called Editor.find with args 'search',"
                                           " FindFlag.FindCaseSensitively|FindWholeWords\n"
                                           "called Editor.ensureCursorVisible\n")

    def test_find_prev(self, monkeypatch, capsys):
        """unittest for EditorPanel.find_prev
        """
        def mock_find(what, how):
            print(f"called Editor.find with args '{what}', {how}")
            return False
        def mock_find_2(what, how):
            print(f"called Editor.find with args '{what}', {how}")
            return True
        monkeypatch.setattr(testee.EditorPanel, 'ensureCursorVisible',
                            mockqtw.MockEditorWidget.ensureCursorVisible)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.srchtext = 'search'
        testobj.parent.srchflags = testee.gui.QTextDocument.FindFlag
        testobj.find = mock_find
        testobj.find_prev()
        assert capsys.readouterr().out == ("called Editor.find with args 'search',"
                                           " FindFlag.FindBackward\n")
        testobj.find = mock_find_2
        testobj.find_prev()
        assert capsys.readouterr().out == ("called Editor.find with args 'search',"
                                           " FindFlag.FindBackward\n"
                                           "called Editor.ensureCursorVisible\n")
        testobj.parent.srchflags = testee.gui.QTextDocument.FindFlag.FindWholeWords
        testobj.find_prev()
        assert capsys.readouterr().out == ("called Editor.find with args 'search',"
                                           " FindFlag.FindBackward|FindWholeWords\n"
                                           "called Editor.ensureCursorVisible\n")


class TestMainGui:
    """unittest for qtgui.MainGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.MainGui object

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
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        def mock_init(self, *args, **kwargs):
            print('called MainWindow.__init__')
        monkeypatch.setattr(testee.qtw.QApplication, '__init__',
                            mockqtw.MockApplication.__init__)
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mock_init)
        testobj = testee.MainGui('master', 'title')
        assert testobj.master == 'master'
        assert testobj.title == 'title'
        assert capsys.readouterr().out == ("called Application.__init__\n"
                                           "called MainWindow.__init__\n")

    def test_setup_screen(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.setup_screen
        """
        def mock_menubar():
            print('called MainWindow.menuBar')
            return menubar
        def mock_menu(*args):
            print('called MainGui.create_menu with args', args)
        def mock_toolbar():
            print('called MainGui.create_styletoolbar')
        def mock_getmenu():
            print('called MainGui.get_menu_data')
            return 'menudata'
        def mock_icon(self, arg):
            print(f'called Icon.__init__ with arg of type {type(arg)}')
        def mock_seticon(self, data):
            print('called Action.setIcon')
        # monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.gui.QIcon, '__init__', mock_icon)
        monkeypatch.setattr(testee.qtw, 'QSystemTrayIcon', mockqtw.MockSysTrayIcon)
        monkeypatch.setattr(testee.qtw, 'QSplitter', mockqtw.MockSplitter)
        monkeypatch.setattr(testee.gui, 'QPixmap', mockqtw.MockPixmap)
        monkeypatch.setattr(testee, 'UndoRedoStack', MockStack)
        monkeypatch.setattr(testee, 'TreePanel', MockTree)
        monkeypatch.setattr(testee, 'EditorPanel', MockEditor)
        monkeypatch.setattr(testee.gui.QTextDocument, 'FindFlag', 'searchflags')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockqtw.MockApplication()
        testobj.title = 'title'
        monkeypatch.setattr(testee.qtw.QMainWindow, 'move', mockqtw.MockMainWindow.move)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'statusBar', mockqtw.MockMainWindow.statusBar)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                            mockqtw.MockMainWindow.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget',
                            mockqtw.MockMainWindow.setCentralWidget)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'move', mockqtw.MockMainWindow.move)
        testobj.create_menu = mock_menu
        testobj.create_stylestoolbar = mock_toolbar
        testobj.setcoloraction_color = mockqtw.MockColor(1)
        monkeypatch.setattr(mockqtw.MockAction, 'setIcon', mock_seticon)
        testobj.setcolor_action = mockqtw.MockAction()
        testobj.setbackgroundcoloraction_color = mockqtw.MockColor(2)
        testobj.setbackgroundcolor_action = mockqtw.MockAction()
        testobj.revive = lambda *x: 'dummy callback'
        menubar = mockqtw.MockMenuBar()
        testobj.menuBar = mock_menubar
        testobj.master = MockMainWindow()
        testobj.master.opts = {'ScreenSize': (1, 2)}
        testobj.master.get_menu_data = mock_getmenu

        # breakpoint()
        testobj.setup_screen()
        assert isinstance(testobj.nt_icon, testee.gui.QIcon)
        assert isinstance(testobj.tray_icon, testee.qtw.QSystemTrayIcon)
        assert isinstance(testobj.statusbar, mockqtw.MockStatusBar)
        assert isinstance(testobj.splitter, testee.qtw.QSplitter)
        assert isinstance(testobj.tree, testee.TreePanel)
        assert isinstance(testobj.editor, testee.EditorPanel)
        assert testobj.undo_stack
        assert testobj.menulist == []
        assert testobj.mainactiondict == {}
        assert testobj.styleactiondict == {}
        assert testobj.editor.new_content
        assert not testobj.menu_disabled
        assert testobj.srchtext == ''
        assert testobj.srchtype == 0
        assert testobj.srchflags == 'searchflags'
        assert not testobj.srchlist
        assert not testobj.srchwrap
        assert capsys.readouterr().out == expected_output['maingui'].format(testobj=testobj,
                                                                            here=testee.os.getcwd(),
                                                                            menubar=menubar)

    def test_create_menu(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.create_menu
        """
        def mock_add(arg):
            print(f'called MainGui.addToolBar with arg {arg}')
            return toolbar
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.core, 'QSize', mockqtw.MockSize)
        monkeypatch.setattr(testee.gui, 'QFont', mockqtw.MockFont)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menulist = []
        testobj.mainactiondict = {}
        testobj.styleactiondict = {}
        toolbar = mockqtw.MockToolBar()
        assert capsys.readouterr().out == "called ToolBar.__init__\n"
        testobj.addToolBar = mock_add
        menubar = mockqtw.MockMenuBar()
        assert capsys.readouterr().out == "called MenuBar.__init__\n"
        testobj.create_menu(menubar, [])
        assert capsys.readouterr().out == ("")
        callbacks = [lambda: x for x in range(11)]
        menudata = [('aaa', [('aaaa', callbacks[0], '', 'aaa.ico', ''),
                             ('exit', callbacks[1], 'Ctrl+X,Esc', 'exit.ico', '')]),
                    ('xxx', [('LinE sPacINg', '', '', '', ''),
                             ('pARAgraph sPAcinG', '', '', '', '')]),
                    ('yyy', [('B', callbacks[2], '', '', 'CheckB'),
                             ('I', callbacks[3], '', '', 'CheckI'),
                             ('U', callbacks[4], '', '', 'CheckU'),
                             ('S', callbacks[5], '', '', 'CheckS'),
                             (),
                             (),
                             ('X', callbacks[6], '', '', 'Check'),
                             ()]),
                    ('zzz', [('&Undo', callbacks[7], 'Ctrl+Z', '', 'undo'),
                             ('&Redo', callbacks[8], 'Ctrl+Y', '', 'redo'),
                             ('', callbacks[0], '', '', 'xxx')]),
                    ('bbb', [('bbbb', callbacks[9], '', '', '')]),
                    ('ccc', [('cccc', callbacks[10], '', '', '')])]
        # breakpoint()
        testobj.create_menu(menubar, menudata)
        assert capsys.readouterr().out == expected_output['menu'].format(testobj=testobj,
                                                                         testee=testee,
                                                                         callbacks=callbacks)
        assert len(testobj.menulist) == 6
        assert isinstance(testobj.viewmenu, mockqtw.MockMenu)
        assert isinstance(testobj.notemenu, mockqtw.MockMenu)
        assert isinstance(testobj.treemenu, mockqtw.MockMenu)
        assert testobj.menulist[1] == testobj.notemenu
        assert testobj.menulist[2] == testobj.viewmenu
        assert testobj.menulist[3] == testobj.treemenu
        assert len(testobj.menulist[0].actions()) == 2
        assert len(testobj.menulist[1].actions()) == 0
        assert len(testobj.menulist[2].actions()) == 7
        assert len(testobj.menulist[3].actions()) == 2
        assert len(testobj.menulist[4].actions()) == 1
        assert len(testobj.menulist[5].actions()) == 1
        assert isinstance(testobj.undo_item, testee.gui.QAction)
        assert testobj.undo_item.text() == '&Undo'
        assert capsys.readouterr().out == 'called Action.text\n'
        assert testobj.undo_item.shortcuts() == ['Ctrl+Z']
        assert capsys.readouterr().out == 'called Action.shortcuts\n'
        assert isinstance(testobj.redo_item, testee.gui.QAction)
        assert testobj.redo_item.text() == '&Redo'
        assert capsys.readouterr().out == 'called Action.text\n'
        assert testobj.redo_item.shortcuts() == ['Ctrl+Y']
        assert capsys.readouterr().out == 'called Action.shortcuts\n'
        assert isinstance(testobj.quit_action, testee.gui.QAction)
        assert testobj.quit_action.text() == 'exit'
        assert capsys.readouterr().out == 'called Action.text\n'
        assert testobj.quit_action.shortcuts() == ['Ctrl+X', 'Esc']
        assert capsys.readouterr().out == 'called Action.shortcuts\n'
        # assert testobj.mainactiondict == {'aaa': callback0, 'exit': callback99}
        assert len(testobj.mainactiondict) == 2
        # assert testobj.styleactiondict == {'ccc': callback7}
        assert len(testobj.styleactiondict) == 1

    def test_disable_menu(self, monkeypatch, capsys):
        """unittest for MainGui.disable_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menulist = [mockqtw.MockMenu(), mockqtw.MockMenu(), mockqtw.MockMenu()]
        testobj.mainactiondict = {'&Open': mockqtw.MockAction(), '&Init': mockqtw.MockAction,
                                  'Anything': mockqtw.MockAction(), 'e&Xit': mockqtw.MockAction()}
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n")
        testobj.disable_menu()
        assert testobj.menu_disabled
        assert capsys.readouterr().out == ("called Menu.setDisabled with arg 'True'\n"
                                           "called Menu.setDisabled with arg 'True'\n"
                                           "called Action.setDisabled with arg `True`\n")
        testobj.disable_menu(False)
        assert not testobj.menu_disabled
        assert capsys.readouterr().out == ("called Menu.setDisabled with arg 'False'\n"
                                           "called Menu.setDisabled with arg 'False'\n"
                                           "called Action.setDisabled with arg `False`\n")

    def test_create_stylestoolbar(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.create_stylestoolbar
        """
        def mock_add(arg):
            print(f'called MainGui.addToolBar with arg {arg}')
            return toolbar
        def mock_icon(self, arg):
            print(f'called Icon.__init__ with arg of type {type(arg)}')
        monkeypatch.setattr(testee.gui, 'QFontDatabase',
                            types.SimpleNamespace(standardSizes=lambda: [10, 12, 20]))
        monkeypatch.setattr(mockqtw.MockFontComboBox, 'currentTextChanged',
                            {str: mockqtw.MockSignal()})
        monkeypatch.setattr(testee.qtw, 'QFontComboBox', mockqtw.MockFontComboBox)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.gui, 'QPixmap', mockqtw.MockPixmap)
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(mockqtw.MockIcon, '__init__', mock_icon)
        toolbar = mockqtw.MockToolBar()
        assert capsys.readouterr().out == ("called Signal.__init__\n"
                                           "called ToolBar.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.styleactiondict = {}
        testobj.addToolBar = mock_add
        testobj.editor = MockEditor()
        testobj.editor.text_family = lambda: 'family'
        testobj.editor.text_size = lambda: 'size'
        testobj.editor.font = lambda: mockqtw.MockFont()
        testobj.editor.select_text_color = lambda: 'text color'
        testobj.editor.set_text_color = lambda: 'text color'
        testobj.editor.select_background_color = lambda: 'bg color'
        testobj.editor.set_background_color = lambda: 'bg color'
        testobj.create_stylestoolbar()
        assert isinstance(testobj.combo_font, testee.qtw.QFontComboBox)
        assert isinstance(testobj.combo_size, testee.qtw.QComboBox)
        assert testobj.setcoloraction_color == testee.core.Qt.GlobalColor.black
        assert isinstance(testobj.setcolor_action, testee.gui.QAction)
        assert testobj.setbackgroundcoloraction_color == testee.core.Qt.GlobalColor.white
        assert isinstance(testobj.setbackgroundcolor_action, testee.gui.QAction)
        assert list(testobj.styleactiondict) == ['&Color...', '&Background...']
        for item in testobj.styleactiondict.values():
            assert isinstance(item, testee.gui.QAction)
        assert capsys.readouterr().out == expected_output['toolbar'].format(testobj=testobj)

    def test_show_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.show_statusmessage
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.statusbar = mockqtw.MockStatusBar()
        assert capsys.readouterr().out == "called StatusBar.__init__ with args ()\n"
        testobj.show_statusmessage('text')
        assert capsys.readouterr().out == ("called StatusBar.showMessage with arg `text`\n")

    def test_set_version(self, monkeypatch, capsys):
        """unittest for MainGui.set_version
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockMainWindow()
        testobj.master.opts = {}
        testobj.set_version()
        assert testobj.master.opts["Version"] == "Qt"

    def test_set_window_dimensions(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_dimensions
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_window_dimensions('x', 'y')
        assert capsys.readouterr().out == ("called MainWindow.resize with args ('x', 'y')\n")

    def test_get_screensize(self, monkeypatch, capsys):
        """unittest for MainGui.get_screensize
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'width', mockqtw.MockMainWindow.width)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'height', mockqtw.MockMainWindow.height)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_screensize() == ('width', 'height')
        assert capsys.readouterr().out == ("called MainWindow.width with args ()\n"
                                           "called MainWindow.height with args ()\n")

    def test_set_windowtitle(self, monkeypatch, capsys):
        """unittest for MainGui.set_windowtitle
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                            mockqtw.MockMainWindow.setWindowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_windowtitle('title')
        assert capsys.readouterr().out == ("called MainWindow.setWindowTitle with arg `title`\n")

    def test_set_window_split(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_split
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.splitter = mockqtw.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__\n"
        testobj.set_window_split('pos')
        assert capsys.readouterr().out == "called Splitter.setSizes with args ('pos',)\n"

    def test_get_splitterpos(self, monkeypatch, capsys):
        """unittest for MainGui.get_splitterpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.splitter = mockqtw.MockSplitter()
        assert capsys.readouterr().out == "called Splitter.__init__\n"
        assert testobj.get_splitterpos() == ('left this wide', 'right that wide')

    def test_init_app(self, monkeypatch, capsys):
        """unittest for MainGui.init_app
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack(testobj)
        assert capsys.readouterr().out == f"called UndoStack.__init__ with args ({testobj},)\n"
        testobj.init_app()
        assert capsys.readouterr().out == "called UndoRedoStack.clear\n"

    def test_set_focus_to_tree(self, monkeypatch, capsys):
        """unittest for MainGui.set_focus_to_tree
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.set_focus_to_tree()
        assert not testobj.in_editor
        assert capsys.readouterr().out == "called Tree.setFocus\n"

    def test_set_focus_to_editor(self, monkeypatch, capsys):
        """unittest for MainGui.set_focus_to_editor
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockMainWindow()
        testobj.master.activeitem = 'active item'
        testobj.master.text_positions = {'itemkey': 99}
        testobj.tree = MockTree()
        testobj.editor = MockEditor()
        assert capsys.readouterr().out == "called TreePanel.__init__ with args ()\n"
        testobj.set_focus_to_editor()
        assert testobj.in_editor
        assert capsys.readouterr().out == ("called Editor.setFocus\n"
                                           "called TreePanel.getitemkey with arg 'active item'\n"
                                           "called Editor.set_text_position with arg 99\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for MainGui.go
        """
        def mock_set():
            print('called MainGui.set_focus_to_editor')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockqtw.MockApplication()
        assert capsys.readouterr().out == "called Application.__init__\n"
        monkeypatch.setattr(testee.qtw.QMainWindow, 'show', mockqtw.MockMainWindow.show)
        testobj.set_focus_to_editor = mock_set
        with pytest.raises(SystemExit) as e:
            testobj.go()
        assert capsys.readouterr().out == ("called MainWindow.show\n"
                                           "called MainGui.set_focus_to_editor\n"
                                           "called Application.exec\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for MainGui.close
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'close', mockqtw.MockMainWindow.close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close()
        assert capsys.readouterr().out == ("called MainWindow.close\n")

    def test_closeEvent(self, monkeypatch, capsys):
        """unittest for MainGui.closeEvent
        """
        def mock_cleanup():
            print('called MainWindow.cleanup_files')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockMainWindow()
        testobj.master.cleanup_files = mock_cleanup
        event = mockqtw.MockEvent()
        testobj.master.handle_save_needed = lambda: False
        testobj.closeEvent(event)
        assert capsys.readouterr().out == ("called event.ignore\n")
        testobj.master.handle_save_needed = lambda: True
        testobj.closeEvent(event)
        assert capsys.readouterr().out == ("called MainWindow.cleanup_files\n"
                                           "called event.accept\n")

    def test_hide_me(self, monkeypatch, capsys):
        """unittest for MainGui.hide_me
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'hide', mockqtw.MockMainWindow.hide)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tray_icon = mockqtw.MockSysTrayIcon()
        assert capsys.readouterr().out == "called TrayIcon.__init__\n"
        testobj.hide_me()
        assert capsys.readouterr().out == ("called TrayIcon.show\n"
                                           "called MainWindow.hide\n")

    def test_revive(self, monkeypatch, capsys):
        """unittest for MainGui.revive
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'show', mockqtw.MockMainWindow.show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tray_icon = mockqtw.MockSysTrayIcon()
        assert capsys.readouterr().out == "called TrayIcon.__init__\n"
        testobj.revive()
        assert capsys.readouterr().out == ("called MainWindow.show\n"
                                           "called TrayIcon.hide\n")
        testobj.revive(testee.qtw.QSystemTrayIcon.ActivationReason.Unknown)
        assert capsys.readouterr().out == (
                "called TrayIcon.showMessage with args ('DocTree', 'Click to revive DocTree')\n")
        testobj.revive(testee.qtw.QSystemTrayIcon.ActivationReason.Context)
        assert capsys.readouterr().out == ""

    def test_expand_root(self, monkeypatch, capsys):
        """unittest for MainGui.expand_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.expand_root()
        assert capsys.readouterr().out == "called TreeItem.setExpanded with arg `True`\n"

    def test_start_add(self, monkeypatch, capsys):
        """unittest for MainGui.start_add
        """
        class MockAdd:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called AddCommand.__init__ with args', args, kwargs)
        monkeypatch.setattr(testee, 'AddCommand', MockAdd)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack(testobj)
        assert capsys.readouterr().out == f"called UndoStack.__init__ with args ({testobj},)\n"
        testobj.start_add()
        assert capsys.readouterr().out == (
                f"called AddCommand.__init__ with args ({testobj}, None, True, '', None) {{}}\n"
                "called UndoRedoStack.push\n")
        testobj.start_add(root='root', under=False, new_title='xxx', extra_titles=[])
        assert capsys.readouterr().out == (
                f"called AddCommand.__init__ with args ({testobj}, 'root', False, 'xxx', []) {{}}\n"
                "called UndoRedoStack.push\n")

    def test_set_next_item(self, monkeypatch, capsys):
        """unittest for MainGui.set_next_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockEditor()
        testobj.master.activeitem = mockqtw.MockTreeItem()
        child = mockqtw.MockTreeItem()
        testobj.master.activeitem.addChild(child)
        testobj.tree = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called Tree.__init__\n")
        assert testobj.set_next_item(any_level=True)
        assert capsys.readouterr().out == ("called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 0\n"
                                           f"called Tree.setCurrentItem with arg `{child}`\n")

        testobj.master.activeitem._parent = None
        assert not testobj.set_next_item()
        assert capsys.readouterr().out == "called TreeItem.parent\n"

        parent = mockqtw.MockTreeItem()
        parent.addChild(testobj.master.activeitem)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n")
        assert not testobj.set_next_item()
        # deze gaat de any_level branch in maar gaat niet dieper omdat er geen grandparent is.
        # en dat stuk moet misschien anders, zie ticket #1018
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.indexOfChild\n"
                                           "called TreeItem.childCount\n")

        # assert testobj.set_next_item(any_level=True)
        # assert capsys.readouterr().out == ("")

    def _test_set_prev_item(self, monkeypatch, capsys):
        """unittest for MainGui.set_prev_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_prev_item() == "expected_result"
        assert capsys.readouterr().out == ("")
        assert testobj.set_prev_item(any_level=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_start_copy(self, monkeypatch, capsys):
        """unittest for MainGui.start_copy
        """
        class MockCopy:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called CopyCommand.__init__ with args', args, kwargs)
        monkeypatch.setattr(testee, 'CopyCommand', MockCopy)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack(testobj)
        assert capsys.readouterr().out == f"called UndoStack.__init__ with args ({testobj},)\n"
        testobj.start_copy()
        assert capsys.readouterr().out == (
                f"called CopyCommand.__init__ with args ({testobj}, False, True, None) {{}}\n"
                "called UndoRedoStack.push\n")
        testobj.start_copy(True, False, 'current')
        assert capsys.readouterr().out == (
                f"called CopyCommand.__init__ with args ({testobj}, True, False, 'current') {{}}\n"
                "called UndoRedoStack.push\n")

    def test_start_paste(self, monkeypatch, capsys):
        """unittest for MainGui.start_paste
        """
        class MockPaste:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called PasteCommand.__init__ with args', args, kwargs)
        monkeypatch.setattr(testee, 'PasteCommand', MockPaste)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack(testobj)
        assert capsys.readouterr().out == f"called UndoStack.__init__ with args ({testobj},)\n"
        testobj.start_paste()
        assert capsys.readouterr().out == (
                f"called PasteCommand.__init__ with args ({testobj}, True, False, None) {{}}\n"
                "called UndoRedoStack.push\n")
        testobj.start_paste(False, True, 'dest')
        assert capsys.readouterr().out == (
                f"called PasteCommand.__init__ with args ({testobj}, False, True, 'dest') {{}}\n"
                "called UndoRedoStack.push\n")

    def test_reorder_items(self, monkeypatch, capsys):
        """unittest for MainGui.reorder_items
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        root = mockqtw.MockTreeItem()
        root.addChild(mockqtw.MockTreeItem('xxx'))
        root.addChild(mockqtw.MockTreeItem('yyy'))
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ('xxx',)\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.__init__ with args ('yyy',)\n"
                                           "called TreeItem.addChild\n")
        testobj.reorder_items(root)
        assert capsys.readouterr().out == (
                "called TreeItem.sortChildren with args"
                f" (0, {testee.core.Qt.SortOrder.AscendingOrder!r})\n")
        testobj.reorder_items(root, recursive=True)
        assert capsys.readouterr().out == (
                "called TreeItem.sortChildren with args"
                f" (0, {testee.core.Qt.SortOrder.AscendingOrder!r})\n"
                "called TreeItem.childCount\n"
                "called TreeItem.child with arg 0\n"
                "called TreeItem.sortChildren with args"
                f" (0, {testee.core.Qt.SortOrder.AscendingOrder!r})\n"
                "called TreeItem.childCount\n"
                "called TreeItem.child with arg 1\n"
                "called TreeItem.sortChildren with args"
                f" (0, {testee.core.Qt.SortOrder.AscendingOrder!r})\n"
                "called TreeItem.childCount\n")

    def test_rebuild_root(self, monkeypatch, capsys):
        """unittest for MainGui.rebuild_root
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        testobj.master = MockEditor()
        testobj.master.opts = {'RootTitle': 'title', 'RootData': 'data'}
        # testobj.root = mockqtw.MockTreeItem()
        # assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        assert testobj.rebuild_root() == testobj.root
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called Tree.takeTopLevelItem with arg `0`\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with arg `title` for col 0\n"
                                           "called TreeItem.setText with arg `data` for col 1\n"
                                           "called Tree.addTopLevelItem\n")

    def setup_viewmenu(self, capsys):
        """define a menu with more than 8 options to be used in the next cuople of tests
        """
        viewmenu = mockqtw.MockMenu()
        viewmenu.addAction('xx1')
        viewmenu.addAction('xx2')
        viewmenu.addAction('xx3')
        viewmenu.addAction('xx4')
        viewmenu.addAction('xx5')
        viewmenu.addAction('xx6')
        viewmenu.addAction('xx7')
        viewmenu.addAction('xx8')
        action9 = viewmenu.addAction('&1 xx9')
        action0 = viewmenu.addAction('&2 x10')
        assert capsys.readouterr().out == (
                "called Menu.__init__ with args ()\n"
                "called Menu.addAction with args `xx1` None\n"
                "called Action.__init__ with args ('xx1', None)\n"
                "called Menu.addAction with args `xx2` None\n"
                "called Action.__init__ with args ('xx2', None)\n"
                "called Menu.addAction with args `xx3` None\n"
                "called Action.__init__ with args ('xx3', None)\n"
                "called Menu.addAction with args `xx4` None\n"
                "called Action.__init__ with args ('xx4', None)\n"
                "called Menu.addAction with args `xx5` None\n"
                "called Action.__init__ with args ('xx5', None)\n"
                "called Menu.addAction with args `xx6` None\n"
                "called Action.__init__ with args ('xx6', None)\n"
                "called Menu.addAction with args `xx7` None\n"
                "called Action.__init__ with args ('xx7', None)\n"
                "called Menu.addAction with args `xx8` None\n"
                "called Action.__init__ with args ('xx8', None)\n"
                "called Menu.addAction with args `&1 xx9` None\n"
                "called Action.__init__ with args ('&1 xx9', None)\n"
                "called Menu.addAction with args `&2 x10` None\n"
                "called Action.__init__ with args ('&2 x10', None)\n")
        return viewmenu, action9, action0

    def test_clear_viewmenu(self, monkeypatch, capsys):
        """unittest for MainGui.clear_viewmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        testobj.clear_viewmenu()
        assert len(list(testobj.viewmenu.actions())) == 8
        assert capsys.readouterr().out == (f"called Menu.removeaction with arg {action9}\n"
                                           f"called Menu.removeaction with arg {action0}\n")

    def test_add_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.add_viewmenu_option
        """
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = MockMainWindow()
        testobj.master.select_view = lambda: 'dummy'
        testobj.viewmenu = mockqtw.MockMenu()
        result = testobj.add_viewmenu_option('optiontext')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                "called Menu.__init__ with args ()\n"
                f"called Action.__init__ with args ('optiontext', {testobj})\n"
                f"called Signal.connect with args ({testobj.master.select_view},)\n"
                "called Menu.addAction\n")

    def test_check_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.check_viewmenu_option
        """
        def mock_sender():
            print('called MainWindow.sender')
            return action0
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        action = mockqtw.MockAction()
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        assert testobj.check_viewmenu_option(action) == ""
        assert capsys.readouterr().out == "called Action.setChecked with arg `True`\n"

        action.setChecked(False)
        testobj.viewmenu.addAction(action)
        testobj.sender = mock_sender
        action9.setChecked(True)
        assert capsys.readouterr().out == ("called Action.setChecked with arg `False`\n"
                                           "called Menu.addAction\n"
                                           "called Action.setChecked with arg `True`\n")
        assert testobj.check_viewmenu_option() == "&2 x10"
        assert capsys.readouterr().out == ("called MainWindow.sender\n"
                                           "called Action.isChecked\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.text\n"
                                           "called Action.setChecked with arg `True`\n"
                                           "called Action.isChecked\n")

    def test_uncheck_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.uncheck_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        testobj.master = MockEditor()
        testobj.master.opts = {'ActiveView': 1}
        testobj.uncheck_viewmenu_option()
        assert capsys.readouterr().out == ("called Action.setChecked with arg `False`\n")
        # alleen: welke wordt er nu precies unchecked?

    def test_rename_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.rename_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        testobj.master = MockEditor()
        testobj.master.opts = {'ActiveView': 1}
        testobj.rename_viewmenu_option('newname')
        assert capsys.readouterr().out == ("called Action.text\n"
                                           "called Action.setText with arg `&1 newname`\n")

    def test_check_next_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.check_next_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        action9.setChecked(True)
        assert capsys.readouterr().out == "called Action.setChecked with arg `True`\n"
        testobj.check_next_viewmenu_option()
        assert capsys.readouterr().out == ("called Action.isChecked\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.isChecked\n"
                                           "called Action.setChecked with arg `True`\n")
        assert not action9.isChecked()
        assert action0.isChecked()

    def test_check_next_viewmenu_option_2(self, monkeypatch, capsys):
        """unittest for MainGui.check_next_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        action0.setChecked(True)
        assert capsys.readouterr().out == "called Action.setChecked with arg `True`\n"
        testobj.check_next_viewmenu_option()
        assert capsys.readouterr().out == ("called Action.isChecked\n"
                                           "called Action.isChecked\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `True`\n")
        assert not action0.isChecked()
        assert action9.isChecked()

    def test_check_prev_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.check_next_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        action9.setChecked(True)
        assert capsys.readouterr().out == "called Action.setChecked with arg `True`\n"
        testobj.check_next_viewmenu_option(prev=True)
        assert capsys.readouterr().out == ("called Action.isChecked\n"
                                           "called Action.isChecked\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `True`\n")
        assert not action9.isChecked()
        assert action0.isChecked()

    def test_check_prev_viewmenu_option_2(self, monkeypatch, capsys):
        """unittest for MainGui.check_next_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        action9.setChecked(True)
        assert capsys.readouterr().out == "called Action.setChecked with arg `True`\n"
        testobj.check_next_viewmenu_option(prev=True)
        assert capsys.readouterr().out == ("called Action.isChecked\n"
                                           "called Action.isChecked\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `True`\n")
        assert not action9.isChecked()
        assert action0.isChecked()

    def test_remove_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.remove_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        testobj.master = MockEditor()
        testobj.master.opts = {'ActiveView': 1}
        assert testobj.remove_viewmenu_option('xx9') == action0
        assert capsys.readouterr().out == ("called Action.text\n"
                                           f"called Menu.removeaction with arg {action9}\n"
                                           "called Action.text\n"
                                           "called Action.setText with arg `&1 x10`\n")

    def test_remove_viewmenu_option_2(self, monkeypatch, capsys):
        """unittest for MainGui.remove_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        testobj.master = MockEditor()
        testobj.master.opts = {'ActiveView': 2}
        assert testobj.remove_viewmenu_option('x10') == action9
        assert capsys.readouterr().out == ("called Action.text\n"
                                           "called Action.text\n"
                                           f"called Menu.removeaction with arg {action0}\n")

    def test_remove_viewmenu_option_3(self, monkeypatch, capsys):
        """unittest for MainGui.remove_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.viewmenu, action9, action0 = self.setup_viewmenu(capsys)
        testobj.viewmenu.addAction('&3 xxx')
        assert capsys.readouterr().out == ("called Menu.addAction with args `&3 xxx` None\n"
                                           "called Action.__init__ with args ('&3 xxx', None)\n")
        testobj.master = MockEditor()
        testobj.master.opts = {'ActiveView': 2}
        assert testobj.remove_viewmenu_option('xx9') == action0
        assert capsys.readouterr().out == ("called Action.text\n"
                                           f"called Menu.removeaction with arg {action9}\n"
                                           "called Action.text\n"
                                           "called Action.setText with arg `&1 x10`\n"
                                           "called Action.text\n"
                                           "called Action.setText with arg `&2 xxx`\n")

    def test_tree_undo(self, monkeypatch, capsys):
        """unittest for MainGui.tree_undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack(testobj)
        assert capsys.readouterr().out == f"called UndoStack.__init__ with args ({testobj},)\n"
        testobj.tree_undo()
        assert capsys.readouterr().out == "called UndoRedoStack.undo\n"

    def test_tree_redo(self, monkeypatch, capsys):
        """unittest for MainGui.tree_redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack(testobj)
        assert capsys.readouterr().out == f"called UndoStack.__init__ with args ({testobj},)\n"
        testobj.tree_redo()
        assert capsys.readouterr().out == "called UndoRedoStack.redo\n"

    def test_find_needle(self, monkeypatch, capsys):
        """unittest for MainGui.find_needle
        """
        def mock_find(self, text, options):
            print(f"called TextDocument.find with args '{text}' '{options}'")
            return types.SimpleNamespace(isNull=lambda: True)
        def mock_find2(self, text, options):
            print(f"called TextDocument.find with args '{text}' '{options}'")
            return types.SimpleNamespace(isNull=lambda: False)
        monkeypatch.setattr(mockqtw.MockTextDocument, 'find', mock_find)
        monkeypatch.setattr(testee.gui, 'QTextDocument', mockqtw.MockTextDocument)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.srchtext = 'needle'
        testobj.srchflags = 'searchflags'
        assert not testobj.find_needle('haystack')
        assert capsys.readouterr().out == (
                "called TextDocument.__init__ with args ()\n"
                "called TextDocument.setPlainText with arg 'haystack'\n"
                "called TextDocument.find with args 'needle' 'searchflags'\n")
        monkeypatch.setattr(mockqtw.MockTextDocument, 'find', mock_find2)
        assert testobj.find_needle('haystack')
        assert capsys.readouterr().out == (
                "called TextDocument.__init__ with args ()\n"
                "called TextDocument.setPlainText with arg 'haystack'\n"
                "called TextDocument.find with args 'needle' 'searchflags'\n")

    def test_goto_searchresult(self, monkeypatch, capsys):
        """unittest for MainGui.goto_searchresult
        """
        def mock_find(text, options):
            print(f"called Editor.find with args '{text}' '{options}'")
            return False
        def mock_find2(text, options):
            print(f"called Editor.find with args '{text}' '{options}'")
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        testobj.root = mockqtw.MockTreeItem('root')
        item = mockqtw.MockTreeItem('level1')
        testobj.root.addChild(item)
        item2 = mockqtw.MockTreeItem('level2')
        item.addChild(item2)
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ('root',)\n"
                                           "called TreeItem.__init__ with args ('level1',)\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.__init__ with args ('level2',)\n"
                                           "called TreeItem.addChild\n")
        testobj.editor = MockEditor()
        testobj.editor.find = mock_find
        testobj.srchtext = 'needle'
        testobj.srchflags = 'searchflags'
        testobj.srchtype = 1
        testobj.goto_searchresult([0, 0])
        assert capsys.readouterr().out == ("called TreeItem.child with arg 0\n"
                                           "called TreeItem.child with arg 0\n"
                                           f"called Tree.setCurrentItem with arg `{item2}`\n")
        testobj.srchtype = 2
        testobj.goto_searchresult([0, 0])
        assert capsys.readouterr().out == ("called TreeItem.child with arg 0\n"
                                           "called TreeItem.child with arg 0\n"
                                           f"called Tree.setCurrentItem with arg `{item2}`\n"
                                           "called Editor.find with args 'needle' 'searchflags'\n")
        testobj.editor.find = mock_find2
        testobj.goto_searchresult([0, 0])
        assert capsys.readouterr().out == ("called TreeItem.child with arg 0\n"
                                           "called TreeItem.child with arg 0\n"
                                           f"called Tree.setCurrentItem with arg `{item2}`\n"
                                           "called Editor.find with args 'needle' 'searchflags'\n"
                                           "called Editor.ensureCursorVisible\n")

    def test_add_escape_action(self, monkeypatch, capsys):
        """unittest for MainGui.add_escape_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.quit_shortcuts = ['Ctrl-Q', 'Esc']
        testobj.quit_action = mockqtw.MockAction()
        testobj.quit_action.setShortcuts(['x', 'y'])
        assert capsys.readouterr().out == ("called Action.__init__ with args ()\n"
                                           "called Action.setShortcuts with arg `['x', 'y']`\n")
        testobj.add_escape_action()
        assert capsys.readouterr().out == ("called Action.shortcuts\n")
        testobj.quit_action.setShortcut('x')
        assert capsys.readouterr().out == ("called Action.setShortcut with arg `x`\n")
        testobj.add_escape_action()
        assert capsys.readouterr().out == (
                "called Action.shortcuts\n"
                "called Action.setShortcuts with arg `['Ctrl-Q', 'Esc']`\n")

    def test_remove_escape_action(self, monkeypatch, capsys):
        """unittest for MainGui.remove_escape_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.quit_shortcuts = ['Ctrl-Q', 'Esc']
        testobj.quit_action = mockqtw.MockAction()
        testobj.quit_action.setShortcut('x')
        assert capsys.readouterr().out == ('called Action.__init__ with args ()\n'
                                           'called Action.setShortcut with arg `x`\n')
        testobj.remove_escape_action()
        assert capsys.readouterr().out == "called Action.shortcuts\n"

        testobj.quit_action.setShortcuts(['x', 'y'])
        assert capsys.readouterr().out == "called Action.setShortcuts with arg `['x', 'y']`\n"
        testobj.remove_escape_action()
        assert capsys.readouterr().out == ("called Action.shortcuts\n"
                                           "called Action.setShortcuts with arg `['Ctrl-Q']`\n")
