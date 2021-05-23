import platform
import shutil
import tempfile
import os
import github
import logging
from packaging import version
from pubsub import pub


# This file coordinates execution from the install and github packages. Should be
# called in a different thread to not lock UI thread
class InstallHandler:
    def __init__(self):
        self.__latest_release = github.get_latest_release()
        self.__installer_url, self.__installer_path = github.get_asset_url_and_name(self.__latest_release)
        self.mac_app_path = "/Applications/OpenRCT2.app"
        
        self.current_platform = platform.system()
        self.is_latest_installed = self.check_if_latest_is_installed()

    def check_if_latest_is_installed(self):
        global install_info
        from install import windows, macos
        pub.sendMessage("updateSysTray", text="Checking OpenRCT2 Install...")

        if self.current_platform == "Windows":
            install_info = windows.get_install_folder_and_version()
        elif self.current_platform == "Darwin":
            install_info = macos.get_app_version(self.mac_app_path)

        try:
            installed = version.parse(install_info[1])
        except TypeError:
            # If check_openrct2_install returns null, the "[1]" thing will throw this exception
            # meaning an installation was not found
            return False

        latest = version.parse(github.get_latest_version(self.__latest_release))

        if latest >= installed:
            return True
        else:
            return False

    def update_openrct2(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            logging.info(f"Created temp dir at {temp_dir}")

            # Download ----------------
            if self.__installer_url is None or self.__installer_path is None:
                return
            else:
                github.download_asset(temp_dir, self.__installer_url, self.__installer_path)

            # Install -----------------
            from install import windows, macos
            pub.sendMessage("updateSysTray", text="Installing...")

            # TODO: remove current installation if it exists

            if self.current_platform == "Windows":
                windows.do_silent_install(temp_dir, self.__installer_path)
            elif self.current_platform == "Darwin":
                if os.path.exists(self.mac_app_path):
                    shutil.rmtree(self.mac_app_path)
                    logging.info("Removed old installation")
                
                macos.copy_to_applications(temp_dir, self.__installer_path)

            pub.sendMessage("updateSysTray", text="Finished installing")
