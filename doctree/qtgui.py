"""DocTree: qt specific stuff
"""
import os
import sys
import contextlib
import subprocess
import PyQt6.QtGui as gui
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as core


def show_message(win, text):
    "show a confirmable message"
    qtw.QMessageBox.information(win, "DocTree", text, qtw.QMessageBox.StandardButton.Ok)


def ask_ynquestion(win, text):
    "ask a yes/no answerable question"
    result = qtw.QMessageBox.question(win, "DocTree", text, qtw.QMessageBox.StandardButton.Yes
                                      | qtw.QMessageBox.StandardButton.No,
                                      defaultButton=qtw.QMessageBox.StandardButton.Yes)
    return result == qtw.QMessageBox.StandardButton.Yes


def ask_yncquestion(win, text):
    "ask a yes/no answerable question with possibilty to cancel"
    result = qtw.QMessageBox.question(win, "DocTree", text, qtw.QMessageBox.StandardButton.Yes
                                      | qtw.QMessageBox.StandardButton.No
                                      | qtw.QMessageBox.StandardButton.Cancel,
                                      defaultButton=qtw.QMessageBox.StandardButton.Yes)
    return (result == qtw.QMessageBox.StandardButton.Yes,
            result == qtw.QMessageBox.StandardButton.Cancel)


def get_text(win, caption, oldtext):
    "open a dialog and get text input from the user"
    data, ok = qtw.QInputDialog.getText(win, "DocTree", caption, text=oldtext)
    newtext = str(data) if ok else oldtext
    return ok, newtext


def get_choice(win, caption, options, current):
    "open a dialog and let the user choose from a set of possible values"
    data, ok = qtw.QInputDialog.getItem(win, "DocTree", caption, options, current, editable=False)
    newtext = str(data) if ok else ''
    return ok, newtext


def get_filename(win, title, start, save=False):
    "routine for selection of filename"
    file_filter = "{}s (*{})".format(*win.master.FILE_TYPE)
    if save:
        filename = qtw.QFileDialog.getSaveFileName(win, title, start, file_filter)
    else:
        filename = qtw.QFileDialog.getOpenFileName(win, title, start, file_filter)
    ok = bool(filename[0])
    return ok, filename[0]


def show_dialog(dlg):
    "show dialog and return when confirmed or rejected"
    result = dlg.gui.exec()
    return result == qtw.QDialog.DialogCode.Accepted, dlg.dialog_data


def show_nonmodal(dlg):
    "show dialog and return to ongoing business"
    dlg.gui.show()


class MainGui(qtw.QMainWindow):
    "Primary application window (main screen)"
    def __init__(self, master, title):
        self.master = master
        self.title = title
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        offset = 40 if os.name != 'posix' else 10
        self.move(offset, offset)
        self.nt_icon = gui.QIcon(str(self.master.HERE / 'icons' / "doctree.xpm"))
        self.setWindowIcon(self.nt_icon)
        self.tray_icon = qtw.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip("Click to revive DocTree")
        self.tray_icon.activated.connect(self.revive)
        self.tray_icon.hide()
        self.menulist = []
        self.mainactiondict = {}
        self.styleactiondict = {}
        self.resize(self.master.opts['ScreenSize'][0], self.master.opts['ScreenSize'][1])
        self.setWindowTitle(self.title)
        self.in_editor = False

    def create_menu(self, menudata):
        """bouw het menu en de meeste toolbars op"""
        menubar = self.menuBar()
        for item, data in menudata:
            menu = menubar.addMenu(item)
            self.menulist.append(menu)
            toolbar_added = False
            if item == menudata[2][0]:
                self.viewmenu = menu
            elif item == menudata[1][0]:
                self.notemenu = menu
            elif item == menudata[3][0]:
                self.treemenu = menu
            prev = ''
            for menudef in data:
                if not menudef:
                    if prev != 'spacer':
                        prev = 'spacer'
                        menu.addSeparator()
                    else:
                        prev = ''
                    continue
                label, handler, shortcut, icon, info = menudef
                # (nog) niet in Qt geïmplementeerde menukeuzes overslaan
                if 'line spacing' in label.lower() or 'paragraph spacing' in label.lower():
                    continue
                if icon:
                    action = gui.QAction(gui.QIcon(str(self.master.HERE / icon)), label, self)
                    if not toolbar_added:
                        toolbar = self.addToolBar(item)
                        toolbar.setIconSize(core.QSize(16, 16))
                        toolbar_added = True
                    toolbar.addAction(action)
                else:
                    action = gui.QAction(label, self)
                if item == menudata[3][0]:
                    if label == '&Undo':
                        self.undo_item = action
                    elif label == '&Redo':
                        self.redo_item = action
                if shortcut:
                    # print('  item is', item, 'shortcut is', shortcut)
                    keys = list(shortcut.split(","))
                    action.setShortcuts(keys)
                    if menudef == menudata[0][1][-1]:
                        self.quit_action = action
                        self.quit_shortcuts = keys
                if info.startswith("Check"):
                    action.setCheckable(True)
                    info = info[5:]
                    if info in ('B', 'I', 'U', 'S', 'M'):
                        font = gui.QFont()
                        if info == 'B':
                            font.setBold(True)
                        elif info == 'I':
                            font.setItalic(True)
                        elif info == 'U':
                            font.setUnderline(True)
                        # else:
                        elif info == 'S':
                            font.setStrikeOut(True)
                        else:  # if info == 'M':
                            font.setFixedPitch(True)
                        action.setFont(font)
                        info = ''
                if info:
                    action.setStatusTip(info)
                action.triggered.connect(handler)
                if label:
                    menu.addAction(action)
                    if menu == self.menulist[0]:
                        self.mainactiondict[label] = action
                    elif len(self.menulist) > 5 and menu == self.menulist[5]:
                        self.styleactiondict[label] = action

    def create_splitter(self):
        "create main pportion of window"
        self.splitter = qtw.QSplitter(self)
        self.setCentralWidget(self.splitter)

    def create_tree_on_left(self):
        "create treeview for organizing"
        self.tree = TreePanel(self)
        self.splitter.addWidget(self.tree)

    def create_editor_on_right(self):
        "create editor"
        self.editor = EditorPanel(self)
        self.editor.setReadOnly(True)
        # self.editor.new_content = True
        self.splitter.addWidget(self.editor)

    def create_statusbar_at_bottom(self):
        "create area for status messages"
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

    def finalize_display(self):
        "finish off screen creation"
        self.menu_disabled = False
        self.undo_stack = UndoRedoStack(self)
        self.create_stylestoolbar()

        # dit lijkt in create_stylestoolbar ook gedaan te worden
        # pix = gui.QPixmap(14, 14)
        # pix.fill(self.setcoloraction_color)
        # self.setcolor_action.setIcon(gui.QIcon(pix))
        # pix = gui.QPixmap(18, 18)
        # pix.fill(self.setbackgroundcoloraction_color)
        # self.setbackgroundcolor_action.setIcon(gui.QIcon(pix))

    def disable_menu(self, value=True):
        """disable most menu actions when tree is not properly initialized;
        re-enable menu actions after tree is properly initialized
        """
        for menu in self.menulist[1:]:
            menu.setDisabled(value)
        for text, action in self.mainactiondict.items():
            if text not in ('&Open', '&Init', 'e&Xit'):
                action.setDisabled(value)
        self.menu_disabled = value

    def create_stylestoolbar(self):
        "build toolbar with buttons to change styles"
        # most is done during menu creation, this is some leftover stuff
        toolbar = self.addToolBar('styles')
        # self.combo_font = qtw.QFontComboBox(toolbar)
        # toolbar.addWidget(self.combo_font)
        # self.combo_font.currentTextChanged[str].connect(self.editor.text_family)
        # # self.combo_font.activated.connect(self.editor.text_family)
        # self.combo_size = qtw.QComboBox(toolbar)
        # toolbar.addWidget(self.combo_size)
        # self.combo_size.setEditable(True)
        # # db = gui.QFontDatabase()
        # self.fontsizes = []
        # # for size in db.standardSizes():
        # for size in gui.QFontDatabase.standardSizes():
        #     self.combo_size.addItem(str(size))
        #     self.fontsizes.append(str(size))
        self.fontsizes = [str(x) for x in gui.QFontDatabase.standardSizes()]
        # # self.combo.size.additems(self.fontsizes)
        # # self.combo_size.activated[str].connect(self.editor.text_size)
        # self.combo_size.activated.connect(self.editor.text_size)
        # self.combo_size.setCurrentIndex(self.combo_size.findText(
        #     str(self.editor.font().pointSize())))

        self.setcoloraction_color = core.Qt.GlobalColor.black
        pix = gui.QPixmap(14, 14)
        pix.fill(self.setcoloraction_color)
        action = gui.QAction(gui.QIcon(pix), "Change text color", self)
        action.triggered.connect(self.editor.select_text_color)
        toolbar.addAction(action)
        self.styleactiondict["&Color..."] = action
        pix = gui.QPixmap(14, 14)
        pix.fill(self.setcoloraction_color)
        action = gui.QAction(gui.QIcon(pix), "Set text color", self)
        action.triggered.connect(self.editor.set_text_color)
        toolbar.addAction(action)
        self.setcolor_action = action

        self.setbackgroundcoloraction_color = core.Qt.GlobalColor.white
        pix = gui.QPixmap(18, 18)
        pix.fill(self.setbackgroundcoloraction_color)
        action = gui.QAction(gui.QIcon(pix), "Change background color", self)
        action.triggered.connect(self.editor.select_background_color)
        toolbar.addAction(action)
        self.styleactiondict["&Background..."] = action
        pix = gui.QPixmap(18, 18)
        pix.fill(self.setbackgroundcoloraction_color)
        action = gui.QAction(gui.QIcon(pix), "Set background color", self)
        action.triggered.connect(self.editor.set_background_color)
        toolbar.addAction(action)
        self.setbackgroundcolor_action = action

    def show_statusmessage(self, text):
        "show message in status bar"
        self.statusbar.showMessage(text)

    def set_version(self):
        "GUI type instellen"
        self.master.opts["Version"] = "Qt"

    def set_window_dimensions(self, x, y):
        "venstergrootte instellen"
        self.resize(x, y)

    def get_screensize(self):
        "return the window's dimensions"
        return self.width(), self.height()

    def set_windowtitle(self, title):
        """standaard titel updaten"""
        self.setWindowTitle(title)

    def set_window_split(self, pos):
        "split positie instellen"
        # try:
        #     self.splitter.restoreState(pos)
        # except TypeError:
        #     pass
        self.splitter.setSizes(pos)

    def get_splitterpos(self):
        "return the position at which the screen is split"
        # return self.splitter.saveState()
        return self.splitter.sizes()

    def init_app(self):
        "undo stack leegmaken"
        self.undo_stack.clear()

    def set_focus_to_tree(self):
        "schakel over naar tree"
        self.tree.setFocus()
        self.in_editor = False

    def set_focus_to_editor(self):
        "set focus to the editor panel"
        self.editor.setFocus()
        ref = self.tree.getitemkey(self.master.activeitem)
        with contextlib.suppress(KeyError):
            self.editor.set_text_position(self.master.text_positions[ref])
        self.in_editor = True

    def go(self):
        "start the application's event loop"
        self.show()
        self.set_focus_to_editor()
        sys.exit(self.app.exec())

    def close(self):
        """applicatie afsluiten"""
        super().close()

    def closeEvent(self, event):
        "reimplemented event handler"
        # print('in closeEvent')
        if not self.master.handle_save_needed():
            event.ignore()
        else:
            self.master.cleanup_files()
            event.accept()

    def hide_me(self):
        """applicatie verbergen"""
        self.tray_icon.show()
        self.hide()

    def revive(self, event=None):
        """applicatie weer zichtbaar maken"""
        if event == qtw.QSystemTrayIcon.ActivationReason.Unknown:
            self.tray_icon.showMessage('DocTree', "Click to revive DocTree")
        elif event == qtw.QSystemTrayIcon.ActivationReason.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    def expand_root(self):
        "expandeer het root item"
        self.root.setExpanded(True)

    def start_add(self, root=None, under=True, new_title='', extra_titles=None):
        """nieuw item toevoegen (default: onder het geselecteerde)
        """
        command = AddCommand(self, root, under, new_title, extra_titles)
        self.undo_stack.push(command)

    def set_next_item(self, any_level=False):
        "for go to next"
        if any_level and self.master.activeitem.childCount() > 0:
            item = self.master.activeitem.child(0)
            self.tree.setCurrentItem(item)
            return True
        parent = self.master.activeitem.parent()
        if parent is not None:
            pos = parent.indexOfChild(self.master.activeitem)
            if pos < parent.childCount() - 1:
                item = parent.child(pos + 1)
                self.tree.setCurrentItem(item)
                return True
            if any_level:
                gp = parent.parent()
                while gp:
                    pos = gp.indexOfChild(parent)
                    if pos < gp.childCount() - 1:
                        item = gp.child(pos + 1)
                        self.tree.setCurrentItem(item)
                        return True
                    parent = gp
                    gp = parent.parent()
        return False

    def set_prev_item(self, any_level=False):
        "for go to previous"
        def get_prev_child_if_any(item):
            "search recursively"
            test = item.childCount()
            if test > 0:
                item = get_prev_child_if_any(item.child(test - 1))
            return item
        parent = self.master.activeitem.parent()
        if parent is not None:
            pos = parent.indexOfChild(self.master.activeitem)
            if any_level:
                if pos == 0:
                    self.tree.setCurrentItem(parent)
                    return True
                item = get_prev_child_if_any(parent.child(pos - 1))
                self.tree.setCurrentItem(item)
                return True
            if pos > 0:
                item = parent.child(pos - 1)
                self.tree.setCurrentItem(item)
                return True

    def start_copy(self, cut=False, retain=True, current=None):
        """start copy/cut/delete action

        parameters: cut: remove item from tree (True for cut, delete and move)
                    retain: remember item for pasting (True for cut and copy)
                    current: item to copy
        """
        command = CopyCommand(self, cut, retain, current)
        self.undo_stack.push(command)

    def start_paste(self, before=True, below=False, dest=None):
        """start paste actie
        """
        command = PasteCommand(self, before, below, dest)
        self.undo_stack.push(command)

    def reorder_items(self, root, recursive=False):
        "(re)order_items"
        root.sortChildren(0, core.Qt.SortOrder.AscendingOrder)
        if recursive:
            for num in range(root.childCount()):
                tag = root.child(num)
                self.reorder_items(tag, recursive)

    def rebuild_root(self):
        "tree leegmaken en root opnieuw neerzetten"
        self.root = self.tree.takeTopLevelItem(0)
        self.root = qtw.QTreeWidgetItem()
        self.tree.setitemkey(self.root, "-1")   # vaste waarde die niet in de itemdict voorkomt
        self.tree.setitemtitle(self.root, self.master.opts["RootTitle"])
        self.tree.setitemtext(self.root, self.master.opts["RootData"])
        self.tree.addTopLevelItem(self.root)
        return self.root

    # def clear_viewmenu(self):
    #     "remove all view actions from viewmenu"
    #     menuitem_list = list(self.viewmenu.actions())
    #     for menuitem in menuitem_list[8:]:
    #         self.viewmenu.removeAction(menuitem)

    def add_viewmenu_option(self, optiontext, callback):
        "add view action to viewmenu"
        action = gui.QAction(optiontext, self)
        action.setStatusTip("switch to this view")
        action.setCheckable(True)
        action.triggered.connect(callback)
        self.viewmenu.addAction(action)
        return action

    # def check_viewmenu_option(self, action=None):
    #     "check the given view action or determine which one to set"
    #     if action:
    #         action.setChecked(True)
    #         return ''
    #     sender = self.sender()
    #     menuitem_list = list(self.viewmenu.actions())
    #     for menuitem in menuitem_list[8:]:
    #         if menuitem == sender:
    #             newview = sender.text()
    #             sender.setChecked(True)
    #         elif menuitem.isChecked():
    #             menuitem.setChecked(False)
    #     return newview

    def check_menuitem_option(self, arg, value):
        "add or remove a checkmark to/from the given menu option"
        arg.setChecked(value)

    def determine_viewmenuitem(self, *args):
        "determine which menu option sent the menu event"
        # for qt this is the first argument
        return args[0]

    # def uncheck_viewmenu_option(self):
    #     "uncheck the active viewmenu action"
    #     menuitem_list = list(self.viewmenu.actions())
    #     for idx, menuitem in enumerate(menuitem_list[8:]):
    #         if idx == self.master.opts["ActiveView"]:
    #             menuitem.setChecked(False)

    # def rename_viewmenu_option(self, newname):
    #     "update action text"
    #     action = self.viewmenu.actions()[self.master.opts["ActiveView"] + 7]
    #     action.setText(f'{action.text().split()[0]} {newname}')

    # def check_next_viewmenu_option(self, prev=False):
    #     "find the currently checked option, uncheck it and check the next/previous one"
    #     menuitem_list = list(self.viewmenu.actions())[8:]
    #     if prev:
    #         menuitem_list.reverse()
    #     found_item = False
    #     for menuitem in menuitem_list:
    #         if menuitem.isChecked():
    #             found_item = True
    #             menuitem.setChecked(False)
    #         elif found_item:
    #             menuitem.setChecked(True)
    #             found_item = False
    #             break
    #     else:
    #         menuitem_list[0].setChecked(True)

    # def remove_viewmenu_option(self, viewname):
    #     "find the currently checked option, remove it and check the next one"
    #     menuitem_list = list(self.viewmenu.actions())
    #     removed = False
    #     item_to_check = None
    #     for menuitem in menuitem_list[8:]:
    #         num, naam = str(menuitem.text()).split(None, 1)
    #         if removed:
    #             menuitem.setText(f'&{int(num[1:]) - 1} {naam}')
    #             if not item_to_check:
    #                 item_to_check = menuitem
    #         if naam == viewname:
    #             self.viewmenu.removeAction(menuitem)
    #             removed = True
    #     return item_to_check or menuitem_list[8]

    def get_viewmenu_options(self):
        "return a list of items in a menu"
        return list(self.viewmenu.actions())  # [8:]

    def get_viewmenuoption_state(self, menuitem):
        "return the checked state of a menu option"
        return menuitem.isChecked()

    def get_menuitem_text(self, menuitem):
        "return the text of a menu option"
        return str(menuitem.text())

    def set_menuitem_text(self, menuitem, text):
        "set the text for a menu option"
        menuitem.setText(text)

    def remove_menuoption(self, menu, menuitem):
        "remove an option from a menu"
        menu.removeAction(menuitem)

    def tree_undo(self):  # , event=None):
        "start undo action"
        self.undo_stack.undo()

    def tree_redo(self):  # , event=None):
        "start redo action"
        self.undo_stack.redo()

    def find_needle(self, haystack):
        "search in plain text version of text"
        doc = gui.QTextDocument()
        doc.setPlainText(haystack)
        ok = doc.find(self.master.srchtext, options=self.set_searchflags())
        return not ok.isNull()

    def set_searchflags(self, backwards=False):
        """determine search flags from parent
        """
        # trucje om `flags` om op een valide "nul"waarde te initialiseren
        flags = gui.QTextDocument.FindFlag.FindBackward & ~gui.QTextDocument.FindFlag.FindBackward
        if self.master.srchflags.get('case', False):
            flags |= gui.QTextDocument.FindFlag.FindCaseSensitively
        if self.master.srchflags.get('words', False):
            flags |= gui.QTextDocument.FindFlag.FindWholeWords
        if backwards:
            flags |= gui.QTextDocument.FindFlag.FindBackward
        return flags

    def goto_searchresult(self, loc):
        "position on found data in text"
        treeitem = self.root
        for x in loc:
            treeitem = treeitem.child(x)
        self.tree.setCurrentItem(treeitem)
        if self.master.srchtype & 2:
            self.editor.search_from_start()   # bij de gratie van altijd naar de eerste gaan

    def add_escape_action(self):
        "Add accelerator to for Esc key to close application"
        if len(self.quit_action.shortcuts()) < len(['Ctrl-Q', 'Esc']):
            self.quit_action.setShortcuts(self.quit_shortcuts)

    def remove_escape_action(self):
        "Remove accelerator for Esc key to close application"
        if len(self.quit_action.shortcuts()) > 1:
            self.quit_action.setShortcuts(self.quit_shortcuts[:-1])

    def cleanup_after_writing(self):
        "re-initialize if necessary"
        self.undo_stack.setClean()


class TreePanel(qtw.QTreeWidget):
    "Tree structure depicting the notes organization"
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.setColumnCount(2)
        self.hideColumn(1)
        self.headerItem().setHidden(True)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        self.setDragDropMode(self.DragDropMode.InternalMove)
        self.setDropIndicatorShown(True)
        self.setUniformRowHeights(True)

    def selectionChanged(self, newsel, oldsel):
        """wordt aangeroepen als de selectie gewijzigd is

        de tekst van de oude selectie wordt in de itemdict geactualiseerd
        en die van de nieuwe wordt erin opgezocht en getoond"""
        # helaas zijn newsel en oldsel niet makkelijk om te rekenen naar treeitems
        self.parent.master.check_active()
        item = self.currentItem()
        self.parent.master.activate_item(item)
        self.parent.master.set_window_title()

    def dropEvent(self, event):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        deze methode breidt de Treewidget methode uit met wat visuele zaken
        """
        dragitem = self.selectedItems()[0]
        ## dragparent = dragitem.parent()
        pos = event.position().toPoint()
        dropitem = self.itemAt(pos)
        if not dropitem:
            ## event.ignore()
            return
        super().dropEvent(event)
        count = self.topLevelItemCount()
        if count > 1:
            for ix in range(count):
                if self.topLevelItem(ix) == dragitem:
                    self.takeTopLevelItem(ix)
                    self.oldparent.insertChild(self.oldpos, dragitem)
                    self.setCurrentItem(dragitem)
                    break
            return
        self.parent.master.set_project_dirty(True)
        self.setCurrentItem(dragitem)
        dropitem.setExpanded(True)

    def mousePressEvent(self, event):
        """remember the current parent in preparation for "canceling" a dragmove
        """
        pos = event.position().toPoint()  # event.x(), event.y()
        item = self.itemAt(pos)  # int(xc), int(yc))
        if item:
            self.oldparent, self.oldpos = self.getitemparentpos(item)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        "event handler for showing a context menu using the mouse"
        if event.button() == core.Qt.MouseButton.RightButton:
            # xc, yc = event.x(), event.y()
            # item = self.itemAt(xc, yc)
            pos = event.position().toPoint()  # event.x(), event.y()
            item = self.itemAt(pos)  # int(xc), int(yc))
            if item:
                self.create_popupmenu(item)
                return
            ## else:
                ## event.ignore()
        ## else:
            ## event.ignore()
        super().mouseReleaseEvent(event)

    def keyReleaseEvent(self, event):
        "event handler for showing a context menu using the keyboard"
        if event.key() == core.Qt.Key.Key_Menu:
            item = self.currentItem()
            self.create_popupmenu(item)
            return
        ## else:
            ## gui.QMainWindow.keyReleaseEvent(self, event)
        super().keyReleaseEvent(event)

    def create_popupmenu(self, item):
        "build the context menu"
        actiontexts = ('&Add', '&Delete', '&Forward', '&Back')
        menu = qtw.QMenu()
        for action in self.parent.notemenu.actions():
            menu.addAction(action)
            if item == self.parent.root and action.text() in actiontexts:
                action.setEnabled(False)
        menu.addSeparator()
        for action in self.parent.treemenu.actions():
            menu.addAction(action)
            if item == self.parent.root:
                action.setEnabled(False)
        menu.exec(self.mapToGlobal(self.visualItemRect(item).center()))
        # na uitsturen (en verwerken?) van het menu de uitgangssituatie terugzetten:
        if item == self.parent.root:
            for action in self.parent.notemenu.actions():
                if action.text() in actiontexts:
                    action.setEnabled(True)
            for action in self.parent.treemenu.actions():
                action.setEnabled(True)

    def add_to_parent(self, itemkey, titel, parent, pos=-1):
        """add item to tree at a given location
        """
        new = qtw.QTreeWidgetItem()
        self.setitemtitle(new, titel.rstrip())  # new.setText(0, titel.rstrip())
        # save plain text on tree item to facilitate search
        # faster that using BeautifulSoup? Also, we don't need the import this way
        doc = gui.QTextDocument()
        doc.setHtml(self.parent.master.itemdict[itemkey][1])
        rawtext = doc.toPlainText()
        self.setitemtext(new, rawtext)   # new.setData(0, core.Qt.ItemDataRole.UserRole, rawtext)
        self.setitemkey(new, itemkey)    # new.setText(1, str(itemkey))
        if pos == -1:
            parent.addChild(new)
        else:
            parent.insertChild(pos, new)
        return new

    def getitemdata(self, item):
        "titel + data in de visual tree ophalen"
        return self.getitemtitle(item), self.getitemkey(item)

    @staticmethod
    def getitemtext(item):
        "data in de visual tree ophalen"
        # eigenlijk is dit hetzelfde als item.text(1) - behalve bij het root item ?
        return item.data(0, core.Qt.ItemDataRole.UserRole)

    @staticmethod
    def getitemtitle(item):
        "alleen titel in de visual tree ophalen"
        return item.text(0)

    @staticmethod
    def getitemkey(item):
        "sleutel voor de itemdict ophalen"
        # value = item.text(1)
        # # with contextlib.suppress(ValueError):  # root item heeft tekst in plaats van itemdict key
        # # dat kwam doordat er een fout zat in de setitemtext methode
        # # root item moet nu altijd keywaarde -1 hebben
        # try:
        #     value = int(value)
        # except ValueError:                      # zou niet meer nodig moeten zijn
        #     print(f'{item=}, {self.root=}')
        #     value = -1
        # return value
        return int(item.text(1))

    @staticmethod
    def setitemkey(item, value):
        "sleutel voor de itemdict onthouden"
        item.setText(1, str(value))

    @staticmethod
    def setitemtitle(item, title):
        "titel (en tooltip instellen)"
        item.setText(0, title)
        item.setToolTip(0, title)

    @staticmethod
    def setitemtext(item, text):
        """Meant to set the text for the (root) item
        """
        item.setData(0, core.Qt.ItemDataRole.UserRole, text)

    @staticmethod
    def getitemkids(item):
        "children van item ophalen"
        return [item.child(num) for num in range(item.childCount())]

    @staticmethod
    def getitemparentpos(item):
        "parent en positie van item onder parent bepalen"
        root = item.parent()
        pos = root.indexOfChild(item) if root else -1
        return root, pos

    def getselecteditem(self):
        "return first selected item"
        return self.selectedItems()[0]

    @staticmethod
    def set_item_expanded(item):
        "expand a tree item"
        item.setExpanded(True)  # of: self.expandItem(item)

    @staticmethod
    def set_item_collapsed(item):
        "collapse a tree item"
        item.setExpanded(False)  # of: self.collapseItem(item)

    def set_item_selected(self, item):
        "select a tree item"
        self.setCurrentItem(item)

    def get_selected_item(self):
        "return the selected tree item"
        return self.currentItem()

    def removeitem(self, item):
        "removes current treeitem and returns the previous one"
        cut_from_itemdict = []
        parent, pos = self.getitemparentpos(item)
        oldloc = (parent, pos)
        if pos - 1 >= 0:
            prev = parent.child(pos - 1)
        else:
            prev = parent
            if prev == self.parent.root:
                prev = parent.child(pos + 1)
            if prev is None:
                prev = self.parent.root
        cut_from_itemdict = self.parent.master.popitems(item, cut_from_itemdict)
        # bij een undo van een add moeten met " \ " toegevoegde items ook verwijderd worden
        to_remove = [(parent, pos)] if parent else []
        while True:
            if item.childCount() == 0:
                break
            to_remove.append((item, 0))  # er is er altijd maar één
            item = item.child(0)
        for parent, pos in reversed(to_remove):
            parent.takeChild(pos)
        return oldloc, prev, cut_from_itemdict


def tabsize(pointsize):
    """pointsize omrekenen in pixels t.b.v. (gemiddelde) tekenbreedte
    """
    x, y = divmod(pointsize * 8, 10)
    return x * 4 if y < 5 else (x + 1) * 4


class EditorPanel(qtw.QTextEdit):
    "Rich text editor displaying the selected note"
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.setAcceptRichText(True)
        ## self.setTabChangesFocus(True)
        self.setAutoFormatting(qtw.QTextEdit.AutoFormattingFlag.AutoAll)
        self.currentCharFormatChanged.connect(self.charformat_changed)
        self.cursorPositionChanged.connect(self.cursorposition_changed)
        font = self.currentFont()
        self.setTabStopDistance(tabsize(font.pointSize()))
        self.paragraph_increment = 1  # 100

    def canInsertFromMimeData(self, source):
        "reimplemented"
        if source.hasImage():
            return True
        return super().canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        "reimplemented"
        if source.hasImage():
            image = source.imageData()
        elif self.islocalimage(source):
            image = gui.QImage()
            image.load(source.text().strip().removeprefix('file://'))
        else:
            super().insertFromMimeData(source)
            return
        cursor = self.textCursor()
        document = self.document()
        num = self.parent.master.opts['ImageCount']
        num += 1
        self.parent.master.opts['ImageCount'] = num
        url = self.parent.master.temp_imagepath / f'{num:05}.png'
        image.save(str(url))
        document.addResource(gui.QTextDocument.ResourceType.ImageResource, core.QUrl(str(url)),
                             image)
        cursor.insertImage(str(url))

    def islocalimage(self, source):
        """controleer of te plakken item een reeds opgeslagen plaatje is
        """
        source = source.text()
        try:
            if source.startswith('file://'):
                source = source.removeprefix('file://')
        except AttributeError:     # not a string
            return False
        source = source.strip()
        if not os.path.exists(source):  # does not exist
            return False
        test = subprocess.run(['file', '-bi', source], capture_output=True)
        return test.stdout.decode().startswith('image')  # is an image or not

    def set_contents(self, data):
        """load contents into editor

        also edits in the image references to point to the right location
        and retains the original value
        """
        data = data.replace('img src="', f'img src="{self.parent.master.temp_imagepath}/')
        self.setHtml(data)
        # dit hopenlijk niet nodig, want merkt document altijd aan als gewijzigd
        # fmt = gui.QTextCharFormat()
        # self.charformat_changed(fmt)  # callback voor currentCharFormatChanged event
        self.oldtext = data

    def get_contents(self):
        """return contents from editor

        also puts a plaintext version of the text in the internal tree (for searching)
        and removes the extraction location from the image references
        """
        # update plain text in tree item to facilitate search
        # self.parent.tree.currentItem().setData(0, core.Qt.ItemDataRole.UserRole, self.toPlainText())
        item = self.parent.tree.currentItem()
        self.parent.tree.setitemtext(item, self.toPlainText())
        return self.toHtml().replace(f'img src="{self.parent.master.temp_imagepath}/', 'img src="')

    def get_text_position(self):
        """return where the cursor is positioned in the text
        """
        cursor = self.textCursor()
        pos = cursor.position()
        # if cursor.atEnd():
        #     pos -= 1
        return pos

    def set_text_position(self, pos):
        """set where the cursor should appear in the text
        """
        cursor = self.textCursor()
        cursor.setPosition(pos)
        # cursor.movePosition(gui.QTextCursor.MoveOperation.NextCharacter, n=pos)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def select_all(self):
        "select complete text"
        self.selectAll()

    def text_bold(self):  # , event=None):
        "selectie vet maken"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        if self.parent.styleactiondict['&Bold'].isChecked():
            fmt.setFontWeight(gui.QFont.Weight.Bold)
        else:
            fmt.setFontWeight(gui.QFont.Weight.Normal)
        self.mergeCurrentCharFormat(fmt)

    def text_italic(self):  # , event=None):
        "selectie schuin schrijven"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontItalic(self.parent.styleactiondict['&Italic'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_underline(self):  # , event=None):
        "selectie onderstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontUnderline(self.parent.styleactiondict['&Underline'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_strikethrough(self):  # , event=None):
        "selectie doorstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontStrikeOut(self.parent.styleactiondict['Strike&through'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_monospace(self):  # , event=None):
        "selectie monospaced maken"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontFixedPitch(self.parent.styleactiondict['&Monospace'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def align_left(self):  # , event=None):
        "alinea links uitlijnen"
        if not self.hasFocus():
            return
        self.parent.styleactiondict["C&enter"].setChecked(False)
        self.parent.styleactiondict["Align &Right"].setChecked(False)
        self.parent.styleactiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignAbsolute)

    def align_center(self):  # , event=None):
        "alinea centreren"
        if not self.hasFocus():
            return
        self.parent.styleactiondict["Align &Left"].setChecked(False)
        self.parent.styleactiondict["Align &Right"].setChecked(False)
        self.parent.styleactiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignmentFlag.AlignHCenter)

    def align_right(self):  # , event=None):
        "alinea rechts uitlijnen"
        if not self.hasFocus():
            return
        self.parent.styleactiondict["Align &Left"].setChecked(False)
        self.parent.styleactiondict["C&enter"].setChecked(False)
        self.parent.styleactiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignAbsolute)

    def text_justify(self):  # , event=None):
        "alinea aan weerszijden uitlijnen"
        if not self.hasFocus():
            return
        self.parent.styleactiondict["Align &Left"].setChecked(False)
        self.parent.styleactiondict["C&enter"].setChecked(False)
        self.parent.styleactiondict["Align &Right"].setChecked(False)
        self.setAlignment(core.Qt.AlignmentFlag.AlignJustify)

    def indent_more(self):  # , event=None):
        "alinea verder laten inspringen"
        # uitgeprobeerd en alles wordt uitgevoerd
        if not self.hasFocus():
            return
        where = self.textCursor()
        fmt = where.blockFormat()
        wid = fmt.indent()
        fmt.setIndent(wid + self.paragraph_increment)
        where.setBlockFormat(fmt)
        self.setTextCursor(where)

    def indent_less(self):  # , event=None):
        "alinea minder ver laten inspringen"
        if not self.hasFocus():
            return
        where = self.textCursor()
        fmt = where.blockFormat()
        wid = fmt.indent()
        if wid >= self.paragraph_increment:
            fmt.setIndent(wid - self.paragraph_increment)
        where.setBlockFormat(fmt)
        self.setTextCursor(where)

    def increase_parspacing(self):
        "not implemented in Qt"

    def decrease_parspacing(self):
        "not implemented in Qt"

    # ProbReg gebruikt LineHeight
    def set_linespacing_10(self):
        "not implemented in Qt"

    def set_linespacing_15(self):
        "not implemented in Qt"

    def set_linespacing_20(self):
        "not implemented in Qt"

    def text_font(self):  # , event=None):
        "lettertype en/of -grootte instellen"
        if not self.hasFocus():
            return
        font, ok = qtw.QFontDialog.getFont(self.currentFont(), self)
        if ok:
            fmt = gui.QTextCharFormat()
            fmt.setFont(font)
            ## pointsize = float(font.pointSize())
            self.setTabStopDistance(tabsize(font.pointSize()))
            self.mergeCurrentCharFormat(fmt)

    def text_family(self, family):
        "lettertype instellen"
        fmt = gui.QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeCurrentCharFormat(fmt)
        self.setFocus()

    def enlarge_text(self):  # , event=None):
        "tekst groter maken"
        self.set_text_size(enlarge=True)

    def shrink_text(self):  # , event=None):
        "tekst kleiner maken"
        self.set_text_size(shrink=True)

    def set_text_size(self, enlarge=False, shrink=False):
        "lettergrootte instellen"
        # size = self.parent.combo_size.currentText()
        fmt = gui.QTextCharFormat()
        size = int(fmt.fontPointSize())
        # print(f'size from charformat {size}')
        if not size:
            size = gui.QFontDatabase.systemFont(gui.QFontDatabase.SystemFont.GeneralFont).pointSize()
        # dit werkt maar één keer en past feitelijk twee keer aan, omdat de uitgelezen grootte
        # nooit verandert
        size = str(size)
        # print(f"in editorpanel.set_text_size {size=} {self.parent.fontsizes=}", flush=True)
        indx = self.parent.fontsizes.index(size)
        # print(f'   {indx=} {len(self.parent.fontsizes)=}', flush=True)
        if enlarge and indx < len(self.parent.fontsizes) - 1:
            # print('enlarging text...', flush=True)
            size = self.parent.fontsizes[indx + 1]
        elif shrink and indx > 0:
            # print('shrinking text...', flush=True)
            size = self.parent.fontsizes[indx - 1]
        else:
            # print('doing nothing', flush=True)
            return
        # print(f'{size=}', flush=True)
        pointsize = float(size)
        if pointsize > 0:
            fmt = gui.QTextCharFormat()
            # print(f'setting pointsize to {pointsize=}', flush=True)
            fmt.setFontPointSize(pointsize)
            # self.setTabStopWidth(tabsize(pointsize))
            self.mergeCurrentCharFormat(fmt)
            # dit werkt om het zichtbaar te maken, maar blijkbaar niet om het te onthouden
            self.setFocus()
        # else:
        #     print(f'{pointsize=}, still doing nothing...', flush=True)

    def select_text_color(self):  # , event=None):
        "tekstkleur instellen"
        if not self.hasFocus():
            show_message(self, "Can't do this outside text field")
            return
        col = qtw.QColorDialog.getColor(self.textColor(), self)
        if not col.isValid():
            return
        self.parent.setcoloraction_color = col
        fmt = gui.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeCurrentCharFormat(fmt)
        self.color_changed(col)
        pix = gui.QPixmap(14, 14)
        pix.fill(col)
        self.parent.setcolor_action.setIcon(gui.QIcon(pix))

    def set_text_color(self):  # , event=None):
        "tekstkleur instellen"
        if not self.hasFocus():
            show_message(self, "Can't do this outside text field")
            return
        col = self.parent.setcoloraction_color
        fmt = gui.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeCurrentCharFormat(fmt)

    def select_background_color(self):  # , event=None):
        "achtergrondkleur instellen"
        if not self.hasFocus():
            show_message(self, "Can't do this outside text field")
            return
        col = qtw.QColorDialog.getColor(self.textBackgroundColor(), self)
        if not col.isValid():
            return
        self.parent.setbackgroundcoloraction_color = col
        fmt = gui.QTextCharFormat()
        fmt.setBackground(col)
        self.mergeCurrentCharFormat(fmt)
        self.background_changed(col)
        pix = gui.QPixmap(18, 18)
        pix.fill(col)
        self.parent.setbackgroundcolor_action.setIcon(gui.QIcon(pix))

    def set_background_color(self):  # , event=None):
        "achtergrondkleur instellen"
        if not self.hasFocus():
            show_message(self, "Can't do this outside text field")
            return
        col = self.parent.setbackgroundcoloraction_color
        fmt = gui.QTextCharFormat()
        fmt.setBackground(col)
        self.mergeCurrentCharFormat(fmt)

    def charformat_changed(self, fmt):
        "wordt aangeroepen als het tekstformat gewijzigd is"
        self.font_changed(fmt.font())
        self.color_changed(fmt.foreground().color())
        backg = fmt.background()
        bgcol = (core.Qt.GlobalColor.white if backg.style() == core.Qt.BrushStyle.NoBrush
                 else backg.color())
        self.background_changed(bgcol)

    def cursorposition_changed(self):
        "wordt aangeroepen als de cursorpositie gewijzigd is"
        self.alignment_changed(self.alignment())

    def font_changed(self, font):
        """fontgegevens aanpassen

        de selectie in de comboboxen wordt aangepast, de van toepassing zijnde
        menuopties worden aangevinkt, en en de betreffende toolbaricons worden
        geaccentueerd"""
        # self.parent.combo_font.setCurrentIndex(
        #     self.parent.combo_font.findText(gui.QFontInfo(font).family()))
        # self.parent.combo_size.setCurrentIndex(
        #     self.parent.combo_size.findText(str(font.pointSize())))
        self.parent.styleactiondict["&Bold"].setChecked(font.bold())
        self.parent.styleactiondict["&Italic"].setChecked(font.italic())
        self.parent.styleactiondict["&Underline"].setChecked(font.underline())
        self.parent.styleactiondict["Strike&through"].setChecked(font.strikeOut())
        self.parent.styleactiondict["&Monospace"].setChecked(font.fixedPitch())

    def color_changed(self, col):
        """kleur aanpassen

        het icon in de toolbar krijgt een andere kleur"""
        pix = gui.QPixmap(14, 14)
        pix.fill(col)
        self.parent.styleactiondict["&Color..."].setIcon(gui.QIcon(pix))

    def background_changed(self, col):
        """kleur aanpassen

        het icon in de toolbar krijgt een andere kleur"""
        pix = gui.QPixmap(18, 18)
        pix.fill(col)
        self.parent.styleactiondict["&Background..."].setIcon(gui.QIcon(pix))

    def alignment_changed(self, align):
        """alignment aanpassen

        de van toepassing zijnde menuitems worden aangevinkt
        en de betreffende toolbaricons worden geaccentueerd"""
        self.parent.styleactiondict["Align &Left"].setChecked(False)
        self.parent.styleactiondict["C&enter"].setChecked(False)
        self.parent.styleactiondict["Align &Right"].setChecked(False)
        self.parent.styleactiondict["&Justify"].setChecked(False)
        if align & core.Qt.AlignmentFlag.AlignLeft:
            self.parent.styleactiondict["Align &Left"].setChecked(True)
        elif align & core.Qt.AlignmentFlag.AlignHCenter:
            self.parent.styleactiondict["C&enter"].setChecked(True)
        elif align & core.Qt.AlignmentFlag.AlignRight:
            self.parent.styleactiondict["Align &Right"].setChecked(True)
        elif align & core.Qt.AlignmentFlag.AlignJustify:
            self.parent.styleactiondict["&Justify"].setChecked(True)

    def mergeCurrentCharFormat(self, fmt):
        "de geselecteerde tekst op de juiste manier weergeven"
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(gui.QTextCursor.SelectionType.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        super().mergeCurrentCharFormat(fmt)

    def check_dirty(self):
        "check for modifications"
        return self.document().isModified()

    def mark_dirty(self, value):
        "manually turn modified flag on/off (mainly intended for off)"
        self.document().setModified(value)

    def openup(self, value):
        "make text accessible (or not)"
        self.setReadOnly(not value)

    def focusInEvent(self, *args):
        "reimplemented to correctly set application title"
        self.parent.in_editor = True
        self.parent.master.set_window_title()
        super().focusInEvent(*args)

    def focusOutEvent(self, *args):
        "reimplemented to correctly set application title"
        self.parent.in_editor = False
        self.parent.master.set_window_title()
        super().focusOutEvent(*args)

    def search_from_start(self):
        "start search in textarea"
        self.moveCursor(gui.QTextCursor.MoveOperation.Start)
        ok = self.find(self.parent.master.srchtext, self.parent.set_searchflags())
        if ok:
            self.ensureCursorVisible()
        return ok

    def find_next(self):
        "search forward in textarea"
        if self.find(self.parent.master.srchtext, self.parent.set_searchflags()):
            self.ensureCursorVisible()

    def find_prev(self):
        "search backwards in textarea"
        if self.find(self.parent.master.srchtext, self.parent.set_searchflags(backward=True)):
            self.ensureCursorVisible()

    # no need to reimplement this in this gui version
    # def clear(self):
    #     "empty the editor's contents"
    #     self.editor.clear()


class UndoRedoStack(gui.QUndoStack):
    """Undo stack (subclass overriding some event handlers)
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.cleanChanged.connect(self.clean_changed)
        self.indexChanged.connect(self.index_changed)
        self.setUndoLimit(1)  # self.unset_undo_limit(False)
        win = self.parent()
        win.undo_item.setText('Nothing to undo')
        win.redo_item.setText('Nothing to redo')
        win.undo_item.setDisabled(True)
        win.redo_item.setDisabled(True)

    def clean_changed(self, state):
        """clear text of undo/redo menuitems according to stack change
        """
        win = self.parent()
        if state:
            win.undo_item.setText('Nothing to undo')
            win.redo_item.setText('Nothing to redo')
        win.undo_item.setDisabled(state)

    def index_changed(self, num):
        """change text of undo/redo menuitems according to stack change

        "num" argument is provided by the signal this slot is connected to
        """
        win = self.parent()
        test = self.undoText()
        if test:
            win.undo_item.setText('&Undo ' + test)
            win.undo_item.setEnabled(True)
        else:
            win.undo_item.setText('Nothing to undo')
            win.undo_item.setDisabled(True)
        test = self.redoText()
        if test:
            win.redo_item.setText('&Redo ' + test)
            win.redo_item.setEnabled(True)
        else:
            win.redo_item.setText('Nothing to redo')
            win.redo_item.setDisabled(True)


class AddCommand(gui.QUndoCommand):
    """Nieuwe notitie toevoegen
    """
    def __init__(self, win, root, under, new_title, extra_titles, description='Add'):
        self.win = win
        self.root = root if root is not None else self.win.master.activeitem
        if root == self.win.root:
            description += " top level item"
        self.under = under
        if under:
            self.pos = -1
        else:
            self.pos = self.win.tree.getitemparentpos(self.win.master.activeitem)[1] + 1
        self.add_to_itemdict = [new_title, '']  # , []]
        subel = self.add_to_itemdict  # [2]
        for x in extra_titles:
            new_subel = [x, '']  # , []]
            subel.append(new_subel)
            subel = new_subel  # [2]
        subel.append([])
        self.is_first_edit = not self.win.master.project_dirty
        super().__init__(description)

    def redo(self):
        """actie uitvoeren
        """
        self.data = self.win.master.do_addaction(self.root, self.under, self.pos,
                                                 self.add_to_itemdict)

    def undo(self):
        """actie ongedaan maken
        """
        new_item = self.data
        self.add_to_itemdict = self.win.tree.removeitem(new_item)[2]
        if self.is_first_edit:
            self.win.master.set_project_dirty(False)


class PasteCommand(gui.QUndoCommand):
    """Notitie toevoegen vanuit copy buffer
    """
    def __init__(self, win, before, below, item, description="Paste"):
        self.win = win
        if below:
            description += ' Under'
        elif before:
            description += ' Before'
        else:
            description += ' After'
        self.before = before
        self.below = below
        self.item = item
        super().__init__(description)
        # self.key = int(self.item.text(1))
        # self.title = str(self.item.text(0))
        self.first_edit = not self.win.master.project_dirty
        self.replaced = None    # in case item is replaced while redoing

    def redo(self):
        """actie uitvoeren
        """
        self.views = self.win.master.views  # huidige stand onthouden tbv redo
        self.used_keys, self.used_parent = self.win.master.do_pasteaction(self.before, self.below,
                                                                          self.item)

    def undo(self):
        """actie ongedaan maken
        "essentially 'cut' Command"
        """
        for key in self.used_keys:
            self.win.master.itemdict.pop(key)
        # items weer uit de visual tree halen
        parent, pos = self.used_parent
        if pos == -1:
            pos = parent.childCount() - 1
        parent.takeChild(pos)
        # eventueel andere views weer aanpassen
        self.win.master.views = self.views
        if self.first_edit:
            self.win.master.set_project_dirty(False)
        self.win.statusbar.showMessage(f'{self.text()} undone')


class CopyCommand(gui.QUndoCommand):
    """Notitie in copy buffer halen
    """
    def __init__(self, win, cut, retain, item):
        description = "Copy" if not cut else "Cut" if retain else "Delete"
        super().__init__(description)
        self.undodata = None
        self.win = win
        self.item = item
        # self.key = int(self.item.text(1))
        # self.title = str(self.item.text(0))
        self.first_edit = not self.win.master.project_dirty
        self.cut = cut
        self.retain = retain

    def redo(self):
        """actie uitvoeren
        """
        self.oldstate = self.win.master.opts["ActiveItem"], self.win.master.views
        self.newstate = self.win.master.do_copyaction(self.cut, self.retain, self.item)

    def undo(self):
        """actie ongedaan maken
        """
        # terugzetten in tree en itemdict indien nodig
        copied_items, oldloc, cut_from_itemdict = self.newstate
        if self.cut:
            for key, value in cut_from_itemdict:
                self.win.master.itemdict[key] = value
            parent, pos = oldloc
            newitem = self.win.master.putsubtree(self.win.tree, parent, *copied_items, pos=pos)
            self.win.master.activeitem = self.item = newitem
        self.win.master.opts["ActiveItem"], self.win.master.views = self.oldstate
        if self.first_edit:
            self.win.master.set_project_dirty(False)
        self.win.statusbar.showMessage(f'{self.text()} undone')


class CheckDialog(qtw.QDialog):
    """Generieke dialoog om iets te melden en te vragen of deze melding in het vervolg
    nog getoond moet worden

    Eventueel ook te implementeren d.m.v. QErrorMessage
    """
    def __init__(self, master, parent, title):
        self.master = master
        # self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.nt_icon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        # self.resize(574 + breedte, 480)

    def add_label(self, labeltext):
        """create a text on the screen
        """
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(labeltext, self))
        self.vbox.addLayout(hbox)

    def add_checkbox(self, message):
        """create a checkbox
        """
        hbox = qtw.QHBoxLayout()
        check = qtw.QCheckBox(message, self)
        hbox.addWidget(check)
        self.vbox.addLayout(hbox)
        return check

    def add_ok_buttonbox(self):
        """create a button strip with handlers
        """
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.klaar)
        hbox.addWidget(ok_button)
        hbox.addStretch(1)
        self.vbox.addLayout(hbox)

    def get_checkbox_value(self, check):
        """return the value of a checkbox
        """
        return check.isChecked()

    def klaar(self):
        "dialoog afsluiten"
        self.master.dialog_data = self.master.confirm()
        super().accept()


class OptionsDialog(qtw.QDialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, master, parent, title):
        self.master = master
        # self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.vbox = qtw.QVBoxLayout()
        self.gbox = qtw.QGridLayout()
        self.vbox.addLayout(self.gbox)
        self.setLayout(self.vbox)

    def add_checkbox_line_to_grid(self, row, labeltext, value):
        """create a line to turn an option on/off
        """
        lbl = qtw.QLabel(labeltext, self)
        self.gbox.addWidget(lbl, row, 0)
        chk = qtw.QCheckBox('', self)
        chk.setChecked(value)
        self.gbox.addWidget(chk, row, 1)
        return chk

    def add_buttonbox(self, okvalue, cancelvalue):
        """create a button strip with handlers
        """
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton(okvalue, self)
        ok_button.clicked.connect(self.accept)
        hbox.addWidget(ok_button)
        cancel_button = qtw.QPushButton(cancelvalue, self)
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)
        hbox.addStretch(1)
        self.vbox.addLayout(hbox)

    def get_checkbox_value(self, check):
        """return the value of a checkbox
        """
        return check.isChecked()

    def accept(self):
        """exchange data with caller (overridden event handler)
        """
        self.master.dialog_data = self.master.confirm()
        super().accept()


class SearchDialog(qtw.QDialog):
    """search mode: 0 = current document, 1 = all titles, 2 = all texts
    """
    def __init__(self, master, parent):
        self.master = master
        # self.parent = parent
        ## self.option = option
        super().__init__(parent)
        self.setWindowTitle(parent.title)
        self.setWindowIcon(parent.nt_icon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_label(self, text):
        "zet een vaste tekst op het scherm"
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(text, self))
        self.vbox.addLayout(hbox)

    def add_textentry(self):
        "zet een tekstinvoer veld op het scherm"
        hbox = qtw.QHBoxLayout()
        edit = qtw.QLineEdit(self)
        hbox.addWidget(edit)
        self.vbox.addLayout(hbox)
        return edit

    def build_search_selector(self, searchdefs, callback):
        "zet een selector voor zoeklocatie op het scherm"
        checks = []
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        vbox2 = qtw.QVBoxLayout()
        vbox2.addSpacing(3)
        vbox2.addWidget(qtw.QLabel('In: ', self))
        vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox2 = qtw.QVBoxLayout()
        for text in searchdefs:
            check = qtw.QCheckBox(text, self)
            check.clicked.connect(callback)
            checks.append(check)
            vbox2.addWidget(check)
        hbox.addLayout(vbox2)
        hbox.addStretch()
        self.vbox.addLayout(hbox)
        return checks

    def build_options_selector(self, optiondefs):
        "zet een selector voor zoekmethode op het schem"
        checks = []
        hbox = qtw.QHBoxLayout()
        vbox2 = qtw.QVBoxLayout()
        for text in optiondefs:
            check = qtw.QCheckBox(text, self)
            checks.append(check)
            vbox2.addWidget(check)
        hbox.addLayout(vbox2)
        hbox.addStretch()
        self.vbox.addLayout(hbox)
        return checks

    def add_vertical_space(self, height):
        "voeg verticale witruimte toe"
        self.vbox.addSpacing(height)

    def add_checkbox(self, text):
        "voeg een checkbox toe aan het scherm"
        check = qtw.QCheckBox(text, self)
        self.vbox.addWidget(check)
        return check

    def add_buttons(self):
        "voeg actie knoppen toe aan het scherm"
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.accept)
        hbox.addWidget(ok_button)
        cancel_button = qtw.QPushButton("&Cancel", self)
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)
        hbox.addStretch(1)
        self.vbox.addLayout(hbox)

    def set_checkbox_value(self, cb, value):
        "stel de waarde van een selector in"
        cb.setChecked(value)

    def set_textentry_value(self, text, value):
        "stel de waarde van de tekstinvoer in"
        text.setText(value)

    # def case_sensitive_search(self):
    #     return self.parent.srchflags.value & gui.QTextDocument.FindFlag.FindCaseSensitively.value
    # def search_for_whole_words(self):
    #     return self.parent.srchflags.value & gui.QTextDocument.FindFlag.FindWholeWords.value

    def set_focus_to(self, widget):
        "geef de focus aan een gegeven widget"
        widget.setFocus()

    def set_modechecks(self):
        """stel checkboxen in afhankelijk van gekozen zoekmanier

        bij aanzetten current:
            titel en text uitzetten
            lijst en search backwards deactiveren
        bij aanzetten titel of text:
            current uitzetten
            lijst en search backwards activeren
        """
        this_object = self.sender()
        if this_object.isChecked():
            if this_object == self.master.c_curr:
                self.master.c_titl.setChecked(False)
                self.master.c_text.setChecked(False)
            else:
                self.master.c_curr.setChecked(False)
        self.master.c_lijst.setEnabled(not self.master.c_curr.isChecked())
        # self.master.c_resperdoc.setChecked(self.master.c_text.isChecked())
        # self.master.c_resperdoc.setEnabled(self.master.c_text.isChecked())

    def get_checkbox_value(self, cb):
        "geef de waarde van een gegeven selector terug"
        return cb.isChecked()

    def get_textentry_value(self, text):
        "geeft de waarde van een gegeven tekstinvoer veld terug"
        return text.text()

    def accept(self):
        "haal het dialoogresultaat op en beëindig indien accoord"
        ok = self.master.set_search_parameters()
        if ok:
            super().accept()


class ResultsDialog(qtw.QDialog):
    "Present search results in a non-modal dialog"
    def __init__(self, master, parent):
        self.master = master
        # self.parent = parent
        super().__init__(parent)
        self.setWindowTitle("Search Results")
        self.setWindowIcon(parent.nt_icon)
        # non-modaal maken!
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def set_toptext(self, text):
        "zet toelichting op scherm"
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(text, self))
        self.vbox.addLayout(hbox)

    def add_results_list(self, labels, callback):
        "voeg de resultatenlijst toe aan het scherm"
        hbox = qtw.QHBoxLayout()
        listbox = qtw.QTreeWidget()
        listbox.setColumnCount(len(labels))
        listbox.setHeaderLabels(labels)
        ## self.result_list.setSelectionMode(self.SingleSelection)
        listbox.itemDoubleClicked.connect(callback)
        # self.populate_list()
        hbox.addWidget(listbox)
        self.vbox.addLayout(hbox)
        return listbox

    def add_buttons(self, buttondefs):
        "voeg actie knoppen toe aan het scherm"
        buttons = []
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        for text, callback in buttondefs:
            button = qtw.QPushButton(text, self)
            button.clicked.connect(callback)
            hbox.addWidget(button)
            buttons.append(button)
        hbox.addStretch(1)
        self.vbox.addLayout(hbox)
        return buttons

    def add_item_to_list(self, listbox, loc, root, title):
        "item opbouwen"
        new = qtw.QTreeWidgetItem()
        new.setText(0, root)
        new.setData(0, core.Qt.ItemDataRole.UserRole, loc)
        new.setText(1, title)
        new.setData(1, core.Qt.ItemDataRole.UserRole, loc)
        listbox.addTopLevelItem(new)

    def get_next_item(self, listbox):
        "geef volgende zoekresultaat uit lijst terug"
        return listbox.itemBelow(listbox.currentItem())

    def get_prev_item(self, listbox):
        "geef voorgaande zoekresultaat uit lijst terug"
        return listbox.itemAbove(listbox.currentItem())

    def getselection(self, listbox):
        "geef het geselecteerd item terug"
        return listbox.currentItem()

    def setselection(self, listbox, item):
        "stel het te selecteren item in"
        listbox.setCurrentItem(item)

    def disable_widget(self, widget):
        "maak interactie met een wisget onmogelijk"
        widget.setEnabled(False)

    def enable_button_if_disabled(self, button):
        "maak een onbruikbare knop bruikbaar"
        if not button.isEnabled():
            button.setEnabled(True)

    def get_item_data(self, item):
        "geef de bij een item geassocieerde data terug"
        return item.data(0, core.Qt.ItemDataRole.UserRole)

    def accept(self):
        "sluit dialoog"
        self.master.srchlist = False
        super().accept()

    def reject(self):
        "sluit dialoog"
        self.master.srchlist = False
        super().reject()
