"""DocTree: Main program, meant to be gui-toolkit agnostic
"""
# import os
# import sys
import pathlib
import shutil
from datetime import datetime
import tempfile
# import pickle as pck
# import zipfile as zpf
import doctree.pickle_dml as dml
from doctree import gui
from doctree import shared

app_info = "\n".join(["DocTree door Albert Visser",
                      "Uitgebreid electronisch notitieblokje",
                      "PyQt versie"])
help_info = "\n".join([
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
    "See menu for editing keys"])


def init_opts():
    """return dict of options and their initial values
    """
    return {"Application": "DocTree", "NotifyOnSave": True, 'NotifyOnLoad': True,
            "AskBeforeHide": True, "EscapeClosesApp": True, "SashPosition": (180, 0),
            "ScreenSize": (800, 500), "ActiveItem": [0], "ActiveView": 0, "ViewNames": ["Default"],
            "RootTitle": "MyNotes", "RootData": "", "ImageCount": 0}


def add_newitems(cut_from_itemdict, itemdict):
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
    # shared.log(f"add_newitems: cut_from_itemdict is {cut_from_itemdict}")
    for key, item in cut_from_itemdict:
        title, text = item
        itemdict[newkey] = (title, text)
        keymap[key] = newkey
        newkey += 1
    # shared.log(f"add_newitems: keymap is {keymap}")
    return itemdict, keymap


def replace_keys(item, keymap):
    """kopie van toe te voegen deelstructuur maken met vervangen van oude key
    door nieuwe key volgens keymap
    """
    item = list(item)   # mutable maken (item is een tuple)
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


def add_subitem_to_view(view, ref, newitem):
    """zoeken waar het subitem moet worden toegevoegd en het toevoegen"""
    retval = ""
    for itemref, subview in view:
        if itemref == ref:
            subview.append(newitem)
            retval = 'Stop'
        else:
            retval = add_subitem_to_view(subview, ref, newitem)
        if retval == 'Stop':
            break
    return retval


def remove_item_from_view(view, to_remove):
    "recursieve routine om een view bij te werken"
    klaar = False
    for idx, item in reversed(list(enumerate(view))):
        itemref, subview = item
        if itemref in to_remove:
            remove_item_from_view(subview, to_remove)
            if not subview:
                view.pop(idx)
            else:
                view[idx] = subview[0]
            klaar = True
        else:
            klaar = remove_item_from_view(subview, to_remove)
        ## if klaar:
            ## break
    return klaar


def reset_toolkit_file_if_needed():
    "see if toolkit.py needs to be restored"
    path = pathlib.Path(__file__).parent.resolve()
    if (path / 'toolkit-orig').exists():
        (path / 'toolkit-orig').rename(path / 'toolkit.py')


class MainWindow:
    "Primary application window (main screen)"
    def __init__(self, fname=''):
        self.project_dirty = False
        self.add_node_on_paste = False
        self.has_treedata = False
        self.imagelist = []
        self.temp_imagepath = pathlib.Path(tempfile.mkdtemp())
        self.copied_item, self.cut_from_itemdict = (), []
        self.opts = init_opts()
        # self.toolkit = gui.toolkit
        self.images_embedded = gui.toolkit == 'wx'
        self.gui = gui.MainGui(self, title="Doctree")
        self.gui.setup_screen()
        if fname:
            self.project_file = pathlib.Path(fname).resolve()
            if not self.project_file.exists():
                ok = gui.ask_ynquestion(self.gui,
                                        fname + " does not exist, do you want to create it?")
                if ok:
                    self.new(filename=fname, ask_ok=False)
                    self.set_project_dirty(True)
                else:
                    self.gui.disable_menu()
            else:
                err = self.read()
                if err:
                    gui.show_message(self.gui, err[0])
        else:
            self.new(ask_ok=False)  # fname='' forces filename dialog
        reset_toolkit_file_if_needed()
        self.gui.go()

    def get_menu_data(self):
        """Menu options definitions
        """
        return (
            ("&Main", (
                ("Re&Load", self.reread, 'Ctrl+R', 'icons/filerevert.png', 'Reread notes file'),
                ("&Open", self.open, 'Ctrl+O', 'icons/fileopen.png',
                 "Choose and open notes file"),
                ("&Init", self.new, 'Shift+Ctrl+I', 'icons/filenew.png',
                 'Start a new notes file'),
                ("&Save", self.save, 'Ctrl+S', 'icons/filesave.png', 'Save notes file'),
                ("Save as", self.saveas, 'Shift+Ctrl+S', 'icons/filesaveas.png',
                 'Name and save notes file'),
                (),
                ("&Root title", self.rename_root, 'Shift+F2', '', 'Rename root'),
                ("Items sorteren", self.order_top, '', '', 'Bovenste niveau sorteren op titel'),
                ("Items recursief sorteren", self.order_all, '', '',
                 'Alle niveaus sorteren op titel'),
                (),
                ("&Hide", self.hide_me, 'Ctrl+H', '', 'verbergen in system tray'),
                ("Switch pane", self.change_pane, 'Ctrl+Tab', '',
                 'switch tussen tree en editor'),
                (),
                ("s&Ettings", self.set_options, 'Alt+O', '',
                 'Show settings for some display options'),
                ("e&Xit", self.gui.close, 'Ctrl+Q,Escape', 'icons/exit.png', 'Exit program'))),
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
                ("&Forward", self.next_note_any, 'Ctrl+Down', '', 'View next note'),
                ("For&ward on same level", self.next_note, 'Shift+Ctrl+Down', '',
                 'View next note'),
                ("&Back", self.prev_note_any, 'Ctrl+Up', '', 'View previous note'),
                ("Bac&k on same level", self.prev_note, 'Shift+Ctrl+Up', '',
                 'View previous note'))),
            ("&View", (
                ('&New View', self.add_view, '', '',
                 'Add an alternative view (tree) to this data'),
                ('&Rename Current View', self.rename_view, '', '',
                 'Rename the current tree view'),
                ('&Delete Current View', self.remove_view, '', '',
                 'Remove the current tree view'),
                (),
                ('Goto (Select) View', self.select_view_from_dropdown, 'Ctrl+G', '',
                 'Switch to another view'),
                ('Next View', self.next_view, 'Ctrl+PgDown', '',
                 'Switch to the next view in the list'),
                ('Prior View', self.prev_view, 'Ctrl+PgUp', '',
                 'Switch to the previous view in the list'),
                ())),
            ('&Tree', (
                ('&Undo', self.gui.tree_undo, 'Ctrl+Alt+Z', '', 'Undo last operation'),
                ('&Redo', self.gui.tree_redo, 'Ctrl+Alt+Y', '', 'Redo last undone operation'),
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
                ('Expand', self.expand_item, 'Ctrl+Alt++', '', 'Expand tree item'),
                ('Collapse', self.collapse_item, 'Ctrl+Alt+-', '', 'Collapse tree item'),
                ('Expand all', self.expand_all, 'Ctrl+Alt+Shift++', '',
                 'Expand all subitems'),
                ('Collapse all', self.collapse_all, 'Ctrl+Alt+Shift+-', '',
                 'Collapse all subitems'))),
            ('T&ext', (
                ('&Undo', self.gui.editor.undo, 'Ctrl+Z', 'icons/edit-undo.png',
                 'Undo last operation'),
                ('&Redo', self.gui.editor.redo, 'Ctrl+Y', 'icons/edit-redo.png',
                 'Redo last undone operation'),
                (),
                ('Cu&t', self.gui.editor.cut, 'Ctrl+X', 'icons/edit-cut.png',
                 'Copy the selection and delete from text'),
                ('&Copy', self.gui.editor.copy, 'Ctrl+C', 'icons/edit-copy.png',
                 'Just copy the selection'),
                ('&Paste', self.gui.editor.paste, 'Ctrl+V', 'icons/edit-paste.png',
                 'Paste the copied selection'),
                (),
                ('Select A&ll', self.gui.editor.select_all, 'Ctrl+A', "",
                 'Select the entire text'),
                ("&Clear All (can't undo)", self.gui.editor.clear, '', '',
                 'Delete the entire text'))),
            ('&Format', (
                ('&Bold', self.gui.editor.text_bold, 'Ctrl+B', 'icons/format-text-bold.png',
                 'CheckB'),
                ('&Italic', self.gui.editor.text_italic, 'Ctrl+I',
                 'icons/format-text-italic.png', 'CheckI'),
                ('&Underline', self.gui.editor.text_underline, 'Ctrl+U',
                 'icons/format-text-underline.png', 'CheckU'),
                ('Strike&through', self.gui.editor.text_strikethrough, 'Ctrl+~',
                 'icons/format-text-strikethrough.png', 'CheckS'),
                (),
                ('Align &Left', self.gui.editor.align_left, 'Shift+Ctrl+L',
                 'icons/format-justify-left.png', 'Check'),
                ('C&enter', self.gui.editor.align_center, 'Shift+Ctrl+C',
                 'icons/format-justify-center.png', 'Check'),
                ('Align &Right', self.gui.editor.align_right, 'Shift+Ctrl+R',
                 'icons/format-justify-right.png', 'Check'),
                # niet implemented in wx - vind ik ook eigenlijk niet nodig
                # ('&Justify', self.gui.editor.text_justify, 'Shift+Ctrl+J',
                #  'icons/format-justify-fill.png', 'Check'),
                (),
                # in wx nog niet duidelijk hoe goed te krijgen
                # ("Indent &More", self.gui.editor.indent_more, 'Ctrl+]',
                #  'icons/format-indent-more.png', 'Increase indentation'),
                # ("Indent &Less", self.gui.editor.indent_less, 'Ctrl+[',
                #  'icons/format-indent-less.png', 'Decrease indentation'),
                # (),
                # niet implemented in qt - vind ik oom eigenlijk niet nodig
                # ("Increase Paragraph &Spacing", self.gui.editor.increaseparspacing, ''),
                # ("Decrease &Paragraph Spacing", self.gui.editor.decreaseparspacing, ''),
                # (),
                # niet implemented in qt - vind ik oom eigenlijk niet nodig
                # ("Normal Line Spacing", self.gui.editor.set_linespacing_10, ''),
                # ("1.5 Line Spacing", self.gui.editor.set_linespacing_15,''),
                # ("Double Line Spacing", self.gui.editor.set_linespacing_20, ''),
                # (),
                ("&Font...", self.gui.editor.text_font, '', '', 'Set/change font'),
                ("&Enlarge text", self.gui.editor.enlarge_text, 'Ctrl++', '',
                 'Use bigger letters'),
                ("&Shrink text", self.gui.editor.shrink_text, 'Ctrl+-', '',
                 'Use smaller letters'),
                (),
                ("&Color...", self.gui.editor.text_color, '', '', 'Set/change colour'),
                ("&Background...", self.gui.editor.background_color, '', '',
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

    def set_window_title(self):
        """standaard manier van venstertitel opbouwen"""
        if self.gui.in_editor:
            if not self.activeitem:
                return
            text = f'title: {self.gui.tree.getitemtitle(self.activeitem)}'
        else:
            text = f'view: {self.opts["ViewNames"][self.opts["ActiveView"]]}'
        mark = '*' if self.project_dirty else ''
        self.gui.set_windowtitle(f"{self.project_file.name}{mark} ({text}) - Doctree")

    # menu callbacks en hulpmethoden

    def new(self, *args, filename='', ask_ok=True):
        "Afhandelen Menu - Init / Ctrl-I"
        # print('in new:', filename)
        # in plaats van de prompt voor een filenaam moet er een prompt komen of het wel ok is
        # om de data te initialiseren
        if ask_ok:
            ok = gui.ask_ynquestion(self.gui, 'Ok to initialize data?')
            if not ok:
                return  # False
        filename = pathlib.Path(filename)
        self.project_file = filename
        self.views = [[]]
        self.viewcount = 1
        self.itemdict = {}
        self.text_positions = {}
        self.imagelist = []
        self.opts = init_opts()
        self.has_treedata = True
        self.set_window_title()
        self.set_project_dirty(False)
        # self.opts = init_opts()  -- dubbele aanroep
        self.gui.set_version()
        self.gui.set_window_dimensions(self.opts['ScreenSize'][0], self.opts['ScreenSize'][1])
        if self.gui.menu_disabled:
            self.gui.disable_menu(False)
        self.gui.clear_viewmenu()
        self.gui.add_viewmenu_option('&1 Default')
        self.gui.init_app()
        self.activeitem = self.gui.rebuild_root()  # item_to_activate =
        # print('in new() - after creating self.activeitem:', self.activeitem)
        self.gui.editor.set_contents(self.opts["RootData"])
        self.gui.editor.openup(False)
        self.gui.set_focus_to_tree()
        # return True

    def open(self, *args):
        "afhandelen Menu > Open / Ctrl-O"
        if not self.handle_save_needed():
            return
        dirname = str(self.project_file)
        ok, filename = gui.get_filename(self.gui, "DocTree - choose file to open", dirname)
        if not ok:
            return
        self.project_file = pathlib.Path(filename)
        err = self.read()
        if err:  # is alleen gevuld bij fout en is dan een 1-tuple
            gui.show_message(self.gui, err[0])
        else:
            self.gui.show_statusmessage(f'{self.project_file} gelezen')
            if self.gui.menu_disabled:
                self.gui.disable_menu(False)

    def reread(self, *args):
        """afhandelen Menu > Reload (Ctrl-R)"""
        if not self.handle_save_needed():
            return
        ## if self._ok_to_reload():
        self.read()     # no need to check te result, should be ok when rereading
        load_text = f'{self.project_file} herlezen'
        self.confirm(setting="NotifyOnLoad", textitem=load_text)
        self.gui.show_statusmessage(load_text)

    def save(self, *args):
        """afhandelen Menu > save"""
        if self.project_file and self.project_file.name:
            self.write(meld=True)
        else:
            self.saveas()

    def saveas(self, *args):
        """afhandelen Menu > Save As"""
        dirname = str(self.project_file)
        ok, filename = gui.get_filename(self.gui, "DocTree - save file as:", dirname, save=True)
        if ok:
            filename = pathlib.Path(filename)
            test = filename.suffix
            if test != shared.FILE_TYPE[1]:
                filename = filename.with_suffix(shared.FILE_TYPE[1])
            self.project_file = filename
            self.write(meld=True)
            self.set_window_title()

    def rename_root(self, *args):
        """afhandelen Menu > Rename Root (Shift-Ctrl-F2"""
        ok, data = gui.get_text(self.gui, 'Geef nieuwe titel voor het root item:',
                                self.opts['RootTitle'])
        if ok:
            self.set_project_dirty(True)
            self.opts['RootTitle'] = data
            self.gui.tree.setitemtitle(self.gui.root, data)

    def add_item(self, *args):
        """nieuw item toevoegen (default: onder het geselecteerde)
        """
        self.new_item()

    def root_item(self, *args):
        """nieuw item toevoegen onder root"""
        self.new_item(root=self.gui.root)

    def insert_item(self, *args):
        """nieuw item toevoegen *achter* het geselecteerde (en onder diens parent)"""
        self.new_item(under=False)

    def new_item(self, root=None, under=True):
        "nieuw item toevoegen"
        new_title, extra_titles = self.get_item_title()
        if new_title:
            # pos = -1  # doesn't matter for now - will be determined in do_addaction
            # log('under is {}, pos is {}'.format(under, pos))
            self.gui.start_add(root, under, new_title, extra_titles)

    def get_item_title(self):
        """bepaal een titel voor het nieuwe (en eventueel onderliggende) item
        """
        title = "Geef een titel op voor het nieuwe item"
        text = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        new = self.ask_title(title, text)
        if not new:
            return None, None
        new_title, extra_titles = new
        # stel de inhoud van het item onder de cursor veilig
        self.check_active()
        return new_title, extra_titles

    def do_addaction(self, root, under, origpos, new_title, extra_titles):
        """toevoegen nieuw item
        """
        # bepaal nieuwe key in itemdict
        newkey = len(self.itemdict)
        while newkey in self.itemdict:  # rekening houden met verwijderde items
            newkey += 1
        # voeg nieuw item toe aan itemdict
        self.itemdict[newkey] = (new_title, "")
        # voeg nieuw item toe aan visual tree
        parent, pos = self.get_add_dest(root, under, origpos)
        item = self.gui.tree.add_to_parent(newkey, new_title, parent, pos)
        new_item = item
        # doe hetzelfde met het via \ toegevoegde item
        extra_keys = []
        subkey = newkey
        while extra_titles:
            subkey += 1
            self.itemdict[subkey] = (extra_titles[0], "")
            item = self.gui.tree.add_to_parent(subkey, extra_titles[0], item)
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
        self.gui.tree.set_item_expanded(parent)
        self.gui.tree.set_item_selected(item)
        if item != self.gui.root:
            self.gui.set_focus_to_editor()
        # resultaat t.b.v. undo/redo mechanisme
        return newkey, extra_keys, new_item, subitem

    def get_add_dest(self, root, under, origpos):
        """bepaal de parent voor het nieuwe item en op welke plek eronder het moet komen
        """
        if not root:
            root = self.activeitem or self.gui.root
        if under:
            parent = root
            pos = -1
        else:
            parent, pos = self.gui.tree.getitemparentpos(root)
            if origpos == -1:
                pos += 1    # we want to insert after, not before
                if pos == len(self.gui.tree.getitemkids(parent)):
                    pos = -1
            else:
                pos = origpos
        return parent, pos

    def rename_item(self, *args):
        """titel van item wijzigen"""
        root = item = self.activeitem
        self.check_active()
        new = self.ask_title('Nieuwe titel voor het huidige item:',
                             self.gui.tree.getitemtitle(item))
        if not new:
            return
        self.set_project_dirty(True)
        new_title, extra_titles = new
        self.gui.tree.setitemtitle(self.activeitem, new_title)
        if item == self.gui.root:
            self.opts['RootTitle'] = new_title
            return
        ref = self.gui.tree.getitemkey(self.activeitem)
        data = self.itemdict[ref][1]
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
                item = self.gui.tree.add_to_parent(subkey, extra_titles[0], item)
                extra_keys.append(subkey)
                subref += 1
                extra_titles = extra_titles[1:]
            # voeg de items ook toe aan de niet zichtbare views
            subitem = []
            for subkey in reversed(extra_keys):
                subitem = [(subkey, subitem)]
            for idx, view in enumerate(self.views):
                if idx != self.opts["ActiveView"]:
                    add_subitem_to_view(view, ref, subitem[0])
            self.gui.tree.set_item_expanded(root)
        self.gui.tree.set_item_selected(item)

    def ask_title(self, title, text):
        """vraag titel voor item (ingesloten backslashes gelden als
        scheidingstekens voor titels van onderliggende items)
        """
        ok, data = gui.get_text(self.gui, title, text)
        if ok:
            if data:
                test = data.split(" \\ ")
                new_title, extra_title = test[0], test[1:]
            else:
                new_title, extra_title = '(untitled)', []
            return new_title, extra_title
        return ()

    def expand_item(self, *args):
        "expand one level"
        self.expand()

    def collapse_item(self, *args):
        "collapse one level"
        self.collapse()

    def expand_all(self, *args):
        "expand all levels"
        self.expand(recursive=True)

    def collapse_all(self, *args):
        "collapse all levels"
        self.collapse(recursive=True)

    def expand(self, recursive=False):
        "expandeer tree vanaf huidige item"
        def expand_all(item):
            "do it recursively"
            for sub in self.gui.tree.getitemkids(item):
                self.gui.tree.set_item_expanded(sub)
                expand_all(sub)
        item = self.gui.tree.get_selected_item()
        self.gui.tree.set_item_expanded(item)
        if recursive:
            expand_all(item)

    def collapse(self, recursive=False):
        "collapse huidige item en daaronder"
        def collapse_all(item):
            "do it recursively"
            for sub in self.gui.tree.getitemkids(item):
                collapse_all(sub)
                self.gui.tree.set_item_collapsed(sub)
        item = self.gui.tree.get_selected_item()
        if recursive:
            collapse_all(item)
        self.gui.tree.set_item_collapsed(item)

    def next_note(self, *args):
        """move to next item"""
        if not self.gui.set_next_item():
            gui.show_message(self.gui, "Geen volgend item op dit niveau")

    def prev_note(self, *args):
        """move to previous item"""
        if not self.gui.set_prev_item():
            gui.show_message(self.gui, "Geen vorig item op dit niveau")

    def next_note_any(self, *args):
        """move to next item"""
        if not self.gui.set_next_item(any_level=True):
            gui.show_message(self.gui, "Geen volgend item")

    def prev_note_any(self, *args):
        """move to previous item"""
        if not self.gui.set_prev_item(any_level=True):
            gui.show_message(self.gui, "Geen vorig item")

    def cut_item(self, *args):
        "cut = copy with removing item from tree"
        self.get_copy_item(cut=True)

    def delete_item(self, *args):
        "delete = copy with removing item from tree and memory"
        self.get_copy_item(cut=True, retain=False)

    def copy_item(self, *args):
        "copy: retain item in tree and in memory"
        self.get_copy_item()

    def get_copy_item(self, cut=False, retain=True, to_other_file=None):
        """start copy/cut/delete action

        parameters: cut: remove item from tree (True for cut, delete and move)
                    retain: remember item for pasting (True for cut and copy)
                    other_file:
        """
        current = self.get_copy_source(cut, retain, to_other_file)
        if current:
            self.gui.start_copy(cut, retain, current)  # to_other_file)

    def get_copy_source(self, cut, retain, to_other_file):
        "can we copy from here?"
        if to_other_file:
            current = to_other_file
        else:
            current = self.gui.tree.getselecteditem()
            if current == self.gui.root:
                gui.show_message(self.gui, "Can't do this with root")
                return None
        # are-you-sure message + cancel this action if applicable
        go_on = True
        if cut and not retain and not to_other_file:
            go_on = gui.ask_ynquestion(self.gui, "Are you sure you want to remove this item?")
        if go_on:
            return current
        return None

    def do_copyaction(self, cut, retain, current):  # to_other_file):
        "do the copying"
        # create a copy buffer
        item_to_copy, itemlist = self.gui.tree.getsubtree(current)
        # shared.log(f'in main.do_copyaction na getsubtree, copied_item is {copied_item},'
        #            f' itemlist is {itemlist}')
        cut_from_itemdict = [(int(x), self.itemdict[int(x)]) for x in itemlist]
        # shared.log(f'  cut_from_itemdict wordt dan {cut_from_itemdict}')
        oldloc = None  # alleen interessant bij undo van cut/delete
        if retain:
            self.copied_item = item_to_copy
            self.cut_from_itemdict = cut_from_itemdict
            self.add_node_on_paste = True
        if cut:
            # remove item (and subitems) from tree and itemdict
            # they're buffered in (self.)cut_from_itemdict because we still need them
            self.add_node_on_paste = False
            oldloc, prev = self.gui.tree.removeitem(current, cut_from_itemdict)
            self.activeitem = None

            # remove item(s) from view(s)
            removed = [x[0] for x in cut_from_itemdict]
            for ix, item in enumerate(self.opts["ActiveItem"]):
                if item in removed:
                    self.opts["ActiveItem"][ix] = self.gui.tree.getitemkey(prev)
            for ix, view in enumerate(self.views):
                if ix != self.opts["ActiveView"]:
                    remove_item_from_view(view, removed)

            # finish up
            self.set_project_dirty(True)
            self.gui.tree.set_item_selected(prev)

        return item_to_copy, oldloc, cut_from_itemdict

    def popitems(self, current, itemlist):
        """recursieve routine om de structuur uit de itemdict en de
        niet-actieve views te verwijderen
        """
        ref = self.gui.tree.getitemkey(current)
        ## try:
        self.itemdict.pop(ref)
        ## except KeyError:
            ## pass
        ## else:
        for kid in self.gui.tree.getitemkids(current):
            self.popitems(kid, itemlist)

    def paste_item(self, *args):
        "paste before"
        self.put_paste_item()

    def paste_item_after(self, *args):
        "paste after instead of before"
        self.put_paste_item(before=False)

    def paste_item_below(self, *args):
        "paste below instead of before"
        self.put_paste_item(below=True)

    def put_paste_item(self, before=True, below=False):
        "start paste actie"
        current = self.get_paste_dest(below)  # before,
        if current:
            self.gui.start_paste(before, below, current)

    def get_paste_dest(self, below):  # , before
        "can we paste here?"
        current = self.gui.tree.getselecteditem()
        # als het geselecteerde item het top item is moet het automatisch below worden
        # maar dan wel als eerste  - of het moet niet mogen
        if current == self.gui.root and not below:
            gui.show_message(self.gui, 'Can only copy *below* the root')
            return None
        if not self.copied_item:
            gui.show_message(self.gui, 'Nothing to paste')
            return None
        return current

    def do_pasteaction(self, before, below, current):
        "do the pasting"
        # items toevoegen aan itemdict
        if not self.add_node_on_paste:
            pasted_item = self.copied_item
            used_keys = self.add_items_back()
        else:
            self.itemdict, keymap = add_newitems(self.cut_from_itemdict, self.itemdict)
            pasted_item = replace_keys(self.copied_item, keymap)
            used_keys = list(keymap.values())
       # items toevoegen aan visual tree
        if below:
            self.gui.tree.putsubtree(current, *pasted_item)
            used_parent = (current, -1)
        else:
            add_to, pos = self.gui.tree.getitemparentpos(current)
            if not before:
                pos += 1
            self.gui.tree.putsubtree(add_to, *pasted_item, pos=pos)
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
        self.gui.tree.set_item_expanded(current)
        self.gui.tree.set_item_selected(current)
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

    def move_to_file(self, *args):
        "afhandelen Menu > Move / Ctrl-M"

        # 0. check the selected item (copied from the copy routine)
        # eventueel check_copyable aanroepen in plaats van dit

        current = self.gui.tree.getselecteditem()  # self.activeitem kan niet?
        if current == self.gui.root:
            gui.show_message(self.gui, "Can't do this with root")
            return

        # 1. ask which file to move to (from here you can still cancel the action)

        dirname = str(self.project_file.parent)
        ok, filename = gui.get_filename(self.gui, "DocTree - choose file to move the item to",
                                        dirname)
        if not ok:
            return

        # 2. read the file

        other_file = pathlib.Path(filename)
        if other_file == self.project_file:
            gui.show_message(self.gui, 'Destination file is the same as origin file')
            return

        # opts, views, itemdict, positions = read_or_init_other_file(other_file)
        if other_file.exists():
            data = self.read(other_file=other_file)
            if len(data) == 1:
                gui.show_message(self.gui, data[0])
                return
            opts, views, itemdict, positions = data
        else:
            opts = init_opts()
            opts['Version'] = self.opts.get('Version', None)
            views, itemdict = [[]], {}

        # 3. cut action on the item

        self.get_copy_item(cut=True, to_other_file=current)

        # 3a. Make a list of the images contained in self.cut_from_itemdict
        #      so they can be copied over to the other zipfile

        extra_images = []
        # if self.toolkit != 'wx':    # wx xml bevat plaatjes inline
        if not self.images_embedded:
            self.cut_from_itemdict, extra_images = dml.verify_imagenames(self.cut_from_itemdict,
                                                                         self.temp_imagepath,
                                                                         other_file)

        # 4. paste action on the other file

        itemdict, keymap = add_newitems(self.cut_from_itemdict, itemdict)
        new_copied_item = replace_keys(self.copied_item, keymap)
        for view in views:
            add_item_to_view(new_copied_item, view)
        positions = {}
        for key, value in keymap.items():
            positions[value] = self.text_positions[key]
            self.text_positions.pop(key)

        # 5. write back the updated structure

        # save_images = self.toolkit != 'wx'
        dml.write_to_files(other_file, opts, views, itemdict, positions, self.temp_imagepath,
                           extra_images, save_images=not self.images_embedded)

    def order_top(self, *args):
        """order items directly under the top level"""
        self.reorder(self.gui.root)

    def order_all(self, *args):
        """order items under top level and below"""
        self.reorder(self.gui.root, recursive=True)

    def order_this(self, *args):
        """order items directly under current level"""
        self.reorder(self.activeitem)

    def order_lower(self, *args):
        """order items under current level and below"""
        self.reorder(self.activeitem, recursive=True)

    def reorder(self, root, recursive=False):
        "(re)order_items"
        self.gui.reorder_items(root, recursive)
        self.set_project_dirty(True)

    def hide_me(self, *args):
        """applicatie verbergen"""
        self.confirm(setting="AskBeforeHide", textitem=shared.HIDE_TEXT)
        self.gui.hide_me()

    def change_pane(self, *args):
        "wissel tussen tree en editor"
        if self.gui.in_editor:
            self.check_active()
            self.gui.set_focus_to_tree()
        else:
            self.gui.set_focus_to_editor()

    def set_options(self, *args):
        """check settings for showing various messages"""
        if gui.show_dialog(self.gui, gui.OptionsDialog):
            self.set_escape_action()

    def add_view(self, *args):
        "handles Menu > View > New view"
        self.check_active()
        self.opts["ActiveItem"][self.opts["ActiveView"]] = self.gui.tree.getitemdata(
            self.activeitem)
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.viewcount += 1
        new_view = f"New View #{self.viewcount}"
        self.opts["ViewNames"].append(new_view)
        active = self.opts["ActiveItem"][self.opts["ActiveView"]]
        self.opts["ActiveItem"].append(active)
        self.gui.uncheck_viewmenu_option()
        action = self.gui.add_viewmenu_option(f'&{self.viewcount} {new_view}')
        self.gui.check_viewmenu_option(action)
        self.opts["ActiveView"] = self.opts["ViewNames"].index(new_view)
        self.gui.rebuild_root()
        self.activeitem = self.gui.root
        newtree = []
        for key in sorted(self.itemdict.keys()):
            newtree.append((key, []))
        self.views.append(newtree)
        tree_item = self.viewtotree()
        self.set_project_dirty(True)
        self.gui.tree.set_item_selected(tree_item)

    def rename_view(self, *args):
        "handles Menu > View > Rename current view"
        oldname = self.opts["ViewNames"][self.opts["ActiveView"]]
        ok, newname = gui.get_text(self.gui, 'Geef een nieuwe naam voor de huidige view', oldname)
        if ok and newname != oldname:
            self.gui.rename_viewmenu_option(newname)
            self.opts["ViewNames"][self.opts["ActiveView"]] = newname
            self.set_project_dirty(True)

    def remove_view(self, *args):
        "handles Menu > View > Delete current view"
        if self.viewcount == 1:
            gui.show_message(self.gui, "Can't delete the last (only) view")
            return
        ok = gui.ask_ynquestion(self.gui, "Are you sure you want to remove this view?")
        if not ok:
            return
        self.viewcount -= 1
        viewname = self.opts["ViewNames"][self.opts["ActiveView"]]
        self.opts["ViewNames"].remove(viewname)
        self.opts["ActiveItem"].pop(self.opts["ActiveView"])
        self.views.pop(self.opts["ActiveView"])
        if self.opts["ActiveView"] > 0:
            self.opts["ActiveView"] -= 1
        action_to_check = self.gui.remove_viewmenu_option(viewname)
        self.gui.check_viewmenu_option(action_to_check)
        self.gui.rebuild_root()
        self.set_project_dirty(True)
        self.gui.tree.set_item_selected(self.viewtotree())

    def next_view(self, *args):
        """cycle to next view if available (default direction / forward)"""
        self.goto_view(goto_next=True)

    def prev_view(self, *args):
        """cycle to previous view (alternate direction / backward)"""
        self.goto_view(goto_next=False)

    def goto_view(self, goto_next=True):
        "handles menu -> goto next/ previous view"
        if self.viewcount == 1:
            gui.show_message(self.gui, "This is the only view")
            return
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.gui.editor.clear()
        if goto_next:
            self.gui.check_next_viewmenu_option()
            self.opts["ActiveView"] += 1
            if self.opts["ActiveView"] >= len(self.opts["ViewNames"]):
                self.opts["ActiveView"] = 0
        else:
            self.gui.check_next_viewmenu_option(prev=True)
            self.opts["ActiveView"] -= 1
            if self.opts["ActiveView"] < 0:
                self.opts["ActiveView"] = len(self.opts["ViewNames"]) - 1
        self.gui.rebuild_root()
        self.activeitem = self.gui.root
        tree_item = self.viewtotree()
        self.set_window_title()
        self.gui.tree.set_item_selected(tree_item)

    def select_view_from_dropdown(self):
        "handles Menu > View > Goto View"
        ok, newview = gui.get_choice(self.gui, 'Select a view:', self.opts["ViewNames"],
                                     self.opts["ActiveView"])
        if not ok:
            return
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.gui.editor.clear()
        self.opts["ActiveView"] = self.opts["ViewNames"].index(newview)
        self.gui.rebuild_root()
        self.activeitem = self.gui.root
        tree_item = self.viewtotree()
        self.set_window_title()
        self.gui.tree.set_item_selected(tree_item)

    def select_view(self):
        "handles Menu > View > <view name>"
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.gui.editor.clear()
        newview = self.gui.check_viewmenu_option()
        newviewtext = str(newview).split(None, 1)[1]
        self.opts["ActiveView"] = self.opts["ViewNames"].index(newviewtext)
        self.gui.rebuild_root()
        self.activeitem = self.gui.root
        tree_item = self.viewtotree()
        self.set_window_title()
        self.gui.tree.set_item_selected(tree_item)

    def search(self, *args):  # , mode=0):
        """start search action
        """
        # print('starting new search, srchlist =', self.gui.srchlist)
        if self.gui.srchlist:
            gui.show_message(self.gui, 'Cannot start new search while results screen is showing')
            return
        ok = gui.show_dialog(self.gui, gui.SearchDialog)  # , {'mode': mode})
        if not ok:
            return
        if self.gui.srchtype == 0:
            ok = self.gui.editor.search_from_start()
            if not ok:
                gui.show_message(self.gui, 'Search string not found')
            return
        if self.gui.srchtype not in (1, 2, 3):  # failsafe
            gui.show_message(self.gui, 'Wrong search type')
            return
        self.search_results = self.search_from(self.gui.root)
        if not self.search_results:
            self.gui.srchlist = False
            gui.show_message(self.gui, 'Search string not found')
            return
        if self.gui.srchlist:
            gui.show_nonmodal(self.gui, gui.ResultsDialog)
        else:
            self.srchno = 0
            self.go_to_result()

    def search_texts(self, *args):
        "search in all texts"
        self.search(mode=2)

    def search_titles(self, *args):
        "search in all titles"
        self.search(mode=1)

    def find_next(self, *args):
        "search forward"
        if not self.gui.srchtext:
            return
        if self.gui.srchtype:
            self.srchno += 1
            self.go_to_result()
        else:
            self.gui.editor.find_next()

    def find_prev(self, *args):
        "search backward"
        if not self.gui.srchtext:
            return
        if self.gui.srchtype:
            self.srchno -= 1
            self.go_to_result()
        else:
            self.gui.editor.find_prev()

    def search_from(self, parent, loc=None):
        """recursive search in tree items
        assumes item.text(0) contains title, item.data(0) contains text without format
        result is a list of 3-tuples with items:
        - node address in the form of a series of sequence numbers
        - indication of where the string was found (title or text)
        - title of the itemdict item
        """
        result = []
        location = loc or []
        # for ix in range(parent.childCount()):
        for ix, treeitem in enumerate(self.gui.tree.getitemkids(parent)):
            loc = location + [ix]
            # treeitem = parent.child(ix)
            title = self.gui.tree.getitemtitle(treeitem)
            text = self.gui.tree.getitemuserdata(treeitem)
            # or
            # title, text = self.gui.tree.getitemdata(treeitem)
            if len(loc) == 1:
                self.first_title = title
            if self.gui.srchtype & 1 and self.gui.find_needle(title):
                result.append((loc, 'title', self.first_title, title))
            if self.gui.srchtype & 2 and self.gui.find_needle(text):
                result.append((loc, 'text', self.first_title, title))
            test = self.search_from(treeitem, loc)
            if test:
                result.extend(test)
        return result

    def go_to_result(self):
        "view search result"
        msg = ''
        if self.srchno >= len(self.search_results):
            if self.gui.srchwrap:
                self.srchno = 0
            else:
                self.srchno = len(self.search_results) - 1
                msg = 'No next result'
        elif self.srchno < 0:
            if self.gui.srchwrap:
                self.srchno = len(self.search_results) - 1
            else:
                self.srchno = 0
                msg = 'No prior result'
        if msg:
            gui.show_message(self.gui, msg)
            return
        ## key, loc, type, text = self.search_results[self.srchno]
        self.gui.goto_searchresult(self.search_results[self.srchno][0])  # [:2])  # niet *self.srchno?

    def info_page(self, *args):
        """help -> about"""
        gui.show_message(self.gui, app_info)

    def help_page(self, *args):
        """help -> keys"""
        gui.show_message(self.gui, help_info)

    def set_project_dirty(self, value):
        "indicate that there have been changes"
        self.project_dirty = value
        self.set_window_title()

    def handle_save_needed(self, always_check=True):
        """vraag of het bestand opgeslagen moet worden als er iets aan de
        verzameling notities is gewijzigd

        Geeft tevens de mogelijkheid om de bestaande actie af te breken
        in dat geval wordt er (niet opgeslagen en) False geretourneerd
        anders wordt afhankelijk van de gemaakte keuze opgeslagen en True geretourneerd
          als signaal dat er kan worden doorgegaan
        """
        save_is_needed = self.has_treedata and self.project_dirty
        # bij wisselen van pagina wordt de inhoud indien nodig opgeslagen en weten we
        # of er wat veranderd is. Bij afsluiten hoeft dat nog niet gebeurd te zijn
        # maar willen we toch weten of er iets gewijzigd is
        need_to_save = self.gui.editor.check_dirty() if always_check else False
        if save_is_needed or need_to_save:
            if self.gui.in_editor:
                self.check_active()
            question = "Data changed - save current file before continuing?"
            ok, cancel = gui.ask_yncquestion(self.gui, question)
            if ok:
                self.save()
            elif cancel:
                return False
        return True

    def treetoview(self):
        """zet de visuele tree om in een tree om op te slaan"""
        def lees_item(item):
            """recursieve functie om de data in een pickle-bare structuur om te zetten"""
            textref = self.gui.tree.getitemkey(item)
            if item == self.activeitem:
                self.opts["ActiveItem"][self.opts["ActiveView"]] = textref
            kids = [lees_item(x) for x in self.gui.tree.getitemkids(item)]
            return textref, kids
        data = [lees_item(x) for x in self.gui.tree.getitemkids(self.gui.root)]
        return data

    def viewtotree(self):
        """zet de geselecteerde view om in een visuele tree"""
        def maak_item(parent, key, children=None):
            """recursieve functie om de TreeCtrl op te bouwen vanuit de opgeslagen data"""
            item_to_activate = None
            if children is None:
                children = []
            titel = self.itemdict[key][0]
            tree_item = self.gui.tree.add_to_parent(key, titel, parent)
            if key == self.opts["ActiveItem"][self.opts['ActiveView']]:
                item_to_activate = tree_item
            for child in children:
                y = maak_item(tree_item, *child)[1]
                if y is not None:
                    item_to_activate = y
            return key, item_to_activate
        item_to_activate = None
        current_view = self.views[self.opts['ActiveView']]
        for item in current_view:
            y = maak_item(self.gui.root, *item)[1]
            if y is not None:
                item_to_activate = y
        return item_to_activate

    def check_active(self):
        """zorgen dat de editor inhoud voor het huidige item bewaard wordt in de treectrl"""
        # shared.log('*** in main.check_active ***')
        if self.activeitem:
            text = self.gui.tree.getitemtitle(self.activeitem)
            # shared.log(f'active item is {self.activeitem} ({text})')
            ref = self.gui.tree.getitemkey(self.activeitem)
            pos = self.gui.editor.get_text_position()
            # try:
            #     ref = int(ref)  # is dit niet altijd al een int?
            # except ValueError:
            #     ref = -1
            if ref != -1:
                self.text_positions[ref] = pos
            if self.gui.editor.check_dirty():
                # shared.log(f'contents is {self.gui.tree.getitemdata(self.activeitem)}')
                content = str(self.gui.editor.get_contents())
                try:
                    # titel, tekst = self.itemdict[int(ref)]
                    titel, tekst = self.itemdict[ref]
                # except (KeyError, ValueError):
                except KeyError:
                    if content:
                        self.gui.tree.setitemtext(self.gui.root, content)
                        self.opts["RootData"] = content
                else:
                    # self.itemdict[int(ref)] = (titel, content)
                    self.itemdict[ref] = (titel, content)
                self.gui.editor.mark_dirty(False)
                self.set_project_dirty(True)

    def activate_item(self, item):
        """meegegeven item "actief" maken (accentueren en in de editor zetten)"""
        # shared.log(f'*** in main.activate_item, item is {item}')
        self.activeitem = item
        ref = self.gui.tree.getitemkey(item)
        # try:
        #     titel, tekst = self.itemdict[ref]
        # except (KeyError, ValueError):
        #     self.gui.editor.set_contents(str(ref))
        #     ref = -1
        # else:
        # self.gui.editor.set_contents(tekst)  # , titel)
        if ref == -1:
            tekst = self.opts['RootData']
        else:
            tekst = self.itemdict[ref][1]
            try:
                self.gui.editor.set_text_position(self.text_positions[ref])
            except KeyError:  # item is nieuw
                self.text_positions[ref] = self.gui.editor.get_text_position()
        self.gui.editor.set_contents(tekst)  # , titel)
        self.gui.editor.openup(True)

    def cleanup_files(self):
        "remove temporary files on exit (as they have been zipped)"
        shutil.rmtree(self.temp_imagepath)

    def read(self, other_file=''):
        """settings dictionary lezen, opgeslagen data omzetten naar tree"""
        if not other_file:
            self.has_treedata = False  # wordt deze ergens onderwater gebruikt? Ivm terugzetten
        self.opts = init_opts()
        nt_data = dml.read_from_files(self.project_file, other_file, self.temp_imagepath)
        if len(nt_data) == 1:
            return (nt_data[0],)  # foutmelding - teruggeven als 1-tuple

        if other_file:
            return nt_data[:-1]  # zonder imagelist

        for key, value in nt_data[0].items():
            if key == 'RootData' and value is None:
                value = ""
            self.opts[key] = value
        self.views, self.itemdict, self.text_positions, self.imagelist = nt_data[1:]
        self.viewcount = len(self.views)
        if self.imagelist:
            self.opts['ImageCount'] = int(max(self.imagelist).split('.')[0])

        self.gui.set_version()
        self.gui.set_window_dimensions(self.opts['ScreenSize'][0], self.opts['ScreenSize'][1])
        self.set_windowsplit()
        self.set_escape_action()

        self.activeitem = self.gui.rebuild_root()  # item_to_activate =
        self.gui.init_app()
        self.gui.editor.set_contents(self.opts["RootData"])
        self.setup_viewmenu()
        self.gui.set_focus_to_tree()
        item_to_activate = self.viewtotree()
        self.has_treedata = True
        self.set_project_dirty(False)
        self.gui.expand_root()
        if item_to_activate != self.activeitem:
            self.gui.tree.set_item_selected(item_to_activate)
        return []  # self.opts, self.views, self.itemdict, self.text_positions, self.imagelist

    def set_windowsplit(self):
        "set and/or correct sash position"
        if isinstance(self.opts['SashPosition'], int):  # compatibility old version
            righthand_size = self.opts['ScreenSize'][0] - self.opts['SashPosition']
            self.opts['SashPosition'] = (self.opts['SashPosition'], righthand_size)
        elif len(self.opts['SashPosition']) == 1:
            righthand_size = self.opts['ScreenSize'][0] - self.opts['SashPosition'][0]
            self.opts['SashPosition'] = (self.opts['SashPosition'][0], righthand_size)
        try:
            self.gui.set_window_split(self.opts['SashPosition'])
        except TypeError:
            gui.show_message(self.gui, 'Ignoring incompatible sash position')

    def set_escape_action(self):
        "respect setting whether using escape shuts down the application or not"
        if self.opts['EscapeClosesApp']:
            self.gui.add_escape_action()
        else:
            self.gui.remove_escape_action()

    def setup_viewmenu(self):
        "set new viewmenu options"
        self.gui.clear_viewmenu()
        for idx, name in enumerate(self.opts["ViewNames"]):
            action = self.gui.add_viewmenu_option(f'&{idx + 1} {name}')
            if idx == self.opts["ActiveView"]:
                self.gui.check_viewmenu_option(action)

    def write(self, meld=True):
        """settings en tree data in een structuur omzetten en opslaan"""
        self.opts['ScreenSize'] = self.gui.get_screensize()
        self.opts['SashPosition'] = self.gui.get_splitterpos()
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        # # do not write screen positions
        # self.imagelist = write_to_files(self.project_file, self.opts, self.views, self.itemdict)
        # also write screen positions
        # save_images = self.toolkit != 'wx'
        self.imagelist = dml.write_to_files(self.project_file, self.opts, self.views, self.itemdict,
                                            # self.text_positions, save_images=save_images)
                                            self.text_positions, self.temp_imagepath,
                                            save_images=not self.images_embedded)
        self.set_project_dirty(False)
        save_text = f"{self.project_file} is opgeslagen"
        if meld:
            ## print('In save - notify is', self.opts['NotifyOnSave'])
            self.confirm(setting="NotifyOnSave", textitem=save_text)
        self.gui.show_statusmessage(save_text)

    def confirm(self, setting='', textitem=''):
        "ask for confirmation when changing a setting"
        if self.opts[setting]:
            gui.show_dialog(self.gui, gui.CheckDialog, {'message': textitem, 'option': setting})
            # opslaan zonder vragen, backuppen en zippen
            dml.write_to_files(self.project_file, self.opts, self.views, self.itemdict,
                               self.text_positions, self.temp_imagepath, backup=False,
                               save_images=False)
