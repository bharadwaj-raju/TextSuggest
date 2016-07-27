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

install -d /usr/share/
cp -rf textsuggest/ /usr/share/
install -D -m755 TextSuggest.py /usr/bin/textsuggest
install -D -m644 languages.py -t /usr/lib/python3.5/site-packages/
install -D -m644 fonts.py -t /usr/lib/python3.5/site-packages/
install -D -m644 suggestions.py /usr/lib/python3.5/site-packages/
install -D -m644 docs/textsuggest.1 -t /usr/share/man/man1/
install -D -m644 README.md /usr/share/doc/textsuggest/README
install -D -m644 LICENSE /usr/share/licenses/textsuggest/COPYING
