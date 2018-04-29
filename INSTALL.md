# Installing TextSuggest

## Easiest method: download built release and install

Run the `download-install.sh` script.


## Build and install yourself

Make sure you have the development tools:

  - `g++`
  - Qt 5 development libraries
  - `qmake` and `moc` (should come as part of Qt SDK)
  - `dbus-c++` development headers

Download the source. `cd` into it.

Now, run `build.sh`, then `sudo sh install.sh`.