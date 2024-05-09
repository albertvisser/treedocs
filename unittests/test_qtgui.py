"""unittests for ./doctree/qtgui.py
"""
from doctree import qtgui as testee


def _test_show_message(monkeypatch, capsys):
    """unittest for qtgui.show_message
    """
    assert testee.show_message(win, text) == "expected_result"


def _test_ask_ynquestion(monkeypatch, capsys):
    """unittest for qtgui.ask_ynquestion
    """
    assert testee.ask_ynquestion(win, text) == "expected_result"


def _test_ask_yncquestion(monkeypatch, capsys):
    """unittest for qtgui.ask_yncquestion
    """
    assert testee.ask_yncquestion(win, text) == "expected_result"


def _test_get_text(monkeypatch, capsys):
    """unittest for qtgui.get_text
    """
    assert testee.get_text(win, caption, oldtext) == "expected_result"


def _test_get_choice(monkeypatch, capsys):
    """unittest for qtgui.get_choice
    """
    assert testee.get_choice(win, caption, options, current) == "expected_result"


def _test_get_filename(monkeypatch, capsys):
    """unittest for qtgui.get_filename
    """
    assert testee.get_filename(win, title, start, save=False) == "expected_result"


def _test_show_dialog(monkeypatch, capsys):
    """unittest for qtgui.show_dialog
    """
    assert testee.show_dialog(win, cls, kwargs=None) == "expected_result"


def _test_show_nonmodal(monkeypatch, capsys):
    """unittest for qtgui.show_nonmodal
    """
    assert testee.show_nonmodal(win, cls) == "expected_result"


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
        assert capsys.readouterr().out == 'called CheckDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for CheckDialog.__init__
        """
        testobj = testee.CheckDialog(parent, message="", option="")
        assert capsys.readouterr().out == ("")

    def _test_klaar(self, monkeypatch, capsys):
        """unittest for CheckDialog.klaar
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.klaar() == "expected_result"
        assert capsys.readouterr().out == ("")


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
        assert capsys.readouterr().out == 'called OptionsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for OptionsDialog.__init__
        """
        testobj = testee.OptionsDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for OptionsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


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
        assert capsys.readouterr().out == 'called SearchDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SearchDialog.__init__
        """
        testobj = testee.SearchDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_check_modes(self, monkeypatch, capsys):
        """unittest for SearchDialog.check_modes
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.check_modes() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SearchDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestResultsDialog:
    """unittest for qtgui.ResultsDialog
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
        assert capsys.readouterr().out == 'called ResultsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ResultsDialog.__init__
        """
        testobj = testee.ResultsDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_populate_list(self, monkeypatch, capsys):
        """unittest for ResultsDialog.populate_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.populate_list() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_goto_next(self, monkeypatch, capsys):
        """unittest for ResultsDialog.goto_next
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.goto_next() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_goto_prev(self, monkeypatch, capsys):
        """unittest for ResultsDialog.goto_prev
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.goto_prev() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_goto_selected(self, monkeypatch, capsys):
        """unittest for ResultsDialog.goto_selected
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.goto_selected() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_goto_and_close(self, monkeypatch, capsys):
        """unittest for ResultsDialog.goto_and_close
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.goto_and_close() == "expected_result"
        assert capsys.readouterr().out == ("")

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
        assert capsys.readouterr().out == 'called UndoRedoStack.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for UndoRedoStack.__init__
        """
        testobj = testee.UndoRedoStack(parent)
        assert capsys.readouterr().out == ("")

    def _test_clean_changed(self, monkeypatch, capsys):
        """unittest for UndoRedoStack.clean_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clean_changed(state) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_index_changed(self, monkeypatch, capsys):
        """unittest for UndoRedoStack.index_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.index_changed(num) == "expected_result"
        assert capsys.readouterr().out == ("")


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
        assert capsys.readouterr().out == 'called AddCommand.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for AddCommand.__init__
        """
        testobj = testee.AddCommand(win, root, under, new_title, extra_titles, description='Add')
        assert capsys.readouterr().out == ("")

    def _test_redo(self, monkeypatch, capsys):
        """unittest for AddCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.redo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_undo(self, monkeypatch, capsys):
        """unittest for AddCommand.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.undo() == "expected_result"
        assert capsys.readouterr().out == ("")


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
        assert capsys.readouterr().out == 'called PasteCommand.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for PasteCommand.__init__
        """
        testobj = testee.PasteCommand(win, before, below, item, description="Paste")
        assert capsys.readouterr().out == ("")

    def _test_redo(self, monkeypatch, capsys):
        """unittest for PasteCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.redo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_undo(self, monkeypatch, capsys):
        """unittest for PasteCommand.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.undo() == "expected_result"
        assert capsys.readouterr().out == ("")


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
        assert capsys.readouterr().out == 'called CopyCommand.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for CopyCommand.__init__
        """
        testobj = testee.CopyCommand(win, cut, retain, item, description="")
        assert capsys.readouterr().out == ("")

    def _test_redo(self, monkeypatch, capsys):
        """unittest for CopyCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.redo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_undo(self, monkeypatch, capsys):
        """unittest for CopyCommand.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.undo() == "expected_result"
        assert capsys.readouterr().out == ("")


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
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for TreePanel.__init__
        """
        testobj = testee.TreePanel(parent)
        assert capsys.readouterr().out == ("")

    def _test_selectionChanged(self, monkeypatch, capsys):
        """unittest for TreePanel.selectionChanged
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.selectionChanged(newsel, oldsel) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_dropEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.dropEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.dropEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_mousePressEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mousePressEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.mousePressEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_mouseReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mouseReleaseEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.mouseReleaseEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.keyReleaseEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.keyReleaseEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_create_popupmenu(self, monkeypatch, capsys):
        """unittest for TreePanel.create_popupmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_popupmenu(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_to_parent(self, monkeypatch, capsys):
        """unittest for TreePanel.add_to_parent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_to_parent(itemkey, titel, parent, pos=-1) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getitemdata(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemdata
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getitemdata(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getitemuserdata(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemuserdata
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getitemuserdata(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getitemtitle(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemtitle
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getitemtitle(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getitemkey(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemkey
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getitemkey(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setitemtitle(self, monkeypatch, capsys):
        """unittest for TreePanel.setitemtitle
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setitemtitle(item, title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setitemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.setitemtext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setitemtext(item, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getitemkids(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemkids
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getitemkids(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getitemparentpos(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemparentpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getitemparentpos(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getselecteditem(self, monkeypatch, capsys):
        """unittest for TreePanel.getselecteditem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getselecteditem() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_item_expanded(self, monkeypatch, capsys):
        """unittest for TreePanel.set_item_expanded
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_item_expanded(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_item_collapsed(self, monkeypatch, capsys):
        """unittest for TreePanel.set_item_collapsed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_item_collapsed(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_item_selected(self, monkeypatch, capsys):
        """unittest for TreePanel.set_item_selected
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_item_selected(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selected_item(self, monkeypatch, capsys):
        """unittest for TreePanel.get_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_removeitem(self, monkeypatch, capsys):
        """unittest for TreePanel.removeitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.removeitem(item, cut_from_itemdict) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getsubtree(self, monkeypatch, capsys):
        """unittest for TreePanel.getsubtree
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getsubtree(item, itemlist=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_putsubtree(self, monkeypatch, capsys):
        """unittest for TreePanel.putsubtree
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.putsubtree(parent, titel, key, subtree=None, pos=-1) == "expected_result"
        assert capsys.readouterr().out == ("")


def _test_tabsize(monkeypatch, capsys):
    """unittest for qtgui.tabsize
    """
    assert testee.tabsize(pointsize) == "expected_result"


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
        assert capsys.readouterr().out == 'called EditorPanel.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for EditorPanel.__init__
        """
        testobj = testee.EditorPanel(parent)
        assert capsys.readouterr().out == ("")

    def _test_canInsertFromMimeData(self, monkeypatch, capsys):
        """unittest for EditorPanel.canInsertFromMimeData
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.canInsertFromMimeData(source) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_insertFromMimeData(self, monkeypatch, capsys):
        """unittest for EditorPanel.insertFromMimeData
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.insertFromMimeData(source) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_contents(data) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_contents(self, monkeypatch, capsys):
        """unittest for EditorPanel.get_contents
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_contents() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_text_position(self, monkeypatch, capsys):
        """unittest for EditorPanel.get_text_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_text_position() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_text_position(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_text_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_text_position(pos) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_select_all(self, monkeypatch, capsys):
        """unittest for EditorPanel.select_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.select_all() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_bold(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_bold
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_bold() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_italic(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_italic
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_italic() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_underline(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_underline
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_underline() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_strikethrough(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_strikethrough
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_strikethrough() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_align_left(self, monkeypatch, capsys):
        """unittest for EditorPanel.align_left
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.align_left() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_align_center(self, monkeypatch, capsys):
        """unittest for EditorPanel.align_center
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.align_center() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_align_right(self, monkeypatch, capsys):
        """unittest for EditorPanel.align_right
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.align_right() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_justify(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_justify
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_justify() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_indent_more(self, monkeypatch, capsys):
        """unittest for EditorPanel.indent_more
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.indent_more() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_indent_less(self, monkeypatch, capsys):
        """unittest for EditorPanel.indent_less
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.indent_less() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_increase_parspacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.increase_parspacing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.increase_parspacing() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_decrease_parspacing(self, monkeypatch, capsys):
        """unittest for EditorPanel.decrease_parspacing
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.decrease_parspacing() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_linespacing_10(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_linespacing_10
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_linespacing_10() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_linespacing_15(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_linespacing_15
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_linespacing_15() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_linespacing_20(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_linespacing_20
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_linespacing_20() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_font(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_font
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_font() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_family(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_family
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_family(family) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enlarge_text(self, monkeypatch, capsys):
        """unittest for EditorPanel.enlarge_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enlarge_text() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_shrink_text(self, monkeypatch, capsys):
        """unittest for EditorPanel.shrink_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.shrink_text() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_size(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_size
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_size(size) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_text_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.text_color
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.text_color() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_text_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_text_color
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_text_color() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_background_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.background_color
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.background_color() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_background_color(self, monkeypatch, capsys):
        """unittest for EditorPanel.set_background_color
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_background_color() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_charformat_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.charformat_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.charformat_changed(fmt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_cursorposition_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.cursorposition_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.cursorposition_changed() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_font_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.font_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.font_changed(font) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_color_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.color_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.color_changed(col) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_background_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.background_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.background_changed(col) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_alignment_changed(self, monkeypatch, capsys):
        """unittest for EditorPanel.alignment_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.alignment_changed(align) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_mergeCurrentCharFormat(self, monkeypatch, capsys):
        """unittest for EditorPanel.mergeCurrentCharFormat
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.mergeCurrentCharFormat(fmt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_check_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel.check_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.check_dirty() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_mark_dirty(self, monkeypatch, capsys):
        """unittest for EditorPanel.mark_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.mark_dirty(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_openup(self, monkeypatch, capsys):
        """unittest for EditorPanel.openup
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.openup(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_focusInEvent(self, monkeypatch, capsys):
        """unittest for EditorPanel.focusInEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.focusInEvent(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_focusOutEvent(self, monkeypatch, capsys):
        """unittest for EditorPanel.focusOutEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.focusOutEvent(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_search_from_start(self, monkeypatch, capsys):
        """unittest for EditorPanel.search_from_start
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.search_from_start() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_find_next(self, monkeypatch, capsys):
        """unittest for EditorPanel.find_next
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_next() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_find_prev(self, monkeypatch, capsys):
        """unittest for EditorPanel.find_prev
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_prev() == "expected_result"
        assert capsys.readouterr().out == ("")


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

    def _test_init(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        testobj = testee.MainGui(master, title)
        assert capsys.readouterr().out == ("")

    def _test_setup_screen(self, monkeypatch, capsys):
        """unittest for MainGui.setup_screen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_screen() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_create_menu(self, monkeypatch, capsys):
        """unittest for MainGui.create_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_menu(menubar, menudata) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_disable_menu(self, monkeypatch, capsys):
        """unittest for MainGui.disable_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.disable_menu(value=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_create_stylestoolbar(self, monkeypatch, capsys):
        """unittest for MainGui.create_stylestoolbar
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_stylestoolbar() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.show_statusmessage
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_statusmessage(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_version(self, monkeypatch, capsys):
        """unittest for MainGui.set_version
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_version() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_window_dimensions(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_dimensions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_window_dimensions(x, y) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_screensize(self, monkeypatch, capsys):
        """unittest for MainGui.get_screensize
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_screensize() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_windowtitle(self, monkeypatch, capsys):
        """unittest for MainGui.set_windowtitle
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_windowtitle(title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_window_split(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_split
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_window_split(pos) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_splitterpos(self, monkeypatch, capsys):
        """unittest for MainGui.get_splitterpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_splitterpos() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_app(self, monkeypatch, capsys):
        """unittest for MainGui.init_app
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_app() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_focus_to_tree(self, monkeypatch, capsys):
        """unittest for MainGui.set_focus_to_tree
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_focus_to_tree() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_focus_to_editor(self, monkeypatch, capsys):
        """unittest for MainGui.set_focus_to_editor
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_focus_to_editor() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go(self, monkeypatch, capsys):
        """unittest for MainGui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_close(self, monkeypatch, capsys):
        """unittest for MainGui.close
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.close() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_closeEvent(self, monkeypatch, capsys):
        """unittest for MainGui.closeEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.closeEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_hide_me(self, monkeypatch, capsys):
        """unittest for MainGui.hide_me
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.hide_me() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_revive(self, monkeypatch, capsys):
        """unittest for MainGui.revive
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.revive(event=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_expand_root(self, monkeypatch, capsys):
        """unittest for MainGui.expand_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.expand_root() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_start_add(self, monkeypatch, capsys):
        """unittest for MainGui.start_add
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.start_add(root=None, under=True, new_title='', extra_titles=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_next_item(self, monkeypatch, capsys):
        """unittest for MainGui.set_next_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_next_item(any_level=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_prev_item(self, monkeypatch, capsys):
        """unittest for MainGui.set_prev_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_prev_item(any_level=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_start_copy(self, monkeypatch, capsys):
        """unittest for MainGui.start_copy
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.start_copy(cut=False, retain=True, current=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_start_paste(self, monkeypatch, capsys):
        """unittest for MainGui.start_paste
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.start_paste(before=True, below=False, dest=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_reorder_items(self, monkeypatch, capsys):
        """unittest for MainGui.reorder_items
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.reorder_items(root, recursive=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_rebuild_root(self, monkeypatch, capsys):
        """unittest for MainGui.rebuild_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.rebuild_root() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_viewmenu(self, monkeypatch, capsys):
        """unittest for MainGui.clear_viewmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_viewmenu() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.add_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_viewmenu_option(optiontext) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_check_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.check_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.check_viewmenu_option(action=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_uncheck_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.uncheck_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.uncheck_viewmenu_option() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_rename_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.rename_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.rename_viewmenu_option(newname) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_check_next_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.check_next_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.check_next_viewmenu_option(prev=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_viewmenu_option(self, monkeypatch, capsys):
        """unittest for MainGui.remove_viewmenu_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_viewmenu_option(viewname) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_tree_undo(self, monkeypatch, capsys):
        """unittest for MainGui.tree_undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.tree_undo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_tree_redo(self, monkeypatch, capsys):
        """unittest for MainGui.tree_redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.tree_redo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_find_needle(self, monkeypatch, capsys):
        """unittest for MainGui.find_needle
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_needle(haystack) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_goto_searchresult(self, monkeypatch, capsys):
        """unittest for MainGui.goto_searchresult
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.goto_searchresult(loc) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_escape_action(self, monkeypatch, capsys):
        """unittest for MainGui.add_escape_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_escape_action() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_escape_action(self, monkeypatch, capsys):
        """unittest for MainGui.remove_escape_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_escape_action() == "expected_result"
        assert capsys.readouterr().out == ("")
