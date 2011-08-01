#! /usr/bin/env python
# -*- coding: utf-8 -*-

"DocTree PyQt versie"

import os
import sys
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import cPickle as pck
import shutil
import pprint
import datetime as dt
HERE = os.path.dirname(__file__)

def tabsize(pointsize):
     "pointsize omrekenen in pixels t.b.v. (gemiddelde) tekenbreedte"
     x, y = divmod(pointsize * 8, 10)
     return x * 4 if y < 5 else (x + 1) * 4

def getsubtree(item):
    """recursieve functie om de strucuur onder de te verplaatsen data
    te onthouden"""
    titel = item.text(0)
    text = item.text(1)
    subtree = []
    for num in range(item.childCount()):
        kid = item.child(num)
        subtree.append(getsubtree(kid))
    return titel, text, subtree

def putsubtree(parent, titel, text, subtree=None):
    """recursieve functie om de onthouden structuur terug te zetten"""
    if subtree is None:
        subtree = []
    new = gui.QTreeWidgetItem()
    new.setText(0, titel)
    new.setText(1, text)
    parent.addChild(new)
    for sub in subtree:
        putsubtree(new, *sub)
    return new

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
        self.connect(ok_button, core.SIGNAL('clicked()'), self.klaar)

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

    def selectionChanged(self, newsel, oldsel):
        """wordt aangeroepen als de selectie gewijzigd is

        de tekst van de oude selectie wordt in de itemdict geactualiseerd
        en die van de nieuwe wordt erin opgezocht en getoond"""
        # helaas zijn newsel en oldsel niet makkelijk om te rekenen naar treeitems
        self.parent.check_active()
        h = self.currentItem()
        self.parent.activate_item(h)

    def dropEvent(self, event):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        deze methode breidt de Treewidget methode uit met wat visuele zaken
        """
        dragitem = self.selectedItems()[0]
        gui.QTreeWidget.dropEvent(self, event)
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
        self.connect(self, core.SIGNAL('currentCharFormatChanged(QTextCharFormat)'),
             self.charformat_changed)
        self.connect(self, core.SIGNAL('cursorPositionChanged()'),
             self.cursorposition_changed)
        font = self.currentFont()
        self.setTabStopWidth(tabsize(font.pointSize()))

    def set_contents(self, data):
        "load contents into editor"
        ## self.setHtml(data)
        self.codec = core.QTextCodec.codecForHtml(data)
        self.setHtml(self.codec.toUnicode(data))

    def get_contents(self):
        "return contents from editor"
        ## return str(self.toHtml())
        data = self.codec.fromUnicode(self.toHtml())
        return data

    def text_bold(self, event = None):
        "selectie vet maken"
        fmt = gui.QTextCharFormat()
        if self.parent.actiondict['&Bold'].isChecked():
            fmt.setFontWeight(gui.QFont.Bold)
        else:
            fmt.setFontWeight(gui.QFont.Normal)
        self.mergeCurrentCharFormat(fmt)

    def text_italic(self, event = None):
        "selectie schuin schrijven"
        fmt = gui.QTextCharFormat()
        fmt.setFontItalic(self.parent.actiondict['&Italic'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def text_underline(self, event = None):
        "selectie onderstrepen"
        fmt = gui.QTextCharFormat()
        fmt.setFontUnderline(self.parent.actiondict['&Underline'].isChecked())
        self.mergeCurrentCharFormat(fmt)

    def align_left(self, event = None):
        "alinea links uitlijnen"
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignLeft | core.Qt.AlignAbsolute)

    def align_center(self, event = None):
        "alinea centreren"
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignHCenter)

    def align_right(self, event = None):
        "alinea rechts uitlijnen"
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["&Justify"].setChecked(False)
        self.setAlignment(core.Qt.AlignRight | core.Qt.AlignAbsolute)

    def text_justify(self, event = None):
        "alinea aan weerszijden uitlijnen"
        self.parent.actiondict["Align &Left"].setChecked(False)
        self.parent.actiondict["C&enter"].setChecked(False)
        self.parent.actiondict["Align &Right"].setChecked(False)
        self.setAlignment(core.Qt.AlignJustify)

    def indent_more(self, event = None):
        "alinea verder laten inspringen"
        ## print(self.document().indentWidth())
        where = self.textCursor().block()
        ## fmt = gui.QTextBlockFormat()
        fmt = where.blockFormat()
        wid = fmt.indent()
        print('indent_more called, current indent is {}'.format(wid))
        fmt.setIndent(wid + 100)
        print('indent_more called, indent aangepast naar {}'.format(fmt.indent()))
        # maar hier is geen merge methode voor, lijkt het...

    def indent_less(self, event = None):
        "alinea minder ver laten inspringen"
        fmt = gui.QTextBlockFormat()
        wid = fmt.indent()
        print('indent_less called, current indent is {}'.format(wid))
        if wid > 100:
            fmt.setIndent(wid - 100)

    def text_font(self, event = None):
        "lettertype en/of -grootte instellen"
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
        col = gui.QColorDialog.getColor(self.textColor(), self)
        if not col.isValid():
            return
        fmt = gui.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeCurrentCharFormat(fmt)
        self.color_changed(col)

    def charformat_changed(self, format):
        "wordt aangeroepen als het tekstformat gewijzigd is"
        self.font_changed(format.font());
        self.color_changed(format.foreground().color())

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
        pix = gui.QPixmap(16, 16)
        pix.fill(col)
        self.parent.actiondict["&Color..."].setIcon(gui.QIcon(pix))

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
    def __init__(self, parent = None, fnaam = ""):
        self.opts = {
            "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
            "ActiveItem": [0,], "ActiveView": 0, "ViewNames": ["Default",],
            "RootTitle": "MyNotes", "RootData": ""}
        gui.QMainWindow.__init__(self)
        self.nt_icon = gui.QIcon(os.path.join(HERE, "doctree.xpm"))
        self.tray_icon = gui.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip("Click to revive DocTree")
        self.connect(self.tray_icon, core.SIGNAL('clicked'),
            self.revive)
        tray_signal = "activated(QSystemTrayIcon::ActivationReason)"
        self.connect(self.tray_icon, core.SIGNAL(tray_signal),
            self.revive)
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
                ## ("e&Xit", self.afsl, 'Ctrl+Q', 'icons/exit.png', 'Exit program'),
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
                ), ), # label, handler, shortcut, icon, info
            ('&Edit', (
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
                ), ),
            ("&Help", (
                ("&About", self.info_page, '', '', 'About this application'),
                ("&Keys", self.help_page, 'F1', '', 'Keyboard shortcuts'),
                ), ),
            )
        )
        self.create_stylestoolbar()

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
                    action = gui.QAction(gui.QIcon(os.path.join(HERE, icon)), label, self)
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
                if label:
                    menu.addAction(action)
                    self.actiondict[label] = action

    def create_stylestoolbar(self):
        toolbar = self.addToolBar('styles')
        self.combo_font = gui.QFontComboBox(toolbar)
        toolbar.addWidget(self.combo_font)
        self.connect(self.combo_font, core.SIGNAL('activated(QString)'),
            self.editor.text_family)
        self.combo_size = gui.QComboBox(toolbar)
        toolbar.addWidget(self.combo_size)
        self.combo_size.setEditable(True)
        db = gui.QFontDatabase()
        for size in db.standardSizes():
            self.combo_size.addItem(str(size))
        self.connect(self.combo_size, core.SIGNAL('activated(QString)'),
            self.editor.text_size)
        self.combo_size.setCurrentIndex(self.combo_size.findText(
            str(self.editor.font().pointSize())))

        pix = gui.QPixmap(16, 16)
        pix.fill(core.Qt.black)
        action = gui.QAction(gui.QIcon(pix), "&Color...", self)
        self.connect(action, core.SIGNAL('triggered()'), self.editor.text_color)
        toolbar.addAction(action)
        self.actiondict["&Color..."] = action

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
        self.save_needed()
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
        for menuitem in menuitem_list[4:]:
            self.viewmenu.removeAction(menuitem)
        action = gui.QAction('&Default', self)
        action.setStatusTip("switch to this view")
        action.setCheckable(True)
        self.connect(action, core.SIGNAL('triggered()'), self.select_view)
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
        self.tree.setFocus()

    def save_needed(self):
        """eigenlijk bedoeld om te reageren op een indicatie dat er iets aan de
        verzameling notities is gewijzigd (de oorspronkelijke self.project_dirty)"""
        if not self.has_treedata:
            return
        retval = gui.QMessageBox.question(self, "DocTree",
            "Save current file before continuing?",
            gui.QMessageBox.Yes | gui.QMessageBox.No)
        if retval == gui.QMessageBox.Yes:
            self.save()

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
            tree_item.setText(1, str(item))
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
        for menuitem in menuitem_list[4:]:
            self.viewmenu.removeAction(menuitem)
        for idx, name in enumerate(self.opts["ViewNames"]):
            action = gui.QAction(name, self)
            action.setStatusTip("switch to this view")
            action.setCheckable(True)
            self.connect(action, core.SIGNAL('triggered()'), self.select_view)
            self.viewmenu.addAction(action)
            if idx == self.opts["ActiveView"]:
                action.setChecked(True)
        item_to_activate = self.viewtotree()
        self.has_treedata = True
        self.root.setExpanded(True)
        if item_to_activate != self.activeitem:
            self.tree.setCurrentItem(item_to_activate)
        self.set_title()
        self.tree.setFocus()

    def reread(self, event = None):
        """afhandelen Menu > Reload (Ctrl-R)"""
        retval = gui.QMessageBox.question(self, "DocTree", "OK to reload?",
            gui.QMessageBox.Ok | gui.QMessageBox.Cancel)
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
        f_out = open(self.project_file,"w")
        pck.dump(nt_data, f_out)
        f_out.close()
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

    def afsl(self, event = None):
        """applicatie afsluiten"""
        if self.has_treedata:
            self.save(meld=False)

    def add_view(self, event = None):
        "handles Menu > View > New view"
        self.check_active()
        self.opts["ActiveItem"][self.opts["ActiveView"]] = self.activeitem.text(1)
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.viewcount += 1
        new_view = "New View #{}".format(self.viewcount)
        self.opts["ViewNames"].append(new_view)
        active = self.opts["ActiveItem"][self.opts["ActiveView"]]
        self.opts["ActiveItem"].append(active)
        menuitem_list = [x for x in self.viewmenu.actions()]
        for idx, menuitem in enumerate(menuitem_list[4:]):
            if idx == self.opts["ActiveView"]:
                menuitem.setChecked(False)
        action = gui.QAction(new_view, self)
        action.setStatusTip("switch to this view")
        action.setCheckable(True)
        self.connect(action, core.SIGNAL('triggered()'), self.select_view)
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
                self.viewmenu.actions()[self.opts["ActiveView"] + 4].setText(newname)
                self.opts["ViewNames"][self.opts["ActiveView"]] = newname
                self.set_title()

    def select_view(self, event = None):
        "handles Menu > View > <view name>"
        sender = self.sender()
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.editor.clear()
        menuitem_list = [x for x in self.viewmenu.actions()]
        for menuitem in menuitem_list[4:]:
            if menuitem == sender:
                newview = sender.text()
                sender.setChecked(True)
            else:
                if menuitem.isChecked():
                    menuitem.setChecked(False)
        self.opts["ActiveView"] = self.opts["ViewNames"].index(newview)
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
        retval = gui.QMessageBox.question(self, "DocTree",
            "Are you sure you want to remove this view?",
            gui.QMessageBox.Yes | gui.QMessageBox.No)
        if retval == gui.QMessageBox.Yes:
            self.viewcount -= 1
            viewname = self.opts["ViewNames"][self.opts["ActiveView"]]
            self.opts["ViewNames"].remove(viewname)
            self.opts["ActiveItem"].pop(self.opts["ActiveView"])
            self.views.pop(self.opts["ActiveView"])
            if self.opts["ActiveView"] > 0:
                self.opts["ActiveView"] -= 1
            menuitem_list = [x for x in self.viewmenu.actions()]
            menuitem_list[self.opts["ActiveView"] + 4].setChecked(True)
            for menuitem in menuitem_list:
                if menuitem.text() == viewname:
                    self.viewmenu.removeAction(menuitem)
                    break
            if self.opts["ActiveView"] == 0:
                menuitem_list[4].setChecked(True)
            self.root = self.tree.takeTopLevelItem(0)
            self.root = gui.QTreeWidgetItem()
            self.root.setText(0, self.opts["RootTitle"])
            self.root.setText(1, self.opts["RootData"])
            self.tree.addTopLevelItem(self.root)
            self.activeitem = self.root
            self.tree.setCurrentItem(self.viewtotree())
            self.set_title()

    def rename_root(self, event=None):
        """afhandelen Menu > Rename Root (Shift-Ctrl-F2"""
        data, ok = gui.QInputDialog.getText(self, 'DocTree',
            'Geef nieuwe titel voor het root item:',
            gui.QLineEdit.Normal, self.root.text(0))
        if ok:
            data = str(data)
            if data:
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
            item.addChild(sub_item)
            item = sub_item
        for idx, view in enumerate(self.views):
            if idx != self.opts["ActiveView"]:
                subitem = []
                if extra_title:
                    subitem.append((subkey, []))
                view.append((newkey, subitem))
        root.setExpanded(True)
        self.tree.setCurrentItem(item)
        if item != self.root:
            self.editor.setFocus()

    def root_item(self, event = None):
        """nieuw item toevoegen onder root"""
        self.add_item(root = self.root)

    def insert_item(self, event=None):
        """nieuw item toevoegen *achter* het geselecteerde (en onder diens parent)"""
        self.add_item(event = event, under = False)

    def delete_item(self, event = None):
        """item verwijderen"""
        def check_item(view, ref):
            klaar = False
            for item, subview in view:
                if item == ref:
                    view.remove((item, subview))
                    klaar = True
                    break
                else:
                    klaar = check_item(subview, item)
                    if klaar:
                        break
            return klaar
        item = self.tree.selectedItems()[0]
        if item != self.root:
            parent = item.parent()
            pos = parent.indexOfChild(item)
            if pos - 1 >= 0:
                prev = parent.child(pos - 1)
            else:
                prev = parent
                if prev == self.root:
                    prev = parent.child(pos + 1)
            self.activeitem = None
            ref = item.text(1)
            self.itemdict.pop(int(ref))
            parent.takeChild(pos)
            for ix, view in enumerate(self.views):
                if ix != self.opts["ActiveView"]:
                    check_item(view, ref)
            self.tree.setCurrentItem(prev)
        else:
            messagebox(self, "Can't delete root", "Error")

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
        new_title, extra_title = new
        self.activeitem.setText(0, new_title)
        ref = self.activeitem.text(1)
        old_title, data = self.itemdict[int(ref)]
        self.itemdict[int(ref)] = (new_title, data)
        if extra_title:
            sub_item = gui.QTreeWidgetItem()
            subitem.setText(0, extra_title)
            self.activeitem.addChild(sub_item)
            subref = int(ref) + 1
            while subref in self.itemdict:
                subref += 1
            self.itemdict[subref] = (extra_title, data)
            subitem.setText(1, str(subref))
            item = sub_item
            for idx, view in enumerate(self.views):
                if idx != self.opts["ActiveView"]:
                    check_item(view, ref, subref)
        root.setExpanded(True)
        self.tree.setCurrentItem(item)
        if item != self.root:
            self.editor.setFocus()

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

    def order_this(self, event = None):
        """order items directly under current level"""
        self.reorder_items(self.activeitem)

    def order_lower(self, event = None):
        """order items under current level and below"""
        self.reorder_items(self.activeitem, recursive = True)

    def next_note(self, event = None):
        """move to next item"""
        parent = self.activeitem.parent()
        pos = parent.indexOfChild(self.activeitem)
        if pos < parent.childCount() - 1:
            item = parent.child(pos + 1)
            self.tree.setCurrentItem(item)

    def prev_note(self, event = None):
        """move to previous item"""
        parent = self.activeitem.parent()
        pos = parent.indexOfChild(self.activeitem)
        if pos > 0:
            item = parent.child(pos - 1)
            self.tree.setCurrentItem(item)

    def check_active(self, message = None):
        """zorgen dat de editor inhoud voor het huidige item bewaard wordt in de treectrl"""
        if self.activeitem:
            if self.editor.document().isModified():
                if message:
                    print(message) # moet dit niet messagebox zijn?
                ref = self.activeitem.text(1)
                content = self.editor.get_contents()
                try:
                    titel, tekst = self.itemdict[int(ref)]
                except (KeyError, ValueError):
                    if content:
                        self.root.setText(1, content)
                        self.opts["RootData"] = content
                else:
                    self.itemdict[int(ref)] = (titel, content)

    def activate_item(self, item):
        """meegegeven item "actief" maken (accentueren en in de editor zetten)"""
        self.activeitem = item
        ref = item.text(1)
        try:
            titel, tekst = self.itemdict[int(ref)]
        except (KeyError, ValueError):
            self.editor.set_contents(ref)
        else:
            self.editor.set_contents(tekst)
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
