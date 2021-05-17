import zipfile
import util
from distutils.dir_util import copy_tree


def copy_to_applications(installer_path):
    print("Opening macOS release zip file...")
    with zipfile.ZipFile(installer_path, "r") as downloaded_zip:
        downloaded_zip.extract("OpenRCT2.app/")
        print("Extracted OpenRCT2.app")

        if util.get_current_platform(True) == "Darwin":
            copy_tree("OpenRCT2.app/", "/Applications")
            return 0
        else:
            print("You are running in a system different from macOS while attempting to install like if it were macOS.")
            return "Installation not finished because you're not using macOS"
