# TextSuggest

X11 utility to autocomplete words in the GUI.

[![TextSuggest in action](http://i.imgur.com/qa2PExH.gif)](http://i.imgur.com/qa2PExH.gif)

Uses [Rofi](https://davedavenport.github.io/rofi/) for a simple popup menu.
Uses a few libraries (in `libscreenkey/`) from [Screenkey](https://github.com/wavexx/Screenkey).

Uses the [English Open Word List](http://dreamsteep.com/projects/the-english-open-word-list.html) for a basic English dictionary, plus a Bangla dictionary ported from [ibus-avro](https:github.com/sarim/ibus-avro). For other languages, see the [Other languages](#other-languages) section.

You can define custom words, see [the note](#custom-words).

Licensed under the [GNU GPL 3](https://www.gnu.org/licenses/gpl.txt). TextSuggest is free as in freedom.

# Installation

## Packages

### [![Ubuntu](https://www.pylint.org/assets/img/ubuntu.png)](https://ubuntu.com) Ubuntu and Debian

Debian/Ubuntu `deb` package: [Download `textsuggest-git.deb`](https://github.com/bharadwaj-raju/packages/raw/master/TextSuggest/textsuggest-git.deb)

### [![Arch Linux](https://www.pylint.org/assets/img/arch.png)](https://archlinux.org) Arch Linux

AUR (Arch User Repository): [`textsuggest-git`](https://aur.archlinux.org/packages/textsuggest-git/), maintained by [Daniel Sandman (shellkr)](https://github.com/shellkr)

Both packages build from this Git repository.

Now, see [Post-install](#post-install)

## Manual

Make sure you have all the requirements:

 - `xdotool`
 - `xsel`
 - `rofi` (Debian/Ubuntu and Arch package name: `rofi`)

Run the included install script with `sudo ./install.sh`.

Now, see [Post-install](#post-install)

See also: [Uninstallation](#uninstallation)

## Post-install

Assign keyboard shortcuts to

- `textsuggest`
- `textsuggest --no-selection`

The first one gives you suggestions on the currently highlighted word.
The second one simply gives you a list of all word, you can search through them.

The two commands offer the most basic of TextSuggest features. For more, see [options](#options)

The script stores frequently used words in a history file (`~/.config/textsuggest/history.txt`). Suggestions more often used
are at the top of list. History can be disabled: use the `--no-history` option.

**TIP:** You can search for words by their parts by
typing `part1 part2 ... partN` at the `Type to search >` prompt.

### Uninstallation

Run:

```bash
$ sudo ./install.sh --uninstall
```

To also remove configuration files, use

```bash
$ sudo ./install.sh --uninstall-full
```

# Options

Documented in the manual page: `man textsuggest` and `TextSuggest.py --help`.

# Expansions

TextSuggest can handle a range of expansions

## Custom words

Simply add them to `~/.config/textsuggest/Custom_Words.txt` like this:

    custom=My custom Expansion!

and whenever `custom` is typed, 'My custom Expansion!' will be inserted.

## Command expansions

Similar to `bash`'s `$()` syntax, it inserts the output of a command:

    #ls

when typed into a TextSuggest window, will insert output of `ls`

### Custom words + Command expansions

Add in `~/.config/textsuggest/Custom_Words.txt`:

    custom=#command --opts

and whenever you type `custom` into TextSuggest, the output of `command --opts` will be inserted.

## Math

Simply type:

    %2 + 3

And '5' will be inserted. You can do any math expression that Python supports.

### Custom Words + Math

Add in `~/.config/textsuggest/Custom_Words.txt`:

    custom=%2+3

And whenever you type 'command' into TextSuggest, 5 will be inserted.

# Other langauges

English and Bangla dictionaries are provided by default.

For other langauges, follow these steps:

- Get a suitable dictionary/wordlist for your language. Search online for "<language name> wordlist" or "<language name> dictionary".

- Move said dictionary into a new directory in `/usr/share/textsuggest/dictionaries` with its name being your language's name (English name, like "German" instead of "Deutsch").

- A suitable font should be auto-detected. If not, pass a suitable font with the `--font` option.

- Language should be auto-detected. If not, manually set language using the `--language` option.
