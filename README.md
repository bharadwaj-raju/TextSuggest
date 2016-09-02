# TextSuggest

Save keystrokes, use [word expansions](#custom-words), type results of [math](#math), [commands](#commands) and more.

A utility to autocomplete words in the GUI.

[![TextSuggest in action](http://i.imgur.com/qa2PExH.gif)](http://i.imgur.com/qa2PExH.gif)

Licensed under the [GNU GPL 3](https://www.gnu.org/licenses/gpl.txt). TextSuggest is free as in freedom.

## Overview

TextSuggest is a script that, when a [keyboard shortcut](#post-install) is pressed, shows completions for the word selected or [currently being typed](#auto-selection).

Then you can efficiently search for the right word with smart search (thanks to [Rofi](https://github.com/DaveDavenport/Rofi)) and hit Enter to choose. Or Esc to exit.

An [alternative background service](#textsuggestd) that intelligently offers completions when appropriate, without the need of pressing a shortcut is in development.

## Installation

### Packages

#### [![Ubuntu](https://www.pylint.org/assets/img/ubuntu.png)](https://ubuntu.com) Ubuntu and Debian

[Download `textsuggest-git.deb`](https://github.com/bharadwaj-raju/packages/raw/master/TextSuggest/textsuggest-git.deb)

#### [![Arch Linux](https://www.pylint.org/assets/img/arch.png)](https://archlinux.org) Arch Linux

AUR (Arch User Repository): [`textsuggest-git`](https://aur.archlinux.org/packages/textsuggest-git/), submitted by [Daniel Sandman (shellkr)](https://github.com/shellkr)

Both packages build from this Git repository.

Now, see [Post-install](#post-install)

### Manual

Make sure you have all the requirements:

 - `xdotool`
 - `xsel`
 - `rofi`

Run the included install script with `sudo ./install.sh`.

Now, see [Post-install](#post-install)

### Post-install

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

If you installed it using [Packages](#packages), use your system's package manager.

Otherwise:

```bash
$ sudo ./install.sh --uninstall
```

To also remove configuration files, use

```bash
$ sudo ./install.sh --uninstall-full
```

## Options

Documented in the manual page: `man textsuggest` and `--help`.

## Expansions

TextSuggest can handle a range of expansions:

### Custom words

Simply add them to `~/.config/textsuggest/Custom_Words.txt` like this:

    custom=My custom Expansion!

and whenever 'custom' is typed, 'My custom Expansion!' will be inserted.

### Commands

Similar to `bash`'s `$()`, it inserts the output of a command:

    #ls

when typed into a TextSuggest window, will insert output of `ls`

#### Custom words + Commands

Add in `~/.config/textsuggest/Custom_Words.txt`:

    custom=#command --opts

and whenever you type 'custom' into TextSuggest, the output of `command --opts` will be inserted.

### Math

Simply type into TextSuggest:

    %2 + 3

And '5' will be inserted. You can do any math expression that Python supports.

#### Custom Words + Math

Add in `~/.config/textsuggest/Custom_Words.txt`:

    custom=%2+3

And whenever you type 'custom' into TextSuggest, 5 will be inserted.

## Other langauges

English and Bangla dictionaries are provided by default.

For other langauges, follow these steps:

- Get a suitable dictionary/wordlist for your language. Search online for "<language name> wordlist" or "<language name> dictionary".

- Move said dictionary into a new directory in `/usr/share/textsuggest/dictionaries` with its name being your language's name (English name, like "German" instead of "Deutsch").

- A suitable font should be auto-detected. If not, pass a suitable font with the `--font` option.

- Language should be auto-detected. If not, manually set language using the `--language` option.

## textsuggestd

`textsuggestd` is a work-in-progress background service that automatically launches TextSuggest when appropriate.

It is an effort to achieve TextSuggest's final goal: to be like the suggestions on mobile phones, which appear without stealing focus and disrupting typing, and without having to press shortcuts.

### Running textsuggestd

**WARNING**: It is almost unusable. See [escaping](#escaping-textsuggestd).

Simply do:

```bash
$ ./textsuggestd &
```

### Escaping textsuggestd

Get to a terminal somehow (TTY, maybe?) and run:

```bash
for i in $(pgrep python3); do
    ps -fp $i | grep 'textsuggestd' && kill $i
done
```
