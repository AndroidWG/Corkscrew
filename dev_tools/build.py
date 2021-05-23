import os
import platform
import shutil
import PyInstaller.__main__
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main

current_platform = platform.system()
files_to_bundle = ["resources/icon.ico;resources"]

version = main.__version
version_split = version.split(".")
temp_ver_info_file = "file_ver_info.txt"

if current_platform == "Darwin":
    icon_file = "resources/icon.icns"
elif current_platform == "Windows":
    icon_file = "resources/icon.ico"

    with open("resources/file_version_template.txt", "rt") as file_in:
        with open(temp_ver_info_file, "wt") as file_out:
            for line in file_in:
                file_out.write(line
                               .replace("#VERSION#", version)
                               .replace("#, #, #, #", f"{version_split[0]}, {version_split[1]}, {version_split[2]}, 0"))


args = [
    "main.py",
    "--icon=%s" % icon_file,
    "--name=%s" % "Corkscrew",
    "--version-file=%s" % temp_ver_info_file,
    "--noconsole",
    "--onefile",
    "--osx-bundle-identifier=%s" % "com.androidwg.corkscrew"
]

for file in files_to_bundle:
    file_formatted = file
    if current_platform != "Windows":
        file_formatted = file.replace(";", ":")

    arg = "--add-data=%s" % file_formatted
    args.append(arg)

# if UPX folder is found inside root, make sure that PyInstaller uses it
if os.path.exists("../upx/"):
    args.append("--upx-dir=%s" % "upx/")

PyInstaller.__main__.run(args)

os.remove("file_ver_info.txt")

final_name = f"dist/corkscrew-v{version}"

if current_platform == "Windows":
    shutil.move("dist/Corkscrew.exe", final_name + ".exe")
    print("Renamed file")
elif current_platform == "Darwin":
    shutil.make_archive(final_name + ".zip", "zip", "dist/Corkscrew.app")

    print("Packaged app to zip")

print(f"Finished build with version {version}")
