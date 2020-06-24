"""DocTree: wxPython specific stuff
"""
import os
import tempfile
import wx
import wx.adv
import wx.lib.mixins.treemixin as treemix
import wx.richtext as rt
import doctree.shared as shared


def show_message(win, text):
    "show a confirmable message"
    with wx.MessageDialog(win, text, "DocTree", wx.OK | wx.ICON_INFORMATION) as dlg:
        dlg.ShowModal()


def ask_ynquestion(win, text):
    "ask a yes/no answerable question"
    with wx.MessageDialog(win, text, 'DocTree', wx.YES_NO | wx.ICON_QUESTION) as dlg:
        result = dlg.ShowModal()
    return result == wx.ID_YES


def ask_yncquestion(win, text):
    "ask a yes/no answerable question with possibilty to cancel"
    with wx.MessageDialog(win, text, 'DocTree', wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION) as dlg:
        result = dlg.ShowModal()
    return result == wx.ID_YES, result == wx.ID_CANCEL


def get_text(win, caption, oldtext):
    "open a dalog and get text input from the user"
    newtext = oldtext
    with wx.TextEntryDialog(win, caption, 'DocTree', oldtext) as dlg:
        ok = dlg.ShowModal() == wx.ID_OK
        newtext = dlg.GetValue()
    return ok, newtext


def get_filename(win, title, start, save=False):
    "routine for selection of filename"
    filter = "Pickle files (*.pck)|*.pck"
    start = os.path.dirname(start)
    if save:
        dlg = wx.FileDialog(win, title, start, '', filter, wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    else:
        dlg = wx.FileDialog(win, title, start, '', filter, wx.FD_OPEN)
    ok, filename = False, ''
    with dlg:
        if dlg.ShowModal() == wx.ID_OK:
            ok = True
            filename = os.path.join(dlg.GetDirectory(), dlg.GetFilename())
    return ok, filename


def show_dialog(win, cls, kwargs=None):
    "show dialog and return if confirmed or rejected"
    if kwargs:
        dlg = cls(win, **kwargs)
    else:
        dlg = cls(win)
    with dlg:
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            dlg.accept()
    return ok == wx.ID_OK


def show_nonmodal(win, cls):
    "show dialog and return to ongoing business"


def get_hotkeys_from_text(label):
    """if menu text contains accelerator, retrieve keys part, strip off brackets and split on comma
    """
    text = label.split('\n')
    hotkeys = []
    if len(text) == 2:
        keys = text[1][1:-1].split(', ')
        for item in keys:
            test = item.split('+')
            key = test[-1]
            mods = []
            if len(test) > 1:
                mods = test[:-1]
            key = {'F1': wx.WXK_F1,
                   'F2': wx.WXK_F2,
                   'Insert': wx.WXK_INSERT,
                   'Del': wx.WXK_DELETE,
                   'PgDn': wx.WXK_PAGEDOWN,
                   'PgUp': wx.WXK_PAGEUP,
                   'Esc': wx.WXK_ESCAPE}.get(ord(key))
            for ix, mod in enumerate(mods):
                mods[ix] = {'Ctrl': wx.MOD_CONTROL,
                            'Shift': wx.MOD_SHIFT}.get()
        hotkeys.append(mods, key)
    return hotkeys


class CheckDialog(wx.Dialog):
    """Dialoog om te melden dat de applicatie verborgen gaat worden

    AskBeforeHide bepaalt of deze getoond wordt of niet
    """
    def __init__(self, parent, message="", option=""):
        self.parent = parent
        self.option = option
        super().__init__(parent, title="DocTree", size=(-1, 120), pos=wx.DefaultPosition,
                         style=wx.DEFAULT_DIALOG_STYLE)
        pnl = wx.Panel(self, -1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(wx.StaticText(pnl, label=message), 1, wx.ALL, 5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.check_box = wx.CheckBox(pnl, -1, "Deze melding niet meer laten zien")
        sizer1.Add(self.check_box, 0, wx.EXPAND)
        sizer0.Add(sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(pnl, id=wx.ID_OK)
        ## self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        sizer1.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()

    def accept(self):
        "dialoog afsluiten"
        self.parent.master.opts[self.option] = not self.check_box.GetValue()


class OptionsDialog(wx.Dialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, parent, id):
        self.parent = parent
        sett2text = shared.get_setttexts(self.parent.master.opts)
        super().__init__(parent, id, title='A Propos Settings')
        pnl = self  # wx.Panel(self, -1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.FlexGridSizer(cols=2)
        self.controls = []
        for key, value in self.parent.master.opts.items():
            if key not in sett2text:
                continue
            sizer1.Add(wx.StaticText(pnl, -1, sett2text[key]), 1, wx.ALL, 5)
            chk = wx.CheckBox(self, -1, '')
            chk.SetValue(value)
            sizer1.Add(chk, 1, wx.ALL, 5)
            self.controls.append((key, chk))
        sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(pnl, id=wx.ID_APPLY)
        sizer1.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.SetAffirmativeId(wx.ID_APPLY)
        btn = wx.Button(pnl, id=wx.ID_CLOSE)
        sizer1.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.SetEscapeId(wx.ID_CLOSE)
        # sizer1 = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()

    def accept(self):
        "dialoog afsluiten"
        for keyvalue, control in self.controls:
            self.parent.master.opts[keyvalue] = control.GetValue()


class SearchDialog(wx.Dialog):
    """search mode: 0 = current document, 1 = all titles, 2 = all texts
    """
    def __init__(self, parent, mode=0):
        pass

    def check_modes(self):
        """
        bij aanzetten current:
            titel en text uitzetten
            lijst en search backwards deactiveren
        bij aanzetten titel of text:
            current uitzetten
            lijst en search backwards activeren
        """

    def accept(self):
        "afsluiten met bijwerken"


class ResultsDialog(wx.Dialog):
    "Present search results in a non-modal dialog"
    def __init__(self, parent):
        pass

    def populate_list(self):
        "zoekresultaten vullen in list"
        def add_item_to_list():
            "item opbouwen"

    def goto_next(self):
        "sync displays voor zoek volgende"

    def goto_selected(self):
        "toon geselecteerd zoekresultaat"

    def goto_and_close(self):
        "toon zoekresultaat en sluit dialoog"

    def accept(self):
        "sluit dialoog"

    def reject(self):
        "sluit dialoog"


class TaskbarIcon(wx.adv.TaskBarIcon):
    "icon in the taskbar"
    id_revive = wx.NewId()
    ## id_close = wx.NewId()

    def __init__(self, parent):
        # super().__init__(wx.adv.TBI_DOCK)
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(parent.app_icon, "Click to revive DocTree")
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, parent.revive)
        self.Bind(wx.EVT_MENU, parent.revive, id=self.id_revive)
        ## self.Bind(wx.EVT_MENU, parent.close, id=self.id_close)

    def CreatePopupMenu(self):
        """reimplemented"""
        menu = wx.Menu()
        menu.Append(self.id_revive, 'Revive Doctree')
        ## menu.Append(self.id_close, 'Close DocTree')
        return menu


class TreePanel(treemix.DragAndDrop, wx.TreeCtrl):
    "Tree structure depicting the notes organization"
    ## def __init__(self, *args, **kwargs):
        ## super(TreePanel, self).__init__(*args, **kwargs)

    def OnDrop(self, dropitem, dragitem):
        """reimplemented from treemix.DragAndDrop

        wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        """
        if dropitem == self.GetRootItem():
            return
        if dropitem is None:
            dropitem = self.root
        ## dragtext = self.GetItemText(dragitem)  # alleen gebruikt in print statement?
        ## dragdata = self.GetItemData(dragitem)  # niet gebruikt?
        dragtree = shared.getsubtree(self, dragitem)
        ## pprint.pprint(dragtree)
        ## droptext = self.GetItemText(dropitem)  # alleen gebruikt in print statement?
        ## dropdata = self.GetItemData(dropitem)  # niet gebruikt?
        self.Delete(dragitem)
        ## item = self.AppendItem(dropitem, dragtext)
        ## self.SetItemData(item, dragdata)
        shared.putsubtree(self, dropitem, *dragtree)
        self.Expand(dropitem)

    def create_popupmenu(self, item):
        "rightclick menu in tree - not implemented yet in this version"
        pass

    def add_to_parent(self, itemkey, titel, parent, pos=-1):
        """add item to tree at a given location
        """
        ## log('*** in add_to_parent ***')
        ## log('parent is {}, pos is {}'.format(parent, pos))
        if pos == -1:
            ## log('append new item')
            new = self.AppendItem(parent, titel)
        else:
            ## log('insert before pos {}'.format(pos))
            new = self.InsertItem(parent, pos, titel)
        self.SetItemData(new, itemkey)
        return new

    def getitemdata(self, item):
        "titel + data in de visual tree ophalen"
        return self.GetItemText(item), self.GetItemData(item)

    def getitemuserdata(self, item):
        "data in de visual tree ophalen"
        return self.GetItemData(item)

    def getitemtitle(self, item):
        "alleen titel in de visual tree ophalen"
        return self.GetItemText(item)

    def getitemkey(self, item):
        "sleutel voor de itemdict ophalen"
        return self.GetItemData(item)

    def setitemtitle(self, item, title):
        "titel (en tooltip instellen)"
        self.SetItemText(item, title)

    def setitemtext(self, item, text):
        """Meant to set the text for the root item (goes in same place as the keys
        for the other items)
        """
        self.SetItemData(item, text)

    def getitemkids(self, item):
        "children van item ophalen"
        tag, cookie = self.GetFirstChild(item)
        children = []
        while tag.IsOk():
            children.append(tag)
            tag, cookie = self.GetNextChild(item, cookie)
        return children

    def getitemparentpos(self, item):
        "parent en positie van item onder parent bepalen"
        shared.log('*** in wx.tree.getitemparentpos ***')
        shared.log('item is {} {}'.format(item, self.getitemtitle(item)))
        try:
            root = self.GetItemParent(item)
        except TypeError:   # geen item meegegeven - mag dat eigenlijk wel?
            root = item
            pos = -1
        else:
            pos = 0
            tag, cookie = self.GetFirstChild(root)
            if tag:
                shared.log('start at tag {} {}'.format(tag, self.getitemtitle(tag)))
            while tag != item and tag.IsOk():
                pos += 1
                tag, cookie = self.GetNextChild(root, cookie)
                shared.log('next ok tag is {} {}'.format(tag, self.getitemtitle(tag)))
        return root, pos

    def getselecteditem(self):
        "return first selected item"
        return self.GetSelection()

    def set_item_expanded(self, item):
        "expand a tree item"
        self.Expand(item)

    def set_item_collapsed(self, item):
        "collapse a tree item"
        self.Collapse(item)

    def set_item_selected(self, item):
        "select a tree item"
        self.SelectItem(item)

    def get_selected_item(self):
        "return the selected tree item"
        return self.GetSelection()

    def removeitem(self, item, cut_from_itemdict):
        "removes current treeitem and returns the previous one"
        parent, pos = self.getitemparentpos(item)
        oldloc = parent, pos
        prev = self.GetPrevSibling(item)
        if not prev.IsOk():
            prev = parent
            if prev == self.root:
                prev = self.GetNextSibling(item)
        self.parent.parent.popitems(item, cut_from_itemdict)
        self.Delete(item)
        return oldloc, prev

    def getsubtree(self, item, itemlist=None):
        "return part of the tree structure"
        shared.getsubtree(self, item, itemlist)

    def putsubtree(self, parent, titel, key, subtree=None, pos=-1):
        "build a new part of the tree"
        shared.putsubtree(self, parent, titel, key, subtree, pos)


class EditorPanel(rt.RichTextCtrl):
    "Rich text editor displaying the selected note"
    def __init__(self, parent, _id):
        rt.RichTextCtrl.__init__(self, parent, _id,  # size=(400,200),
                                 style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)
        self.textAttr = rt.RichTextAttr()

    def on_url(self, evt):
        "dummy handler for clicking on a url"
        wx.MessageBox(evt.GetString(), "URL Clicked")

    def set_contents(self, data):
        "load contents into editor"
        shared.log("*** in set_contents: ***")
        shared.log(data)
        self.Clear()
        data = str(data)
        self.SetValue(data)
        # if data.startswith("<?xml"):
        #     # out = io.StringIO()              -- out moet een OutputStream subclass zijn?
        #     #                                     bv StringOutputStream maar die zijn er nog niet?
        #     # out = io.BytesIO()
        #     handler = rt.RichTextXMLHandler()
        #     _buffer = self.GetBuffer()
        #     _buffer.AddHandler(handler)
        #     with tempfile.NamedTemporaryFile(mode='w+') as out:
        #         out.write(data)
        #         # out.seek(0)
        #         handler.LoadFile(_buffer, out.name)
        #     # out.write(data)
        #     # out.seek(0)
        #     # handler.LoadFile(_buffer, out)
        #     # handler.ImportXML(_buffer, data)
        # else:
        #     self.SetValue(data)  # WriteText(data)
        self.Refresh()

    def get_contents(self):
        "return contents from editor"
        content = self.GetValue()
        # # out = io.StringIO()                  -- out moet een OutputStream subclass zijn?
        # #                                         bv StringOutputStream maar die zijn er nog niet?
        # # out = io.BytesIO()
        # handler = rt.RichTextXMLHandler()
        # _buffer = self.GetBuffer()
        # # print(type(_buffer), type(out))
        # with tempfile.NamedTemporaryFile(mode='w+') as out:
        #     handler.SaveFile(_buffer, out.name)
        #     # handler.ExportXML(_buffer, content)
        #     # # of moet dit zijn ok = _buffer.SaveFile(_out) ?
        #     # out.seek(0)
        #     content = out.read()
        # # handler.SaveFile(_buffer, out)
        # # out.seek(0)
        # # content = out.read()
        shared.log("*** in get_contents: ***")
        shared.log(content)
        return content

    def get_text_position(self):
        """return where the cursor is positioned in the text
        """
        return self.GetInsertionPoint()

    def set_text_position(self, pos):
        """set where the cursor should appear in the text
        """
        self.SetInsertionPoint(pos)
        self.ScrollIntoView(pos, 0)

    def undo(self, evt):
        "relay undo action"
        self.Undo()

    def redo(self, evt):
        "relay redo action"
        self.Redo()

    def cut(self, evt):
        "relay cut action"
        self.Cut()

    def copy(self, evt):
        "relay copy action"
        self.Copy()

    def paste(self, evt):
        "relay paste action"
        self.Paste()

    def select_all(self):
        "select complete text"
        self.SelectAll()

    def clear(self):
        "empty the editor's contents"
        self.Clear()

    def text_bold(self, evt):
        "selectie vet maken"
        self.ApplyBoldToSelection()

    def text_italic(self, evt):
        "selectie schuin schrijven"
        self.ApplyItalicToSelection()

    def text_underline(self, evt):
        "selectie onderstrepen"
        self.ApplyUnderlineToSelection()

    def text_strikethrough(self, evt):
        "selectie onderstrepen"
        # self.ApplyUnderlineToSelection() - as yet unclear how to implement

    def align_left(self, evt):
        "alinea links uitlijnen"
        self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)

    def align_center(self, evt):
        "alinea centreren"
        self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)

    def align_right(self, evt):
        "alinea rechts uitlijnen"
        self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)

    def text_justify(self, evt):  # TODO
        "alinea uitvullen"
        return  # self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)

    def indent_more(self, evt):
        "alinea verder laten inspringen"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.SetStyle(range, attr)

    def indent_less(self, evt):
        "alinea minder ver laten inspringen"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
        if attr.GetLeftIndent() >= 100:
            attr.SetLeftIndent(attr.GetLeftIndent() - 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.SetStyle(range, attr)

    def increase_parspacing_more(self, evt):
        "ruimte tussen alinea's vergroten"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + 20)
            attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
            self.SetStyle(range, attr)

    def decrease_parspacing_less(self, evt):
        "ruimte tussen alinea's verkleinen"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            if attr.GetParagraphSpacingAfter() >= 20:
                attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() - 20)
                attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
                self.SetStyle(range, attr)

    def set_linespacing_10(self, evt):
        "enkele regelafstand instellen"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(10)
            self.SetStyle(range, attr)

    def set_linespacing_15(self, evt):
        "halve regelafstand instellen"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                r = self.GetSelectionRange()
            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(15)
            self.SetStyle(r, attr)

    def set_linespacing_20(self, evt):
        "dubbele regelafstand instellen"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(20)
            self.SetStyle(range, attr)

    def text_font(self, evt):
        "lettertype en/of grootte instellen"
        if not self.HasSelection():
            return

        range = self.GetSelectionRange()
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_FONT)
        if self.GetStyle(self.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())

        with wx.FontDialog(self, fontData) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                fontData = dlg.GetFontData()
                font = fontData.GetChosenFont()
                if font:
                    attr.SetFlags(wx.TEXT_ATTR_FONT)
                    attr.SetFont(font)
                    self.SetStyle(range, attr)
        ## dlg.Destroy()

    def enlarge_text(self, evt):
        "letters groter maken"  # TODO

    def shrink_text(self, evt):
        "letters kleiner maken"  # TODO

    def text_color(self, evt):
        "tekstkleur instellen"
        colourData = wx.ColourData()
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
        if self.GetStyle(self.GetInsertionPoint(), attr):
            colourData.SetColour(attr.GetTextColour())

        with wx.ColourDialog(self, colourData) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                colourData = dlg.GetColourData()
                colour = colourData.GetColour()
                if colour:
                    if not self.HasSelection():
                        self.BeginTextColour(colour)
                    else:
                        range = self.GetSelectionRange()
                        attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
                        attr.SetTextColour(colour)
                        self.SetStyle(range, attr)
        ## dlg.Destroy()

    def background_color(self, evt):
        "achtergrondkleur voor tekst instellen"  # TODO

    def update_bold(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionBold())

    def update_italic(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionItalics())

    def update_underline(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionUnderlined())

    def update_alignleft(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))

    def update_center(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionAligned(wx.TEXT_ALIGNMENT_CENTRE))

    def update_alignright(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionAligned(wx.TEXT_ALIGNMENT_RIGHT))

    def check_dirty(self):
        "mixin exit to check for modifications"
        return self.IsModified()

    def mark_dirty(self, value):
        "mixin exit to manually turn modified flag on/off (mainly intended for off)"
        self.SetModified(not value)

    def openup(self, value):
        "mixin exit to make text accessible (or not)"
        self.Enable(value)

    def search_from_start(self):
        "start search in textarea"
        # move cursor to start of text
        # find first position of text and ensure it is visible

    def find_next(self):
        "search forward in textarea"

    def find_prev(self):
        "search backwards in textarea"


class MainGui(wx.Frame):
    "Primary application window (main screen)"
    def __init__(self, master, title):
        self.master = master
        self.title = title
        self.app = wx.App()
        super().__init__(parent=None, title=title, size=self.master.opts['ScreenSize'],
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

    def setup_screen(self):
        "continue after we have a reference to the class"
        self.app_icon = wx.Icon(os.path.join(shared.HERE, "doctree.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.app_icon)
        self.statbar = self.CreateStatusBar()

        tbar = wx.ToolBar(self, -1)
        self.SetToolBar(tbar)  # - is blijkbaar niet nodig
        menuBar = wx.MenuBar()
        self.SetMenuBar(menuBar)

        ## self.splitter = wx.Frame(self)
        self.splitter = wx.SplitterWindow(self, -1)  # , style = wx.NO_3D) # |wx.SP_3D
        self.splitter.SetMinimumPaneSize(1)

        self.tree = TreePanel(self.splitter, -1, style=wx.TR_HAS_BUTTONS)
        self.root = self.tree.AddRoot("MyNotes")
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.tree.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.editor = EditorPanel(self.splitter, -1)
        self.editor.Enable(False)
        self.editor.new_content = True
        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.create_menu(menuBar, self.master.get_menu_data())
        self.create_stylestoolbar(tbar)  # frm)

        self.splitter.SplitVertically(self.tree, self.editor)
        self.splitter.SetSashPosition(self.master.opts['SashPosition'], True)
        ## ## self.splitter.Bind(wx.EVT_KEY_DOWN, self.on_key)
        ## ## self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_CLOSE, self.afsl)

        vbox = wx.BoxSizer(wx.VERTICAL)
        ## hbox = wx.BoxSizer(wx.HORIZONTAL)
        ## hbox.Add(self.splitter, 1, wx.EXPAND)
        vbox.Add(self.splitter, 1, wx.EXPAND)
        ## vbox.Add(hbox, 1, wx.EXPAND)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        ## vbox.SetSizeHints(self)
        self.SetSize(self.master.opts['ScreenSize'])
        self.in_editor = False
        self.Layout()
        ## self.tree.SetFocus()
        self.Show(True)

        self.srchtext = ''
        self.srchtype = 0
        self.srchflags = []
        self.srchlist = self.srchwrap = False

    def create_menu(self, menubar, menudata):
        """bouw het menu en de meeste toolbars op"""
        self.keydef_to_method = {}
        for item, data in menudata:
            menu_label = item
            submenu = wx.Menu()
            # if item == "&View":
            if item == menudata[2][0]:  # "&View":
                self.viewmenu = submenu
            elif item == menudata[1][0]:
                self.notemenu = submenu
            elif item == menudata[3][0]:
                self.treemenu = submenu
            for menudef in data:
                label = ''
                if not menudef:
                    submenu.AppendSeparator()
                    continue
                label, handler, shortcut, icon, info = menudef
                # icon is mede bedoeld om van hieruit de toolbar op te zetten
                if info.startswith("Check"):
                    menu_item = wx.MenuItem(submenu, -1, label, info)  # , wx.ITEM_CHECK)
                else:
                    menu_item = wx.MenuItem(submenu, -1, label, info)
                if item == menudata[3][0]:
                    if label == '&Undo':
                        self.undo_item = menu_item
                    elif label == '&Redo':
                        self.redo_item = menu_item
                self.Bind(wx.EVT_MENU, handler, menu_item)
                if icon:
                    menu_item.SetBitmap(wx.Bitmap(os.path.join(shared.HERE, icon),
                                                  wx.BITMAP_TYPE_PNG))
                submenu.Append(menu_item)
                # TODO afwijkende callback / update_ui regelen voor:
                # edit -> undo, redo, cut, copy, paste, select_all - allemaal 2x self.forward_event
                # format - bold, italic, underline: self.editor_text_xx, self.editor_update_xx
                # format - left, center, right: self.editor.align_xx, self.editor_update_xx
                # if updateUI is not None:
                #     self.Bind(wx.EVT_UPDATE_UI, updateUI, menu_item)
            menubar.Append(submenu, menu_label)

    def create_stylestoolbar(self, tbar):
        "build toolbar with buttons to change styles"
        # in de qt versie zijn de meeste van deze al tijdens het opzetten van het menu
        # aan de toolbar gekoppeld
        for action in ((wx.ID_CUT, "edit-cut.png", "Cut", None, None),
                       (wx.ID_COPY, "edit-copy.png", "Copy", None, None),
                       (wx.ID_PASTE, "edit-paste.png", "Paste", None, None),
                       (),
                       (wx.ID_UNDO, "edit-undo.png", "Undo", None, None),
                       (wx.ID_REDO, "edit-redo.png", "Redo", None, None),
                       (),
                       (-1, "format-text-bold.png", "Bold", self.editor.text_bold,
                        self.editor.update_bold),
                       (-1, "format-text-italic.png", "Italic",
                        self.editor.text_italic, self.editor.update_italic),
                       (-1, "format-text-underline.png", "Underline",
                        self.editor.text_underline, self.editor.update_underline),
                       (-1, "format-justify-left.png", "Align Left",
                        self.editor.align_left, self.editor.update_alignleft),
                       (-1, "format-justify-center.png", "Center",
                        self.editor.align_center, self.editor.update_center),
                       (-1, "format-justify-right.png", "Align Right",
                        self.editor.align_right, self.editor.update_alignright),
                       (),
                       (-1, "format-indent-less.png", "Indent Less",
                        self.editor.indent_less, None),
                       (-1, "format-indent-more.png", "Indent More",
                        self.editor.indent_more, None),
                       (),
                       (-1, "gnome-settings-font.png", "Font",
                        self.editor.text_font, None),
                       (-1, "gnome-settings-font.png", "Font Colour",
                        self.editor.text_color, None)):
            if not action:
                tbar.AddSeparator()
                continue
            actionid, iconame, shorthelp, handler, update_ui = action
            tooltype = wx.ITEM_NORMAL
            if handler is None:
                handler = update_ui = self.forward_event
            elif update_ui is not None:
                tooltype = wx.ITEM_CHECK
            bmp = wx.Bitmap(os.path.join(shared.HERE, "icons", iconame), type=wx.BITMAP_TYPE_PNG)
            label = os.path.splitext(os.path.basename(iconame))[0]
            item = tbar.AddTool(actionid, label, bmp, shortHelp=shorthelp, kind=tooltype)

            self.Bind(wx.EVT_TOOL, handler, item)
            if update_ui is not None:
                self.Bind(wx.EVT_UPDATE_UI, update_ui, item)

        tbar.Realize()

    def show_statusmessage(self, text):
        "show a message in the status bar"
        self.statbar.SetStatusText(text)

    def set_version(self):
        "GUI type instellen"
        self.master.opts["Version"] = "Wx"

    def set_window_dimensions(self, x, y):
        "venstergrootte instellen"
        self.SetSize(x, y)
        # self.SetSize(self.opts["ScreenSize"])

    def get_screensize(self):
        "return the window's dimensions"
        return tuple(self.GetSize())

    def set_windowtitle(self, title):
        """standaard titel instellen"""
        self.SetTitle(title)

    def set_window_split(self, pos):
        "split positie instellen"
        self.splitter.SetSashPosition(self.master.opts["SashPosition"], True)

    def get_splitterpos(self):
        "return the position at which the screen is split"
        return self.splitter.GetSashPosition()

    def init_app(self):
        "undo stack leegmaken"
        # self.undo_stack.clear()

    def set_focus_to_tree(self):
        "schakel over naar tree"
        self.tree.SetFocus()
        self.in_editor = False

    def set_focus_to_editor(self):
        "set focus to the editor panel"
        self.editor.SetFocus()
        self.in_editor = True

    def go(self):
        "start the application's event loop"
        self.app.MainLoop()

    def hide_me(self):
        """applicatie verbergen"""
        ## self.tbi = wx.adv.TaskBarIcon()
        self.tbi = TaskbarIcon(self)
        ## self.tbi.SetIcon(self.app_icon, "Click to revive DocTree")
        ## wx.adv.EVT_TASKBAR_LEFT_UP(self.tbi, self.revive)
        ## wx.adv.EVT_TASKBAR_RIGHT_UP(self.tbi, self.revive)
        self.Hide()

    def revive(self, event=None):
        """applicatie weer zichtbaar maken"""
        self.Show()
        self.tbi.Destroy()

    def close(self, event=None):
        """quit application from menu"""
        self.Close()

    def afsl(self, event=None):
        """applicatie afsluiten"""
        if not self.master.save_needed(meld=False):
            return
        self.master.cleanup_files()
        if event:
            event.Skip()

    def expand_root(self):
        "expandeer het root item"

    def start_add(self, root=None, under=True, new_title='', extra_titles=None):
        """nieuw item toevoegen (default: onder het geselecteerde)
        """
        origpos = -1  # is dit niet te beperkt?
        self.master.do_additem(self, root, under, origpos, new_title, extra_titles)

    def set_next_item(self, any_level=False):
        "for go to next"
        item = self.tree.GetNextSibling(self.master.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        return item.IsOk()

    def set_prev_item(self, any_level=False):
        "for go to previous"
        item = self.tree.GetPrevSibling(self.master.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        return item.IsOk()

    def start_copy(self, cut=False, retain=True, current=None):
        """start copy/cut/delete action

        parameters: cut: remove item from tree (True for cut, delete and move)
                    retain: remember item for pasting (True for cut and copy)
                    current: item to copy
        """
        self.master.do_copyaction(self, cut, retain, current)

    def start_paste(self, before=True, below=False, dest=None):
        """start paste actie
        """
        self.master.do_pasteitem(self, before, below, dest)

    def reorder_items(self, root, recursive=False):
        "(re)order_items"
        self.tree.SortChildren(root)
        if recursive:
            tag, cookie = self.tree.GetFirstChild(root)
            while tag.IsOk():
                if recursive:
                    self._reorder_items(tag, recursive)
                tag, cookie = self.tree.GetNextChild(root, cookie)

    def rebuild_root(self):
        "tree leegmaken en root opnieuw neerzetten"
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemData(root, '')
        self.root = self.tree.AppendItem(root, self.master.project_file.stem)
        self.tree.SetItemText(self.root, self.master.opts["RootTitle"].rstrip())
        self.tree.SetItemData(self.root, self.master.opts["RootData"])
        return self.root

    def clear_viewmenu(self):
        "remove all view actions from viewmenu"
        menuitem_list = [x for x in self.viewmenu.GetMenuItems()]
        for menuitem in menuitem_list[4:]:
            self.viewmenu.Delete(menuitem)

    def add_viewmenu_option(self, optiontext):
        "add view action to viewmenu"
        _id = wx.NewId()
        menu_item = wx.MenuItem(self.viewmenu, _id, optiontext, 'Switch to this view',
                                wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.master.select_view, menu_item)
        self.viewmenu.Append(menu_item)
        return menu_item

    def check_viewmenu_option(self, menu_item=None):
        "check the given view action or determine which one to set"
        if menu_item:
            menu_item.Check()
            return ''
        menu_id = self._event.GetId()
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for menuitem in menuitem_list[7:]:  # was 4
            if menuitem.GetId() == menu_id:
                newview = menuitem.GetItemLabelText()
                menuitem.Check()
            else:
                if menuitem.IsChecked():
                    menuitem.Check(False)
        return newview

    def uncheck_viewmenu_option(self):
        "uncheck the active viewmenu action"
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for idx, menuitem in enumerate(menuitem_list[7:]):  # was 4
            if idx == self.opts["ActiveView"]:
                menuitem.Check(False)

    def add_view_to_menu(self, newname):
        "update menuitem text"
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for idx, menuitem in enumerate(menuitem_list[7:]):  # was 4
            if idx == self.opts["ActiveView"]:
                menuitem.SetItemLabel(newname)

    def check_next_viewmenu_option(self, prev=False):
        "find the currently checked option, uncheck it and check the next/previous one"
        menuitem_list = [x for x in self.viewmenu.actions()][7:]
        if prev:
            menuitem_list.reverse()
        found_item = False
        for menuitem in menuitem_list:
            if menuitem.IsChecked():
                found_item = True
                menuitem.Check(False)
            elif found_item:
                menuitem.Check(True)
                found_item = False
                break
        if found_item:
            menuitem_list[0].Check(True)

    def update_removedview(self, viewname):
        "view menu bijwerken n.a.v. verwijderen view"
        menuitem_list = self.viewmenu.GetMenuItems()
        removed = 0
        item_to_check = None  # menuitem_list[self.opts["ActiveView"] + 4].Check()
        for menuitem in menuitem_list[7:]:
            num, naam = str(menuitem.GetItemLabelText()).split(None, 1)
            if removed:
                menuitem.SetItemLabelText('&{} {}'.format(int(num[1:]) - 1, naam))
                if not item_to_check:
                    item_to_check = menuitem
            if naam == viewname:
                self.viewmenu.Delete(menuitem)
                removed = True
                if self.master.opts['ActiveView'] >= int(num[1:]) - 1:
                    self.master.opts['ActiveView'] -= 1
                break
        if not item_to_check:
            item_to_check = menuitem_list[7]
        return item_to_check

    def tree_undo(self):  # , event=None):
        "start undo action"

    def tree_redo(self):  # , event=None):
        "start redo action"

    def find_needle(self, haystack):
        "search in plain text version of text"

    def goto_searchresult(self, loc, srchtype):
        "position on found data in text"

    def forward_event(self, evt):
        """The RichTextCtrl can handle menu and update events for undo, redo,
        cut, copy, paste, delete, and select all, so just forward the event to it
        """
        ## print('forwarding', evt, 'to editor')
        self.editor.ProcessEvent(evt)

    def on_key(self, event):
        """afhandeling toetscombinaties"""
        skip = True
        keycode = event.GetKeyCode()
        mods = event.GetModifiers()
        win = event.GetEventObject()
        if keycode == wx.WXK_ESCAPE:
            self.close()
        if keycode == wx.WXK_TAB and win == self.editor:
            if self.editor.IsModified():
                key = self.tree.GetItemData(self.activeitem)
                try:
                    titel = self.itemdict[key][0]
                except KeyError:
                    print("on_key (tab): KeyError, waarschijnlijk op root")
                    if key:
                        self.tree.SetItemData(self.root, key)
                else:
                    self.itemdict[key] = (titel, self.editor.get_contents())
            self.tree.SetFocus()
            skip = False
        if event and skip:
            event.Skip()

    def OnSelChanged(self, event=None):
        """zorgen dat het eerder actieve item onthouden wordt, daarna het geselecteerde
        tot nieuw actief item benoemen"""
        x = event.GetItem()
        ## log("onselchanged aangeroepen op '{}'".format(self.tree.GetItemText(x)))
        self.master.check_active()
        self.master.activate_item(x)
        event.Skip()
