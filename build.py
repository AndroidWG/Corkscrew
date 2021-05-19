import platform
import PyInstaller.__main__

# Windows uses ; to separate source and destination strings, while Unix uses :
current_platform = platform.system()
if current_platform == "Windows":
    add_data_string = "layouts/*;layouts"
else:
    add_data_string = "layouts/*:layouts"

PyInstaller.__main__.run([
    "main.py",
    "--add-data=%s" % add_data_string,
    "--icon=%s" % "resources/icon.ico",
    "--name=%s" % "OpenRCT2SilentLauncher",
    "--upx-dir=%s" % "upx/",
    "--noconsole",
    "--onefile"
])
