This folder has some resources needed to build a macOS Product Installer. To make sure we don't need to retype the names if anything changes, there are a few "tags" that are replaced with the function `macos_installer.replace_instances()`. These are:

- `#NAME#` | Name of the program used throughout this code, and is used in all lowercase when necessary.
- `#VERSION#` | String with version in format `0.0.0`
- `#PACKAGE#` | Package name, in the format of an inverted domain, like `com.apple.siri`
- `#LOCATION#` | Where the thing was installed