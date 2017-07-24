# -*- coding: utf-8 -*-
"""Doctree wxPython specifieke code - currently unmaintained
"""

import os
import datetime as dt
import StringIO as io

import wx
import wx.lib.mixins.treemixin as treemix
import wx.richtext as rt

HERE = os.path.dirname(__file__)
import doctree_shared as dts

class CheckDialog(wx.Dialog):
    """Dialoog om te melden dat de applicatie verborgen gaat worden
    AskBeforeHide bepaalt of deze getoond wordt of niet"""
    def __init__(self, parent, _id, title, size=(-1, 120), pos = wx.DefaultPosition,
            style = wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, _id, title, pos, size, style)
        pnl = wx.Panel(self, -1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(wx.StaticText(pnl, -1, "\n".join((
                "DocTree gaat nu slapen in de System tray",
                "Er komt een icoontje waarop je kunt klikken om hem weer wakker te maken"
                ))), 1, wx.ALL, 5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.check_box = wx.CheckBox(pnl, -1, "Deze melding niet meer laten zien")
        sizer1.Add(self.check_box, 0, wx.EXPAND)
        sizer0.Add(sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(pnl, id = wx.ID_OK)
        ## self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        sizer1.Add(self.ok_button, 0, wx.EXPAND | wx.ALL, 2)
        sizer0.Add(sizer1, 0,
            wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()

class TreePanel(treemix.DragAndDrop, wx.TreeCtrl):
    "Tree structure depicting the notes organization"
    def __init__(self, *args, **kwargs):
        super(TreePanel, self).__init__(*args, **kwargs)

    def OnDrop(self, dropitem, dragitem):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item"""
        if dropitem == self.GetRootItem():
            return
        if dropitem is None:
            dropitem = self.root
        dragText = self.GetItemText(dragitem) # alleen gebruikt in print statement?
        dragData = self.GetItemPyData(dragitem) # niet gebruikt?
        dragtree = getsubtree(self, dragitem)
        ## pprint.pprint(dragtree)
        dropText = self.GetItemText(dropitem) # alleen gebruikt in print statement?
        dropData = self.GetItemPyData(dropitem) # niet gebruikt?
        self.Delete(dragitem)
        ## item = self.AppendItem(dropitem, dragText)
        ## self.SetItemPyData(item, dragData)
        putsubtree(self, dropitem, *dragtree)
        self.Expand(dropitem)
    def create_popupmenu(self, item):
        "rightclick menu in tree - not implemented yet in this version"
        pass

    def add_to_parent(self, itemkey, titel, parent, pos=-1):
        if pos == -1:
            new = self.AppendItem(parent, titel)
        else:
            test = 0
            tag, cookie = self.GetFirstChild(parent)
            while test < pos and tag.IsOk():
                tag, cookie = tree.GetNextChild(parent, cookie)
                pos += 1
            new = self.tree.InsertItem (root, tag, new_title)
        self.SetItemPyData(new, itemkey)

    def _getitemdata(self, item):
        return self.GetItemText(item), self.GetItemPyData(item)

    def _getitemtitle(self, item):
        return self.GetItemText(item)

    def _getitemtext(self, item):
        return self.GetItemPyData(item)

    def _setitemtitle(self, item, title):
        self.SetItemText(item, title)

    def _setitemtext(self, item, text):
        self.SetItemPyData(item, text)

    def _getitemkids(self, item):
        tag, cookie = self.GetFirstChild(item)
        children = []
        while tag.IsOk():
            children.append(tag)
            tag, cookie = self.GetNextChild(item, cookie)
        return children

    def _getitemparentpos(self, item):
        root = self.GetItemParent(item)
        pos = 0
        tag, cookie = self.GetFirstChild(item)
        while tag != item and tag.IsOk():
            pos += 1
            tag, cookie = tree.GetNextChild(item, cookie)
        return root, pos

    def _getselecteditem(self):
        return self.GetSelection()

    def _removeitem(self, item):
        prev = self.tree.GetPrevSibling(item)
        if not prev.IsOk():
            prev = self.tree.GetItemParent(item)
            if prev == self.root:
                prev = self.tree.GetNextSibling(item)
        self._popitems(item, self.cut_from_itemdict)
        self.tree.Delete(item)
        return prev

class EditorPanel(rt.RichTextCtrl):
    "Rich text editor displaying the selected note"
    def __init__(self, parent, _id):
        rt.RichTextCtrl.__init__(self, parent, _id, # size=(400,200),
            style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER)
        self.textAttr = rt.RichTextAttr()

    def on_url(self, evt):
        wx.MessageBox(evt.GetString(), "URL Clicked")

    def set_contents(self, data):
        "load contents into editor"
        self.Clear()
        if data.startswith("<?xml"):
            out = io.StringIO()
            handler = rt.RichTextXMLHandler()
            _buffer = self.GetBuffer()
            _buffer.AddHandler(handler)
            out.write(data)
            out.seek(0)
            handler.LoadStream(_buffer, out)
        else:
            self.WriteText(data)
        self.Refresh()

    def get_contents(self):
        "return contents from editor"
        out = io.StringIO()
        handler = rt.RichTextXMLHandler()
        _buffer = self.GetBuffer()
        handler.SaveStream(_buffer, out)
        out.seek(0)
        content = out.read()
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
        self.ApplyAlignmentToSelection(rt.TEXT_ALIGNMENT_LEFT)

    def align_center(self, evt):
        "alinea centreren"
        self.ApplyAlignmentToSelection(rt.TEXT_ALIGNMENT_CENTRE)

    def align_right(self, evt):
        "alinea rechts uitlijnen"
        self.ApplyAlignmentToSelection(rt.TEXT_ALIGNMENT_RIGHT)

    def indent_more(self, evt):
        "alinea verder laten inspringen"
        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                r = self.GetSelectionRange()
            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
            self.SetStyle(r, attr)

    def indent_less(self, evt):
        "alinea minder ver laten inspringen"
        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                r = self.GetSelectionRange()
        if attr.GetLeftIndent() >= 100:
            attr.SetLeftIndent(attr.GetLeftIndent() - 100)
            attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
            self.SetStyle(r, attr)

    def text_font(self, evt):
        "lettertype en/of grootte instellen"
        if not self.HasSelection():
            return

        r = self.GetSelectionRange()
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_FONT)
        if self.GetStyle(self.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())

        dlg = wx.FontDialog(self, fontData)
        if dlg.ShowModal() == wx.ID_OK:
            fontData = dlg.GetFontData()
            font = fontData.GetChosenFont()
            if font:
                attr.SetFlags(rt.TEXT_ATTR_FONT)
                attr.SetFont(font)
                self.SetStyle(r, attr)
        dlg.Destroy()


    def text_color(self, evt):
        "tekstkleur instellen"
        colourData = wx.ColourData()
        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_TEXT_COLOUR)
        if self.GetStyle(self.GetInsertionPoint(), attr):
            colourData.SetColour(attr.GetTextColour())

        dlg = wx.ColourDialog(self, colourData)
        if dlg.ShowModal() == wx.ID_OK:
            colourData = dlg.GetColourData()
            colour = colourData.GetColour()
            if colour:
                if not self.HasSelection():
                    self.BeginTextColour(colour)
                else:
                    r = self.GetSelectionRange()
                    attr.SetFlags(rt.TEXT_ATTR_TEXT_COLOUR)
                    attr.SetTextColour(colour)
                    self.SetStyle(r, attr)
        dlg.Destroy()

    def paragraphspacing_more(self, evt):
        "ruimte tussen alinea's vergroten"
        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                r = self.GetSelectionRange()
            attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + 20)
            attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
            self.SetStyle(r, attr)

    def paragraphspacing_less(self, evt):
        "ruimte tussen alinea's verkleinen"
        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                r = self.GetSelectionRange()
            if attr.GetParagraphSpacingAfter() >= 20:
                attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() - 20)
                attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
                self.SetStyle(r, attr)


    def linespacing_single(self, evt):
        "enkele regelafstand instellen"
        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                r = self.GetSelectionRange()

            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(10)
            self.SetStyle(r, attr)


    def linespacing_half(self, evt):
        "halve regelafstand instellen"
        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                r = self.GetSelectionRange()

            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(15)
            self.SetStyle(r, attr)


    def linespacing_double(self, evt):
        "dubbele regelafstand instellen"
        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                r = self.GetSelectionRange()

            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(20)
            self.SetStyle(r, attr)


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
        evt.Check(self.IsSelectionAligned(rt.TEXT_ALIGNMENT_LEFT))

    def update_center(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionAligned(rt.TEXT_ALIGNMENT_CENTRE))

    def update_alignright(self, evt):
        "het betreffende menuitem aanvinken indien van toepassing"
        evt.Check(self.IsSelectionAligned(rt.TEXT_ALIGNMENT_RIGHT))
    def _check_dirty(self):
        "mixin exit to check for modifications"
        return self.IsModified()

    def _mark_dirty(self, value):
        "mixin exit to manually turn modified flag on/off (mainly intended for off)"
        self.SetModified(not value)

    def _openup(self, value):
        "mixin exit to make text accessible (or not)"
        self.Enable(value)

class MainWindow(wx.Frame, dts.Mixin):
    """Hoofdscherm van de applicatie"""
    def __init__(self, parent, _id, title):
        self.opts = dts.init_opts()
        wx.Frame.__init__(self, parent, _id, title, size=self.opts['ScreenSize'],
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        dts.Mixin.__init__(self)
        self.nt_icon = wx.Icon(os.path.join(HERE, "doctree.ico"),wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.nt_icon)
        self.statbar = self.CreateStatusBar()

        tbar = wx.ToolBar(self, -1)
        menuBar = wx.MenuBar()
        self.SetMenuBar(menuBar)

        self.splitter = wx.SplitterWindow (self, -1, style = wx.NO_3D) # |wx.SP_3D
        self.splitter.SetMinimumPaneSize (1)

        self.tree = TreePanel(self.splitter, -1, style=wx.TR_HAS_BUTTONS
            | wx.TR_EDIT_LABELS | wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.root = self.tree.AddRoot("MyNotes")
        ## self.activeitem = self.root
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.tree.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.editor = EditorPanel(self.splitter, -1)
        self.editor.Enable(0)
        self.editor.new_content = True
        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.create_menu(menuBar, self._get_menu_data())
        ## self.create_toolbar(tbar) # frm)

        self.splitter.SplitVertically(self.tree, self.editor)
        self.splitter.SetSashPosition(self.opts['SashPosition'], True)
        ## self.splitter.Bind(wx.EVT_KEY_DOWN, self.on_key)
        ## self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_CLOSE, self.afsl)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.splitter, 1, wx.EXPAND )
        vbox.Add(hbox, 1, wx.EXPAND)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        ## self.tree.SetFocus()
        self.Show(True)

    def _get_menu_data(self):
        return (
            ("&Main", (
                ("Re&Load (Ctrl-R)", self.reread, 'Reread notes file'),
                ("&Open (Ctrl-O)", self.open, "Choose and open notes file"),
                ("&Init (Ctrl-I)", self.new, 'Start a new notes file'),
                ("&Save (Ctrl-S)", self.save, 'Save notes file'),
                ("Save as (Shift-Ctrl-S)", self.saveas, 'Name and save notes file'),
                ("", None, None),
                ("&Root title (Shift-F2)", self.rename_root, 'Rename root'),
                ("Items sorteren", self.order_top, 'Bovenste niveau sorteren op titel'),
                ("Items recursief sorteren", self.order_all, 'Alle niveaus sorteren op titel'),
                ("", None, None),
                ("&Hide (Ctrl-H)", self.hide_me, 'verbergen in system tray'),
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
            ('&Edit', (
                ("&Undo\tCtrl+Z", self.forward_event, self.forward_event, wx.ID_UNDO, "", None),
                ("&Redo\tCtrl+Y", self.forward_event, self.forward_event, wx.ID_REDO, "", None),
                ("", None, None),
                ("Cu&t\tCtrl+X", self.forward_event, self.forward_event, wx.ID_CUT, "", None),
                ("&Copy\tCtrl+C", self.forward_event, self.forward_event, wx.ID_COPY, "", None),
                ("&Paste\tCtrl+V", self.forward_event, self.forward_event, wx.ID_PASTE, "", None),
                ("&Delete\tDel", self.forward_event, self.forward_event, wx.ID_CLEAR, "", None),
                ("", None, None),
                ("Select A&ll\tCtrl+A", self.forward_event, self.forward_event, wx.ID_SELECTALL, "", None),
                ), ),
            ('&Format', (
                ("&Bold\tCtrl+B", self.editor.text_bold, self.editor.update_bold, -1, "", wx.ITEM_CHECK),
                ("&Italic\tCtrl+I", self.editor.text_italic, self.editor.update_italic, -1, "", wx.ITEM_CHECK),
                ("&Underline\tCtrl+U", self.editor.text_underline, self.editor.update_underline, -1, "", wx.ITEM_CHECK),
                ("", None, None),
                ("L&eft Align", self.editor.align_left, self.editor.update_alignleft, -1, "", wx.ITEM_CHECK),
                ("&Centre", self.editor.align_center, self.editor.update_center, -1, "", wx.ITEM_CHECK),
                ("&Right Align", self.editor.align_right, self.editor.update_alignright, -1, "", wx.ITEM_CHECK),
                ("", None, None),
                ("Indent &More", self.editor.indent_more, 'Increase indentation'),
                ("Indent &Less", self.editor.indent_less, 'Decrease indentation'),
                ("", None, None),
                ("Increase Paragraph &Spacing", self.editor.paragraphspacing_more, ''),
                ("Decrease &Paragraph Spacing", self.editor.paragraphspacing_less, ''),
                ("", None, None),
                ("Normal Line Spacing", self.editor.linespacing_single, ''),
                ("1.5 Line Spacing", self.editor.linespacing_half,''),
                ("Double Line Spacing", self.editor.linespacing_double, ''),
                ("", None, None),
                ("&Font...", self.editor.text_font, 'Set/change font'),
                ), ),
            ("&Help", (
                ("&About", self.info_page, 'About this application'),
                ("&Keys (F1)", self.help_page, 'Keyboard shortcuts'),
                ), ),
            )

    def forward_event(self, evt):
        # The RichTextCtrl can handle menu and update events for undo,
        # redo, cut, copy, paste, delete, and select all, so just
        # forward the event to it.
        self.editor.ProcessEvent(evt)

    def change_pane(self, event=None):
        "wissel tussen tree en editor - niet geïmplementeerd in deze versie (?)"
        ## if self.tree.hasFocus():
            ## self.editor.setFocus()
        ## elif self.editor.hasFocus():
            ## self.check_active()
            ## self.tree.setFocus()
        pass

    def create_menu(self, menuBar, menudata):
        """bouw het menu op"""
        for item, data in menudata:
            menu_label = item
            submenu = wx.Menu()
            if item == "&View":
                self.viewmenu = submenu
            for menudef in data:
                if len(menudef) == 3:
                    label, handler, info = menudef
                    if label != "":
                        menu_item = wx.MenuItem(submenu, -1, label, info)
                        self.Bind(wx.EVT_MENU, handler, menu_item)
                        submenu.AppendItem(menu_item)
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
                        submenu.AppendItem(menu_item)
                        if updateUI is not None:
                            self.Bind(wx.EVT_UPDATE_UI, updateUI, menu_item)
            menuBar.Append(submenu, menu_label)

    def create_toolbar(self, tbar): # , parent)
        def doBind(item, handler, updateUI=None):
            self.Bind(wx.EVT_TOOL, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)

        doBind(tbar.AddTool(wx.ID_CUT, wx.Icon(os.path.join(
                HERE, "icons", "edit-cut.png"), wx.BITMAP_TYPE_PNG),
                shortHelpString="Cut"), self.forward_event, self.forward_event)
        doBind(tbar.AddTool(wx.ID_COPY, wx.Icon(os.path.join(
                HERE, "icons", "edit-copy.png"), wx.BITMAP_TYPE_PNG),
                shortHelpString="Copy"), self.forward_event, self.forward_event)
        doBind(tbar.AddTool(wx.ID_PASTE, wx.Icon(os.path.join(
                HERE, "icons", "edit-paste.png"), wx.BITMAP_TYPE_PNG),
                shortHelpString="Paste"), self.forward_event, self.forward_event)
        tbar.AddSeparator()
        doBind(tbar.AddTool(wx.ID_UNDO, wx.Icon(os.path.join(
                HERE, "icons", "edit-undo.png"), wx.BITMAP_TYPE_PNG),
                shortHelpString="Undo"), self.forward_event, self.forward_event)
        doBind(tbar.AddTool(wx.ID_REDO, wx.Icon(os.path.join(
                HERE, "icons", "edit-redo.png"), wx.BITMAP_TYPE_PNG),
                shortHelpString="Redo"), self.forward_event, self.forward_event)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, wx.Icon(os.path.join(HERE, "icons",
                "format-text-bold.png"), wx.BITMAP_TYPE_PNG), isToggle=True,
                shortHelpString="Bold"), self.editor.text_bold, self.editor.update_bold)
        doBind(tbar.AddTool(-1, wx.Icon(os.path.join(HERE, "icons",
                "format-text-italic.png"), wx.BITMAP_TYPE_PNG), isToggle=True,
                shortHelpString="Italic"), self.editor.text_italic, self.editor.update_italic)
        doBind(tbar.AddTool(-1, wx.Icon(os.path.join(HERE, "icons",
                "format-text-underline.png"), wx.BITMAP_TYPE_PNG), isToggle=True,
                shortHelpString="Underline"), self.editor.text_underline, self.editor.update_underline)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, wx.Icon(os.path.join(HERE, "icons",
                "format-justify-left.png"), wx.BITMAP_TYPE_PNG), isToggle=True,
                shortHelpString="Align Left"), self.editor.align_left, self.editor.update_alignleft)
        doBind(tbar.AddTool(-1, wx.Icon(os.path.join(HERE, "icons",
                "format-justify-center.png"), wx.BITMAP_TYPE_PNG), isToggle=True,
                shortHelpString="Center"), self.editor.align_center, self.editor.update_center)
        doBind(tbar.AddTool(-1, wx.Icon(os.path.join(HERE, "icons",
                "format-justtify-right.png"), wx.BITMAP_TYPE_PNG), isToggle=True,
                shortHelpString="Align Right"), self.editor.align_right, self.editor.update_alignright)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, wx.Icon(os.path.join(HERE, "icons",
                "format-indent-less.png"), wx.BITMAP_TYPE_PNG),
                shortHelpString="Indent Less"), self.editor.indent_less)
        doBind(tbar.AddTool(-1, wx.Icon(os.path.join(HERE, "icons",
                "formt-indent-more.png"), wx.BITMAP_TYPE_PNG),
                shortHelpString="Indent More"), self.editor.indent_more)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, wx.Icon(os.path.join(
                HERE, "icons", "gnome-settings-font.png"), wx.BITMAP_TYPE_PNG),
                shortHelpString="Font"), self.editor.text_font)
        doBind(tbar.AddTool(-1, wx.Icon(os.path.join(
                HERE, "icons", "gnome-settings-font.png"), wx.BITMAP_TYPE_PNG),
                shortHelpString="Font Colour"), self.editor.text_color)
        tbar.Realize()

    def on_key(self, event):
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
            elif keycode == wx.WXK_PAGEDOWN:
                self.next_note()
            elif keycode == wx.WXK_PAGEUP:
                self.prev_note()
        elif mods == wx.MOD_CONTROL | wx.MOD_SHIFT:
            if keycode == ord("N"):
                self.add_item(root = self.root)
            elif keycode == ord("S"):
                self.saveas()
        elif keycode == wx.WXK_F1:
            self.help_page()
        elif keycode == wx.WXK_F2:
            if mods == wx.MOD_SHIFT:
                self.rename_root()
            else:
                self.rename_item()
        elif keycode == wx.WXK_INSERT and win == self.tree:
            self.insert_item()
        elif keycode == wx.WXK_DELETE:
            print("delete key pressed")
            if win == self.tree:
                print("in tree")
                self.delete_item()
            elif win == self.editor:
                print("in editor")
        elif keycode == wx.WXK_TAB and win == self.editor:
            if self.editor.IsModified():
                key = self.tree.GetItemPyData(self.activeitem)
                try:
                    titel, tekst = self.itemdict[key]
                except KeyError:
                    print("on_key (tab): KeyError, waarschijnlijk op root")
                    if key:
                        self.tree.SetItemPyData(self.root, key)
                else:
                    self.itemdict[key] = (titel, self.editor.get_contents())
            self.tree.SetFocus()
            skip = False
        elif keycode == wx.WXK_ESCAPE:
            self.Close()
        if event and skip:
            event.Skip()

    def OnSelChanged(self, event=None):
        """zorgen dat het eerder actieve item onthouden wordt, daarna het geselecteerde
        tot nieuw actief item benoemen"""
        x = event.GetItem()
        print("onselchanged aangeroepen op '{}'".format(self.tree.GetItemText(x)))
        self.check_active()
        self.activate_item(x)
        event.Skip()

    def show_message(self, text, title):
        wx.MessageBox(text, title, parent=self)

    def show_statusmessage(self, text):
        self.statbar.SetStatusText(text)

    def set_title(self):
        "standaard manier van window titel instellen"
        self.SetTitle("DocTree - {} (view: {})".format(
            os.path.split(self.project_file)[1],
            self.opts["ViewNames"][self.opts['ActiveView']]))

    def getfilename(self, title, start, save=False):
        filter = "Pickle files (*.pck)|*.pck"
        if save:
            dlg = wx.FileDialog(self, title, start, '', filter, wx.SAVE |
                wx.OVERWRITE_PROMPT)
        else:
            dlg = wx.FileDialog(self, title, start, '', filter, wx.OPEN)
        ok, filename = False, ''
        if dlg.ShowModal() == wx.ID_OK:
            ok = True
            filename = os.path.join(dlg.GetDirectory(), dlg.GetFilename())
        return ok, filename

    def new(self, event=None):
        "Afhandelen Menu - Init / Ctrl-I"
        if not dts.Mixin.new(self, event):
            return
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemPyData(root, '')
        rootitem = self.tree.AppendItem(root, os.path.splitext(
            os.path.basename(self.project_file))[0])
        self.activeitem = self.root = rootitem
        self.tree.SetItemBold(rootitem, True)
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for menuitem in menuitem_list[4:]:
            self.viewmenu.DeleteItem(menuitem)
        _id = wx.NewId()
        menu_item = wx.MenuItem(self.viewmenu, _id, '&Default',
            'Switch to this view', wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.select_view, menu_item)
        self.viewmenu.AppendItem(menu_item)
        menu_item.Check()
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.SetItemText(self.root, self.opts["RootTitle"].rstrip())
        self.tree.SetItemPyData(self.root, self.opts["RootData"])
        self.editor.set_contents(self.opts["RootData"])
        self.editor.Enable(True)
        self.tree.SetFocus()

    def save_needed(self, meld=True):
        """eigenlijk bedoeld om te reageren op een indicatie dat er iets aan de
        verzameling notities is gewijzigd (de oorspronkelijke self.project_dirty)"""
        ## if not dts.Mixin.save_needed(self): # too restrictive
        if not self.has_treedata:
            return True
        dlg = wx.MessageDialog(self, "Save current file before continuing?",
            "DocTree", wx.YES_NO)
        h = dlg.ShowModal()
        if h == wx.ID_YES:
            self.save(meld=meld)
        dlg.Destroy()
        return False if h == wx.ID_CANCEL else True

    def _read(self):
        """settings dictionary lezen, opgeslagen data omzetten naar tree"""
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemPyData(root, '')
        self.root = self.tree.AppendItem(root, os.path.splitext(
            os.path.basename(self.project_file))[0])
        self.activeitem = item_to_activate = self.root
        self.editor.Clear()
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.SetItemText(self.root, self.opts["RootTitle"].rstrip())
        self.tree.SetItemPyData(self.root, self.opts["RootData"])
        self.editor.set_contents(self.opts["RootData"])
        menuitem_list = [x for x in self.viewmenu.GetMenuItems()]
        for menuitem in menuitem_list[4:]:
            self.viewmenu.DeleteItem(menuitem)
        for idx, name in enumerate(self.opts["ViewNames"]):
            menu_item = wx.MenuItem(self.viewmenu, -1, name, "switch to this view",
                wx.ITEM_CHECK)
            self.Bind(wx.EVT_MENU, self.select_view, menu_item)
            self.viewmenu.AppendItem(menu_item)
            if idx == self.opts["ActiveView"]:
                menu_item.Check()

    def _finish_read(self, item_to_activate):
        ## print(item_to_activate, self.activeitem)
        self.tree.Expand(self.root)
        if item_to_activate and item_to_activate != self.activeitem:
            self.tree.SelectItem(item_to_activate)
        self.tree.SetFocus()

    def _finish_add(self, parent, item):
        self.tree.Expand(parent)
        self.tree.SelectItem(item)
        if item != self.root:
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()

    def _finish_copy(self, prev):
        self.tree.SelectItem(prev)

    def _finish_paste(self, current):
        "nog niet geactiveerd in deze versie"
        pass

    def _finish_rename(self, item, item_to_expand):
        self.tree.Expand(root_to_expand)
        self.tree.SelectItem(item)

    def ok_to_reload(self):
        dlg = wx.MessageDialog(self, 'OK to reload?', 'DocTree', wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        dlg.Destroy()
        return True if result == wx.ID_OK else False

    def write(self, meld=True):
        self.opts["ScreenSize"] = tuple(self.GetSize())
        self.opts["SashPosition"] = self.splitter.GetSashPosition()
        dts.Mixin.write(self, meld=meld)

    def hide_me(self, event = None):
        """applicatie verbergen"""
        if self.opts["AskBeforeHide"]:
            dlg = CheckDialog(self, -1, 'DocTree')
            dlg.ShowModal()
            if dlg.check_box.GetValue():
                self.opts["AskBeforeHide"] = False
            dlg.Destroy()
        self.tbi = wx.TaskBarIcon()
        self.tbi.SetIcon(self.nt_icon,"Click to revive DocTree")
        wx.EVT_TASKBAR_LEFT_UP(self.tbi, self.revive)
        wx.EVT_TASKBAR_RIGHT_UP(self.tbi, self.revive)
        self.Hide()

    def revive(self, event = None):
        """applicatie weer zichtbaar maken"""
        self.Show()
        self.tbi.Destroy()

    def afsl(self, event = None):   # check
        """applicatie afsluiten"""
        if self.has_treedata:
            self.save(meld=False)
        if event:
            event.Skip()

    def _update_newview(self, new_view):
        "view menu bijwerken n.a.v. toevoeging nieuwe view"
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for idx, menuitem in enumerate(menuitem_list[4:]):
            if idx == self.opts["ActiveView"]:
                menuitem.Check(False)
        menu_item = wx.MenuItem(self.viewmenu, -1, new_view, "switch to this view",
            wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.select_view, menu_item)
        self.viewmenu.AppendItem(menu_item)
        menu_item.Check()

    def _rebuild_root(self):
        "tree leegmaken en root opnieuw neerzetten"
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemPyData(root, '')
        self.root = self.tree.AppendItem(root, os.path.splitext(
            os.path.basename(self.project_file))[0])
        self.tree.SetItemText(self.root, self.opts["RootTitle"].rstrip())
        self.tree.SetItemPyData(self.root, self.opts["RootData"])

    def _get_name(self, caption, title, oldname):
        newname = oldname
        dlg = wx.TextEntryDialog(self, caption, title, oldname)
        ok = dlg.ShowModal()
        if ok:
            newname = dlg.GetValue()
        return ok, newname

    def _add_view_to_menu(self, newname):
        pass # benodigde acties al uitgevoerd in _update_newview

    def _finish_add_view(self, event=None):
        "handles Menu > View > New view"
        self.tree.SelectItem(tree_item)

    def next_view(self, prev=False):
        "not implemented in this version"

    def _update_selectedview(self):
        self.editor.Clear()
        menu_id = event.GetId()
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for menuitem in menuitem_list[4:]:
            if menuitem.GetId() == menu_id:
                newview = menuitem.GetItemLabelText()
                menuitem.Check()
            else:
                if menuitem.IsChecked():
                    menuitem.Check(False)
        return newview.split(None,1)[1]

    def _finish_select_view(self, tree_item):
        self.tree.SelectItem(tree_item)

    def _confirm(self, title, text):
        "handles Menu > View > Delete current view"
        dlg = wx.MessageDialog(self, text, title, wx.YES_NO)
        hlp = dlg.ShowModal()
        dlg.Destroy()
        return True if hlp == wx.ID_YES else False

    def _update_removedview(self):
        menuitem_list = self.viewmenu.GetMenuItems()
        menuitem_list[self.opts["ActiveView"] + 4].Check()
        for menuitem in menuitem_list:
            if menuitem.GetItemLabelText() == viewname:
                self.viewmenu.DeleteItem(menuitem)
                break
        if self.opts["ActiveView"] == 0:
            menuitem_list[4].Check()

    def _finish_remove_view(self, item):
        self.tree.SelectItem(item)

    def _reorder_items(self, root, recursive = False):
        "(re)order_items"
        data = []
        tag, cookie = self.tree.GetFirstChild(root)
        while tag.IsOk():
            if recursive:
                self.reorder_items(tag, recursive)
            data.append(getsubtree(self.tree, tag))
            tag, cookie = self.tree.GetNextChild(root, cookie)
        self.tree.DeleteChildren(root)
        for item in sorted(data):
            putsubtree(self.tree, root, *item)

    def _set_next_item(self):
        item = self.tree.GetNextSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        return item.IsOK()

    def _set_prev_item(self):
        item = self.tree.GetPrevSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        return item.IsOK()

def main(fname=''):
    app = wx.App(redirect=True, filename="doctree_wx.log")
    print(dt.datetime.today().strftime("%d-%m-%Y %H:%M:%S").join(
        ("\n------------------","------------------\n")))
    frame = MainWindow(None, -1, "DocTree - " + fname)
    app.SetTopWindow(frame)
    if fname:
        frame.project_file = fname
        err = frame.read()
        if err:
            wx.MessageBox(err, "Error")
    app.MainLoop()

if __name__ == '__main__':
    main('wx_tree.pck')
