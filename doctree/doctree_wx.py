# -*- coding: utf-8 -*-
"""Doctree wxPython specifieke code - currently unmaintained
"""

import os
import datetime as dt
import pathlib
## import io
import tempfile

import wx
import wx.adv
import wx.lib.mixins.treemixin as treemix
import wx.richtext as rt

import doctree.doctree_shared as shared  # was "dts"
HERE = os.path.dirname(__file__)
log = shared.log


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
    def __init__(self, parent, _id, title, size=(-1, 120), pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, _id, title, pos, size, style)
        pnl = wx.Panel(self, -1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(wx.StaticText(pnl, -1, shared.HIDE_TEXT), 1, wx.ALL, 5)
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
        log('*** in wx.tree.getitemparentpos ***')
        log('item is {} {}'.format(item, self.getitemtitle(item)))
        try:
            root = self.GetItemParent(item)
        except TypeError:   # geen item meegegeven - mag dat eigenlijk wel?
            root = item
            pos = -1
        else:
            pos = 0
            tag, cookie = self.GetFirstChild(root)
            if tag:
                log('start at tag {} {}'.format(tag, self.getitemtitle(tag)))
            while tag != item and tag.IsOk():
                pos += 1
                tag, cookie = self.GetNextChild(root, cookie)
                log('next ok tag is {} {}'.format(tag, self.getitemtitle(tag)))
        return root, pos

    def getselecteditem(self):
        "return first selected item"
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
        self.Parent.Parent.popitems(item, cut_from_itemdict)
        self.Delete(item)
        return oldloc, prev


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
        log("*** in set_contents: ***")
        log(data)
        self.Clear()
        data = str(data)
        ## self.SetValue(data)
        if data.startswith("<?xml"):
            ## out = io.StringIO()                  -- out moet een OutputStream subclass zijn?
            ##                                                  bv StringOutputStream maar die zijn er nog niet?
            ## out = io.BytesIO()
            handler = rt.RichTextXMLHandler()
            _buffer = self.GetBuffer()
            _buffer.AddHandler(handler)
            with tempfile.NamedTemporaryFile(mode='w+') as out:
                out.write(data)
                ## out.seek(0)
                handler.LoadFile(_buffer, out.name)
            ## out.write(data)
            ## out.seek(0)
            ## handler.LoadFile(_buffer, out)
            ## handler.ImportXML(_buffer, data)
        else:
            self.SetValue(data)  # WriteText(data)
        self.Refresh()

    def get_contents(self):
        "return contents from editor"
        ## content = self.GetValue()
        ## out = io.StringIO()                  -- out moet een OutputStream subclass zijn?
        ##                                                  bv StringOutputStream maar die zijn er nog niet?
        ## out = io.BytesIO()
        handler = rt.RichTextXMLHandler()
        _buffer = self.GetBuffer()
        ## print(type(_buffer), type(out))
        with tempfile.NamedTemporaryFile(mode='w+') as out:
            handler.SaveFile(_buffer, out.name)
            ## handler.ExportXML(_buffer, content)
            ## # of moet dit zijn ok = _buffer.SaveFile(_out) ?
            ## out.seek(0)
            content = out.read()
        ## handler.SaveFile(_buffer, out)
        ## out.seek(0)
        ## content = out.read()
        log("*** in get_contents: ***")
        log(content)
        return content

    def text_bold(self, evt):
        "selectie vet maken"
        self.ApplyBoldToSelection()

    def text_italic(self, evt):
        "selectie schuin schrijven"
        self.ApplyItalicToSelection()

    def text_underline(self, evt):
        "selectie onderstrepen"
        self.ApplyUnderlineToSelection()

    def align_left(self, evt):
        "alinea links uitlijnen"
        self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)

    def align_center(self, evt):
        "alinea centreren"
        self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)

    def align_right(self, evt):
        "alinea rechts uitlijnen"
        self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)

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

    def paragraphspacing_more(self, evt):
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

    def paragraphspacing_less(self, evt):
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

    def linespacing_single(self, evt):
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

    def linespacing_half(self, evt):
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

    def linespacing_double(self, evt):
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


class MainWindow(wx.Frame, shared.Mixin):
    """Hoofdscherm van de applicatie"""

    def __init__(self, parent, _id, title):
        self.opts = shared.init_opts()
        wx.Frame.__init__(self, parent, _id, title, size=self.opts['ScreenSize'],
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        shared.Mixin.__init__(self)
        self.app_icon = wx.Icon(os.path.join(HERE, "doctree.ico"), wx.BITMAP_TYPE_ICO)
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

        self.create_menu(menuBar, self._get_menu_data())
        self.create_toolbar(tbar) # frm)

        self.splitter.SplitVertically(self.tree, self.editor)
        self.splitter.SetSashPosition(self.opts['SashPosition'], True)
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
        self.SetSize(self.opts['ScreenSize'])
        self.Layout()
        ## self.tree.SetFocus()
        self.Show(True)
        ## print('end of init')

    def _get_menu_data(self):
        """Menu option definitions

        TODO: kijken of ik deze kan vervangen door de versie van de mixin en wat
        daarvoor aangepast moet worden
        """
        return (("&Main", (("Re&Load\tCtrl+R", self.reread, 'Reread notes file'),
                           ("&Open\tCtrl+O", self.open, "Choose and open notes file"),
                           ("&Init\tShift+Ctrl+I", self.new, 'Start a new notes file'),
                           ("&Save\tCtrl+S", self.save, 'Save notes file'),
                           ("Save as\tShift+Ctrl+S", self.saveas, 'Name and save notes file'),
                           ("", None, None),
                           ("&Root title\tShift+F2", self.rename_root, 'Rename root'),
                           ("Items sorteren", self.order_top, 'Bovenste niveau sorteren op titel'),
                           ("Items recursief sorteren", self.order_all, 'Alle niveaus sorteren op '
                            'titel'),
                           ("", None, None),
                           ("&Hide\tCtrl+H", self.hide_me, 'verbergen in system tray'),
                           ("", None, None),
                           ("e&Xit\tCtrl+Q", self.close, 'Exit program'), ), ),
                ("&Note", (("&New\tCtrl+N", self.add_item, 'Add note (below current level)'),
                           ("&Add\tShift+Ctrl+N", self.insert_item, 'Add note (after current)'),
                           ("&Delete\tCtrl+D", self.delete_item, 'Remove note'),
                           ("", None, None),
                           ("Note &Title\tF2", self.rename_item, 'Rename current note'),
                           ("Subitems sorteren", self.order_this, 'Onderliggend niveau sorteren '
                            'op titel'),
                           ("Subitems recursief sorteren", self.order_lower, "Alle onderliggende "
                            "niveaus sorteren op titel"),
                           ("", None, None),
                           ("&Forward\tCtrl+PageDown", self.next_note, 'View next note'),
                           ("&Back\tCtrl+PageUp", self.prev_note, 'View previous note'), ), ),
                ("&View", (('&New View', self.add_view, 'Add an alternative view (tree) to this data'),
                           ('&Rename Current View', self.rename_view, 'Rename the current tree view'),
                           ('&Delete Current View', self.remove_view, 'Remove the current tree view'),
                           ("", None, None), ), ),
                ('&Edit', (("&Undo\tCtrl+Z", self.forward_event, self.forward_event, wx.ID_UNDO, "",
                            None),
                           ("&Redo\tCtrl+Y", self.forward_event, self.forward_event, wx.ID_REDO, "",
                            None),
                           ("", None, None),
                           ("Cu&t\tCtrl+X", self.forward_event, self.forward_event, wx.ID_CUT, "",
                            None),
                           ("&Copy\tCtrl+C", self.forward_event, self.forward_event, wx.ID_COPY, "",
                            None),
                           ("&Paste\tCtrl+V", self.forward_event, self.forward_event, wx.ID_PASTE,
                            "", None),
                           ## ("&Delete\tDel", self.forward_event, self.forward_event, wx.ID_CLEAR, "",
                            ## None),
                           ("", None, None),
                           ("Select A&ll\tCtrl+A", self.forward_event, self.forward_event,
                            wx.ID_SELECTALL, "", None), ), ),
                ('&Format', (("&Bold\tCtrl+B", self.editor.text_bold, self.editor.update_bold, -1,
                              "", wx.ITEM_CHECK),
                             ("&Italic\tCtrl+I", self.editor.text_italic, self.editor.update_italic,
                              -1, "", wx.ITEM_CHECK),
                             ("&Underline\tCtrl+U", self.editor.text_underline,
                              self.editor.update_underline, -1, "", wx.ITEM_CHECK),
                             ("", None, None),
                             ("L&eft Align", self.editor.align_left, self.editor.update_alignleft,
                              -1, "", wx.ITEM_CHECK),
                             ("&Center", self.editor.align_center, self.editor.update_center, -1,
                              "", wx.ITEM_CHECK),
                             ("&Right Align", self.editor.align_right, self.editor.update_alignright,
                              -1, "", wx.ITEM_CHECK),
                             ("", None, None),
                             ("Indent &More", self.editor.indent_more, 'Increase indentation'),
                             ("Indent &Less", self.editor.indent_less, 'Decrease indentation'),
                             ("", None, None),
                             ("Increase Paragraph &Spacing", self.editor.paragraphspacing_more, ''),
                             ("Decrease &Paragraph Spacing", self.editor.paragraphspacing_less, ''),
                             ("", None, None),
                             ("Normal Line Spacing", self.editor.linespacing_single, ''),
                             ("1.5 Line Spacing", self.editor.linespacing_half, ''),
                             ("Double Line Spacing", self.editor.linespacing_double, ''),
                             ("", None, None),
                             ("&Font...", self.editor.text_font, 'Set/change font'), ), ),
                ("&Help", (("&About", self.info_page, 'About this application'),
                           ("&Keys\tF1", self.help_page, 'Keyboard shortcuts'), ), ), )

    def new(self, event=None, fname=''):
        "set up a new document collection"
        if not shared.Mixin.new(self, fname):
            return
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemData(root, '')
        rootitem = self.tree.AppendItem(root,
                                        os.path.splitext(os.path.basename(self.project_file))[0])
        self.activeitem = self.root = rootitem
        self.tree.SetItemBold(rootitem, True)
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for menuitem in menuitem_list[4:]:
            self.viewmenu.Delete(menuitem)
        _id = wx.NewId()
        menu_item = wx.MenuItem(self.viewmenu, _id, '&Default', 'Switch to this view',
                                wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.select_view, menu_item)
        self.viewmenu.Append(menu_item)
        menu_item.Check()
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.SetItemText(self.root, self.opts["RootTitle"].rstrip())
        self.tree.SetItemData(self.root, self.opts["RootData"])
        self.editor.set_contents(self.opts["RootData"])
        self.editor.Enable(True)
        self.tree.SetFocus()

    def open(self, evt=None):
        "swallow event parameter"
        shared.Mixin.open(self)

    def reread(self, evt=None):
        "swallow event parameter"
        shared.Mixin.reread(self)

    def save(self, evt=None, meld=False):
        "swallow event parameter"
        shared.Mixin.save(self, meld=meld)

    def saveas(self, evt=None):
        "swallow event parameter"
        shared.Mixin.saveas(self)

    def rename_root(self, evt=None):
        "swallow event parameter"
        shared.Mixin.rename_root(self)

    def hide_me(self, event=None):
        """applicatie verbergen"""
        if self.opts["AskBeforeHide"]:
            dlg = CheckDialog(self, -1, 'DocTree')
            dlg.ShowModal()
            if dlg.check_box.GetValue():
                self.opts["AskBeforeHide"] = False
            dlg.Destroy()
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
        if not self.save_needed(meld=False):
            return
        if event:
            event.Skip()

    def add_item(self, evt=None):
        "swallow event parameter"
        shared.Mixin.add_item(self)

    def root_item(self, evt=None):
        "FIXME: to be implemented"

    def insert_item(self, evt=None):
        "swallow event parameter"
        shared.Mixin.insert_item(self)

    def cut_item(self, evt=None):
        "FIXME: to be implemented"

    def delete_item(self, evt=None):
        "swallow event parameter"
        shared.Mixin.delete_item(self)

    def copy_item(self, evt=None):
        "FIXME: to be implemented"

    def paste_item(self, evt=None):
        "FIXME: to be implemented"

    def paste_item_after(self, evt=None):
        "FIXME: to be implemented"

    def paste_item_below(self, evt=None):
        "FIXME: to be implemented"

    def rename_item(self, evt=None):
        "swallow event parameter"
        shared.Mixin.rename_item(self)

    def move_to_file(self, evt=None):
        "FIXME: to be implemented"

    def order_top(self, evt=None):
        "swallow event parameter"
        shared.Mixin.order_top(self)

    def order_all(self, evt=None):
        "swallow event parameter"
        shared.Mixin.order_all(self)

    def order_this(self, evt=None):
        "swallow event parameter"
        shared.Mixin.order_this(self)

    def order_lower(self, evt=None):
        "swallow event parameter"
        shared.Mixin.order_lower(self)

    def next_note(self, evt=None):
        "swallow event parameter"
        shared.Mixin.next_note(self)

    def prev_note(self, evt=None):
        "swallow event parameter"
        shared.Mixin.prev_note(self)

    def next_note_any(self, evt=None):
        "swallow event parameter"
        shared.Mixin.next_note_any(self)

    def prev_note_any(self, evt=None):
        "swallow event parameter"
        shared.Mixin.prev_note_any(self)

    def add_view(self, evt=None):
        "swallow event parameter"
        shared.Mixin.add_view(self)

    def rename_view(self, evt=None):
        "swallow event parameter"
        shared.Mixin.rename_view(self)

    def remove_view(self, evt=None):
        "swallow event parameter"
        shared.Mixin.remove_view(self)

    def next_view(self, evt=None, prev=False):
        "swallow event parameter"
        if self.viewcount == 1:
            self.show_message("This is the only view", 'Doctree')
            return
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.editor.clear()            # GUI specific?
        menuitem_list = [x for x in self.viewmenu.actions()][7:]
        if prev:
            menuitem_list.reverse()
        found_item = False
        for menuitem in menuitem_list:
            if menuitem.isChecked():            # GUI specific
                found_item = True
                menuitem.setChecked(False)            # GUI specific
            elif found_item:
                menuitem.setChecked(True)            # GUI specific
                found_item = False
                break
        if found_item:
            menuitem_list[0].setChecked(True)            # GUI specific
        if prev:
            self.opts["ActiveView"] -= 1
            if self.opts["ActiveView"] < 0:
                self.opts["ActiveView"] = len(self.opts["ViewNames"]) - 1
        else:
            self.opts["ActiveView"] += 1
            if self.opts["ActiveView"] >= len(self.opts["ViewNames"]):
                self.opts["ActiveView"] = 0
        ## self.root = self.tree.takeTopLevelItem(0)            # GUI specific
        ## self.root = qtw.QTreeWidgetItem()            # GUI specific
        ## self.root.setText(0, self.opts["RootTitle"])            # GUI specific
        ## self.root.setText(1, self.opts["RootData"])            # GUI specific
        ## self.tree.addTopLevelItem(self.root)
        self.activeitem = self.root
        tree_item = self.viewtotree()
        self.set_windowtitle()
        self.tree.SelectItem(tree_item)

    def prev_view(self, evt=None):
        "swallow event parameter"
        shared.Mixin.prev_view(self)

    def tree_undo(self):
        "FIXME: to be implemented"

    def tree_redo(self):
        "FIXME: to be implemented"

    def expand_item(self):
        "FIXME: to be implemented"

    def collapse_item(self):
        "FIXME: to be implemented"

    def expand_all(self):
        "FIXME: to be implemented"

    def collapse_all(self):
        "FIXME: to be implemented"


    def info_page(self, evt=None):
        "swallow event parameter"
        shared.Mixin.info_page(self)

    def help_page(self, evt=None):
        "swallow event parameter"
        shared.Mixin.help_page(self)

    def create_menu(self, menuBar, menudata):
        """bouw het menu op"""
        self.keydef_to_method = {}
        for item, data in menudata:
            menu_label = item
            submenu = wx.Menu()
            if item == "&View":
                self.viewmenu = submenu
            for menudef in data:
                label = ''
                if len(menudef) == 3:
                    label, handler, info = menudef
                    if label != "":
                        menu_item = wx.MenuItem(submenu, -1, label, info)
                        self.Bind(wx.EVT_MENU, handler, menu_item)
                        submenu.Append(menu_item)
                    else:
                        submenu.AppendSeparator()
                elif len(menudef) == 6:
                    label, handler, updateUI, _id, info, _type = menudef
                    if label != "":
                        if _type is None:
                            menu_item = wx.MenuItem(submenu, _id, label, info)
                        else:
                            menu_item = wx.MenuItem(submenu, _id, label, info, _type)
                        self.Bind(wx.EVT_MENU, handler, menu_item)
                        submenu.Append(menu_item)
                        if updateUI is not None:
                            self.Bind(wx.EVT_UPDATE_UI, updateUI, menu_item)
            menuBar.Append(submenu, menu_label)

    def create_toolbar(self, tbar):  # , parent)
        "bouw de toolbar op"
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
            bmp = wx.Bitmap(os.path.join(HERE, "icons", iconame), type=wx.BITMAP_TYPE_PNG)
            label = os.path.splitext(os.path.basename(iconame))[0]
            item = tbar.AddTool(actionid, label, bmp, shortHelp=shorthelp, kind=tooltype)

            self.Bind(wx.EVT_TOOL, handler, item)
            if update_ui is not None:
                self.Bind(wx.EVT_UPDATE_UI, update_ui, item)

        print('realizing toolbar')
        tbar.Realize()
        print('toolbar realized')

    def getfilename(self, title, start, save=False):
        "routine for selection of filename"
        filter = "Pickle files (*.pck)|*.pck"
        start = os.path.dirname(start)
        if save:
            dlg = wx.FileDialog(self, title, start, '', filter, wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        else:
            dlg = wx.FileDialog(self, title, start, '', filter, wx.FD_OPEN)
        ok, filename = False, ''
        if dlg.ShowModal() == wx.ID_OK:
            ok = True
            filename = os.path.join(dlg.GetDirectory(), dlg.GetFilename())
        return ok, filename

    def show_message(self, text, title):
        "show a message in a box with a title"
        wx.MessageBox(text, title, parent=self)

    def show_statusmessage(self, text):
        "show a message in the status bar"
        self.statbar.SetStatusText(text)

    def set_windowtitle(self):
        "standaard manier van window titel instellen"
        viewn = self.opts["ViewNames"][self.opts['ActiveView']]
        self.SetTitle("DocTree - {} (view: {})".format(os.path.basename(self.project_file), viewn))

    def save_needed(self, meld=True, always_check=True):
        """vraag of het bestand opgeslagen moet worden als er iets aan de
        verzameling notities is gewijzigd

        eigenlijk bedoeld om te reageren op een indicatie dat er iets aan de
        verzameling notities is gewijzigd (de oorspronkelijke self.project_dirty)
        """
        ## if not dts.Mixin.save_needed(self): # too restrictive
        ## if not self.has_treedata:
            ## print('no tree data: save not applicable')
            ## return True
        ## print(self.project_dirty, self)
        ## if not self.project_dirty:
            ## print('not modified: save not needed')
            ## return False
        save_is_needed = shared.Mixin.save_needed(self)
        need_to_save = self.editor.check_dirty() if always_check else False
        if save_is_needed or need_to_save:
            if self.editor.HasFocus():
                self.check_active()
            with wx.MessageDialog(self, "Data changed - save current file before continuing?",
                                  "DocTree", wx.YES_NO | wx.CANCEL) as dlg:
                h = dlg.ShowModal()
                if h == wx.ID_YES:
                    self.save(meld=meld)
                if h == wx.ID_CANCEL:
                    return False
        ## dlg.Destroy()
        return True

    def ok_to_reload(self):
        "ask for confirmation (specific)"
        dlg = wx.MessageDialog(self, 'OK to reload?', 'DocTree', wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        dlg.Destroy()
        return True if result == wx.ID_OK else False

    def _confirm(self, title, text):
        "ask for confirmation (generic)"
        # "handles Menu > View > Delete current view"
        dlg = wx.MessageDialog(self, text, title, wx.YES_NO)
        hlp = dlg.ShowModal()
        dlg.Destroy()
        return True if hlp == wx.ID_YES else False

    def _read(self):
        """GUI-specifieke zaken binnen Mixin.read()"

        settings dictionary lezen, opgeslagen data omzetten naar tree"""
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemData(root, '')
        self.root = self.tree.AppendItem(root,
                                         os.path.splitext(os.path.basename(self.project_file))[0])
        self.activeitem = self.root   # = item_to_activate
        self.editor.Clear()
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.SetItemText(self.root, self.opts["RootTitle"].rstrip())
        self.tree.SetItemData(self.root, self.opts["RootData"])
        self.editor.set_contents(self.opts["RootData"])
        menuitem_list = [x for x in self.viewmenu.GetMenuItems()]
        for menuitem in menuitem_list[4:]:
            self.viewmenu.Delete(menuitem)
        for idx, name in enumerate(self.opts["ViewNames"]):
            menu_item = wx.MenuItem(self.viewmenu, -1, name, "switch to this view", wx.ITEM_CHECK)
            self.Bind(wx.EVT_MENU, self.select_view, menu_item)
            self.viewmenu.Append(menu_item)
            if idx == self.opts["ActiveView"]:
                menu_item.Check()

    def _finish_read(self, item_to_activate):
        "finalize open action"
        ## print(item_to_activate, self.activeitem)
        self.tree.Expand(self.root)
        if item_to_activate and item_to_activate != self.activeitem:
            self.tree.SelectItem(item_to_activate)
        self.tree.SetFocus()

    def write(self, meld=True):
        "start write action"
        self.opts["ScreenSize"] = tuple(self.GetSize())
        self.opts["SashPosition"] = self.splitter.GetSashPosition()
        shared.Mixin.write(self, meld=meld)

    def _finish_add(self, parent, item):
        "finalize add action"
        self.tree.Expand(parent)
        self.tree.SelectItem(item)
        if item != self.root:
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()

    def _finish_copy(self, prev):
        "finalize copy action"
        self.tree.SelectItem(prev)

    def _finish_paste(self, current):
        "finalize paste action"
        # nog niet geactiveerd in deze versie

    def _finish_rename(self, item, item_to_expand):
        "finalize rename action"
        self.tree.Expand(item_to_expand)
        self.tree.SelectItem(item)

    def _get_name(self, caption, title, oldname):
        "ask for (new) name"
        newname = oldname
        with wx.TextEntryDialog(self, caption, title, oldname) as dlg:
            ok = dlg.ShowModal() == wx.ID_OK
            newname = dlg.GetValue()
        return ok, newname

    def _rebuild_root(self):
        "tree leegmaken en root opnieuw neerzetten"
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemData(root, '')
        self.root = self.tree.AppendItem(root, os.path.splitext(
            os.path.basename(self.project_file))[0])
        self.tree.SetItemText(self.root, self.opts["RootTitle"].rstrip())
        self.tree.SetItemData(self.root, self.opts["RootData"])

    def _set_activeitem_for_view(self):
        "pylint klaagt erover dat deze niet geherimplementeerd is"

    def _update_newview(self, new_view):
        "view menu bijwerken n.a.v. toevoeging nieuwe view"
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for idx, menuitem in enumerate(menuitem_list[4:]):
            if idx == self.opts["ActiveView"]:
                menuitem.Check(False)
        menu_item = wx.MenuItem(self.viewmenu, -1, new_view, "switch to this view", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.select_view, menu_item)
        self.viewmenu.Append(menu_item)
        menu_item.Check()

    def _add_view_to_menu(self, newname):
        "update menuitem text"
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for idx, menuitem in enumerate(menuitem_list[4:]):
            if idx == self.opts["ActiveView"]:
                menuitem.SetItemLabel(newname)

    def _finish_add_view(self, tree_item):
        "handles Menu > View > New view"
        self.tree.SelectItem(tree_item)

    def select_view(self, event):
        """handle menu action and remember trigger event
        """
        self._event = event
        shared.Mixin.select_view(self)

    def _update_selectedview(self):
        "view menu bijwerken n.a.v. wijzigen view naam"
        self.editor.Clear()
        menu_id = self._event.GetId()
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for menuitem in menuitem_list[4:]:
            if menuitem.GetId() == menu_id:
                newview = menuitem.GetItemLabelText()
                menuitem.Check()
            else:
                if menuitem.IsChecked():
                    menuitem.Check(False)
        return newview      # .split(None, 1)[1]

    def _finish_select_view(self, tree_item):
        "finalize select view action"
        self.tree.SelectItem(tree_item)

    def _update_removedview(self, viewname):
        "view menu bijwerken n.a.v. verwijderen view"
        menuitem_list = self.viewmenu.GetMenuItems()
        menuitem_list[self.opts["ActiveView"] + 4].Check()
        for menuitem in menuitem_list:
            if menuitem.GetItemLabelText() == viewname:
                self.viewmenu.Delete(menuitem)
                break
        if self.opts["ActiveView"] == 0:
            menuitem_list[4].Check()

    def _finish_remove_view(self, item):
        "finalize action"
        self.tree.SelectItem(item)

    def _expand(self, recursive=False):
        "expandeer tree vanaf huidige item"
        # nog niet geïmplementeerd?

    def _collapse(self, recursive=False):
        "collapse huidige item en daaronder"
        # nog niet geïmplementeerd?

    def _reorder_items(self, root, recursive=False):
        "(re)order_items"
        self.tree.SortChildren(root)
        if recursive:
            tag, cookie = self.tree.GetFirstChild(root)
            while tag.IsOk():
                if recursive:
                    self._reorder_items(tag, recursive)
                tag, cookie = self.tree.GetNextChild(root, cookie)

    def _set_next_item(self):
        "for go to next"
        item = self.tree.GetNextSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        return item.IsOk()

    def _set_prev_item(self):
        "for go to previous"
        item = self.tree.GetPrevSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        return item.IsOk()


    def forward_event(self, evt):
        """The RichTextCtrl can handle menu and update events for undo, redo,
        cut, copy, paste, delete, and select all, so just forward the event to it
        """
        ## print('forwarding', evt, 'to editor')
        self.editor.ProcessEvent(evt)

    def change_pane(self, event=None):
        "wissel tussen tree en editor - niet geïmplementeerd in deze versie"
        ## if self.tree.hasFocus():
            ## self.editor.setFocus()
        ## elif self.editor.hasFocus():
            ## self.check_active()
            ## self.tree.setFocus()

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
        self.check_active()
        self.activate_item(x)
        event.Skip()


def main(fname=''):
    "entry point"
    app = wx.App()  # redirect=True, filename="doctree_wx.log")
    log(dt.datetime.today().strftime("%d-%m-%Y %H:%M:%S").join(("------------------",
                                                                "------------------")))
    frame = MainWindow(None, -1, "DocTree - " + fname)
    app.SetTopWindow(frame)
    if fname:
        frame.project_file = pathlib.Path(fname).resolve()
        if not os.path.exists(fname):
            mld = fname + ' does not exist, do you want to create it?'
            with wx.MessageDialog(frame, mld, 'DocTree', wx.OK | wx.CANCEL) as dlg:
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    log('in main: {}'.format(fname))
                    frame.new(fname=fname)
                    frame.set_project_dirty(True)
        else:
            err = frame.read()
            if err:
                wx.MessageBox(err, "Error")
    app.MainLoop()


if __name__ == '__main__':
    main('wx_tree.pck')
