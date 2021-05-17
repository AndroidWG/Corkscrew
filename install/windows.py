import subprocess


def do_silent_install(installer_path):
    command = f"\'{installer_path}\" /S"

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.returncode)
