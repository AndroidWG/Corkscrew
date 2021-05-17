import atexit
import os
import shutil
import sys
import tempfile
import threading
import gi
import handler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("layouts/mainWindow.glade")

if sys.argv.__contains__("-forceWindows"):
    print("Force Windows platform enabled")
elif sys.argv.__contains__("-forceLinux"):
    print("Force Linux platform enabled")
elif sys.argv.__contains__("-forceMacOS"):
    print("Force macOS platform enabled")


def call_download_handler(button):
    download_handler = handler.DownloadInstallHandler(builder)

    thread = threading.Thread(target=download_handler.download_and_install)
    thread.start()


handlers = {
    "onDestroy": Gtk.main_quit,
    "onDownloadClick": call_download_handler
}
builder.connect_signals(handlers)

win = builder.get_object("MainWindow")
win.show_all()
Gtk.main()
