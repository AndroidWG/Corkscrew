import configparser
import logging
import os.path
import platform


class Settings:
    """This class is used so that everytime that a setting is changed it is saved on the app data folder."""
    def __init__(self):
        self.app_data_path = setup_app_data_dir()
        self.__config_path = os.path.join(self.app_data_path, "settings.ini")
        self.__github_username = ""

        if os.path.exists(self.__config_path):
            config = configparser.ConfigParser()
            config.read(self.__config_path)

            self.__github_username = config["APP"]["github_username"]

    @property
    def github_username(self):
        return self.__github_username

    @github_username.setter
    def github_username(self, value):
        self.__github_username = value
        self.save()

    def save(self):
        config = configparser.ConfigParser()

        if not os.path.exists(self.__config_path):
            logging.debug("Creating config file...")
            config.add_section("APP")
        else:
            config.read(self.__config_path)

        config["APP"]["github_username"] = self.github_username
        with open(self.__config_path, "w") as file:
            config.write(file)


def setup_app_data_dir() -> str:
    """Gets the folder where to store app files like settings based on OS.

    :return: Path to app data folder.
    :rtype: str
    """
    current_platform = platform.system()

    if current_platform == "Windows":
        return os.path.join(os.getenv("localappdata"), "Corkscrew")
    elif current_platform == "Darwin":
        return os.path.join(os.path.expanduser("~/Library/Logs"), "Corkscrew")
    else:
        return ""


local_settings = Settings()
