"""DocTree: relay imports from actual gui module
"""
from .toolkit import toolkit
if toolkit == 'qt':
    from .qtgui import show_message, ask_ynquestion, ask_yncquestion, get_text, get_filename, \
                       show_dialog, show_nonmodal, CheckDialog, OptionsDialog, SearchDialog, \
                       ResultsDialog, MainGui
elif toolkit == 'wx':
    from .wxgui import show_message, ask_ynquestion, ask_yncquestion, get_text, get_filename, \
                       show_dialog, show_nonmodal, CheckDialog, OptionsDialog, SearchDialog, \
                       ResultsDialog, MainGui
# elif toolkit == 'no':
#     from .nogui import show_message, ask_question, MainGui
else:
    raise ValueError('Unsupported GUI toolkit')
