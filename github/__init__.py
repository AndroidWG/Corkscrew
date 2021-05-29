import logging
import os.path
import random
import string
import requests
import platform
import util
from github import exceptions, requests
from settings import local_settings


def set_random_username() -> str:
    username = "corkscrew_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
    local_settings.github_username = username
    return username


def get_latest_release():
    """ Returns the JSON object of the latest release of OpenRCT2

    :return: JSON object from requests call
    """
    url = f"https://api.github.com/repos/OpenRCT2/OpenRCT2/releases/latest"
    accept = "application/vnd.github.v3+json"

    logging.info("\nGetting latest release from GitHub...")
    responses = requests.send_request(url, accept)
    logging.info("Finished getting release info\n")
    return responses.json()


def get_version(json) -> str:
    """Gets the version string in a GitHub latest release request.

    :param json: GitHub latest release JSON object from Requests
    :type json: str
    :return: Version as string without "v" prefix
    :rtype: str
    """
    version = str(json["tag_name"]).replace("v", "")  # Removes the "v" prefix from version tags
    return version


# noinspection PyTypeChecker
def get_asset_url_and_name(json):
    """Find the URL and filename of the correct binaries for the current OS using a JSON object from a GitHub release
    request response.

    :param json: GitHub latest release JSON object from Requests
    :type json: str
    :return: Tuple containing URL and filename respectively for the current OS
    :rtype: tuple
    """
    logging.info("\nFinding assets from release...")
    assets = json["assets"]

    os_specific_binaries = {
        "Win_32": ["", ""],
        "Win_64": ["", ""],
        "Linux_32": ["", ""],
        "Linux_64": ["", ""],
        "macOS": ["", ""],
    }

    # TODO: Add error handling if one of these keys isn't found, so the program keeps going
    # noinspection PyUnboundLocalVariable
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

    logging.info(f"Selected {selected_filename} based on {current_platform} {platform.architecture()[0]}\n")
    return selected_url, selected_filename


def download_asset(temp_dir: str, url: str, filename: str):
    """Downloads a file in 512 byte chunks from a GitHub octet-stream.

    :param temp_dir: Temporary directory to be used
    :type temp_dir: str
    :param url: URL to the octet-stream API call
    :type url: str
    :param filename: Name of the downloaded file
    :type filename: str
    """

    logging.info("\nSending asset download request...")
    response = requests.send_request(url, "application/octet-stream")
    response_size = int(response.headers['content-length'])

    logging.debug(f"Started downloading {response_size} bytes...")

    with open(os.path.join(temp_dir, filename), "wb") as file:
        bytes_read = 0

        chunk_size = 512
        for chunk in response.iter_content(chunk_size):
            file.write(chunk)  # TODO: Add error handling for IO exceptions

            bytes_read += chunk_size
            util.print_progress(bytes_read, response_size, suffix="Downloaded")

    logging.info(f"Successfully finished downloading {filename}\n")
    return True
