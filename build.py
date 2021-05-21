import os
import platform
import PyInstaller.__main__

# Windows uses ; to separate source and destination strings, while Unix uses :
current_platform = platform.system()
if current_platform == "Windows":
    add_data_string = "layouts/*;layouts"
else:
    add_data_string = "layouts/*:layouts"

if current_platform == "Darwin":
    icon_file = "resources/openrct2.icns"
else:
    icon_file = "resources/icon.ico"

args = [
    "main.py",
    "--add-data=%s" % add_data_string,
    "--icon=%s" % icon_file,
    "--name=%s" % "OpenRCT2 Silent Launcher",
    "--noconsole",
    "--onefile"
]

# if UPX folder is found inside root, make sure that PyInstaller uses it
if os.path.exists("upx/"):
    args.append("--upx-dir=%s" % "upx/")

PyInstaller.__main__.run(args)
