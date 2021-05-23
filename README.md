# OpenRCT2 Silent Launcher (aka Corkscrew)
A background updater for OpenRCT2. Instead of only updating when you launch the game, it runs on the background (system tray for Windows and background agent on macOS) periodically checking if an update was found and quitting if there's no work to be done.

## OPENRCT2 SILENT LAUNCHER IS, PARADOXICALLY, *NOT* A LAUNCHER!
Yes the name is wrong and the proper name that will be applied later is Corkscrew. What it does is run in the background (in the system tray on Windows and as an invisible Launch Agent in macOS) and checks for updates. If one is found, it quietly downloads and installs it. Also, if OpenRCT2 is **not installed**, it'll install the latest version automatically.

### Platforms Supported
- Windows
- macOS

### How to Install
At the moment there is no installer for this app, however that is planned for later releases. What you have to do to get it running and working is:

#### Windows
- Download compiled binaries from Releases
- Place it a safe place
- Create a task using Task Scheduler to run every X amount of time (6 hours is my personal preference)
- Run it by double clicking the .exe (optional)
- ???
- Profit

#### macOS
- Download compiled binaries from Releases
- Copy/move the application to your Applications folder
- Download `setup_agent.py` and `requirements.txt` files from the GitHub master
- Run `python3 -m pip install -r requirements.txt`
- Run `python3 setup_agents.py`
- The app will now be run immediately in the background and then every 6 hours
