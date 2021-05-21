import gi
import util
from pubsub import pub

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.Builder()


# ------- LISTENERS -------
def progress_bar_listener(fraction):
    builder.get_object("progress_main").set_fraction(fraction)


def label_text_listener(new_text):
    builder.get_object("label_main").set_text(new_text)

# -------------------------


def show_gui():
    global builder
    builder.add_from_file(util.resource_path("resources/update_window.glade"))

    main_window = builder.get_object("main_window")
    main_window.connect("destroy", Gtk.main_quit)

    pub.subscribe(progress_bar_listener, "progressChanged")
    pub.subscribe(label_text_listener, "statusChanged")

    print("Showing main window")
    win = builder.get_object("main_window")
    win.show_all()
    Gtk.main()
