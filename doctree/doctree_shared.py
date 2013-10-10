# -*- coding: utf-8 -*-

"DocTree gui-onafhankelijk gedeelte"

import os
import sys
if sys.version[0] < '3':
    import cPickle as pck
    str = unicode
else:
    import pickle as pck
import shutil
import pprint
import logging
logging.basicConfig(filename='doctree.log', level=logging.DEBUG,
    format='%(asctime)s %(message)s')
import datetime as dt

def init_opts():
    return {
        "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
        "ActiveItem": [0,], "ActiveView": 0, "ViewNames": ["Default",],
        "RootTitle": "MyNotes", "RootData": "", "ImageCount": 0}

def log(message):
    "write message to logfile"
    logging.info(message)

def getsubtree(tree, item, itemlist=None):
    """recursieve functie om de structuur onder de te verplaatsen data
    te onthouden"""
    if itemlist is None:
        itemlist = []
    titel, key = tree._getitemdata(item)
    itemlist.append(key)
    log(' getsubtree item {}, {}'.format(titel, key))
    subtree = []
    for kid in tree._getitemkids(item):
        data, itemlist = getsubtree(tree, kid, itemlist)
        subtree.append(data)
    return (titel, key, subtree), itemlist

def putsubtree(tree, parent, titel, key, subtree=None, pos=-1):
    """recursieve functie om de onthouden structuur terug te zetten"""
    if subtree is None:
        subtree = []
    new = tree.add_to_parent(str(key), str(titel), parent, pos)
    for subtitel, subkey, subsubtree in subtree:
        putsubtree(tree, new, subtitel, subkey, subsubtree)
    return new # , itemdict

class TreePanel(object):
    "geen mixin, maar een placeholder om te tonen dat deze gebouwd moet worden"
    def __init__(self, parent):
        raise NotImplementedError

class EditorPanel(object):
    "geen mixin, maar een placeholder om te tonen dat deze gebouwd moet worden"
    def __init__(self, parent):
        raise NotImplementedError

class Mixin(object):
    """Hoofdscherm van de applicatie"""
    def __init__(self): #, parent=None, fnaam=""):
        self.project_dirty = False # self.set_project_dirty(False)
        self.add_node_on_paste = False
        self.has_treedata = False

    def _get_menu_data(self):
        return (
            ("&Main", (
                ("Re&Load", self.reread, 'Ctrl+R', 'icons/filerevert.png', 'Reread notes file'),
                ("&Open", self.open, 'Ctrl+O', 'icons/fileopen.png', "Choose and open notes file"),
                ("&Init", self.new, 'Shift+Ctrl+I', 'icons/filenew.png', 'Start a new notes file'),
                ("&Save", self.save, 'Ctrl+S', 'icons/filesave.png', 'Save notes file'),
                ("Save as", self.saveas, 'Shift+Ctrl+S', 'icons/filesaveas.png', 'Name and save notes file'),
                (),
                ("&Root title", self.rename_root, 'Shift+F2', '', 'Rename root'),
                ("Items sorteren", self.order_top, '', '', 'Bovenste niveau sorteren op titel'),
                ("Items recursief sorteren", self.order_all, '', '', 'Alle niveaus sorteren op titel'),
                (),
                ("&Hide", self.hide_me, 'Ctrl+H', '', 'verbergen in system tray'),
                ("Switch pane", self.change_pane, 'Ctrl+Tab', '', 'switch tussen tree en editor'),
                (),
                ("e&Xit", self.afsl, 'Ctrl+Q,Escape', 'icons/exit.png', 'Exit program'),
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
            ('&Tree', (
                ## ('&Undo', self.tree.undo,  'Ctrl+Z', 'icons/edit-undo.png', 'Undo last operation'),
                ## ('&Redo', self.tree.redo, 'Ctrl+Y', 'icons/edit-redo.png', 'Redo last undone operation'),
                ## (),
                ('Cu&t', self.cut_item, 'Ctrl+Alt+X', 'icons/treeitem-cut.png', 'Copy the selection and delete from tree'),
                ('&Copy', self.copy_item, 'Ctrl+Alt+C', 'icons/treeitem-copy.png', 'Just copy the selection'),
                ('&Paste Under', self.paste_item_below, 'Ctrl+Alt+V', 'icons/treeitem-paste.png', 'Paste the copied selection under the selected item'),
                ('&Paste After', self.paste_item_after, 'Shift+Ctrl+Alt+V', '', 'Paste the copied selection after the selected item (same parent)'),
                ('&Paste Before', self.paste_item, '', '', 'Paste the copied selection before the selected item (same parent)'),
                (),
                ('Expand', self.expand_item, 'Ctrl+<', '', 'Expand tree item'),
                ('Collapse', self.collapse_item, 'Ctrl+>', '', 'Collapse tree item'),
                ('Expand all', self.expand_all, 'Ctrl+Alt+<', '', 'Expand all subitems'),
                ('Collapse all', self.collapse_all, 'Ctrl+Alt+>', '', 'Collapse all subitems'),
                ## (),
                ## ('Select A&ll', self.tree.selectAll, 'Ctrl+A', "", 'Select the entire tree'),
                ## ("&Clear All (can't undo)", self.tree.clear, '', '', 'Delete the entire tree'),
                ), ),
            ('T&ext', (
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
                ("&Enlarge text", self.editor.enlarge_text, 'Ctrl+Up', '', 'Use bigger letters'),
                ("&Shrink text", self.editor.shrink_text, 'Ctrl+Down', '', 'Use smaller letters'),
                (),
                ("&Color...", self.editor.text_color, '', '', 'Set/change colour'),
                ("&Background...", self.editor.background_color, '', '',
                    'Set/change background colour'),
                ), ),
            ("&Help", (
                ("&About", self.info_page, '', '', 'About this application'),
                ("&Keys", self.help_page, 'F1', '', 'Keyboard shortcuts'),
                ), ), )

    def show_message(self, text='', title=''):
        "voor elke gui variant apart te implementeren"
        print('{}: {}'.format(title, text))

    def show_statusbar_message(self, text):
        "voor elke gui variant apart te implementeren"
        print('status: {}'.format(text))

    def change_pane(self, event=None):
        "wissel tussen tree en editor"
        raise NotImplementedError

    def set_project_dirty(self, value):
        self.project_dirty = value
        self.set_title()

    def set_title(self):
        """standaard titel updaten"""
        raise NotImplementedError

    def open(self, event=None):
        "afhandelen Menu > Open / Ctrl-O"
        if not self.save_needed():
            return
        dirname = os.path.dirname(self.project_file)
        ok, filename = self.getfilename("DocTree - choose file to open", dirname)
        if ok:
            self.project_file = str(filename)
            err = self.read()
            if err:
                self.show_message(title="Error", text=err)
            self.show_statusmessage('{} gelezen'.format(self.project_file))

    def new(self, event = None):
        "Afhandelen Menu - Init / Ctrl-I"
        if not self.save_needed():
            return False
        dirname = os.path.dirname(self.project_file)
        ok, filename = self.getfilename("DocTree - enter name for new file",
            dirname, save=True)
        if not ok:
            return
        filename = str(filename)
        test = os.path.splitext(filename)
        if len(test) == 1 or test[1] != '.pck':
            filename += '.pck'
        self.project_file = filename
        self.views = [[],]
        self.viewcount = 1
        self.itemdict = {}
        self.opts = init_opts()
        self.has_treedata = True
        self.set_title()
        self.set_project_dirty(False)
        return True

    def save_needed(self, meld=True):
        """vraag of het bestand opgeslagen moet worden als er iets aan de
        verzameling notities is gewijzigd"""
        # meld is only to keep signatures aligned
        return self.has_treedata and self.project_dirty

    def treetoview(self):
        """zet de visuele tree om in een tree om op te slaan"""
        def lees_item(item):
            """recursieve functie om de data in een pickle-bare structuur om te zetten"""
            textref = self.tree._getitemtext(item)
            if item == self.activeitem:
                self.opts["ActiveItem"][self.opts["ActiveView"]] = textref
            kids = [lees_item(x) for x in self.tree._getitemkids(item)]
            return textref, kids
        data = [lees_item(x) for x in self.tree._getitemkids(self.root)]
        return data

    def viewtotree(self):
        """zet de geselecteerde view om in een visuele tree"""
        def maak_item(parent, key, children = None):
            """recursieve functie om de TreeCtrl op te bouwen vanuit de opgeslagen data"""
            item_to_activate = None
            if children is None:
                children = []
            titel = self.itemdict[key][0]
            tree_item = self.tree.add_to_parent(key, titel, parent)
            if key == self.opts["ActiveItem"][self.opts['ActiveView']]:
                item_to_activate = tree_item
            for child in children:
                x, y = maak_item(tree_item, *child)
                if y is not None:
                    item_to_activate = y
            return key, item_to_activate
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
            "RootTitle": "MyNotes", "RootData": "", "ImageCount": 0}
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
        self._read()
        item_to_activate = self.viewtotree()
        self.has_treedata = True
        self.set_title()
        self.set_project_dirty(False)
        self._finish_read(item_to_activate)

    def _read(self):
        raise NotImplementedError

    def reread(self, event=None):
        """afhandelen Menu > Reload (Ctrl-R)"""
        if self._ok_to_reload():
            self.read()
        self.show_statusmessage('{} herlezen'.format(self.project_file))

    def _ok_to_reload(self):
        return NotImplementedError

    def save(self, event=None, meld=True):
        """afhandelen Menu > save"""
        if self.project_file:
            self.write(meld=meld)
        else:
            self.saveas()
        self.show_statusmessage('{} opgeslagen'.format(self.project_file))

    def write(self, event=None, meld=True):
        """settings en tree data in een structuur omzetten en opslaan"""
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        nt_data = {0: self.opts, 1: self.views, 2: self.itemdict}
        try:
            shutil.copyfile(self.project_file, self.project_file + ".bak")
        except IOError:
            pass
        f_out = open(self.project_file,"wb")
        pck.dump(nt_data, f_out, protocol=2)
        f_out.close()
        self.set_project_dirty(False)
        if meld:
            self.show_message(self.project_file + " is opgeslagen", "DocTool")

    def saveas(self, event=None):
        """afhandelen Menu > Save As"""
        dirname = os.path.dirname(self.project_file)
        ok, filename = self.getfilename("DocTree - save file as:", dirname,
            save=True)
        if ok:
            filename = str(filename)
            test = os.path.splitext(filename)
            if len(test) == 1 or test[1] != '.pck':
                filename += '.pck'
            self.project_file = filename
            self.write()
            self.set_title()

    def hide_me(self, event=None):
        """applicatie verbergen"""
        raise NotImplementedError

    def revive(self, event=None):
        """applicatie weer zichtbaar maken"""
        raise NotImplementedError

    def afsl(self, event=None):
        raise NotImplementedError

    def add_view(self, event = None):
        "handles Menu > View > New view"
        self.check_active()
        self.opts["ActiveItem"][self.opts["ActiveView"]] = self.tree._getitemdata(
            self.activeitem)
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.viewcount += 1
        new_view = "New View #{}".format(self.viewcount)
        self.opts["ViewNames"].append(new_view)
        active = self.opts["ActiveItem"][self.opts["ActiveView"]]
        self.opts["ActiveItem"].append(active)
        self._update_newview(new_view)
        self.opts["ActiveView"] = self.opts["ViewNames"].index(new_view)
        self._rebuild_root()
        self.activeitem = self.root
        newtree = []
        for key in sorted(self.itemdict.keys()):
            newtree.append((key, []))
        self.views.append(newtree)
        self._tree_item = self.viewtotree()
        self.set_title()
        self.set_project_dirty(True)
        self._finish_add_view()

    def _set_activeitem_for_view(self):
        raise NotImplementedError

    def _update_newview(self):
        "view menu bijwerken n.a.v. toevoeging nieuwe view"
        raise NotImplementedError

    def _rebuild_root(self):
        "tree leegmaken en root opnieuw neerzetten"
        raise NotImplementedError

    def rename_view(self, event = None):
        "handles Menu > View > Rename current view"
        oldname = self.opts["ViewNames"][self.opts["ActiveView"]]
        ok, newname = self._get_name('Geef een nieuwe naam voor de huidige view',
            'DocTree', oldname)
        if ok and newname != oldname:
            self._add_view_to_menu(newname)
            self.opts["ViewNames"][self.opts["ActiveView"]] = newname
            self.set_project_dirty(True)
            self.set_title()

    def _get_name(self, caption, title, oldname):
        raise NotImplementedError

    def _add_view_to_menu(self, newname):
        raise NotImplementedError

    def next_view(self, prev=False): # voorlopig even overgeslagen
        """cycle to next view if available (default direction / forward)"""
        raise NotImplementedError

    def prev_view(self):
        """cycle to previous view (alternate direction / backward)"""
        self.next_view(prev=True)

    def select_view(self, event=None):
        "handles Menu > View > <view name>"
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        newviewtext = self._update_selectedview()
        self.opts["ActiveView"] = self.opts["ViewNames"].index(newviewtext)
        self._rebuild_root()
        tree_item = self.viewtotree()
        self.set_title()
        self._finish_select_view(tree_item)

    def _update_selectedview(self):
        "view menu bijwerken n.a.v. wijzigen view naam"
        raise NotImplementedError

    def remove_view(self, event = None):
        "handles Menu > View > Delete current view"
        if self.viewcount == 1:
            self.show_message('Doctree', "Can't delete the last (only) view")
            return
        ok = self._confirm("DocTree", "Are you sure you want to remove this view?")
        if not ok:
            return
        self.viewcount -= 1
        viewname = self.opts["ViewNames"][self.opts["ActiveView"]]
        self.opts["ViewNames"].remove(viewname)
        self.opts["ActiveItem"].pop(self.opts["ActiveView"])
        self.views.pop(self.opts["ActiveView"])
        if self.opts["ActiveView"] > 0:
            self.opts["ActiveView"] -= 1
        self._update_removedview()
        self._rebuild_root()
        self.set_project_dirty(True)
        self.set_title()
        self._finish_remove_view(self.viewtotree())

    def _confirm(self, title, text):
        ok = input('{}: {} (y/N)'.format(title, text))
        ok = True if ok.upper() == 'Y' else False
        return ok

    def _update_removedview(self):
        "view menu bijwerken n.a.v. verwijderen view"
        raise NotImplementedError

    def rename_root(self, event=None):
        """afhandelen Menu > Rename Root (Shift-Ctrl-F2"""
        ok, data = self._get_name('Geef nieuwe titel voor het root item:',
            'DocTree', self.opts['RootTitle'])
        if ok:
            self.set_project_dirty(True)
            self.opts['RootTitle'] = data
            self.tree._setitemtitle(self.root, data)

    def add_item(self, event = None, root = None, under = True):
        """nieuw item toevoegen (default: onder het geselecteerde)"""
        if under:
            if root is None:
                root = self.activeitem or self.root
        else:
            root, pos = self.tree._getitemparentpos(self.activeitem)
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
        if under:
            pos = -1
        item = self.tree.add_to_parent(newkey, new_title, root, pos)
        if extra_title:
            subkey = newkey + 1
            self.itemdict[subkey] = (extra_title, "")
            item = self.add_to_parent(subkey, extra_title, item)
        for idx, view in enumerate(self.views):
            if idx != self.opts["ActiveView"]:
                subitem = []
                if extra_title:
                    subitem.append((subkey, []))
                view.append((newkey, subitem))
        self.set_project_dirty(True)
        self._finish_add(root, item)

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
        current = self.tree._getselecteditem() # self.activeitem kan niet?
        if current == self.root:
            self.show_message("Can't do this with root", "DocTree")
            return
        go_on = True
        if cut and not retain:
            go_on = self._confirm("DocTree",
                "Are you sure you want to remove this item?")
        if not go_on:
            return

        self.cut_from_itemdict = []
        if retain:
            self.copied_item, itemlist = getsubtree(self.tree, current)
            self.cut_from_itemdict = [(int(x), self.itemdict[int(x)]) for x in itemlist]
            self.add_node_on_paste = True
        if not cut:
            return

        self.add_node_on_paste = False
        prev = self.tree._removeitem(current)
        self.activeitem = None
        self._removed = [x[0] for x in self.cut_from_itemdict]
        for ix, item in enumerate(self.opts["ActiveItem"]):
            if item in self._removed:
                self.opts["ActiveItem"][ix] = self.tree._getitemtext(prev)
        for ix, view in enumerate(self.views):
            if ix != self.opts["ActiveView"]:
                self._updateview(view)
        self.set_project_dirty(True)
        self._finish_copy(prev)

    def _popitems(self, current, itemlist):
        """recursieve routine om de structuur uit de itemdict en de
        niet-actieve views te verwijderen
        """
        ref = self.tree._getitemtext(current)
        ## try:
        data = self.itemdict.pop(ref)
        ## except KeyError:
            ## pass
        ## else:
        itemlist.append((ref, data))
        for kid in self.tree._getitemkids(current):
            self._popitems(kid, itemlist)

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
        def add_to_view(item, struct):
            titel, key, children = item
            kids = []
            struct.append((int(key), kids))
            for child in children:
                add_to_view(child, kids)
        current = self.tree._getselecteditem()
        # als het geselecteerde item het top item is moet het automatisch below worden
        # maar dan wel als eerste  - of het moet niet mogen
        if current == self.root and not below:
            self.show_message('Kan alleen *onder* de root kopiëren', 'DocTree')
            return
        if not self.copied_item:
            return
        copied_item = self.copied_item
        if self.add_node_on_paste:
            # met behulp van cut_from_itemdict nieuwe toevoegingen aan itemdict maken
                # - voor elk item nieuwe key opvoeren met dezelfde data value
                # - bij elke bestaande key de nieuwe key onthouden
            keymap = {}
            newkey = max(self.itemdict.keys()) + 1
            for key, item in self.cut_from_itemdict:
                title, text = item
                self.itemdict[newkey] = (title, text)
                keymap[key] = newkey
                newkey += 1
            # kopie van copied_item maken met vervangen van oude key door nieuwe key
            # geen add_nodes en itemdict nodig: itemdict hoeft niet tijdens verloop te worden aangevuld
            def replace_keys(item, keymap):
                item = list(item)
                oldkey = int(item[1])
                item[1] = keymap[oldkey]
                hlp = []
                for subitem in item[2]:
                    subitem = replace_keys(subitem, keymap)
                    hlp.append(subitem)
                item[2] = hlp
                return tuple(item)
            copied_item = replace_keys(copied_item, keymap)

        if below:
            putsubtree(self.tree, current, *copied_item)
        else:
            add_to, pos = self.tree._getitemparentpos(current)
            if before:
                pos -= 1
            putsubtree(self.tree, add_to, *copied_item, pos=pos)
        if self.add_node_on_paste:
            # het copied_item in eventuele andere views ook toevoegen
            for ix, view in enumerate(self.views):
                if ix != self.opts["ActiveView"]:
                    titel, key, children = copied_item
                    struct = []
                    for child in children:
                        add_to_view(child, struct)
                    view.append((int(key), struct))
        else:
            self.add_node_on_paste = True
        self.set_project_dirty(True)
        self._finish_paste(current)

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
        new = self.ask_title('Nieuwe titel voor het huidige item:',
            self.tree._getitemtitle(item))
        if not new: # titel leegmaken - moet ik dan niet als een fout melden?
            return
        self.set_project_dirty(True)
        new_title, extra_title = new
        self.tree._setitemtitle(self.activeitem, new_title)
        if item == self.root:
            self.opts['RootTitle'] = new_title
            return
        ref = self.tree._getitemtext(self.activeitem)
        old_title, data = self.itemdict[ref]
        self.itemdict[ref] = (new_title, data)
        if extra_title:
            subref = int(ref) + 1
            while subref in self.itemdict:
                subref += 1
            self.itemdict[subref] = (extra_title, data)
            sub_item = self.tree.add_to_parent(subref, extra_title, self.activeitem)
            item = sub_item
            for idx, view in enumerate(self.views):
                if idx != self.opts["ActiveView"]:
                    check_item(view, ref, subref)
        self._finish_rename(item, root)

    def _expand(self, recursive=False):
        raise NotImplementedError('expand {}'.format('all' if recursive else 'item'))

    def _collapse(self, recursive=False):
        raise NotImplementedError('collapse {}'.format('all' if recursive else 'item'))

    def expand_item(self):
        self._expand()

    def collapse_item(self):
        self._collapse()

    def expand_all(self):
        self._expand(recursive=True)

    def collapse_all(self):
        self._collapse(recursive=True)

    def ask_title(self, _title, _text):
        """vraag titel voor item"""
        ok, data = self._get_name(_title, 'DocTree', _text)
        if ok:
            if data:
                try:
                    new_title, extra_title = data.split(" \\ ")
                except ValueError:
                    new_title, extra_title = data, ""
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
        self._reorder_items(root, recursive)
        self.set_project_dirty(True)

    def _reorder_items(self, root, recursive = False):
        "(re)order_items"
        raise NotImplementedError

    def order_this(self, event = None):
        """order items directly under current level"""
        self.reorder_items(self.activeitem)

    def order_lower(self, event = None):
        """order items under current level and below"""
        self.reorder_items(self.activeitem, recursive = True)

    def next_note(self, event = None):
        """move to next item"""
        if not self._set_next_item():
            self.show_message("Geen volgend item op dit niveau", "DocTree")

    def prev_note(self, event = None):
        """move to previous item"""
        if not self._set_prev_item():
            self.show_message("Geen vorig item op dit niveau", "DocTree")

    def check_active(self, message = None):
        """zorgen dat de editor inhoud voor het huidige item bewaard wordt in de treectrl"""
        if self.activeitem:
            if self.editor._check_dirty():
                if message:
                    self.show_message(message, 'Doctree')
                ref = self.tree._getitemtext(self.activeitem)
                content = self.editor.get_contents()
                try:
                    titel, tekst = self.itemdict[int(ref)]
                except (KeyError, ValueError):
                    if content:
                        self.tree._setitemtext(self.root, content) # gui
                        self.opts["RootData"] = str(content)
                else:
                    self.itemdict[int(ref)] = (titel, content)
                self.editor._mark_dirty(False)
                self.set_project_dirty(True)

    def activate_item(self, item):
        """meegegeven item "actief" maken (accentueren en in de editor zetten)"""
        self.activeitem = item
        ref = self.tree._getitemtext(item)
        try:
            titel, tekst = self.itemdict[ref]
        except (KeyError, ValueError):
            self.editor.set_contents(str(ref))
        else:
            self.editor.set_contents(tekst) # , titel)
        self.editor._openup(True)

    def info_page(self, event = None):
        """help -> about"""
        info = [
            "DocTree door Albert Visser",
            "Uitgebreid electronisch notitieblokje",
            "PyQt versie",
            ]
        self.show_message("\n".join(info), "DocTree")

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
            "Shift-Ctrl-I\t\t- initialiseer (nieuw) notitiebestand",
            "Ctrl-Q, Esc\t\t- opslaan en sluiten",
            "Ctrl-H\t\t- verbergen in system tray",
            "",
            "F1\t\t- deze (help)informatie",
            "F2\t\t- wijzig notitie titel",
            "Shift-F2\t\t- wijzig root titel",
            "",
            "See menu for editing keys",
            ]
        self.show_message("\n".join(info), "DocTree")
