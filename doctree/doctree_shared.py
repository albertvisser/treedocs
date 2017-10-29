# -*- coding: utf-8 -*-
"""DocTree gui-onafhankelijk gedeelte
"""
import os
import pathlib
import sys
try:
    import cPickle as pck  # Python 2
except ImportError:
    import pickle as pck
else:
    str = unicode
import shutil
from datetime import datetime
import zipfile as zip
## import pprint
import logging
## import datetime as dt
import bs4 as bs
HERE = pathlib.Path(__file__).parent.resolve()
logging.basicConfig(filename=str(HERE / 'logs' / 'doctree.log'),
                    level=logging.DEBUG, format='%(asctime)s %(message)s')


def init_opts():
    """return dict of options and their initial values
    """
    return {"Application": "DocTree", "NotifyOnSave": True,
            "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
            "ActiveItem": [0], "ActiveView": 0, "ViewNames": ["Default"],
            "RootTitle": "MyNotes", "RootData": "", "ImageCount": 0}


def log(message):
    "write message to logfile"
    if 'DEBUG' in os.environ and os.environ['DEBUG'] != "0":
        logging.info(message)


def getsubtree(tree, item, itemlist=None):
    """recursieve functie om de structuur onder de te verplaatsen data
    te onthouden"""
    if itemlist is None:
        itemlist = []
    titel, key = tree.getitemdata(item)
    itemlist.append(key)
    log(' getsubtree item {}, {}'.format(titel, key))
    subtree = []
    for kid in tree.getitemkids(item):
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
    return new  # , itemdict


def add_newitems(copied_item, cut_from_itemdict, itemdict):
    """met behulp van cut_from_itemdict nieuwe toevoegingen aan itemdict maken
        - voor elk item nieuwe key opvoeren met dezelfde data value
        - bij elke bestaande key de nieuwe key onthouden
    kopie van copied_item maken met vervangen van oude key door nieuwe key
    """
    keymap = {}
    try:
        newkey = max(itemdict.keys()) + 1
    except ValueError:
        newkey = 0
    log("add_newitem: cut_from_itemdict is {}".format(cut_from_itemdict))
    for key, item in cut_from_itemdict:
        title, text = item
        itemdict[newkey] = (title, text)
        keymap[key] = newkey
        newkey += 1
    log("add_newitem: keymap is {}".format(keymap))
    copied_item = replace_keys(copied_item, keymap)
    used_keys = list(keymap.values())
    return copied_item, itemdict, used_keys


def replace_keys(item, keymap):
    """kopie van toe te voegen deelstructuur maken met vervangen van oude key
    door nieuwe key volgens keymap
    """
    item = list(item)   # mutable maken
    oldkey = int(item[1])
    item[1] = keymap[oldkey]
    hlp = []
    for subitem in item[2]:
        subitem = replace_keys(subitem, keymap)
        hlp.append(subitem)
    item[2] = hlp
    return tuple(item)


def add_item_to_view(item, view):
    """nieuwe deelstructuur achteraan toevoegen aan tree view
    """
    def add_to_view(item, struct):
        "do so recursively"
        _, key, children = item
        kids = []
        struct.append((int(key), kids))
        for child in children:
            add_to_view(child, kids)
    _, key, children = item
    struct = []
    for child in children:
        add_to_view(child, struct)
    view.append((int(key), struct))


def _write(filename, opts, views, itemdict, extra_images=None):
    """settings en tree data in een structuur omzetten en opslaan

    images contained are saved in a separate zipfile"""
    nt_data = {0: opts, 1: views, 2: itemdict}
    zipfile = filename.with_suffix('.zip')
    try:
        shutil.copyfile(str(filename), str(filename) + ".bak")
        shutil.copyfile(str(zipfile), str(zipfile) + ".bak")
    except IOError as err:
        print(err)
    with filename.open("wb") as f_out:
        pck.dump(nt_data, f_out, protocol=2)

    if extra_images is None:
        # scan de itemdict af op image files en zet ze in een list
        _filenames = []
        for _, data in nt_data[2].values():
            names = [img['src'] for img in bs.BeautifulSoup(data).find_all('img')]
            _filenames.extend(names)
        ## fname = os.path.basename(filename)
        mode = "w"
    else:
        _filenames = extra_images
        mode = "a"
    # add extra images to the zipfile
    path = filename.parent  # eventueel eerst absoluut maken
    zipped = []
    with zip.ZipFile(str(zipfile), mode) as _out:
        for name in _filenames:
            if name.startswith(str(filename)):
                ## _out.write(os.path.join(path, name), arcname=os.path.basename(name))
                _out.write(str(path / name), arcname=pathlib.Path(name).name)
                zipped.append(name)
    return zipped


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
    def __init__(self):  # , parent=None, fnaam=""):
        self.project_dirty = False  # need to set this directly here
        self.add_node_on_paste = False
        self.has_treedata = False
        self._filenames = []
        self.copied_item, self.cut_from_itemdict = (), []

    def _get_menu_data(self):
        return (
            ("&Main", (
                ("Re&Load", self.reread, 'Ctrl+R', 'icons/filerevert.png',
                 'Reread notes file'),
                ("&Open", self.open, 'Ctrl+O', 'icons/fileopen.png',
                 "Choose and open notes file"),
                ("&Init", self.new, 'Shift+Ctrl+I', 'icons/filenew.png',
                 'Start a new notes file'),
                ("&Save", self.save, 'Ctrl+S', 'icons/filesave.png', 'Save notes file'),
                ("Save as", self.saveas, 'Shift+Ctrl+S', 'icons/filesaveas.png',
                 'Name and save notes file'),
                (),
                ("&Root title", self.rename_root, 'Shift+F2', '', 'Rename root'),
                ("Items sorteren", self.order_top, '', '',
                 'Bovenste niveau sorteren op titel'),
                ("Items recursief sorteren", self.order_all, '', '',
                 'Alle niveaus sorteren op titel'),
                (),
                ("&Hide", self.hide_me, 'Ctrl+H', '', 'verbergen in system tray'),
                ("Switch pane", self.change_pane, 'Ctrl+Tab', '',
                 'switch tussen tree en editor'),
                (),
                ("e&Xit", self.afsl, 'Ctrl+Q,Escape', 'icons/exit.png', 'Exit program'))),
            ("&Note", (
                ("&New", self.add_item, 'Ctrl+N', '', 'Add note (below current level)'),
                ("&Add", self.insert_item, 'Insert', '', 'Add note (after current)'),
                ("New &under root", self.root_item, 'Shift+Ctrl+N', '',
                 'Add note (below root)'),
                ("&Delete", self.delete_item, 'Ctrl+D,Delete', '', 'Remove note'),
                ("&Move", self.move_to_file, 'Ctrl+M', '',
                 'Copy note to other file and remove'),
                (),
                ("Edit &Title", self.rename_item, 'F2', '', 'Rename current note'),
                ("Subitems &sorteren", self.order_this, '', '',
                 'Onderliggend niveau sorteren op titel'),
                ("Subitems &recursief sorteren", self.order_lower, '', '',
                 'Alle onderliggende niveaus sorteren op titel'),
                (),
                ("&Forward (same level)", self.next_note, 'Ctrl+PgDown', '',
                 'View next note'),
                ("For&ward (regardless)", self.next_note_any, 'Shift+Ctrl+PgDown', '',
                 'View next note'),
                ("&Back (same level)", self.prev_note, 'Ctrl+PgUp', '',
                 'View previous note'),
                ("Bac&k (regardless)", self.prev_note_any, 'Shift+Ctrl+PgUp', '',
                 'View previous note'))),
            ("&View", (
                ('&New View', self.add_view, '', '',
                 'Add an alternative view (tree) to this data'),
                ('&Rename Current View', self.rename_view, '', '',
                 'Rename the current tree view'),
                ('&Delete Current View', self.remove_view, '', '',
                 'Remove the current tree view'),
                (),
                ('Next View', self.next_view, 'Ctrl++', '',
                 'Switch to the next view in the list'),
                ('Prior View', self.prev_view, 'Ctrl+-', '',
                 'Switch to the previous view in the list'),
                ())),  # label, handler, shortcut, icon, info
            ('&Tree', (
                ('&Undo', self.tree_undo, 'Ctrl+Alt+Z', '', 'Undo last operation'),
                ('&Redo', self.tree_redo, 'Ctrl+Alt+Y', '', 'Redo last undone operation'),
                (),
                ('Cu&t', self.cut_item, 'Ctrl+Alt+X', 'icons/treeitem-cut.png',
                 'Copy the selection and delete from tree'),
                ('&Copy', self.copy_item, 'Ctrl+Alt+C', 'icons/treeitem-copy.png',
                 'Just copy the selection'),
                ('&Paste Under', self.paste_item_below, 'Ctrl+Alt+V',
                 'icons/treeitem-paste.png',
                 'Paste the copied selection under the selected item'),
                ('&Paste After', self.paste_item_after, 'Shift+Ctrl+Alt+V', '',
                 'Paste the copied selection after the selected item (same parent)'),
                ('&Paste Before', self.paste_item, '', '',
                 'Paste the copied selection before the selected item (same parent)'),
                (),
                ('Expand', self.expand_item, 'Ctrl+<', '', 'Expand tree item'),
                ('Collapse', self.collapse_item, 'Ctrl+>', '', 'Collapse tree item'),
                ('Expand all', self.expand_all, 'Ctrl+Alt+<', '', 'Expand all subitems'),
                ('Collapse all', self.collapse_all, 'Ctrl+Alt+>', '',
                 'Collapse all subitems'))),
            ('T&ext', (
                ('&Undo', self.editor.undo, 'Ctrl+Z', 'icons/edit-undo.png',
                 'Undo last operation'),
                ('&Redo', self.editor.redo, 'Ctrl+Y', 'icons/edit-redo.png',
                 'Redo last undone operation'),
                (),
                ('Cu&t', self.editor.cut, 'Ctrl+X', 'icons/edit-cut.png',
                 'Copy the selection and delete from text'),
                ('&Copy', self.editor.copy, 'Ctrl+C', 'icons/edit-copy.png',
                 'Just copy the selection'),
                ('&Paste', self.editor.paste, 'Ctrl+V', 'icons/edit-paste.png',
                 'Paste the copied selection'),
                (),
                ('Select A&ll', self.editor.selectAll, 'Ctrl+A', "",
                 'Select the entire text'),
                ("&Clear All (can't undo)", self.editor.clear, '', '',
                 'Delete the entire text'))),
            ('&Format', (
                ('&Bold', self.editor.text_bold, 'Ctrl+B', 'icons/format-text-bold.png',
                 'CheckB'),
                ('&Italic', self.editor.text_italic, 'Ctrl+I',
                 'icons/format-text-italic.png', 'CheckI'),
                ('&Underline', self.editor.text_underline, 'Ctrl+U',
                 'icons/format-text-underline.png', 'CheckU'),
                ('Strike&through', self.editor.text_strikethrough, 'Ctrl+~',
                 'icons/format-text-strikethrough.png', 'CheckS'),
                (),
                ('Align &Left', self.editor.align_left, 'Shift+Ctrl+L',
                 'icons/format-justify-left.png', 'Check'),
                ('C&enter', self.editor.align_center, 'Shift+Ctrl+C',
                 'icons/format-justify-center.png', 'Check'),
                ('Align &Right', self.editor.align_right, 'Shift+Ctrl+R',
                 'icons/format-justify-right.png', 'Check'),
                ('&Justify', self.editor.text_justify, 'Shift+Ctrl+J',
                 'icons/format-justify-fill.png', 'Check'),
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
                ("&Enlarge text", self.editor.enlarge_text, 'Ctrl+Up', '',
                 'Use bigger letters'),
                ("&Shrink text", self.editor.shrink_text, 'Ctrl+Down', '',
                 'Use smaller letters'),
                (),
                ("&Color...", self.editor.text_color, '', '', 'Set/change colour'),
                ("&Background...", self.editor.background_color, '', '',
                 'Set/change background colour'))),
            ('&Search', (
                ('&Current text', self.search, 'Ctrl+F', '', "Search in current text"),
                ('All t&exts', self.search_texts, 'Shift+Ctrl+F', '',
                 "Search in all texts"),
                ('All t&itles', self.search_titles, 'Ctrl+Alt+F', '',
                 "Search in all titles"),
                (),
                ('&Next', self.find_next, 'F3', '', 'Repeat search forwards'),
                ('&Previous', self.find_prev, 'Shift+F3', '',
                 'Repeat search backwards'))),
            ("&Help", (
                ("&About", self.info_page, '', '', 'About this application'),
                ("&Keys", self.help_page, 'F1', '', 'Keyboard shortcuts'))))

    def show_message(self, text='', title=''):
        "voor elke gui variant apart te implementeren"
        print('{}: {}'.format(title, text))

    def show_statusbar_message(self, text):
        "voor elke gui variant apart te implementeren"
        print('status: {}'.format(text))

    def change_pane(self):
        "wissel tussen tree en editor"
        raise NotImplementedError

    def set_project_dirty(self, value):
        "indicate that there have been changes"
        self.project_dirty = value
        self.set_title()

    def set_title(self):
        """standaard titel updaten"""
        raise NotImplementedError

    def open(self):
        "afhandelen Menu > Open / Ctrl-O"
        if not self.save_needed():
            return
        dirname = str(self.project_file)
        ok, filename = self.getfilename("DocTree - choose file to open", dirname)
        if not ok:
            return
        self.project_file = pathlib.Path(filename)
        err = self.read()
        if err:
            self.show_message(title="Error", text=err)
        else:
            self.show_statusmessage('{} gelezen'.format(str(self.project_file)))

    def new(self):
        "Afhandelen Menu - Init / Ctrl-I"
        if not self.save_needed():
            return False
        dirname = str(self.project_file.parent)
        ok, filename = self.getfilename("DocTree - enter name for new file",
                                        dirname, save=True)
        if not ok:
            return
        filename = pathlib.Path(filename)
        test = filename.suffix
        if test != '.pck':
            filename = filename.with_suffix('.pck')
        self.project_file = filename
        self.views = [[]]
        self.viewcount = 1
        self.itemdict = {}
        self._filenames = []
        self.opts = init_opts()
        self.has_treedata = True
        self.set_title()
        self.set_project_dirty(False)
        return True

    def save_needed(self):
        """check if anything has changed"""
        return self.has_treedata and self.project_dirty

    def treetoview(self):
        """zet de visuele tree om in een tree om op te slaan"""
        def lees_item(item):
            """recursieve functie om de data in een pickle-bare structuur om te zetten"""
            textref = self.tree.getitemkey(item)
            if item == self.activeitem:
                self.opts["ActiveItem"][self.opts["ActiveView"]] = textref
            kids = [lees_item(x) for x in self.tree.getitemkids(item)]
            return textref, kids
        data = [lees_item(x) for x in self.tree.getitemkids(self.root)]
        return data

    def viewtotree(self):
        """zet de geselecteerde view om in een visuele tree"""
        def maak_item(parent, key, children=None):
            """recursieve functie om de TreeCtrl op te bouwen vanuit de opgeslagen data"""
            item_to_activate = None
            if children is None:
                children = []
            titel = self.itemdict[key][0]
            tree_item = self.tree.add_to_parent(key, titel, parent)
            if key == self.opts["ActiveItem"][self.opts['ActiveView']]:
                item_to_activate = tree_item
            for child in children:
                _, y = maak_item(tree_item, *child)
                if y is not None:
                    item_to_activate = y
            return key, item_to_activate
        item_to_activate = None
        current_view = self.views[self.opts['ActiveView']]
        for item in current_view:
            _, y = maak_item(self.root, *item)
            if y is not None:
                item_to_activate = y
        return item_to_activate

    def read(self, other_file=''):
        """settings dictionary lezen, opgeslagen data omzetten naar tree"""
        if not other_file:
            self.has_treedata = False
        self.opts = init_opts()
        mld = ''

        # determine the name of the file to read and read + unpickle it if possible,
        # otherwise cancel
        infile = other_file or self.project_file
        if not infile:
            return
        try:
            f_in = infile.open("rb")
        except IOError:
            return "couldn't open {}".format(str(infile))
        with f_in:
            try:
                nt_data = pck.load(f_in)
            except EOFError:
                return "couldn't load data from {}".format(str(infile))

        # read/init/check settings if possible, otherwise cancel
        ## print(nt_data[0])
        test = nt_data[0].get("Application", None)
        if test and test != 'DocTree':
            return "{} is not a valid Doctree data file".format(str(infile))

        # read views
        try:
            views = list(nt_data[1])
        except KeyError:
            views = [[]]
        viewcount = len(views)

        # read itemdict
        try:
            itemdict = nt_data[2]
        except KeyError:
            itemdict = {}

        # exit if meant for file to copy stuff to
        if other_file:
            return nt_data[0], views, viewcount, itemdict

        # make settings, views and itemdict into attributes
        for key, value in nt_data[0].items():
            if key == 'RootData' and value is None:
                value = ""
            self.opts[key] = value
        self.views, self.viewcount, self.itemdict = views, viewcount, itemdict

        # if possible, build a list of referred-to image files
        ## path = os.path.dirname((self.project_file))
        path = str(self.project_file.parent)
        self._filenames = []
        err = FileNotFoundError if sys.version >= '3.3' else OSError
        try:
            with zip.ZipFile(str(self.project_file.with_suffix('.zip'))) as _in:
                _in.extractall(path=path)
                self._filenames = _in.namelist()
        except err:
            pass

        # finish up (set up necessary attributes etc)
        self._read()  # do gui-specific stuff
        item_to_activate = self.viewtotree()
        self.has_treedata = True
        ## self.set_title()
        self.set_project_dirty(False)
        self._finish_read(item_to_activate)

    def _read(self):
        "placeholder"
        raise NotImplementedError

    def reread(self):
        """afhandelen Menu > Reload (Ctrl-R)"""
        if not self.save_needed():
            return
        ## if self._ok_to_reload():
        self.read()
        self.show_statusmessage('{} herlezen'.format(str(self.project_file)))

    def _ok_to_reload(self):
        "placeholder"
        return NotImplementedError

    def save(self, meld=True):
        """afhandelen Menu > save"""
        if self.project_file:
            self.write(meld=meld)
        else:
            self.saveas()
        self.show_statusmessage('{} opgeslagen'.format(str(self.project_file)))

    def write(self, meld=True):
        """settings en tree data in een structuur omzetten en opslaan"""
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self._filenames = _write(self.project_file, self.opts, self.views,
                                 self.itemdict)
        self.set_project_dirty(False)
        if meld:
            save_text = str(self.project_file) + " is opgeslagen"
            self.confirm(setting="NotifyOnSave", textitem=save_text)

    def saveas(self):
        """afhandelen Menu > Save As"""
        dirname = str(self.project_file)
        ok, filename = self.getfilename("DocTree - save file as:", dirname, save=True)
        if ok:
            filename = pathlib.Path(filename)
            test = filename.suffix
            if test != '.pck':
                filename = filename.with_suffix('.pck')
            self.project_file = filename
            self.write()
            self.set_title()

    def hide_me(self):
        """applicatie verbergen"""
        raise NotImplementedError

    def revive(self):
        """applicatie weer zichtbaar maken"""
        raise NotImplementedError

    def afsl(self):
        "remove temporary files on exit (as they have been zipped)"
        for name in self._filenames:
            try:
                os.remove(name)
            except FileNotFoundError:
                pass

    def add_view(self):
        "handles Menu > View > New view"
        self.check_active()
        self.opts["ActiveItem"][self.opts["ActiveView"]] = self.tree.getitemdata(
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
        ## self.set_title()
        self.set_project_dirty(True)
        self._finish_add_view()

    def _set_activeitem_for_view(self):
        "placeholder"
        raise NotImplementedError

    def _update_newview(self, new_view):
        "view menu bijwerken n.a.v. toevoeging nieuwe view"
        raise NotImplementedError

    def _rebuild_root(self):
        "tree leegmaken en root opnieuw neerzetten"
        raise NotImplementedError

    def rename_view(self):
        "handles Menu > View > Rename current view"
        oldname = self.opts["ViewNames"][self.opts["ActiveView"]]
        ok, newname = self._get_name('Geef een nieuwe naam voor de huidige view',
                                     'DocTree', oldname)
        if ok and newname != oldname:
            self._add_view_to_menu(newname)
            self.opts["ViewNames"][self.opts["ActiveView"]] = newname
            self.set_project_dirty(True)
            ## self.set_title()

    def _get_name(self, caption, title, oldname):
        "placeholder"
        raise NotImplementedError

    def _add_view_to_menu(self, newname):
        "placeholder"
        raise NotImplementedError

    def next_view(self, prev=False):  # voorlopig even overgeslagen
        """cycle to next view if available (default direction / forward)"""
        raise NotImplementedError

    def prev_view(self):
        """cycle to previous view (alternate direction / backward)"""
        self.next_view(prev=True)

    def select_view(self):
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

    def remove_view(self):
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
        self._update_removedview(viewname)
        self._rebuild_root()
        self.set_project_dirty(True)
        ## self.set_title()
        self._finish_remove_view(self.viewtotree())

    def _confirm(self, title, text):
        "get confirmation"
        ok = input('{}: {} (y/N)'.format(title, text))
        ok = True if ok.upper() == 'Y' else False
        return ok

    def _update_removedview(self):
        "view menu bijwerken n.a.v. verwijderen view"
        raise NotImplementedError

    def rename_root(self):
        """afhandelen Menu > Rename Root (Shift-Ctrl-F2"""
        ok, data = self._get_name('Geef nieuwe titel voor het root item:',
                                  'DocTree', self.opts['RootTitle'])
        if ok:
            self.set_project_dirty(True)
            self.opts['RootTitle'] = data
            self.tree.setitemtitle(self.root, data)

    def add_item(self):
        """nieuw item toevoegen (default: onder het geselecteerde)

        separate entry point for menu callback
        """
        self._add_item()

    def _add_item(self, root=None, under=True):
        "nieuw item toevoegen"
        test = self._check_addable()
        if test:
            new_title, extra_titles = test
            pos = -1  # doesn't matter for now
            self.do_additem(root, under, pos, new_title, extra_titles)

    def _check_addable(self):
        """bepaal een titel voor het nieuwe (en eventueel onderliggende) item
        """
        title = "Geef een titel op voor het nieuwe item"
        text = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        new = self.ask_title(title, text)
        if not new:
            return False
        new_title, extra_titles = new
        # stel de inhoud van het item onder de cursor veilig
        self.check_active()
        return new_title, extra_titles

    def do_additem(self, root, under, origpos, new_title, extra_titles):
        """toevoegen nieuw item
        """
        log('in shared.do_additem')
        # bepaal nieuwe key in itemdict
        newkey = len(self.itemdict)
        while newkey in self.itemdict:
            newkey += 1
        # voeg nieuw item toe aan itemdict
        self.itemdict[newkey] = (new_title, "")
        # voeg nieuw item toe aan visual tree
        # bepaal eerst de parent voor het nieuwe item
        log('root is {} ({}), under is {}, origpos is {}'.format(root, root.text(0),
                                                                 under, origpos))
        if under:
            ## if root is None:
                ## root = self.activeitem or self.root
            parent = root or self.activeitem or self.root
            pos = -1
        else:
            ## root, pos = getitemparentpos(self.activeitem)
            parent, pos = self.tree.getitemparentpos(root)
            log("na getitemparentpos: root, pos is {}, {}".format(parent, pos))
            if origpos == -1:
                pos += 1    # we want to insert after, not before
                if pos == parent.childCount():
                    pos = -1
            else:
                pos = origpos
        log('parent, pos is {} ({}), {}'.format(parent, parent.text(0), pos))
        item = self.tree.add_to_parent(newkey, new_title, parent, pos)
        new_item = item
        # doe hetzelfde met het via \ toegevoegde item
        extra_keys = []
        subkey = newkey
        while extra_titles:
            subkey += 1
            self.itemdict[subkey] = (extra_titles[0], "")
            item = self.tree.add_to_parent(subkey, extra_titles[0], item)
            extra_keys.append(subkey)
            extra_titles = extra_titles[1:]
        # voeg de items ook toe aan de niet zichtbare views
        subitem = []
        for subkey in reversed(extra_keys):
            subitem = [(subkey, subitem)]
        for idx, view in enumerate(self.views):
            if idx != self.opts["ActiveView"]:
                view.append((newkey, subitem))
        # data is gewijzigd
        self.set_project_dirty(True)
        # afmaken
        self._finish_add(parent, item)
        # resultaat t.b.v. undo/redo mechanisme
        return newkey, extra_keys, new_item, subitem

    def root_item(self):
        """nieuw item toevoegen onder root"""
        self._add_item(root=self.root)

    def insert_item(self):
        """nieuw item toevoegen *achter* het geselecteerde (en onder diens parent)"""
        self._add_item(under=False)

    def cut_item(self):
        "cut = copy with removing item from tree"
        self._copy_item(cut=True)

    def delete_item(self):
        "delete = copy with removing item from tree and memory"
        self._copy_item(cut=True, retain=False)

    def copy_item(self):
        "copy: retain item in tree and in memory"
        self._copy_item()

    def _copy_item(self, cut=False, retain=True, to_other_file=None):
        """start copy/cut/delete action

        parameters: cut: remove item from tree (True for cut, delete and move)
                    retain: remember item for pasting (True for cut and copy)
                    other_file:
        """
        test = self._check_copyable(cut, retain, to_other_file)
        if test:
            current = test
            self.do_copyaction(cut, retain, current)  # to_other_file)

    def _check_copyable(self, cut, retain, to_other_file):
        "can we copy from here?"
        if to_other_file:
            current = to_other_file
        else:
            current = self.tree.getselecteditem()
            if current == self.root:
                self.show_message("Can't do this with root", "DocTree")
                return False
        # are-you-sure message + cancel this action if applicable
        go_on = True
        if cut and not retain and not to_other_file:
            go_on = self._confirm("DocTree", "Are you sure you want to remove this item?")
        if go_on:
            return current
        else:
            return go_on

    def do_copyaction(self, cut, retain, current):  # to_other_file):
        "do the copying"
        # create a copy buffer
        # self.cut_from_itemdict = []
        copied_item, itemlist = getsubtree(self.tree, current)
        cut_from_itemdict = [(int(x), self.itemdict[int(x)]) for x in itemlist]
        oldloc = None  # alleen interessant bij undo van cut/delete
        if retain:
            self.copied_item = copied_item
            self.cut_from_itemdict = cut_from_itemdict
            self.add_node_on_paste = True
        if cut:
            # remove item (and subitems) from tree and itemdict
            # they're buffered in (self.)cut_from_itemdict because we still need them
            self.add_node_on_paste = False
            oldloc, prev = self.tree.removeitem(current, cut_from_itemdict)
            self.activeitem = None

            # remove item(s) from view(s)
            removed = [x[0] for x in cut_from_itemdict]
            for ix, item in enumerate(self.opts["ActiveItem"]):
                if item in removed:
                    self.opts["ActiveItem"][ix] = self.tree.getitemkey(prev)
            for ix, view in enumerate(self.views):
                if ix != self.opts["ActiveView"]:
                    self._updateview(view, removed)

            # finish up
            self.set_project_dirty(True)
            self._finish_copy(prev)  # do gui-specific stuff

        return copied_item, oldloc, cut_from_itemdict

    def popitems(self, current, itemlist):
        """recursieve routine om de structuur uit de itemdict en de
        niet-actieve views te verwijderen
        """
        ref = self.tree.getitemkey(current)
        ## try:
        self.itemdict.pop(ref)
        ## except KeyError:
            ## pass
        ## else:
        for kid in self.tree.getitemkids(current):
            self.popitems(kid, itemlist)

    def _updateview(self, view, removed):
        "recursieve routine om de view bij te werken"
        klaar = False
        for idx, item in reversed(list(enumerate(view))):
            itemref, subview = item
            if itemref in removed:
                self._updateview(subview, removed)
                if not subview:
                    view.pop(idx)
                else:
                    view[idx] = subview[0]
                klaar = True
            else:
                klaar = self._updateview(subview, removed)
            ## if klaar:
                ## break
        return klaar

    def paste_item(self):
        "paste before"
        self._paste_item()

    def paste_item_after(self):
        "paste after instead of before"
        self._paste_item(before=False)

    def paste_item_below(self):
        "paste below instead of before"
        self._paste_item(below=True)

    def _paste_item(self, before=True, below=False):
        "start paste actie"
        test = self._check_pasteable(below)  # before,
        if test:
            current = test
            self.do_pasteitem(before, below, current)

    def _check_pasteable(self, below):  # , before
        "can we paste here?"
        current = self.tree.getselecteditem()
        # als het geselecteerde item het top item is moet het automatisch below worden
        # maar dan wel als eerste  - of het moet niet mogen
        if current == self.root and not below:
            self.show_message('Kan alleen *onder* de root kopiëren', 'DocTree')
            return False
        if not self.copied_item:
            self.show_message('Nothing to paste', 'DocTree')
            return False
        return current

    def do_pasteitem(self, before, below, current):
        "do the pasting"
        # items toevoegen aan itemdict
        if not self.add_node_on_paste:
            pasted_item = self.copied_item
            used_keys = self.add_items_back()
        else:
            pasted_item, self.itemdict, used_keys = add_newitems(
                self.copied_item, self.cut_from_itemdict, self.itemdict)
        # items toevoegen aan visual tree
        if below:
            putsubtree(self.tree, current, *pasted_item)
            used_parent = (current, -1)
        else:
            add_to, pos = self.tree.getitemparentpos(current)
            if not before:
                pos += 1
            putsubtree(self.tree, add_to, *pasted_item, pos=pos)
            used_parent = (add_to, pos)
        # indien nodig het copied_item in eventuele andere views ook toevoegen
        if self.add_node_on_paste:
            for ix, view in enumerate(self.views):
                if ix != self.opts["ActiveView"]:
                    add_item_to_view(pasted_item, view)
        else:
            self.add_node_on_paste = True   # for the next time

        ## self.copied_item = pasted_item
        self.set_project_dirty(True)
        self._finish_paste(current)
        return used_keys, used_parent

    def add_items_back(self):
        """ de/het verwijderde itemdict item(s) weer onder dezelfde key opvoeren
        """
        keys = []
        for key, item in self.cut_from_itemdict:
            keys.append(key)
            ## title, text = item
            self.itemdict[key] = item  # (title, text)
        # alternatief:
        #   self.itemdict.update({key: item for key, item in self.cut_from_itemdict})
        #   keys = [key for key, item in self.cut_from_itemdict]
        return keys

    def rename_item(self):
        """titel van item wijzigen"""
        def check_item(view, ref, newitem):
            """zoeken waar het subitem moet worden toegevoegd"""
            retval = ""
            for itemref, subview in view:
                if itemref == ref:
                    subview.append(newitem)
                    retval = 'Stop'
                else:
                    retval = check_item(subview, ref, newitem)
                if retval == 'Stop':
                    break
            return retval
        root = item = self.activeitem
        self.check_active()
        new = self.ask_title('Nieuwe titel voor het huidige item:',
                             self.tree.getitemtitle(item))
        if not new:
            return
        self.set_project_dirty(True)
        new_title, extra_titles = new
        self.tree.setitemtitle(self.activeitem, new_title)
        if item == self.root:
            self.opts['RootTitle'] = new_title
            return
        ref = self.tree.getitemkey(self.activeitem)
        old_title, data = self.itemdict[ref]
        self.itemdict[ref] = (new_title, data)
        # toevoegen nieuwe onderliggende items
        if extra_titles:
            subref = int(ref) + 1
            while subref in self.itemdict:
                subref += 1
            extra_keys = []
            item = self.activeitem
            while extra_titles:
                subkey = subref
                self.itemdict[subkey] = (extra_titles[0], data)
                item = self.tree.add_to_parent(subkey, extra_titles[0], item)
                extra_keys.append(subkey)
                subref += 1
                extra_titles = extra_titles[1:]
            # voeg de items ook toe aan de niet zichtbare views
            subitem = []
            for subkey in reversed(extra_keys):
                subitem = [(subkey, subitem)]
            for idx, view in enumerate(self.views):
                if idx != self.opts["ActiveView"]:
                    check_item(view, ref, subitem[0])
        self._finish_rename(item, root)

    def move_to_file(self):
        "afhandelen Menu > Move / Ctrl-M"

        # 0. check the selected item (copied from the copy routine)
        # eventueel check_copyable aanroepen in plaats van dit

        current = self.tree.getselecteditem()  # self.activeitem kan niet?
        if current == self.root:
            self.show_message("Can't do this with root", "DocTree")
            return

        # 1. ask which file to move to (from here you can still cancel the action)

        dirname = str(self.project_file.parent)
        ok, filename = self.getfilename("DocTree - choose file to move the item to",
                                        dirname)
        if not ok:
            return

        # 2. read the file

        other_file = pathlib.Path(filename)
        if not other_file.exists():
            opts = init_opts()
            opts['Version'] = self.opts.get('Version', None)
            views, viewcount, itemdict = [[]], 1, {}
        else:
            opts, views, viewcount, itemdict = self.read(other_file=other_file)

        # 3. cut action on the item

        self._copy_item(cut=True, to_other_file=current)

        # 3a. Make a list of the images contained in self.cut_from_itemdict
        #      so they can be copied over to the other zipfile

        extra_images = []
        for _, data in [x[1] for x in self.cut_from_itemdict]:
            names = [img['src'] for img in bs.BeautifulSoup(data).find_all('img')]
            extra_images.extend(names)

        # 4. paste action on the other file
        #     note that these functions mutate their arguments...

        self.copied_item, itemdict, used_keys = add_newitems(self.copied_item,
                                                             self.cut_from_itemdict,
                                                             itemdict)
        for view in views:
            add_item_to_view(self.copied_item, view)

        # 5. write back the updated structure

        _write(other_file, opts, views, itemdict, extra_images)

    def _expand(self, recursive=False):
        "placeholder"
        raise NotImplementedError('expand {}'.format('all' if recursive else 'item'))

    def _collapse(self, recursive=False):
        "placeholder"
        raise NotImplementedError('collapse {}'.format('all' if recursive else 'item'))

    def expand_item(self):
        "expand one level"
        self._expand()

    def collapse_item(self):
        "collapse one level"
        self._collapse()

    def expand_all(self):
        "expand all levels"
        self._expand(recursive=True)

    def collapse_all(self):
        "collapse all levels"
        self._collapse(recursive=True)

    def ask_title(self, _title, _text):
        """vraag titel voor item (ingesloten backslashes gelden als
        scheidingstekens voor titels van onderliggende items)
        """
        ok, data = self._get_name(_title, 'DocTree', _text)
        if ok:
            if data:
                test = data.split(" \\ ")
                new_title, extra_title = test[0], test[1:]
            else:
                new_title, extra_title = '(untitled)', []
            return new_title, extra_title
        return

    def order_top(self):
        """order items directly under the top level"""
        self.reorder_items(self.root)

    def order_all(self):
        """order items under top level and below"""
        self.reorder_items(self.root, recursive=True)

    def reorder_items(self, root, recursive=False):
        "(re)order_items"
        self._reorder_items(root, recursive)
        self.set_project_dirty(True)

    def _reorder_items(self, root, recursive=False):
        "(re)order_items"
        raise NotImplementedError

    def order_this(self):
        """order items directly under current level"""
        self.reorder_items(self.activeitem)

    def order_lower(self):
        """order items under current level and below"""
        self.reorder_items(self.activeitem, recursive=True)

    def next_note(self):
        """move to next item"""
        if not self._set_next_item():
            self.show_message("Geen volgend item op dit niveau", "DocTree")

    def prev_note(self):
        """move to previous item"""
        if not self._set_prev_item():
            self.show_message("Geen vorig item op dit niveau", "DocTree")

    def next_note_any(self):
        """move to next item"""
        if not self._set_next_item(any_level=True):
            self.show_message("Geen volgend item", "DocTree")

    def prev_note_any(self):
        """move to previous item"""
        if not self._set_prev_item(any_level=True):
            self.show_message("Geen vorig item", "DocTree")

    def check_active(self, message=None):
        """zorgen dat de editor inhoud voor het huidige item bewaard wordt in de treectrl"""
        if self.activeitem:
            if self.editor.check_dirty():
                if message:
                    self.show_message(message, 'Doctree')
                ref = self.tree.getitemkey(self.activeitem)
                content = str(self.editor.get_contents())
                try:
                    titel, tekst = self.itemdict[int(ref)]
                except (KeyError, ValueError):
                    if content:
                        self.tree.setitemtext(self.root, content)
                        self.opts["RootData"] = content
                else:
                    self.itemdict[int(ref)] = (titel, content)
                self.editor.mark_dirty(False)
                self.set_project_dirty(True)

    def activate_item(self, item):
        """meegegeven item "actief" maken (accentueren en in de editor zetten)"""
        self.activeitem = item
        ref = self.tree.getitemkey(item)
        try:
            titel, tekst = self.itemdict[ref]
        except (KeyError, ValueError):
            self.editor.set_contents(str(ref))
        else:
            self.editor.set_contents(tekst)  # , titel)
        self.editor.openup(True)

    def info_page(self):
        """help -> about"""
        info = ["DocTree door Albert Visser",
                "Uitgebreid electronisch notitieblokje",
                "PyQt versie"]
        self.show_message("\n".join(info), "DocTree")

    def help_page(self):
        """help -> keys"""
        info = ["Ctrl-N\t\t- nieuwe notitie onder huidige",
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
                "See menu for editing keys"]
        self.show_message("\n".join(info), "DocTree")

    def confirm(self, setting='', textitem=''):
        "confirm action if necessary"
        if self.opts[setting]:
            print(textitem)

    def tree_undo(self):
        "placeholder"
        pass

    def tree_redo(self):
        "placeholder"
        pass
