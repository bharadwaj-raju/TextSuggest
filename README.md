# TextSuggest

Simple Linux utility to autocomplete words in the GUI.

![TextSuggest in action](http://i.imgur.com/BU0wFk1.gif)

Uses [Rofi](https://davedavenport.github.io/rofi/) for a simple popup menu.

Uses the [English Open Word List](http://dreamsteep.com/projects/the-english-open-word-list.html) for a basic dictionary. You can define custom words, see [the note](#custom-words).

Licensed under the [GNU GPL 3](https://www.gnu.org/licenses/gpl.txt).

# Installation

## Packages

Debian/Ubuntu `deb` package: [bharadwaj-raju/packages/TextSuggest/textsuggest_1.0_all.deb](https://github.com/bharadwaj-raju/packages/raw/master/TextSuggest/textsuggest_1.0_all.deb)

AUR (Arch User Repository): `textsuggest-git` (https://aur.archlinux.org/packages/textsuggest-git/, maintained by [Daniel Sandman (shellkr)](https://github.com/shellkr))

Now, see [Post-install](#post-install)

## Manual

Make sure you have all the requirements:

 - `xdotool`
 - `xclip`
 - `rofi` (Debian/Ubuntu and Arch package name: `rofi`)

Move `English/` into `~/.config/textsuggest/dictionaries/` and `Extra_Words.txt` into `~/.config/textsuggest/` directory.

Now, see [Post-install](#post-install)

## Post-install

Assign keyboard shortcuts to

- `python3 /path/to/TextSuggest.py`
- `python3 /path/to/TextSuggest.py --noselect`

**NOTE:** If you installed TextSuggest through the `deb` package, replace `python3 /path/to/TextSuggest.py` with just `textsuggest`.

The first one gives you suggestions on the currently highlighted word.
The second one simply gives you a list of all word, you can search through them.

The script stores frequently used words in a history file (`~/.config/textsuggest/history.txt`). Suggestions more often used
are at the top of list.

**TIP:** You can search for words by their parts by
typing `part1 part2 ... partN` at the `Type to search >` prompt.

# Options

- `--showerrors`

Instead of exiting silently when a word is not found, display a message for ~1 second.

- `--font "Font"`

Specify font to use in menu. Format: `FontName (Weight (optional) FontSize)`. Example: `--font Monaco Bold 10` or `--font Monaco 10`

- `--plainrofi`

Read Rofi settings from `~/.Xresources` (see Rofi documentation) or default.

- `--word "Word"`

Give suggestions for "Word" specified. Ignored if `--noselect`.

- `--nohistory`

Disable the history of frequently-used words (stored in `~/.config/textsuggest/history.txt`)

- `--language`

Manually set language, in case script fails to auto-detect from keyboard layout.

# Custom words

Simply add them to a `~/.Custom_Words.txt` file. The `Extra_Words.txt` file included already has a
few jargon, abbreviations and words (total 1653) not included in the EOWL.

You can also define expansions, in `~/.Custom_Words.txt`.
An entry for an expansion in the `~/.Custom_Words.txt` looks like:

    short=really_long_text_you_want_to_type

and will show up as `short=really_lon...` in the menu and when selected, will type `really_long_text_you_want_to_type`.

## Command outputs

Simply type `#command --options`, for example `#date -u`.

### Combining command outputs and expansions

Simply do:

    short_cmd=#long_command and --options

# Other langauges

Follow these steps:

- Get a suitable dictionary/wordlist for your language

- Move said dictionary into a new directory in `~/.config/textsuggest/dictionaries` with its name being your language's name.

- Pass a suitable font with the `--font` option

- Language should be auto-detected. If not, manually set language using the `--language` option.
