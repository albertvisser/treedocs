"""unittests for ./doctree/shared.py
"""
import doctree.shared as testee


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


def _test_getsubtree(monkeypatch, capsys):
    """unittest for shared.getsubtree
    """
    testee.getsubtree(tree, item, itemlist=None)


def _test_putsubtree(monkeypatch, capsys):
    """unittest for shared.putsubtree
    """
    testee.putsubtree(tree, parent, titel, key, subtree=None, pos=-1)


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
