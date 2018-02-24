#!/bin/bash

# Copyright © 2016-2018 Bharadwaj Raju <bharadwaj DOT raju777 AT gmail DOT com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

set -e

# Script to install TextSuggest

# Check if running as root user
if [ "$(id -u)" -ne 0 ]; then
	echo "This script needs root (sudo) to run. Please enter your password:"
	sudo sh "$0" "$@"
	exit
fi


case "$1" in
	"--uninstall")
		echo "Uninstalling..."
		rm -rf /usr/share/textsuggest
		rm /usr/bin/textsuggest
		rm -rf /usr/lib/textsuggest
		rm -rf /usr/share/doc/textsuggest
		rm -rf /usr/share/licenses/textsuggest
		exit
		;;
esac

user_pre_sudo="$SUDO_USER"
user_home=$(eval echo "~$SUDO_USER")

echo $user_home


echo "Verifying dependencies..."

for dep in xclip xdotool; do
	if ! command -v "$dep" > /dev/null 2>&1; then
		echo "$dep not installed!"
		exit 1
	fi
done

if ! python3 -c 'from PyQt5 import Qt' > /dev/null 2>&1; then
	echo "PyQt5 not installed!"
	exit 1
fi

if ! python3 -c 'import dbus' > /dev/null 2>&1; then
	echo "python-dbus not installed!"
	exit 1
fi

if ! python3 -c 'from gi.repository import GObject' > /dev/null 2>&1; then
	echo "PyGObject not installed!"
	exit 1
fi

if ! python3 -c 'import pyperclip' > /dev/null 2>&1; then
	echo "pyperclip not installed!"
	exit 1
fi


echo -e "Installing..."

install -d /usr/share/textsuggest
install -d ${XDG_CONFIG_HOME:-$user_home/.config}/textsuggest
install -d ${XDG_CONFIG_HOME:-$user_home/.config}/textsuggest/processors
if [ ! -s ${XDG_CONFIG_HOME:-$user_home/.config} ]; then
	echo "{}" > ${XDG_CONFIG_HOME:-$user_home/.config}/textsuggest/custom-words.json
fi
cp -rf textsuggest/dictionaries/ /usr/share/textsuggest/
cp -rf textsuggest/processors/ /usr/share/textsuggest

install -D -m755 textsuggest.py /usr/share/textsuggest/textsuggest
install -D -m755 textsuggest-server.py /usr/share/textsuggest/textsuggest-server

install -D -m644 README.md /usr/share/doc/textsuggest/README

chmod 664 /usr/share/doc/textsuggest/README
install -D -m644 LICENSE /usr/share/licenses/textsuggest/COPYING

chown -R $user_pre_sudo ${XDG_CONFIG_HOME:-$user_home/.config}/textsuggest

ln -sf /usr/share/textsuggest/textsuggest.py /usr/bin/textsuggest
ln -sf /usr/share/textsuggest/textsuggest-server.py /usr/bin/textsuggest-server

chmod -R a+r /usr/share/textsuggest
chmod a+x /usr/bin/textsuggest
chmod a+x /usr/bin/textsuggest-server


