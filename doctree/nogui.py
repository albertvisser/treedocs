"""DocTree: simple text interface stuff for now, could be turned into a curses ui
"""


def show_message(win, text):
    "show a confirmable message"
    print(text, end='\n\n')


def ask_question(win, text):
    "ask a yes/no answerable question"
    result = input(text + ' ([Y]es/[n]o)')
    if not result:
        return True
    return result[0].lower() != 'n'


class MainGui:
    "Primary application window (main screen): dummy version"
    def __init__(self):
        pass

    def go(self):
        "pretend starting the GUI"
