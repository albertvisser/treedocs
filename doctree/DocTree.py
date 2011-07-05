#! /usr/bin/env python
# -*- coding: utf-8 -*-
# het principe (splitter window met een tree en een tekst deel) komt oorspronkelijk van een ibm site

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
    ## print("calling getsubtree on {}".format(titel))
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
    ## print("calling putsubtree on {}".format(titel))
    tree.SetItemPyData(new, text)
    for sub in subtree:
        putsubtree(tree, new, *sub)
    return new

def messagebox(window, string, title="DocTree"):
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

    ## def OnBeginDrag(self, event):
        ## print("start dragging")
        ## treemix.DragAndDrop.OnBeginDrag(self, event)

    ## def OnDragging(self, event):
        ## print("keep dragging")
        ## treemix.DragAndDrop.OnDragging(self, event)

    ## def OnEndDrag(self, event):
        ## print("stop dragging")
        ## treemix.DragAndDrop.OnEndDrag(self, event)

    def OnDrop(self, dropitem, dragitem):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item"""
        if dropitem == self.GetRootItem():
            ## print("drop on rootitem")
            return
        ## print self.GetItemText(dropitem)
        if dropitem is None:
            ## print("dropitem is None")
            dropitem = self.root
        dragText = self.GetItemText(dragitem)
        dragData = self.GetItemPyData(dragitem)
        dragtree = getsubtree(self, dragitem)
        ## pprint.pprint(dragtree)
        dropText = self.GetItemText(dropitem)
        dropData = self.GetItemPyData(dropitem)
        print('drop "%s" on "%s" ' % (dragText, dropText))
        self.Delete(dragitem)
        ## item = self.AppendItem(dropitem, dragText)
        ## self.SetItemPyData(item, dragData)
        putsubtree(self, dropitem, *dragtree)
        self.Expand(dropitem)

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        self.opts = {
            "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
            "ActiveItem": [0,], "ActiveView": 0, "ViewNames": ["Default",],
            "RootTitle": "MyNotes", "RootData": ""}
        wx.Frame.__init__(self, parent, -1, title, size = self.opts['ScreenSize'],
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.nt_icon = wx.Icon(os.path.join(
            os.path.dirname(__file__),"doctree.ico"),wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.nt_icon)
        mainwindow = self
        self.sb = self.CreateStatusBar()

        self.create_menu((
            ("&Main", (
                ("Re&Load (Ctrl-R)", self.reread, 'Reread .ini file'),
                ("&Open (Ctrl-O)", self.open, "Choose and open .ini file"),
                ("&Init (Ctrl-I)", self.new, 'Start a new .ini file'),
                ("&Save (Ctrl-S)", self.save, 'Save .ini file'),
                ("Save as (Shift-Ctrl-S)", self.saveas, 'Name and save .ini file'),
                ("", None, None),
                ("&Root title (Shift-F2)", self.rename_root, 'Rename root'),
                ("Items sorteren", self.order_top, 'Bovenste niveau sorteren op titel'),
                ("Items recursief sorteren", self.order_all, 'Alle niveaus sorteren op titel'),
                ("", None, None),
                ("&Hide (Ctrl-H)", self.hide, 'verbergen in system tray'),
                ("", None, None),
                ("e&Xit (Ctrl-Q, Esc)", self.afsl, 'Exit program'),
                ), ),
            ("&Note", (
                ("&New (Ctrl-N)", self.add_item, 'Add note (below current level)'),
                ("&Add (Insert)", self.insert_item, 'Add note (after current)'),
                ("&Delete (Ctrl-D, Del)", self.delete_item, 'Remove note'),
                ("", None, None),
                ("Note &Title (F2)", self.rename_item, 'Rename current note'),
                ("Subitems sorteren", self.order_this, 'Onderliggend niveau sorteren op titel'),
                ("Subitems recursief sorteren", self.order_lower, 'Alle onderliggende niveaus sorteren op titel'),
                ("", None, None),
                ("&Forward (Ctrl-PgDn)", self.next_note, 'View next note'),
                ("&Back (Ctrl-PgUp)", self.prev_note, 'View previous note'),
                ),),
            ("&View", (
                ('&New View', self.add_view, 'Add an alternative view (tree) to this data'),
                ('&Rename Current View', self.rename_view, 'Rename the current tree view'),
                ('&Delete Current View', self.remove_view, 'Remove the current tree view'),
                ("", None, None),
                ), ),
            ("&Help", (
                    ("&About", self.info_page, 'About this application'),
                    ("&Keys (F1)", self.help_page, 'Keyboard shortcuts'),
                ), ),
            )
        )

        self.splitter = wx.SplitterWindow (self, -1, style = wx.NO_3D) # |wx.SP_3D
        self.splitter.SetMinimumPaneSize (1)
        self.splitter.SetSashPosition(self.opts['SashPosition'], True)

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

        self.tree.SetFocus()
        self.Show(True)

    def create_menu(self, menudata):
        """bouw het menu op"""
        menuBar = wx.MenuBar()
        for item, data in menudata:
            menu_label = item
            submenu = wx.Menu()
            if item == "&View":
                self.viewmenu = submenu
            for label, handler, info in data:
                if label != "":
                    menu_item = wx.MenuItem(submenu, -1, label, info)
                    self.Bind(wx.EVT_MENU, handler, menu_item)
                    submenu.AppendItem(menu_item)
                else:
                    ## menu_item = wx.MenuItem(submenu, wx.ID_SEPARATOR)
                    submenu.AppendSeparator()
                ## submenu.AppendItem(menu_item)
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
                self.rename_root()
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
        ## messagebox(self, "onselchanged aangeroepen op {} {}".format(x,
            ## self.tree.GetItemText(x)), 'AHEM')
        self.check_active()
        self.activate_item(x)
        ## print "self.editor.IsModified is nu", self.editor.IsModified
        event.Skip()

    def set_title(self):
        self.SetTitle("DocTree - {} (view: {})".format(os.path.split(self.project_file)[1],
            self.opts["ViewNames"][self.opts['ActiveView']]))

    def open(self, event=None):
        "afhandelen Menu > Open / Ctrl-O"
        dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self, "DocTree - choose file to open",
            dirname, "", "INI files|*.ini", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename, dirname = dlg.GetFilename(), dlg.GetDirectory()
            ## self.save_needed()
            self.project_file = os.path.join(dirname, filename)
            ## print "ok, reading", self.project_file
            e = self.read()
            if e:
                messagebox(self,e, "Error")
        dlg.Destroy()

    def new(self, event=None):
        "Afhandelen Menu - Init / Ctrl-I"
        self.save_needed()
        dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self, "DocTree - enter name for new file",
            dirname, "", "INI files|*.ini", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename, dirname = dlg.GetFilename(), dlg.GetDirectory()
            self.project_file = os.path.join(dirname, filename)
            self.has_treedata = True
            self.tree.DeleteAllItems()
            root = self.tree.AddRoot("hidden_root")
            self.tree.SetItemPyData(root, '')
            rootitem = self.tree.AppendItem(root, os.path.splitext(
                os.path.basename(self.project_file))[0])
            self.activeitem = self.root = rootitem
            self.tree.SetItemBold(rootitem, True)
            self.views = [[],]
            self.viewcount = 1
            self.itemdict = {}
            self.opts = {
                "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
                "ActiveItem": [0,], "ActiveView": 0, "ViewNames": ["Default",],
                "RootTitle": "MyNotes", "RootData": ""}
            _id = wx.NewId()
            menu_item = wx.MenuItem(self.viewmenu, _id, '&Default',
                'Switch to this view', wx.ITEM_CHECK)
            self.Bind(wx.EVT_MENU, self.select_view, menu_item)
            self.viewmenu.AppendItem(menu_item)
            menu_item.Check()
            self.SetSize(self.opts["ScreenSize"])
            self.splitter.SetSashPosition(self.opts["SashPosition"], True)
            self.tree.SetItemText(self.root,self.opts["RootTitle"].rstrip())
            self.tree.SetItemPyData(self.root, self.opts["RootData"])
            self.editor.SetValue(self.opts["RootData"])
            self.editor.Enable(True)
            self.editor.Clear()
            self.set_title()
            self.tree.SetFocus()
        dlg.Destroy()

    def save_needed(self):
        """eigenlijk bedoeld om te reageren op een indicatie dat er iets aan de
        verzameling notities is gewijzigd (de oorspronkelijke self.project_dirty)"""
        ## self.save()
        if not self.has_treedata:
            return
        dlg=wx.MessageDialog(self, "Save current file before continuing?",
            "DocTree", wx.YES_NO)
        h = dlg.ShowModal()
        if h == wx.ID_YES:
            self.save()
        dlg.Destroy()

    def treetoview(self):
        """zet de visuele tree om in een tree om op te slaan"""
        def lees_item(item):
            """recursieve functie om de data in een pickle-bare structuur om te zetten"""
            ## titel = self.tree.GetItemText(item)
            textref = self.tree.GetItemPyData(item)
            if item == self.activeitem:
                print "lees_item voor activeview {}: activeitem is {}".format(
                    self.opts["ActiveView"], self.tree.GetItemText(item))
                self.opts["ActiveItem"][self.opts["ActiveView"]] = textref
            kids = []
            tag, cookie = self.tree.GetFirstChild(item)
            while tag.IsOk():
                kids.append(lees_item(tag))
                tag, cookie = self.tree.GetNextChild(item, cookie) # tag, cookie)
            return textref, kids
        ## messagebox(self, "starting treetoview")
        data = []
        tag, cookie = self.tree.GetFirstChild(self.root)
        while tag.IsOk():
            data.append(lees_item(tag))
            tag, cookie = self.tree.GetNextChild(self.root, cookie)
        ## messagebox(self, "ending treetoview")
        return data

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
        ## messagebox(self, "starting viewtotree")
        item_to_activate = 0
        current_view = self.views[self.opts['ActiveView']]
        for item in current_view:
            x, y = maak_item(self.root, *item)
            if y is not None:
                item_to_activate = y
        ## messagebox(self, "ending viewtotree")
        return item_to_activate

    def read(self):
        """settings dictionary lezen, opgeslagen data omzetten naar tree"""
        ## print self.project_file.join(("reading: ","..."))
        self.has_treedata = False
        self.opts = {
            "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
            "ActiveItem": [0,], "ActiveView": 0, "ViewNames": ["Default",],
            "RootTitle": "MyNotes", "RootData": ""}
        mld = ''
        try:
            file = open(self.project_file,"rb")
        except IOError:
            return "couldn't open "+ self.project_file
        try:
            nt_data = pck.load(file)
        except EOFError:
            mld = "couldn't load data"
        finally:
            file.close()
        if mld:
            return mld
        ## pprint.pprint(nt_data)
        self.has_treedata = True
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemPyData(root, '')
        self.root = self.tree.AppendItem(root, os.path.splitext(
            os.path.basename(self.project_file))[0])
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
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.SetItemText(self.root,self.opts["RootTitle"].rstrip())
        self.tree.SetItemPyData(self.root, self.opts["RootData"])
        self.editor.SetValue(self.opts["RootData"])
        print "read - RootData:", self.opts["RootData"]
        ## self.editor.IsModified = False
        for ix, name in enumerate(self.opts["ViewNames"]):
            # nieuwe menu items toevoegen
            menu_item = wx.MenuItem(self.viewmenu, -1, name, "switch to this view",
                wx.ITEM_CHECK)
            self.Bind(wx.EVT_MENU, self.select_view, menu_item)
            self.viewmenu.AppendItem(menu_item)
            if ix == self.opts["ActiveView"]:
                menu_item.Check()
        item_to_activate = self.viewtotree()
        self.tree.Expand(self.root)
        if item_to_activate != self.activeitem:
            self.tree.SelectItem(item_to_activate)
        self.set_title()
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
        self.sb.SetStatusText('{} opgeslagen'.format(self.project_file))

    def write(self, event=None, meld=True):
        """settings en tree data in een structuur omzetten en opslaan"""
        # TODO: aanpassen voor wegschrijven multiple trees met aparte data
        ## print "write - active item was",self.tree.GetItemText(self.activeitem)
        self.check_active() # even zorgen dat de editor inhoud geassocieerd wordt
        self.opts["ScreenSize"] = tuple(self.GetSize())
        self.opts["SashPosition"] = self.splitter.GetSashPosition()
        ## self.opts["RootTitle"] = self.tree.GetItemText(self.root)
        ## self.opts["RootData"] = self.tree.GetItemPyData(self.root)
        ## print len(self.views), "views aanwezig"
        self.views[self.opts["ActiveView"]] = self.treetoview()
        nt_data = {0: self.opts, 1: self.views, 2: self.itemdict}
        pprint.pprint(nt_data)
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
        dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self,"DocTree - Save File as:", dirname, "",
            "INI files|*.ini", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename, dirname = dlg.GetFilename(), dlg.GetDirectory()
            self.project_file = os.path.join(dirname, filename)
            self.write()
            self.set_title()
            ## if self.original_name:
                ## self.project_file = original_name
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
        if self.has_treedata:
            self.save(meld=False)
        if event:
            event.Skip()

    def add_view(self,event=None):
        "handles Menu > View > New view"
        self.check_active() # even zorgen dat de editor inhoud geassocieerd wordt
        self.opts["ActiveItem"][self.opts["ActiveView"]] = self.tree.GetItemPyData(
            self.activeitem)
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.viewcount += 1
        new_view = "New View #{}".format(self.viewcount)
        self.opts["ViewNames"].append(new_view)
        active = self.opts["ActiveItem"][self.opts["ActiveView"]]
        self.opts["ActiveItem"].append(active)
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for ix, menuitem in enumerate(menuitem_list[4:]):
            if ix == self.opts["ActiveView"]:
                menuitem.Check(False)
        menu_item = wx.MenuItem(self.viewmenu, -1, new_view, "switch to this view",
            wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.select_view, menu_item)
        self.viewmenu.AppendItem(menu_item)
        menu_item.Check()
        self.opts["ActiveView"] = self.opts["ViewNames"].index(new_view) # = self.viewcount - 1
        ## messagebox(self, "nieuwe tree maken")
        ## self.tree.DeleteChildren(self.root)
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemPyData(root, '')
        self.root = self.tree.AppendItem(root, os.path.splitext(
            os.path.basename(self.project_file))[0])
        self.tree.SetItemText(self.root,self.opts["RootTitle"].rstrip())
        self.tree.SetItemPyData(self.root, self.opts["RootData"])

        ## messagebox(self, "eerst alles onder root weg: {}".format(self.root))
        newtree = []
        for key in sorted(self.itemdict.keys()):
            newtree.append((key, []))
        ## messagebox(self, "nieuwe tree toevoegen aan self.views")
        self.views.append(newtree)
        ## messagebox(self, "nieuwe visuele tree opbouwen")
        tree_item = self.viewtotree()
        self.set_title()
        self.tree.SelectItem(tree_item)

    def rename_view(self,event=None):
        "handles Menu > View > Rename current view"
        oldname = self.opts["ViewNames"][self.opts["ActiveView"]]
        dlg = wx.TextEntryDialog(self, 'Geef een nieuwe naam voor de huidige view',
                'DocTree', oldname)
        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            if newname != oldname:
                self.viewmenu.GetMenuItems()[self.opts["ActiveView"] + 4].SetItemLabel(
                    newname)
                self.opts["ViewNames"][self.opts["ActiveView"]] = newname
                self.set_title()
        dlg.Destroy()

    def select_view(self,event=None):
        "handles Menu > View > <view name>"
        self.check_active() # even zorgen dat de editor inhoud geassocieerd wordt
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.editor.Clear()
        menu_id = event.GetId()
        ## print "the chosen menu's id is {}".format(menu_id)
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for menuitem in menuitem_list[4:]:
            ## print('checking menu item {}: id is {}'.format(menuitem.GetItemLabelText(),
                ## menuitem.GetId())
            if menuitem.GetId() == menu_id:
                newview = menuitem.GetItemLabelText()
                ## if not menuitem.IsChecked():
                menuitem.Check()
            else:
                if menuitem.IsChecked():
                    menuitem.Check(False)
        self.opts["ActiveView"] = self.opts["ViewNames"].index(newview)
        print('switching to view {}: {}'.format(self.opts["ActiveView"], newview))
        ## self.tree.DeleteChildren(self.root)
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemPyData(root, '')
        self.root = self.tree.AppendItem(root, os.path.splitext(
            os.path.basename(self.project_file))[0])
        self.tree.SetItemText(self.root, self.opts["RootTitle"].rstrip())
        self.tree.SetItemPyData(self.root, self.opts["RootData"])
        self.set_title()

        self.tree.SelectItem(self.viewtotree())

    def remove_view(self,event=None):
        "handles Menu > View > Delete current view"
        dlg=wx.MessageDialog(self, "Are you sure you want to remove this view?",
            "DocTree", wx.YES_NO)
        h = dlg.ShowModal()
        if h == wx.ID_YES:
            self.viewcount -= 1
            viewname = self.opts["ViewNames"][self.opts["ActiveView"]]
            self.opts["ViewNames"].remove(viewname)
            self.opts["ActiveItem"].pop(self.opts["ActiveView"])
            self.views.pop(self.opts["ActiveView"])
            if self.opts["ActiveView"] > 0:
                self.opts["ActiveView"] -= 1
            menuitem_list = self.viewmenu.GetMenuItems()
            menuitem_list[self.opts["ActiveView"] + 4].Check()
            for menuitem in menuitem_list:
                if menuitem.GetItemLabelText() == viewname:
                    self.viewmenu.DeleteItem(menuitem)
                    break
            if self.opts["ActiveView"] == 0:
                menuitem_list[4].Check()
            ## self.tree.DeleteChildren(self.root)
            self.tree.DeleteAllItems()
            root = self.tree.AddRoot("hidden_root")
            self.tree.SetItemPyData(root, '')
            self.root = self.tree.AppendItem(root, os.path.splitext(
                os.path.basename(self.project_file))[0])
            self.tree.SetItemText(self.root,self.opts["RootTitle"].rstrip())
            self.tree.SetItemPyData(self.root, self.opts["RootData"])
            self.tree.SelectItem(self.viewtotree())
            self.set_title()
        dlg.Destroy()

    def rename_root(self, event=None):
        """afhandelen Menu > Rename Root (Shift-Ctrl-F2"""
        dlg = wx.TextEntryDialog(self, 'Geef nieuwe titel voor het hoofditem:',
                'DocTree', self.tree.GetItemText(self.root))
        if dlg.ShowModal() == wx.ID_OK:
            newtitle = dlg.GetValue()
            self.tree.SetItemText(self.root, newtitle)
            self.opts['RootTitle'] = newtitle
        dlg.Destroy()

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
            if ix != self.opts["ActiveView"]:
                print "andere views updaten:", ix
                subitem = []
                if extra_title:
                    subitem.append((subkey,[]))
                view.append((newkey, subitem))
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
        def check_item(view, ref):
            for item, subview in view:
                if item == ref:
                    view.pop((item, subview))
                else:
                    check_item(item)
            tag, cookie = view.GetFirstChild(item) # moet dit niet self.tree.Get... zijn?
            while tag.IsOk():
                textref = view.GetItemPyData(tag) # moet dit niet self.tree.Get... zijn?
                if textref == ref:
                    view.Delete(tag) # moet dit niet self.tree.Delete zijn?
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
                    check_item(view, ref)
            self.activate_item(prev)
        else:
            messagebox(self, "Can't delete root", "Error")

    def rename_item(self):
        """titel van item wijzigen"""
        def check_item(view, item, ref, new_title, extra_title, subref):
            retval = ""
            tag, cookie = view.GetFirstChild(item) # moet dit niet self.tree.Get... zijn?
            while tag.IsOk():
                textref = view.GetItemPyData(tag) # moet dit niet self.tree.Get... zijn?
                if textref == ref:
                    view.SetItemText(tag, new_title) # moet dit niet self.tree.Delete zijn?
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
        self.tree.SetItemText(self.activeitem, new_title)
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
                print("check_active op {}".format(self.tree.GetItemText(self.activeitem)))
                try:
                    titel, tekst = self.itemdict[ref]
                except KeyError:
                    print "check_active: KeyError, waarschijnlijk op root - ref is", ref
                    ref = self.editor.GetValue()
                    print('ref is nu {}'.format(ref))
                    if ref:
                        self.tree.SetItemPyData(self.root, ref)
                        self.opts["RootData"] = ref
                    ## print self.opts["RootData"] = ref
                else:
                    self.itemdict[ref] = (titel, self.editor.GetValue())

    def activate_item(self, item):
        """geselecteerd item "actief" maken (accentueren)"""
        ## print "activating item", item, self.tree.GetItemText(item)
        self.activeitem = item
        self.tree.SetItemBold(item, True)
        ref = self.tree.GetItemPyData(item)
        ## print self.tree.GetItemText(item), ref
        ## print "activate_item op {}".format(self.tree.GetItemText(item))
        try:
            titel, tekst = self.itemdict[ref]
        except KeyError:
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