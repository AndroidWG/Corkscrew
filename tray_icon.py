import sys

from infi.systray import SysTrayIcon
from pubsub import pub


def dummy_function(dummy_var):
    pass


def on_quit_callback(_systray):
    systray.shutdown()
    sys.exit()
    # TODO: Properly quit everything here


def update_systray_hover_text_listener(text):
    systray.update(hover_text=text)


def quit_tray_icon_listener():
    systray.shutdown()


def start_tray_icon():
    global systray

    menu_options = (("Starting...", None, dummy_function),)
    systray = SysTrayIcon("design/icon.ico", "OpenRCT2 Silent Launcher", menu_options)
    systray.start()

    pub.subscribe(update_systray_hover_text_listener, "updateSysTray")
    pub.subscribe(quit_tray_icon_listener, "quitSysTray")
