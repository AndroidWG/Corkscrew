import os.path
import zipfile
import util
import subprocess
from shutil import copytree


def copy_to_applications(temp_dir, installer_path):
    print("Installing for macOS...")

    zip_path = os.path.join(temp_dir, installer_path)
    with zipfile.ZipFile(zip_path, "r") as downloaded_zip:
        downloaded_zip.extractall(temp_dir)
        print("Extracted OpenRCT2.app")

        if util.get_current_platform(True) == "Darwin":
            # for some reason zipfile extracts the main executable from the zip as a non-executable file
            # so we need to manually do that
            make_unix_executable(temp_dir, "OpenRCT2.app/Contents/MacOS/OpenRCT2")

            copytree(os.path.join(temp_dir, "OpenRCT2.app"), "/Applications/OpenRCT2.app", symlinks=True)
            
            print(os.path.join(temp_dir, "OpenRCT2.app/"))
            print("Done installing")
            return 0
        else:
            print("You are forcing a operating system different from the current, so no installation will take place.")
            return "Installation not finished because you're not using macOS"

def make_unix_executable(temp_dir, file):
    file_path = os.path.join(temp_dir, file)
    process = subprocess.Popen(["chmod", "+x", file_path], stdout=subprocess.PIPE)
    process.wait()