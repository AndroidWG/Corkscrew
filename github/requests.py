import logging
import time
import requests
import github
import util.timeout
from github import set_random_username, exceptions
from util.settings import local_settings
from typing import Callable
from requests.auth import HTTPBasicAuth


@util.timeout.exit_after(180)
def send_request(url: str, accept: str) -> requests.Response:
    """ Sends a request to the specified URL with the specified accept header. Uses "Corkscrew" User-Agent and
    authenticates with a random username stored in the app's settings. Raises a ClientError when a 4xx status
    code is received and a ServerError when a 5xx status code is received.

    :param url: URL to send to
    :type url: str
    :param accept: Accept parameter to be inserted in the header
    :type accept: str
    :return: Response object
    :rtype: requests.Response
    """
    if local_settings.github_username == "":
        set_random_username()

    response = requests.get(
        url,
        headers={"User-Agent": "Corkscrew", "Accept": accept},
        auth=HTTPBasicAuth(util.local_settings.github_username, "")
    )

    logging.debug("Got response")

    status_code = response.status_code
    if str(status_code).startswith("4"):
        logging.error(f"Received a client error status code from GitHub releases")
        logging.error(response.json())
        raise exceptions.ClientError(status_code)
    elif str(status_code).startswith("5"):
        logging.error(f"Received a server error status code from GitHub releases")
        logging.error(response.json())
        raise exceptions.ServerError(status_code)
    else:
        return response


def wait_for_internet():
    """Sends a request to google.com up to 300 times to check if there's internet connectivity. Returns True if it was
    able to connect in under 300 tries and False if it reached that limit.

    :return: Boolean indicating if caller should try again or give up
    :rtype: bool
    """
    counter = 0
    while True:
        try:
            requests.get("https://google.com")
            logging.info("Connected to the internet again")
            return True
        except requests.exceptions.ConnectionError:
            logging.info(f"Unable to connect to google.com (tried {counter} times)")
            counter += 1

            if counter > 300:
                logging.error("Unable to connect after 300 tries. Exiting...")
                return False

            time.sleep(1.5)


def try_to_get_request(request_func: Callable, message: str = "request", *args):
    """Tries to run ``request_func`` and catches common exception errors from methods that use
    ``requests.get``. Returns None if the request ultimately fails.

    :param args: Non-keyworded parameters to send to function
    :param message: Name to be used when logging
    :type message: str
    :param request_func: The function that we will try. Should be from github.__init__ and be
    decorated with @util.timeout.exit_after(2)
    :type request_func: Callable
    :return: request_func result or None if it fails
    """
    counter = 0
    while True:
        try:
            if len(args) == 0:
                return request_func()
            else:
                return request_func(*args)
        except requests.exceptions.ConnectionError:
            logging.warning(f"A connection error occurred while getting {message}")
            if not wait_for_internet():
                return None
        except requests.exceptions.Timeout:
            logging.warning(f"Timed out while requesting {message}")
            if not wait_for_internet():
                return None
        except requests.exceptions.MissingSchema as e:
            logging.error(f"Wrong URL was sent in {message} request. Exiting...", exc_info=e)
            return None
        except github.exceptions.ServerError as e:
            logging.warning(f"Received a server error status code while getting {message}. Trying again...",
                            exc_info=e)
            counter += 1
        except github.exceptions.ClientError as e:
            logging.warning(f"Received a client error status code while getting {message}. Trying again...",
                            exc_info=e)
            counter += 1
        except requests.exceptions.ChunkedEncodingError:
            logging.warning(f"Connection error while downloading {message}")
            wait_for_internet()
            counter += 1
        except KeyboardInterrupt as e:
            logging.error(f"Request took too long to respond. Exiting...", exc_info=e)
            return None

        if counter >= 5:
            logging.error("Getting latest release failed after 5 tries. Exiting...")
            return None
