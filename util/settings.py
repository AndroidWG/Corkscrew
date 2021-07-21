import configparser
import logging
import os.path
import platform


class Settings:
    """This class is used so that everytime that a setting is changed it is saved on the app data folder."""
    __github_username: str
    __max_logs: int

    def __init__(self):
        self.app_data_path = setup_app_data_dir()
        self.logs_path = setup_logs_dir()
        self.__config_path = os.path.join(self.app_data_path, "settings.ini")

        self.__github_username = ""
        self.__max_logs = 25

        if os.path.exists(self.__config_path):
            config = configparser.ConfigParser()
            config.read(self.__config_path)

            handler = ConfigParserHandler(config)

            self.__github_username = handler.try_get_config("APP", "github_username", self.__github_username)
            self.__max_logs = int(handler.try_get_config("APP", "max_logs", self.__max_logs))

            self.save()

    @property
    def github_username(self):
        return self.__github_username

    @github_username.setter
    def github_username(self, value):
        self.__github_username = value
        self.save()

    @property
    def max_logs(self):
        return self.__max_logs

    @max_logs.setter
    def max_logs(self, value):
        self.__max_logs = value
        self.save()

    def save(self):
        config = configparser.ConfigParser()

        if not os.path.exists(self.__config_path):
            logging.debug("Creating config file...")
            config.add_section("APP")
        else:
            config.read(self.__config_path)

        config["APP"]["github_username"] = self.github_username
        config["APP"]["max_logs"] = str(self.__max_logs)
        with open(self.__config_path, "w") as file:
            config.write(file)


class ConfigParserHandler:
    """Handles KeyErrors when getting config values, returning the original value passed if key wasn't found."""
    def __init__(self, parser: configparser.ConfigParser):
        self.__parser__ = parser

    def try_get_config(self, group, key, original_value):
        try:
            value = self.__parser__[group][key]
            return value
        except KeyError:
            return original_value


def make_dir(path: str):
    print(f"Path chosen for app data: {path}")
    try:
        os.mkdir(path)
        print("Created dir")
    except FileExistsError:
        pass


def setup_app_data_dir() -> str:
    """Gets the folder where to store log files based on OS.

    :return: Path to logs folder.
    :rtype: str
    """
    current_platform = platform.system()

    if current_platform == "Windows":
        path = os.path.join(os.getenv("localappdata"), "Corkscrew")
        make_dir(path)
        return path
    elif current_platform == "Darwin":
        path = os.path.join(os.path.expanduser("~/Library/Application Support"), "Corkscrew")
        make_dir(path)
        return path
    else:
        return ""


def setup_logs_dir() -> str:
    """Gets the folder where to store app files, like settings files, based on OS.

    :return: Path to app data folder.
    :rtype: str
    """
    current_platform = platform.system()

    if current_platform == "Windows":
        path = os.path.join(os.getenv("localappdata"), "Corkscrew")
        make_dir(path)
        return path
    elif current_platform == "Darwin":
        path = os.path.join(os.path.expanduser("~/Library/Logs"), "Corkscrew")
        make_dir(path)
        return path
    else:
        return ""


local_settings = Settings()
