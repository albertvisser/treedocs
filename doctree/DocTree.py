#! /usr/bin/env python

# -*- coding: latin-1 -*-
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

def MsgBox(window, string, title):
    """Toon een boodschap"""
    print "MsgBox aangeroepen:", string
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

class main_window(wx.Frame):
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
                ("Re&Load (Ctrl-L)",self.reread, 'Reread .ini file'),
                ("&Open (Shift-Ctrl-L)",self.open,"Choose and open .ini file"),
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
                ("Note &Title (F2)",self.ask_title, 'Rename current note'),
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
        self.editor.Bind(wx.EVT_TEXT, self.OnEvtText)
        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.splitter.SplitVertically(self.tree, self.editor)
        self.splitter.SetSashPosition(180, True)
        self.splitter.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

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
        if mods == wx.MOD_CONTROL: # evt.ControlDown()
            if keycode == ord("L"): # 76: Ctrl-L Load tabs
                self.open()
            elif keycode == ord("I"):
                self.new()
            elif keycode == ord("N"): # 78: Ctrl-N nieuwe tab
                self.add_item(root=self.activeitem)
            elif keycode == ord("D"):
                self.delete_item()
            elif keycode == ord("H"): # 72: Ctrl-H Hide/minimize
                self.hide()
            elif keycode == ord("S"): # 83: Ctrl-S saven zonder afsluiten
                self.save()
            elif keycode == ord("Q"): # 81: Ctrl-Q afsluiten na saven
                self.afsl()
            elif keycode == wx.WXK_PAGEDOWN: #  and win == self.editor:
                self.next_note()
            elif keycode == wx.WXK_PAGEUP: #  and win == self.editor:
                self.prev_note()
        elif mods == wx.MOD_CONTROL | wx.MOD_SHIFT: # evt.ControlDown()
            if keycode == ord("L"): # 76: Shift-Ctrl-L reload tabs
                self.reread()
            elif keycode == ord("N"): # 78: Shift-Ctrl-N nieuwe tab
                self.add_item(root=self.root) # eigenlijk: add_item_at_top
            elif keycode == ord("S"): # 83: Shift-Ctrl-S
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
            if self.editor.IsModified:
                self.tree.SetItemPyData(self.activeitem,self.editor.GetValue())
        elif keycode == wx.WXK_ESCAPE:
            self.afsl()
        if event and skip:
            event.Skip()

    def OnEvtText(self,event): # seems to work
        "als er iets met de tekst gebeurt de editor-inhoud als 'aangepast' markeren"
        self.editor.IsModified = True

    def OnSelChanging(self, event=None): # works (tm)
        "was ooit bedoeld om acties op de root te blokkeren"
        ## if event.GetItem() == self.root:
            ## event.Veto()
        event.Skip()

    def OnSelChanged(self, event=None): # works (tm)
        """zorgen dat het eerder actieve item onthouden wordt, daarna het geselecteerde
        tot nieuw actief item benoemen"""
        self.check_active()
        self.activate_item(event.GetItem())
        event.Skip()

    def open(self, event=None):
        self.dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self, "DocTree - choose file to open",
            self.dirname, "", "INI files|*.ini", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            ## self.save_needed()
            self.project_file = os.path.join(self.dirname,self.filename)
            print "ok, reading", self.project_file
            e = self.read()
            if e:
                MsgBox(self,e, "Error")
            else:
                self.SetTitle("DocTree - " + self.filename)
        dlg.Destroy()

    def new(self, event=None):
        self.dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self, "DocTree - enter name for new file",
            self.dirname, "", "INI files|*.ini", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.save_needed()
            self.project_file = os.path.join(self.dirname,self.filename)
            self.nt_data = {}
            self.tree.DeleteAllItems()
            root = self.tree.AddRoot("hidden_root")
            item = self.tree.AppendItem(root, os.path.splitext(
                os.path.split(self.project_file)[1])[0])
            self.activeitem = self.root = item
            self.tree.SetItemBold(item, True)
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
            "DocTree", wx.YESNO)
        if dlg.ShowModal() == wx.YES:
            self.save()
        dlg.Destroy()

    def read(self):
        """settings dictionary lezen, opgeslagen data omzetten naar tree"""
        def maak_item(parent, tag, text, children = None):
            """recursieve functie om de TreeCtrl op te bouwen vanuit de opgeslagen data"""
            if children is None:
                children = []
            item = self.tree.AppendItem (parent, tag.rstrip())
            self.tree.SetItemPyData(item, text.rstrip())
            for child in children:
                maak_item(item, *child)
            return item
        ## print self.project_file.join(("reading: ","..."))
        self.opts = {
            "AskBeforeHide": True,"ActiveItem": 0, "SashPosition": 180,
            "ScreenSize": (800, 500), "RootTitle": "MyNotes", "RootData": ""}
        self.nt_data = {}
        try:
            file = open(self.project_file,"rb")
        except IOError:
            return "couldn't open "+ self.project_file
        try:
            self.nt_data = pck.load(file)
        except EOFError:
            return "couldn't load data"
        file.close()
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.root = self.tree.AppendItem(root, os.path.splitext(
            os.path.split(self.project_file)[1])[0])
        self.activeitem = item_to_activate = self.root
        self.editor.Clear()
        ## self.editor.Enable (False)
        for key, value in self.nt_data.items():
            if key == 0 and "AskBeforeHide" in value:
                for key,val in value.items():
                    self.opts[key] = val
            else:
                item = maak_item(self.root, *value)
                if key == self.opts["ActiveItem"]:
                    item_to_activate = item
        self.tree.SetItemText(self.root,self.opts["RootTitle"].rstrip())
        self.tree.SetItemPyData(self.root, self.opts["RootData"])
        self.editor.SetValue(self.opts["RootData"])
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.Expand (self.root)
        if item_to_activate != self.activeitem:
            self.tree.SelectItem(item_to_activate)
        self.tree.SetFocus()

    def reread(self,event=None):
        dlg=wx.MessageDialog(self, 'OK to reload?', 'DocTree', wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.read()

    def save(self, event=None, meld=True):
        if self.project_file:
            self.write(meld=meld)
        else:
            self.saveas()

    def write(self, event=None, meld=True):
        """settings en tree data in een structuur omzetten en opslaan"""
        def lees_item(item):
            """recursieve functie om de data in een pickle-bare structuur om te zetten"""
            titel = self.tree.GetItemText(item)
            text = self.tree.GetItemPyData(item)
            kids = []
            tag, cookie = self.tree.GetFirstChild(item)
            while tag.IsOk():
                kids.append(lees_item(tag))
                tag, cookie = self.tree.GetNextChild(item, cookie) # tag, cookie)
            return titel, text, kids
        ## print "save - active item was",self.tree.GetItemText(self.activeitem)
        self.check_active() # even zorgen dat de editor inhoud geassocieerd wordt
        self.opts["ScreenSize"] = tuple(self.GetSize())
        self.opts["SashPosition"] = self.splitter.GetSashPosition()
        self.opts["RootTitle"] = self.tree.GetItemText(self.root)
        self.opts["RootData"] = self.tree.GetItemPyData(self.root)
        ky = 0
        self.nt_data = {ky: self.opts}
        tag, cookie = self.tree.GetFirstChild(self.root)
        while tag.IsOk():
            ky += 1
            if tag == self.activeitem:
                self.opts["ActiveItem"] = ky
            self.nt_data[ky] = lees_item(tag)
            tag, cookie = self.tree.GetNextChild(self.root, cookie)
        try:
            shutil.copyfile(self.project_file,self.project_file + ".bak")
        except IOError:
            pass
        file = open(self.project_file,"w")
        pck.dump(self.nt_data, file)
        file.close()
        if meld:
            MsgBox(self, self.project_file + " is opgeslagen","DocTool")
        self.SetTitle("DocTree - " + self.project_file)

    def saveas(self, event=None):
        ## original_name = self.project_file
        self.dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self,"DocTree - Save File as:", self.dirname, "",
            "INI files|*.ini", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.project_file = os.path.join(self.dirname,self.filename)
            self.write()
            ## if self.original_name:
                ## self.project_file = original_name
        dlg.Destroy()

    def rename(self, event=None):
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
        self.Close()

    def add_item(self, event=None, root=None): # works
        """nieuw item toevoegen onder het geselecteerde"""
        if root is None:
            root = self.activeitem if self.activeitem else self.root
        title = "Geef een titel op voor het nieuwe item"
        text = ""
        new = self.ask_title(title, text)
        if not new:
            return
        new_title, extra_title = new
        self.check_active()
        item = self.tree.AppendItem (root, new_title)
        self.tree.SetItemPyData(item, "")
        ## self.editor.Clear()
        if extra_title:
            new_item = self.tree.AppendItem(item, extra_title)
            item = new_item
        self.tree.SelectItem(item) #   self.activate_item(item)
        self.tree.Expand (root)
        if item != self.root:
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()

    def insert_item(self, event=None): # works
        """nieuw item toevoegen *achter* het geselecteerde (en onder diens parent)"""
        title = "Geef een titel op voor het nieuwe item"
        root = self.tree.GetItemParent(self.activeitem)
        text = ""
        new = self.ask_title(title, text)
        if not new:
            return
        new_title, extra_title = new
        self.check_active()
        item = self.tree.InsertItem (root, self.activeitem, new_title)
        self.tree.SetItemPyData(item, "")
        ## self.editor.Clear()
        if extra_title:
            new_item = self.tree.AppendItem(item, extra_title)
            item = new_item
        self.tree.SelectItem(item) # self.activate_item(item)
        self.tree.Expand (root)
        if item != self.root:
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()

    def delete_item(self, event=None):
        """item verwijderen"""
        item = self.tree.GetSelection()
        if item != self.root:
            prev = self.tree.GetPrevSibling(item)
            if not prev.IsOk():
                prev = self.tree.GetItemParent(item)
            print self.tree.GetItemText(prev)
            self.activeitem = None
            self.tree.Delete(item)
            self.activate_item(prev)
        else:
            MsgBox(self, "Can't delete root", "Error")

    def rename_item(self):
        """titel van item wijzigen"""
        title = 'Nieuwe titel voor het huidige item:'
        root = item = self.activeitem
        text = self.tree.GetItemText(item)
        self.check_active()
        new = self.ask_title(title, text)
        if not new:
            return
        new_title, extra_title = new
        self.tree.SetItemText(self.activeitem,new_title)
        if extra_title:
            data = self.tree.GetItemPyData(self.activeitem)
            ## self.tree.SetItemPyData(self.activeitem, "")
            new_item = self.tree.AppendItem(self.activeitem, extra_title)
            self.tree.SetItemPyData(new_item, data)
            item = new_item
        self.tree.Expand (root)
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
        print "order_top"
        self.reorder_items(self.root)

    def order_all(self,event=None):
        print "order_all"
        self.reorder_items(self.root, recursive=True)

    def reorder_items(self, root, recursive=False):
        ## print "sorteren werkt nog niet helemaal niet"
        ## return
        # dit moet eigenlijk met recursieve ondervoeg routines die ook bij copy-paste gebruikt
        # (kunnen) worden
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
        print "order_this"
        self.reorder_items(self.activeitem)

    def order_lower(self,event=None):
        print "order_lower"
        self.reorder_items(self.activeitem, recursive=True)

    def next_note(self, event=None):
        item = self.tree.GetNextSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)

    def prev_note(self, event=None):
        item = self.tree.GetPrevSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)

    def check_active(self,message=None): # works, I guess
        """zorgen dat de editor inhoud voor het huidige item bewaard wordt in de treectrl"""
        ## print "check_active",self.activeitem
        if self.activeitem:
            self.tree.SetItemBold(self.activeitem, False)
            if self.editor.IsModified:
                if message:
                    print(message)
                self.tree.SetItemPyData(self.activeitem,self.editor.GetValue())

    def activate_item(self, item): # works too, it would seem
        """geselecteerd item "actief" maken (accentueren)"""
        self.activeitem = item
        ## if item != self.root:
        self.tree.SetItemBold(item, True)
        self.editor.SetValue(self.tree.GetItemPyData(item))
        self.editor.Enable(True)
        ## else:
            ## self.editor.Clear()
            ## self.editor.Enable(False)

    def info_page(self,event=None):
        """help -> about"""
        info = [
            "DocTree door Albert Visser",
            "Electronisch notitieblokje",
            ]
        dlg = wx.MessageDialog(self, "\n".join(info),'Apropos',
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
            "Ctrl-L                   - alle notities opnieuw laden",
            "Shift-Ctrl-L             - ander bestand met notities laden",
            "Ctrl-I                   - initialiseer (nieuw) notitiebestand"
            "Ctrl-Q, Esc              - opslaan en sluiten",
            "Ctrl-H                   - verbergen in system tray",
            "",
            "F1                       - deze (help)informatie",
            "F2                       - wijzig notitie titel",
            "Shift-F2                 - wijzig root titel",
            ]
        dlg = wx.MessageDialog(self, "\n".join(info),'Apropos',
            wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

class App(wx.App):
    def __init__(self,fn):
        self.fn = fn
        wx.App.__init__(self, redirect=True, filename="doctree.log")
        print dt.datetime.today().strftime("%d-%m-%Y %H:%M:%S").join(("\n------------------","------------------\n"))
        frame = main_window(None, -1, "DocTree - " + self.fn)
        self.SetTopWindow(frame)
        frame.project_file = self.fn
        e = frame.read()
        if e:
            MsgBox(frame, e, "Error")

if __name__ == "__main__":
    app = App('DocTree.ini')
    app.MainLoop()