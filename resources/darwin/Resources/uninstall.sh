#!/bin/bash

#Generate application uninstallers for macOS
#Parameters
INSTALL_PATH=#LOCATION#
PACKAGE=#PACKAGE#

#Check running user
if (( EUID != 0 )); then
    echo "Please run as root."
    exit
fi

echo "#NAME# v#VERSION# will be removed."
while true; do
    read -r -p "Do you wish to continue [Y/n]?" answer
    [[ $answer == "y" || $answer == "Y" || $answer == "" ]] && break
    [[ $answer == "n" || $answer == "N" ]] && exit 0
    echo "Please answer with 'y' or 'n'"
done

echo "Application uninstalling process started"

#Forget from pkgutil
pkgutil --forget "$PACKAGE" > /dev/null 2>&1
if [ $? -eq 0 ]
then
  echo "Successfully deleted application information"
else
  echo "[ERROR] Could not delete application information" >&2
fi

#Remove application source distribution
[ -e "$INSTALL_PATH" ] && rm -rf "$INSTALL_PATH"
if [ $? -eq 0 ]
then
  echo "Successfully deleted application"
else
  echo "[ERROR] Could not delete application" >&2
fi

echo "Application uninstall process finished"
exit 0
