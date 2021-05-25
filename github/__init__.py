import logging
import os.path
import requests
import platform
import util
from pubsub import pub


def get_latest_release():
    """ Returns the JSON object of the latest release of OpenRCT2

    :return: JSON object from requests call
    """
    pub.sendMessage("updateSysTray", text="Getting version info from GitHub...")

    url = f"https://api.github.com/repos/OpenRCT2/OpenRCT2/releases/latest"
    try:  # TODO: Add random simple user auth to prevent request limiting
        response = requests.get(
            url,
            headers={"User-Agent": "Corkscrew"}
        )
    except Exception as e:
        logging.error("An error occurred while connecting to the download server. Please check your connection "
                      "and try again.\nException info: ")
        logging.exception(e)

        pub.sendMessage("updateSysTray", text="Error while checking latest version. Check your "
                                              "connection and try again.")
        return None, None

    logging.info(f"Got latest release from GitHub")

    status_code = response.status_code
    if status_code == 200:
        json_response = response.json()
        return json_response
    else:
        logging.error(f"The latest release request returned status code {status_code}")
        pub.sendMessage("updateSysTray", text=f"Bad status code {status_code} received while getting "
                                              f"release")
        return None, None


def get_latest_version(json) -> str:
    """Gets the version string in a GitHub latest release request.

    :param json: GitHub latest release JSON object from Requests
    :type json: str
    :return: Version as string without "v" prefix
    :rtype: str
    """
    latest_version = str(json["tag_name"]).replace("v", "")  # removes the "v" prefix from version tags
    return latest_version


# noinspection PyTypeChecker
def get_asset_url_and_name(json):
    """Find the URL and filename of the correct binaries for the current OS.

    :param json: GitHub latest release JSON object from Requests
    :type json: str
    :return: Tuple containing URL and filename respectively for the current OS
    :rtype: tuple
    """
    assets = json["assets"]

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

    logging.info(f"Selected {selected_filename} based on {current_platform} {platform.architecture()[0]}")
    return selected_url, selected_filename


def download_asset(temp_dir: str, url: str, filename: str):
    """Downloads a file in 512 byte chunks from a GitHub octet-stream.

    :param temp_dir: Temporary directory to be used
    :type temp_dir: str
    :param url: URL to the octect-stream API call
    :type url: str
    :param filename: Name of the downloaded file
    :type filename: str
    """
    pub.sendMessage("updateSysTray", text="Downloading...")

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Corkscrew", "Accept": "application/octet-stream"},
            stream=True
        )
    except Exception as e:
        logging.error("An error occurred while connecting to the download server. Please check your connection "
                      "and try again.")
        logging.exception(e)
        pub.sendMessage("updateSysTray", text="Error while downloading. Check your connection and try "
                                              "again.")
        return

    response_size = int(response.headers['content-length'])

    if response.status_code == 200 or response.status_code == 302:
        logging.info(f"Started download request with size: {response_size} bytes")

        pub.sendMessage("updateSysTray", text="Downloading... 0%")
        with open(os.path.join(temp_dir, filename), "wb") as file:
            bytes_read = 0

            chunk_size = 512
            try:
                for chunk in response.iter_content(chunk_size):
                    file.write(chunk)

                    bytes_read += chunk_size
                    percentage = (bytes_read / response_size) * 100
                    progress_string = "Downloading... {:.0f}%".format(percentage)

                    util.print_progress(bytes_read, response_size, suffix="Downloaded", bar_length=55)

                    if int(percentage) % 5 == 0:  # To avoid lagging out the tray icon, only update every 5% of progress
                        pub.sendMessage("updateSysTray", text=progress_string)
            except requests.exceptions.ChunkedEncodingError:
                logging.warn("Connection was lost while downloading. Please try again.")
                pub.sendMessage("updateSysTray", text="Connection was lost while downloading. Please try "
                                                      "again.")
                return
            except ConnectionError:
                logging.error("An error occurred while connecting to the download server. Please check your connection "
                              "and try again.")
                pub.sendMessage("updateSysTray", text="Connection error. Please try again.")
                return
    else:
        logging.error(f"The download request returned status code {response.status_code}.")
        pub.sendMessage("updateSysTray", text="Bad status code received while downloading")
        return

    logging.info("Successfully finished downloading")
