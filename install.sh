#!/bin/sh

set -e

# Script to install TextSuggest

# Check if running as root user
if [ $(id -u) -ne 0 ]; then
    echo "You have to run this script as root. Please enter your password."
    sudo $0
	exit
fi

echo "Verifying dependencies..."
echo "-------------------------"
if hash rofi 2>/dev/null; then
	echo "Rofi\tOK"
else
	echo "Rofi not installed!"
	exit 1
fi

if hash xclip 2>/dev/null; then
	echo "xsel\tOK..."
else
	echo "xsel not installed!"
	exit 1
fi

if hash xdotool 2>/dev/null; then
	echo "xdotool\tOK..."
else
	echo "xdotool not installed!"
	exit 1
fi

echo "\nAll dependencies OK!"

echo "\n"
echo "Installing..."
echo "--------------"

echo "Copying dictionaries..."
mkdir -p /usr/share/textsuggest/
cp -R textsuggest/* /usr/share/textsuggest/

echo "Copying configuration files..."
mkdir -p ~/.config/textsuggest

echo "Installing libraries..."
cp languages.py /usr/lib/python3.5/languages.py
cp fonts.py /usr/lib/python3.5/fonts.py
cp suggestions.py /usr/lib/python3.5/suggestions.py

echo "Installing textsuggest script to /usr/bin/textsuggest..."
cp TextSuggest.py /usr/bin/textsuggest
chmod a+x /usr/bin/textsuggest

echo "Installing manual page..."
cp docs/textsuggest.1 /usr/local/man/textsuggest.1
