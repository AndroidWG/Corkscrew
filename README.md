# Corkscrew
A background updater for OpenRCT2. Instead of only updating when you launch the game, it periodically runs in the background and silently downloads and installs new versions of the game.

## CORKSCREW IS *NOT* A LAUNCHER!
Corkscrew runs in the background (in the system tray on Windows and as an invisible Launch Agent in macOS) and checks for updates. If one is found, it quietly downloads and installs it, but **does not launch it.**
Also, if OpenRCT2 is **not installed**, it'll install the latest version automatically.

### Python Version
If you're running the source code, the minimum Python version you need is 3.6. If you download a binary from the Releases section, **you do not need Python installed.**

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
- ???
- Profit

#### macOS
- Download binaries from Releases
- Copy/move the application to your Applications folder
- Download `setup_agent.py` and `requirements.txt` files from the GitHub master
- Run `python3 -m pip install -r requirements.txt`
- Run `python3 setup_agents.py`
- The app will now be run immediately in the background and then automatically every 6 hours
