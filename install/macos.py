import os.path
import zipfile
import subprocess
import plistlib
from shutil import copytree


def get_install_folder_and_version():
    app_path = "/Applications/OpenRCT2.app"

    if os.path.exists(app_path):
        with open(os.path.join(app_path, "/Contents/Info.plist"), "rb") as file:
            plist = plistlib.load(file)
            return app_path, plist["CFBundleShortVersionString"]
    else:
        return None, None


def copy_to_applications(temp_dir, installer_path):
    print("Installing for macOS...")

    zip_path = os.path.join(temp_dir, installer_path)
    with zipfile.ZipFile(zip_path, "r") as downloaded_zip:
        downloaded_zip.extractall(temp_dir)
        print("Extracted OpenRCT2.app")

        # for some reason zipfile extracts the main executable inside the .app as a
        # non-executable file, so we need to manually do that
        make_unix_executable(temp_dir, "OpenRCT2.app/Contents/MacOS/OpenRCT2")
        copytree(os.path.join(temp_dir, "OpenRCT2.app"), "/Applications/OpenRCT2.app", symlinks=True)

        print("Finished installation successfully")


def make_unix_executable(temp_dir, file):
    file_path = os.path.join(temp_dir, file)

    process = subprocess.Popen(["chmod", "+x", file_path], stdout=subprocess.PIPE)
    process.wait()
