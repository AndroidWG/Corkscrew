import winreg


def find_openrct2_install_folder():
    print("Attempting to find Windows install")

    access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    openrct2_key_location = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\OpenRCT2"

    try:
        access_key = winreg.OpenKey(access_registry, openrct2_key_location)
    except FileNotFoundError:
        print("OpenRCT2 installation not found.")
        return None

    install_location = winreg.QueryValueEx(access_key, "Install Folder")
    print(install_location[0])
