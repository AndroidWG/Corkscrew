# Corkscrew
A background updater for OpenRCT2. Instead of only updating when you launch the game, it periodically runs in the background and silently downloads and installs new versions of the game.

## CORKSCREW IS *NOT* A LAUNCHER!
Corkscrew runs in the background and checks for updates regularly. If one is found, it quietly downloads and installs it, but **does not launch it.**
Also, if OpenRCT2 is not installed, it'll install the latest version automatically.

### How to Install
[Go to the Releases page](https://github.com/AndroidWG/Corkscrew/releases) and download the latest version for your OS and install it. The installer will create a Task on Windows and a LaunchAgent for macOS that will check for updates every 4 hours.

If you are on Windows 10 and have winget, just type `winget install androidWG.Corkscrew` to download Corkscrew.

### Platforms Supported
- Windows
- macOS

#### Why no Linux?
OpenRCT2 has packages for the most popular package managers out there. Since I assume most people will run `sudo apt-get upgrade` (or the equivalent for your distro) semi-frequently, I considered Windows and macOS as the primary platforms I should focus on.

### Logs & Settings
The app keeps the log of the last 25 times it was run (this is configurable in the settings file). Settings are stored in the same folder in Windows.

| Type         | Windows                    | macOS                                     |
|--------------|----------------------------|-------------------------------------------|
| Logs         | `%LOCALAPPDATA%\Corkscrew` | `~/Library/Logs/Corkscrew`                |
| Settings     | `%LOCALAPPDATA%\Corkscrew` | `~/Library/Application Support/Corkscrew` |

Please post your log *in full* on a website like [pastebin](https://pastebin.com/) when opening an Issue.

### Building from Source
Python 3.6 or newer is needed. Run `python -m pip install -r requirements.txt` to install required packages and then run `python build/build.py` **from the root folder**. An executable file for your OS will be created on the `dist` folder in the repo's root directory.

You can add the flag `--no-installer` if you don't want the script to make an installer.

> **NOTE:** On macOS, run `python3` instead of `python`
 
#### Installer
The Build script will generate an installer by default. In Windows, it'll use Inno Setup 6 installed at C:\Program Files (x86)\Inno Setup 6 (change that path in `build/installer.py` if you need it).

Installers will be named ready to be added to a GitHub Release, and will use the version string specified in `main.py`.
