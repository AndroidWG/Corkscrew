import sys
import threading
import handler
import ui
from pubsub import pub

if not sys.argv.__contains__("--silentMode") and not sys.argv.__contains__("-S"):
    thread = threading.Thread(target=ui.show_gui)
    thread.start()

download_handler = handler.InstallHandler()
is_up_to_date = download_handler.is_latest_installed

if is_up_to_date:
    print("OpenRCT2 is already up to date")
    pub.sendMessage("statusChanged", new_text="OpenRCT2 is up to date")
else:
    download_handler.update_openrct2()
