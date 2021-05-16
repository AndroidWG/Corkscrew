import os.path
import requests
import platform


class ReleaseManager:
    def __init__(self, package_name, author_name, builder):
        self.package_name = package_name
        self.author_name = author_name
        self.builder = builder

        self.selected_url = ""
        self.selected_filename = ""
        self.download_view_container = builder.get_object("DownloadContainer")
        self.download_label = builder.get_object("LblSpeed")

    def get_asset_download_url_and_name(self):
        self.download_view_container.set_no_show_all(False)
        self.download_view_container.show_all()
        self.download_label.set_text("Getting latest release...")

        url = f"https://api.github.com/repos/{self.author_name}/{self.package_name}/releases/latest"
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "OpenRCT2 Silent Launcher"}
            )
        except Exception as e:
            print("An error occurred while connecting to the download server. Please check your connection "
                  "and try again.")
            print(e)
            self.download_view_container.hide_all()

        print(f"Got latest release from {self.package_name} with response code {response.status_code}")

        json_response = response.json()
        assets = json_response["assets"]

        os_specific_binaries = {
            "Win_32": ["", ""],
            "Win_64": ["", ""],
            "Linux_32": ["", ""],
            "Linux_64": ["", ""],
            "macOS": ["", ""],
        }

        for file in assets:
            if file["content_type"] == "application/x-ms-dos-executable":
                if "win32" in file["name"]:
                    os_specific_binaries["Win_32"][0] = file["url"]
                    os_specific_binaries["Win_32"][1] = file["name"]
                    print(f"Found Win32 file in URL {file['url']} with name {file['name']}")
                elif "x64" in file["name"]:
                    os_specific_binaries["Win_64"][0] = file["url"]
                    os_specific_binaries["Win_64"][1] = file["name"]
                    print(f"Found Win64 file in URL {file['url']} with name {file['name']}")

            elif file["content_type"] == "application/gzip":
                if "linux-i686" in file["name"]:
                    os_specific_binaries["Linux_32"][0] = file["url"]
                    os_specific_binaries["Linux_32"][1] = file["name"]
                    print(f"Found Linux32 file in URL {file['url']} with name {file['name']}")
                elif "linux-x86_64" in file["name"]:
                    os_specific_binaries["Linux_64"][0] = file["url"]
                    os_specific_binaries["Linux_64"][1] = file["name"]
                    print(f"Found Linux64 file in URL {file['url']} with name {file['name']}")

            elif file["content_type"] == "application/zip" and "macos" in file["name"]:
                os_specific_binaries["macOS"][0] = file["url"]
                os_specific_binaries["macOS"][1] = file["name"]
                print(f"Found macOS file in URL {file['url']} with name {file['name']}")

        current_platform = platform.system()
        is_64_bit = platform.architecture()[0] == "64bit"

        if current_platform == "Windows":
            if is_64_bit:
                self.selected_url = os_specific_binaries["Win_64"][0]
                self.selected_filename = os_specific_binaries["Win_64"][1]
            else:
                self.selected_url = os_specific_binaries["Win_32"][0]
                self.selected_filename = os_specific_binaries["Win_32"][1]
        elif current_platform == "Linux":
            if is_64_bit:
                self.selected_url = os_specific_binaries["Linux_64"][0]
                self.selected_filename = os_specific_binaries["Linux_64"][1]
            else:
                self.selected_url = os_specific_binaries["Linux_32"][0]
                self.selected_filename = os_specific_binaries["Linux_32"][1]
        elif current_platform == "Darwin":
            self.selected_url = os_specific_binaries["macOS"][0]
            self.selected_filename = os_specific_binaries["macOS"][1]

        print(f"Selected {self.selected_filename} based on {current_platform} {platform.architecture()[0]}")

    def download_latest_asset(self, download_path):
        self.download_label.set_text("Starting download...")

        if self.selected_url == "":
            self.get_asset_download_url_and_name()

        try:
            response = requests.get(
                self.selected_url,
                headers={"User-Agent": "OpenRCT2 Silent Launcher", "Accept": "application/octet-stream"},
                stream=True
            )
        except Exception as e:
            print("An error occurred while connecting to the download server. Please check your connection "
                  "and try again.")
            print(e)
            self.download_view_container.hide_all()

        response_size = int(response.headers['content-length'])

        print(f"Started download request with response code {response.status_code}. Download size: {response_size} bytes")

        if response.status_code == 200 or response.status_code == 463:
            with open(os.path.join(download_path, self.selected_filename), "wb") as file:
                bytes_read = 0
                print("Downloading...")

                chunk_size = 512
                try:
                    for chunk in response.iter_content(chunk_size):
                        file.write(chunk)

                        bytes_read += chunk_size
                        progress = bytes_read / response_size
                        self.builder.get_object("PgrDownload").set_fraction(progress)
                except requests.exceptions.ChunkedEncodingError:
                    print("Connection was lost while downloading. Please try again.")
                    self.download_view_container.hide_all()
                except ConnectionError:
                    print("An error occurred while connecting to the download server. Please check your connection "
                          "and try again.")
                    self.download_view_container.hide_all()

        print("Successfully finished downloading")
