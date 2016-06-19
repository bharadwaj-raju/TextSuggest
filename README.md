# TextSuggest

Simple Linux utility to autocomplete words in the GUI.

![TextSuggest in action](http://i.imgur.com/BU0wFk1.gif)

**NOTE:** If you have not installed `dmenu2` (an extended fork of `dmenu`), you will see the suggestion bar at the bottom of the screen. To get the menu in the video, see [note](#note-on-dmenu).

Uses the [English Open Word List](http://dreamsteep.com/projects/the-english-open-word-list.html) for a basic dictionary. You can define custom words, see [the note](#custom-words).

Licensed under the [GNU GPL 3](https://www.gnu.org/licenses/gpl.txt).

# Installation

`deb` package: [bharadwaj-raju/packages/TextSuggest/textsuggest_1.0_all.deb](https://github.com/bharadwaj-raju/packages/raw/master/TextSuggest/textsuggest_1.0_all.deb)

Make sure you have all the requirements:

 - `xdotool`
 - `xclip`
 - `dmenu` (See [note](#note-on-dmenu))

Assign keyboard shortcuts to

- `python3 /path/to/TextSuggest.py`
- `python3 /path/to/TextSuggest.py --noselect`

**NOTE:** If you installed TextSuggest through the `deb` package, replace `python3 /path/to/TextSuggest.py` with just `textsuggest`.

The first one gives you suggestions on the currently highlighted word.
The second one simply gives you a list of all word, you can search through them.

The script stores frequently used words in a history file (`~/.textsuggest_history.txt`). Suggestions more often used
are at the top of list.

**TIP:** You can search for words by their parts by
typing `part1 part2 ... partN` at the `Type to search >` prompt.

# Custom words

Simply add them to a `~/.Custom_Words.txt` file. The `Extra_Words.txt` file included already has a
few jargon, abbreviations and words (total 1653 by default) not included in the EOWL.

You can also define expansions, in `~/.Custom_Words.txt`.
An entry for an expansion in the `~/.Custom_Words.txt` looks like:

    short=really_long_text_you_want_to_type

and will show up as `short=really_lon...` in the menu and when selected, will type `really_long_text_you_want_to_type`.

## Command outputs

You can also make it type shell command outputs, define them in `~/.Custom_Words.txt` like this:

    #shell_command

For example, a `#date` definition will type out the ouput of Unix `/bin/date`.

If you want the output of a shell command *not* defined, then simply type `#command` at the `Type to search >` prompt.

### Combining command outputs and expansions

Simply do:

    short_cmd=#long_command and --options

# Note on dmenu

`dmenu` is contained in the `suckless-tools` package in Debian/Ubuntu. The `.deb` package automatically installs the better `dmenu2` instead of the older `dmenu` in `suckless-tools`

For a better search menu, with position at mouse cursor instead of bottom and compact size,
Install `dmenu2`, an extended fork of `dmenu`, by Michał Lemke at [melek/dmenu2](https://bitbucket.org/melek/dmenu2).

TextSuggest assumes that you have `dmenu2` installed. If you want to use the old `dmenu`, pass the `--olddmenu` option.
