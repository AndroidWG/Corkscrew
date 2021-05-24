import os
import platform
import shutil
import tempfile

import PyInstaller.__main__
import sys

import util

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main

# Define variables
current_platform = platform.system()
files_to_bundle = ["resources/icon.ico;resources"]

version = main.__version
version_split = version.split(".")
temp_ver_info_file = "file_ver_info.txt"

# Prepare system specific resources
if current_platform == "Darwin":
    icon_file = "resources/icon.icns"
elif current_platform == "Windows":
    icon_file = "resources/icon.ico"

    tags = [
        ("#VERSION#", version),
        ("VERSION_TUPLE", f"{version_split[0]}, {version_split[1]}, {version_split[2]}, 0")
    ]
    util.replace_instances("resources/file_version_template.txt", tags, temp_ver_info_file)


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

# If UPX folder is found inside root, make sure that PyInstaller uses it
if os.path.exists("../upx/"):
    args.append("--upx-dir=%s" % "upx/")

# Run PyInstaller
PyInstaller.__main__.run(args)

# Make platform installer
final_name = f"dist/corkscrew-v{version}"

if current_platform == "Windows":
    shutil.move("dist/Corkscrew.exe", final_name + ".exe")
    os.remove("file_ver_info.txt")
    print("Renamed file and removed file_ver_info")
elif current_platform == "Darwin":
    import macos_installer

    info = macos_installer.PackageInfo(
        name="Corkscrew",
        version=version,
        package="com.androidwg.corkscrew",
        install_location="/Library/Corkscrew"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        print("\nStarted building macOS installer")
        macos_installer.copy_darwin_directory(info, temp_dir)

        files = [
            "dist/Corkscrew",
            os.path.join(temp_dir, "darwin/Resources/com.androidwg.corkscrew.plist"),
            os.path.join(temp_dir, "darwin/Resources/uninstall.sh")
        ]

        distribution = os.path.join(temp_dir, "darwin/distribution.plist")
        resources_path = os.path.join(temp_dir, "darwin/Resources")
        packages_path = os.path.join(temp_dir, "package")

        main_package = macos_installer.create_package(info, files, temp_dir)
        macos_installer.create_product_installer(info, distribution, resources_path, packages_path, temp_dir)

print(f"Finished building version {version}")
