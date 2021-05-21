import os.path
import subprocess
import platform
from pubsub import pub


def get_install_folder_and_version():
    # only Windows has the winreg package, so make sure the script doesn't go apeshit in other systems
    if platform.system() == "Windows":
        import winreg
        print("Attempting to find Windows install...")

        access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        openrct2_key_location = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\OpenRCT2"

        try:
            access_key = winreg.OpenKey(access_registry, openrct2_key_location)
        except FileNotFoundError:
            print("OpenRCT2 installation not found")
            return None, None

        install_location = winreg.QueryValueEx(access_key, "Install Folder")[0]
        version = winreg.QueryValueEx(access_key, "DisplayVersion")[0]

        return install_location, version


def do_silent_install(temp_dir, installer_path):
    print("Installing for Windows...")
    command = f"\"{os.path.join(temp_dir, installer_path)}\" /S"

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

    print("Finished installation successfully")
    pub.sendMessage("statusChanged", new_text="Finished installing")
