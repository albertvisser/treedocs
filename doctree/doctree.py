# -*- coding: utf-8 -*-

"DocTree PyQt versie"

import os
import sys
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
if sys.version[0] < '3':
    import cPickle as pck
else:
    import pickle as pck
import shutil
import pprint
import logging
logging.basicConfig(filename='doctree_qt.log', level=logging.DEBUG,
    format='%(asctime)s %(message)s')
import datetime as dt
HERE = os.path.dirname(__file__)

def log(message):
    "write message to logfile"
    logging.info(message)

def tabsize(pointsize):
     "pointsize omrekenen in pixels t.b.v. (gemiddelde) tekenbreedte"
     x, y = divmod(pointsize * 8, 10)
     return x * 4 if y < 5 else (x + 1) * 4

def getsubtree(item):
    """recursieve functie om de strucuur onder de te verplaatsen data
    te onthouden"""
    titel = item.text(0)
    key = item.text(1)
    log(' getsubtree item {}, {}'.format(titel, key))
    subtree = []
    for num in range(item.childCount()):
        kid = item.child(num)
        subtree.append(getsubtree(kid))
    return titel, key, subtree

def putsubtree(parent, titel, key, subtree=None, pos=-1, add_nodes=None,
        itemdict=None):
    """recursieve functie om de onthouden structuur terug te zetten"""
    if subtree is None:
        subtree = []
    if add_nodes is None:
        add_nodes = []
    if itemdict is None:
        itemdict = {}
    log(' putsubtree item {}, {}, {}, {}, {}'.format(titel, key, subtree, pos,
        add_nodes))
    if add_nodes:
        for key, data in add_nodes:
            itemdict[int(key)] = str(data)
        add_nodes = []
    else:
        newkey = len(itemdict)
        while newkey in itemdict:
            newkey += 1
        itemdict[newkey] = (titel, itemdict[int(key)][1])
    new = gui.QTreeWidgetItem()
    new.setText(0, str(titel))
    new.setText(1, str(key))
    new.setToolTip(0, str(titel))
    if pos == -1:
        parent.addChild(new)
    else:
        parent.insertChild(pos + 1, new)
    for subtitel, subkey, subsubtree in subtree:
        putsubtree(new, subtitel, subkey, subsubtree, itemdict=itemdict)
    return new # , itemdict

class CheckDialog(gui.QDialog):
    """Dialoog om te melden dat de applicatie verborgen gaat worden
    AskBeforeHide bepaalt of deze getoond wordt of niet"""
    def __init__(self, parent):
        self.parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle('DocTree')
        self.setWindowIcon(self.nt_icon)
        txt = gui.QLabel("\n".join((
            "DocTree gaat nu slapen in de System tray",
            "Er komt een icoontje waarop je kunt klikken om hem weer wakker te maken"
                )), self)
        self.check = gui.QCheckBox("Deze melding niet meer laten zien", self)
        ok_button = gui.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.klaar)

        vbox = gui.QVBoxLayout()

        hbox = gui.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.check)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(ok_button)
        hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        ## self.resize(574 + breedte, 480)
        self.exec_()

    def klaar(self):
        "dialoog afsluiten"
        if self.check.isChecked():
            self.parent.opts["AskBeforeHide"] = False
        gui.QDialog.done(self, 0)


class TreePanel(gui.QTreeWidget):
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
        ## log("size hint for row: {}".format(self.sizeHintForRow(0)))
        ## log('uniform row heights: {}'.format(self.uniformRowHeights()))
        ## log('vertical offset {}'.format(self.verticalOffset()))
        ## log('icon size {}'.format(str(self.iconSize())))
        ## self.setIconSize(core.QSize(32,32)) groter maken helpt niet
        self.setUniformRowHeights(True)

    ## def drawRow(self, painter, options, idx):
        ## gui.QTreeWidget.drawRow(self, painter, options, idx)
        ## s = idx.sibling(idx.row(), 0)
        ## if s.isValid():
            ## rect = self.visualRect(s)
            ## print rect.height()
            ## rect.setHeight(30)
            ## painter.setPen(core.Qt.DotLine)
            ## painter.drawRect(rect)

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
        gui.QTreeWidget.dropEvent(self, event)
        self.parent.project_dirty = True
        dropitem = dragitem.parent()
        self.setCurrentItem(dragitem)
        dropitem.setExpanded(True)

class EditorPanel(gui.QTextEdit):
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

    def set_contents(self, data, where='root'):
        "load contents into editor"
        ## try:
            ## self.codec = core.QTextCodec.codecForHtml(str(data))
            ## self.setHtml(self.codec.toUnicode(data))
        ## except TypeError:
            ## log('typeerror on data at: {}'.format(where))
        self.setHtml(data)
        fmt = gui.QTextCharFormat()
        self.charformat_changed(fmt)

    def get_contents(self):
        "return contents from editor"
        return self.toHtml()
        ## data = self.codec.fromUnicode(self.toHtml())
        ## return unicode(data)

    def text_bold(self, event = None):
        "selectie vet maken"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        if self.parent.actiondict['&Bold'].isChecked():
            fmt.setFontWeight(gui.QFont.Bold)
        else:
            fmt.setFontWeight(gui.QFont.Normal)
        self.mergeCurrentCharFormat(fmt)

    def text_italic(self, event = None):
        "selectie schuin schrijven"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontItalic(self.parent.actiondict['&Italic'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_underline(self, event = None):
        "selectie onderstrepen"
        if not self.hasFocus():
            return
        fmt = gui.QTextCharFormat()
        fmt.setFontUnderline(self.parent.actiondict['&Underline'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def align_left(self, event = None):
        "alinea links uitlijnen"
        if not self.hasFocus():
            return
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignLeft | core.Qt.AlignAbsolute)

    def align_center(self, event = None):
        "alinea centreren"
        if not self.hasFocus():
            return
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignHCenter)

    def align_right(self, event = None):
        "alinea rechts uitlijnen"
        if not self.hasFocus():
            return
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignRight | core.Qt.AlignAbsolute)

    def text_justify(self, event = None):
        "alinea aan weerszijden uitlijnen"
        if not self.hasFocus():
            return
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.setAlignment(core.Qt.AlignJustify)

    def indent_more(self, event = None):
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

    def indent_less(self, event = None):
        "alinea minder ver laten inspringen"
        if not self.hasFocus():
            return
        fmt = gui.QTextBlockFormat()
        wid = fmt.indent()
        log('indent_less called, current indent is {}'.format(wid))
        if wid > 100:
            fmt.setIndent(wid - 100)

    def text_font(self, event = None):
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

    def text_size(self, size):
        "lettergrootte instellen"
        pointsize = float(size)
        if pointsize > 0:
            fmt = gui.QTextCharFormat()
            fmt.setFontPointSize(pointsize)
            self.setTabStopWidth(tabsize(pointsize))
            self.mergeCurrentCharFormat(fmt)
            self.setFocus()

    def text_color(self, event = None):
        "tekstkleur instellen"
        if not self.hasFocus():
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

    def set_text_color(self, event = None):
        "tekstkleur instellen"
        if not self.hasFocus():
            return
        col = self.parent.setcoloraction_color
        fmt = gui.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeCurrentCharFormat(fmt)

    def background_color(self, event = None):
        "achtergrondkleur instellen"
        if not self.hasFocus():
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

    def set_background_color(self, event = None):
        "achtergrondkleur instellen"
        if not self.hasFocus():
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

class MainWindow(gui.QMainWindow):
    """Hoofdscherm van de applicatie"""
    def __init__(self, parent=None, fnaam=""):
        self.opts = {
            "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
            "ActiveItem": [0,], "ActiveView": 0, "ViewNames": ["Default",],
            "RootTitle": "MyNotes", "RootData": ""}
        gui.QMainWindow.__init__(self)
        self.nt_icon = gui.QIcon(os.path.join(HERE, "doctree.xpm"))
        self.tray_icon = gui.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip("Click to revive DocTree")
        self.connect(self.tray_icon, core.SIGNAL('clicked'),
            self.revive) # werkt dit wel?
        self.tray_icon.activated.connect(self.revive)
        self.tray_icon.hide()

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

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

        ## splitter.moveSplitter(180, 0)
        self.create_menu(menubar, (
            ("&Main", (
                ("Re&Load", self.reread, 'Ctrl+R', 'icons/filerevert.png', 'Reread .ini file'),
                ("&Open", self.open, 'Ctrl+O', 'icons/fileopen.png', "Choose and open .ini file"),
                ("&Init", self.new, 'Shift+Ctrl+I', 'icons/filenew.png', 'Start a new .ini file'),
                ("&Save", self.save, 'Ctrl+S', 'icons/filesave.png', 'Save .ini file'),
                ("Save as", self.saveas, 'Shift+Ctrl+S', 'icons/filesaveas.png', 'Name and save .ini file'),
                (),
                ("&Root title", self.rename_root, 'Shift+F2', '', 'Rename root'),
                ("Items sorteren", self.order_top, '', '', 'Bovenste niveau sorteren op titel'),
                ("Items recursief sorteren", self.order_all, '', '', 'Alle niveaus sorteren op titel'),
                (),
                ("&Hide", self.hide_me, 'Ctrl+H', '', 'verbergen in system tray'),
                ("Switch pane", self.change_pane, 'Ctrl+Tab', '', 'switch tussen tree en editor'),
                (),
                ("e&Xit", core.SLOT('close()'), 'Ctrl+Q,Escape', 'icons/exit.png', 'Exit program'),
                ), ),
            ("&Note", (
                ("&New", self.add_item, 'Ctrl+N', '', 'Add note (below current level)'),
                ("&Add", self.insert_item, 'Insert', '', 'Add note (after current)'),
                ("New under &Root", self.root_item, 'Shift+Ctrl+N', '', 'Add note (below root)'),
                ("&Delete", self.delete_item, 'Ctrl+D,Delete', '', 'Remove note'),
                (),
                ("Edit &Title", self.rename_item, 'F2', '', 'Rename current note'),
                ("Subitems sorteren", self.order_this, '', '', 'Onderliggend niveau sorteren op titel'),
                ("Subitems recursief sorteren", self.order_lower, '', '', 'Alle onderliggende niveaus sorteren op titel'),
                (),
                ("&Forward", self.next_note, 'Ctrl+PgDown', '', 'View next note'),
                ("&Back", self.prev_note, 'Ctrl+PgUp', '', 'View previous note'),
                ),),
            ("&View", (
                ('&New View', self.add_view, '', '', 'Add an alternative view (tree) to this data'),
                ('&Rename Current View', self.rename_view, '', '', 'Rename the current tree view'),
                ('&Delete Current View', self.remove_view, '', '', 'Remove the current tree view'),
                (),
                ('Next View', self.next_view, 'Ctrl++', '', 'Switch to the next view in the list'),
                ('Prior View', self.prev_view, 'Ctrl+-', '', 'Switch to the previous view in the list'),
                (),
                ), ), # label, handler, shortcut, icon, info
            ('E&dit (Tree)', (
                ## ('&Undo', self.tree.undo,  'Ctrl+Z', 'icons/edit-undo.png', 'Undo last operation'),
                ## ('&Redo', self.tree.redo, 'Ctrl+Y', 'icons/edit-redo.png', 'Redo last undone operation'),
                ## (),
                ('Cu&t', self.cut_item, 'Ctrl+Alt+X', 'icons/treeitem-cut.png', 'Copy the selection and delete from tree'),
                ('&Copy', self.copy_item, 'Ctrl+Alt+C', 'icons/treeitem-copy.png', 'Just copy the selection'),
                ('&Paste', self.paste_item_after, 'Ctrl+Alt+V', 'icons/treeitem-paste.png', 'Paste the copied selection'),
                ## (),
                ## ('Select A&ll', self.tree.selectAll, 'Ctrl+A', "", 'Select the entire tree'),
                ## ("&Clear All (can't undo)", self.tree.clear, '', '', 'Delete the entire tree'),
                ), ),
            ('&Edit (Text)', (
                ('&Undo', self.editor.undo,  'Ctrl+Z', 'icons/edit-undo.png', 'Undo last operation'),
                ('&Redo', self.editor.redo, 'Ctrl+Y', 'icons/edit-redo.png', 'Redo last undone operation'),
                (),
                ('Cu&t', self.editor.cut, 'Ctrl+X', 'icons/edit-cut.png', 'Copy the selection and delete from text'),
                ('&Copy', self.editor.copy, 'Ctrl+C', 'icons/edit-copy.png', 'Just copy the selection'),
                ('&Paste', self.editor.paste, 'Ctrl+V', 'icons/edit-paste.png', 'Paste the copied selection'),
                (),
                ('Select A&ll', self.editor.selectAll, 'Ctrl+A', "", 'Select the entire text'),
                ("&Clear All (can't undo)", self.editor.clear, '', '', 'Delete the entire text'),
                ), ),
            ('&Format', (
                ('&Bold', self.editor.text_bold, 'Ctrl+B', 'icons/format-text-bold.png', 'CheckB'),
                ('&Italic', self.editor.text_italic, 'Ctrl+I', 'icons/format-text-italic.png', 'CheckI'),
                ('&Underline', self.editor.text_underline, 'Ctrl+U', 'icons/format-text-underline.png', 'CheckU'),
                (),
                ('Align &Left', self.editor.align_left, 'Shift+Ctrl+L', 'icons/format-justify-left.png', 'Check'),
                ('C&enter', self.editor.align_center, 'Shift+Ctrl+C', 'icons/format-justify-center.png', 'Check'),
                ('Align &Right', self.editor.align_right, 'Shift+Ctrl+R', 'icons/format-justify-right.png', 'Check'),
                ('&Justify', self.editor.text_justify, 'Shift+Ctrl+J', 'icons/format-justify-fill.png', 'Check'),
                (),
                ## ("Indent &More", self.editor.indent_more, 'Ctrl+]', '', 'Increase indentation'),
                ## ("Indent &Less", self.editor.indent_less, 'Ctrl+[', '', 'Decrease indentation'),
                ## (),
                ## ("Increase Paragraph &Spacing", self.editor.OnParagraphSpacingMore, ''),
                ## ("Decrease &Paragraph Spacing", self.editor.OnParagraphSpacingLess, ''),
                ## (),
                ## ("Normal Line Spacing", self.editor.OnLineSpacingSingle, ''),
                ## ("1.5 Line Spacing", self.editor.OnLineSpacingHalf,''),
                ## ("Double Line Spacing", self.editor.OnLineSpacingDouble, ''),
                ## (),
                ("&Font...", self.editor.text_font, '', '', 'Set/change font'),
                ("&Color...", self.editor.text_color, '', '', 'Set/change colour'),
                ("&Background...", self.editor.background_color, '', '',
                    'Set/change background colour'),
                ), ),
            ("&Help", (
                ("&About", self.info_page, '', '', 'About this application'),
                ("&Keys", self.help_page, 'F1', '', 'Keyboard shortcuts'),
                ), ), )
            )
        self.create_stylestoolbar()
        self.project_dirty = False
        self.add_node_on_paste = False

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
            if item == "&View":
                self.viewmenu = menu
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
        for size in db.standardSizes():
            self.combo_size.addItem(str(size))
        self.combo_size.activated[str].connect(self.editor.text_size)
        self.combo_size.setCurrentIndex(self.combo_size.findText(
            str(self.editor.font().pointSize())))

        pix = gui.QPixmap(14, 14)
        pix.fill(core.Qt.black)
        action = gui.QAction(gui.QIcon(pix), "&Color...", self)
        action.triggered.connect(self.editor.text_color)
        toolbar.addAction(action)
        self.actiondict["&Color..."] = action
        pix = gui.QPixmap(14, 14)
        self.setcoloraction_color = core.Qt.magenta
        pix.fill(self.setcoloraction_color)
        action = gui.QAction(gui.QIcon(pix), "Set text color...", self)
        action.triggered.connect(self.editor.set_text_color)
        toolbar.addAction(action)
        self.setcolor_action = action

        pix = gui.QPixmap(18, 18)
        pix.fill(core.Qt.white)
        action = gui.QAction(gui.QIcon(pix), "&Background...", self)
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

    def set_title(self):
        """standaard titel updaten"""
        self.setWindowTitle("DocTree - {} (view: {})".format(
            os.path.split(self.project_file)[1],
            self.opts["ViewNames"][self.opts['ActiveView']]))

    def open(self, event = None):
        "afhandelen Menu > Open / Ctrl-O"
        self.save_needed()
        dirname = os.path.dirname(self.project_file)
        filename = gui.QFileDialog.getOpenFileName(self, "DocTree - choose file to open",
                    dirname, "INI files (*.ini)")
        if filename:
            self.project_file = str(filename)
            err = self.read()
            if err:
                gui.QMessageBox.information(self, "Error", err, gui.QMessageBox.Ok)
            self.statusbar.showMessage('{} opgehaald'.format(self.project_file))

    def new(self, event = None):
        "Afhandelen Menu - Init / Ctrl-I"
        ret = self.save_needed()
        if ret == gui.QMessageBox.Cancel:
            return
        dirname = os.path.dirname(self.project_file)
        filename = gui.QFileDialog.getSaveFileName(self, "DocTree - enter name for new file",
            dirname, "INI files (*.ini)")
        if not filename:
            return
        self.project_file = str(filename)
        self.views = [[],]
        self.viewcount = 1
        self.itemdict = {}
        self.opts = {
            "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
            "ActiveItem": [0,], "ActiveView": 0, "ViewNames": ["Default",],
            "RootTitle": "MyNotes", "RootData": ""}
        self.has_treedata = True
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
        self.root = self.tree.takeTopLevelItem(0)
        self.root = gui.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.root.setText(1, self.opts["RootData"])
        self.tree.addTopLevelItem(self.root)
        self.activeitem = item_to_activate = self.root
        self.editor.set_contents(self.opts["RootData"])
        self.editor.setReadOnly(False)
        self.set_title()
        self.project_dirty = False
        self.tree.setFocus()

    def save_needed(self, meld=True):
        """vraag of het bestand opgeslagen moet worden als er iets aan de
        verzameling notities is gewijzigd"""
        if not self.has_treedata:
            return
        if self.editor.hasFocus():
            self.check_active()
        if self.project_dirty:
            retval = gui.QMessageBox.question(self, "DocTree",
                "Data changed - save current file before continuing?",
                gui.QMessageBox.Yes | gui.QMessageBox.No | gui.QMessageBox.Cancel,
                defaultButton = gui.QMessageBox.Yes)
            if retval == gui.QMessageBox.Yes:
                self.save(meld=meld)
            return retval

    def treetoview(self):
        """zet de visuele tree om in een tree om op te slaan"""
        def lees_item(item):
            """recursieve functie om de data in een pickle-bare structuur om te zetten"""
            textref = int(item.text(1))
            if item == self.activeitem:
                self.opts["ActiveItem"][self.opts["ActiveView"]] = textref
            kids = []
            for num in range(item.childCount()):
                kids.append(lees_item(item.child(num)))
            return textref, kids
        data = []
        for num in range(self.root.childCount()):
            data.append(lees_item(self.root.child(num)))
        return data

    def viewtotree(self):
        """zet de geselecteerde view om in een visuele tree"""
        def maak_item(parent, item, children = None):
            """recursieve functie om de TreeCtrl op te bouwen vanuit de opgeslagen data"""
            item_to_activate = None
            if children is None:
                children = []
            titel, tekst = self.itemdict[item]
            tree_item = gui.QTreeWidgetItem()
            tree_item.setText(0, titel.rstrip())
            ## tree_item.setIcon(0, gui.QIcon(os.path.join(HERE, 'icons/empty.png')))
            tree_item.setText(1, str(item))
            tree_item.setToolTip(0, titel.rstrip())
            parent.addChild(tree_item)
            if item == self.opts["ActiveItem"][self.opts['ActiveView']]:
                item_to_activate = tree_item
            for child in children:
                x, y = maak_item(tree_item, *child)
                if y is not None:
                    item_to_activate = y
            return item, item_to_activate
        item_to_activate = 0
        current_view = self.views[self.opts['ActiveView']]
        for item in current_view:
            x, y = maak_item(self.root, *item)
            if y is not None:
                item_to_activate = y
        return item_to_activate

    def read(self):
        """settings dictionary lezen, opgeslagen data omzetten naar tree"""
        self.has_treedata = False
        self.opts = {
            "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
            "ActiveItem": [0,], "ActiveView": 0, "ViewNames": ["Default",],
            "RootTitle": "MyNotes", "RootData": ""}
        mld = ''
        try:
            f_in = open(self.project_file, "rb")
        except IOError:
            return "couldn't open {}".format(self.project_file)
        try:
            nt_data = pck.load(f_in)
        except EOFError:
            mld = "couldn't load data from {}".format(self.project_file)
        finally:
            f_in.close()
        if mld:
            return mld
        try:
            test = nt_data[0]["AskBeforeHide"]
        except (ValueError, KeyError):
            return "{} is not a valid Doctree data file".format(self.project_file)
        for key, value in nt_data[0].items():
            if key == 'RootData' and value is None:
                value = ""
            self.opts[key] = value
        try:
            self.views = list(nt_data[1])
        except KeyError:
            self.views = [[],]
        self.viewcount = len(self.views)
        try:
            self.itemdict = nt_data[2]
        except KeyError:
            self.itemdict = {}
        self.resize(self.opts['ScreenSize'][0], self.opts['ScreenSize'][1])
        try:
            self.splitter.restoreState(self.opts['SashPosition'])
        except TypeError:
            pass
        self.root = self.tree.takeTopLevelItem(0)
        self.root = gui.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.root.setText(1, self.opts["RootData"])
        self.tree.addTopLevelItem(self.root)
        self.activeitem = item_to_activate = self.root
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
        item_to_activate = self.viewtotree()
        self.has_treedata = True
        self.root.setExpanded(True)
        if item_to_activate != self.activeitem:
            self.tree.setCurrentItem(item_to_activate)
        self.set_title()
        self.project_dirty = False

    def reread(self, event = None):
        """afhandelen Menu > Reload (Ctrl-R)"""
        retval = gui.QMessageBox.question(self, "DocTree", "OK to reload?",
            gui.QMessageBox.Ok | gui.QMessageBox.Cancel,
            defaultButton = gui.QMessageBox.Ok)
        if retval == gui.QMessageBox.Ok:
            self.read()

    def save(self, event = None, meld = True):
        """afhandelen Menu > save"""
        if self.project_file:
            self.write(meld = meld)
        else:
            self.saveas()
        self.statusbar.showMessage('{} opgeslagen'.format(self.project_file))

    def write(self, event = None, meld = True):
        """settings en tree data in een structuur omzetten en opslaan"""
        self.check_active()
        self.opts["ScreenSize"] = self.width(), self.height() # tuple(self.size())
        self.opts["SashPosition"] = self.splitter.saveState()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        nt_data = {0: self.opts, 1: self.views, 2: self.itemdict}
        try:
            shutil.copyfile(self.project_file, self.project_file + ".bak")
        except IOError:
            pass
        f_out = open(self.project_file,"wb")
        pck.dump(nt_data, f_out, protocol=2)
        f_out.close()
        self.project_dirty = False
        if meld:
            gui.QMessageBox.information(self, "DocTool",
                self.project_file + " is opgeslagen", gui.QMessageBox.Ok)

    def saveas(self, event = None):
        """afhandelen Menu > Save As"""
        dirname = os.path.dirname(self.project_file)
        filename = gui.QFileDialog.getSaveFileName(self, "DocTree - save file as:",
            dirname, "INI files (*.ini)")
        if filename:
            self.project_file = str(filename)
            self.write()
            self.set_title()

    def hide_me(self, event = None):
        """applicatie verbergen"""
        if self.opts["AskBeforeHide"]:
            dlg = CheckDialog(self)
        self.tray_icon.show()
        self.hide()

    def revive(self, event = None):
        """applicatie weer zichtbaar maken"""
        if event == gui.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage('DocTree', "Click to revive DocTree")
        elif event == gui.QSystemTrayIcon.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    ## def afsl(self, event = None):
    def closeEvent(self,event):
        """applicatie afsluiten"""
        ret = self.save_needed(meld=False)
        if ret == gui.QMessageBox.Cancel:
            event.ignore()
        else:
            event.accept()

    def viewportEvent(self, event):
        if event.Type == gui.QEvent.ToolTip:
            item = self.tree.currentItem()
            gui.QToolTip.ShowText(event.pos, item.toolTip().text(), item)

    def add_view(self, event = None):
        "handles Menu > View > New view"
        self.check_active()
        self.opts["ActiveItem"][self.opts["ActiveView"]] = str(self.activeitem.text(1))
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.viewcount += 1
        new_view = "New View #{}".format(self.viewcount)
        self.opts["ViewNames"].append(new_view)
        active = self.opts["ActiveItem"][self.opts["ActiveView"]]
        self.opts["ActiveItem"].append(active)
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
        self.opts["ActiveView"] = self.opts["ViewNames"].index(new_view)
        self.root = self.tree.takeTopLevelItem(0)
        self.root = gui.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.root.setText(1, self.opts["RootData"])
        self.tree.addTopLevelItem(self.root)
        self.activeitem = self.root
        newtree = []
        for key in sorted(self.itemdict.keys()):
            newtree.append((key, []))
        self.views.append(newtree)
        tree_item = self.viewtotree()
        self.set_title()
        self.project_dirty = True
        self.tree.setCurrentItem(tree_item)

    def rename_view(self, event = None):
        "handles Menu > View > Rename current view"
        oldname = self.opts["ViewNames"][self.opts["ActiveView"]]
        data, ok = gui.QInputDialog.getText(self, 'DocTree',
            'Geef een nieuwe naam voor de huidige view',
            gui.QLineEdit.Normal, oldname)
        if ok:
            newname = str(data)
            if newname != oldname:
                action = self.viewmenu.actions()[self.opts["ActiveView"] + 7]
                action.setText('{} {}'.format(str(action.text()).split()[0], newname))
                self.opts["ViewNames"][self.opts["ActiveView"]] = newname
                self.project_dirty = True
                self.set_title()

    def next_view(self, prev=False):
        """cycle to next view, if available (default direction / forward)"""
        if self.viewcount == 1:
            gui.QMessageBox.information(self, 'Doctree', "This is the only view")
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

    def prev_view(self):
        """cycle to previous view (alternate direction / backward)"""
        self.next_view(prev=True)

    def select_view(self, event = None):
        "handles Menu > View > <view name>"
        sender = self.sender()
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.editor.clear()
        menuitem_list = [x for x in self.viewmenu.actions()]
        for menuitem in menuitem_list[7:]:
            if menuitem == sender:
                newview = sender.text()
                sender.setChecked(True)
            else:
                if menuitem.isChecked():
                    menuitem.setChecked(False)
        self.opts["ActiveView"] = self.opts["ViewNames"].index(
            str(newview).split(None,1)[1])
        self.root = self.tree.takeTopLevelItem(0)
        self.root = gui.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.root.setText(1, self.opts["RootData"])
        self.tree.addTopLevelItem(self.root)
        self.activeitem = self.root
        tree_item = self.viewtotree()
        self.set_title()
        self.tree.setCurrentItem(tree_item)

    def remove_view(self, event = None):
        "handles Menu > View > Delete current view"
        if self.viewcount == 1:
            gui.QMessageBox.information(self, 'Doctree', "Can't delete the last (only) view")
            return
        retval = gui.QMessageBox.question(self, "DocTree",
            "Are you sure you want to remove this view?",
            gui.QMessageBox.Yes | gui.QMessageBox.No,
            defaultButton = gui.QMessageBox.Yes)
        if retval == gui.QMessageBox.Yes:
            self.viewcount -= 1
            viewname = self.opts["ViewNames"][self.opts["ActiveView"]]
            self.opts["ViewNames"].remove(viewname)
            self.opts["ActiveItem"].pop(self.opts["ActiveView"])
            self.views.pop(self.opts["ActiveView"])
            if self.opts["ActiveView"] > 0:
                self.opts["ActiveView"] -= 1
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
            self.root = self.tree.takeTopLevelItem(0)
            self.root = gui.QTreeWidgetItem()
            self.root.setText(0, self.opts["RootTitle"])
            self.root.setText(1, self.opts["RootData"])
            self.tree.addTopLevelItem(self.root)
            self.activeitem = self.root
            self.tree.setCurrentItem(self.viewtotree())
            self.project_dirty = True
            self.set_title()

    def rename_root(self, event=None):
        """afhandelen Menu > Rename Root (Shift-Ctrl-F2"""
        data, ok = gui.QInputDialog.getText(self, 'DocTree',
            'Geef nieuwe titel voor het root item:',
            gui.QLineEdit.Normal, self.root.text(0))
        if ok:
            data = str(data)
            if data:
                self.project_dirty = True
                self.root.setText(0, data)
                self.opts['RootTitle'] = data

    def add_item(self, event = None, root = None, under = True):
        """nieuw item toevoegen (default: onder het geselecteerde)"""
        if under:
            if root is None:
                root = self.activeitem or self.root
        else:
            root = self.activeitem.parent()
        title = "Geef een titel op voor het nieuwe item"
        text = ""
        new = self.ask_title(title, text)
        if not new:
            return
        new_title, extra_title = new
        self.check_active()
        newkey = len(self.itemdict)
        while newkey in self.itemdict:
            newkey += 1
        self.itemdict[newkey] = (new_title, "")
        item = gui.QTreeWidgetItem()
        item.setText(0, new_title)
        item.setText(1, str(newkey))
        item.setToolTip(0, new_title)
        if under:
            root.addChild(item)
        else:
            pos = root.indexOfChild(self.activeitem)
            root.insertChild(pos + 1, item)
        if extra_title:
            subkey = newkey + 1
            self.itemdict[subkey] = (extra_title, "")
            sub_item = gui.QTreeWidgetItem() #[extra_title, subkey])
            sub_item.setText(0, extra_title)
            sub_item.setText(1, str(subkey))
            sub_item.setToolTip(0, extra_title)
            item.addChild(sub_item)
            item = sub_item
        for idx, view in enumerate(self.views):
            if idx != self.opts["ActiveView"]:
                subitem = []
                if extra_title:
                    subitem.append((subkey, []))
                view.append((newkey, subitem))
        root.setExpanded(True)
        self.project_dirty = True
        self.tree.setCurrentItem(item)
        if item != self.root:
            self.editor.setFocus()

    def root_item(self, event = None):
        """nieuw item toevoegen onder root"""
        self.add_item(root = self.root)

    def insert_item(self, event=None):
        """nieuw item toevoegen *achter* het geselecteerde (en onder diens parent)"""
        self.add_item(event = event, under = False)

    def cut_item(self, evt = None):
        "cut = copy with removing item from tree"
        self.copy_item(cut = True)

    def delete_item(self, evt = None):
        "delete = copy with removing item from tree and memory"
        self.copy_item(cut = True, retain = False)

    def copy_item(self, evt = None, cut = False, retain = True):
        "start copy/cut/delete action"
        current = self.tree.selectedItems()[0]
        if current == self.root:
            gui.QMessageBox.information(self, "DocTree", "Can't do this with root")
            return
        go_on = True
        if cut and not retain:
            retval = gui.QMessageBox.question(self, "DocTree",
                "Are you sure you want to remove this item?",
                gui.QMessageBox.Yes | gui.QMessageBox.No,
                defaultButton = gui.QMessageBox.Yes)
            if retval != gui.QMessageBox.Yes:
                go_on = False
        if not go_on:
            return
        self.cut_from_itemdict = []
        if retain:
            self.cut_item = getsubtree(current)
            ## self.add_node_on_paste = True
        if not cut:
            return
        ## self.add_node_on_paste = False
        parent = current.parent()
        pos = parent.indexOfChild(current)
        if pos - 1 >= 0:
            prev = parent.child(pos - 1)
        else:
            prev = parent
            if prev == self.root:
                prev = parent.child(pos + 1)
        self.activeitem = None
        parent.takeChild(pos)
        self._popitems(current, self.cut_from_itemdict)
        self._removed = [x[0] for x in self.cut_from_itemdict]
        for ix, view in enumerate(self.views):
            print(view)
            if ix != self.opts["ActiveView"]:
                self._updateview(view)
                print(view)
        self.project_dirty = True
        self.tree.setCurrentItem(prev)

    def _popitems(self, current, itemlist):
        """recursieve routine om de structuur uit de itemdict en de
        niet-actieve views te verwijderen
        """
        ref = int(current.text(1))
        data = self.itemdict.pop(ref)
        itemlist.append((ref, data))
        for num in range(current.childCount()):
            self._popitems(current.child(num), itemlist)

    def _updateview(self, view):
        klaar = False
        for idx, item in reversed(list(enumerate(view))):
            itemref, subview = item
            if itemref in self._removed:
                self._updateview(subview)
                if not subview:
                    view.pop(idx)
                else:
                    view[idx] = subview[0]
                klaar = True
            else:
                klaar = self._updateview(subview)
            ## if klaar:
                ## break
        return klaar

    def paste_item_after(self, evt = None):
        "paste after instead of before"
        self.paste_item(before=False)

    def paste_item_below(self, evt = None):
        "paste below instead of before"
        self.paste_item(below=True)

    def paste_item(self, evt = None, before = True, below = False):
        "start paste actie"
        current = self.tree.selectedItems()[0]
        # als het geselecteerde item het top item is moet het automatisch below worden
        # maar dan wel als eerste  - of het moet niet mogen
        if not self.cut_item:
            return
        if below:
            putsubtree(current, *self.cut_item, add_nodes=self.cut_from_itemdict,
                itemdict=self.itemdict)
        else:
            ## add_to = self.tree.itemAbove(current)
            add_to = current.parent()
            pos = add_to.indexOfChild(current) # levert alleen 0 of -1 op
            if before:
                pos -= 1
            putsubtree(add_to, *self.cut_item, pos=pos,
                add_nodes=self.cut_from_itemdict, itemdict=self.itemdict)
        if not self.add_node_on_paste:
            self.add_node_on_paste = True
        self.project_dirty = True
        self.tree.setCurrentItem(current)
        current.setExpanded(True)

    def rename_item(self):
        """titel van item wijzigen"""
        def check_item(view, ref, subref):
            """zoeken waar het subitem moet worden toegevoegd"""
            retval = ""
            for itemref, subview in view:
                if itemref == ref:
                    subview.append((subref, []))
                    retval = 'Stop'
                else:
                    retval = check_item(subview, ref, subref)
                if retval == 'Stop':
                    break
            return retval
        root = item = self.activeitem
        self.check_active()
        new = self.ask_title('Nieuwe titel voor het huidige item:', item.text(0))
        if not new:
            return
        self.project_dirty = True
        new_title, extra_title = new
        self.activeitem.setText(0, new_title)
        self.activeitem.setToolTip(0, new_title)
        if item == self.root:
            self.opts['RootTitle'] = new_title
            return
        ref = self.activeitem.text(1)
        old_title, data = self.itemdict[int(ref)]
        self.itemdict[int(ref)] = (new_title, data)
        if extra_title:
            sub_item = gui.QTreeWidgetItem()
            sub_item.setText(0, extra_title)
            self.activeitem.addChild(sub_item)
            subref = int(ref) + 1
            while subref in self.itemdict:
                subref += 1
            self.itemdict[subref] = (extra_title, data)
            sub_item.setText(1, str(subref))
            sub_item.setToolTip(0, extra_title)
            self.activeitem.setExpanded(True)
            item = sub_item
            for idx, view in enumerate(self.views):
                if idx != self.opts["ActiveView"]:
                    check_item(view, ref, subref)
        root.setExpanded(True)
        self.tree.setCurrentItem(item)
        ## if item != self.root:
            ## self.editor.setFocus()

    def ask_title(self, _title, _text):
        """vraag titel voor item"""
        data, ok = gui.QInputDialog.getText(self, 'DocTree', _title,
            gui.QLineEdit.Normal, _text)
        if ok:
            if data:
                try:
                    new_title, extra_title = str(data).split(" \\ ")
                except ValueError:
                    new_title, extra_title = str(data), ""
                return new_title, extra_title
        return

    def order_top(self, event = None):
        """order items directly under the top level"""
        self.reorder_items(self.root)

    def order_all(self, event = None):
        """order items under top level and below"""
        self.reorder_items(self.root, recursive = True)

    def reorder_items(self, root, recursive = False):
        "(re)order_items"
        root.sortChildren(0, core.Qt.AscendingOrder)
        if recursive:
            for num in range(root.childCount()):
                tag = root.child(num)
                self.reorder_items(tag, recursive)
        self.project_dirty = True

    def order_this(self, event = None):
        """order items directly under current level"""
        self.reorder_items(self.activeitem)

    def order_lower(self, event = None):
        """order items under current level and below"""
        self.reorder_items(self.activeitem, recursive = True)

    def next_note(self, event = None):
        """move to next item"""
        parent = self.activeitem.parent()
        if parent is not None:
            pos = parent.indexOfChild(self.activeitem)
            if pos < parent.childCount() - 1:
                item = parent.child(pos + 1)
                self.tree.setCurrentItem(item)
                return
        gui.QMessageBox.information(self, "DocTree", "Geen volgend item op dit niveau")

    def prev_note(self, event = None):
        """move to previous item"""
        parent = self.activeitem.parent()
        if parent is not None:
            pos = parent.indexOfChild(self.activeitem)
            if pos > 0:
                item = parent.child(pos - 1)
                self.tree.setCurrentItem(item)
                return
        gui.QMessageBox.information(self, "DocTree", "Geen vorig item op dit niveau")

    def check_active(self, message = None):
        """zorgen dat de editor inhoud voor het huidige item bewaard wordt in de treectrl"""
        if self.activeitem:
            if self.editor.document().isModified():
                if message:
                    gui.QMessageBox.information(self, 'Doctree', message)
                ref = self.activeitem.text(1)
                content = self.editor.get_contents()
                try:
                    titel, tekst = self.itemdict[int(ref)]
                except (KeyError, ValueError):
                    if content:
                        self.root.setText(1, content)
                        self.opts["RootData"] = str(content)
                else:
                    self.itemdict[int(ref)] = (titel, content)
                self.editor.document().setModified(False)
                self.project_dirty = True

    def activate_item(self, item):
        """meegegeven item "actief" maken (accentueren en in de editor zetten)"""
        self.activeitem = item
        ref = item.text(1)
        try:
            titel, tekst = self.itemdict[int(ref)]
        except (KeyError, ValueError):
            self.editor.set_contents(ref)
        else:
            self.editor.set_contents(tekst, titel)
        self.editor.setReadOnly(False)

    def info_page(self, event = None):
        """help -> about"""
        info = [
            "DocTree door Albert Visser",
            "Uitgebreid electronisch notitieblokje",
            "PyQt versie",
            ]
        gui.QMessageBox.information(self, "DocTree", "\n".join(info),)

    def help_page(self, event = None):
        """help -> keys"""
        info = [
            "Ctrl-N\t\t- nieuwe notitie onder huidige",
            "Shift-Ctrl-N\t\t- nieuwe notitie onder hoogste niveau",
            "Insert\t\t- nieuwe notitie achter huidige",
            "Ctrl-PgDn in editor of",
            " CursorDown in tree\t- volgende notitie",
            "Ctrl-PgUp in editor of",
            " CursorUp in tree\t- vorige notitie",
            "Ctrl-D of Delete in tree\t- verwijder notitie",
            "Ctrl-S\t\t- alle notities opslaan",
            "Shift-Ctrl-S\t\t- alle notities opslaan onder andere\n\t\t  naam",
            "Ctrl-R\t\t- alle notities opnieuw laden",
            "Ctrl-O\t\t- ander bestand met notities laden",
            "Ctrl-I\t\t- initialiseer (nieuw) notitiebestand",
            "Ctrl-Q, Esc\t\t- opslaan en sluiten",
            "Ctrl-H\t\t- verbergen in system tray",
            "",
            "F1\t\t- deze (help)informatie",
            "F2\t\t- wijzig notitie titel",
            "Shift-F2\t\t- wijzig root titel",
            ]
        gui.QMessageBox.information(self, "DocTree", "\n".join(info),)

def main(fnaam):
    app = gui.QApplication(sys.argv)
    main = MainWindow(fnaam = fnaam)
    app.setWindowIcon(main.nt_icon)
    main.show()
    main.project_file = fnaam
    err = main.read()
    if err:
        gui.QMessageBox.information(main, "Error", err, gui.QMessageBox.Ok)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main('MyMan.ini')

