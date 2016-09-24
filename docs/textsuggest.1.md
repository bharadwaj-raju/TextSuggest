textsuggest(1) -- X11 utility to autocomplete words in the GUI
==============================================================

## SYNOPSIS

  `textsuggest` \[`--help`\] \[`--word` *word* ...\] \[`--no-rofi-customization`\] \[`--font` *font*\] \[`--no-history`\] \[`--language` *language*\] \[`--no-selection`\]

## DESCRIPTION

  https://github.com/bharadwaj-raju/TextSuggest

  textsuggest (or TextSuggest) is a simple X11 utility that saves you keystrokes by autocompleting, suggesting and expanding words.

## USAGE

  Call `textsuggest` to get suggestions, completions etc. See also the **OPTIONS** section.

  For convenience, bind the script to a keyboard shortcut(s):

   - `textsuggest` for replace mode (suggestions for a specific word, taken from X11 selection (see `xsel(1)`) if `--word` is not given)
   - `textsuggest --all-words` for insert mode (get all words)

   Also see the **AUTO-SELECTION** section.

## OPTIONS

  `-h`, `--help`            show a summary of options and exit

  `--word` *word* ...
                        Specify word to give suggestions for. Default: taken from X11 clipboard. Ignored if --no-selection.

  `--all-words`
                        Give all words as suggestions, which you can then filter.

  `--font` *font*
                        Specify font for Rofi. Must be in Pango format: FontName (Weight (optional) FontSize).

  `--no-history`          Disable the frequently-used words history (stored in ~/.config/textsuggest/history.txt)

  `--exit-if-no-words-found`
                        Exit if no words are found (instead of restarting in --no-selection mode)

  `--language` *languages* ...   Manually set language(s), in case script fails to auto-detect from keyboard layout.

  `--auto-selection` *[beginning|middle|end]*
                        Automatically select word under cursor and suggest. See **AUTO-SELECTION**. Ignored if --no-selection.

  `--no-processing`       Disable using of any processors.

  `--rofi-options` *options* ...
                        Specify additonal options to pass to Rofi.

  `--force-gtk3-fix`		Always use the GTK+ 3 workaround. If not specified, it is detected whether use is applicable.

  `-v`, `--version`         Print version and license information.



## EXPANSIONS

  **COMMANDS**

  Use `#command` in TextSuggest to type out the output of `command`.

  **MATH**

  Use `%2+3` in TextSuggest to insert the answer of `2+3`. Can be used with any math valid in `python3(1)`, in addition to its `math` library.

  **ALIASES**

  Define them in `~/.config/textsuggest/Custom_Words.txt`:

  short=really long text!

  Can be combined with **COMMANDS** and **MATH** above.

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

## EXTENSIONS

  TextSuggest supports powerful extensions via it's *processors*.

  A processor does changes to the word chosen by the user and returns it to TextSuggest to type out.

  TextSuggest includes two processors by default: `command` and `math_expression` (see **EXPANSIONS**).

  **Making your own**

  A processor is simply a `python3(1)` script that defines at least two functions:

  - `matches(text)`: Return if `text` should be processed or not (processor's choice)
  - `process(text)`: Return a string containing changed/modified `text`

  Optionally it may define a `process_all` variable, whose valuse may be:

  - `"first"`: To first process text through this processor before any others.
  - `"last"`: After all processors have processed, process the text through this

## BUGS AND FEATURE REQUESTS

  Please file bug reports and feature requests at the GitHub repository: https://github.com/bharadwaj-raju/TextSuggest/issues

  Please include the output of `textsuggest --version` in the report/request.

## SEE ALSO

  - `textsuggestd(1)`
  - `xsel(1)`
  - `xdotool(1)`
  - `python3(1)`
