textsuggest(1) -- X11 utility to autocomplete words in the GUI
==============================================================

## SYNOPSIS

  `textsuggest` \[`--help`\] \[`--word` *word* ...\] \[`--no-rofi-customization`\] \[`--font` *font*\] \[`--no-history`\] \[`--language` *language*\] \[`--no-selection`\]

## DESCRIPTION

  https://github.com/bharadwaj-raju/TextSuggest

  textsuggest is a simple X11 utility that autocompletes, suggests and expands words in the GUI.

## USAGE

  textsuggest has two modes:

   - 'replace' mode: Suggests word completions based on current X11 selection contents. Default.
   - 'insert' mode : Gives a list of all known words, allowing you to search them and choose one. Activated with `--no-selection` option.

  Thus, assign two keyboard shortcuts:

   - `textsuggest` for replace mode
   - `textsuggest --no-selection` for insert mode

## OPTIONS

  `--help`, `-h`
   View a short summary of options.

   `--word` *word*
   Instead of suggesting words based on X11 selection contents, suggest based on *word* specified. Ignored if `--no-selection`.

  `--auto-selection *[beginning|middle|end]*`

  Automatically select words for you before suggestion, saving time and (your) keystrokes. Ignored if `--no-selection`.

  `--auto-selection` has three modes:

  - 'beginning': Assumes text-cursor is at beginning of word.
  - 'middle'   : Assumes text-cursor is somewhere in the middle of word.
  - 'end'      : Assumes text-cursor is at end of word. Default.

  The three choices help choose the keyboard shortcut to be pressed. It would be good to auto-detect the option
  according to the text-cursor's position, but X11 does not provide this.

**NOTE:** The normal "you select text and textsuggests suggests on that" will **not** work with this enabled.

   `--no-rofi-customization`
   Do not apply custom Rofi theme.

   `--font` *font*
   Instead of selecting font based on language (default: Monospace 10), use *font* specified. *font* must be in Pango format: `FontName (Weight) Size`

   `--no-history`
   Disable frequently-used words history (stored in `~/.config/textsuggest/history.txt`)

   `--language` *language*
   Instead of auto-detecting language based on keyboard layout, use *language* specified.

## OTHER LANGUAGES

  By default, English and Bangla dictionaries are provided. To add support for other languages, follow these steps:

  - Get a suitable dictionary/wordlist for your language. Search for '<your language> wordlist' online.
  - After downloading said dictionary (which should be in this format: a `<your language>` directory, with one or more text files with words in them), move it into `/usr/share/textsuggest` directory.

  You're done. The language should be auto-detected, otherwise set langauge with `--language`. A suitable font should also be auto-detected, otherwise set font with `--font`.

## RETURN CODES

  - 0 : Success
  - 1 : No words found
  - 2 : Cancelled by user

## AUTO-SELECTION

  Automatically select word under cursor for you before suggestion, saving time and keystrokes.

  `--auto-selection` has three modes:

  - 'beginning': Assumes text-cursor is at beginning of word.
  - 'middle'   : Assumes text-cursor is somewhere in the middle of word.
  - 'end'      : Assumes text-cursor is at end of word. Default.

  The three choices help choose the keyboard shortcut to be pressed. It would be good to auto-detect the option
  according to the text-cursor's position, but X11 does not provide this.

  **NOTE:** The normal "you select text and textsuggests suggests on that" will **not** work with this enabled.

## BUGS AND FEATURE REQUESTS

  Please file bug reports and feature requests at the GitHub repository: https://github.com/bharadwaj-raju/TextSuggest

## SEE ALSO

  - `textsuggestd(1)`
