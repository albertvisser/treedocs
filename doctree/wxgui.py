"""DocTree: wxPython specific stuff
"""
import os
import sys
import contextlib
import tempfile
import wx
import wx.adv
import wx.lib.mixins.treemixin as treemix
import wx.lib.mixins.listctrl as listmix
import wx.richtext as rt
import wx.lib.colourselect as csel
import wx.lib.buttons as wxlb


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


def get_choice(win, caption, options, current):
    "open a dialog and let the user choose from a set of possible values"
    with wx.SingleChoiceDialog(win, caption, 'DocTree', options, wx.CHOICEDLG_STYLE) as dlg:
        dlg.SetSelection(current)
        h = dlg.ShowModal()
        ok = h == wx.ID_OK
        sel = dlg.GetStringSelection()
    return ok, sel


def get_filename(win, title, start, save=False):
    "routine for selection of filename"
    name, ext = win.master.FILE_TYPE
    filter_ = f"{name} (*{ext})|*{ext}"
    start = os.path.dirname(start)
    if save:
        dlg = wx.FileDialog(win, title, start, '', filter_, wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    else:
        dlg = wx.FileDialog(win, title, start, '', filter_, wx.FD_OPEN)
    ok, filename = False, ''
    with dlg:
        if dlg.ShowModal() == wx.ID_OK:
            ok = True
            filename = os.path.join(dlg.GetDirectory(), dlg.GetFilename())
    return ok, filename


def show_dialog(dlg):
    "show dialog and return whether confirmed or rejected"
    with dlg.gui:
        result = dlg.gui.ShowModal()
        data = dlg.confirm()
    return result == wx.ID_OK, data


def show_nonmodal(dlg):
    "show dialog and return to ongoing business"
    dlg.Show()


# wordt niet gebruikt?
# def get_hotkeys_from_text(label):
#     """if menu text contains accelerator, retrieve keys part, strip off brackets and split on comma
#     """
#     text = label.split('\n')
#     hotkeys = []
#     if len(text) == len(['label', 'key']):
#         keys = text[1][1:-1].split(', ')
#         for item in keys:
#             test = item.split('+')
#             key = test[-1]
#             mods = []
#             if len(test) > 1:
#                 mods = test[:-1]
#             key = {'F1': wx.WXK_F1,
#                    'F2': wx.WXK_F2,
#                    'Insert': wx.WXK_INSERT,
#                    'Del': wx.WXK_DELETE,
#                    'PgDn': wx.WXK_PAGEDOWN,
#                    'PgUp': wx.WXK_PAGEUP,
#                    'Esc': wx.WXK_ESCAPE}.get(ord(key))
#             # for ix, mod in enumerate(mods):
#             for ix in range(mods):
#                 mods[ix] = {'Ctrl': wx.MOD_CONTROL,
#                             'Shift': wx.MOD_SHIFT}.get()
#         hotkeys.append(mods, key)
#     return hotkeys


class MainGui(wx.Frame):
    "Primary application window (main screen)"
    def __init__(self, master, title):
        self.master = master
        self.title = title
        self.app = wx.App()
        super().__init__(parent=None, title=title, size=self.master.opts['ScreenSize'],
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.app_icon = wx.Icon(os.path.join(self.master.HERE, 'icons', "doctree.ico"),
                                wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.app_icon)

    def create_menu(self, menudata):
        """bouw het menu en de meeste toolbars op"""
        toolbar = wx.ToolBar(self)
        self.SetToolBar(toolbar)
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        # update_ui = {}  # bijwerken menu is niet meer nodig
        #              # "&Bold": self.editor.update_bold,
        #              # "&Italic": self.editor.update_italic,
        #              # "&Underline": self.editor.update_underline,
        #              # 'Strike&through': self.editor.update_strikethrough,
        #              # "Align &Left": self.editor.update_alignleft,
        #              # "&Center": self.editor.update_center,
        #              # "Align &Right": self.editor.update_alignright,
        #              # '&Justify': None}
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
            if item in (menudata[3][0], menudata[4][0], menudata[5][0]):
                toolbar.AddSeparator()
            prev = ''
            for menudef in data:
                label = ''
                if not menudef:
                    if prev != 'spacer':
                        prev = 'spacer'
                        submenu.AppendSeparator()
                    continue
                prev = ''
                label, handler, shortcut, icon, info = menudef
                if shortcut == 'Ctrl+Tab':
                    shortcut = ''  # Tab werkt niet in gtk
                # (nog) niet in wx geïmplementeerde menukeuzes overslaan
                if ('monospace' in label.lower() or 'justify' in label.lower()
                        or 'indent' in label.lower()):
                # for text in ('monospace', 'justify', 'indent'):
                #     if text in label.lower():
                    continue
                # icon is mede bedoeld om van hieruit de toolbar op te zetten
                if shortcut:
                    firstkey = shortcut.split(',', 1)[0].replace('PgDown', 'PgDn')
                    menulabel = f'{label}\t{firstkey}'
                else:
                    menulabel = label
                # menuitems kunnen niet zowel een icon als type check hebben
                # if info.startswith("Check"):
                #     menu_item = wx.MenuItem(submenu, -1, menulabel, info, wx.ITEM_CHECK)
                # else:
                menu_item = wx.MenuItem(submenu, -1, menulabel, info)
                # menu_item = submenu.Append(wx.ID_ANY, menulabel, info)
                if item == menudata[3][0]:
                    if label == '&Undo':
                        self.undo_item = menu_item
                    elif label == '&Redo':
                        self.redo_item = menu_item
                self.Bind(wx.EVT_MENU, handler, menu_item)
                if icon:
                    bmp = wx.Bitmap(os.path.join(self.master.HERE, icon), wx.BITMAP_TYPE_PNG)
                    menu_item.SetBitmap(bmp)
                    # tevens opbouwen eerste toolbar
                    # tooltype = wx.ITEM_NORMAL
                    # if label in update_ui and update_ui[label] is not None:
                    #     tooltype = wx.ITEM_CHECK
                    toolitem = toolbar.AddTool(-1, label, bmp)
                    # item = toolbar.AddTool(-1, label, bmp, shortHelp=info, kind=tooltype)
                    # if label in update_ui:
                    #     if update_ui[label]:
                    #         callback, ui_updater = handler, update_ui[label]
                    # else:
                    # #     callback = ui_updater = self.forward_event
                    #     callback, ui_updater = handler, None
                    # self.Bind(wx.EVT_TOOL, callback, toolitem)
                    self.Bind(wx.EVT_TOOL, handler, toolitem)
                    # if ui_updater:
                    #     self.Bind(wx.EVT_UPDATE_UI, ui_updater, toolitem)
                submenu.Append(menu_item)
            menubar.Append(submenu, menu_label)

    def create_splitter(self):
        "create main pportion of window"
        self.splitter = wx.SplitterWindow(self, -1)  # , style = wx.NO_3D) # |wx.SP_3D
        self.splitter.SetMinimumPaneSize(1)
        # self.splitter.parent = self

    def create_tree_on_left(self):
        "create treeview for organizing"
        self.tree = TreePanel(self.splitter, style=wx.TR_HAS_BUTTONS)
        self.tree.controller = self.master
        self.root = self.tree.AddRoot("MyNotes")
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.tree.Bind(wx.EVT_KEY_DOWN, self.on_key)

    def create_editor_on_right(self):
        "create editor"
        self.editor = EditorPanel(self.splitter)
        self.editor.Enable(False)
        # self.editor.new_content = True
        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_key)

    def create_statusbar_at_bottom(self):
        "create area for status messages"
        self.statbar = self.CreateStatusBar()

    def finalize_display(self):
        "finish off screen creation"
        self.menu_disabled = True
        toolbar = self.GetToolBar()
        self.create_stylestoolbar(toolbar)
        toolbar.Realize()

        self.splitter.SplitVertically(self.tree, self.editor)
        try:
            self.splitter.SetSashPosition(self.master.opts['SashPosition'], True)
        except TypeError:
            self.splitter.SetSashPosition(self.master.opts['SashPosition'][0], True)
        self.Bind(wx.EVT_CLOSE, self.afsl)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        # vbox.SetSizeHints(self)
        self.SetSize(self.master.opts['ScreenSize'])
        self.in_editor = False
        self.Layout()
        # self.tree.SetFocus()
        self.Show(True)

    def disable_menu(self, value=True):
        """disable most menu actions when tree is not properly initialized;
        re-enable menu actions after tree is properly initialized
        """
        menubar = self.GetMenuBar()
        for menuindex in range(1, len(menubar.GetMenus())):
            menubar.EnableTop(menuindex, not value)
        mainmenu = menubar.GetMenu(0)
        for menuitem in mainmenu.GetMenuItems():
            if menuitem.GetItemLabelText() not in ('Open', 'Init', 'eXit'):
                mainmenu.Enable(menuitem.GetId(), not value)
        self.menu_disabled = value

    def create_stylestoolbar(self, toolbar):
        "build toolbar with buttons to change styles"
        # most is done during menu creation, this is some leftover stuff
        self.textcolour = wx.BLACK
        # self.fontpicker = wx.FontPickerCtrl(toolbar, style=wx.FNTP_FONTDESC_AS_LABEL)
        # self.fontpicker.Bind(wx.EVT_FONTPICKER_CHANGED, self.editor.text_font)
        # toolbar.AddControl(self.fontpicker)
        self.fgcselect = csel.ColourSelect(toolbar, colour=self.textcolour)
        self.fgcselect.Bind(csel.EVT_COLOURSELECT, self.editor.select_text_color)
        toolbar.AddControl(self.fgcselect)
        bmp = wx.Bitmap(14, 14)
        self.fgcset = wxlb.GenBitmapButton(toolbar, bitmap=bmp, size=(22, 22))
        self.changebitmapbuttoncolour(self.fgcset, self.textcolour)
        self.fgcset.Bind(wx.EVT_BUTTON, self.editor.set_text_color)
        toolbar.AddControl(self.fgcset)
        self.backgroundcolour = wx.WHITE
        self.bgcselect = csel.ColourSelect(toolbar, colour=self.backgroundcolour, size=(24, 24))
        self.bgcselect.Bind(csel.EVT_COLOURSELECT, self.editor.select_background_color)
        toolbar.AddControl(self.bgcselect)
        bmp = wx.Bitmap(16, 16)
        self.bgcset = wxlb.GenBitmapButton(toolbar, bitmap=bmp, size=(24, 24))
        self.changebitmapbuttoncolour(self.bgcset, self.backgroundcolour)
        self.bgcset.Bind(wx.EVT_BUTTON, self.editor.set_background_color)
        toolbar.AddControl(self.bgcset)

    @staticmethod
    def changebitmapbuttoncolour(bitmapbutton, colour):
        "recolor the button"
        bmp = bitmapbutton.GetBitmapLabel()
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush(colour))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)
        bitmapbutton.SetBitmapLabel(bmp)

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
        # self.splitter.SetSashPosition(self.master.opts["SashPosition"], True)
        self.splitter.SetSashPosition(pos[0], True)

    def get_splitterpos(self):
        "return the position at which the screen is split"
        # return self.splitter.GetSashPosition()
        return (self.splitter.GetSashPosition(), )

    def init_app(self):
        "undo stack leegmaken"
        # self.undo_stack.clear()    niet van toepassing voor wx variant

    def set_focus_to_tree(self):
        "schakel over naar tree"
        self.tree.SetFocus()
        self.in_editor = False

    def set_focus_to_editor(self):
        "set focus to the editor panel"
        self.editor.SetFocus()
        ref = self.tree.getitemkey(self.master.activeitem)
        with contextlib.suppress(KeyError):
            self.editor.set_text_position(self.master.text_positions[ref])
        self.in_editor = True

    def go(self):
        "start the application's event loop"
        self.app.MainLoop()

    def close(self, event=None):
        """quit application from menu"""
        self.Close()

    def afsl(self, event=None):
        """applicatie afsluiten"""
        if not self.master.handle_save_needed():
            return
        self.master.cleanup_files()
        if event:
            event.Skip()

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

    def expand_root(self):
        "expandeer het root item"

    def start_add(self, root=None, under=True, new_title='', extra_titles=None):
        """nieuw item toevoegen (default: onder het geselecteerde)
        """
        origpos = -1  # is dit niet te beperkt?
        added_treedata = [new_title, '']  # , []]
        subel = added_treedata  # [2]
        if extra_titles:
            for x in extra_titles:
                new_subel = [x, '']  # , []]
                subel.append(new_subel)
                subel = new_subel  # [2]
        subel.append([])
        self.master.do_addaction(root, under, origpos, added_treedata)

    def set_next_item(self, any_level=False):
        "for go to next"
        item = self.tree.GetNextSibling(self.master.activeitem)
        ok = item.IsOk()
        if ok:
            self.tree.SelectItem(item)
        return ok

    def set_prev_item(self, any_level=False):
        "for go to previous"
        item = self.tree.GetPrevSibling(self.master.activeitem)
        ok = item.IsOk()
        if ok:
            self.tree.SelectItem(item)
        return ok

    def start_copy(self, cut=False, retain=True, current=None):
        """start copy/cut/delete action

        parameters: cut: remove item from tree (True for cut, delete and move)
                    retain: remember item for pasting (True for cut and copy)
                    current: item to copy
        """
        self.master.do_copyaction(cut, retain, current)

    def start_paste(self, before=True, below=False, dest=None):
        """start paste actie
        """
        self.master.do_pasteaction(before, below, dest)

    def reorder_items(self, root, recursive=False):
        "(re)order_items"
        self.tree.SortChildren(root)
        if recursive:
            tag, cookie = self.tree.GetFirstChild(root)
            while tag.IsOk():
                # if recursive:
                self.reorder_items(tag, recursive)
                tag, cookie = self.tree.GetNextChild(root, cookie)

    def rebuild_root(self):
        "tree leegmaken en root opnieuw neerzetten"
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot("hidden_root")
        self.tree.SetItemData(root, '')
        self.root = self.tree.AppendItem(root, self.master.project_file.stem)
        # self.tree.SetItemText(self.root, self.master.opts["RootTitle"].rstrip())
        self.tree.setitemtitle(self.root, self.master.opts["RootTitle"].rstrip())
        self.tree.setitemkey(self.root, -1)
        # self.tree.SetItemData(self.root, self.master.opts["RootData"])
        self.tree.setitemtext(self.root, self.master.opts["RootData"])
        return self.root

    # def clear_viewmenu(self):
    #     "remove all view actions from viewmenu"
    #     menuitem_list = list(self.viewmenu.GetMenuItems())
    #     for menuitem in menuitem_list[4:]:
    #         self.viewmenu.Delete(menuitem)

    def add_viewmenu_option(self, optiontext, callback):
        "add view action to viewmenu"
        menu_item = wx.MenuItem(self.viewmenu, wx.ID_ANY, optiontext, 'Switch to this view',
                                kind=wx.ITEM_CHECK)
        # menu_item = self.viewmenu.AppendCheckItem(wx.ID_ANY, optiontext, 'Switch to this view'),
        self.Bind(wx.EVT_MENU, callback, menu_item)
        self.viewmenu.Append(menu_item)
        return menu_item

    # def check_viewmenu_option(self, arg):  # menu_item=None):
    #     "check the given view action or determine which one to set"
    #     # door *args door te geven komt de menu event hopenlijk alsnog binnen
    #     # if menu_item:
    #     if isinstance(arg, wx.MenuItem):
    #         arg.Check()
    #         return ''
    #     # menu_id = self._event.GetId()
    #     menu_id = arg.GetId()
    #     menuitem_list = list(self.viewmenu.GetMenuItems())
    #     for menuitem in menuitem_list[7:]:  # was 4
    #         if menuitem.GetId() == menu_id:
    #             newview = menuitem.GetItemLabelText()
    #             menuitem.Check()
    #         elif menuitem.IsChecked():
    #             menuitem.Check(False)
    #     return newview

    def check_menuitem_option(self, arg, value):
        "add or remove a checkmark to/from the given menu option"
        arg.Check(value)

    def determine_viewmenuitem(self, *args):
        "determine which menu option sent the menu event"
        # wx sends the event itself
        for item in self.viewmenu.GetMenuItems():
            if item.GetId() == args[0].GetId():
                return item

    # def uncheck_viewmenu_option(self):
    #     "uncheck the active viewmenu action"
    #     menuitem_list = list(self.viewmenu.GetMenuItems())
    #     for idx, menuitem in enumerate(menuitem_list[7:]):  # was 4
    #         if idx == self.master.opts["ActiveView"]:
    #             menuitem.Check(False)
    #             break

    # def rename_viewmenu_option(self, newname):
    #     "update menuitem text"
    #     menuitem_list = list(self.viewmenu.GetMenuItems())
    #     for idx, menuitem in enumerate(menuitem_list[7:]):  # was 4
    #         if idx == self.master.opts["ActiveView"]:
    #             menuitem.SetItemLabel(newname)
    #             break

    # def check_next_viewmenu_option(self, prev=False):
    #     "find the currently checked option, uncheck it and check the next/previous one"
    #     menuitem_list = [x for x in self.viewmenu.actions()][7:]
    #     if prev:
    #         menuitem_list.reverse()
    #     found_item = False
    #     for menuitem in menuitem_list:
    #         if menuitem.IsChecked():
    #             found_item = True
    #             menuitem.Check(False)
    #         elif found_item:
    #             menuitem.Check(True)
    #             found_item = False
    #             break
    #     if found_item:
    #         menuitem_list[0].Check(True)

    # def update_removedview(self, viewname):
    #     "view menu bijwerken n.a.v. verwijderen view"
    #     menuitem_list = self.viewmenu.GetMenuItems()
    #     removed = 0
    #     item_to_check = None  # menuitem_list[self.opts["ActiveView"] + 4].Check()
    #     for menuitem in menuitem_list[7:]:
    #         num, naam = str(menuitem.GetItemLabelText()).split(None, 1)
    #         if removed:
    #             menuitem.SetItemLabelText('&{int(num[1:]) - 1} {naam}')
    #             if not item_to_check:
    #                 item_to_check = menuitem
    #         if naam == viewname:
    #             self.viewmenu.Delete(menuitem)
    #             removed = True
    #             if self.master.opts['ActiveView'] >= int(num[1:]) - 1:
    #                 self.master.opts['ActiveView'] -= 1
    #             break
    #     if not item_to_check:
    #         item_to_check = menuitem_list[7]
    #     return item_to_check

    def get_viewmenu_options(self):
        "return a list of items in a menu"
        return list(self.viewmenu.GetMenuItems())  # [7:]

    def get_viewmenuoption_state(self, menuitem):
        "return the checked state of a menu option"
        return menuitem.IsChecked()

    def get_menuitem_text(self, menuitem):
        "return the text of a menu option"
        return str(menuitem.GetItemLabelText())

    def set_menuitem_text(self, menuitem, text):
        "set the text for a menu option"
        menuitem.SetItemLabel(text)

    def remove_menuoption(self, menu, menuitem):
        "remove an option from a menu"
        menu.Delete(menuitem)

    def tree_undo(self, event=None):
        "start undo action"

    def tree_redo(self, event=None):
        "start redo action"

    def find_needle(self, haystack):
        "search in plain text version of text"

    def goto_searchresult(self, loc):
        "position on found data in text"

    # niet meer nodig?
    # def forward_event(self, evt):
    #     """The RichTextCtrl can handle menu and update events for undo, redo,
    #     cut, copy, paste, delete, and select all, so just forward the event to it
    #     """
    #     ## print('forwarding', evt, 'to editor')
    #     self.editor.ProcessEvent(evt)

    def on_key(self, event):
        """afhandeling toetscombinaties"""
        skip = True
        keycode = event.GetKeyCode()
        # mods = event.GetModifiers()
        win = event.GetEventObject()
        if keycode == wx.WXK_ESCAPE and self.master.opts['EscapeClosesApp']:
            self.close()
        # elif keycode == wx.WXK_DELETE:
            # print('delete pressed', end=' ')
            # if win == self.editor:
            #     print('in editor, let editor handle this')
            # else:
            #     print('in tree: handle with delete item')
            # if win == self.tree:
            #     self.delete_item()
            #     skip = False
        elif keycode == wx.WXK_DELETE and win == self.tree:
            self.delete_item()
            skip = False
        # elif keycode == wx.WXK_TAB and win == self.editor:
        #     # dit betekent dat TAB in de editor geen tab invoegt maar naar de tree navigeert
        #     # dat is niet zoals de qt versie werkt
        #     if self.editor.IsModified():
        #         key = self.tree.GetItemData(self.master.activeitem)
        #         try:
        #             titel = self.itemdict[key][0]
        #         except KeyError:
        #             print("on_key (tab): KeyError, waarschijnlijk op root")
        #             if key:
        #                 self.tree.SetItemData(self.root, key)
        #         else:
        #             self.itemdict[key] = (titel, self.editor.get_contents())
        #     self.tree.SetFocus()
        #     skip = False
        if event and skip:
            event.Skip()

    def OnSelChanged(self, event):
        """zorgen dat het eerder actieve item onthouden wordt, daarna het geselecteerde
        tot nieuw actief item benoemen"""
        x = event.GetItem()
        # print('in OnSelChanged, x is', x)
        self.master.check_active()
        self.master.activate_item(x)
        event.Skip()

    # API compliance: deze twee methoden zijn nu nog onnodig omdat de Esc afhandeling anders gebeurt
    def add_escape_action(self):
        "Add accelerator to for Esc key to close application"

    def remove_escape_action(self):
        "Remove accelerator to for Esc key to close application"

    def cleanup_after_writing(self):
        "re-initialize if necessary"
        # no actions needed (as yet)


class TreePanel(treemix.DragAndDrop, wx.TreeCtrl):
    "Tree structure depicting the notes organization"
    # def __init__(self, *args, **kwargs):
    #     self.controller = args[0].parent
    #     super().__init__(self, *args, **kwargs)

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
        # dragtext = self.GetItemText(dragitem)  # alleen gebruikt in print statement?
        # dragdata = self.GetItemData(dragitem)  # niet gebruikt?
        dragtree = self.controller.getsubtree(self, dragitem)
        # pprint.pprint(dragtree)
        # droptext = self.GetItemText(dropitem)  # alleen gebruikt in print statement?
        # dropdata = self.GetItemData(dropitem)  # niet gebruikt?
        self.Delete(dragitem)
        # item = self.AppendItem(dropitem, dragtext)
        # self.SetItemData(item, dragdata)
        self.controller.putsubtree(self, dropitem, *dragtree)
        self.Expand(dropitem)

    def create_popupmenu(self, item):
        "rightclick menu in tree - not implemented yet in this version"

    def add_to_parent(self, itemkey, titel, parent, pos=-1):
        """add item to tree at a given location
        """
        ## log('*** in add_to_parent ***')
        ## log('parent is {}, pos is {}'.format(parent, pos))
        new = self.AppendItem(parent, titel) if pos == -1 else self.InsertItem(parent, pos, titel)
        # self.SetItemData(new, itemkey)
        # print(f'in add_to_parent, {itemkey=}, {titel=}, {parent=}, {new=}')
        self.setitemkey(new, itemkey)
        self.setitemtext(new, '')  # eigenlijk niet nodig
        return new

    def getitemdata(self, item):
        "titel + data in de visual tree ophalen"
        return self.getitemtitle(item), self.getitemkey(item)

    def getitemtext(self, item):
        "data in de visual tree ophalen"
        return self.GetItemData(item)[1]

    def getitemtitle(self, item):
        "alleen titel in de visual tree ophalen"
        return self.GetItemText(item)

    def getitemkey(self, item):
        "sleutel voor de itemdict ophalen"
        # return self.GetItemData(item)
        # print(f'in getitemkey, {item=}, {self.GetItemData(item)=}')
        value = self.GetItemData(item)
        if value:
            value = value[0]
            try:
                value = int(value)
            except ValueError:  # root element heeft geen numerieke key
                value = -1
            return value

    def setitemkey(self, item, value):
        "sleutel voor de itemdict onthouden"
        data = self.GetItemData(item)
        data = (value, data[1]) if data else (value, '')
        self.SetItemData(item, data)

    def setitemtitle(self, item, title):
        "titel (en tooltip instellen)"
        self.SetItemText(item, title)

    def setitemtext(self, item, text):
        """Meant to set the text for the (root) item
        """
        data = self.GetItemData(item)
        data = (data[0], text) if data else (-2, text)
        self.SetItemData(item, data)

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
        # try:
        root = self.GetItemParent(item)
        # except TypeError:   # geen item meegegeven - mag dat eigenlijk wel?
        if not root.IsOk():
            root = item
            pos = -1
        else:
            pos = 0
            tag, cookie = self.GetFirstChild(root)
            while tag.IsOk() and tag != item:
                pos += 1
                tag, cookie = self.GetNextChild(root, cookie)
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
        # self.SelectItem(item)
        self.SetFocusedItem(item)

    def get_selected_item(self):
        "return the selected tree item"
        return self.GetFocusedItem()

    def removeitem(self, item):   # , cut_from_itemdict):
        "removes current treeitem and returns the previous one"
        cut_from_itemdict = []
        parent, pos = self.getitemparentpos(item)
        oldloc = parent, pos
        prev = self.GetPrevSibling(item)
        if not prev.IsOk():
            prev = parent
            if prev == self.root:
                prev = self.GetNextSibling(item)
        cut_from_itemdict = self.parent.master.popitems(item, cut_from_itemdict)
        self.Delete(item)
        return oldloc, prev, cut_from_itemdict


class EditorPanel(rt.RichTextCtrl):
    "Rich text editor displaying the selected note"
    def __init__(self, parent):
        rt.RichTextCtrl.__init__(self, parent,  # size=(400,200),
                                 style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)
        self.textAttr = rt.RichTextAttr()
        self.parent_ = parent
        self.paragraph_indent = 100
        self.parspace_increment = 20
        self.mark_dirty(False)

    # def on_url(self, evt):
    #     "dummy handler for clicking on a url"
    #     wx.MessageBox(evt.GetString(), "URL Clicked")

    def set_contents(self, data):
        "load contents into editor"
        self.Clear()
        data = str(data)
        # self.SetValue(data)
        # als ik het onderstaande activeer en de app uitvoer krijg ik (maar niet altijd) een fout
        # gemeld in een popup: "xml parsing error: no element found at line 1" .
        if data.startswith("<?xml"):
            handler = rt.RichTextXMLHandler()
            _buffer = self.GetBuffer()
            _buffer.AddHandler(handler)
            # out = io.StringIO()              -- out moet een OutputStream subclass zijn?
            #                                     bv StringOutputStream maar die zijn er nog niet?
            # out = io.BytesIO()
            # out.write(data)
            # out.seek(0)
            # handler.LoadFile(_buffer, out)
            # handler.ImportXML(_buffer, data)
            with tempfile.NamedTemporaryFile(mode='w+') as out:
                out.write(data)
                out.seek(0)
                handler.LoadFile(_buffer, out.name)
            self.teststuff = handler, _buffer, out.name  # alleen t.b.v. unittest
        else:
            self.SetValue(data)  # WriteText(data)
        self.Refresh()

    def get_contents(self):
        "return contents from editor"
        # content = self.GetValue()
        handler = rt.RichTextXMLHandler()
        _buffer = self.GetBuffer()
        _buffer.AddHandler(handler)
        # print(type(_buffer), type(out))
        # out = io.StringIO()                  -- out moet een OutputStream subclass zijn?
        #                                         bv StringOutputStream maar die zijn er nog niet?
        # out = io.BytesIO()
        # handler.SaveFile(_buffer, out)
        # out.seek(0)
        # content = out.read()
        with tempfile.NamedTemporaryFile(mode='w+') as out:
            handler.SaveFile(_buffer, out.name)
            # handler.ExportXML(_buffer, content)
            # # of moet dit zijn ok = _buffer.SaveFile(_out) ?
            out.seek(0)
            content = out.read()
        self.teststuff = handler, _buffer, out.name  # alleen t.b.v. unittest
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
        "selectie doorhalen"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_FONT_STRIKETHROUGH)
        if not self.HasSelection():
            # print('vanaf hier')
            self.BeginStyle(attr)
        else:
            # print('selectie')
            range = self.GetSelectionRange()
            self.SetStyle(range, attr)

    def text_monospace(self, evt):  # 959
        """not implemented (yet)
        """

    def align_left(self, evt):
        "alinea links uitlijnen"
        self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)

    def align_center(self, evt):
        "alinea centreren"
        self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)

    def align_right(self, evt):
        "alinea rechts uitlijnen"
        self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)

    def text_justify(self, evt):
        "alinea uitvullen"
        show_message(self.parent, 'Sorry, Not possible in WxPython at this time')
        # self.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_JUSTIFIED)  # unimplemented vlgs docs

    def indent_more(self, evt):
        "alinea verder laten inspringen"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            attr.SetLeftIndent(attr.GetLeftIndent() + self.paragraph_indent)
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
            value = attr.GetLeftIndent()
            if value >= self.paragraph_indent:
                attr.SetLeftIndent(value - self.paragraph_indent)
                attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
                self.SetStyle(range, attr)

    def increase_parspacing(self, evt):
        "ruimte tussen alinea's vergroten"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + self.parspace_increment)
            attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
            self.SetStyle(range, attr)

    def decrease_parspacing(self, evt):
        "ruimte tussen alinea's verkleinen"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            value = attr.GetParagraphSpacingAfter()
            if value >= self.parspace_increment:
                attr.SetParagraphSpacingAfter(value - self.parspace_increment)
                attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
                self.SetStyle(range, attr)

    def set_linespacing_10(self, evt):
        "enkele regelafstand instellen"
        self.set_linespacing(10)

    def set_linespacing_15(self, evt):
        "halve regelafstand instellen"
        self.set_linespacing(15)

    def set_linespacing_20(self, evt):
        "dubbele regelafstand instellen"
        self.set_linespacing(20)

    def set_linespacing(self, value):
        "stel een gegeven regelafstand in"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.GetInsertionPoint()
        if self.GetStyle(ip, attr):
            range = rt.RichTextRange(ip, ip)
            if self.HasSelection():
                range = self.GetSelectionRange()
            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(value)
            self.SetStyle(range, attr)

    def text_font(self, evt):
        "lettertype en/of grootte instellen"
        font = evt.GetFont()
        attr = rt.RichTextAttr()
        if font:
            if not self.HasSelection():
                # attr.SetFlags(wx.TEXT_ATTR_FONT)
                # attr.SetFont(font)
                # self.SetStyle(self.GetInsertionPoint(), attr)
                self.BeginFont(font)
            else:
                range = self.GetSelectionRange()
                attr.SetFlags(wx.TEXT_ATTR_FONT)
                attr.SetFont(font)
                self.SetStyle(range, attr)
        self.SetFocus()

    def enlarge_text(self, evt):
        "letters groter maken"  # TODO

    def shrink_text(self, evt):
        "letters kleiner maken"  # TODO

    def select_text_color(self, evt):
        "tekstkleur instellen"
        colour = evt.GetEventObject().GetValue()
        if colour:
            self.applyfgcolour(colour)
            self.parent_.textcolour = colour
            self.parent_.changebitmapbuttoncolour(self.parent_.fgcset, colour)
        self.SetFocus()

    def set_text_color(self, evt):
        "tekstkleur instellen"
        self.applyfgcolour(self.parent_.textcolour)
        self.SetFocus()

    def applyfgcolour(self, colour):
        "colorize selected text"
        if not self.HasSelection():
            self.BeginTextColour(colour)
        else:
            range = self.GetSelectionRange()
            attr = rt.RichTextAttr()
            attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
            attr.SetTextColour(colour)
            self.SetStyle(range, attr)

    def select_background_color(self, evt):
        "achtergrondkleur voor tekst instellen"
        colour = evt.GetEventObject().GetValue()
        if colour:
            self.applybgcolour(colour)
            self.parent_.backgroundcolour = colour
            self.parent_.changebitmapbuttoncolour(self.parent_.bgcset, colour)
        self.SetFocus()

    def set_background_color(self, evt):
        "achtergrondkleur instellen"
        self.applybgcolour(self.parent_.backgroundcolour)
        self.SetFocus()

    def applybgcolour(self, colour):
        "colorize background of selected text"
        attr = rt.RichTextAttr()
        attr.SetFlags(wx.TEXT_ATTR_BACKGROUND_COLOUR)
        attr.SetBackgroundColour(colour)
        if not self.HasSelection():
            self.BeginStyle(attr)  # BeginBackgroundColour(colour)
        else:
            range = self.GetSelectionRange()
            self.SetStyle(range, attr)

    # def update_bold(self, evt):
    #     "het betreffende menuitem aanvinken indien van toepassing"
    #     evt.Check(self.IsSelectionBold())

    # def update_italic(self, evt):
    #     "het betreffende menuitem aanvinken indien van toepassing"
    #     evt.Check(self.IsSelectionItalics())

    # def update_underline(self, evt):
    #     "het betreffende menuitem aanvinken indien van toepassing"
    #     evt.Check(self.IsSelectionUnderlined())

    # def update_strikethrough(self, evt):
    #     "het betreffende menuitem aanvinken indien van toepassing"
    #     # evt.Check(self.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))
    #     # zal wel weer via de

    # def update_alignleft(self, evt):
    #     "het betreffende menuitem aanvinken indien van toepassing"
    #     evt.Check(self.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))

    # def update_center(self, evt):
    #     "het betreffende menuitem aanvinken indien van toepassing"
    #     evt.Check(self.IsSelectionAligned(wx.TEXT_ALIGNMENT_CENTRE))

    # def update_alignright(self, evt):
    #     "het betreffende menuitem aanvinken indien van toepassing"
    #     evt.Check(self.IsSelectionAligned(wx.TEXT_ALIGNMENT_RIGHT))

    def check_dirty(self):
        "mixin exit to check for modifications"
        return self.IsModified()

    def mark_dirty(self, value):
        "mixin exit to manually turn modified flag on/off (mainly intended for off)"
        self.SetModified(value)

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


class CheckDialog(wx.Dialog):
    """Generieke dialoog om iets te melden en te vragen of deze melding in het vervolg
    nog getoond moet worden

    Eventueel ook te implementeren m.b.v. wx.RichMessageDialog
    """
    def __init__(self, master, parent, title):
        # self.master = master
        # self.parent = parent
        wx.Dialog.__init__(self, parent, title=title, size=(-1, 120))
        self.SetIcon(parent.app_icon)
        # pnl = wx.Panel(self)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        # pnl.SetSizer(self.vsizer)
        # pnl.SetAutoLayout(True)
        # self.vsizer.Fit(pnl)
        # self.vsizer.SetSizeHints(pnl)
        # pnl.Layout()
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(True)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)
        self.Layout()

    def add_label(self, labeltext):
        """create a text on the screen
        """
        self.vsizer.Add(wx.StaticText(self, label=labeltext), 1, wx.ALL, 5)

    def add_checkbox(self, caption):
        """create a checkbox
        """
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        check = wx.CheckBox(self, label=caption)
        hsizer.Add(check, 0, wx.EXPAND)
        self.vsizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        return check

    def add_ok_buttonbox(self):
        """create a button strip with handlers
        """
        self.vsizer.Add(self.CreateButtonSizer(wx.OK), 0, wx.ALIGN_CENTER_HORIZONTAL)

    def get_checkbox_value(self, check):
        """return the value of a checkbox
        """
        return check.GetValue()


class OptionsDialog(wx.Dialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, master, parent, title):
        # self.master = master
        # self.parent = parent
        super().__init__(parent, title)
        # pnl = self  # wx.Panel(self, -1)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.gsizer = wx.FlexGridSizer(cols=2)
        self.vsizer.Add(self.gsizer, 0,
                        wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(True)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)
        self.Layout()

    def add_checkbox_line_to_grid(self, row, labeltext, value):
        """create a line to turn an option on/off
        """
        # FlexGridsizer heeft row / col niet nodig
        self.gsizer.Add(wx.StaticText(self, label=labeltext), 1, wx.ALL, 5)
        chk = wx.CheckBox(self)
        chk.SetValue(value)
        self.gsizer.Add(chk, 1, wx.ALL, 5)
        return chk

    def add_buttonbox(self, okvalue, cancelvalue):
        """create a button strip with handlers
        """
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, id=wx.ID_OK, label=okvalue)
        hsizer.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        # self.SetAffirmativeId(wx.ID_APPLY)
        btn = wx.Button(self, id=wx.ID_CLOSE, label=cancelvalue)
        hsizer.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.SetEscapeId(wx.ID_CLOSE)
        # sizer1 = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        self.vsizer.Add(hsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

    def get_checkbox_value(self, check):
        """return the value of a checkbox
        """
        return check.GetValue()


class SearchDialog(wx.Dialog):
    """search mode: 0 = current document, 1 = all titles, 2 = all texts
    """
    def __init__(self, master, parent):
        # self.master = master
        # self.parent = parent
        super().__init__(parent, "Search Results")
        self.SetIcon(parent.app_icon)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(True)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)
        self.Layout()

    def add_label(self, text):
        "zet een vaste tekst op het scherm"
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label=text))
        self.vsizer.Add(hsizer)

    def add_textentry(self):
        "zet een tekstinvoer veld op het scherm"
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        edit = wx.TextCtrl(self)
        hsizer.Add(edit)
        self.vsizer.Add(hsizer)
        return edit

    def build_search_selector(self, searchdefs, callback):
        "zet een selector voor zoeklocatie op het scherm"
        checks = []
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddStretchSpacer()
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        vsizer2.AddSpacer(3)
        vsizer2.Add(wx.StaticText(self, label='In: '))
        vsizer2.AddStretchSpacer()
        hsizer.Add(vsizer2)
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        for text in searchdefs:
            check = wx.CheckBox(text, self)
            check.Bind(wx.EVT_CHECKBOX, callback)
            checks.append(check)
            vsizer2.Add(check)
        hsizer.Add(vsizer2)
        hsizer.AddStretchSpacer()
        self.vsizer.Add(hsizer)
        return checks

    def build_options_selector(self, optiondefs):
        "zet een selector voor zoekmethode op het schem"
        checks = []
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        for text in optiondefs:
            check = wx.CheckBox(text, self)
            checks.append(check)
            vsizer2.Add(check)
        hsizer.Add(vsizer2)
        hsizer.AddStretchSpacer()
        self.vsizer.Add(hsizer)
        return checks

    def add_vertical_space(self, height):
        "voeg verticale witruimte toe"
        self.vsizer.AddSpacer(height)

    def add_checkbox(self, text):
        "voeg een checkbox toe aan het scherm"
        check = wx.CheckBox(text, self)
        self.vsizer.Add(check)
        return check

    def add_buttons(self):
        "voeg actie knoppen toe aan het scherm"
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddStretchSpacer()
        # ok_button = wx.Button(self, label="&Ok")
        # ok_button.Bind(wx.EVT_BUTTON, self.accept)
        # hsizer.Add(ok_button)
        btn = wx.Button(self, id=wx.ID_OK, label="&Ok")
        hsizer.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        # cancel_button = wx.Button(self, label="&Cancel")
        # cancel_button.Bind(wx.EVT_BUTTON, self.reject)
        # hsizer.Add(cancel_button)
        btn = wx.Button(self, id=wx.ID_CLOSE, label="&Cancel")
        hsizer.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.SetEscapeId(wx.ID_CLOSE)
        hsizer.AddStretchSpacer()
        self.vsizer.Add(hsizer)

    def set_checkbox_value(self, cb, value):
        "stel de waarde van een selector in"
        cb.SetValue(value)

    def set_textentry_value(self, text, value):
        "stel de waarde van de tekstinvoer in"
        text.SetValue(value)

    # def case_sensitive_search(self):
    #     return gui.QTextDocument.FindFlag.FindCaseSensitively.value
    # def search_for_whole_words(self):
    #     return gui.QTextDocument.FindFlag.FindWholeWords.value

    def set_focus_to(self, widget):
        "geef de focus aan een gegeven widget"
        widget.SetFocus()

    def set_modechecks(self):
        """stel checkboxen in afhankelijk van gekozen zoekmanier

        bij aanzetten current:
            titel en text uitzetten
            lijst en search backwards deactiveren
        bij aanzetten titel of text:
            current uitzetten
            lijst en search backwards activeren
        """

    def get_checkbox_value(self, cb):
        "geef de waarde van een gegeven selector terug"
        return cb.IsChecked()

    def get_textentry_value(self, text):
        "geeft de waarde van een gegeven tekstinvoer veld terug"
        return text.GetValue()

    # def update_searchflags(self, hlett, woord):
    #     # trucje om `flags` op een valide waarde te initialiseren
    #     flags = gui.QTextDocument.FindFlag.FindBackward & ~gui.QTextDocument.FindFlag.FindBackward
    #     if self.get_checkbox_value(hlett):
    #         flags |= gui.QTextDocument.FindFlag.FindCaseSensitively
    #     if self.get_checkbox_value(woord):
    #         flags |= gui.QTextDocument.FindFlag.FindWholeWords
    #     return flags


class ResultsDialog(wx.Dialog):
    "Present search results in a non-modal dialog"
    def __init__(self, master, parent):
        self.master = master
        # self.parent = parent
        super().__init__(parent, title="Search Results")
        self.SetIcon(parent.app_icon)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(True)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)
        self.Layout(self.vsizer)

    def set_toptext(self, text):
        "zet toelichting op scherm"
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label="text"))
        self.vsizer.Add(hsizer)

    def add_results_list(self, labels, callback):
        "voeg de resultatenlijst toe aan het scherm"
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        listbox = MyListCtrl(self, style=wx.LC_REPORT)
        for ix, caption in enumerate(labels):
            listbox.InsertColumn(ix, caption)
            # listbox.SetColumnWidth(ix, ...)
        # listbox.resizeLastColumn(...)
        listbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, callback)
        # self.populate_list()
        hsizer.Add(listbox, 1, wx.EXPAND | wx.ALL, 5)
        self.vsizer.Add(hsizer)
        return listbox

    def add_buttons(self, buttondefs):
        "voeg actie knoppen toe aan het scherm"
        buttons = []
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddStretchSpacer()
        for text, callback in buttondefs:
            button = wx.Button(text, self)
            button.Bind(wx.EVT_BUTTON, callback)
            hsizer.Add(button)
            buttons.append(button)
        hsizer.AddStretchSpacer()
        self.vsizer.Add(hsizer)
        return buttons

    def add_item_to_list(self, listbox, loc, root, title):
        "item opbouwen"
        new = listbox.InsertItem(sys.maxsize, root)
        listbox.SetItem(new, 0, root)
        listbox.SetItem(new, 1, title)
        listbox.SetItemData(new, loc)

    def get_next_item(self, listbox):
        "geef volgende zoekresultaat uit lijst terug"
        result = listbox.GetNextItem(wx.LIST_NEXT_BELOW)
        return None if result == -1 else result

    def get_prev_item(self, listbox):
        "geef voorgaande zoekresultaat uit lijst terug"
        result = listbox.GetNextItem(wx.LIST_NEXT_ABOVE)
        return None if result == -1 else result

    def getselection(self, listbox):
        "geef het geselecteerd item terug"
        return listbox.GetFirstSelected()

    def setselection(self, listbox, item):
        "stel het te selecteren item in"
        listbox.Select(item)

    def disable_widget(self, widget):
        "maak interactie met een wisget onmogelijk"
        widget.Enable(False)

    def enable_button_if_disabled(self, button):
        "maak een onbruikbare knop bruikbaar"
        if not button.IsEnabled():
            button.Enable(True)

    def get_item_data(self, listbox, item):
        "geef de bij een item geassocieerde data terug"
        return listbox.GetItemData(item)


class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    "ListCtrl met mixin voor automatische kolom uitvulling"
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, pos=pos, size=size, style=style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class TaskbarIcon(wx.adv.TaskBarIcon):
    "icon in the taskbar"
    id_revive = wx.ID_ANY
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
