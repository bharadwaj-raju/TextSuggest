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
		rm /usr/bin/textsuggest-server
		rm -rf /usr/lib/textsuggest
		rm -rf /usr/share/doc/textsuggest
		rm -rf /usr/share/licenses/textsuggest
		exit
	;;
esac


echo "Verifying dependencies..."

for dep in xclip xdotool; do
	if ! command -v "$dep" > /dev/null 2>&1; then
		echo "$dep not installed!"
		exit 1
	fi
done

for dep in "libQt5Widgets" "libQt5Core" "libQt5Gui" "dbus-c++-1" "libpthread" "libxcb"; do
	if ! /sbin/ldconfig -p | grep "$dep" > /dev/null 2>&1; then
		echo "$dep not installed!"
		exit 1
	fi
done

echo -e "Installing..."

install -d /usr/share/textsuggest

cp -rf textsuggest/dictionaries/ /usr/share/textsuggest/

install -d /usr/share/textsuggest/processors
cp bin/math_expression /usr/share/textsuggest/processors
cp bin/command /usr/share/textsuggest/processors

install -D -m755 bin/textsuggest /usr/bin/textsuggest
install -D -m755 bin/textsuggest-server /usr/bin/textsuggest-server

chmod -R a+rwx /usr/share/textsuggest/processors

install -D -m644 README.md /usr/share/doc/textsuggest/README
install -D -m644 LICENSE /usr/share/licenses/textsuggest/COPYING

chmod -R a+rw /usr/share/textsuggest
chmod -R a+rw /usr/share/textsuggest/dictionaries
chmod -R a+rw /usr/share/textsuggest/dictionaries/*
chmod a+x /usr/bin/textsuggest
chmod a+x /usr/bin/textsuggest-server


