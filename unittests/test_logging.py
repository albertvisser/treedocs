"""unittests for ./doctree/shared.py
"""
import doctree.do_logging as testee


def test_log(monkeypatch, capsys, tmp_path):
    """unittest for shared.log
    """
    def mock_info(message):
        """stub
        """
        print(f'called logging.info with arg `{message}`')
    def mock_config(**kwargs):
        print('called logging.basicConfig with args', kwargs)
    monkeypatch.setattr(testee, 'LOGFILE', tmp_path / 'logs' / 'doctree.log')
    monkeypatch.setattr(testee.logging, 'basicConfig', mock_config)
    monkeypatch.setattr(testee.logging, 'info', mock_info)

    monkeypatch.setattr(testee, 'WANT_LOGGING', False)
    testee.log('information')
    assert not testee.LOGFILE.exists()
    assert not testee.LOGFILE.parent.exists()
    assert capsys.readouterr().out == ''
    testee.log('information', always=True)
    assert testee.LOGFILE.parent.exists()
    assert testee.LOGFILE.exists()
    assert capsys.readouterr().out == (
            f"called logging.basicConfig with args {{'filename': '{testee.LOGFILE}',"
            " 'level': 10, 'format': '%(asctime)s %(message)s'}\n"
            'called logging.info with arg `information`\n'
            'information\n')
    testee.LOGFILE.unlink()
    testee.LOGFILE.parent.rmdir()
    monkeypatch.setattr(testee, 'WANT_LOGGING', True)
    testee.log('information')
    assert testee.LOGFILE.parent.exists()
    assert testee.LOGFILE.exists()
    assert capsys.readouterr().out == (
            f"called logging.basicConfig with args {{'filename': '{testee.LOGFILE}',"
            " 'level': 10, 'format': '%(asctime)s %(message)s'}\n"
            'called logging.info with arg `information`\n')

    testee.log('information', always=True)
    assert testee.LOGFILE.parent.exists()
    assert testee.LOGFILE.exists()
    assert capsys.readouterr().out == ('called logging.info with arg `information`\n'
                                       'information\n')
