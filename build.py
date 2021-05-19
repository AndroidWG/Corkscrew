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

PyInstaller.__main__.run([
    "main.py",
    "--add-data=%s" % add_data_string,
    "--icon=%s" % icon_file,
    "--name=%s" % "OpenRCT2 Silent Launcher",
    "--upx-dir=%s" % "upx/",
    "--noconsole",
    "--onefile"
])
