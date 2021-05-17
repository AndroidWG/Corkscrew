import os.path
import zipfile
import util
from distutils.dir_util import copy_tree


def copy_to_applications(temp_dir, installer_path):
    print("Installing for macOS")

    zip_path = os.path.join(temp_dir, installer_path)
    with zipfile.ZipFile(zip_path, "r") as downloaded_zip:
        downloaded_zip.extract("OpenRCT2.app/", temp_dir)
        print("Extracted OpenRCT2.app")

        if util.get_current_platform(True) == "Darwin":
            copy_tree(os.path.join(temp_dir, "OpenRCT2.app/"), "/Applications")
            return 0
        else:
            print("You are forcing a operating system different from the current, so no installation will take place.")
            return "Installation not finished because you're not using macOS"
