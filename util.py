import platform
import sys


def get_current_platform(true_platform=False):
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
