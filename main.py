import sys
import handler
import platform
import logging
from pubsub import pub

# Set up logging
#logging.basicConfig(filename=)

if platform.system() == "Windows":
    import tray_icon
    tray_icon.start_tray_icon()

download_handler = handler.InstallHandler()
is_up_to_date = download_handler.is_latest_installed

if download_handler.current_platform == "Linux":
    print("Linux is currently unsupported. Exiting...")
    sys.exit()


if is_up_to_date:
    print("OpenRCT2 is already up to date")
    pub.sendMessage("quitSysTray")
    sys.exit()
else:
    download_handler.update_openrct2()
    pub.sendMessage("quitSysTray")
    sys.exit()
