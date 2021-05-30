import platform
import sys
import tempfile
import os
import github
import logging
import github.requests
import util
from packaging import version
from install import windows, macos


# This file coordinates execution from the install and github packages. Should be
# called in a different thread to not lock UI thread
# noinspection PyProtectedMember
class InstallHandler:
    def __init__(self):
        self.__latest_release = github.requests.try_to_get_request(github.get_latest_release, "latest release")
        if self.__latest_release is None:
            sys.exit(2)

        try:
            self.__installer_url, self.__installer_path = github.get_asset_url_and_name(self.__latest_release)
        except KeyError as e:
            logging.error("Key not found while getting asset URLs and names. Exiting...", exc_info=e)
            sys.exit(2)
        except ValueError as e:
            logging.error("Unable to find filename or URL in latest release. Exiting...", exc_info=e)
            sys.exit(2)

        self.__mac_app_path = "/Applications/OpenRCT2.app"

        self.current_platform = platform.system()
        if sys.argv.__contains__("--force-outdated") or sys.argv.__contains__("-F"):
            self.is_latest_installed = False
        else:
            try:
                self.is_latest_installed = self.check_if_latest_is_installed()
            except OSError as e:
                logging.error("Failed getting Windows Registry connection. "
                              "Latest installed will be set to False", exc_info=e)
                self.is_latest_installed = False
            except TypeError as e:
                logging.error("Type error while parsing version. "
                              "Latest installed will be set to False", exc_info=e)
                self.is_latest_installed = False

    def check_if_latest_is_installed(self):
        global install_info
        from install import windows, macos

        if self.current_platform == "Windows":
            install_info = windows.get_install_folder_and_version()
        elif self.current_platform == "Darwin":
            install_info = macos.get_app_version(self.__mac_app_path)

        try:
            installed = version.parse(install_info[1])
        except TypeError:
            # If check_openrct2_install returns null, the "[1]" thing will throw this exception
            # meaning an installation was not found
            return False

        latest = version.parse(github.get_version(self.__latest_release))
        logging.info(f"Latest version is {latest.__str__()} and installed version is {installed.__str__()}")

        if latest >= installed:
            return True
        else:
            return False

    def update_openrct2(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            logging.info(f"\nCreated temp dir at {temp_dir}")

            # Download ----------------
            func = github.download_asset
            result = github.requests.try_to_get_request(
                func,
                "latest release",
                temp_dir,
                self.__installer_url,
                self.__installer_path)
            if result is None:
                return

            # Install -----------------
            logging.debug(f"Preparing to install file {self.__installer_path}")

            if sys.argv.__contains__("--skip-install") or sys.argv.__contains__("-SI"):
                return

            try:
                util.is_open("openrct2", 20)
            except KeyboardInterrupt:
                logging.error("OpenRCT2 has been running for a long ass time, so we'll stop trying to update it "
                              "for now. Exiting...")
                return

            try:
                if self.current_platform == "Windows":
                    windows.do_silent_install(temp_dir, self.__installer_path)
                elif self.current_platform == "Darwin":
                    if os.path.exists(self.__mac_app_path):
                        import trash
                        trash.send_to_trash(self.__mac_app_path)
                        logging.debug("Removed old installation")

                    macos.copy_to_applications(temp_dir, self.__installer_path)
            except KeyboardInterrupt as e:
                logging.error(f"Install took too long to respond. Exiting...", exc_info=e)
                return

        logging.info("Finished installing OpenRCT2")
