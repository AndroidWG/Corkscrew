import os
import shutil
import sys


# From https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a#file-print_progress-py
def print_progress(iteration: int, total: int, prefix: str = '', suffix: str = '', decimals: int = 1,
                   bar_length: int = 100):
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
    :param bar_length: How many long the progress bar is (doesn't include suffix, prefix and other chars)
    :type bar_length: int
    """
    # TODO: add auto width using os.get_terminal_size()

    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    ready_to_print = ('%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix))

    print(ready_to_print, end="\r", flush=True)

    if iteration == total:
        print('\n')


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


def replace_instances(file: str, tags: list[tuple[str, str]], out_file: str = "temp_"):
    """Takes a text file and replaces all instances of a tag with a string.

    :param file: Path to file that will be modified
    :type file: str
    :param tags: List of tuples containing the tag and its replacement respectively
    :type tags: list
    :param out_file: (optional) File to write to. By default, a file named "temp_" will be created and then renamed to the original file
    :type out_file:
    """
    with open(file, "rt") as file_in:
        with open(out_file, "wt") as file_out:
            for line in file_in:
                replaced_line = line
                for tag in tags:
                    replaced_line = replaced_line.replace(tag[0], tag[1])

                file_out.write(replaced_line)

    print(f"Replaced tags in {file} to temp_ file")

    if out_file == "temp_":
        shutil.move("temp_", file)
        print("Renamed temp_ file")
