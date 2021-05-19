import os
import platform
import sys


def get_current_platform(true_platform=False):
    """ Gets the current OS running the script. If true_platform is set to True, it ignores -force CLI args. """
    if true_platform:
        return platform.system()

    if sys.argv.__contains__("-forceWindows"):
        return "Windows"
    elif sys.argv.__contains__("-forceLinux"):
        return "Linux"
    elif sys.argv.__contains__("-forceMacOS"):
        return "Darwin"
    else:
        return platform.system()


# from https://stackoverflow.com/a/13790741/8286014
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
