import logging
import os
import platform
import datetime as dt
import sys


class MillisecondFormatter(logging.Formatter):
    """A formatter for standard library 'logging' that supports '%f' wildcard in format strings."""
    converter = dt.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)[:-3]
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s


def setup_logging():
    current_platform = platform.system()

    # Define log location, local AppData for Windows and user's Logs folder on macOS.
    logs_path = ""
    if current_platform == "Windows":
        logs_path = os.path.join(os.getenv("localappdata"), "OpenRCT2 Silent Launcher")
    elif current_platform == "Darwin":
        logs_path = os.path.join(os.path.expanduser("~/Library/Log"), "OpenRCT2 Silent Launcher")

    log_path = os.path.join(logs_path, "launcher.log")

    if not os.path.exists(logs_path):
        os.mkdir(logs_path)

    logging.basicConfig(
        filename=log_path,
        filemode="w",
        level=logging.INFO)

    # Set custom Formatter to support DateFormats with milliseconds
    formatter = MillisecondFormatter(fmt="%(asctime)s | %(levelname)-7s | %(message)s",
                                     datefmt="%H:%M:%S.%f")
    log_handler = logging.getLogger().handlers[0]
    log_handler.setFormatter(formatter)

    # Add stdout to log exceptions and also idk why but it makes logging calls print to console too
    # Part of code from https://stackoverflow.com/a/16993115/8286014
    system_handler = logging.StreamHandler(stream=sys.stdout)
    logging.getLogger().addHandler(system_handler)
