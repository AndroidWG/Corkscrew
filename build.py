import os
import platform
import PyInstaller.__main__

current_platform = platform.system()
files_to_bundle = ["resources/*.plist;resources", "resources/icon.ico;resources"]

if current_platform == "Darwin":
    icon_file = "resources/icon.icns"
else:
    icon_file = "resources/icon.ico"

args = [
    "main.py",
    "--icon=%s" % icon_file,
    "--name=%s" % "OpenRCT2 Silent Launcher",
    "--noconsole",
    "--onefile",
    "--osx-bundle-identifier=%s" % "com.androidwg.openrct2silentlauncher"
]

for file in files_to_bundle:
    file_formatted = file
    if current_platform != "Windows":
        file_formatted = file.replace(";", ":")
        
    arg = "--add-data=%s" % file_formatted
    args.append(arg)

# if UPX folder is found inside root, make sure that PyInstaller uses it
if os.path.exists("upx/"):
    args.append("--upx-dir=%s" % "upx/")

PyInstaller.__main__.run(args)
