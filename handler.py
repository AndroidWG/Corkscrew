import tempfile
import util
import gi
import webbrowser
from github import releases
from install import windows, macos

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


# This file is a bridge from UI to code. Main thread calls functions here in a different thread. This file
# only handles (most) UI updates and chains functions together;
class DownloadInstallHandler:
    def __init__(self, builder):
        self.installer_url, self.installer_file = None, None
        self.builder = builder

        self.download_view_container = builder.get_object("DownloadContainer")
        self.download_label = builder.get_object("LblSpeed")
        self.progress_bar = builder.get_object("PgrDownload")

    def download_openrct2(self, temp_dir):
        # UI Updates
        self.download_view_container.set_no_show_all(False)
        self.download_view_container.show_all()
        self.download_label.set_text("Getting latest release...")

        self.installer_url, self.installer_file = releases.get_asset_download_url_and_name()
        if self.installer_url is None and self.installer_file is None:
            self.download_label.set_text("Connection error. Please try again.")
            return

        self.download_label.set_text("Downloading...")
        return_data = releases.download_asset(temp_dir, self.installer_url, self.installer_file, self.progress_bar)

        if return_data != 0:
            self.download_label.set_text(return_data)

    def install_openrct2(self, temp_dir):
        self.download_label.set_text("Installing...")

        current_platform = util.get_current_platform()

        if current_platform == "Windows":
            windows.do_silent_install(temp_dir, self.installer_file)
        elif current_platform == "Darwin":
            return_data = macos.copy_to_applications(temp_dir, self.installer_file)
            if return_data != 0:
                self.download_label.set_text(return_data)
                return

        self.download_label.set_text("Finished installing")

    def download_and_install(self):
        if util.get_current_platform() == "Linux":
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Created temp dir at {temp_dir}")

                self.download_openrct2(temp_dir)
                self.install_openrct2(temp_dir)
        else:
            print("Running on Linux is currently unsupported. Check the GUI alert.")
            GLib.idle_add(show_linux_message)


def show_linux_message():
    dialog = Gtk.MessageDialog(
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.YES_NO,
        text="Linux is currently unsupported. Would you like to visit OpenRCT2's installation guide for Linux?"
    )
    response = dialog.run()
    if response == Gtk.ResponseType.YES:
        webbrowser.open("https://openrct2.org/quickstart/install/linux")

    dialog.destroy()
