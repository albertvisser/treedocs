"""DocTree: logging utilities
"""
import os
import pathlib
import logging

LOGFILE = pathlib.Path('/tmp') / 'logs' / 'doctree.log'
WANT_LOGGING = 'DEBUG' in os.environ and os.environ['DEBUG'] != "0"


def log(message, always=False):
    "write message to logfile"
    if WANT_LOGGING or always:
        if not LOGFILE.exists():
            LOGFILE.parent.mkdir(exist_ok=True)
            LOGFILE.touch(exist_ok=True)
            logging.basicConfig(filename=str(LOGFILE), level=logging.DEBUG,
                                format='%(asctime)s %(message)s')
        logging.info(message)
    if always:
        print(message)
