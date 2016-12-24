# -*- coding: utf-8 -*-

"DocTree PyQt5 specifieke code"

import os
import sys

import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core

HERE = os.path.dirname(__file__)
## from doctree.doctree_shared import Mixin, init_opts, _write, _search, putsubtree
## from doctree.doctree_shared import log
from doctree.doctree_shared import Mixin, init_opts, _write, putsubtree, log

def tabsize(pointsize):
     "pointsize omrekenen in pixels t.b.v. (gemiddelde) tekenbreedte"
     x, y = divmod(pointsize * 8, 10)
     return x * 4 if y < 5 else (x + 1) * 4



class CheckDialog(qtw.QDialog):
    """Dialog die kan worden ingesteld om niet nogmaals te tonen

    wordt aangestuurd met de boodschap die in de dialoog moet worden getoond
    """
    def __init__(self, parent, title, message="", option=""):
        self.parent = parent
        self.option = option
        super().__init__(parent)
        self.setWindowTitle(title)
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
            self.parent.opts[self.option] = False
        super().done(0)


class SearchDialog(qtw.QDialog):
    """search mode: 0 = current document, 1 = all titles, 2 = all texts
    """
    def __init__(self, parent, title='', mode=0):
        self.parent = parent
        if not title:
            title = self.parent.title
        ## self.option = option
        super().__init__(parent)
        self.setWindowTitle(title)
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
        ## self.c_richt = qtw.QCheckBox('Achterwaarts zoeken', self)
        self.c_hlett = qtw.QCheckBox('Hoofdlettergevoelig', self)
        self.c_woord = qtw.QCheckBox('Hele woorden', self)
        vbox2 = qtw.QVBoxLayout()
        ## vbox2.addWidget(self.c_richt)
        vbox2.addWidget(self.c_hlett)
        vbox2.addWidget(self.c_woord)
        hbox.addLayout(vbox2)
        hbox.addStretch()
        vbox.addLayout(hbox)

        vbox.addSpacing(5)
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
        ## if self.parent.srchflags & gui.QTextDocument.FindBackward:
            ## self.c_richt.setChecked(True)
        if self.parent.srchflags & gui.QTextDocument.FindCaseSensitively:
            self.c_hlett.setChecked(True)
        if self.parent.srchflags & gui.QTextDocument.FindWholeWords:
            self.c_woord.setChecked(True)
        if self.parent.srchlist:
            self.c_lijst.setChecked(True)
        self.t_zoek.setFocus()

    def check_modes(self, evt):
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
        pass

    def accept(self):
        zoek = self.t_zoek.text()
        if not zoek:
            self.parent.show_message('Wel iets te zoeken opgeven')
            return
        mode = 0
        if self.c_titl.isChecked():
            mode += 1
        if self.c_text.isChecked():
            mode += 2
        if not mode and not self.c_curr.isChecked():
            self.parent.show_message('Wel een zoek modus kiezen')
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
        super().accept()

class ResultsDialog(qtw.QDialog):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle("Search Results")
        self.setWindowIcon(self.parent.nt_icon)
        # non-modaal maken!
        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel("Now showing: a list of search results"
            " with select & goto possibility in a nonmodal dialog\n"
            "Doubleclick to go to an entry", self))
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
        ok_button = qtw.QPushButton("&Close", self)
        ok_button.clicked.connect(self.accept)
        hbox.addStretch(1)
        hbox.addWidget(go_button)
        hbox.addWidget(gook_button)
        hbox.addWidget(ok_button)
        ## hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def populate_list(self):
        oldloc, oldtype, oldroot, oldtitle = None, None, '', ''
        def add_item_to_list():
            ## result_text = ''
            ## if in_title > 0:
                ## result_text += "title"
            ## if in_title > 1:
                ## result_text += " ({})".format(in_title)
            ## if in_text > 0:
                ## if result_text:
                    ## result_text += ", "
                ## result_text += "text"
            ## if in_text > 1:
                ## result_text += " ({})".format(in_text)
            new = qtw.QTreeWidgetItem()
            ## new.setText(0, str(oldloc))
            new.setText(0, oldroot)
            new.setData(0, core.Qt.UserRole, oldix)
            new.setText(1, oldtitle)
            new.setData(1, core.Qt.UserRole, oldloc)
            ## new.setText(2, result_text.title())
            self.result_list.addTopLevelItem(new)
        for ix, item in enumerate(self.parent.search_results):
            loc, type, root, title = item
            if loc != oldloc:
                if oldloc is not None:
                    add_item_to_list()
                in_title = 0
                in_text = 0
            if type == 'title':
                in_title += 1
            elif type == 'text':
                in_text += 1
            oldloc, oldtype, oldroot, oldtitle = loc, type, root, title
            oldix = ix
        add_item_to_list()

    def goto_selected(self):
        selected = self.result_list.currentItem()
        self.parent.srchno = selected.data(0, core.Qt.UserRole)
        self.parent.go_to_result()

    def goto_and_close(self):
        self.goto_selected()
        super().accept()
#
# Undo stack (subclass overriding some event handlers)
#
class UndoRedoStack(qtw.QUndoStack):

    def __init__(self, parent):
        super().__init__(parent)
        self.cleanChanged.connect(self.clean_changed)
        self.indexChanged.connect(self.index_changed)
        self.setUndoLimit(1) # self.unset_undo_limit(False)
        win = self.parent()
        win.undo_item.setText('Nothing to undo')
        win.redo_item.setText('Nothing to redo')
        win.undo_item.setDisabled(True)
        win.redo_item.setDisabled(True)

    def clean_changed(self, state):
        win = self.parent()
        if state:
            win.undo_item.setText('Nothing to undo')
        win.undo_item.setDisabled(state)

    def index_changed(self, num):
        ## """change text of undo/redo menuitems according to stack change"""
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
#
# UndoCommand subclasses
#
class Add_PasteCommand(qtw.QUndoCommand):

    def __init__(self, win, root, under, description, titles=None, treeitem=None,
            itemdata=None, viewdata=None):
        """treedata is data in the currentview and is structured as:
            (key, nested_list_of_keys)
           dictdata is the concerned entries in itemdict and is structured as:
            [(key, title, text), (key, title, text), ...]
           viewdata is a list of zero or more elements structures like treedata
        """
        # add komt binnen met titles: één of meer die allemaal onder elkaar komen te hangen
        # maar als er al tekst toegevoegd is wil ik dat wel mee krijgen dus zou ik dan in de
        # redo ook een tree item moeten opbouwen met dict keys die tijdens de undo
        # worden opgehaald?
        # paste komt binnen met een bestaande boomstructuur (self.copied_item: opgebouwd
        # als een tuple van titel, key en subtree waarbij de laatste een list is van dit soort tuples),
        # een lijst itemdict items (self.cut_from_itemdict: een list van int(x), self.itemdict[int(x)]
        # tuples) en een indicatie of het om nieuwe of
        # bestaande dict items gaat (self.add_items_on_paste).
        # deze laatste betekent dat de keys wel of niet hergebruikt kunnen worden


class AddCommand(qtw.QUndoCommand):

    def __init__(self, win, root, under, new_title, extra_titles,
            description = 'Add'):
        # root is self.parent.root in geval van "nieuw item onder root"
        # anders is deze None en moet deze bepaald worden op self.win.item
        log('in AddCommand.__init__')
        self.win = win
        self.root = root if root is not None else self.win.activeitem
        if root == self.win.root:
            description += " top level item"
        self.under = under
        if under:
            self.pos = -1
        else:
            self.pos = self.win.tree._getitemparentpos(self.win.activeitem)[1] + 1
        self.new_title = new_title
        self.extra_titles = extra_titles
        self.first_edit = not self.win.project_dirty
        super().__init__(description)

    def redo(self):
        log('in AddCommand.redo')
        log("root, under zijn {} ({}) en {}".format(self.root, self.root.text(0),
            self.under))
        self.data = self.win._do_additem(self.root, self.under, self.pos,
            self.new_title, self.extra_titles)
        # TODO: als ik de undo do na het invullen van tekst raak ik deze kwijt
        #             en kan ik deze dus ook niet terugstoppen

    def undo(self):
        log('in AddCommand.undo')
        newkey, extra_keys, new_item, subitem = self.data
        # TODO: als ik wil dat de eventuele tekstinhoud onthouden wordt
        # dan moet ik volgens mij uitvoeren:
        # self.win.activeitem = new_item
        # self.win.check_active()
        # maar eigenlijk moet ik dit dan ook uitvoeren voor eventuele via \ toegevoegde extra
        # items
        # en misschien moet ik check_active eigenlijk herdefinieren om niet self.activeitem
        # te controleren maar een meegegeven item
        cut_from_itemdict = [(newkey, self.win.itemdict[newkey])]
        for key in extra_keys:
            cut_from_itemdict.append((key, self.win.itemdict[key]))
        self.win.tree._removeitem(new_item, cut_from_itemdict)
        for idx, view in enumerate(self.win.views):
            if idx != self.win.opts["ActiveView"]:
                view.pop()
        if self.first_edit:
            self.win.set_project_dirty(False)
        # TODO: als ik de undo do na het invullen van tekst raak ik deze kwijt
        #  de tekst(en) meegeven in removeitem helpt daar niet bij

class PasteCommand(qtw.QUndoCommand):

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
        log("init {} {}".format(description, self.item))
        super().__init__(description)
        ## self.parent = item.parent()
        self.key = int(self.item.text(1)) # on the root item this can be the editor
            # contents, but we can't paste the root so we don't have to deal with that
        self.title = str(self.item.text(0))
        self.first_edit = not self.win.project_dirty
        self.replaced = None    # in case item is replaced while redoing

    def redo(self):

        # deze buffers worden hier gebruikt; printen om dat te controleren
        ## print(self.win.copied_item, # het bovenste item om in de tree te plakken
            ## self.win.cut_from_itemdict, # de betrokken entries in de itemdict
            ## self.win.add_node_on_paste) # geeft aan of er nieuwe keys in de dictianary moeten
            ## # worden gebruikt
        log("in paste.redo")
        self.views = self.win.views # huidige stand onthouden tbv redo

        # items toevoegen aan itemdict (nieuwe keys of de eerder gebruikte)
        # items toevoegen aan visual tree
        # indien nodig het copied_item in eventuele andere views ook toevoegen
        # afmaken
        self.used_keys, self.used_parent = self.win._do_pasteitem(self.before,
            self.below, self.item)

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
        "essentially 'cut' Command"
        # items weer uit itemdict verwijderen
        log("in paste.undo")
        for key in self.used_keys:
            self.win.itemdict.pop(key)
        # items weer uit de visual tree halen   / _removeitem
        parent, pos = self.used_parent
        ## print(parent, pos)
        if pos == -1:
            pos = parent.childCount() - 1
        log('Taking child {} from parent {} {}'.format(pos, parent, parent.text(0)))
        parent.takeChild(pos)
        # eventueel andere views weer aanpassen
        self.win.views = self.views
        ## self.replaced = self.added   # remember original item in case redo replaces it
        ## item = CopyElementCommand(self.win, self.added, cut=True, retain=False,
            ## description="Undo add element")
        ## item.redo()
        if self.first_edit:
            self.win.set_project_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))


class CopyCommand(qtw.QUndoCommand):
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
        self.key = int(self.item.text(1)) # on the root item this can be the editor
            # contents, but we can't copy the root so we don't have to deal with that
        self.title = str(self.item.text(0))
        self.first_edit = not self.win.project_dirty
        log("init {} {} {}".format(description, self.key, self.item))
        self.cut = cut
        self.retain = retain

    def redo(self):
        data = self.win.itemdict[self.key]
        log('in copy.redo for item {} with key {} and data {}'.format(self.item,
            self.key, data))
        self.oldstate = self.win.opts["ActiveItem"], self.win.views
        log('before (re)do: oldstate is {} {} {}'.format(self.win.activeitem,
            self.win.opts["ActiveItem"], self.win.views))
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
        self.newstate = self.win._do_copyaction(self.cut, self.retain, self.item)
        log(' after (re)do: newstate is {}'.format(self.newstate))

    def undo(self):
        log('Undo copy for {} with key'.format(self.item, self.key))
        ## # self.cut_el = None
        ## if self.cut:
            ## item = PasteElementCommand(self.win, self.tag, self.data, self.parent,
                ## before=False, below=True, data = self.undodata,
                ## description="Undo Copy Element")
            ## item.redo() # add_under=add_under, loc=self.loc)
            ## self.item = item.added
        # terugzetten in tree en itemdict indien nodig
        ## copied_item, itemlist = getsubtree(self.tree, current)
        ## cut_from_itemdict = [(int(x), self.itemdict[int(x)]) for x in itemlist]
        copied_items, oldloc, cut_from_itemdict = self.newstate
        log(' after undo: newstate is {}'.format(self.newstate))
        if self.cut:
            for key, value in cut_from_itemdict:
                self.win.itemdict[key] = value
            parent, pos = oldloc
            newitem = putsubtree(self.win.tree, parent, *copied_items, pos=pos-1)
            self.win.activeitem = self.item = newitem

        ## self.win.copied_item = state['copied_item']
        ## self.win.cut_from_itemdict = state['cut_from_itemdict']
        ## self.win.add_node_on_paste = state['add_node']
        self.win.opts["ActiveItem"], self.win.views = self.oldstate
        log(' after undo: restored old state to {} {} {}'.format(self.win.activeitem,
            self.win.opts["ActiveItem"], self.win.views))

        if self.first_edit:
            self.win.set_project_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))
            ## self.win.tree.setCurrentItem(self.item)

#
# main window components
#
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
        self.parent.check_active()
        h = self.currentItem()
        log('current item is now {} {}'.format(h, h.text(0)))
        self.parent.activate_item(h)

    def dropEvent(self, event):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        deze methode breidt de Treewidget methode uit met wat visuele zaken
        """
        dragitem = self.selectedItems()[0]
        dragparent = dragitem.parent()
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
        self.parent.set_project_dirty(True)
        self.setCurrentItem(dragitem)
        dropitem.setExpanded(True)

    def mousePressEvent(self, event):
        """remember the current parent in preparation for "canceling" a dragmove
        """
        xc, yc = event.x(), event.y()
        item = self.itemAt(xc, yc)
        if item:
            self.oldparent, self.oldpos = self._getitemparentpos(item)
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
        menu = qtw.QMenu()
        for action in self.parent.notemenu.actions():
            act = menu.addAction(action)
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
        """
        """
        new = qtw.QTreeWidgetItem()
        new.setText(0, titel.rstrip())
        # save plain text on tree item to facilitate search
        # faster that using BeautifulSoup? Also, we don't need the import this way
        doc = gui.QTextDocument()
        doc.setHtml(self.parent.itemdict[itemkey][1])
        rawtext = doc.toPlainText()
        new.setData(0, core.Qt.UserRole, rawtext)
        #
        ## new.setIcon(0, gui.QIcon(os.path.join(HERE, 'icons/empty.png')))
        new.setText(1, str(itemkey))
        new.setToolTip(0, titel.rstrip())
        log('adding child {} ({}) to parent {} ({}) at pos {}'.format(new,
            new.text(0), parent, parent.text(0), pos))
        if pos == -1:
            parent.addChild(new)
        else:
            parent.insertChild(pos, new)
        return new

    def _getitemdata(self, item):
        return item.text(0), str(item.text(1)) # kan integer zijn

    def _getitemtitle(self, item):
        "titel in de visual tree ophalen"
        return item.text(0)

    def _getitemkey(self, item):
        "sleutel voor de itemdict ophalen"
        value = item.text(1)
        try:
            value = int(value)
        except ValueError: # root item heeft tekst in plaats van itemdict key
            pass
        return value

    def _setitemtitle(self, item, title):
        item.setText(0, title)
        item.setToolTip(0, title)

    def _setitemtext(self, item, text):
        """Meant to set the text for the root item (goes in same place as the keys
        for the other items)
        """
        item.setText(1, text)

    def _getitemkids(self, item):
        return [item.child(num) for num in range(item.childCount())]

    def _getitemparentpos(self, item):
        root = item.parent()
        if root:
            pos = root.indexOfChild(item)
        else:
            pos = -1
        return root, pos

    def _getselecteditem(self):
        return self.selectedItems()[0] # gui-dependent

    def _removeitem(self, item, cut_from_itemdict):
        "removes current treeitem and returns the previous one"
        log('in _removeitem {} {}'.format(item, cut_from_itemdict))
        parent = item.parent()               # gui-dependent
        pos = parent.indexOfChild(item)
        oldloc = (parent, pos)
        if pos - 1 >= 0:
            prev = parent.child(pos - 1)
        else:
            prev = parent
            if prev == self.parent.root:
                prev = parent.child(pos + 1)
        self.parent._popitems(item, cut_from_itemdict)
        ## parent.takeChild(pos)
        # bij een undo van een add moeten met " \ " toegevoegde items ook verwijderd worden
        to_remove = [(parent, pos)]
        while True:
            log('{} {} {}'.format(item, item.childCount(), item.child(0)))
            if item.childCount() == 0:
                break
            to_remove.append((item, 0)) # er is er altijd maar één
            item = item.child(0)
        for parent, pos in reversed(to_remove):
            parent.takeChild(pos)
        #
        return oldloc, prev

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
        if source.hasImage:
            return True
        else:
            return super().canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        if source.hasImage():
            image = source.imageData()
            if sys.version < '3':
                image = gui.QImage(image)
            cursor = self.textCursor()
            document = self.document()
            num = self.parent.opts['ImageCount']
            num += 1
            self.parent.opts['ImageCount'] = num
            urlname = '{}_{:05}.png'.format(self.parent.project_file,  num)
            ok = image.save(urlname)
            urlname = os.path.basename(urlname) # make name "relative"
            document.addResource(gui.QTextDocument.ImageResource,
                core.QUrl(urlname), image)
            cursor.insertImage(urlname)
        else:
            super().insertFromMimeData(source)

    def set_contents(self, data):
        "load contents into editor"
        data = data.replace('img src="',
            'img src="{}/'.format(os.path.dirname(self.parent.project_file)))
        self.setHtml(data)
        fmt = gui.QTextCharFormat()
        self.charformat_changed(fmt)
        self.oldtext = data

    def get_contents(self):
        "return contents from editor"
        # update plain text in tree item to facilitate search
        self.parent.tree.currentItem().setData(0, core.Qt.UserRole,
            self.toPlainText())
        return self.toHtml().replace('img src="{}/'.format(os.path.dirname(
            self.parent.project_file)), 'img src="')

    def text_bold(self, event=None):
        "selectie vet maken"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        if self.parent.actiondict['&Bold'].isChecked():
            fmt.setFontWeight(gui.QFont.Bold)
        else:
            fmt.setFontWeight(gui.QFont.Normal)
        self.mergeCurrentCharFormat(fmt)

    def text_italic(self, event=None):
        "selectie schuin schrijven"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontItalic(self.parent.actiondict['&Italic'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_underline(self, event=None):
        "selectie onderstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontUnderline(self.parent.actiondict['&Underline'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_strikethrough(self, event=None):
        "selectie doorstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontStrikeOut(self.parent.actiondict['Strike&through'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def align_left(self, event=None):
        "alinea links uitlijnen"
        if not self.hasFocus():
            return
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignLeft | core.Qt.AlignAbsolute)

    def align_center(self, event=None):
        "alinea centreren"
        if not self.hasFocus():
            return
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignHCenter)

    def align_right(self, event=None):
        "alinea rechts uitlijnen"
        if not self.hasFocus():
            return
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignRight | core.Qt.AlignAbsolute)

    def text_justify(self, event=None):
        "alinea aan weerszijden uitlijnen"
        if not self.hasFocus():
            return
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.setAlignment(core.Qt.AlignJustify)

    def indent_more(self, event=None):
        "alinea verder laten inspringen"
        if not self.hasFocus():
            return
        where = self.textCursor().block()
        ## fmt = gui.QTextBlockFormat()
        fmt = where.blockFormat()
        wid = fmt.indent()
        log('indent_more called, current indent is {}'.format(wid))
        fmt.setIndent(wid + 100)
        log('indent_more called, indent aangepast naar {}'.format(fmt.indent()))
        # maar hier is geen merge methode voor, lijkt het...

    def indent_less(self, event=None):
        "alinea minder ver laten inspringen"
        if not self.hasFocus():
            return
        fmt = gui.QTextBlockFormat()
        wid = fmt.indent()
        log('indent_less called, current indent is {}'.format(wid))
        if wid > 100:
            fmt.setIndent(wid - 100)

    def text_font(self, event=None):
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
        fmt.setFontFamily(family);
        self.mergeCurrentCharFormat(fmt)
        self.setFocus()

    def enlarge_text(self, event=None):
        size = self.parent.combo_size.currentText()
        indx = self.parent.fontsizes.index(size)
        if indx < len(self.parent.fontsizes) - 1:
            self.text_size(self.parent.fontsizes[indx + 1])

    def shrink_text(self, event=None):
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

    def text_color(self, event=None):
        "tekstkleur instellen"
        if not self.hasFocus():
            self.parent.show_message("Can't do this outside text field", 'Doctree')
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

    def set_text_color(self, event=None):
        "tekstkleur instellen"
        if not self.hasFocus():
            self.parent.show_message("Can't do this outside text field", 'Doctree')
            return
        col = self.parent.setcoloraction_color
        fmt = gui.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeCurrentCharFormat(fmt)

    def background_color(self, event=None):
        "achtergrondkleur instellen"
        if not self.hasFocus():
            self.parent.show_message("Can't do this outside text field", 'Doctree')
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

    def set_background_color(self, event=None):
        "achtergrondkleur instellen"
        if not self.hasFocus():
            self.parent.show_message("Can't do this outside text field", 'Doctree')
            return
        col = self.parent.setbackgroundcoloraction_color
        fmt = gui.QTextCharFormat()
        fmt.setBackground(col)
        self.mergeCurrentCharFormat(fmt)

    def charformat_changed(self, format):
        "wordt aangeroepen als het tekstformat gewijzigd is"
        self.font_changed(format.font());
        self.color_changed(format.foreground().color())
        backg = format.background()
        if int(backg.style()) == 0: # nul betelkent transparant
            bgcol = core.Qt.white # eigenlijk standaardkleur, niet per se wit
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

    def mergeCurrentCharFormat(self, format):
        "de geselecteerde tekst op de juiste manier weergeven"
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(gui.QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        super().mergeCurrentCharFormat(format)

    def _check_dirty(self):
        "check for modifications"
        return self.document().isModified()

    def _mark_dirty(self, value):
        "manually turn modified flag on/off (mainly intended for off)"
        self.document().setModified(value)

    def _openup(self, value):
        "make text accessible (or not)"
        self.setReadOnly(not value)

class MainWindow(qtw.QMainWindow, Mixin):
    """Hoofdscherm van de applicatie"""

    def __init__(self, parent=None, fnaam=""):
        ## gui.QMainWindow.__init__(self)
        ## Mixin.__init__(self)
        super().__init__()
        offset = 40 if os.name != 'posix' else 10
        self.move(offset, offset)
        self.nt_icon = gui.QIcon(os.path.join(HERE, "doctree.xpm"))
        self.tray_icon = qtw.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip("Click to revive DocTree")
        self.tray_icon.activated.connect(self.revive)
        self.tray_icon.hide()

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        self.opts = init_opts()
        self.resize(self.opts['ScreenSize'][0], self.opts['ScreenSize'][1]) # 800, 500)
        self.title = 'DocTree'
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

        self.create_menu(menubar, self._get_menu_data())
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
        self.srchlist = False

    def change_pane(self, event=None):
        "wissel tussen tree en editor"
        if self.tree.hasFocus():
            self.editor.setFocus()
        elif self.editor.hasFocus():
            self.check_active()
            self.tree.setFocus()

    def create_menu(self, menubar, menudata):
        """bouw het menu en de meeste toolbars op"""
        for item, data in menudata:
            menu = menubar.addMenu(item)
            toolbar_added = False
            if item == menudata[2][0]: # "&View":
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
                    action = qtw.QAction(gui.QIcon(os.path.join(HERE, icon)), label,
                        self)
                    if not toolbar_added:
                        toolbar = self.addToolBar(item)
                        toolbar.setIconSize(core.QSize(16,16))
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
                ## self.connect(action, core.SIGNAL('triggered()'), handler)
                # action.triggered.connect(handler) werkt hier niet
                action.triggered.connect(handler) # voor qt5 toch hopenlijk wel
                if label:
                    menu.addAction(action)
                    self.actiondict[label] = action

    def create_stylestoolbar(self):
        toolbar = self.addToolBar('styles')
        self.combo_font = qtw.QFontComboBox(toolbar)
        toolbar.addWidget(self.combo_font)
        ## self.combo_font.activated[str].connect(self.editor.text_family)
        self.combo_font.activated.connect(self.editor.text_family)
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

    def show_message(self, text, title=''):
        if not title:
            title = self.title
        qtw.QMessageBox.information(self, title, text)

    def show_statusmessage(self, text):
        self.statusbar.showMessage(text)

    def set_title(self):
        """standaard titel updaten"""
        self.setWindowTitle("{}{} (view: {}) - DocTree".format(
            os.path.split(self.project_file)[1],
            '*' if self.project_dirty else '',
            self.opts["ViewNames"][self.opts['ActiveView']]))

    def getfilename(self, title, start, save=False):
        filter = "Pickle files (*.pck)"
        if save:
            filename = qtw.QFileDialog.getSaveFileName(self, title, start, filter)
        else:
            filename = qtw.QFileDialog.getOpenFileName(self, title, start, filter)
        ok = True if filename[0] else False
        return ok, filename[0]

    def new(self, evt=None):
        if not Mixin.new(self, evt):
            return
        self.opts["Version"] = "Qt"
        self.resize(self.opts['ScreenSize'][0], self.opts['ScreenSize'][1])
        menuitem_list = [x for x in self.viewmenu.actions()]
        for menuitem in menuitem_list[7:]:
            self.viewmenu.removeAction(menuitem)
        action = qtw.QAction('&1 Default', self)
        action.setStatusTip("switch to this view")
        action.setCheckable(True)
        action.triggered.connect(self.select_view)
        self.viewmenu.addAction(action)
        action.setChecked(True)
        self.undo_stack.clear()
        self.root = self.tree.takeTopLevelItem(0)
        self.root = qtw.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.root.setText(1, self.opts["RootData"])
        self.tree.addTopLevelItem(self.root)
        self.activeitem = item_to_activate = self.root
        self.editor.set_contents(self.opts["RootData"])
        self.editor.setReadOnly(False)
        self.tree.setFocus()

    def save_needed(self, meld=True, always_check=True):
        """vraag of het bestand opgeslagen moet worden als er iets aan de
        verzameling notities is gewijzigd

        NB de return value hiervan betekent iets anders dan die van de Mixin methode
        Die betekent nl. wat de naam zegt.
        Hier is de vraag gesteld en de gewenste actie ondernomen
        en wil ik alleen nog weten of er gecanceld is (False) of niet (True)
        """
        save_is_needed = Mixin.save_needed(self)
        # bij wisselen van pagina wordt de inhoud indien nodig opgeslagen en weten we
        # of er wat veranderd is. Bij afsluiten hoeft dat nog niet gebeurd te zijn
        # maar willen we toch weten of er iets gewijzigd is
        need_to_save = self.editor._check_dirty() if always_check else False
        if save_is_needed or need_to_save:
            if self.editor.hasFocus():
                self.check_active()
            retval = qtw.QMessageBox.question(self, "DocTree",
                "Data changed - save current file before continuing?",
                qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel,
                defaultButton = qtw.QMessageBox.Yes)
            if retval == qtw.QMessageBox.Yes:
                self.save(meld=meld)
            if retval == qtw.QMessageBox.Cancel:
                return False
        return True

    def _read(self):
        "GUI-specifieke zaken binnen Mixin.read()"
        self.opts["Version"] = "Qt"
        self.resize(self.opts['ScreenSize'][0], self.opts['ScreenSize'][1])
        try:
            self.splitter.restoreState(self.opts['SashPosition'])
        except TypeError:
            pass
        self.activeitem = item_to_activate = None
        self._rebuild_root()
        self.activeitem = item_to_activate = self.root
        self.undo_stack.clear()
        self.editor.set_contents(self.opts["RootData"])
        menuitem_list = [x for x in self.viewmenu.actions()]
        for menuitem in menuitem_list[7:]:
            self.viewmenu.removeAction(menuitem)
        for idx, name in enumerate(self.opts["ViewNames"]):
            action = qtw.QAction('&{} {}'.format(idx + 1, name), self)
            action.setStatusTip("switch to this view")
            action.setCheckable(True)
            action.triggered.connect(self.select_view)
            self.viewmenu.addAction(action)
            if idx == self.opts["ActiveView"]:
                action.setChecked(True)
        ## log('Itemdict items:')
        ## for x, y in self.itemdict.items():
            ## log('  {} ({}): {} ({})'.format(x, type(x), y, type(y)))
        self.tree.setFocus()

    def _finish_read(self, item_to_activate):
        self.root.setExpanded(True)
        try:
            if item_to_activate != self.activeitem:
                self.tree.setCurrentItem(item_to_activate)
        except TypeError:
            pass

    def _finish_add(self, parent, item):
        parent.setExpanded(True)
        self.tree.setCurrentItem(item)
        if item != self.root:
            self.editor.setFocus()

    def _finish_copy(self, prev):
        self.tree.setCurrentItem(prev) # gui-dependent

    def _finish_paste(self, current):
        self.tree.setCurrentItem(current)
        current.setExpanded(True)

    def _finish_rename(self, item, item_to_expand):
        item_to_expand.setExpanded(True)
        self.tree.setCurrentItem(item)
        ## if item != self.root:
            ## self.editor.setFocus()

    def _ok_to_reload(self):
        retval = qtw.QMessageBox.question(self, "DocTree", "OK to reload?",
            qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel,
            defaultButton = gui.QMessageBox.Ok)
        return True if retval == qtw.QMessageBox.Ok else False

    def write(self, meld=True):
        self.opts["ScreenSize"] = self.width(), self.height() # tuple(self.size())
        self.opts["SashPosition"] = self.splitter.saveState()
        Mixin.write(self, meld)

    def hide_me(self, event=None):
        """applicatie verbergen"""
        ## self.confirm(setting="AskBeforeHide", textitem="hide_text")
        hide_text = "\n".join((
            "DocTree gaat nu slapen in de System tray",
            "Er komt een icoontje waarop je kunt klikken om hem weer wakker te maken"
                ))
        self.confirm(setting="AskBeforeHide", textitem=hide_text)
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

    def afsl(self, event=None):
        """applicatie afsluiten"""
        self.close()

    def closeEvent(self, event):
        """applicatie afsluiten"""
        if not self.save_needed(meld=False):
            event.ignore()
        else:
            Mixin.afsl(self)
            event.accept()

    def viewportEvent(self, event):
        if event.Type == core.QEvent.ToolTip:
            item = self.tree.currentItem()
            qtw.QToolTip.ShowText(event.pos, item.toolTip().text(), item)

    def _update_newview(self, new_view):
        "view menu bijwerken n.a.v. toevoeging nieuwe view"
        menuitem_list = [x for x in self.viewmenu.actions()]
        for idx, menuitem in enumerate(menuitem_list[7:]):
            if idx == self.opts["ActiveView"]:
                menuitem.setChecked(False)
        action = qtw.QAction('&{} {}'.format(self.viewcount, new_view), self)
        action.setStatusTip("switch to this view")
        action.setCheckable(True)
        action.triggered.connect(self.select_view)
        self.viewmenu.addAction(action)
        action.setChecked(True)

    def _rebuild_root(self):
        "tree leegmaken en root opnieuw neerzetten"
        self.root = self.tree.takeTopLevelItem(0)
        self.root = qtw.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.root.setText(1, self.opts["RootData"])
        self.tree.addTopLevelItem(self.root)

    def _get_name(self, caption, title, oldname):
        newname = oldname
        data, ok = qtw.QInputDialog.getText(self, title, caption,
            qtw.QLineEdit.Normal, oldname)
        if ok:
            newname = str(data)
        return ok, newname

    def _add_view_to_menu(self, newname):
        action = self.viewmenu.actions()[self.opts["ActiveView"] + 7]
        action.setText('{} {}'.format(str(action.text()).split()[0], newname))

    def _finish_add_view(self, event=None):
        "handles Menu > View > New view"
        self.tree.setCurrentItem(self._tree_item)

    def next_view(self, prev=False):
        """cycle to next view if available (default direction / forward)"""
        if self.viewcount == 1:
            self.show_message("This is the only view", 'Doctree')
            return
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.editor.clear()
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
        if prev:
            self.opts["ActiveView"] -= 1
            if self.opts["ActiveView"] < 0:
                self.opts["ActiveView"] = len(self.opts["ViewNames"]) - 1
        else:
            self.opts["ActiveView"] += 1
            if self.opts["ActiveView"] >= len(self.opts["ViewNames"]):
                self.opts["ActiveView"] = 0
        self.root = self.tree.takeTopLevelItem(0)
        self.root = qtw.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.root.setText(1, self.opts["RootData"])
        self.tree.addTopLevelItem(self.root)
        self.activeitem = self.root
        tree_item = self.viewtotree()
        self.set_title()
        self.tree.setCurrentItem(tree_item)

    def _update_selectedview(self):
        "view menu bijwerken n.a.v. wijzigen view naam"
        sender = self.sender()
        self.editor.clear()
        menuitem_list = [x for x in self.viewmenu.actions()]
        for menuitem in menuitem_list[7:]:
            if menuitem == sender:
                newview = sender.text()
                sender.setChecked(True)
            else:
                if menuitem.isChecked():
                    menuitem.setChecked(False)
        return str(newview).split(None,1)[1]

    def _finish_select_view(self, tree_item):
        self.tree.setCurrentItem(tree_item)

    def _confirm(self, title, text):
        retval = qtw.QMessageBox.question(self, title, text,
            qtw.QMessageBox.Yes | qtw.QMessageBox.No,
            defaultButton = qtw.QMessageBox.Yes)
        return True if retval == qtw.QMessageBox.Yes else False

    def _update_removedview(self):
        "view menu bijwerken n.a.v. verwijderen view"
        menuitem_list = [x for x in self.viewmenu.actions()]
        menuitem_list[self.opts["ActiveView"] + 7].setChecked(True)
        removed = False
        for menuitem in menuitem_list[7:]:
            if removed:
                num, naam = str(menuitem.text()).split(None, 1)
                menuitem.setText('&{} {}'.format(int(num[1:]) - 1, naam))
            if str(menuitem.text()).split(None,1)[1] == viewname:
                self.viewmenu.removeAction(menuitem)
                removed = True
        if self.opts["ActiveView"] == 0:
            menuitem_list[7].setChecked(True)

    def _finish_remove_view(self, item):
        self.tree.setCurrentItem(item)

    ## def _rename_root(self, event=None):
        ## assert self.opts['RootTitle'] == self.root.text(0)
        ## Mixin.rename_root(self, event)
        ## self.root.setText(0, self.opts['RootTitle'])

    def _expand(self, recursive=False):
        "expandeer tree vanaf huidige item"
        def expand_all(item):
            for ix in range(item.childCount()):
                sub = item.child(ix)
                sub.setExpanded(True)
                expand_all(sub)
        item = self.tree.currentItem()
        self.tree.expandItem(item)
        if recursive:
            expand_all(item)

    def _collapse(self, recursive=False):
        "collapse huidige item en daaronder"
        def collapse_all(item):
            for ix in range(item.childCount()):
                sub = item.child(ix)
                collapse_all(sub)
                sub.setExpanded(False)
        item = self.tree.currentItem()
        if recursive:
            collapse_all(item)
        self.tree.collapseItem(item)

    def _reorder_items(self, root, recursive=False):
        "(re)order_items"
        root.sortChildren(0, core.Qt.AscendingOrder)
        if recursive:
            for num in range(root.childCount()):
                tag = root.child(num)
                self._reorder_items(tag, recursive)

    def _set_next_item(self, any_level=False):
        if any_level and self.activeitem.childCount() > 0:
            item = self.activeitem.child(0)
            self.tree.setCurrentItem(item)
            return True
        parent = self.activeitem.parent()
        if parent is not None:
            pos = parent.indexOfChild(self.activeitem)
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

    def _set_prev_item(self, any_level=False):
        def get_prev_child_if_any(item):
            test = item.childCount()
            if test > 0:
                item = get_prev_child_if_any(item.child(test - 1))
            return item
        parent = self.activeitem.parent()
        if parent is not None:
            pos = parent.indexOfChild(self.activeitem)
            if any_level:
                if pos == 0:
                    self.tree.setCurrentItem(parent)
                    return True
                else:
                    item = get_prev_child_if_any(parent.child(pos - 1))
                    self.tree.setCurrentItem(item)
                    return True
            elif pos > 0:
                item = parent.child(pos - 1)
                self.tree.setCurrentItem(item)
                return True

    def confirm(self, setting='', textitem=''):
        if self.opts[setting]:
            dlg = CheckDialog(self, 'Apropos',
                ## message=languages[self.opts["language"]][textitem],
                message=textitem,
                option=setting)
            dlg.exec_()
            # opslaan zonder vragen (en zonder backuppen?)
            _write(self.project_file, self.opts, self.views, self.itemdict)

    def tree_undo(self, event=None):
        self.undo_stack.undo()

    def tree_redo(self, event=None):
        self.undo_stack.redo()

    def add_item(self, event=None, root=None, under=True):
        """nieuw item toevoegen (default: onder het geselecteerde)"""
        log("in qt version's add_item")
        test = self._check_addable()
        if test:
            log("adding item")
            new_title, extra_titles = test
            ## self._do_additem(root, under, new_title, extra_titles) # dit werkt
            command = AddCommand(self, root, under, new_title, extra_titles)
            self.undo_stack.push(command)


    def copy_item(self, evt=None, cut=False, retain=True, to_other_file=None):
        """start copy/cut/delete action

        parameters: cut: remove item from tree (True for cut, delete and move)
                    retain: remember item for pasting (True for cut and copy)
                    other_file:
        """
        test = self._check_copyable(cut, retain, to_other_file)
        if test:
            current = test
            ## self._do_copyaction(cut, retain, current) # to_other_file)
            command = CopyCommand(self, cut, retain, current)
            self.undo_stack.push(command)


    def paste_item(self, evt=None, before=True, below=False):
        "start paste actie"
        test = self._check_pasteable(before, below)
        if test:
            current = test
            ## self._do_pasteitem(before, below, current)
            command = PasteCommand(self, before, below, current)
            self.undo_stack.push(command)

    def _find_in(self, haystack):
        if self.srchflags & 2: pass # case sensitive
        if self.srchflags & 4: pass # whole words
        # simple search for now
        return self.srchtext in haystack

    def _search_from(self, parent, loc=None):
        """recursive search in tree items
        assumes item.text(0) contains title, item.data(0) contains text without format
        result is a list of 3 items:
        - node address in the form of a series of sequence numbers
        - indicatinon of where the string was found
        - title of the itemdict item
        """
        result = []
        if not loc:
            location = []
        else:
            location = loc
        for ix in range(parent.childCount()):
            loc = location + [ix]
            treeitem = parent.child(ix)
            if len(loc) == 1:
                self._root_title = treeitem.text(0)
            title = treeitem.text(0)
            text = treeitem.data(0, core.Qt.UserRole)
            if self.srchtype & 1 and self._find_in(title):
                result.append((loc, 'title',self._root_title, title))
            if self.srchtype & 2 and self._find_in(text):
                result.append((loc, 'text', self._root_title, title))
            test = self._search_from(treeitem, loc)
            if test:
                result.extend(test)
        return result

    def search(self, mode=0):
        dlg = SearchDialog(self, mode=mode)
        if dlg.exec_() != qtw.QDialog.Accepted:
            return
        if self.srchtype == 0:
            self.editor.moveCursor(gui.QTextCursor.Start)
            ok = self.editor.find(self.srchtext, self.srchflags)
            if ok:
                self.editor.ensureCursorVisible()
            else:
                self.show_message('Search string not found')
            return
        if self.srchtype not in (1, 2, 3): # failsafe
            self.show_message('Wrong search type')
            return
        print('start search...')
        # old search assumes view is up-to-date
        ## self.search_results = _search(self.views[self.opts['ActiveView']],
            ## self.itemdict, self.srchtext, self.srchtype, self.srchflags)
        # new search assumes plain text is contained in tree items
        self.search_results = self._search_from(self.root)
        print('searching done')
        if not self.search_results:
            self.show_message('Search string not found')
            return
        if self.srchlist:
            dlg = ResultsDialog(self)
            dlg.show()
        else:
            self.srchno = 0
            self.go_to_result()

    def search_texts(self):
        self.search(mode=2)

    def search_titles(self):
        self.search(mode=1)

    def find_next(self):
        if not self.srchtext:
            return
        if not self.srchtype:
            if self.editor.find(self.srchtext, self.srchflags & (
                    gui.QTextDocument.FindCaseSensitively	|
                    gui.QTextDocument.FindWholeWords)):
                self.editor.ensureCursorVisible()
        else:
            self.srchno += 1
            self.go_to_result()

    def find_prev(self):
        if not self.srchtext:
            return
        if not self.srchtype:
            if self.editor.find(self.srchtext, self.srchflags |
                    gui.QTextDocument.FindBackward):
                self.editor.ensureCursorVisible()
        else:
            self.srchno -= 1
            self.go_to_result()

    def go_to_result(self):
        ## key, loc, type, text = self.search_results[self.srchno]
        loc, type = self.search_results[self.srchno][:2]
        treeitem = self.root
        for x in loc:
            treeitem = treeitem.child(x)
        self.tree.setCurrentItem(treeitem)
        if type == 'text':
            ok = self.editor.find(self.srchtext, self.srchflags)
            if ok:
                self.editor.ensureCursorVisible()


def main(fnaam):
    app = qtw.QApplication(sys.argv)
    if fnaam == '':
        fnaam = 'data/qt_tree.pck'
    main = MainWindow(fnaam=fnaam)
    app.setWindowIcon(main.nt_icon)
    main.show()
    main.project_file = fnaam
    err = main.read()
    if err:
        qtw.QMessageBox.information(main, "Error", err, qtw.QMessageBox.Ok)
    sys.exit(app.exec_())
