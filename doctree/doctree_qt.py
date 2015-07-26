# -*- coding: utf-8 -*-

"DocTree PyQt specifieke code"

import os
import sys

import PyQt4.QtGui as gui
import PyQt4.QtCore as core

HERE = os.path.dirname(__file__)
from doctree.doctree_shared import Mixin, init_opts, _write, putsubtree

def tabsize(pointsize):
     "pointsize omrekenen in pixels t.b.v. (gemiddelde) tekenbreedte"
     x, y = divmod(pointsize * 8, 10)
     return x * 4 if y < 5 else (x + 1) * 4

class CheckDialog(gui.QDialog):
    """Dialog die kan worden ingesteld om niet nogmaals te tonen

    wordt aangestuurd met de boodschap die in de dialoog moet worden getoond
    """
    def __init__(self, parent, title, message="", option=""):
        self.parent = parent
        self.option = option
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self.parent.nt_icon)
        txt = gui.QLabel(message, self)
        ## show_text = languages[self.parent.opts["language"]]["show_text"]
        show_text = "Deze melding niet meer laten zien"
        self.check = gui.QCheckBox(show_text, self)
        ok_button = gui.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.klaar)

        vbox = gui.QVBoxLayout()

        hbox = gui.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(ok_button)
        hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.check)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        ## self.resize(574 + breedte, 480)

    def klaar(self):
        "dialoog afsluiten"
        if self.check.isChecked():
            self.parent.opts[self.option] = False
        gui.QDialog.done(self, 0)


#
# Undo stack (subclass overriding some event handlers)
#
class UndoRedoStack(gui.QUndoStack):

    def __init__(self, parent):
        ## print('init undostack')
        ## super().__init__(parent)
        gui.QUndoStack.__init__(self, parent)
        self.cleanChanged.connect(self.clean_changed)
        self.indexChanged.connect(self.index_changed)
        self.setUndoLimit(1) # self.unset_undo_limit(False)
        win = self.parent()
        win.undo_item.setText('Nothing to undo')
        win.redo_item.setText('Nothing to redo')
        win.undo_item.setDisabled(True)
        win.redo_item.setDisabled(True)

    def clean_changed(self, state):
        ## print('undo stack status changed:', state)
        win = self.parent()
        if state:
            win.undo_item.setText('Nothing to undo')
        win.undo_item.setDisabled(state)

    def index_changed(self, num):
        ## """change text of undo/redo menuitems according to stack change"""
        ## print('undo stack index changed:', num)
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
class Add_PasteCommand(gui.QUndoCommand):

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


class AddCommand(gui.QUndoCommand):

    def __init__(self, win, root, under, new_title, extra_titles,
            description = 'Add'):
        print('in AddCommand.__init__')
        self.win = win
        self.root = root
        if root == self.win.root:
            description += " top level item"
        self.under = under
        self.new_title = new_title
        self.extra_titles = extra_titles
        self.first_edit = not self.win.project_dirty
        super().__init__(description)

    def redo(self):
        print('in AddCommand.redo')
        self.data = self.win._do_additem(self.root, self.under, self.new_title,
            self.extra_titles)
        # TODO: als ik de undo do na het invullen van tekst raak ik deze kwijt
        #             en kan ik deze dus ook niet terugstoppen

    def undo(self):
        print('in AddCommand.undo')
        newkey, extra_keys, new_item, subitem = self.data
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
        #  de tekst(en) meegeven in ermoveitem helpt daar niet bij

class PasteCommand(gui.QUndoCommand):

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
        print("init {}".format(description), self.item)
        super().__init__(description)
        ## self.parent = item.parent()
        self.key = int(self.item.text(1)) # on the root item this can be the editor
            # contents, but we can't paste the root so we don't have to deal with that
        self.title = str(self.item.text(0))
        self.first_edit = not self.win.project_dirty
        self.replaced = None    # in case item is replaced while redoing

    def redo(self):

        # deze buffers worden hier gebruikt; printen om dat te controleren
        print(self.win.copied_item, # het bovenste item om in de tree te plakken
            self.win.cut_from_itemdict, # de betrokken entries in de itemdict
            self.win.add_node_on_paste) # geeft aan of er nieuwe keys in de dictianary moeten
            # worden gebruikt
        self.views = self.win.views # huidige stand onthouden tbv redo

        # items toevoegen aan itemdict (nieuwe keys of de eerder gebruikte)
        # items toevoegen aan visual tree
        # indien nodig het copied_item in eventuele andere views ook toevoegen
        # afmaken
        self.used_keys, self.used_parent = self.win._do_pasteitem(self.before,
            self.below, self.item)

        # kennelijk wordt self.win.copied_item wel veranderd en wel van
        #    ('drijfsijzen', '14', []) in ('drijfsijzen', 15, [])
        print('kijken of de buffers zijn veranderd:')
        print(self.win.copied_item, self.win.cut_from_itemdict,
            self.win.add_node_on_paste)

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
        for key in self.used_keys:
            self.win.itemdict.pop(key)
        # items weer uit de visual tree halen   / _removeitem
        parent, pos = self.used_parent
        print(parent, pos)
        if pos == -1:
            pos = parent.childCount() - 1
        print('Taking child', pos, 'from parent', parent)
        print(parent.text(0))
        parent.takeChild(pos)
        print('Child taken')
        # eventueel andere views weer aanpassen
        self.win.views = self.views
        ## self.replaced = self.added   # remember original item in case redo replaces it
        ## item = CopyElementCommand(self.win, self.added, cut=True, retain=False,
            ## description="Undo add element")
        ## item.redo()
        if self.first_edit:
            self.win.set_project_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))


class CopyCommand(gui.QUndoCommand):
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
        print("init {}".format(description), self.key, self.item)
        self.cut = cut
        self.retain = retain

    def redo(self):
        data = self.win.itemdict[self.key]
        print('copying item', self.item, 'with key', self.key, 'and data', data)
        self.oldstate = self.win.opts["ActiveItem"], self.win.views
        print('before (re)do: oldstate is', self.win.activeitem,
            self.win.opts["ActiveItem"], self.win.views)
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
        print(' after (re)do: newstate is', self.newstate)

    def undo(self):
        print('Undo copy for', self.item, "with key", self.key)
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
        print(' after undo: newstate is', self.newstate)
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
        print(' after undo: restored old state to', self.win.activeitem,
            self.win.opts["ActiveItem"], self.win.views)

        if self.first_edit:
            self.win.set_project_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))
            ## self.win.tree.setCurrentItem(self.item)

#
# main window components
#
class TreePanel(gui.QTreeWidget):
    "Tree structure depicting the notes organization"
    def __init__(self, parent):
        self.parent = parent
        gui.QTreeWidget.__init__(self)
        self.setColumnCount(2)
        self.hideColumn(1)
        self.setItemHidden(self.headerItem(), True)
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
        ## log('size hint for item {}'.format(h.sizeHint(0)))
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
        gui.QTreeWidget.dropEvent(self, event)
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
        gui.QTreeWidget.mousePressEvent(self, event)

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
        gui.QTreeWidget.mouseReleaseEvent(self, event)

    def keyReleaseEvent(self, event):
        "also for showing a context menu"
        if event.key() == core.Qt.Key_Menu:
            item = self.currentItem()
            self.create_popupmenu(item)
            return
        ## else:
            ## gui.QMainWindow.keyReleaseEvent(self, event)
        gui.QTreeWidget.keyReleaseEvent(self, event)

    def create_popupmenu(self, item):
        menu = gui.QMenu()
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
        new = gui.QTreeWidgetItem()
        new.setText(0, titel.rstrip())
        ## new.setIcon(0, gui.QIcon(os.path.join(HERE, 'icons/empty.png')))
        new.setText(1, str(itemkey))
        new.setToolTip(0, titel.rstrip())
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
        print('in _removeitem', item, cut_from_itemdict)
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
            print(item, item.childCount(), item.child(0))
            if item.childCount() == 0:
                break
            to_remove.append((item, 0)) # er is er altijd maar één
            item = item.child(0)
        for parent, pos in reversed(to_remove):
            parent.takeChild(pos)
        #
        return oldloc, prev

class EditorPanel(gui.QTextEdit):
    "Rich text editor displaying the selected note"

    def __init__(self, parent):
        self.parent = parent
        gui.QTextEdit.__init__(self)
        self.setAcceptRichText(True)
        ## self.setTabChangesFocus(True)
        self.setAutoFormatting(gui.QTextEdit.AutoAll)
        self.currentCharFormatChanged.connect(self.charformat_changed)
        self.cursorPositionChanged.connect(self.cursorposition_changed)
        font = self.currentFont()
        self.setTabStopWidth(tabsize(font.pointSize()))

    def canInsertFromMimeData(self, source):
        if source.hasImage:
            return True
        else:
            return gui.QTextEdit.canInsertFromMimeData(source)

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
            gui.QTextEdit.insertFromMimeData(self, source)

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
        font, ok = gui.QFontDialog.getFont(self.currentFont(), self)
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
        col = gui.QColorDialog.getColor(self.textColor(), self)
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
        col = gui.QColorDialog.getColor(self.textBackgroundColor(), self)
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
        gui.QTextEdit.mergeCurrentCharFormat(self, format)

    def _check_dirty(self):
        "check for modifications"
        return self.document().isModified()

    def _mark_dirty(self, value):
        "manually turn modified flag on/off (mainly intended for off)"
        self.document().setModified(value)

    def _openup(self, value):
        "make text accessible (or not)"
        self.setReadOnly(not value)

class MainWindow(gui.QMainWindow, Mixin):
    """Hoofdscherm van de applicatie"""

    def __init__(self, parent=None, fnaam=""):
        gui.QMainWindow.__init__(self)
        Mixin.__init__(self)
        offset = 40 if os.name != 'posix' else 10
        self.move(offset, offset)
        self.nt_icon = gui.QIcon(os.path.join(HERE, "doctree.xpm"))
        self.tray_icon = gui.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip("Click to revive DocTree")
        self.connect(self.tray_icon, core.SIGNAL('clicked'),
            self.revive) # werkt dit wel?
        self.tray_icon.activated.connect(self.revive)
        self.tray_icon.hide()

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        self.opts = init_opts()
        self.resize(self.opts['ScreenSize'][0], self.opts['ScreenSize'][1]) # 800, 500)
        self.setWindowTitle('DocTree')

        self.actiondict = {}
        menubar = self.menuBar()
        self.splitter = gui.QSplitter(self)
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
                    action = gui.QAction(gui.QIcon(os.path.join(HERE, icon)), label,
                        self)
                    if not toolbar_added:
                        toolbar = self.addToolBar(item)
                        toolbar.setIconSize(core.QSize(16,16))
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
                self.connect(action, core.SIGNAL('triggered()'), handler)
                # action.triggered.connect(handler) werkt hier niet
                if label:
                    menu.addAction(action)
                    self.actiondict[label] = action

    def create_stylestoolbar(self):
        toolbar = self.addToolBar('styles')
        self.combo_font = gui.QFontComboBox(toolbar)
        toolbar.addWidget(self.combo_font)
        self.combo_font.activated[str].connect(self.editor.text_family)
        self.combo_size = gui.QComboBox(toolbar)
        toolbar.addWidget(self.combo_size)
        self.combo_size.setEditable(True)
        db = gui.QFontDatabase()
        self.fontsizes = []
        for size in db.standardSizes():
            self.combo_size.addItem(str(size))
            self.fontsizes.append(str(size))
        self.combo_size.activated[str].connect(self.editor.text_size)
        self.combo_size.setCurrentIndex(self.combo_size.findText(
            str(self.editor.font().pointSize())))

        pix = gui.QPixmap(14, 14)
        pix.fill(core.Qt.black)
        action = gui.QAction(gui.QIcon(pix), "Change text color", self)
        action.triggered.connect(self.editor.text_color)
        toolbar.addAction(action)
        self.actiondict["&Color..."] = action
        pix = gui.QPixmap(14, 14)
        self.setcoloraction_color = core.Qt.magenta
        pix.fill(self.setcoloraction_color)
        action = gui.QAction(gui.QIcon(pix), "Set text color", self)
        action.triggered.connect(self.editor.set_text_color)
        toolbar.addAction(action)
        self.setcolor_action = action

        pix = gui.QPixmap(18, 18)
        pix.fill(core.Qt.white)
        action = gui.QAction(gui.QIcon(pix), "Change background color", self)
        action.triggered.connect(self.editor.background_color)
        toolbar.addAction(action)
        self.actiondict["&Background..."] = action
        pix = gui.QPixmap(18, 18)
        self.setbackgroundcoloraction_color = core.Qt.yellow
        pix.fill(self.setbackgroundcoloraction_color)
        action = gui.QAction(gui.QIcon(pix), "Set background color", self)
        action.triggered.connect(self.editor.set_background_color)
        toolbar.addAction(action)
        self.setbackgroundcolor_action = action

    def show_message(self, text, title):
        gui.QMessageBox.information(self, title, text)

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
            filename = gui.QFileDialog.getSaveFileName(self, title, start, filter)
        else:
            filename = gui.QFileDialog.getOpenFileName(self, title, start, filter)
        ok = True if filename else False
        return ok, filename

    def new(self, evt=None):
        if not Mixin.new(self, evt):
            return
        self.opts["Version"] = "Qt"
        self.resize(self.opts['ScreenSize'][0], self.opts['ScreenSize'][1])
        menuitem_list = [x for x in self.viewmenu.actions()]
        for menuitem in menuitem_list[7:]:
            self.viewmenu.removeAction(menuitem)
        action = gui.QAction('&1 Default', self)
        action.setStatusTip("switch to this view")
        action.setCheckable(True)
        action.triggered.connect(self.select_view)
        self.viewmenu.addAction(action)
        action.setChecked(True)
        self.undo_stack.clear()
        self.root = self.tree.takeTopLevelItem(0)
        self.root = gui.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.root.setText(1, self.opts["RootData"])
        self.tree.addTopLevelItem(self.root)
        self.activeitem = item_to_activate = self.root
        self.editor.set_contents(self.opts["RootData"])
        self.editor.setReadOnly(False)
        self.tree.setFocus()

    def save_needed(self, meld=True, always_check=False):
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
            retval = gui.QMessageBox.question(self, "DocTree",
                "Data changed - save current file before continuing?",
                gui.QMessageBox.Yes | gui.QMessageBox.No | gui.QMessageBox.Cancel,
                defaultButton = gui.QMessageBox.Yes)
            if retval == gui.QMessageBox.Yes:
                self.save(meld=meld)
            if retval == gui.QMessageBox.Cancel:
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
            action = gui.QAction('&{} {}'.format(idx + 1, name), self)
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

    def ok_to_reload(self):
        retval = gui.QMessageBox.question(self, "DocTree", "OK to reload?",
            gui.QMessageBox.Ok | gui.QMessageBox.Cancel,
            defaultButton = gui.QMessageBox.Ok)
        return True if retval == gui.QMessageBox.Ok else False

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
        if event == gui.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage('DocTree', "Click to revive DocTree")
        elif event == gui.QSystemTrayIcon.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    def afsl(self, event=None):
        """applicatie afsluiten"""
        self.close()

    def closeEvent(self, event):
        """applicatie afsluiten"""
        if not self.save_needed(meld=False, always_check=True):
            event.ignore()
        else:
            Mixin.afsl(self)
            event.accept()

    def viewportEvent(self, event):
        if event.Type == gui.QEvent.ToolTip:
            item = self.tree.currentItem()
            gui.QToolTip.ShowText(event.pos, item.toolTip().text(), item)

    def _update_newview(self, new_view):
        "view menu bijwerken n.a.v. toevoeging nieuwe view"
        menuitem_list = [x for x in self.viewmenu.actions()]
        for idx, menuitem in enumerate(menuitem_list[7:]):
            if idx == self.opts["ActiveView"]:
                menuitem.setChecked(False)
        action = gui.QAction('&{} {}'.format(self.viewcount, new_view), self)
        action.setStatusTip("switch to this view")
        action.setCheckable(True)
        action.triggered.connect(self.select_view)
        self.viewmenu.addAction(action)
        action.setChecked(True)

    def _rebuild_root(self):
        "tree leegmaken en root opnieuw neerzetten"
        self.root = self.tree.takeTopLevelItem(0)
        self.root = gui.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.root.setText(1, self.opts["RootData"])
        self.tree.addTopLevelItem(self.root)

    def _get_name(self, caption, title, oldname):
        newname = oldname
        data, ok = gui.QInputDialog.getText(self, title, caption,
            gui.QLineEdit.Normal, oldname)
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
        self.root = gui.QTreeWidgetItem()
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
        retval = gui.QMessageBox.question(self, title, text,
            gui.QMessageBox.Yes | gui.QMessageBox.No,
            defaultButton = gui.QMessageBox.Yes)
        return True if retval == gui.QMessageBox.Yes else False

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

    def _set_next_item(self):
        parent = self.activeitem.parent()
        if parent is not None:
            pos = parent.indexOfChild(self.activeitem)
            if pos < parent.childCount() - 1:
                item = parent.child(pos + 1)
                self.tree.setCurrentItem(item)
                return True

    def _set_prev_item(self):
        parent = self.activeitem.parent()
        if parent is not None:
            pos = parent.indexOfChild(self.activeitem)
            if pos > 0:
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
        print("in qt version's add_item")
        test = self._check_addable()
        if test:
            print("adding item")
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


def main(fnaam):
    app = gui.QApplication(sys.argv)
    if fnaam == '':
        fnaam = 'data/qt_tree.pck'
    main = MainWindow(fnaam=fnaam)
    app.setWindowIcon(main.nt_icon)
    main.show()
    main.project_file = fnaam
    err = main.read()
    if err:
        gui.QMessageBox.information(main, "Error", err, gui.QMessageBox.Ok)
    sys.exit(app.exec_())
