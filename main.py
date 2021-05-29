"""Main entrypoint for Corkscrew. Coordinates with the Handler to do the whole checking, downloading and installing.

Flags:
    ``--force-install`` or ``-F``
"""
import sys
import handler
import platform
import logging
from util import log_setup

__version = "0.2.0"


# From https://stackoverflow.com/a/16993115/8286014
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def main():
    current_platform = platform.system()
    log_setup.setup_logging("main.log")

    sys.excepthook = handle_exception
    logging.debug("Hooked exception handling")

    # TODO: Add check if program is already running

    download_handler = handler.InstallHandler()
    if sys.argv.__contains__("--force-install") or sys.argv.__contains__("-F"):
        is_up_to_date = False
    else:
        is_up_to_date = download_handler.is_latest_installed

    if current_platform == "Linux":
        logging.warning("Linux is currently unsupported. Exiting...")
        sys.exit()

    if is_up_to_date:
        logging.info("OpenRCT2 is already up to date")
    else:
        download_handler.update_openrct2()

    sys.exit()


if __name__ == "__main__":
    main()
