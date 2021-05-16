import threading

import gi
import tempfile
import handler
from github import releases

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("layouts/mainWindow.glade")


def call_download_handler(button):
    thread = threading.Thread(target=handler.download_rct2,
                              args=(working_folder.name, builder))
    thread.start()


def get_working_folder():
    temp_dir = tempfile.TemporaryDirectory()
    print(f"Created temp dir at {temp_dir}")
    return temp_dir


working_folder = get_working_folder()

handlers = {
    "onDestroy": Gtk.main_quit,
    "onDownloadClick": call_download_handler
}
builder.connect_signals(handlers)

win = builder.get_object("MainWindow")
win.show_all()
Gtk.main()
