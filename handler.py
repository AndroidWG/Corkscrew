import tempfile
import install
import github
from packaging import version


# This file coordinates execution from the install and github packages. Should be
# called in a different thread to not lock UI thread
class InstallHandler:
    def __init__(self):
        self.installer_url, self.installer_path = None, None
        self.latest_release = github.get_latest_release()
        self.is_latest_installed = self.check_if_latest_is_installed()

    def check_if_latest_is_installed(self):
        try:
            installed = version.parse(install.check_openrct2_install()[1])
        except TypeError:
            # If check_openrct2_install returns null, the "[1]" thing will throw this exception
            # meaning an installation was not found
            return False

        latest = version.parse(github.get_latest_version(self.latest_release))

        if latest >= installed:
            return True
        else:
            return False

    def download_openrct2(self, temp_dir):
        self.installer_url, self.installer_path = github.get_asset_url_and_name(self.latest_release)
        if self.installer_url is None and self.installer_path is None:
            return

        github.download_asset(temp_dir, self.installer_url, self.installer_path)

    def update_openrct2(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Created temp dir at {temp_dir}")

            self.download_openrct2(temp_dir)
            install.install_or_update_openrct2(temp_dir, self.installer_path)
