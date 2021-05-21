import sys
import threading
import gi
import handler
import util

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file(util.resource_path("layouts/mainWindow.glade"))

if sys.argv.__contains__("-forceWindows"):
    print("Force Windows platform enabled")
elif sys.argv.__contains__("-forceLinux"):
    print("Force Linux platform enabled")
elif sys.argv.__contains__("-forceMacOS"):
    print("Force macOS platform enabled")

download_handler = handler.GithubHandler(builder)
is_up_to_date = download_handler.is_latest_installed()
main_button = builder.get_object("BtnMain")

if not is_up_to_date:
    main_button.set_label("Update OpenRCT2")
    main_button.set_sensitive(True)
else:
    main_button.set_label("OpenRCT2 is up to date")


def call_download_handler(button):
    thread = threading.Thread(target=download_handler.update_openrct2)
    thread.start()


handlers = {
    "onDestroy": Gtk.main_quit,
    "onDownloadClick": call_download_handler
}
builder.connect_signals(handlers)

print("Showing main window")

win = builder.get_object("MainWindow")
win.show_all()
Gtk.main()
