import util
from check_install import windows


def check_openrct2_install():
    current_platform = util.get_current_platform()
    if current_platform == "Windows":
        return windows.get_install_folder_and_version()
    if current_platform == "Linux":
        return None  # TODO: Add Linux check_install module
    elif current_platform == "Darwin":
        return None  # TODO: Add macOS check_install module
