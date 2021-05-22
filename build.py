import os
import platform
import PyInstaller.__main__

current_platform = platform.system()
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

# if UPX folder is found inside root, make sure that PyInstaller uses it
if os.path.exists("upx/"):
    args.append("--upx-dir=%s" % "upx/")

PyInstaller.__main__.run(args)
