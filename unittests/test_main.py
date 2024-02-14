"""unittests for ./doctree/main.py
"""
from doctree import main as testee


def test_init_opts(monkeypatch, capsys):
    """unittest for main.init_opts
    """
    assert testee.init_opts() == {
        "Application": "DocTree", "NotifyOnSave": True, 'NotifyOnLoad': True, "AskBeforeHide": True,
        "EscapeClosesApp": True, "SashPosition": 180, "ScreenSize": (800, 500), "ActiveItem": [0],
        "ActiveView": 0, "ViewNames": ["Default"], "RootTitle": "MyNotes", "RootData": "",
        "ImageCount": 0}


def _test_add_newitems(monkeypatch, capsys):
    """unittest for main.add_newitems
    """
    assert testee.add_newitems(copied_item, cut_from_itemdict, itemdict) == "expected_result"


def _test_replace_keys(monkeypatch, capsys):
    """unittest for main.replace_keys
    """
    assert testee.replace_keys(item, keymap) == "expected_result"


def _test_add_item_to_view(monkeypatch, capsys):
    """unittest for main.add_item_to_view
    """
    assert testee.add_item_to_view(item, view) == "expected_result"

    testobj = self.setup_testobj(monkeypatch, capsys)
    assert testobj.add_item_to_view(item, view) == "expected_result"
    assert capsys.readouterr().out == ("")


def _test_reset_toolkit_file_if_needed(monkeypatch, capsys):
    """unittest for main.reset_toolkit_file_if_needed
    """
    assert testee.reset_toolkit_file_if_needed() == "expected_result"


class _TestMainWindow:
    """unittest for main.MainWindow
    """
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
        testobj = testee.MainWindow()
        assert capsys.readouterr().out == 'called MainWindow.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for MainWindow.__init__
        """
        testobj = testee.MainWindow(fname='')
        assert capsys.readouterr().out == ("")

    def _test_get_menu_data(self, monkeypatch, capsys):
        """unittest for MainWindow.get_menu_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_menu_data() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_window_title(self, monkeypatch, capsys):
        """unittest for MainWindow.set_window_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_window_title() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_new(self, monkeypatch, capsys):
        """unittest for MainWindow.new
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.new(*args, filename='', ask_ok=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_open(self, monkeypatch, capsys):
        """unittest for MainWindow.open
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.open(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_reread(self, monkeypatch, capsys):
        """unittest for MainWindow.reread
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.reread(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_save(self, monkeypatch, capsys):
        """unittest for MainWindow.save
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.save(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_saveas(self, monkeypatch, capsys):
        """unittest for MainWindow.saveas
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.saveas(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_rename_root(self, monkeypatch, capsys):
        """unittest for MainWindow.rename_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.rename_root(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_item(self, monkeypatch, capsys):
        """unittest for MainWindow.add_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_item(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_root_item(self, monkeypatch, capsys):
        """unittest for MainWindow.root_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.root_item(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_insert_item(self, monkeypatch, capsys):
        """unittest for MainWindow.insert_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.insert_item(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_new_item(self, monkeypatch, capsys):
        """unittest for MainWindow.new_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.new_item(root=None, under=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_item_title(self, monkeypatch, capsys):
        """unittest for MainWindow.get_item_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_title() == "expected_result"
        assert capsys.readouterr().out == ("")

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

    def _test_ask_title(self, monkeypatch, capsys):
        """unittest for MainWindow.ask_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_title(title, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_expand_item(self, monkeypatch, capsys):
        """unittest for MainWindow.expand_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.expand_item(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_collapse_item(self, monkeypatch, capsys):
        """unittest for MainWindow.collapse_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.collapse_item(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_expand_all(self, monkeypatch, capsys):
        """unittest for MainWindow.expand_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.expand_all(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_collapse_all(self, monkeypatch, capsys):
        """unittest for MainWindow.collapse_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.collapse_all(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_expand(self, monkeypatch, capsys):
        """unittest for MainWindow.expand
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.expand(recursive=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_collapse(self, monkeypatch, capsys):
        """unittest for MainWindow.collapse
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.collapse(recursive=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_next_note(self, monkeypatch, capsys):
        """unittest for MainWindow.next_note
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.next_note(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_prev_note(self, monkeypatch, capsys):
        """unittest for MainWindow.prev_note
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.prev_note(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_next_note_any(self, monkeypatch, capsys):
        """unittest for MainWindow.next_note_any
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.next_note_any(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_prev_note_any(self, monkeypatch, capsys):
        """unittest for MainWindow.prev_note_any
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.prev_note_any(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_cut_item(self, monkeypatch, capsys):
        """unittest for MainWindow.cut_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.cut_item(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_item(self, monkeypatch, capsys):
        """unittest for MainWindow.delete_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_item(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_copy_item(self, monkeypatch, capsys):
        """unittest for MainWindow.copy_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.copy_item(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_copy_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_copy_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_copy_item(cut=False, retain=True, to_other_file=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_copy_source(self, monkeypatch, capsys):
        """unittest for MainWindow.get_copy_source
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_copy_source(cut, retain, to_other_file) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_do_copyaction(self, monkeypatch, capsys):
        """unittest for MainWindow.do_copyaction
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_copyaction(cut, retain, current) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_popitems(self, monkeypatch, capsys):
        """unittest for MainWindow.popitems
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.popitems(current, itemlist) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_paste_item(self, monkeypatch, capsys):
        """unittest for MainWindow.paste_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.paste_item(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_paste_item_after(self, monkeypatch, capsys):
        """unittest for MainWindow.paste_item_after
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.paste_item_after(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_paste_item_below(self, monkeypatch, capsys):
        """unittest for MainWindow.paste_item_below
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.paste_item_below(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_put_paste_item(self, monkeypatch, capsys):
        """unittest for MainWindow.put_paste_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.put_paste_item(before=True, below=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_paste_dest(self, monkeypatch, capsys):
        """unittest for MainWindow.get_paste_dest
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_paste_dest(below) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_do_pasteitem(self, monkeypatch, capsys):
        """unittest for MainWindow.do_pasteitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_pasteitem(before, below, current) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_items_back(self, monkeypatch, capsys):
        """unittest for MainWindow.add_items_back
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_items_back() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_move_to_file(self, monkeypatch, capsys):
        """unittest for MainWindow.move_to_file
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.move_to_file(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_order_top(self, monkeypatch, capsys):
        """unittest for MainWindow.order_top
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.order_top(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_order_all(self, monkeypatch, capsys):
        """unittest for MainWindow.order_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.order_all(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_order_this(self, monkeypatch, capsys):
        """unittest for MainWindow.order_this
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.order_this(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_order_lower(self, monkeypatch, capsys):
        """unittest for MainWindow.order_lower
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.order_lower(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_reorder(self, monkeypatch, capsys):
        """unittest for MainWindow.reorder
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.reorder(root, recursive=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_hide_me(self, monkeypatch, capsys):
        """unittest for MainWindow.hide_me
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.hide_me(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_change_pane(self, monkeypatch, capsys):
        """unittest for MainWindow.change_pane
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.change_pane(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_options(self, monkeypatch, capsys):
        """unittest for MainWindow.set_options
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_options(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_view(self, monkeypatch, capsys):
        """unittest for MainWindow.add_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_view(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_rename_view(self, monkeypatch, capsys):
        """unittest for MainWindow.rename_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.rename_view(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_view(self, monkeypatch, capsys):
        """unittest for MainWindow.remove_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_view(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_next_view(self, monkeypatch, capsys):
        """unittest for MainWindow.next_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.next_view(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_prev_view(self, monkeypatch, capsys):
        """unittest for MainWindow.prev_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.prev_view(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_goto_view(self, monkeypatch, capsys):
        """unittest for MainWindow.goto_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.goto_view(goto_next=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_select_view_from_dropdown(self, monkeypatch, capsys):
        """unittest for MainWindow.select_view_from_dropdown
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.select_view_from_dropdown() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_select_view(self, monkeypatch, capsys):
        """unittest for MainWindow.select_view
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.select_view() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_search(self, monkeypatch, capsys):
        """unittest for MainWindow.search
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.search(*args, mode=0) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_search_texts(self, monkeypatch, capsys):
        """unittest for MainWindow.search_texts
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.search_texts(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_search_titles(self, monkeypatch, capsys):
        """unittest for MainWindow.search_titles
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.search_titles(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_find_next(self, monkeypatch, capsys):
        """unittest for MainWindow.find_next
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_next(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_find_prev(self, monkeypatch, capsys):
        """unittest for MainWindow.find_prev
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_prev(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

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

    def _test_info_page(self, monkeypatch, capsys):
        """unittest for MainWindow.info_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.info_page(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_help_page(self, monkeypatch, capsys):
        """unittest for MainWindow.help_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.help_page(*args) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_project_dirty(self, monkeypatch, capsys):
        """unittest for MainWindow.set_project_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_project_dirty(value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_save_needed(self, monkeypatch, capsys):
        """unittest for MainWindow.save_needed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.save_needed(meld=True, always_check=True) == "expected_result"
        assert capsys.readouterr().out == ("")

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
        assert testobj.check_active(message=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_activate_item(self, monkeypatch, capsys):
        """unittest for MainWindow.activate_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.activate_item(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_cleanup_files(self, monkeypatch, capsys):
        """unittest for MainWindow.cleanup_files
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.cleanup_files() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_read(self, monkeypatch, capsys):
        """unittest for MainWindow.read
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.read(other_file='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_escape_option(self, monkeypatch, capsys):
        """unittest for MainWindow.set_escape_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_escape_option() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_write(self, monkeypatch, capsys):
        """unittest for MainWindow.write
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.write(meld=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_confirm(self, monkeypatch, capsys):
        """unittest for MainWindow.confirm
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.confirm(setting='', textitem='') == "expected_result"
        assert capsys.readouterr().out == ("")
