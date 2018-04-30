set -e

# Script to install TextSuggest

# Check if running as root user
if [ "$(id -u)" -ne 0 ]; then
	echo "This script needs root (sudo) to run. Please enter your password:"
	sudo sh "$0" "$@"
	exit
fi


if command -v apt > /dev/null 2>&1; then
	# Debian (based)
	apt install 'build-essential' 'qt5-default' 'qtbase5-dev' 'qt5-qmake' 'libdbus-c++-dev' 'dbus-c++' 'python-dbus'
	apt install 'xclip' 'xdotool'
elif command -v yum > /dev/null 2>&1; then
	# RedHat/RPM (based)
	yum install 'make' 'automake' 'gcc' 'gcc-c++' 'qt5-qtbase' 'qt5-devel' 'dbus-c++' 'dbus-c++-devel' 'dbus-python'
	yum install 'xclip' 'xdotool'
elif command -v pacman > /dev/null 2>&1; then
	# Arch (based)
	pacman -S 'dbus-c++' 'qt5-base' 'make' 'automake' 'gcc' 'python-dbus'
	pacman -S 'xclip' 'xdotool'
fi

sudo -u "$SUDO_USER" sh build.sh
sh install.sh

