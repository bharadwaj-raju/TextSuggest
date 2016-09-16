#!/bin/bash

set -e

# Script to install TextSuggest

# Check if running as root user
if [ "$(id -u)" -ne 0 ]; then
    echo "This script needs root rights to run. Please enter your password:"
	sudo "$@"
	exit
fi

case "$1" in
	"--uninstall")
		echo "Uninstalling..."
		rm -rf /usr/share/textsuggest
		rm /usr/bin/textsuggest
		rm /usr/lib/python3.5/site-packages/fonts.py
		rm /usr/lib/python3.5/site-packages/suggestions.py
		rm /usr/share/man/man1/textsuggest.1
		rm -rf /usr/share/doc/textsuggest
		rm -rf /usr/share/licenses/textsuggest
		exit
		;;
esac

echo "Verifying dependencies..."

for dep in rofi xsel xdotool; do
	if ! command -v "$dep" > /dev/null 2>&1; then
		echo "$dep not installed!"
		exit 1
	fi
done

echo -e "Installing..."

install -d /usr/share/textsuggest
cp -rf textsuggest/dictionaries/ /usr/share/textsuggest/
cp textsuggest/Extra_Words.txt /usr/share/textsuggest/
cp -rf textsuggest/processors/ /usr/share/textsuggest

install -D -m755 TextSuggest.py /usr/bin/textsuggest

if python3 -c 'import sys; print(sys.path)' | grep 'site-packages' > /dev/null; then
	install -D -m644 languages.py -t /usr/lib/python3.5/site-packages/
	install -D -m644 fonts.py -t /usr/lib/python3.5/site-packages/
	install -D -m644 suggestions.py /usr/lib/python3.5/site-packages/
else
	install -D -m644 languages.py -t /usr/lib/python3.5/
	install -D -m644 fonts.py -t /usr/lib/python3.5/
	install -D -m644 suggestions.py /usr/lib/python3.5/
fi

install -D -m644 docs/textsuggest.1 -t /usr/share/man/man1/
install -D -m644 README.md /usr/share/doc/textsuggest/README

# Strip README of special prettifying (to make it look good online)
sh docs/readme_strip_special_formatting.sh > /usr/share/doc/textsuggest/README
chmod 664 /usr/share/doc/textsuggest/README
install -D -m644 LICENSE /usr/share/licenses/textsuggest/COPYING

chmod -R a+r /usr/share/textsuggest
chmod a+x /usr/bin/textsuggest

