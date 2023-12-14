"""DocTree: toolkit-agnostic subroutines
"""
import os
import pathlib
import logging
import bs4 as bs

HERE = pathlib.Path(__file__).parent.resolve()
FILE_TYPE = ('Doctree File', '.trd')
HIDE_TEXT = ("DocTree gaat nu slapen in de System tray\n"
             "Er komt een icoontje waarop je kunt klikken om hem weer wakker te maken")
LOGFILE = pathlib.Path('/tmp') / 'logs' / 'doctree.log'
WANT_LOGGING = 'DEBUG' in os.environ and os.environ['DEBUG'] != "0"
if WANT_LOGGING:
    LOGFILE.parent.mkdir(exist_ok=True)
    LOGFILE.touch(exist_ok=True)
    logging.basicConfig(filename=str(LOGFILE),
                        level=logging.DEBUG, format='%(asctime)s %(message)s')


def log(message, always=False):
    "write message to logfile"
    if WANT_LOGGING or always:
        logging.info(message)
    if always:
        print(message)


def getsubtree(tree, item, itemlist=None):
    """recursieve functie om de structuur onder de te verplaatsen data
    te onthouden"""
    if itemlist is None:
        itemlist = []
    titel, key = tree.getitemdata(item)
    itemlist.append(key)
    log(f' getsubtree item {titel}, {key}')
    subtree = []
    for kid in tree.getitemkids(item):
        data, itemlist = getsubtree(tree, kid, itemlist)
        subtree.append(data)
    return (titel, key, subtree), itemlist


def putsubtree(tree, parent, titel, key, subtree=None, pos=-1):
    """recursieve functie om de onthouden structuur terug te zetten"""
    log(f'in shared.putsubtree met {parent=}, {titel=}, {key=} of type {type(key)}')
    if subtree is None:
        subtree = []
    new = tree.add_to_parent(key, str(titel), parent, pos)
    for subtitel, subkey, subsubtree in subtree:
        putsubtree(tree, new, subtitel, subkey, subsubtree)
    return new


def get_imagenames(data):
    "analyze text for names of image files"
    return [img['src'] for img in bs.BeautifulSoup(data, 'lxml').find_all('img')]


def get_setttexts():
    """returns texts associated with the message dialogs that can be hidden
    """
    return {'AskBeforeHide': 'Notify that the application will be hidden in the system tray',
            'NotifyOnLoad': 'Notify that the data has been reloaded',
            'NotifyOnSave': 'Notify that the data has been saved',
            'EscapeClosesApp': 'Application can be closed by pressing Escape'}
