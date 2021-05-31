"""Main entrypoint for Corkscrew. Coordinates with the Handler to do the whole checking, downloading and installing.

Flags:
    ``--force-outdated`` or ``-F``
    ``--skip-install`` or ``-SI``
"""
import sys
import handler
import platform
import logging
from util import log_setup

__version = "1.0.1"


# From https://stackoverflow.com/a/16993115/8286014
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def main():
    current_platform = platform.system()
    log_setup.setup_logging("main")

    if current_platform == "Linux":
        logging.warning("Linux is currently unsupported. Exiting...")
        sys.exit()

    sys.excepthook = handle_exception
    logging.debug("Hooked exception handling")

    download_handler = handler.InstallHandler()
    is_up_to_date = download_handler.is_latest_installed

    if is_up_to_date:
        logging.info("OpenRCT2 is already up to date")
    else:
        download_handler.update_openrct2()

    sys.exit()


if __name__ == "__main__":
    main()
