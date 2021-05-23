import logging
import os
import platform
import datetime as dt


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

    # Pipe logs to console so no need to use logging and print for the same messages
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    formatter = logging.Formatter("%(message)s")
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
