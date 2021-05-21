import os.path
import subprocess
import util


def do_silent_install(temp_dir, installer_path):
    if util.get_current_platform(True):
        print("Installing for Windows...")
        command = f"\"{os.path.join(temp_dir, installer_path)}\" /S"

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()

        print("Finished installation")
        return 0
    else:
        print("You are forcing a operating system different from the current, so no installation will take place.")
        return "Installation not finished because you're not using Windows"
