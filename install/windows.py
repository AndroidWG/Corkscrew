import logging
import os.path
import subprocess
import platform


def get_install_folder_and_version() -> tuple[any, any]:
    """Gets the version and install path of OpenRCT2 from the Windows Registry.

    :return: Tuple with installation path an version string respectively. If an installation is not found, a tuple of None and None are returned.
    :rtype: tuple
    """
    # Only Windows has the winreg package, so make sure the script doesn't go apeshit in other systems
    if platform.system() == "Windows":
        import winreg
        logging.info("Attempting to find Windows install...")

        access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        openrct2_key_location = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\OpenRCT2"

        try:
            access_key = winreg.OpenKey(access_registry, openrct2_key_location)
        except FileNotFoundError:
            logging.warning("OpenRCT2 installation not found")
            return None, None

        install_location = winreg.QueryValueEx(access_key, "Install Folder")[0]
        version = winreg.QueryValueEx(access_key, "DisplayVersion")[0]

        logging.debug(f"Found install info - install location: {install_location}\ninstall version:{version}")

        return install_location, version


def do_silent_install(temp_dir: str, installer_path: str):
    """Runs a NSIS-based installer in silent mode under a subprocess and waits for it to finish.

    :param temp_dir: Temporary directory to be used
    :type temp_dir: str
    :param installer_path: Path where the .zip containing the .app folder is located
    :type installer_path: str
    """
    logging.info("Installing for Windows...")

    command = f"\"{os.path.join(temp_dir, installer_path)}\" /S"
    logging.debug(f"Running command: {command}")
    process = subprocess.Popen(command, shell=True)
    process.wait()

    logging.info("Finished installation successfully")
