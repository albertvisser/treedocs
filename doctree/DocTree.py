#!/usr/bin/env python
# -*- coding: latin-1 -*-
import os
import wx
import pickle
import pprint

# van een ibm site afgeplukt

def MsgBox (window, string, title):
     dlg=wx.MessageDialog(window, string, title, wx.OK)
     dlg.ShowModal()
     dlg.Destroy()

class CheckDialog(wx.Dialog):
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

class main_window(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = (800, 500),
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.nt_icon = wx.Icon(os.path.join(
            os.path.dirname(__file__),"doctree.ico"),wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.nt_icon)
        mainwindow = self
        self.sb = self.CreateStatusBar()

        self.menudata = (
            ("&Main",(
                    ("Re&Load (Ctrl-L)",self.reread, 'Reread .ini file'),
                    ("&Save (Ctrl-S)",self.save, 'Save .ini file'),
                    ("",None,None),
                    ("&Root title (Shift-F2)", self.rename, 'Rename root'),
                    ("",None,None),
                    ("&Hide (Ctrl-H)", self.hide, 'verbergen in system tray'),
                    ("",None,None),
                    ("e&Xit (Ctrl-Q, Esc)",self.afsl, 'Exit program'),
                ),),
            ("&Note",(
                    ("&New (Ctrl-N)", self.add_item, 'Add note (below current level)'),
                    ("&Add (Insert)", self.insert_item, 'Add note (after current)'),
                    ("&Delete (Ctrl-D, Del)", self.delete_item, 'Remove note'),
                    ("Note &Title (F2)",self.ask_title, 'Rename current note'),
                    ("",None,None),
                    ("&Forward (Ctrl-PgDn)",self.next_note,'View next note'),
                    ("&Back (Ctrl-PgUp)",self.prev_note,'View previous note'),
                ),),
            ("&Help",(
                    ("&About",self.info_page, 'About this application'),
                    ("&Keys (F1)",self.help_page, 'Keyboard shortcuts'),
                ),),
            )
        self.create_menu()

        self.splitter = wx.SplitterWindow (self, -1, style=wx.NO_3D) # |wx.SP_3D
        self.splitter.SetMinimumPaneSize (1)

        self.tree = wx.TreeCtrl (self.splitter, -1,
            style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.TR_HAS_VARIABLE_ROW_HEIGHT)
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

    def create_menu(self):
        menuBar = wx.MenuBar()
        for item, data in self.menudata:
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
        skip = True
        keycode = event.GetKeyCode()
        win = event.GetEventObject()
        if event.GetModifiers() == wx.MOD_CONTROL: # evt.ControlDown()
            if keycode == ord("L"): # 76: Ctrl-L reload tabs
                self.reread()
            elif keycode == ord("N"): # 78: Ctrl-N nieuwe tab
                if event.GetModifiers() == wx.MOD_SHIFT:
                    self.add_item(root=self.tree) # eigenlijk: add_item_at_top
                else:
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
        elif keycode == wx.WXK_F1:
            self.help_page()
        elif keycode == wx.WXK_F2: # and win == self.tree:
            if event.GetModifiers() == wx.MOD_SHIFT:
                self.rename()
            else:
                self.rename_item()
        elif keycode == wx.WXK_INSERT and win == self.tree:
            self.insert_item() # insert_at_current_level
        elif keycode == wx.WXK_DELETE and win == self.tree:
            self.delete_item()
        elif keycode == wx.WXK_ESCAPE:
            self.afsl()
        if event and skip:
            event.Skip()

    def OnEvtText(self,event): # seems to work
        self.editor.IsModified = True

    def OnSelChanging(self, event=None): # works (tm)
        pass
        ## if event.GetItem() == self.root:
            ## event.Veto()

    def OnSelChanged(self, event=None): # works (tm)
        self.check_active()
        self.activate_item(event.GetItem())
        event.Skip()

    def open(self):
        def maak_item(parent, tag, text, children = None):
            if children is None:
                children = []
            item = self.tree.AppendItem (parent, tag)
            self.tree.SetItemPyData(item, text)
            for child in children:
                maak_item(item, *child)
            return item
        self.opts = {
            "AskBeforeHide": True,"ActiveItem": 0, "SashPosition": 180,
            "ScreenSize": (800, 500), "RootTitle": "MyNotes", "RootData": ""}
        self.nt_data = {}
        try:
            file = open(self.project_file)
        except IOError:
            return
        try:
            self.nt_data = pickle.load(file)
        except EOFError:
            return
        file.close()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot(os.path.splitext(os.path.split(self.project_file)[1])[0])
        item_to_activate = self.root
        self.editor.Clear()
        self.editor.Enable (False)
        for key, value in self.nt_data.items():
            if key == 0 and "AskBeforeHide" in value:
                for key,val in value.items():
                    self.opts[key] = val
            else:
                item = maak_item(self.root, *value)
                if key == self.opts["ActiveItem"]:
                    item_to_activate = item
        self.tree.SetItemText(self.root,self.opts["RootTitle"])
        self.tree.SetItemPyData(self.root, self.opts["RootData"])
        self.editor.SetValue(self.opts["RootData"])
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.Expand (self.root)
        self.tree.SelectItem(item_to_activate)
        self.tree.SetFocus()

    def reread(self,event=None):
        dlg=wx.MessageDialog(self, 'OK to reload?', 'DocTree', wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.open()

    def save(self, event=None):
        def lees_item(item):
            titel = self.tree.GetItemText(item)
            text = self.tree.GetItemPyData(item)
            kids = []
            tag, cookie = self.tree.GetFirstChild(item)
            while tag.IsOk():
                kids.append(lees_item(tag))
                tag, cookie = self.tree.GetNextChild(tag, cookie)
            return titel, text, kids
        self.check_active() # even zorgen dat de editor inhoud geassocieerd wordt
        self.opts["ScreenSize"] = self.GetSize()
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
        file = open(self.project_file,"w")
        pickle.dump(self.nt_data, file)
        file.close()

    def rename(self, event=None):
        dlg = wx.TextEntryDialog(self, 'Geef nieuwe titel voor het hoofditem:',
                'DocTree', self.tree.GetItemText(self.root))
        if dlg.ShowModal() == wx.ID_OK:
            self.tree.SetItemText(self.root,dlg.GetValue())
        dlg.Destroy()

    def hide(self, event=None):
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
        self.Show()
        self.tbi.Destroy()

    def afsl(self, event=None):
        self.save()
        self.Close()

    def add_item(self, event=None, root=None): # works
        # kijk waar de cursor staat (of altijd onderaan toevoegen?)
        title = "Geef een titel op voor het nieuwe item"
        ## root = self.activeitem
        ## if root is None:
            ## root = self.root
        text = ""
        new = self.ask_title(title, text)
        if not new:
            return
        new_title, extra_title = new
        self.check_active()
        item = self.tree.AppendItem (root, new_title)
        self.tree.SetItemPyData(item, "")
        self.editor.Clear()
        if extra_title:
            new_item = self.tree.AppendItem(item, extra_title)
            item = new_item
        self.activate_item(item)
        self.tree.Expand (root)
        if item != self.root:
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()

    def insert_item(self, event=None): # works
        # kijk waar de cursor staat (of altijd onderaan toevoegen?)
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
        self.editor.Clear()
        if extra_title:
            new_item = self.tree.AppendItem(item, extra_title)
            item = new_item
        self.activate_item(item)
        self.tree.Expand (root)
        if item != self.root:
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()

    def delete_item(self, event=None):
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
        title = 'Nieuwe titel voor het huidige item:'
        root = item = self.activeitem
        text = self.tree.GetItemText(item)
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
        self.activate_item(item)
        self.tree.Expand (root)
        if item != self.root:
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()

    def ask_title(self, _title, _text):
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

    def next_note(self, event=None):
        item = self.tree.GetNextSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)

    def prev_note(self, event=None):
        item = self.tree.GetPrevSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)

    def check_active(self,message=None): # works, I guess
        if self.activeitem:
            self.tree.SetItemBold(self.activeitem, False)
            if self.editor.IsModified:
                if message:
                    print(message)
                self.tree.SetItemPyData(self.activeitem,self.editor.GetValue())

    def activate_item(self, item): # works too, it would seem
        self.activeitem = item
        ## if item != self.root:
        self.tree.SetItemBold(item, True)
        self.editor.SetValue(self.tree.GetItemPyData(item))
        self.editor.Enable(True)
        ## else:
            ## self.editor.Clear()
            ## self.editor.Enable(False)

    def info_page(self,event=None):
        info = [
            "DocTree door Albert Visser",
            "Electronisch notitieblokje",
            ]
        dlg = wx.MessageDialog(self, "\n".join(info),'Apropos',
            wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def help_page(self,event=None):
        info = [
            "Ctrl-N                   - nieuwe notitie onder huidige",
            "Shift-Ctrl-N             - nieuwe notitie onder hoogste niveau",
            "Insert                   - nieuwe notitie achter huidige",
            "Ctrl-PgDn    in editor of"
            " CursorDown in tree      - volgende notitie",
            "Ctrl-PgUp    in editor of"
            " CursorUp   in tree      - vorige notitie",
            "Ctrl-D of Delete in tree - verwijder notitie",
            "Ctrl-S                   - alles opslaan",
            "Ctrl-L                   - alles opnieuw laden",
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
        wx.App.__init__(self,False)
        frame = main_window(None, -1, "DocTree - " + self.fn)
        self.SetTopWindow(frame)
        frame.project_file = self.fn
        frame.open()

if __name__ == "__main__":
    app = App('DocTree.ini')
    app.MainLoop()