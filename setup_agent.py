import os
import shutil
import util
import logging
import subprocess
import log_setup

log_setup.setup_logging("macos_setup.log")
logging.info("Started first time setup")

launch_agents_path = os.path.expanduser("~/Library/LaunchAgents")
plist_name = "com.androidwg.openrct2silentlauncher.plist"
plist_path = os.path.join(launch_agents_path, plist_name)

resource_plist_path = util.resource_path(os.path.join("resources", plist_name))

logging.info("Copying plist to LaunchAgents")
shutil.copy(resource_plist_path, plist_path)

logging.debug("Loading plist with launchctl")
process = subprocess.Popen(["launchctl", "load", plist_path], stdout=subprocess.PIPE)
process.wait()

logging.debug("Starting plist with launchctl")
process = subprocess.Popen(["launchctl", "start", plist_name], stdout=subprocess.PIPE)
process.wait()
