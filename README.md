# Corkscrew
A background updater for OpenRCT2. Instead of only updating when you launch the game, it periodically runs in the background and silently downloads and installs new versions of the game.

## CORKSCREW IS *NOT* A LAUNCHER!
Corkscrew runs in the background (in the system tray on Windows and as an invisible Launch Agent in macOS) and checks for updates. If one is found, it quietly downloads and installs it, but **does not launch it.**
Also, if OpenRCT2 is **not installed**, it'll install the latest version automatically.

### Platforms Supported
- Windows
- macOS

### How to Install
At the moment there is no installer for this app, however that is planned for later releases. What you have to do to get it running and working is:

#### Windows
- Download .exe from Releases
- Place it a safe location, that won't be deleted
- Create a task using Task Scheduler to run every X amount of time
- Run it by double-clicking the .exe (optional)
    - A tray icon will appear, and disappear as soon as it's finished. If an update is not found for example, it'll show up and disappear after a few seconds.

#### macOS
- Download binaries from Releases
- Copy/move the application to your Applications folder
- Download `setup_agent.py` and `requirements.txt` files from `dev_tools` folder
- Run `python3 -m pip install -r requirements.txt`
- Run `python3 dev_tools/setup_agents.py`
- The app will now be run immediately in the background and then automatically every 6 hours

### Logs
The app keeps the log of the last execution. It can be found here:

| Windows                    | macOS                      |
|----------------------------|----------------------------|
| `%LOCALAPPDATA%\Corkscrew` | `~/Library/Logs/Corkscrew` |

If you use macOS and you ran the `setup_agent.py` script you'll see a second log file named `macos_setup.log`. This is only needed if you had issues with that script.

Please post your log **in full** on a website like [pastebin](https://pastebin.com/) when opening an Issue.

### Building
Python 3.6 or newer is needed. Simply run `python -m pip install -r requirements.txt` and then `python dev_tools/build.py`. An executable file for your OS will be created on the `dist` folder inside the repo's root directory.