import logging
import requests
from pubsub import pub
from requests.auth import HTTPBasicAuth
from github import set_random_username, exceptions
from settings import local_settings


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
        auth=HTTPBasicAuth(local_settings.github_username, "")
    )

    logging.debug("Got response")

    status_code = response.status_code
    if str(status_code).startswith("4"):
        logging.error(f"Received a client error status code from GitHub releases")
        raise exceptions.ClientError(status_code)
    elif str(status_code).startswith("5"):
        logging.error(f"Received a server error status code from GitHub releases")
        raise exceptions.ServerError(status_code)
    else:
        return response
