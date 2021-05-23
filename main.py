import sys
import handler
import platform
import logging
import log_setup
from pubsub import pub

current_platform = platform.system()
log_setup.setup_logging()
logging.info("Logging setup finished")
logging.info("Starting main.py")

if current_platform == "Windows":
    import tray_icon

    tray_icon.start_tray_icon()

download_handler = handler.InstallHandler()
is_up_to_date = download_handler.is_latest_installed

if current_platform == "Linux":
    logging.warning("Linux is currently unsupported. Exiting...")
    sys.exit()

if is_up_to_date:
    logging.info("OpenRCT2 is already up to date")
else:
    download_handler.update_openrct2()

pub.sendMessage("quitSysTray")
sys.exit()
