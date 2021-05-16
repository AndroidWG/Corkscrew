import asyncio
import asyncio_glib
import gi

asyncio.set_event_loop_policy(asyncio_glib.GLibEventLoopPolicy())

from github import releases

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("layouts/mainWindow.glade")


def call_download(button):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_openrct2())


async def download_openrct2():
    manager = releases.ReleaseManager("OpenRCT2", "OpenRCT2")
    await manager.download_latest_asset("/home/samuel/Downloads/OpenRCT2/", builder.get_object("PgrDownload"))

handlers = {
    "onDestroy": Gtk.main_quit,
    "onDownloadClick": call_download
}
builder.connect_signals(handlers)

win = builder.get_object("MainWindow")
win.show_all()
Gtk.main()
