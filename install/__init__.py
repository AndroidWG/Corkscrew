import platform
from pubsub import pub
from install import windows, macos


def install_or_update_openrct2(temp_dir, installer_file):
    current_platform = platform.system()
    pub.sendMessage("updateSysTray", text="Installing...")

    # TODO: remove current installation if it exists

    if current_platform == "Windows":
        windows.do_silent_install(temp_dir, installer_file)
    elif current_platform == "Darwin":
        macos.copy_to_applications(temp_dir, installer_file)


def check_openrct2_install():
    current_platform = platform.system()
    pub.sendMessage("updateSysTray", text="Checking OpenRCT2 Install...")

    if current_platform == "Windows":
        return windows.get_install_folder_and_version()
    if current_platform == "Linux":
        return None  # TODO: Add Linux check_install function
    elif current_platform == "Darwin":
        return None  # TODO: Add macOS check_install function
