"""DocTree: qt specific stuff
"""
import os
import sys
import PyQt5.QtGui as gui
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as core
import doctree.shared as shared


def show_message(win, text):
    "show a confirmable message"
    qtw.QMessageBox.information(win, "DocTree", text, qtw.QMessageBox.Ok)


def ask_ynquestion(win, text):
    "ask a yes/no answerable question"
    result = qtw.QMessageBox.question(win, "DocTree", text,
                                      qtw.QMessageBox.Yes | qtw.QMessageBox.No)
    return result == qtw.QMessageBox.Yes


def ask_yncquestion(win, text):
    "ask a yes/no answerable question with possibilty to cancel"
    result = qtw.QMessageBox.question(win, "DocTree", text, qtw.QMessageBox.Yes |
                                      qtw.QMessageBox.No | qtw.QMessageBox.Cancel,
                                      defaultButton=qtw.QMessageBox.Yes)
    return result == qtw.QMessageBox.Yes, result == qtw.QMessageBox.Cancel


def get_text(win, caption, oldtext):
    "open a dialog and get text input from the user"
    data, ok = qtw.QInputDialog.getText(win, "DocTree", caption, qtw.QLineEdit.Normal, oldtext)
    newtext = str(data) if ok else oldtext
    return ok, newtext


def get_filename(win, title, start, save=False):
    "routine for selection of filename"
    filter = "Pickle files (*.pck)"
    if save:
        filename = qtw.QFileDialog.getSaveFileName(win, title, start, filter)
    else:
        filename = qtw.QFileDialog.getOpenFileName(win, title, start, filter)
    ok = True if filename[0] else False
    return ok, filename[0]


def show_dialog(win, cls, kwargs=None):
    "show dialog and return if confirmed or rejected"
    if kwargs:
        dlg = cls(win, **kwargs)
    else:
        dlg = cls(win)
    return dlg.exec_() == qtw.QDialog.Accepted


def show_nonmodal(win, cls):
    "show dialog and return to ongoing business"
    cls(win).show()


class CheckDialog(qtw.QDialog):
    """Dialog die kan worden ingesteld om niet nogmaals te tonen

    wordt aangestuurd met de boodschap die in de dialoog moet worden getoond
    """
    def __init__(self, parent, message="", option=""):
        print(message, option)
        self.parent = parent
        self.option = option
        super().__init__(parent)
        self.setWindowTitle('DocTree')
        self.setWindowIcon(self.parent.nt_icon)
        txt = qtw.QLabel(message, self)
        ## show_text = languages[self.parent.opts["language"]]["show_text"]
        show_text = "Deze melding niet meer laten zien"
        self.check = qtw.QCheckBox(show_text, self)
        ok_button = qtw.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.klaar)

        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(ok_button)
        hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.check)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        ## self.resize(574 + breedte, 480)

    def klaar(self):
        "dialoog afsluiten"
        if self.check.isChecked():
            self.parent.master.opts[self.option] = False
        super().done(0)


class OptionsDialog(qtw.QDialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, parent):
        self.parent = parent
        sett2text = shared.get_setttexts(self.parent.master.opts)
        super().__init__(parent)
        self.setWindowTitle('A Propos Settings')
        vbox = qtw.QVBoxLayout()
        self.controls = []

        gbox = qtw.QGridLayout()
        col = 0
        for key, value in self.parent.master.opts.items():
            if key not in sett2text:
                continue
            col += 1
            lbl = qtw.QLabel(sett2text[key], self)
            gbox.addWidget(lbl, col, 0)
            chk = qtw.QCheckBox('', self)
            chk.setChecked(value)
            gbox.addWidget(chk, col, 1)
            self.controls.append((key, chk))
        vbox.addLayout(gbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton("&Apply", self)
        ok_button.clicked.connect(self.accept)
        hbox.addWidget(ok_button)
        cancel_button = qtw.QPushButton("&Close", self)
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def accept(self):
        """overridden event handler
        """
        for keyvalue, control in self.controls:
            self.parent.master.opts[keyvalue] = control.isChecked()
        super().accept()


class SearchDialog(qtw.QDialog):
    """search mode: 0 = current document, 1 = all titles, 2 = all texts
    """
    def __init__(self, parent, mode=0):
        self.parent = parent
        ## self.option = option
        super().__init__(parent)
        self.setWindowTitle(self.parent.title)
        self.setWindowIcon(self.parent.nt_icon)
        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Zoek naar: ', self))
        vbox.addLayout(hbox)

        self.t_zoek = qtw.QLineEdit(self)
        hbox = qtw.QHBoxLayout()
        ## hbox.addStretch()
        hbox.addWidget(self.t_zoek)
        ## hbox.addStretch()
        vbox.addLayout(hbox)

        self.c_titl = qtw.QCheckBox('Alle titels', self)
        self.c_titl.clicked.connect(self.check_modes)
        self.c_text = qtw.QCheckBox('Alle teksten', self)
        self.c_text.clicked.connect(self.check_modes)
        self.c_curr = qtw.QCheckBox('Alleen huidige tekst', self)
        self.c_curr.toggled.connect(self.check_modes)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        vbox2 = qtw.QVBoxLayout()
        vbox2.addSpacing(3)
        vbox2.addWidget(qtw.QLabel('In: ', self))
        vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox2 = qtw.QVBoxLayout()
        vbox2.addWidget(self.c_titl)
        vbox2.addWidget(self.c_text)
        vbox2.addWidget(self.c_curr)
        hbox.addLayout(vbox2)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        self.c_hlett = qtw.QCheckBox('Hoofdlettergevoelig', self)
        self.c_woord = qtw.QCheckBox('Hele woorden', self)
        vbox2 = qtw.QVBoxLayout()
        vbox2.addWidget(self.c_hlett)
        vbox2.addWidget(self.c_woord)
        hbox.addLayout(vbox2)
        hbox.addStretch()
        vbox.addLayout(hbox)

        vbox.addSpacing(5)
        hbox = qtw.QHBoxLayout()
        self.c_wrap = qtw.QCheckBox('Wrap around', self)
        hbox.addWidget(self.c_wrap)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        self.c_lijst = qtw.QCheckBox('Toon lijst met zoekresultaten', self)
        hbox.addWidget(self.c_lijst)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.accept)
        hbox.addWidget(ok_button)
        cancel_button = qtw.QPushButton("&Cancel", self)
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        if mode == 0:
            self.c_curr.setChecked(True)
        elif mode == 1:
            self.c_titl.setChecked(True)
        elif mode == 2:
            self.c_text.setChecked(True)
        if self.parent.srchtext:
            self.t_zoek.setText(self.parent.srchtext)
        if self.parent.srchflags & gui.QTextDocument.FindCaseSensitively:
            self.c_hlett.setChecked(True)
        if self.parent.srchflags & gui.QTextDocument.FindWholeWords:
            self.c_woord.setChecked(True)
        if self.parent.srchlist:
            self.c_lijst.setChecked(True)
        if self.parent.srchwrap:
            self.c_wrap.setChecked(True)
        self.t_zoek.setFocus()

    def check_modes(self):
        """
        bij aanzetten current:
            titel en text uitzetten
            lijst en search backwards deactiveren
        bij aanzetten titel of text:
            current uitzetten
            lijst en search backwards activeren
        """
        if self.sender() == self.c_curr:
            self.c_titl.setChecked(False)
            self.c_text.setChecked(False)
            ## self.c_richt.setEnabled(False)
            self.c_lijst.setEnabled(False)
        else:
            self.c_curr.setChecked(False)
            ## self.c_richt.setEnabled(False) # True)
            self.c_lijst.setEnabled(True)

    def accept(self):
        "afsluiten met bijwerken"
        zoek = self.t_zoek.text()
        if not zoek:
            show_message(self, 'Wel iets te zoeken opgeven')
            return
        mode = 0
        if self.c_titl.isChecked():
            mode += 1
        if self.c_text.isChecked():
            mode += 2
        if not mode and not self.c_curr.isChecked():
            show_message(self, 'Wel een zoek modus kiezen')
            return
        self.parent.srchtext = zoek
        self.parent.srchtype = mode
        flags = gui.QTextDocument.FindFlags()
        ## if self.c_richt.isChecked():
            ## flags |= gui.QTextDocument.FindBackward
        if self.c_hlett.isChecked():
            flags |= gui.QTextDocument.FindCaseSensitively
        if self.c_woord.isChecked():
            flags |= gui.QTextDocument.FindWholeWords
        self.parent.srchflags = flags
        self.parent.srchlist = self.c_lijst.isChecked()
        self.parent.srchwrap = self.c_wrap.isChecked()
        super().accept()


class ResultsDialog(qtw.QDialog):
    "Present search results in a non-modal dialog"
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle("Search Results")
        self.setWindowIcon(self.parent.nt_icon)
        # non-modaal maken!
        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        where = ''
        if self.parent.srchtype & 1:
            where += 'titles'
        if self.parent.srchtype & 2:
            if self.parent.srchtype & 1:
                where += ' and '
            where += 'texts'
        hbox.addWidget(qtw.QLabel('\n'.join((
            "Showing results of searching for `{}` in all {}".format(
                self.parent.srchtext, where),
            "Doubleclick to go to an entry")), self))
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        self.result_list = qtw.QTreeWidget()
        self.result_list.setColumnCount(2)
        self.result_list.setHeaderLabels(('Node Root', 'Node Title'))
        ## self.result_list.setSelectionMode(self.SingleSelection)
        self.result_list.itemDoubleClicked.connect(self.goto_selected)
        self.populate_list()
        hbox.addWidget(self.result_list)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        go_button = qtw.QPushButton("&Goto", self)
        go_button.clicked.connect(self.goto_selected)
        gook_button = qtw.QPushButton("g&Oto and Close", self)
        gook_button.clicked.connect(self.goto_and_close)
        self.next_button = qtw.QPushButton("Goto &Next", self)
        self.next_button.clicked.connect(self.goto_next)
        self.prev_button = qtw.QPushButton("Goto &Previous", self)
        self.prev_button.clicked.connect(self.goto_prev)
        self.prev_button.setEnabled(False)
        ok_button = qtw.QPushButton("&Close", self)
        ok_button.clicked.connect(self.accept)
        hbox.addStretch(1)
        hbox.addWidget(go_button)
        hbox.addWidget(gook_button)
        hbox.addWidget(self.next_button)
        hbox.addWidget(self.prev_button)
        hbox.addWidget(ok_button)
        ## hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.result_list.setCurrentItem(self.result_list.itemAt(0, 0))

    def populate_list(self):
        "zoekresultaten vullen in list"
        def add_item_to_list():
            "item opbouwen"
            new = qtw.QTreeWidgetItem()
            new.setText(0, oldroot)
            new.setData(0, core.Qt.UserRole, oldix)
            new.setText(1, oldtitle)
            new.setData(1, core.Qt.UserRole, oldloc)
            self.result_list.addTopLevelItem(new)
        oldloc, oldtype, oldroot, oldtitle = None, None, '', ''
        for ix, item in enumerate(self.parent.search_results):
            loc, newtype, root, title = item
            if loc != oldloc:
                if oldloc is not None:
                    add_item_to_list()
                in_title = 0
                in_text = 0
            if newtype == 'title':
                in_title += 1
            elif newtype == 'text':
                in_text += 1
            oldloc, oldtype, oldroot, oldtitle = loc, newtype, root, title
            oldix = ix
        add_item_to_list()

    def goto_next(self):
        "sync displays voor zoek volgende"
        new = self.result_list.itemBelow(self.result_list.currentItem())
        if new:
            self.result_list.setCurrentItem(new)
            self.goto_selected()
        else:
            self.next_button.setEnabled(False)
            show_message(self, 'This is the last one')

    def goto_prev(self):
        "sync displays voor zoek vorige"
        new = self.result_list.itemAbove(self.result_list.currentItem())
        if new:
            self.result_list.setCurrentItem(new)
            self.goto_selected()
        else:
            self.prev_button.setEnabled(False)
            show_message(self, 'This is the first one')

    def goto_selected(self):
        "toon geselecteerd zoekresultaat"
        if not self.next_button.isEnabled():
            self.next_button.setEnabled(True)
        if not self.prev_button.isEnabled():
            self.prev_button.setEnabled(True)
        selected = self.result_list.currentItem()
        self.parent.srchno = selected.data(0, core.Qt.UserRole)
        self.parent.go_to_result()

    def goto_and_close(self):
        "toon zoekresultaat en sluit dialoog"
        self.goto_selected()
        self.accept()

    def accept(self):
        "sluit dialoog"
        self.parent.srchlist = False
        super().accept()

    def reject(self):
        "sluit dialoog"
        self.parent.srchlist = False
        super().reject()


class UndoRedoStack(qtw.QUndoStack):
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


class AddCommand(qtw.QUndoCommand):
    """Nieuwe notitie toevoegen
    """
    def __init__(self, win, root, under, new_title, extra_titles,
                 description='Add'):
        # root is self.parent.root in geval van "nieuw item onder root"
        # anders is deze None en moet deze bepaald worden op self.win.item
        shared.log('in AddCommand.__init__')
        self.win = win
        # bepalen root en pos gebeurt eigenlijk in do_additem maar ik heb ze hier al nodig
        self.root = root if root is not None else self.win.master.activeitem
        if root == self.win.root:
            description += " top level item"
        self.under = under
        if under:
            self.pos = -1
        else:
            self.pos = self.win.tree.getitemparentpos(self.win.master.activeitem)[1] + 1
        self.new_title = new_title
        self.extra_titles = extra_titles
        self.first_edit = not self.win.master.project_dirty
        super().__init__(description)

    def redo(self):
        """actie uitvoeren
        """
        shared.log('in AddCommand.redo')
        shared.log("root, under zijn {} ({}) en {}".format(self.root, self.root.text(0),
                                                           self.under))
        self.data = self.win.master.do_additem(self.root, self.under, self.pos,
                                               self.new_title, self.extra_titles)
        # TODO: als ik de undo do na het invullen van tekst raak ik deze kwijt
        #             en kan ik deze dus ook niet terugstoppen

    def undo(self):
        """actie ongedaan maken
        """
        shared.log('in AddCommand.undo')
        newkey, extra_keys, new_item, subitem = self.data
        # TODO: als ik wil dat de eventuele tekstinhoud onthouden wordt
        # dan moet ik volgens mij uitvoeren:
        # self.win.master.activeitem = new_item
        # self.win.master.check_active()
        # maar eigenlijk moet ik dit dan ook uitvoeren voor eventuele via \ toegevoegde extra
        # items
        # en misschien moet ik check_active eigenlijk herdefinieren om niet self.activeitem
        # te controleren maar een meegegeven item - oh dat is al zo - is dit dan nog een issue?
        cut_from_itemdict = [(newkey, self.win.master.itemdict[newkey])]
        for key in extra_keys:
            cut_from_itemdict.append((key, self.win.master.itemdict[key]))
        self.win.tree.removeitem(new_item, cut_from_itemdict)
        for idx, view in enumerate(self.win.master.views):
            if idx != self.win.master.opts["ActiveView"]:
                view.pop()
        if self.first_edit:
            self.win.master.set_project_dirty(False)
        # TODO: als ik de undo do na het invullen van tekst raak ik deze kwijt
        #  de tekst(en) meegeven in removeitem helpt daar niet bij


class PasteCommand(qtw.QUndoCommand):
    """Notitie toevoegen vanuit copy buffer
    """
    def __init__(self, win, before, below, item, description="Paste"):
        self.win = win          # treewidget
        if below:
            description += ' Under'
        elif before:
            description += ' Before'
        else:
            description += ' After'
        self.before = before
        self.below = below
        self.item = item        # where we are now
        shared.log("init {} {}".format(description, self.item))
        super().__init__(description)
        ## self.parent = item.parent()
        self.key = int(self.item.text(1))  # on the root item this can be the editor
        # contents, but we can't paste the root so we don't have to deal with that
        self.title = str(self.item.text(0))
        self.first_edit = not self.win.master.project_dirty
        self.replaced = None    # in case item is replaced while redoing

    def redo(self):
        """actie uitvoeren
        """
        # deze buffers worden hier gebruikt; printen om dat te controleren
        ## print(self.win.copied_item, # het bovenste item om in de tree te plakken
            ## self.win.cut_from_itemdict, # de betrokken entries in de itemdict
            ## self.win.add_node_on_paste) # geeft aan of er nieuwe keys in de dictianary moeten
            ## # worden gebruikt
        shared.log("in paste.redo")
        self.views = self.win.master.views  # huidige stand onthouden tbv redo

        # items toevoegen aan itemdict (nieuwe keys of de eerder gebruikte)
        # items toevoegen aan visual tree
        # indien nodig het copied_item in eventuele andere views ook toevoegen
        # afmaken
        self.used_keys, self.used_parent = self.win.master.do_pasteitem(self.before, self.below,
                                                                        self.item)

        ## # kennelijk wordt self.win.copied_item wel veranderd en wel van
        ## #    ('drijfsijzen', '14', []) in ('drijfsijzen', 15, [])
        ## print('kijken of de buffers zijn veranderd:')
        ## print(self.win.copied_item, self.win.cut_from_itemdict,
            ## self.win.add_node_on_paste)

        ## def zetzeronder(node, data, before=False, below=True):
            ## text, data, children = data
            ## tag, value = data
            ## self.win.item = node
            ## is_attr = False if text.startswith(ELSTART) else True
            ## add_under = self.win._add_item(tag, value, before=before,
                ## below=below, attr=is_attr)
            ## below = True
            ## for item in children:
                ## zetzeronder(add_under, item)
            ## return add_under
        ## self.added = self.win._add_item(self.tag, self.data, before=self.before,
            ## below=self.below)
        ## if self.children is not None:
            ## for item in self.children[0][2]:
                ## zetzeronder(self.added, item)
        ## self.win.tree.expandItem(self.added)

    def undo(self):
        """actie ongedaan maken
        "essentially 'cut' Command"
        """
        # items weer uit itemdict verwijderen
        shared.log("in paste.undo")
        for key in self.used_keys:
            self.win.master.itemdict.pop(key)
        # items weer uit de visual tree halen   / removeitem
        parent, pos = self.used_parent
        ## print(parent, pos)
        if pos == -1:
            pos = parent.childCount() - 1
        shared.log('Taking child {} from parent {} {}'.format(pos, parent, parent.text(0)))
        parent.takeChild(pos)
        # eventueel andere views weer aanpassen
        self.win.master.views = self.views
        ## self.replaced = self.added   # remember original item in case redo replaces it
        ## item = CopyElementCommand(self.win, self.added, cut=True, retain=False,
            ## description="Undo add element")
        ## item.redo()
        if self.first_edit:
            self.win.master.set_project_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))


class CopyCommand(qtw.QUndoCommand):
    """Notitie in copy buffer halen
    """
    def __init__(self, win, cut, retain, item, description=""):
        if cut:
            if retain:
                description = "Cut"
            else:
                description = "Delete"
        else:
            description = "Copy"
        super().__init__(description)
        self.undodata = None
        self.win = win      # treewidget
        self.item = item    # where we are now
        self.key = int(self.item.text(1))  # on the root item this can be the editor
        # contents, but we can't copy the root so we don't have to deal with that
        self.title = str(self.item.text(0))
        self.first_edit = not self.win.master.project_dirty
        self.cut = cut
        self.retain = retain
        shared.log("init {} {} {}i {} {}".format(description, self.key, self.item, self.cut,
                                                 self.retain))

    def redo(self):
        """actie uitvoeren
        """
        data = self.win.master.itemdict[self.key]
        shared.log('in copy.redo for item {} with key {} and data {}'.format(self.item, self.key,
                                                                             data))
        self.oldstate = self.win.master.opts["ActiveItem"], self.win.master.views
        shared.log('before (re)do: oldstate is {} {} {}'.format(
            self.win.master.activeitem, self.win.master.opts["ActiveItem"], self.win.master.views))
        ## def get_children(current):
            ## count = current.childCount()
            ## if count == 0:
                ## return []
            ## for ix in count:
                ## item = current.child(ix)
                ## text, key, data = current.text(0), current.text[1],
                    ## get_children(current)
        ## state['current'] = current.text(0), current.text[1], get_children(current)
        ## print('state is', state)
        self.newstate = self.win.master.do_copyaction(self.cut, self.retain, self.item)
        shared.log(' after (re)do: newstate is {}'.format(self.newstate))

    def undo(self):
        """actie ongedaan maken
        """
        shared.log('Undo copy for {} with key {}'.format(self.item, self.key))
        ## # self.cut_el = None
        ## if self.cut:
            ## item = PasteElementCommand(self.win, self.tag, self.data, self.parent,
                ## before=False, below=True, data = self.undodata,
                ## description="Undo Copy Element")
            ## item.redo() # add_under=add_under, loc=self.loc)
            ## self.item = item.added
        # terugzetten in tree en itemdict indien nodig
        ## copied_item, itemlist = self.tree.getsubtree(current)
        ## cut_from_itemdict = [(int(x), self.itemdict[int(x)]) for x in itemlist]
        copied_items, oldloc, cut_from_itemdict = self.newstate
        shared.log(' in undo: newstate is {}'.format(self.newstate))
        if self.cut:
            shared.log('itemdict terugzetten in redo bij cut, cut_from_itemdict is {}'.format(
                cut_from_itemdict))
            for key, value in cut_from_itemdict:
                self.win.master.itemdict[key] = value
            parent, pos = oldloc
            shared.log('na terugzetten, itemdict is {}'.format(self.win.master.itemdict))
            shared.log('calling tree.putsubtree using parent, *copied_items ({}), pos'.format(
                copied_items))
            newitem = self.win.tree.putsubtree(parent, *copied_items, pos=pos - 1)
            self.win.master.activeitem = self.item = newitem

        ## self.win.copied_item = state['copied_item']
        ## self.win.cut_from_itemdict = state['cut_from_itemdict']
        ## self.win.add_node_on_paste = state['add_node']
        self.win.master.opts["ActiveItem"], self.win.master.views = self.oldstate
        shared.log(' after undo: restored old state to {} {} {}'.format(
            self.win.master.activeitem, self.win.master.opts["ActiveItem"], self.win.master.views))

        if self.first_edit:
            self.win.master.set_project_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))
        ## self.win.tree.setCurrentItem(self.item)


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
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(self.InternalMove)
        self.setDropIndicatorShown(True)
        self.setUniformRowHeights(True)

    def selectionChanged(self, newsel, oldsel):
        """wordt aangeroepen als de selectie gewijzigd is

        de tekst van de oude selectie wordt in de itemdict geactualiseerd
        en die van de nieuwe wordt erin opgezocht en getoond"""
        # helaas zijn newsel en oldsel niet makkelijk om te rekenen naar treeitems
        self.parent.master.check_active()
        item = self.currentItem()
        shared.log('current item is now {} {}'.format(item, item.text(0)))
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
        dropitem = self.itemAt(event.pos())
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
        xc, yc = event.x(), event.y()
        item = self.itemAt(xc, yc)
        if item:
            self.oldparent, self.oldpos = self.getitemparentpos(item)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        "for showing a context menu"
        if event.button() == core.Qt.RightButton:
            xc, yc = event.x(), event.y()
            item = self.itemAt(xc, yc)
            if item:
                self.create_popupmenu(item)
                return
            ## else:
                ## event.ignore()
        ## else:
            ## event.ignore()
        super().mouseReleaseEvent(event)

    def keyReleaseEvent(self, event):
        "also for showing a context menu"
        if event.key() == core.Qt.Key_Menu:
            item = self.currentItem()
            self.create_popupmenu(item)
            return
        ## else:
            ## gui.QMainWindow.keyReleaseEvent(self, event)
        super().keyReleaseEvent(event)

    def create_popupmenu(self, item):
        "also for showing a context menu"
        menu = qtw.QMenu()
        for action in self.parent.notemenu.actions():
            menu.addAction(action)
            if item == self.parent.root and action.text() in ('&Add', '&Delete',
                                                              '&Forward', '&Back'):
                action.setEnabled(False)
        menu.addSeparator()
        for action in self.parent.treemenu.actions():
            menu.addAction(action)
            if item == self.parent.root:
                action.setEnabled(False)
        menu.exec_(self.mapToGlobal(self.visualItemRect(item).center()))
        if item == self.parent.root:
            for action in self.parent.notemenu.actions():
                if item == self.parent.root and action.text() in ('&Add', '&Delete',
                                                                  '&Forward', '&Back'):
                    action.setEnabled(True)
            for action in self.parent.treemenu.actions():
                action.setEnabled(True)

    def add_to_parent(self, itemkey, titel, parent, pos=-1):
        """add item to tree at a given location
        """
        shared.log('in add_to_parent, itemkey is {}, titel is {}, parent is {},'.format(itemkey,
                                                                                        titel,
                                                                                        parent))
        new = qtw.QTreeWidgetItem()
        new.setText(0, titel.rstrip())
        # save plain text on tree item to facilitate search
        # faster that using BeautifulSoup? Also, we don't need the import this way
        doc = gui.QTextDocument()
        shared.log('   itemdict is {}'.format(self.parent.master.itemdict))
        shared.log('   itemkey is {}, {}'.format(itemkey, type(itemkey)))
        doc.setHtml(self.parent.master.itemdict[itemkey][1])
        rawtext = doc.toPlainText()
        new.setData(0, core.Qt.UserRole, rawtext)
        #
        ## new.setIcon(0, gui.QIcon(str(HERE / 'icons/empty.png')))
        new.setText(1, str(itemkey))
        new.setToolTip(0, titel.rstrip())
        shared.log('adding child {} ({}) to parent {} ({}) at pos {}'.format(
            new, new.text(0), parent, parent.text(0), pos))
        if pos == -1:
            parent.addChild(new)
        else:
            parent.insertChild(pos, new)
        return new

    def getitemdata(self, item):
        "titel + data in de visual tree ophalen"
        return item.text(0), self.getitemkey(item)  # str(item.text(1))  # kan integer zijn

    def getitemuserdata(self, item):
        "data in de visual tree ophalen"
        # eigenlijk is dit hetzelfde als item.text(1) - behalve bij het root item ?
        return item.data(0, core.Qt.UserRole)

    def getitemtitle(self, item):
        "alleen titel in de visual tree ophalen"
        return item.text(0)

    def getitemkey(self, item):
        "sleutel voor de itemdict ophalen"
        value = item.text(1)
        shared.log('in tree.getitemkey, type voor omzetten is {}'.format(type(value), always=True))
        try:
            value = int(value)
        except ValueError:  # root item heeft tekst in plaats van itemdict key
            pass
        shared.log('in tree.getitemkey, type na omzetten is {}'.format(type(value), always=True))
        return value

    def setitemtitle(self, item, title):
        "titel (en tooltip instellen)"
        item.setText(0, title)
        item.setToolTip(0, title)

    def setitemtext(self, item, text):
        """Meant to set the text for the root item (goes in same place as the keys
        for the other items)
        """
        item.setText(1, text)

    def getitemkids(self, item):
        "children van item ophalen"
        return [item.child(num) for num in range(item.childCount())]

    def getitemparentpos(self, item):
        "parent en positie van item onder parent bepalen"
        root = item.parent()
        if root:
            pos = root.indexOfChild(item)
        else:
            pos = -1
        return root, pos

    def getselecteditem(self):
        "return first selected item"
        return self.selectedItems()[0]

    def set_item_expanded(self, item):
        "expand a tree item"
        item.setExpanded(True)  # of: self.expandItem(item)

    def set_item_collapsed(self, item):
        "collapse a tree item"
        item.setExpanded(False)  # of: self.collapseItem(item)

    def set_item_selected(self, item):
        "select a tree item"
        self.setCurrentItem(item)

    def get_selected_item(self):
        "return the selected tree item"
        return self.currentItem()

    def removeitem(self, item, cut_from_itemdict):
        "removes current treeitem and returns the previous one"
        shared.log('in removeitem {} {}'.format(item, cut_from_itemdict))
        ## parent = item.parent()               # gui-dependent
        ## pos = parent.indexOfChild(item)
        parent, pos = self.getitemparentpos(item)
        oldloc = (parent, pos)
        if pos - 1 >= 0:
            prev = parent.child(pos - 1)
        else:
            prev = parent
            if prev == self.parent.root:
                prev = parent.child(pos + 1)
        self.parent.master.popitems(item, cut_from_itemdict)
        shared.log('  na popitem: cut_from_itemdict is {}'.format(cut_from_itemdict))
        ## parent.takeChild(pos)
        # bij een undo van een add moeten met " \ " toegevoegde items ook verwijderd worden
        to_remove = [(parent, pos)]
        while True:
            shared.log('{} {} {}'.format(item, item.childCount(), item.child(0)))
            if item.childCount() == 0:
                break
            to_remove.append((item, 0))  # er is er altijd maar één
            item = item.child(0)
        for parent, pos in reversed(to_remove):
            parent.takeChild(pos)
        return oldloc, prev

    def getsubtree(self, item, itemlist=None):
        "return part of the tree structure"
        return shared.getsubtree(self, item, itemlist)

    def putsubtree(self, parent, titel, key, subtree=None, pos=-1):
        "build a new part of the tree"
        shared.log('in TreePanel.putsubtree met parent {}, titel {}, key {} of type {}'.format(
            parent, titel, key, type(key)))
        shared.log('calling shared.putsubtree met parent, titel, key, subtree, pos)')
        return shared.putsubtree(self, parent, titel, key, subtree, pos)


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
        self.setAutoFormatting(qtw.QTextEdit.AutoAll)
        self.currentCharFormatChanged.connect(self.charformat_changed)
        self.cursorPositionChanged.connect(self.cursorposition_changed)
        font = self.currentFont()
        self.setTabStopWidth(tabsize(font.pointSize()))

    def canInsertFromMimeData(self, source):
        "reimplemented"
        if source.hasImage:
            return True
        return super().canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        "reimplemented"
        if source.hasImage():
            image = source.imageData()
            if sys.version < '3':
                image = gui.QImage(image)
            cursor = self.textCursor()
            document = self.document()
            num = self.parent.master.opts['ImageCount']
            num += 1
            self.parent.master.opts['ImageCount'] = num
            ## urlname = '{}_{:05}.png'.format(str(self.parent.project_file), num)
            img = '{}_{:05}.png'.format(self.parent.master.project_file.name, num)
            url = self.parent.master.project_file.parent / img
            image.save(str(url))
            ## urlname = os.path.basename(urlname)  # make name "relative"
            document.addResource(gui.QTextDocument.ImageResource,
            #                      core.QUrl(url.name), image)
                                 core.QUrl(str(url)), image)
            # cursor.insertImage(url.name)
            cursor.insertImage(str(url))
        else:
            super().insertFromMimeData(source)

    def set_contents(self, data):
        "load contents into editor"
        data = data.replace('img src="', 'img src="{}/'.format(
            str(self.parent.master.project_file.parent)))
        self.setHtml(data)
        fmt = gui.QTextCharFormat()
        self.charformat_changed(fmt)
        self.oldtext = data

    def get_contents(self):
        "return contents from editor"
        # update plain text in tree item to facilitate search
        self.parent.tree.currentItem().setData(0, core.Qt.UserRole,
                                               self.toPlainText())
        return self.toHtml().replace('img src="{}/'.format(
            str(self.parent.master.project_file.parent)), 'img src="')

    def get_text_position(self):
        """return where the cursor is positioned in the text
        """
        return self.textCursor().position()

    def set_text_position(self, pos):
        """set where the cursor should appear in the text
        """
        cursor = self.textCursor()
        cursor.setPosition(pos)
        self.setTextCursor(cursor)

    def select_all(self):
        "select complete text"
        self.selectAll()

    def text_bold(self):  # , event=None):
        "selectie vet maken"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        if self.parent.actiondict['&Bold'].isChecked():
            fmt.setFontWeight(gui.QFont.Bold)
        else:
            fmt.setFontWeight(gui.QFont.Normal)
        self.mergeCurrentCharFormat(fmt)

    def text_italic(self):  # , event=None):
        "selectie schuin schrijven"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontItalic(self.parent.actiondict['&Italic'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_underline(self):  # , event=None):
        "selectie onderstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontUnderline(self.parent.actiondict['&Underline'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_strikethrough(self):  # , event=None):
        "selectie doorstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontStrikeOut(self.parent.actiondict['Strike&through'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def align_left(self):  # , event=None):
        "alinea links uitlijnen"
        if not self.hasFocus():
            return
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignLeft | core.Qt.AlignAbsolute)

    def align_center(self):  # , event=None):
        "alinea centreren"
        if not self.hasFocus():
            return
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignHCenter)

    def align_right(self):  # , event=None):
        "alinea rechts uitlijnen"
        if not self.hasFocus():
            return
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignRight | core.Qt.AlignAbsolute)

    def text_justify(self):  # , event=None):
        "alinea aan weerszijden uitlijnen"
        if not self.hasFocus():
            return
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.setAlignment(core.Qt.AlignJustify)

    def indent_more(self):  # , event=None):
        "alinea verder laten inspringen"
        if not self.hasFocus():
            return
        where = self.textCursor().block()
        ## fmt = gui.QTextBlockFormat()
        fmt = where.blockFormat()
        wid = fmt.indent()
        shared.log('indent_more called, current indent is {}'.format(wid))
        fmt.setIndent(wid + 100)
        shared.log('indent_more called, indent aangepast naar {}'.format(fmt.indent()))
        # maar hier is geen merge methode voor, lijkt het...

    def indent_less(self):  # , event=None):
        "alinea minder ver laten inspringen"
        if not self.hasFocus():
            return
        fmt = gui.QTextBlockFormat()
        wid = fmt.indent()
        shared.log('indent_less called, current indent is {}'.format(wid))
        if wid > 100:
            fmt.setIndent(wid - 100)

    def increase_parspacing(self):
        "relay"
        self.OnParagraphSpacingMore()

    def decrease_parspacing(self):
        "relay"
        self.OnParagraphSpacingLess()

    def set_linespacing_10(self):
        "relay"
        self.OnLineSpacingSingle()

    def set_linespacing_15(self):
        "relay"
        self.OnLineSpacingHalf()

    def set_linespacing_20(self):
        "relay"
        self.OnLineSpacingDouble()

    def text_font(self):  # , event=None):
        "lettertype en/of -grootte instellen"
        if not self.hasFocus():
            return
        font, ok = qtw.QFontDialog.getFont(self.currentFont(), self)
        if ok:
            fmt = gui.QTextCharFormat()
            fmt.setFont(font)
            ## pointsize = float(font.pointSize())
            self.setTabStopWidth(tabsize(font.pointSize()))
            self.mergeCurrentCharFormat(fmt)

    def text_family(self, family):
        "lettertype instellen"
        fmt = gui.QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeCurrentCharFormat(fmt)
        self.setFocus()

    def enlarge_text(self):  # , event=None):
        "tekst groter maken"
        size = self.parent.combo_size.currentText()
        indx = self.parent.fontsizes.index(size)
        if indx < len(self.parent.fontsizes) - 1:
            self.text_size(self.parent.fontsizes[indx + 1])

    def shrink_text(self):  # , event=None):
        "tekst kleiner maken"
        size = self.parent.combo_size.currentText()
        indx = self.parent.fontsizes.index(size)
        if indx > 0:
            self.text_size(self.parent.fontsizes[indx - 1])

    def text_size(self, size):
        "lettergrootte instellen"
        pointsize = float(size)
        if pointsize > 0:
            fmt = gui.QTextCharFormat()
            fmt.setFontPointSize(pointsize)
            self.setTabStopWidth(tabsize(pointsize))
            self.mergeCurrentCharFormat(fmt)
            self.setFocus()

    def text_color(self):  # , event=None):
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

    def background_color(self):  # , event=None):
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
        if int(backg.style()) == 0:  # nul betekent transparant
            bgcol = core.Qt.white  # eigenlijk standaardkleur, niet per se wit
        else:
            bgcol = backg.color()
        self.background_changed(bgcol)

    def cursorposition_changed(self):
        "wordt aangeroepen als de cursorpositie gewijzigd is"
        self.alignment_changed(self.alignment())

    def font_changed(self, font):
        """fontgegevens aanpassen

        de selectie in de comboboxen wordt aangepast, de van toepassing zijnde
        menuopties worden aangevinkt, en en de betreffende toolbaricons worden
        geaccentueerd"""
        self.parent.combo_font.setCurrentIndex(
            self.parent.combo_font.findText(gui.QFontInfo(font).family()))
        self.parent.combo_size.setCurrentIndex(
            self.parent.combo_size.findText(str(font.pointSize())))
        self.parent.actiondict["&Bold"].setChecked(font.bold())
        self.parent.actiondict["&Italic"].setChecked(font.italic())
        self.parent.actiondict["&Underline"].setChecked(font.underline())
        self.parent.actiondict["Strike&through"].setChecked(font.strikeOut())

    def color_changed(self, col):
        """kleur aanpassen

        het icon in de toolbar krijgt een andere kleur"""
        pix = gui.QPixmap(14, 14)
        pix.fill(col)
        self.parent.actiondict["&Color..."].setIcon(gui.QIcon(pix))

    def background_changed(self, col):
        """kleur aanpassen

        het icon in de toolbar krijgt een andere kleur"""
        pix = gui.QPixmap(18, 18)
        pix.fill(col)
        self.parent.actiondict["&Background..."].setIcon(gui.QIcon(pix))

    def alignment_changed(self, align):
        """alignment aanpassen

        de van toepassing zijnde menuitems worden aangevinkt
        en de betreffende toolbaricons worden geaccentueerd"""
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        if align & core.Qt.AlignLeft:
            self.parent.actiondict["Align &Left"].setChecked(True)
        elif align & core.Qt.AlignHCenter:
            self.parent.actiondict["C&enter"].setChecked(True)
        elif align & core.Qt.AlignRight:
            self.parent.actiondict["Align &Right"].setChecked(True)
        elif align & core.Qt.AlignJustify:
            self.parent.actiondict["&Justify"].setChecked(True)

    def mergeCurrentCharFormat(self, fmt):
        "de geselecteerde tekst op de juiste manier weergeven"
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(gui.QTextCursor.WordUnderCursor)
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
        self.moveCursor(gui.QTextCursor.Start)
        ok = self.find(self.parent.srchtext, self.parent.srchflags)
        if ok:
            self.ensureCursorVisible()
        return ok

    def find_next(self):
        "search forward in textarea"
        if self.find(self.parent.srchtext,
                     self.parent.srchflags & (gui.QTextDocument.FindCaseSensitively |
                                              gui.QTextDocument.FindWholeWords)):
            self.ensureCursorVisible()

    def find_prev(self):
        "search backwards in textarea"
        if self.find(self.parent.srchtext,
                     self.parent.srchflags | gui.QTextDocument.FindBackward):
            self.ensureCursorVisible()

    # no need to reimplement this in this gui version
    # def clear(self):
    #     "empty the editor's contents"
    #     self.editor.clear()


class MainGui(qtw.QMainWindow):
    "Primary application window (main screen)"
    def __init__(self, master, title):
        self.master = master
        self.title = title
        self.app = qtw.QApplication(sys.argv)
        super().__init__()

    def setup_screen(self):
        "continue after we have a reference to the class"
        offset = 40 if os.name != 'posix' else 10
        self.move(offset, offset)
        self.nt_icon = gui.QIcon(str(shared.HERE / "doctree.xpm"))
        self.app.setWindowIcon(self.nt_icon)
        self.tray_icon = qtw.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip("Click to revive DocTree")
        self.tray_icon.activated.connect(self.revive)
        self.tray_icon.hide()

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        self.resize(self.master.opts['ScreenSize'][0], self.master.opts['ScreenSize'][1])
        self.in_editor = False
        self.setWindowTitle(self.title)

        self.actiondict = {}
        menubar = self.menuBar()
        self.splitter = qtw.QSplitter(self)
        self.setCentralWidget(self.splitter)
        self.tree = TreePanel(self)
        self.splitter.addWidget(self.tree)
        self.editor = EditorPanel(self)
        self.editor.setReadOnly(True)
        self.editor.new_content = True
        self.splitter.addWidget(self.editor)

        self.create_menu(menubar, self.master.get_menu_data())
        self.undo_stack = UndoRedoStack(self)
        self.create_stylestoolbar()

        pix = gui.QPixmap(14, 14)
        pix.fill(self.setcoloraction_color)
        self.setcolor_action.setIcon(gui.QIcon(pix))
        pix = gui.QPixmap(18, 18)
        pix.fill(self.setbackgroundcoloraction_color)
        self.setbackgroundcolor_action.setIcon(gui.QIcon(pix))

        self.srchtext = ''
        self.srchtype = 0
        self.srchflags = gui.QTextDocument.FindFlags()
        self.srchlist = self.srchwrap = False

    def create_menu(self, menubar, menudata):
        """bouw het menu en de meeste toolbars op"""
        for item, data in menudata:
            menu = menubar.addMenu(item)
            toolbar_added = False
            if item == menudata[2][0]:  # "&View":
                self.viewmenu = menu
            elif item == menudata[1][0]:
                self.notemenu = menu
            elif item == menudata[3][0]:
                self.treemenu = menu
            for menudef in data:
                if not menudef:
                    menu.addSeparator()
                    continue
                label, handler, shortcut, icon, info = menudef
                if icon:
                    action = qtw.QAction(gui.QIcon(str(shared.HERE / icon)), label, self)
                    if not toolbar_added:
                        toolbar = self.addToolBar(item)
                        toolbar.setIconSize(core.QSize(16, 16))
                        toolbar_added = True
                    toolbar.addAction(action)
                else:
                    action = qtw.QAction(label, self)
                if item == menudata[3][0]:
                    if label == '&Undo':
                        self.undo_item = action
                    elif label == '&Redo':
                        self.redo_item = action
                if shortcut:
                    action.setShortcuts([x for x in shortcut.split(",")])
                if info.startswith("Check"):
                    action.setCheckable(True)
                    info = info[5:]
                    if info in ('B', 'I', 'U'):
                        font = gui.QFont()
                        if info == 'B':
                            font.setBold(True)
                        elif info == 'I':
                            font.setItalic(True)
                        elif info == 'U':
                            font.setUnderline(True)
                        action.setFont(font)
                        info = ''
                if info:
                    action.setStatusTip(info)
                action.triggered.connect(handler)
                if label:
                    menu.addAction(action)
                    self.actiondict[label] = action

    def create_stylestoolbar(self):
        "build toolbar with buttons to change styles"
        toolbar = self.addToolBar('styles')
        self.combo_font = qtw.QFontComboBox(toolbar)
        toolbar.addWidget(self.combo_font)
        self.combo_font.activated[str].connect(self.editor.text_family)
        ## self.combo_font.activated.connect(self.editor.text_family)
        self.combo_size = qtw.QComboBox(toolbar)
        toolbar.addWidget(self.combo_size)
        self.combo_size.setEditable(True)
        db = gui.QFontDatabase()
        self.fontsizes = []
        for size in db.standardSizes():
            self.combo_size.addItem(str(size))
            self.fontsizes.append(str(size))
        ## self.combo_size.activated[str].connect(self.editor.text_size)
        self.combo_size.activated.connect(self.editor.text_size)
        self.combo_size.setCurrentIndex(self.combo_size.findText(
            str(self.editor.font().pointSize())))

        pix = gui.QPixmap(14, 14)
        pix.fill(core.Qt.black)
        action = qtw.QAction(gui.QIcon(pix), "Change text color", self)
        action.triggered.connect(self.editor.text_color)
        toolbar.addAction(action)
        self.actiondict["&Color..."] = action
        pix = gui.QPixmap(14, 14)
        self.setcoloraction_color = core.Qt.magenta
        pix.fill(self.setcoloraction_color)
        action = qtw.QAction(gui.QIcon(pix), "Set text color", self)
        action.triggered.connect(self.editor.set_text_color)
        toolbar.addAction(action)
        self.setcolor_action = action

        pix = gui.QPixmap(18, 18)
        pix.fill(core.Qt.white)
        action = qtw.QAction(gui.QIcon(pix), "Change background color", self)
        action.triggered.connect(self.editor.background_color)
        toolbar.addAction(action)
        self.actiondict["&Background..."] = action
        pix = gui.QPixmap(18, 18)
        self.setbackgroundcoloraction_color = core.Qt.yellow
        pix.fill(self.setbackgroundcoloraction_color)
        action = qtw.QAction(gui.QIcon(pix), "Set background color", self)
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
        try:
            self.splitter.restoreState(pos)
        except TypeError:
            pass

    def get_splitterpos(self):
        "return the position at which the screen is split"
        return self.splitter.saveState()

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
        self.in_editor = True

    def go(self):
        "start the application's event loop"
        self.show()
        sys.exit(self.app.exec_())

    def close(self):
        """applicatie afsluiten"""
        super().close()

    def closeEvent(self, event):
        "reimplemented event handler"
        if not self.master.save_needed(meld=False):
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
        if event == qtw.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage('DocTree', "Click to revive DocTree")
        elif event == qtw.QSystemTrayIcon.Context:
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
                if gp is not None:
                    pos = gp.indexOfChild(parent)
                    if pos < gp.childCount() - 1:
                        item = gp.child(pos + 1)
                        self.tree.setCurrentItem(item)
                        return True
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
            elif pos > 0:
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
        root.sortChildren(0, core.Qt.AscendingOrder)
        if recursive:
            for num in range(root.childCount()):
                tag = root.child(num)
                self.reorder_items(tag, recursive)

    def rebuild_root(self):
        "tree leegmaken en root opnieuw neerzetten"
        self.root = self.tree.takeTopLevelItem(0)
        self.root = qtw.QTreeWidgetItem()
        self.root.setText(0, self.master.opts["RootTitle"])
        self.root.setText(1, self.master.opts["RootData"])
        self.tree.addTopLevelItem(self.root)
        return self.root

    def clear_viewmenu(self):
        "remove all view actions from viewmenu"
        menuitem_list = [x for x in self.viewmenu.actions()]
        for menuitem in menuitem_list[7:]:
            self.viewmenu.removeAction(menuitem)

    def add_viewmenu_option(self, optiontext):
        "add view action to viewmenu"
        action = qtw.QAction(optiontext, self)
        action.setStatusTip("switch to this view")
        action.setCheckable(True)
        action.triggered.connect(self.master.select_view)
        self.viewmenu.addAction(action)
        return action

    def check_viewmenu_option(self, action=None):
        "check the given view action or determine which one to set"
        if action:
            action.setChecked(True)
            return ''
        sender = self.sender()
        menuitem_list = [x for x in self.viewmenu.actions()]
        for menuitem in menuitem_list[7:]:
            if menuitem == sender:
                newview = sender.text()
                sender.setChecked(True)
            else:
                if menuitem.isChecked():
                    menuitem.setChecked(False)
        return newview

    def uncheck_viewmenu_option(self):
        "uncheck the active viewmenu action"
        menuitem_list = [x for x in self.viewmenu.actions()]
        for idx, menuitem in enumerate(menuitem_list[7:]):
            if idx == self.master.opts["ActiveView"]:
                menuitem.setChecked(False)

    def add_view_to_menu(self, newname):
        "update action text"
        action = self.viewmenu.actions()[self.master.opts["ActiveView"] + 7]
        action.setText('{} {}'.format(str(action.text()).split()[0], newname))

    def check_next_viewmenu_option(self, prev=False):
        "find the currently checked option, uncheck it and check the next/previous one"
        menuitem_list = [x for x in self.viewmenu.actions()][7:]
        if prev:
            menuitem_list.reverse()
        found_item = False
        for menuitem in menuitem_list:
            if menuitem.isChecked():
                found_item = True
                menuitem.setChecked(False)
            elif found_item:
                menuitem.setChecked(True)
                found_item = False
                break
        if found_item:
            menuitem_list[0].setChecked(True)

    def remove_viewmenu_option(self, viewname):
        "find the currently checked option, remove it and check the next one"
        menuitem_list = [x for x in self.viewmenu.actions()]
        removed = False
        item_to_check = None
        for menuitem in menuitem_list[7:]:
            num, naam = str(menuitem.text()).split(None, 1)
            if removed:
                menuitem.setText('&{} {}'.format(int(num[1:]) - 1, naam))
                if not item_to_check:
                    item_to_check = menuitem
            if naam == viewname:
                self.viewmenu.removeAction(menuitem)
                removed = True
                if self.master.opts['ActiveView'] >= int(num[1:]) - 1:
                    self.master.opts['ActiveView'] -= 1
                break
        if not item_to_check:
            item_to_check = menuitem_list[7]
        return item_to_check

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
        ok = doc.find(self.srchtext, options=self.srchflags)
        ## return ok.hasSelection()
        return not ok.isNull()

    def goto_searchresult(self, loc, srchtype):
        "position on found data in text"
        treeitem = self.root
        for x in loc:
            treeitem = treeitem.child(x)
        self.tree.setCurrentItem(treeitem)
        if srchtype == 'text':
            ok = self.editor.find(self.srchtext, self.srchflags)
            if ok:
                self.editor.ensureCursorVisible()
