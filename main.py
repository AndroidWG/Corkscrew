import platform

import gi
import threading
from github import releases

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("layouts/mainWindow.glade")


def get_download_folder():
    if platform.system() == "Windows":
        return "C:\\Users\\samu-\\Downloads\\OpenRCT2"
    else:
        return "/home/samuel/Downloads/OpenRCT2/"


def download_openrct2(button):
    manager = releases.ReleaseManager("OpenRCT2", "OpenRCT2", builder)
    thread = threading.Thread(target=manager.download_latest_asset,
                              args=(get_download_folder(), ))
    thread.start()


handlers = {
    "onDestroy": Gtk.main_quit,
    "onDownloadClick": download_openrct2
}
builder.connect_signals(handlers)

win = builder.get_object("MainWindow")
win.show_all()
Gtk.main()
