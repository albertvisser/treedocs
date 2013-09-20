#! /usr/bin/env python
# -*- coding: utf-8 -*-
# het principe (splitter window met een tree en een tekst deel) komt oorspronkelijk van een ibm site

# TODO - toolbar definitie afmaken (is misschien niet nodig)

import os
import wx
import wx.lib.mixins.treemixin as treemix
import wx.richtext as rt
import cPickle as pck
import shutil
import pprint
import datetime as dt
import StringIO as io
HERE = os.path.dirname(__file__)
FILTER = "Pickle files|*.pck"


def getsubtree(tree, item):
    """recursieve functie om de strucuur onder de te verplaatsen data
    te onthouden"""
    titel = tree.GetItemText(item)
    ## print("calling getsubtree on {}".format(titel))
    text = tree.GetItemPyData(item)
    subtree = []
    tag, cookie = tree.GetFirstChild(item)
    while tag.IsOk():
        subtree.append(getsubtree(tree, tag))
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
    """TreeCtrl met drag&drop faciliteit"""
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

class EditorPanel(rt.RichTextCtrl):
    def __init__(self, parent, _id):
        rt.RichTextCtrl.__init__(self, parent, _id,
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

class MainWindow(wx.Frame):
    """Hoofdscherm van de applicatie"""
    def __init__(self, parent, _id, title):
        self.opts = {
            "AskBeforeHide": True, "SashPosition": 180, "ScreenSize": (800, 500),
            "ActiveItem": [0,], "ActiveView": 0, "ViewNames": ["Default",],
            "RootTitle": "MyNotes", "RootData": ""}
        wx.Frame.__init__(self, parent, _id, title, size = self.opts['ScreenSize'],
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.nt_icon = wx.Icon(os.path.join(HERE, "doctree.ico"),wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.nt_icon)
        self.statbar = self.CreateStatusBar()

        tbar = wx.ToolBar(self, -1)
        menuBar = wx.MenuBar()
        self.SetMenuBar(menuBar)

        self.splitter = wx.SplitterWindow (self, -1, style = wx.NO_3D) # |wx.SP_3D
        self.splitter.SetMinimumPaneSize (1)

        self.tree = TreePanel(self.splitter, -1,
            style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.TR_HAS_VARIABLE_ROW_HEIGHT
            )
        self.root = self.tree.AddRoot("MyNotes")
        self.activeitem = self.root
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.tree.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.editor = EditorPanel(self.splitter, -1)
        self.editor.Enable(0)
        self.editor.new_content = True
        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.create_menu(menuBar, (
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
        )
        ## self.create_toolbar(tbar) # frm)

        self.splitter.SplitVertically(self.tree, self.editor)
        self.splitter.SetSashPosition(self.opts['SashPosition'], True)
        ## self.splitter.Bind(wx.EVT_KEY_DOWN, self.on_key)
        ## self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_CLOSE, self.afsl)

        self.tree.SetFocus()
        self.Show(True)

    def forward_event(self, evt):
        # The RichTextCtrl can handle menu and update events for undo,
        # redo, cut, copy, paste, delete, and select all, so just
        # forward the event to it.
        self.editor.ProcessEvent(evt)

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
                    print "on_key (tab): KeyError, waarschijnlijk op root"
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

    def set_title(self):
        "standaard manier van window titel instellen"
        self.SetTitle("DocTree - {} (view: {})".format(
            os.path.split(self.project_file)[1],
            self.opts["ViewNames"][self.opts['ActiveView']]))

    def open(self, event=None):
        "afhandelen Menu > Open / Ctrl-O"
        self.save_needed()
        dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self, "DocTree - choose file to open",
            dirname, "", FILTER, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename, dirname = dlg.GetFilename(), dlg.GetDirectory()
            self.project_file = os.path.join(dirname, filename)
            err = self.read()
            if err:
                wx.MessageBox(err, "Error")
        dlg.Destroy()

    def new(self, event=None):
        "Afhandelen Menu - Init / Ctrl-I"
        self.save_needed()
        dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self, "DocTree - enter name for new file",
            dirname, "", FILTER, wx.SAVE | wx.OVERWRITE_PROMPT)
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
            self.set_title()
            self.tree.SetFocus()
        dlg.Destroy()

    def save_needed(self):
        """eigenlijk bedoeld om te reageren op een indicatie dat er iets aan de
        verzameling notities is gewijzigd (de oorspronkelijke self.project_dirty)"""
        if not self.has_treedata:
            return
        dlg = wx.MessageDialog(self, "Save current file before continuing?",
            "DocTree", wx.YES_NO)
        h = dlg.ShowModal()
        if h == wx.ID_YES:
            self.save()
        dlg.Destroy()

    def treetoview(self):
        """zet de visuele tree om in een tree om op te slaan"""
        def lees_item(item):
            """recursieve functie om de data in een pickle-bare structuur om te zetten"""
            textref = self.tree.GetItemPyData(item)
            if item == self.activeitem:
                self.opts["ActiveItem"][self.opts["ActiveView"]] = textref
            kids = []
            tag, cookie = self.tree.GetFirstChild(item)
            while tag.IsOk():
                kids.append(lees_item(tag))
                tag, cookie = self.tree.GetNextChild(item, cookie) # tag, cookie)
            return textref, kids
        data = []
        tag, cookie = self.tree.GetFirstChild(self.root)
        while tag.IsOk():
            data.append(lees_item(tag))
            tag, cookie = self.tree.GetNextChild(self.root, cookie)
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
            "RootTitle": "MyNotes", "RootData": ""}
        mld = ''
        try:
            f_in = open(self.project_file, "rb")
        except IOError:
            return "couldn't open "+ self.project_file
        try:
            nt_data = pck.load(f_in)
        except EOFError:
            mld = "couldn't load data"
        finally:
            f_in.close()
        try:
            test = nt_data[0]["AskBeforeHide"]
        except (ValueError, KeyError):
            mld = "not a valid Doctree data file"
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
        item_to_activate = self.viewtotree()
        self.tree.Expand(self.root)
        if item_to_activate != self.activeitem:
            self.tree.SelectItem(item_to_activate)
        self.set_title()
        self.tree.SetFocus()

    def reread(self, event = None):
        """afhandelen Menu > Reload (Ctrl-R)"""
        dlg = wx.MessageDialog(self, 'OK to reload?', 'DocTree', wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.read()

    def save(self, event = None, meld = True):
        """afhandelen Menu > save"""
        if self.project_file:
            self.write(meld = meld)
        else:
            self.saveas()
        self.statbar.SetStatusText('{} opgeslagen'.format(self.project_file))

    def write(self, event = None, meld = True):
        """settings en tree data in een structuur omzetten en opslaan"""
        self.check_active()
        self.opts["ScreenSize"] = tuple(self.GetSize())
        self.opts["SashPosition"] = self.splitter.GetSashPosition()
        self.views[self.opts["ActiveView"]] = self.treetoview()
        nt_data = {0: self.opts, 1: self.views, 2: self.itemdict}
        try:
            shutil.copyfile(self.project_file, self.project_file + ".bak")
        except IOError:
            pass
        f_out = open(self.project_file,"w")
        pck.dump(nt_data, f_out)
        f_out.close()
        if meld:
            wx.MessageBox(self.project_file + " is opgeslagen","DocTool")

    def saveas(self, event = None):
        """afhandelen Menu > Save As"""
        dirname = os.path.dirname(self.project_file)
        dlg = wx.FileDialog(self, "DocTree - Save File as:", dirname, "",
            FILTER, wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename, dirname = dlg.GetFilename(), dlg.GetDirectory()
            self.project_file = os.path.join(dirname, filename)
            self.write()
            self.set_title()
        dlg.Destroy()

    def hide(self, event = None):
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

    def afsl(self, event = None):
        """applicatie afsluiten"""
        if self.has_treedata:
            self.save(meld=False)
        if event:
            event.Skip()

    def add_view(self, event = None):
        "handles Menu > View > New view"
        self.check_active()
        self.opts["ActiveItem"][self.opts["ActiveView"]] = self.tree.GetItemPyData(
            self.activeitem)
        self.views[self.opts["ActiveView"]] = self.treetoview()
        self.viewcount += 1
        new_view = "New View #{}".format(self.viewcount)
        self.opts["ViewNames"].append(new_view)
        active = self.opts["ActiveItem"][self.opts["ActiveView"]]
        self.opts["ActiveItem"].append(active)
        menuitem_list = list(self.viewmenu.GetMenuItems())
        for idx, menuitem in enumerate(menuitem_list[4:]):
            if idx == self.opts["ActiveView"]:
                menuitem.Check(False)
        menu_item = wx.MenuItem(self.viewmenu, -1, new_view, "switch to this view",
            wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.select_view, menu_item)
        self.viewmenu.AppendItem(menu_item)
        menu_item.Check()
        self.opts["ActiveView"] = self.opts["ViewNames"].index(new_view)
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemPyData(root, '')
        self.activeitem = self.root = self.tree.AppendItem(root, os.path.splitext(
            os.path.basename(self.project_file))[0])
        self.tree.SetItemText(self.root, self.opts["RootTitle"].rstrip())
        self.tree.SetItemPyData(self.root, self.opts["RootData"])
        newtree = []
        for key in sorted(self.itemdict.keys()):
            newtree.append((key, []))
        self.views.append(newtree)
        tree_item = self.viewtotree()
        self.set_title()
        self.tree.SelectItem(tree_item)

    def rename_view(self, event = None):
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

    def select_view(self, event = None):
        "handles Menu > View > <view name>"
        self.check_active()
        self.views[self.opts["ActiveView"]] = self.treetoview()
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
        self.opts["ActiveView"] = self.opts["ViewNames"].index(newview)
        self.tree.DeleteChildren(self.root)
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemPyData(root, '')
        self.activeitem = self.root = self.tree.AppendItem(root, os.path.splitext(
            os.path.basename(self.project_file))[0])
        self.tree.SetItemText(self.root, self.opts["RootTitle"].rstrip())
        self.tree.SetItemPyData(self.root, self.opts["RootData"])
        self.set_title()

        self.tree.SelectItem(self.viewtotree())

    def remove_view(self, event = None):
        "handles Menu > View > Delete current view"
        dlg = wx.MessageDialog(self, "Are you sure you want to remove this view?",
            "DocTree", wx.YES_NO)
        hlp = dlg.ShowModal()
        if hlp == wx.ID_YES:
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
            self.tree.DeleteAllItems()
            root = self.tree.AddRoot("hidden_root")
            self.tree.SetItemPyData(root, '')
            self.activeitem = self.root = self.tree.AppendItem(root, os.path.splitext(
                os.path.basename(self.project_file))[0])
            self.tree.SetItemText(self.root, self.opts["RootTitle"].rstrip())
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
        if under:
            item = self.tree.AppendItem (root, new_title)
        else:
            item = self.tree.InsertItem (root, self.activeitem, new_title)
        self.tree.SetItemPyData(item, newkey)
        if extra_title:
            subkey = newkey + 1
            self.itemdict[subkey] = (extra_title, "")
            sub_item = self.tree.AppendItem(item, extra_title)
            self.tree.SetItemPyData(sub_item, subkey)
            item = sub_item
        for idx, view in enumerate(self.views):
            if idx != self.opts["ActiveView"]:
                subitem = []
                if extra_title:
                    subitem.append((subkey, []))
                view.append((newkey, subitem))
        self.tree.Expand(root)
        self.tree.SelectItem(item)
        if item != self.root:
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()

    def insert_item(self, event=None):
        """nieuw item toevoegen *achter* het geselecteerde (en onder diens parent)"""
        self.add_item(event = event, under = False)

    def delete_item(self, event = None):
        """item verwijderen"""
        def check_item(view, ref):
            klaar = False
            for item, subview in view:
                if item == ref:
                    view.remove((item, subview))
                    klaar = True
                    break
                else:
                    klaar = check_item(subview, item)
                    if klaar:
                        break
            return klaar
        item = self.tree.GetSelection()
        if item != self.root:
            prev = self.tree.GetPrevSibling(item)
            if not prev.IsOk():
                prev = self.tree.GetItemParent(item)
                if prev == self.root:
                    prev = self.tree.GetNextSibling(item)
            self.activeitem = None
            ref = self.tree.GetItemPyData(item)
            self.itemdict.pop(ref)
            self.tree.Delete(item)
            for ix, view in enumerate(self.views):
                if ix != self.opts["ActiveView"]:
                    check_item(view, ref)
            self.tree.SelectItem(prev)
        else:
            wx.MessageBox("Can't delete root", "Error")

    def rename_item(self):
        """titel van item wijzigen"""
        def check_item(view, ref, subref):
            """zoeken waar het subitem moet worden toegevoegd"""
            retval = ""
            print(view)
            for itemref, subview in view:
                if itemref == ref:
                    subview.append((subref, []))
                    retval = 'Stop'
                else:
                    retval = check_item(subview, ref, subref)
                if retval == 'Stop':
                    break
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
            for idx, view in enumerate(self.views):
                if idx != self.opts["ActiveView"]:
                    check_item(view, ref, subref)
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

    def order_top(self, event = None):
        """order items directly under the top level"""
        self.reorder_items(self.root)

    def order_all(self, event = None):
        """order items under top level and below"""
        self.reorder_items(self.root, recursive = True)

    def reorder_items(self, root, recursive = False):
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

    def order_this(self, event = None):
        """order items directly under current level"""
        self.reorder_items(self.activeitem)

    def order_lower(self, event = None):
        """order items under current level and below"""
        self.reorder_items(self.activeitem, recursive = True)

    def next_note(self, event = None):
        """move to next item"""
        item = self.tree.GetNextSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)

    def prev_note(self, event = None):
        """move to previous item"""
        item = self.tree.GetPrevSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)

    def check_active(self, message = None):
        """zorgen dat de editor inhoud voor het huidige item bewaard wordt in de treectrl"""
        if self.activeitem:
            self.tree.SetItemBold(self.activeitem, False)
            if self.editor.IsModified():
                if message:
                    wx.MessageBox(message, 'DocTree')
                ref = self.tree.GetItemPyData(self.activeitem)
                try:
                    titel, tekst = self.itemdict[ref]
                except KeyError:
                    ref = self.editor.get_contents()
                    if ref:
                        self.tree.SetItemPyData(self.root, ref)
                        self.opts["RootData"] = ref
                else:
                    self.itemdict[ref] = (titel, self.editor.get_contents())

    def activate_item(self, item):
        """geselecteerd item "actief" maken (accentueren)"""
        self.activeitem = item
        self.tree.SetItemBold(item, True)
        ref = self.tree.GetItemPyData(item)
        try:
            titel, tekst = self.itemdict[ref]
        except KeyError:
            self.editor.set_contents(ref)
        else:
            self.editor.set_contents(tekst)
        self.editor.Enable(True)

    def info_page(self, event = None):
        """help -> about"""
        info = [
            "DocTree door Albert Visser",
            "Uitgebreid electronisch notitieblokje",
            "wxPython versie",
            ]
        dlg = wx.MessageDialog(self, "\n".join(info), 'DocTree',
            wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def help_page(self, event = None):
        """help -> keys"""
        info = [
            "Ctrl-N\t\t- nieuwe notitie onder huidige",
            "Shift-Ctrl-N\t\t- nieuwe notitie onder hoogste niveau",
            "Insert\t\t- nieuwe notitie achter huidige",
            "Ctrl-PgDn in editor of"
            " CursorDown in tree\t- volgende notitie",
            "Ctrl-PgUp in editor of"
            " CursorUp in tree\t- vorige notitie",
            "Ctrl-D of Delete in tree\t- verwijder notitie",
            "Ctrl-S\t\t- alle notities opslaan",
            "Shift-Ctrl-S\t\t- alle notities opslaan omder andere naam",
            "Ctrl-R\t\t- alle notities opnieuw laden",
            "Ctrl-O\t\t- ander bestand met notities laden",
            "Ctrl-I\t\t- initialiseer (nieuw) notitiebestand",
            "Ctrl-Q, Esc\t\t- opslaan en sluiten",
            "Ctrl-H\t\t- verbergen in system tray",
            "",
            "F1\t\t- deze (help)informatie",
            "F2\t\t- wijzig notitie titel",
            "Shift-F2\t\t- wijzig root titel",
            ]
        dlg = wx.MessageDialog(self, "\n".join(info), 'DocTree',
            wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

def main(fname=''):
    app = wx.App(redirect=True, filename="doctree.log")
    print dt.datetime.today().strftime("%d-%m-%Y %H:%M:%S").join(
        ("\n------------------","------------------\n"))
    frame = MainWindow(None, -1, "DocTree - " + fname)
    app.SetTopWindow(frame)
    if fname:
        frame.project_file = fname
        err = frame.read()
        if err:
            wx.MessageBox(err, "Error")
    app.MainLoop()

