"""unittests for ./doctree/main.py
"""
import pytest
import doctree.main as testee


def test_init_opts():
    """unittest for main.init_opts
    """
    assert testee.init_opts() == {
        "Application": "DocTree", "NotifyOnSave": True, 'NotifyOnLoad': True, "AskBeforeHide": True,
        "EscapeClosesApp": True, "SashPosition": 180, "ScreenSize": (800, 500), "ActiveItem": [0],
        "ActiveView": 0, "ViewNames": ["Default"], "RootTitle": "MyNotes", "RootData": "",
        "ImageCount": 0}


def _test_add_newitems():
    """unittest for main.add_newitems
    """
    testee.add_newitems(copied_item, cut_from_itemdict, itemdict)


def _test_replace_keys():
    """unittest for main.replace_keys
    """
    testee.replace_keys(item, keymap)


def _test_add_item_to_view():
    """unittest for main.add_item_to_view
    """
    testee.add_item_to_view(item, view)


def _test_reset_toolkit_file_if_needed():
    """unittest for main.reset_toolkit_file_if_needed
    """
    testee.reset_toolkit_file_if_needed()


def _test_mainwindow_init(monkeypatch, capsys):
    """unittest for MainWindow.init
    """
    testobj.__init__(fname='')

def _test_mainwindow_get_menu_data(monkeypatch, capsys):
    """unittest for MainWindow.get_menu_data
    """
    testobj.get_menu_data()

def _test_mainwindow_set_window_title(monkeypatch, capsys):
    """unittest for MainWindow.set_window_title
    """
    testobj.set_window_title()

def _test_mainwindow_new(monkeypatch, capsys):
    """unittest for MainWindow.new
    """
    testobj.new(*args, filename='', ask_ok=True)

def _test_mainwindow_open(monkeypatch, capsys):
    """unittest for MainWindow.open
    """
    testobj.open(*args)

def _test_mainwindow_reread(monkeypatch, capsys):
    """unittest for MainWindow.reread
    """
    testobj.reread(*args)

def _test_mainwindow_save(monkeypatch, capsys):
    """unittest for MainWindow.save
    """
    testobj.save(*args)

def _test_mainwindow_saveas(monkeypatch, capsys):
    """unittest for MainWindow.saveas
    """
    testobj.saveas(*args)

def _test_mainwindow_rename_root(monkeypatch, capsys):
    """unittest for MainWindow.rename_root
    """
    testobj.rename_root(*args)

def _test_mainwindow_add_item(monkeypatch, capsys):
    """unittest for MainWindow.
    """
    testobj.add_item(*args)

def _test_mainwindow_root_item(monkeypatch, capsys):
    """unittest for MainWindow.root_item
    """
    testobj.root_item(*args)

def _test_mainwindow_insert_item(monkeypatch, capsys):
    """unittest for MainWindow.insert_item
    """
    testobj.insert_item(*args)

def _test_mainwindow_new_item(monkeypatch, capsys):
    """unittest for MainWindow.new_item
    """
    testobj.new_item(root=None, under=True)

def _test_mainwindow_get_item_title(monkeypatch, capsys):
    """unittest for MainWindow.get_item_title
    """
    testobj.get_item_title()

def _test_mainwindow_do_additem(monkeypatch, capsys):
    """unittest for MainWindow.do_additem
    """
    testobj.do_additem(root, under, origpos, new_title, extra_titles)

def _test_mainwindow_rename_item(monkeypatch, capsys):
    """unittest for MainWindow.rename_item
    """
    testobj.rename_item(*args)

def _test_mainwindow_ask_title(monkeypatch, capsys):
    """unittest for MainWindow.ask_title
    """
    testobj.ask_title(title, text)

def _test_mainwindow_expand_item(monkeypatch, capsys):
    """unittest for MainWindow.expand_item
    """
    testobj.expand_item(*args)

def _test_mainwindow_collapse_item(monkeypatch, capsys):
    """unittest for MainWindow.collapse_item
    """
    testobj.collapse_item(*args)

def _test_mainwindow_expand_all(monkeypatch, capsys):
    """unittest for MainWindow.expand_all
    """
    testobj.expand_all(*args)

def _test_mainwindow_collapse_all(monkeypatch, capsys):
    """unittest for MainWindow.collapse_all
    """
    testobj.collapse_all(*args)

def _test_mainwindow_expand(monkeypatch, capsys):
    """unittest for MainWindow.expand
    """
    testobj.expand(recursive=False)

def _test_mainwindow_collapse(monkeypatch, capsys):
    """unittest for MainWindow.collapse
    """
    testobj.collapse(recursive=False)

def _test_mainwindow_next_note(monkeypatch, capsys):
    """unittest for MainWindow.next_note
    """
    testobj.next_note(*args)

def _test_mainwindow_prev_note(monkeypatch, capsys):
    """unittest for MainWindow.prev_note
    """
    testobj.prev_note(*args)

def _test_mainwindow_next_note_any(monkeypatch, capsys):
    """unittest for MainWindow.next_note_any
    """
    testobj.next_note_any(*args)

def _test_mainwindow_prev_note_any(monkeypatch, capsys):
    """unittest for MainWindow.prev_note_any
    """
    testobj.prev_note_any(*args)

def _test_mainwindow_cut_item(monkeypatch, capsys):
    """unittest for MainWindow.cut_item
    """
    testobj.cut_item(*args)

def _test_mainwindow_delete_item(monkeypatch, capsys):
    """unittest for MainWindow.delete_item
    """
    testobj.delete_item(*args)

def _test_mainwindow_copy_item(monkeypatch, capsys):
    """unittest for MainWindow.copy_item
    """
    testobj.copy_item(*args)

def _test_mainwindow_get_copy_item(monkeypatch, capsys):
    """unittest for MainWindow.get_copy_item
    """
    testobj.get_copy_item(cut=False, retain=True, to_other_file=None)

def _test_mainwindow_get_copy_source(monkeypatch, capsys):
    """unittest for MainWindow.get_copy_source
    """
    testobj.get_copy_source(cut, retain, to_other_file)

def _test_mainwindow_do_copyaction(monkeypatch, capsys):
    """unittest for MainWindow.do_copyaction
    """
    testobj.do_copyaction(cut, retain, current)  # to_other_file):

def _test_mainwindow_popitems(monkeypatch, capsys):
    """unittest for MainWindow.popitems
    """
    testobj.popitems(current, itemlist)

def _test_mainwindow_paste_item(monkeypatch, capsys):
    """unittest for MainWindow.paste_item
    """
    testobj.paste_item(*args)

def _test_mainwindow_paste_item_after(monkeypatch, capsys):
    """unittest for MainWindow.paste_item_after
    """
    testobj.paste_item_after(*args)

def _test_mainwindow_paste_item_below(monkeypatch, capsys):
    """unittest for MainWindow.paste_item_below
    """
    testobj.paste_item_below(*args)

def _test_mainwindow_put_paste_item(monkeypatch, capsys):
    """unittest for MainWindow.put_paste_item
    """
    testobj.put_paste_item(before=True, below=False)

def _test_mainwindow_get_paste_dest(monkeypatch, capsys):
    """unittest for MainWindow.get_paste_dest
    """
    testobj.get_paste_dest(below)  # , before

def _test_mainwindow_do_pasteitem(monkeypatch, capsys):
    """unittest for MainWindow.do_pasteitem
    """
    testobj.do_pasteitem(before, below, current)

def _test_mainwindow_add_items_back(monkeypatch, capsys):
    """unittest for MainWindow.add_items_back
    """
    testobj.add_items_back()

def _test_mainwindow_move_to_file(monkeypatch, capsys):
    """unittest for MainWindow.move_to_file
    """
    testobj.move_to_file(*args)

def _test_mainwindow_order_top(monkeypatch, capsys):
    """unittest for MainWindow.order_top
    """
    testobj.order_top(*args)

def _test_mainwindow_order_all(monkeypatch, capsys):
    """unittest for MainWindow.order_all
    """
    testobj.order_all(*args)

def _test_mainwindow_order_this(monkeypatch, capsys):
    """unittest for MainWindow.order_this
    """
    testobj.order_this(*args)

def _test_mainwindow_order_lower(monkeypatch, capsys):
    """unittest for MainWindow.order_lower
    """
    testobj.order_lower(*args)

def _test_mainwindow_reorder(monkeypatch, capsys):
    """unittest for MainWindow.reorder
    """
    testobj.reorder(root, recursive=False)

def _test_mainwindow_hide_me(monkeypatch, capsys):
    """unittest for MainWindow.hide_me
    """
    testobj.hide_me(*args)

def _test_mainwindow_change_pane(monkeypatch, capsys):
    """unittest for MainWindow.change_pane
    """
    testobj.change_pane(*args)

def _test_mainwindow_set_options(monkeypatch, capsys):
    """unittest for MainWindow.set_options
    """
    testobj.set_options(*args)

def _test_mainwindow_add_view(monkeypatch, capsys):
    """unittest for MainWindow.add_view
    """
    testobj.add_view(*args)

def _test_mainwindow_rename_view(monkeypatch, capsys):
    """unittest for MainWindow.rename_view
    """
    testobj.rename_view(*args)

def _test_mainwindow_remove_view(monkeypatch, capsys):
    """unittest for MainWindow.remove_view
    """
    testobj.remove_view(*args)

def _test_mainwindow_next_view(monkeypatch, capsys):
    """unittest for MainWindow.next_view
    """
    testobj.next_view(*args)

def _test_mainwindow_prev_view(monkeypatch, capsys):
    """unittest for MainWindow.prev_view
    """
    testobj.prev_view(*args)

def _test_mainwindow_goto_view(monkeypatch, capsys):
    """unittest for MainWindow.goto_view
    """
    testobj.goto_view(goto_next=True)

def _test_mainwindow_select_view_from_dropdown(monkeypatch, capsys):
    """unittest for MainWindow.select_view_from_dropdown
    """
    testobj.select_view_from_dropdown()

def _test_mainwindow_select_view(monkeypatch, capsys):
    """unittest for MainWindow.select_view
    """
    testobj.select_view()

def _test_mainwindow_search(monkeypatch, capsys):
    """unittest for MainWindow.search
    """
    testobj.search(*args, mode=0)

def _test_mainwindow_search_texts(monkeypatch, capsys):
    """unittest for MainWindow.search_texts
    """
    testobj.search_texts(*args)

def _test_mainwindow_search_titles(monkeypatch, capsys):
    """unittest for MainWindow.search_titles
    """
    testobj.search_titles(*args)

def _test_mainwindow_find_next(monkeypatch, capsys):
    """unittest for MainWindow.find_next
    """
    testobj.find_next(*args)

def _test_mainwindow_find_prev(monkeypatch, capsys):
    """unittest for MainWindow.find_prev
    """
    testobj.find_prev(*args)

def _test_mainwindow_search_from(monkeypatch, capsys):
    """unittest for MainWindow.search_from
    """
    testobj.search_from(parent, loc=None)

def _test_mainwindow_go_to_result(monkeypatch, capsys):
    """unittest for MainWindow.go_to_result
    """
    testobj.go_to_result()

def _test_mainwindow_info_page(monkeypatch, capsys):
    """unittest for MainWindow.info_page
    """
    testobj.info_page(*args)

def _test_mainwindow_help_page(monkeypatch, capsys):
    """unittest for MainWindow.help_page
    """
    testobj.help_page(*args)

def _test_mainwindow_set_project_dirty(monkeypatch, capsys):
    """unittest for MainWindow.set_project_dirty
    """
    testobj.set_project_dirty(value)

def _test_mainwindow_save_needed(monkeypatch, capsys):
    """unittest for MainWindow.save_needed
    """
    testobj.save_needed(meld=True, always_check=True)

def _test_mainwindow_treetoview(monkeypatch, capsys):
    """unittest for MainWindow.treetoview
    """
    testobj.treetoview()

def _test_mainwindow_viewtotree(monkeypatch, capsys):
    """unittest for MainWindow.viewtotree
    """
    testobj.viewtotree()

def _test_mainwindow_check_active(monkeypatch, capsys):
    """unittest for MainWindow.check_active
    """
    testobj.check_active(message=None)

def _test_mainwindow_activate_item(monkeypatch, capsys):
    """unittest for MainWindow.activate_item
    """
    testobj.activate_item(item)

def _test_mainwindow_cleanup_files(monkeypatch, capsys):
    """unittest for MainWindow.cleanup_files
    """
    testobj.cleanup_files()

def _test_mainwindow_read(monkeypatch, capsys):
    """unittest for MainWindow.read
    """
    testobj.read(other_file='')

def _test_mainwindow_set_escape_option(monkeypatch, capsys):
    """unittest for MainWindow.set_escape_option
    """
    testobj.set_escape_option()

def _test_mainwindow_write(monkeypatch, capsys):
    """unittest for MainWindow.write
    """
    testobj.write(meld=True)

def _test_mainwindow_confirm(monkeypatch, capsys):
    """unittest for MainWindow.confirm
    """
    testobj.confirm(setting='', textitem='')
