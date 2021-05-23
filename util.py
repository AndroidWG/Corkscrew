import os
import sys


# CLI Progress Bar yoinked from https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a#file-print_progress-py
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    # TODO: add auto width using os.get_terminal_size()
    # TODO: change docstring to reStructured Text

    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    ready_to_print = ('%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix))

    print(ready_to_print, end="\r", flush=True)

    if iteration == total:
        print('\n')


# From https://stackoverflow.com/a/13790741/8286014
def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    @params:
        relative_path  - Required  : relative path to file (Str)
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
