cd /tmp

echo "Downloading latest release..."

wget https://github.com/bharadwaj-raju/TextSuggest/releases/latest/TextSuggest.zip
unzip TextSuggest.zip

cd TextSuggest

# This prebuilt ZIP from the Releases page contains the textsuggest binary already built

echo "Installing..."
echo "Please enter your password."

sudo sh install.sh
