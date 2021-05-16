import os.path

import requests
import platform
import asyncio


class ReleaseManager:
    def __init__(self, package_name, author_name):
        self.package_name = package_name
        self.author_name = author_name

        self.selected_url = ""
        self.selected_filename = ""

    async def get_asset_download_url_and_name(self):
        url = f"https://api.github.com/repos/{self.author_name}/{self.package_name}/releases/latest"
        response = requests.get(
            url,
            headers={"User-Agent": "OpenRCT2 Silent Launcher"}
        )

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

    async def download_latest_asset(self, download_path, progress_bar):
        if self.selected_url == "":
            await self.get_asset_download_url_and_name()

        response = requests.get(
            self.selected_url,
            headers={"User-Agent": "OpenRCT2 Silent Launcher", "Accept": "application/octet-stream"},
            stream=True
        )
        response_size = int(response.headers['content-length'])

        print(f"Started download request with response code {response.status_code}. Download size: {response_size} bytes")

        if response.status_code == 200:
            with open(os.path.join(download_path, self.selected_filename), "wb") as file:
                bytes_read = 0
                print("Downloading...")

                for chunk in response.iter_content(512):
                    file.write(chunk)

                    bytes_read += 512
                    progress = bytes_read / response_size
                    # progress_bar.set_fraction(progress)

        print("Successfully finished downloading")
