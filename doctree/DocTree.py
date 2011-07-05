#! /usr/bin/env python
# -*- coding: latin-1 -*-
# het principe (splitter window met een tree en een tekst deel) komt oorspronkelijk van een ibm site

"""
TODOs i.v.m. aanpassen datamodel (splitsen tree en data en vooruitlopen op meer trees)
* MainWindow.__init__():
    view selecteerbaar maken d.m.v. bijvoorbeeld tabs
    eventueel notebook van maken waarvan de pages bij het laden toegevoegd worden
* MainWindow.read():
    tabs maken voor viewnamen
    als het linkerpanel een notebook is kun je evenzoveel pagina's maken
    dat is een andere aanpak dan self.tree steeds gelijk maken aan de tree die je wilt zien?
* MainWindow.add_item():
    ook iets erbij om te waarschuwen dat het item in de andere views generiek is
    toegevoegd en nog op de juiste plaats moet worden gezet
* MainWindow.select_view():
    nieuw om het wisselen van tree uit te voeren:
        de huidige actieve tree wordt op de juiste plek in self.views gezet,
        self.opts["ActiveView"] wordt bijgewerkt en de gekozen view wordt uit self.views
        overgenomen
        hierbij moet ook het geactiveerde item wordt overgenomen in de juiste waarde
        van self.opts["ActiveItem"] - en die voor de nieuw geactiveerde tree eruit
        gehaald
* MainWindow.edit_viewname():
    nieuw om de naam van een view tab te wijzigen -> self.opts["ViewNames"]
"""

import os
import wx
import wx.lib.mixins.treemixin as treemix
import cPickle as pck
import shutil
import pprint
import datetime as dt

def getsubtree(tree,item):
    """recursieve functie om de strucuur onder de te verplaatsen data
    te onthouden"""
    titel = tree.GetItemText(item)
    text = tree.GetItemPyData(item)
    subtree = []
    tag, cookie = tree.GetFirstChild(item)
    while tag.IsOk():
        subtree.append(getsubtree(tree,tag))
        tag, cookie = tree.GetNextChild(item, cookie)
    return titel, text, subtree

def putsubtree(tree, parent, titel, text, subtree=None):
    """recursieve functie om de onthouden structuur terug te zetten"""
    if subtree is None:
        subtree = []
    new = tree.AppendItem(parent, titel)
    tree.SetItemPyData(new, text)
    for sub in subtree:
        putsubtree(tree, new, *sub)
    return new

def messagebox(window, string, title):
    """Toon een boodschap"""
    ## print "messagebox aangeroepen:", string
    dlg=wx.MessageDialog(window, string, title, wx.OK)
    dlg.ShowModal()
    dlg.Destroy()

class CheckDialog(wx.Dialog):
    """Dialoog om te melden dat de applicatie verborgen gaat worden
    AskBeforeHide bepaalt of deze getoond wordt of niet"""
    def __init__(self,parent,id,title, size=(-1,120), pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self,parent,id,title,pos,size,style)
        pnl = wx.Panel(self,-1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(wx.StaticText(pnl,-1,"\n".join((
                "DocTree gaat nu slapen in de System tray",
                "Er komt een icoontje waarop je kunt klikken om hem weer wakker te maken"
                ))),1,wx.ALL,5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.Check = wx.CheckBox(pnl, -1, "Deze melding niet meer laten zien")
        sizer1.Add(self.Check,0,wx.EXPAND)
        sizer0.Add(sizer1,0,wx.ALIGN_CENTER_HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.bOk = wx.Button(pnl,id=wx.ID_OK)
        ## self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        sizer1.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        sizer0.Add(sizer1,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,5)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()

class DnDTree(treemix.DragAndDrop, wx.TreeCtrl):
    """TreeCtrl met drag&drop faciliteit"""
    def __init__(self, *args, **kwargs):
        super(DnDTree, self).__init__(*args, **kwargs)

    def OnDrop(self,dropitem,dragitem):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item"""
        if dropitem == self.GetRootItem():
            return
        ## print self.GetItemText(dropitem)
        if dropitem is None:
            dropitem = self.root
        dragText = self.GetItemText(dragitem)
        dragData = self.GetItemPyData(dragitem)
        dragtree = getsubtree(self,dragitem)
        ## pprint.pprint(dragtree)
        dropText = self.GetItemText(dropitem)
        dropData = self.GetItemPyData(dropitem)
        ## print('drop "%s" on "%s" ' % (dragText, dropText))
        self.Delete(dragitem)
        ## item = self.AppendItem(dropitem, dragText)
        ## self.SetItemPyData(item, dragData)
        putsubtree(self, dropitem, *dragtree)
        self.Expand(dropitem)

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = (800, 500),
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.nt_icon = wx.Icon(os.path.join(
            os.path.dirname(__file__),"doctree.ico"),wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.nt_icon)
        mainwindow = self
        self.sb = self.CreateStatusBar()

        self.create_menu((
            ("&Main",(
                ("Re&Load (Ctrl-R)",self.reread, 'Reread .ini file'),
                ("&Open (Ctrl-O)",self.open,"Choose and open .ini file"),
                ("&Init (Ctrl-I)",self.new,'Start a new .ini file'),
                ("&Save (Ctrl-S)",self.save, 'Save .ini file'),
                ("Save as (Shift-Ctrl-S)",self.saveas, 'Name and save .ini file'),
                ("",None,None),
                ("&Root title (Shift-F2)", self.rename, 'Rename root'),
                ("Items sorteren", self.order_top, 'Bovenste niveau sorteren op titel'),
                ("Items recursief sorteren", self.order_all, 'Alle niveaus sorteren op titel'),
                ("",None,None),
                ("&Hide (Ctrl-H)", self.hide, 'verbergen in system tray'),
                ("",None,None),
                ("e&Xit (Ctrl-Q, Esc)",self.afsl, 'Exit program'),
                ),),
            ("&Note",(
                ("&New (Ctrl-N)", self.add_item, 'Add note (below current level)'),
                ("&Add (Insert)", self.insert_item, 'Add note (after current)'),
                ("&Delete (Ctrl-D, Del)", self.delete_item, 'Remove note'),
                ("",None,None),
                ("Note &Title (F2)",self.rename_item, 'Rename current note'),
                ("Subitems sorteren", self.order_this, 'Onderliggend niveau sorteren op titel'),
                ("Subitems recursief sorteren", self.order_lower, 'Alle onderliggende niveaus sorteren op titel'),
                ("",None,None),
                ("&Forward (Ctrl-PgDn)",self.next_note,'View next note'),
                ("&Back (Ctrl-PgUp)",self.prev_note,'View previous note'),
                ),),
            ("&Help",(
                    ("&About",self.info_page, 'About this application'),
                    ("&Keys (F1)",self.help_page, 'Keyboard shortcuts'),
                ),),
            )
        )

        self.splitter = wx.SplitterWindow (self, -1, style=wx.NO_3D) # |wx.SP_3D
        self.splitter.SetMinimumPaneSize (1)
        self.splitter.SetSashPosition(180, True)

        # TODO: view selecteerbaar maken d.m.v. bijvoorbeeld tabs
        # eventueel notebook van maken waarvan de pages bij het laden toegevoegd worden
        self.tree = DnDTree(self.splitter, -1,
            style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.TR_HAS_VARIABLE_ROW_HEIGHT
            )
        self.root = self.tree.AddRoot("MyNotes")
        self.activeitem = self.root
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelChanging, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.tree.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.editor = wx.TextCtrl(self.splitter, -1, style=wx.TE_MULTILINE)
        self.editor.Enable(0)
        self.editor.new_content = True
        ## self.editor.Bind(wx.EVT_TEXT, self.OnEvtText)
        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.splitter.SplitVertically(self.tree, self.editor)
        self.splitter.SetSashPosition(180, True)
        self.splitter.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_CLOSE, self.afsl)

        self.Show(True)

    def create_menu(self, menudata):
        """bouw het menu op"""
        menuBar = wx.MenuBar()
        for item, data in menudata:
            menu_label = item
            submenu = wx.Menu()
            for label, handler, info in data:
                if label != "":
                    menu_item = wx.MenuItem(submenu, -1, label, info)
                    self.Bind(wx.EVT_MENU, handler, menu_item)
                else:
                    menu_item = wx.MenuItem(submenu, wx.ID_SEPARATOR)
                submenu.AppendItem(menu_item)
            menuBar.Append(submenu, menu_label)
        self.SetMenuBar(menuBar)

    def on_key(self,event):
        """afhandeling toetscombinaties"""
        skip = True
        keycode = event.GetKeyCode()
        mods = event.GetModifiers()
        win = event.GetEventObject()
        if mods == wx.MOD_CONTROL:
            if keycode == ord("O"):
                self.open()
            elif keycode == ord("R"):
                self.reread()
            elif keycode == ord("I"):
                self.new()
            elif keycode == ord("N"):
                self.add_item(root=self.activeitem)
            elif keycode == ord("D"):
                self.delete_item()
            elif keycode == ord("H"):
                self.hide()
            elif keycode == ord("S"):
                self.save()
            elif keycode == ord("Q"):
                self.Close()
            elif keycode == wx.WXK_PAGEDOWN: #  and win == self.editor:
                self.next_note()
            elif keycode == wx.WXK_PAGEUP: #  and win == self.editor:
                self.prev_note()
        elif mods == wx.MOD_CONTROL | wx.MOD_SHIFT: # evt.ControlDown()
            if keycode == ord("N"):
                self.add_item(root=self.root) # eigenlijk: add_item_at_top
            elif keycode == ord("S"):
                self.saveas()
        elif keycode == wx.WXK_F1:
            self.help_page()
        elif keycode == wx.WXK_F2: # and win == self.tree:
            if mods == wx.MOD_SHIFT:
                self.rename()
            else:
                self.rename_item()
        elif keycode == wx.WXK_INSERT and win == self.tree:
            self.insert_item() # insert_at_current_level
        elif keycode == wx.WXK_DELETE and win == self.tree:
            self.delete_item()
        elif keycode == wx.WXK_TAB and win == self.editor:
            if self.editor.IsModified():
                print "Tab gebruikt bij:", self.tree.GetItemText(self.activeitem)
                key = self.tree.GetItemPyData(self.activeitem)
                try:
                    titel, tekst = self.itemdict[key]
                except KeyError:
                    print "on_key (tab): KeyError, waarschijnlijk op root"
                    if key:
                        self.tree.SetItemPyData(self.root, key) # self.opts["RootData"] = key
                else:
                    self.itemdict[key] = (titel, self.editor.GetValue())
        elif keycode == wx.WXK_ESCAPE:
            self.Close()
        if event and skip:
            event.Skip()

    ## def OnEvtText(self,event):
        ## "als er iets met de tekst gebeurt de editor-inhoud als 'aangepast' markeren"
        ## if not self.editor.new_content:
            ## self.editor.IsModified = True
            ## self.editor.new_content = False
        ## print "tekst event! self.editor.IsModified is nu", self.editor.IsModified

    def OnSelChanging(self, event=None):
        "was ooit bedoeld om acties op de root te blokkeren"
        ## if event.GetItem() == self.root:
            ## event.Veto()
        event.Skip()

    def OnSelChanged(self, event=None):
        """zorgen dat het eerder actieve item onthouden wordt, daarna het geselecteerde
        tot nieuw actief item benoemen"""
        x = event.GetItem()
        ## print "onselchanged aangeroepen op", x, self.tree.GetItemText(x)
        self.check_active()
        self.activate_item(event.GetItem())
        ## print "self.editor.IsModified is nu", self.editor.IsModified
        event.Skip()

    def open(self, event=None):
        "afhandelen Menu > Open / Ctrl-O"
        self.dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self, "DocTree - choose file to open",
            self.dirname, "", "INI files|*.ini", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            ## self.save_needed()
            self.project_file = os.path.join(self.dirname,self.filename)
            ## print "ok, reading", self.project_file
            e = self.read()
            if e:
                messagebox(self,e, "Error")
            else:
                self.SetTitle("DocTree - " + self.filename)
        dlg.Destroy()

    def new(self, event=None):
        "Afhandelen Menu - Init / Ctrl-I"
        self.save_needed()
        self.dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self, "DocTree - enter name for new file",
            self.dirname, "", "INI files|*.ini", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.project_file = os.path.join(self.dirname, self.filename)
            ## nt_data = {}
            self.tree.DeleteAllItems()
            self.views = []
            self.viewcount = 1
            self.itemdict = {}
            root = self.tree.AddRoot("hidden_root")
            rootitem = self.tree.AppendItem(root, os.path.splitext(
                os.path.split(self.project_file)[1])[0])
            self.views = [self.tree,]
            self.viewcount = 1
            self.itemdict = {}
            self.activeitem = self.root = rootitem
            self.tree.SetItemBold(rootitem, True)
            self.editor.Enable(True)
            self.editor.Clear()
            self.SetTitle("DocTree - " + self.filename)
            self.tree.SetFocus()
        dlg.Destroy()

    def save_needed(self):
        """eigenlijk bedoeld om te reageren op een indicatie dat er iets aan de
        verzameling notities is gewijzigd (de oorspronkelijke self.project_dirty)"""
        ## self.save()
        ## return
        dlg=wx.MessageDialog(self, "Save current file before continuing?",
            "DocTree", wx.YES_NO)
        h = dlg.ShowModal()
        if h == wx.ID_YES:
            self.save()
        dlg.Destroy()

    def viewtotree(self):
        """zet de geselecteerde view om in een visuele tree"""
        def maak_item(parent, item, children = None):
            """recursieve functie om de TreeCtrl op te bouwen vanuit de opgeslagen data"""
            item_to_activate = None
            if children is None:
                children = []
            titel, tekst = self.itemdict[item]
            tree_item = self.tree.AppendItem (parent, titel.rstrip())
            self.tree.SetItemPyData(tree_item, item)
            if item == self.opts["ActiveItem"][self.opts['ActiveView']]:
                item_to_activate = tree_item
            for child in children:
                x, y = maak_item(tree_item, *child)
                if y is not None:
                    item_to_activate = y
            return item, item_to_activate
        item_to_activate = self.root
        current_view = self.views[self.opts['ActiveView']]
        for item in current_view:
            x, y = maak_item(self.root, *item)
            if y is not None:
                item_to_activate = y
        return item_to_activate

    def read(self):
        """settings dictionary lezen, opgeslagen data omzetten naar tree"""
        ## print self.project_file.join(("reading: ","..."))
        self.opts = {
            "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
            "ActiveItem": [0,], "ActiveView": 0, "ViewNames": ["Default",],
            "RootTitle": "MyNotes", "RootData": ""}
        nt_data = {}
        try:
            file = open(self.project_file,"rb")
        except IOError:
            return "couldn't open "+ self.project_file
        try:
            nt_data = pck.load(file)
        except EOFError:
            return "couldn't load data"
        file.close()
        ## pprint.pprint(nt_data)
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.root = self.tree.AppendItem(root, os.path.splitext(
            os.path.split(self.project_file)[1])[0])
        self.activeitem = item_to_activate = self.root
        self.editor.Clear()
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
        ## try:
            ## self.opts["ActiveItem"][self.opts['ActiveView']]
        ## except TypeError:
            ## self.opts["ActiveItem"] = [self.opts['ActiveView'],]
        ## self.item_to_activate = []
        item_to_activate = self.viewtotree()
        self.tree.SetItemText(self.root,self.opts["RootTitle"].rstrip())
        self.tree.SetItemPyData(self.root, self.opts["RootData"])
        print "read - RootData:", self.opts["RootData"]
        self.editor.SetValue(self.opts["RootData"])
        ## self.editor.IsModified = False
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.Expand(self.root)
        if item_to_activate != self.activeitem:
            self.tree.SelectItem(item_to_activate)
        self.tree.SetFocus()

    def reread(self,event=None):
        """afhandelen Menu > Reload (Ctrl-R)"""
        dlg=wx.MessageDialog(self, 'OK to reload?', 'DocTree', wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.read()

    def save(self, event=None, meld=True):
        """afhandelen Menu > save"""
        if self.project_file:
            self.write(meld=meld)
        else:
            self.saveas()

    def write(self, event=None, meld=True):
        """settings en tree data in een structuur omzetten en opslaan"""
        # TODO: aanpassen voor wegschrijven multiple trees met aparte data
        def lees_item(item):
            """recursieve functie om de data in een pickle-bare structuur om te zetten"""
            ## titel = self.tree.GetItemText(item)
            textref = self.tree.GetItemPyData(item)
            kids = []
            tag, cookie = self.tree.GetFirstChild(item)
            while tag.IsOk():
                kids.append(lees_item(tag))
                tag, cookie = self.tree.GetNextChild(item, cookie) # tag, cookie)
            return textref, kids
        ## print "save - active item was",self.tree.GetItemText(self.activeitem)
        self.check_active() # even zorgen dat de editor inhoud geassocieerd wordt
        self.opts["ScreenSize"] = tuple(self.GetSize())
        self.opts["SashPosition"] = self.splitter.GetSashPosition()
        self.opts["RootTitle"] = self.tree.GetItemText(self.root)
        self.opts["RootData"] = self.tree.GetItemPyData(self.root)
        pprint.pprint(self.opts)
        nt_data = {0: self.opts}
        self.views[self.opts["ActiveView"]] = self.tree
        views = []
        for view in self.views:
            data = []
            tag, cookie = view.GetFirstChild(self.root)
            while tag.IsOk():
                if tag == self.activeitem:
                    self.opts["ActiveItem"][self.opts["ActiveView"]] = self.tree.GetItemPyData(tag)
                data.append(lees_item(tag))
                tag, cookie = self.tree.GetNextChild(self.root, cookie)
            views.append(data)
        nt_data[1] = views
        nt_data[2] = self.itemdict
        try:
            shutil.copyfile(self.project_file,self.project_file + ".bak")
        except IOError:
            pass
        file = open(self.project_file,"w")
        pck.dump(nt_data, file)
        file.close()
        if meld:
            messagebox(self, self.project_file + " is opgeslagen","DocTool")

    def saveas(self, event=None):
        """afhandelen Menu > Save As"""
        self.dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self,"DocTree - Save File as:", self.dirname, "",
            "INI files|*.ini", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.write()
            self.project_file = os.path.join(self.dirname,self.filename)
            self.SetTitle("DocTree - " + self.project_file)
            ## if self.original_name:
                ## self.project_file = original_name
        dlg.Destroy()

    def rename(self, event=None):
        """afhandelen Menu > Rename Root (Shift-Ctrl-F2"""
        dlg = wx.TextEntryDialog(self, 'Geef nieuwe titel voor het hoofditem:',
                'DocTree', self.tree.GetItemText(self.root))
        if dlg.ShowModal() == wx.ID_OK:
            self.tree.SetItemText(self.root,dlg.GetValue())
        dlg.Destroy()

    def hide(self, event=None):
        """applicatie verbergen"""
        if self.opts["AskBeforeHide"]:
            dlg = CheckDialog(self,-1,'DocTree')
            dlg.ShowModal()
            if dlg.Check.GetValue():
                self.opts["AskBeforeHide"] = False
            dlg.Destroy()
        self.tbi = wx.TaskBarIcon()
        self.tbi.SetIcon(self.nt_icon,"Click to revive DocTree")
        wx.EVT_TASKBAR_LEFT_UP(self.tbi, self.revive)
        wx.EVT_TASKBAR_RIGHT_UP(self.tbi, self.revive)
        self.Hide()

    def revive(self, event=None):
        """applicatie weer zichtbaar maken"""
        self.Show()
        self.tbi.Destroy()

    def afsl(self, event=None):
        """applicatie afsluiten"""
        self.save(meld=False)
        if event:
            event.Skip()

    def add_item(self, event = None, root = None, under = True):
        """nieuw item toevoegen (default: onder het geselecteerde)"""
        if under:
            if root is None:
                root = self.activeitem or self.root
        else:
            root = self.tree.GetItemParent(self.activeitem)
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
        ## print "new item {} {}".format(newkey, self.itemdict[newkey])
        if under:
            item = self.tree.AppendItem (root, new_title)
        else:
            item = self.tree.InsertItem (root, self.activeitem, new_title)
        ## print "item appended/inserted:", item
        self.tree.SetItemPyData(item, newkey)
        ## print "item data set to", newkey
        ## self.editor.Clear()
        if extra_title:
            ## print("extra title verwerking")
            subkey = newkey + 1
            self.itemdict[subkey] = (extra_title, "")
            sub_item = self.tree.AppendItem(item, extra_title)
            self.tree.SetItemPyData(sub_item, subkey)
            item = sub_item
        for ix, view in enumerate(self.views):
            # item en subitem ook toevoegen aan de eventuele andere views
            ## print "andere views updaten"
            if ix != self.opts["ActiveView"]:
                print ix
                view_root = view.GetRootItem()
                view_item = self.tree.AppendItem (view_root, new_title)
                view.SetItemPyData(view_item, newkey)
                if extra_title:
                    view_subitem = self.tree.AppendItem(view_item, extra_title)
                    self.tree.SetItemPyData(view_subitem, subkey)
        ## print "now we're going to select the item", item, self.tree.GetItemText(item)
        self.tree.Expand(root)
        self.tree.SelectItem(item)
        if item != self.root:
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()

    def insert_item(self, event=None):
        """nieuw item toevoegen *achter* het geselecteerde (en onder diens parent)"""
        self.add_item(event = event, under = False)

    def delete_item(self, event=None):
        """item verwijderen"""
        def check_item(view, item, ref):
            retval = ""
            tag, cookie = view.GetFirstChild(item)
            while tag.IsOk():
                textref = view.GetItemPyData(tag)
                if textref == ref:
                    view.Delete(tag)
                    retval = "Ready"
                    break
                else:
                    test = check_item(view, tag, ref)
                    if test == "Ready":
                        retval = "Ready"
                        break
                tag, cookie = self.tree.GetNextChild(item, cookie) # tag, cookie)
            return retval
        item = self.tree.GetSelection()
        if item != self.root:
            prev = self.tree.GetPrevSibling(item)
            if not prev.IsOk():
                prev = self.tree.GetItemParent(item)
            print self.tree.GetItemText(prev)
            self.activeitem = None
            ref = self.tree.GetItemPyData(item)
            self.itemdict.pop(ref)
            self.tree.Delete(item)
            for ix, view in enumerate(self.views):
                # item ook verwijderen uit de eventuele andere views
                if ix != self.opts["ActiveView"]:
                    check_item(view, view.GetRootItem(), ref)
            self.activate_item(prev)
        else:
            messagebox(self, "Can't delete root", "Error")

    def rename_item(self):
        """titel van item wijzigen"""
        def check_item(view, item, ref, new_title, extra_title, subref):
            retval = ""
            tag, cookie = view.GetFirstChild(item)
            while tag.IsOk():
                textref = view.GetItemPyData(tag)
                if textref == ref:
                    view.SetItemText(tag, new_title)
                    if extra_title:
                        sub_item = self.tree.AppendItem(tag, extra_title)
                        self.tree.SetItemPyData(sub_item, subref)
                    retval = "Ready"
                    break
                else:
                    test = check_item(view, tag, ref)
                    if test == "Ready":
                        retval = "Ready"
                        break
                tag, cookie = self.tree.GetNextChild(item, cookie)
            return retval
        title = 'Nieuwe titel voor het huidige item:'
        root = item = self.activeitem
        text = self.tree.GetItemText(item)
        self.check_active()
        new = self.ask_title(title, text)
        if not new:
            return
        new_title, extra_title = new
        self.tree.SetItemText(self.activeitem,new_title)
        ref = self.tree.GetItemPyData(self.activeitem)
        old_title, data = self.itemdict[ref]
        self.itemdict[ref] = (new_title, data)
        if extra_title:
            sub_item = self.tree.AppendItem(self.activeitem, extra_title)
            subref = ref + 1
            while subref in self.itemdict:
                subref += 1
            self.itemdict[subref] = (extra_title, data)
            self.tree.SetItemPyData(sub_item, subref)
            item = sub_item
        else:
            subref = 0
            for ix, view in enumerate(self.views):
                # item ook aanpassen in de eventuele andere views
                if ix != self.opts["ActiveView"]:
                    check_item(view, view.GetRootItem(), ref, new_title,
                        extra_title, subref)
        self.tree.Expand(root)
        self.tree.SelectItem(item)
        if item != self.root:
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()

    def ask_title(self, _title, _text):
        """vraag titel voor item"""
        dlg = wx.TextEntryDialog(self, _title,
                'DocTree', _text)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetValue()
            dlg.Destroy()
            if data:
                try:
                    new_title, extra_title = data.split(" \\ ")
                except ValueError:
                    new_title, extra_title = data,""
                return new_title, extra_title
        return

    def order_top(self,event=None):
        print """order items directly under the top level"""
        self.reorder_items(self.root)

    def order_all(self,event=None):
        print """order items under top level and below"""
        self.reorder_items(self.root, recursive=True)

    def reorder_items(self, root, recursive=False):
        print "reorder_items"
        data = []
        tag, cookie = self.tree.GetFirstChild(root)
        while tag.IsOk():
            if recursive:
                self.reorder_items(tag, recursive)
            data.append(getsubtree(self.tree,tag))
            tag, cookie = self.tree.GetNextChild(root, cookie)
        self.tree.DeleteChildren(root)
        for item in sorted(data):
            putsubtree(self.tree, root, *item)

    def order_this(self,event=None):
        print """order items directly under current level"""
        self.reorder_items(self.activeitem)

    def order_lower(self,event=None):
        print """order items under current level and below"""
        self.reorder_items(self.activeitem, recursive=True)

    def next_note(self, event=None):
        """move to next item"""
        item = self.tree.GetNextSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)

    def prev_note(self, event=None):
        """move to previous item"""
        item = self.tree.GetPrevSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)

    def check_active(self,message=None):
        """zorgen dat de editor inhoud voor het huidige item bewaard wordt in de treectrl"""
        ## print "self.check_active called on item", self.activeitem, self.tree.GetItemText(self.activeitem)
        if self.activeitem:
            self.tree.SetItemBold(self.activeitem, False)
            if self.editor.IsModified():
                ## print "editor was modified"
                if message:
                    print(message) # moet dit niet messagebox zijn?
                ref = self.tree.GetItemPyData(self.activeitem)
                print self.tree.GetItemText(self.activeitem), ref
                try:
                    titel, tekst = self.itemdict[ref]
                except KeyError:
                    print "check_active: KeyError, waarschijnlijk op root"
                    ref = self.editor.GetValue()
                    if ref:
                        self.tree.SetItemPyData(self.root, ref) # self.opts["RootData"] = ref
                    ## print self.opts["RootData"] = ref
                else:
                    self.itemdict[ref] = (titel, self.editor.GetValue())

    def activate_item(self, item):
        """geselecteerd item "actief" maken (accentueren)"""
        ## print "activating item", item, self.tree.GetItemText(item)
        self.activeitem = item
        self.tree.SetItemBold(item, True)
        ref = self.tree.GetItemPyData(item)
        print self.tree.GetItemText(item), ref
        try:
            titel, tekst = self.itemdict[ref]
        except KeyError:
            print "activate_item: KeyError, waarschijnlijk op root"
            self.editor.SetValue(ref) # self.opts["RootData"])
        else:
            self.editor.SetValue(self.itemdict[ref][1])
        self.editor.Enable(True)

    def info_page(self,event=None):
        """help -> about"""
        info = [
            "DocTree door Albert Visser",
            "Electronisch notitieblokje",
            ]
        dlg = wx.MessageDialog(self, "\n".join(info),'DocTree',
            wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def help_page(self,event=None):
        """help -> keys"""
        info = [
            "Ctrl-N                   - nieuwe notitie onder huidige",
            "Shift-Ctrl-N             - nieuwe notitie onder hoogste niveau",
            "Insert                   - nieuwe notitie achter huidige",
            "Ctrl-PgDn    in editor of"
            " CursorDown in tree      - volgende notitie",
            "Ctrl-PgUp    in editor of"
            " CursorUp   in tree      - vorige notitie",
            "Ctrl-D of Delete in tree - verwijder notitie",
            "Ctrl-S                   - alle notities opslaan",
            "Shift-Ctrl-S             - alle notities opslaan omder andere naam",
            "Ctrl-R                   - alle notities opnieuw laden",
            "Ctrl-O                   - ander bestand met notities laden",
            "Ctrl-I                   - initialiseer (nieuw) notitiebestand",
            "Ctrl-Q, Esc              - opslaan en sluiten",
            "Ctrl-H                   - verbergen in system tray",
            "",
            "F1                       - deze (help)informatie",
            "F2                       - wijzig notitie titel",
            "Shift-F2                 - wijzig root titel",
            ]
        dlg = wx.MessageDialog(self, "\n".join(info),'DocTree',
            wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

class App(wx.App):
    def __init__(self,fn):
        self.fn = fn
        wx.App.__init__(self, redirect=True, filename="doctree.log")
        print dt.datetime.today().strftime("%d-%m-%Y %H:%M:%S").join(
            ("\n------------------","------------------\n"))
        frame = MainWindow(None, -1, "DocTree - " + self.fn)
        self.SetTopWindow(frame)
        frame.project_file = self.fn
        e = frame.read()
        if e:
            messagebox(frame, e, "Error")

if __name__ == "__main__":
    app = App('MyMan.ini')
    app.MainLoop()