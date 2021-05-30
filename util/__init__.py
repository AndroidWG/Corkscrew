import os
import shutil
import sys
import logging
import time
import psutil
import util.timeout


# From https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a#file-print_progress-py
def print_progress(iteration: int, total: int, prefix: str = "", suffix: str = "done", decimals: int = 1):
    """Call in a loop to create a CLI progress bar.

    :param iteration: Current iteration
    :type iteration: int
    :param total: Total number of iterations
    :type total: int
    :param prefix: Prefix to progress bar
    :type prefix: str
    :param suffix: Suffix to progress bar
    :type suffix: str
    :param decimals: Number of decimals to be shown in percentage
    :type decimals: int
    """

    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))

    cli_length = shutil.get_terminal_size().columns
    available_length = cli_length - len("%s || 100.0%s %s" % (prefix, "%", suffix))

    filled_length = int(round(available_length * iteration / float(total)))
    bar = "#" * filled_length + '-' * (available_length - filled_length)

    ready_to_print = ("%s |%s| %s%s %s" % (prefix, bar, percents, "%", suffix))

    print(ready_to_print, end="\r", flush=True)

    if iteration >= total:
        print(ready_to_print)
    else:
        sys.stdout.flush()


# From https://stackoverflow.com/a/13790741/8286014
def resource_path(relative_path: str) -> str:
    """Gets the absolute path to a file, dealing with temp resource folders from PyInstaller

    :param relative_path: Path of a file in relative space
    :type relative_path: str
    :return: Absolute path to a resource
    :rtype: str
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def replace_instances(file: str, tags: list, out_file: str = "temp_", encoding: str = "utf-8"):
    """Takes a text file and replaces all instances of a tag with a string.

    :param encoding: Encoding to open and save to file with.
    :type encoding: str
    :param file: Path to file that will be modified
    :type file: str
    :param tags: List of tuples containing the tag and its replacement respectively
    :type tags: list
    :param out_file: (optional) File to write to. By default, a file named "temp_" will be created and then renamed
    to the original file
    :type out_file:
    """
    with open(file, "rt", encoding=encoding) as file_in:
        with open(out_file, "wt", encoding=encoding) as file_out:
            for line in file_in:
                replaced_line = line
                for tag in tags:
                    replaced_line = replaced_line.replace(tag[0], tag[1])

                file_out.write(replaced_line)

    print(f"Replaced tags in {file}")

    if out_file == "temp_":
        shutil.move("temp_", file)
        print("Renamed temp_ file")


@util.timeout.exit_after(300)  # 5 minutes
def is_open(process_name: str, sleep: float):
    """Checks if ``process_name`` is open every ``sleep`` seconds, and quits after 5 minutes of trying with a
    KeyboardInterrupt exception.

    :param process_name: Lowercase name of the process you want to catch
    :type process_name: str
    :param sleep: Amount of seconds to wait before trying again
    :type sleep: float
    """
    while process_name in (p.name().lower().removesuffix(".exe") for p in psutil.process_iter()):
        logging.info(f"{process_name} is running. Trying again in 20 seconds...")
        time.sleep(sleep)
