import os.path
import requests
import platform
from pubsub import pub

import util


def get_latest_release():
    """ Returns the unmodified JSON response of the latest release of OpenRCT2"""
    pub.sendMessage("updateSysTray", text="Getting version info from GitHub...")

    url = f"https://api.github.com/repos/OpenRCT2/OpenRCT2/releases/latest"
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "OpenRCT2 Silent Launcher"}
        )
    except Exception as e:
        print("An error occurred while connecting to the download server. Please check your connection "
              "and try again.")
        print(e)

        pub.sendMessage("updateSysTray", text="Error while checking latest version. Check your "
                                              "connection and try again.")
        return None, None

    print(f"Got latest release from GitHub")

    status_code = response.status_code
    if status_code == 200:
        json_response = response.json()
        return json_response
    else:
        print(f"The latest release request returned status code {status_code}")
        pub.sendMessage("updateSysTray", text=f"Bad status code {status_code} received while getting "
                                              f"release")
        return None, None


def get_latest_version(json_response):
    latest_version = str(json_response["tag_name"]).replace("v", "")  # removes the "v" prefix from version tags
    return latest_version


def get_asset_url_and_name(json_response):
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
            elif "x64" in file["name"]:
                os_specific_binaries["Win_64"][0] = file["url"]
                os_specific_binaries["Win_64"][1] = file["name"]

        elif file["content_type"] == "application/gzip":
            if "linux-i686" in file["name"]:
                os_specific_binaries["Linux_32"][0] = file["url"]
                os_specific_binaries["Linux_32"][1] = file["name"]
            elif "linux-x86_64" in file["name"]:
                os_specific_binaries["Linux_64"][0] = file["url"]
                os_specific_binaries["Linux_64"][1] = file["name"]

        elif file["content_type"] == "application/zip" and "macos" in file["name"]:
            os_specific_binaries["macOS"][0] = file["url"]
            os_specific_binaries["macOS"][1] = file["name"]

    current_platform = platform.system()
    is_64_bit = platform.architecture()[0] == "64bit"

    if current_platform == "Windows":
        if is_64_bit:
            selected_url = os_specific_binaries["Win_64"][0]
            selected_filename = os_specific_binaries["Win_64"][1]
        else:
            selected_url = os_specific_binaries["Win_32"][0]
            selected_filename = os_specific_binaries["Win_32"][1]
    elif current_platform == "Linux":
        if is_64_bit:
            selected_url = os_specific_binaries["Linux_64"][0]
            selected_filename = os_specific_binaries["Linux_64"][1]
        else:
            selected_url = os_specific_binaries["Linux_32"][0]
            selected_filename = os_specific_binaries["Linux_32"][1]
    elif current_platform == "Darwin":
        selected_url = os_specific_binaries["macOS"][0]
        selected_filename = os_specific_binaries["macOS"][1]
    else:
        selected_url = None
        selected_filename = None

    print(f"Selected {selected_filename} based on {current_platform} {platform.architecture()[0]}")
    return selected_url, selected_filename


def download_asset(temp_dir, url, filename):
    pub.sendMessage("updateSysTray", text="Downloading...")

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "OpenRCT2 Silent Launcher", "Accept": "application/octet-stream"},
            stream=True
        )
    except Exception as e:
        print("An error occurred while connecting to the download server. Please check your connection "
              "and try again.")
        print(e)
        pub.sendMessage("updateSysTray", text="Error while downloading. Check your connection and try "
                                              "again.")
        return

    response_size = int(response.headers['content-length'])

    if response.status_code == 200 or response.status_code == 302:
        print(f"Started download request with size: {response_size} bytes")

        with open(os.path.join(temp_dir, filename), "wb") as file:
            bytes_read = 0

            chunk_size = 512
            try:
                for chunk in response.iter_content(chunk_size):
                    file.write(chunk)

                    bytes_read += chunk_size
                    percentage = (bytes_read / response_size)*100
                    progress_string = "Downloading... {:.0f}%".format(percentage)

                    util.print_progress(bytes_read, response_size, suffix="Downloaded", bar_length=65)
                    pub.sendMessage("updateSysTray", text=progress_string)
            except requests.exceptions.ChunkedEncodingError:
                print("Connection was lost while downloading. Please try again.")
                pub.sendMessage("updateSysTray", text="Connection was lost while downloading. Please try "
                                                      "again.")
                return
            except ConnectionError:
                print("An error occurred while connecting to the download server. Please check your connection "
                      "and try again.")
                pub.sendMessage("updateSysTray", text="Connection error. Please try again.")
                return
    else:
        print(f"The download request returned status code {response.status_code}.")
        pub.sendMessage("updateSysTray", text="Bad status code received while downloading")
        return

    print("\nSuccessfully finished downloading")
