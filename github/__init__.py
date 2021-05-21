import os.path
import requests
import platform
import util
from gi.repository import GLib


def update_progress(progress_bar, fraction):
    progress_bar.set_fraction(fraction)


def get_latest_release():
    """ Returns the unmodified JSON response of the latest release of OpenRCT2"""
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
        return None, None

    print(f"Got latest release from OpenRCT2 with response code {response.status_code}")

    if response.status_code == 200:
        json_response = response.json()
        return json_response
    else:
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

    current_platform = util.get_current_platform()
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


def download_asset(temp_dir, url, filename, progress_bar):
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
        return "Error while downloading. Check your connection and try again."

    response_size = int(response.headers['content-length'])

    if response.status_code == 200 or response.status_code == 302:
        print(f"Started download request with size: {response_size} bytes")

        with open(os.path.join(temp_dir, filename), "wb") as file:
            bytes_read = 0
            print("Downloading...")

            chunk_size = 512
            try:
                for chunk in response.iter_content(chunk_size):
                    file.write(chunk)

                    bytes_read += chunk_size
                    progress = bytes_read / response_size
                    GLib.idle_add(update_progress, progress_bar, progress)
            except requests.exceptions.ChunkedEncodingError:
                print("Connection was lost while downloading. Please try again.")
                return "Connection was lost while downloading. Please try again."
            except ConnectionError:
                print("An error occurred while connecting to the download server. Please check your connection "
                      "and try again.")
                return "Connection error. Please try again."
    else:
        print(f"The download request returned status code {response.status_code}.")
        return "Bad status code received."

    print("Successfully finished downloading")
    return 0
