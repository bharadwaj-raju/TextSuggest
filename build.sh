#!/bin/bash

# Copyright © 2016-2018 Bharadwaj Raju <bharadwaj DOT raju777 AT gmail DOT com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

set -e

# Script to build textsuggest-ui

for dep in "g++" "qmake" "moc"; do
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


echo -e "Building..."

cd ui

qmake -makefile
make
mkdir -p ../bin
mv textsuggest ../bin/textsuggest
make clean
rm Makefile
rm .qmake.stash

cd ..

cd server
make
mkdir -p ../bin
mv textsuggest-server ../bin/textsuggest-server

cd ..

cd textsuggest/processors

for processor in "command" "math_expression"; do
	echo "g++ -Ofast -std=c++14 $processor.cpp -o $processor"
	g++ -Ofast "$processor.cpp" -o "$processor"
	mv "$processor" "../../bin/$processor"
done


echo "Finished building textsuggest"

