import pytest

create_checkdialog = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('DocTree',)
called Dialog.setWindowIcon with args ('Icon',)
called Label.__init__ with args ('{message}', {testobj})
called CheckBox.__init__ with text 'Deze melding niet meer laten zien'
called PushButton.__init__ with args ('&Ok', {testobj}) {{}}
called Signal.connect with args ({testobj.klaar},)
called VBox.__init__
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.insertStretch
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
create_optionsdialog = """\
called shared.get_setttexts
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('A Propos Settings',)
called VBox.__init__
called Grid.__init__
called Label.__init__ with args ('xxxxxxxxxxxxxx', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 0)
called CheckBox.__init__ with text ''
called CheckBox.setChecked with arg True
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'> at (1, 1)
called Label.__init__ with args ('yyyyyyyyyyyyyyy', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (2, 0)
called CheckBox.__init__ with text ''
called CheckBox.setChecked with arg False
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'> at (2, 1)
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Apply', {testobj}) {{}}
called Signal.connect with args ({testobj.accept},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Close', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
create_searchdialog = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('Title',)
called Dialog.setWindowIcon with args ('Icon',)
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('Zoek naar: ', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called LineEdit.__init__
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called CheckBox.__init__ with text 'Alle titels'
called Signal.connect with args ({testobj.check_modes},)
called CheckBox.__init__ with text 'Alle teksten'
called Signal.connect with args ({testobj.check_modes},)
called CheckBox.__init__ with text 'Alleen huidige tekst'
called Signal.connect with args ({testobj.check_modes},)
called HBox.__init__
called HBox.addStretch
called VBox.__init__
called VBox.addSpacing
called Label.__init__ with args ('In: ', {testobj})
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addStretch
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called VBox.__init__
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called CheckBox.__init__ with text 'Hoofdlettergevoelig'
called CheckBox.__init__ with text 'Hele woorden'
called VBox.__init__
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called VBox.addSpacing
called HBox.__init__
called CheckBox.__init__ with text 'Wrap around'
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called CheckBox.__init__ with text 'Toon lijst met zoekresultaten'
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Ok', {testobj}) {{}}
called Signal.connect with args ({testobj.accept},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
called CheckBox.setChecked with arg True
"""
search_middle = """\
called LineEdit.setText with arg `Find`
called CheckBox.setChecked with arg True
called CheckBox.setChecked with arg True
"""
search_middle2 = """\
called CheckBox.setChecked with arg True
called CheckBox.setChecked with arg True
"""
search_end = """\
called LineEdit.setFocus
"""
create_resultsdialog = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('Search Results',)
called Dialog.setWindowIcon with args ('Icon',)
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('Showing results of searching for `Find` in all {where}\\nDoubleclick to go to an entry', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called Tree.__init__
called Tree.setColumnCount with arg `2`
called Tree.setHeaderLabels with arg `('Node Root', 'Node Title')`
called Signal.connect with args ({testobj.goto_selected},)
called ResultsDialog.populate_list
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockTreeWidget'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called PushButton.__init__ with args ('&Goto', {testobj}) {{}}
called Signal.connect with args ({testobj.goto_selected},)
called PushButton.__init__ with args ('g&Oto and Close', {testobj}) {{}}
called Signal.connect with args ({testobj.goto_and_close},)
called PushButton.__init__ with args ('Goto &Next', {testobj}) {{}}
called Signal.connect with args ({testobj.goto_next},)
called PushButton.__init__ with args ('Goto &Previous', {testobj}) {{}}
called Signal.connect with args ({testobj.goto_prev},)
called PushButton.setEnabled with arg `False`
called PushButton.__init__ with args ('&Close', {testobj}) {{}}
called Signal.connect with args ({testobj.accept},)
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
called Tree.itemAt with args (0, 0)
called Tree.setCurrentItem with arg `item at (0, 0)`
"""
main_gui = """\
called Application.__init__
called Action.__init__ with args ()
called Action.__init__ with args ()
called MenuBar.__init__
called MainWindow.move with args (10, 10)
called Icon.__init__ with arg of type <class 'str'>
called Application.setWindowIcon
called TrayIcon.__init__
called TrayIcon.setToolTip with args ('Click to revive DocTree',)
called Signal.connect with args ({testobj.revive},)
called TrayIcon.hide
called MainWindow.statusBar
called StatusBar.__init__ with args ()
called StatusBar.showMessage with arg `Ready`
called MainWindow.resize with args (1, 2)
called MainWindow.setWindowTitle with arg `title`
called MainWindow.menuBar
called Splitter.__init__
called MainWidget.setCentralWindow with arg of type `<class 'mockgui.mockqtwidgets.MockSplitter'>`
called TreePanel.__init__ with args ({testobj},)
called Splitter.addWidget with arg of type <class 'test_qtgui.MockTree'>
called Editor.setReadOnly with arg True
called Splitter.addWidget with arg of type <class 'test_qtgui.MockEditor'>
called MainGui.get_menu_data
called MainGui.create_menu with args ({menubar}, 'menudata')
called gui.UndoRedoStack.__init__ with arg {testobj}
called MainGui.create_styletoolbar
called Pixmap.__init__
called Pixmap.fill with arg 'color 1'
called Icon.__init__ with arg of type <class 'mockgui.mockqtwidgets.MockPixmap'>
called Action.setIcon
called Pixmap.__init__
called Pixmap.fill with arg 'color 2'
called Icon.__init__ with arg of type <class 'mockgui.mockqtwidgets.MockPixmap'>
called Action.setIcon
"""
main_menu = """\
called MenuBar.addMenu with arg  aaa
called Menu.__init__ with args ('aaa',)
called Icon.__init__ with arg `{testobj.master.HERE}/aaa.ico`
called Action.__init__ with args ('item of type Icon', 'aaaa', {testobj})
called MainGui.addToolBar with arg aaa
called Size.__init__ with args (16, 16)
called ToolBar.setIconSize
called ToolBar.addAction
called Signal.connect with args ({callbacks[0]},)
called Menu.addAction
called Icon.__init__ with arg `{testobj.master.HERE}/exit.ico`
called Action.__init__ with args ('item of type Icon', 'exit', {testobj})
called ToolBar.addAction
called Action.setShortcuts with arg `['Ctrl+X', 'Esc']`
called Signal.connect with args ({callbacks[1]},)
called Menu.addAction
called MenuBar.addMenu with arg  xxx
called Menu.__init__ with args ('xxx',)
called MenuBar.addMenu with arg  yyy
called Menu.__init__ with args ('yyy',)
called Action.__init__ with args ('B', {testobj})
called Font.__init__
called Font.setBold with arg `True`
called Action.setFont
called Signal.connect with args ({callbacks[2]},)
called Menu.addAction
called Action.__init__ with args ('I', {testobj})
called Font.__init__
called Font.setItalic with arg `True`
called Action.setFont
called Signal.connect with args ({callbacks[3]},)
called Menu.addAction
called Action.__init__ with args ('U', {testobj})
called Font.__init__
called Font.setUnderline with arg `True`
called Action.setFont
called Signal.connect with args ({callbacks[4]},)
called Menu.addAction
called Action.__init__ with args ('S', {testobj})
called Font.__init__
called Font.setStrikeOut with arg `True`
called Action.setFont
called Signal.connect with args ({callbacks[5]},)
called Menu.addAction
called Action.__init__ with args ('M', {testobj})
called Font.__init__
called Font.setFixedPitch with arg `True`
called Action.setFont
called Signal.connect with args ({callbacks[11]},)
called Menu.addAction
called Menu.addSeparator
called Action.__init__ with args ('-----', None)
called Action.__init__ with args ('X', {testobj})
called Signal.connect with args ({callbacks[6]},)
called Menu.addAction
called Menu.addSeparator
called Action.__init__ with args ('-----', None)
called MenuBar.addMenu with arg  zzz
called Menu.__init__ with args ('zzz',)
called Action.__init__ with args ('&Undo', {testobj})
called Action.setShortcuts with arg `['Ctrl+Z']`
called Signal.connect with args ({callbacks[7]},)
called Menu.addAction
called Action.__init__ with args ('&Redo', {testobj})
called Action.setShortcuts with arg `['Ctrl+Y']`
called Signal.connect with args ({callbacks[8]},)
called Menu.addAction
called Action.__init__ with args ('', {testobj})
called Signal.connect with args ({callbacks[0]},)
called MenuBar.addMenu with arg  bbb
called Menu.__init__ with args ('bbb',)
called Action.__init__ with args ('bbbb', {testobj})
called Signal.connect with args ({callbacks[9]},)
called Menu.addAction
called MenuBar.addMenu with arg  ccc
called Menu.__init__ with args ('ccc',)
called Action.__init__ with args ('cccc', {testobj})
called Signal.connect with args ({callbacks[10]},)
called Menu.addAction
"""
dummy = """\
called ComboBox.__init__
called ToolBar.addWidget with arg {testobj.combo_font}
called Signal.connect with args ({testobj.editor.text_family},)
called ComboBox.__init__
called ToolBar.addWidget with arg {testobj.combo_size}
called ComboBox.setEditable with arg `True`
called ComboBox.addItem with arg `10`
called ComboBox.addItem with arg `12`
called ComboBox.addItem with arg `20`
called Signal.connect with args ({testobj.editor.text_size},)
called Font.__init__
called Font.pointSize
called ComboBox.findText with args ('fontsize',)
called ComboBox.setCurrentIndex with arg `1`
"""
main_toolbar = """\
called MainGui.addToolBar with arg styles
called Pixmap.__init__
called Pixmap.fill with arg {testobj.setcoloraction_color}
called Icon.__init__ with arg of type <class 'mockgui.mockqtwidgets.MockPixmap'>
called Action.__init__ with args ('item of type Icon', 'Change text color', {testobj})
called Signal.connect with args ({testobj.editor.select_text_color},)
called ToolBar.addAction
called Pixmap.__init__
called Pixmap.fill with arg {testobj.setcoloraction_color}
called Icon.__init__ with arg of type <class 'mockgui.mockqtwidgets.MockPixmap'>
called Action.__init__ with args ('item of type Icon', 'Set text color', {testobj})
called Signal.connect with args ({testobj.editor.set_text_color},)
called ToolBar.addAction
called Pixmap.__init__
called Pixmap.fill with arg {testobj.setbackgroundcoloraction_color}
called Icon.__init__ with arg of type <class 'mockgui.mockqtwidgets.MockPixmap'>
called Action.__init__ with args ('item of type Icon', 'Change background color', {testobj})
called Signal.connect with args ({testobj.editor.select_background_color},)
called ToolBar.addAction
called Pixmap.__init__
called Pixmap.fill with arg {testobj.setbackgroundcoloraction_color}
called Icon.__init__ with arg of type <class 'mockgui.mockqtwidgets.MockPixmap'>
called Action.__init__ with args ('item of type Icon', 'Set background color', {testobj})
called Signal.connect with args ({testobj.editor.set_background_color},)
called ToolBar.addAction
"""

@pytest.fixture
def expected_output():
    return {'checkdialog': create_checkdialog, 'optionsdialog': create_optionsdialog,
            'searchdialog': create_searchdialog + search_end,
            'searchdialog1': create_searchdialog + search_middle + search_end,
            'searchdialog2': create_searchdialog + search_middle + search_middle2 + search_end,
            'resultsdialog': create_resultsdialog, 'maingui': main_gui, 'menu': main_menu,
            'toolbar': main_toolbar
            }
