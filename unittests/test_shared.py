"""unittests for ./doctree/shared.py
"""
import doctree.shared as testee


class MockTree:
    "stub"
    def __init__(self):
        self.counter = 0
    def getitemdata(self, item):
        print(f"called Tree.getitemdata with arg '{item}'")
        return 'item title', 'item key'
    def getitemkids(self, item):
        print(f"called Tree.getitemkids with arg '{item}'")
        self.counter += 1
        if self.counter == 1:
            return ['kid1', 'kid2']
        return []
    def add_to_parent(self, *args):
        print(f"called Tree.add_to_parent with args", args)
        return 'new treeitem'

def test_log(monkeypatch, capsys):
    """unittest for shared.log
    """
    def mock_info(message):
        """stub
        """
        print(f'called logging.info with arg `{message}`')
    monkeypatch.setattr(testee.logging, 'info', mock_info)
    monkeypatch.setattr(testee, 'WANT_LOGGING', True)
    testee.log('information')
    assert capsys.readouterr().out == 'called logging.info with arg `information`\n'
    testee.log('information', always=True)
    assert capsys.readouterr().out == ('called logging.info with arg `information`\n'
                                       'information\n')
    monkeypatch.setattr(testee, 'WANT_LOGGING', False)
    testee.log('information')
    assert capsys.readouterr().out == ''
    testee.log('information', always=True)
    assert capsys.readouterr().out == ('called logging.info with arg `information`\n'
                                       'information\n')


def test_getsubtree(monkeypatch, capsys):
    """unittest for shared.getsubtree
    """
    tree = MockTree()
    assert testee.getsubtree(tree, 'item') == (
            ('item title', 'item key', [('item title', 'item key', []),
                                        ('item title', 'item key', [])]),
            ['item key', 'item key', 'item key'])
    assert capsys.readouterr().out == ("called Tree.getitemdata with arg 'item'\n"
                                       "called Tree.getitemkids with arg 'item'\n"
                                       "called Tree.getitemdata with arg 'kid1'\n"
                                       "called Tree.getitemkids with arg 'kid1'\n"
                                       "called Tree.getitemdata with arg 'kid2'\n"
                                       "called Tree.getitemkids with arg 'kid2'\n")


def test_putsubtree(monkeypatch, capsys):
    """unittest for shared.putsubtree
    """
    tree = MockTree()
    subtree = [('subtitle1', 'subkey1', []), ('subtitle2', 'subkey2', [])]
    assert testee.putsubtree(tree, 'parent', 'titel', 'key', subtree, pos=1) == 'new treeitem'
    assert capsys.readouterr().out == (
            "called Tree.add_to_parent with args ('key', 'titel', 'parent', 1)\n"
            "called Tree.add_to_parent with args ('subkey1', 'subtitle1', 'new treeitem', -1)\n"
            "called Tree.add_to_parent with args ('subkey2', 'subtitle2', 'new treeitem', -1)\n")
    assert testee.putsubtree(tree, 'parent', 'titel', 'key', pos=1) == 'new treeitem'
    assert capsys.readouterr().out == (
            "called Tree.add_to_parent with args ('key', 'titel', 'parent', 1)\n")


def test_get_imagenames(monkeypatch, capsys):
    """unittest for shared.get_imagenames
    """
    assert testee.get_imagenames('<div><img src="x.png"/><img src="y.png"/></div>') == ['x.png',
                                                                                        'y.png']


def test_get_setttexts(monkeypatch, capsys):
    """unittest for shared.get_setttexts
    """
    assert testee.get_setttexts() == {
            'AskBeforeHide': 'Notify that the application will be hidden in the system tray',
            'NotifyOnLoad': 'Notify that the data has been reloaded',
            'NotifyOnSave': 'Notify that the data has been saved',
            'EscapeClosesApp': 'Application can be closed by pressing Escape'}
