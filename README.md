# TextSuggest
### Universal Autocomplete

Autocomplete, text expansion, etc, in all GUI apps (on X11).

TextSuggest supports [multiple languages](#other-languages) and [extensions](#extensions).

<!--**Click the image to view a GIF demo.**-->

![TextSuggest in action](img/demo.png)

Licensed under the [GNU GPL 3](https://www.gnu.org/licenses/gpl.txt). TextSuggest is free as in freedom.

[Acknowledgements for the dictionaries.](#dictionary-credits)

## Overview

TextSuggest is a program that shows completions for the word selected or (optionally) [currently being typed](#auto-selection).

It can be easily bound to a keyboard shortcut.

### Features

  - Fast
  - Autocomplete in all GUI apps
  - Text expansions (including shell commands, math, etc)
  - Fuzzy matching (e.g. 'exmy' matches 'extremely', 'empnt' matches 'employment', etc)
  - Very configurable
  - History (more used words rise to the top)
  - Native (Qt 5) UI


## Installation

Make sure you have all the requirements:

  - `xdotool`
  - `xclip`
  - `PyQt5`
  - `python-dbus`
  - `pyperclip` (from `pip install pyperclip`)

Then run the included install script with `sudo ./install.sh`.

**Now, see [Post-install](#post-install)**


### Post-install

Run the command `textsuggest-server` in the background, and set it to run on startup.

Set the command `textsuggest` to a keyboard shortcut. Type a word, select it, press the shortcut and TextSuggest will give you autocomplete.

This offers the most basic use of TextSuggest. For more, see [options](#options) and browse through the rest of this page.

### Uninstallation

If you installed it using packages, use your system's package manager.

Otherwise use `sudo ./install.sh --uninstall`.

## Options

    $ textsuggest --help
	usage: textsuggest [options]

	TextSuggest — universal autocomplete

	optional arguments:
	  
	  -h, --help            show this help message and exit
	  
	  --word WORD [...]
	                        Specify word to give suggestions for. Default: all words. 
	                         
	  --no-history          Disable the frequently-used words history (stored in ~/.config/textsuggest/history.txt) 
	                         
	  --language languages [...]
	                        Set language(s). Default: English. See also: --auto-detect-language. 
	                         
	  --auto-detect-language
	                        Auto-detect language from keyboard layout. 
	                         
	  --selection           Show suggestions for currently selected word. See also: --auto-selection 
	                         
	  --auto-selection [beginning|middle|end]
	                        Automatically select word under cursor and suggest. Ignored if --no-selection. 
	                         
	  --custom-words-only   Show custom words only. 
	                         
	  --no-processing       Disable using of any processors. 
	                         
	  -v, --version         Print version and license information.


## Expansions

TextSuggest can handle a range of expansions. It can also be [extended](#extensions).

### Custom words

Simply add them to `~/.config/textsuggest/custom-words.json` in a JSON format like this:

	{
	    "custom": "Expansion",
	    "another": "Another expansion"
	}

and whenever 'custom' is typed, 'Expansion' will be typed. Similarly for 'another' ('Another expansion').

### Commands

Inserts the output of a command:

    #ls -l

when typed into a TextSuggest window, will insert output of `ls -l` as if it was run in a shell.

#### Custom words + Commands

Add in `~/.config/textsuggest/Custom_Words.txt`:

    "custom": "#command --opts"

and whenever you type 'custom' into TextSuggest, the output of `command --opts` will be inserted.

### Math

Simply type into TextSuggest:

    = 2 + 3

And '5' will be inserted. You can do any math expression that Python supports.

You can also use any function in the Python [`math`](https://docs.python.org/3/library/math.html) library, for example `= sqrt(25)` for √25.

#### Custom Words + Math

Add in `~/.config/textsuggest/Custom_Words.txt`:

    "custom": "= 2 + 3"

And whenever you type 'custom' into TextSuggest, 5 will be inserted.

## Extensions

TextSuggest supports powerful *processors* for extensions.

A processor *processes* text before handing it over to TextSuggest to type it out.
By default TextSuggest has two processors, [`command`](#commands) and [`math_expression`](#math).

You can see this in TextSuggest output:

```bash
$ textsuggest --all-words
Running in insert mode.
Chosen word: =2 + 3
Using processor math_expression from /usr/share/textsuggest/processors/math_expression.py
Processed: 5
```

### Making your own extension

A *processor* is a simple Python script, that *must* define two functions, `matches()` and `process()`. Look into this example:

```python
def matches(text):

	# Return whether this processor should process 'text' or not. (True or False)
	# For example, the command processor has it like this:
	#     return True if text.startswith('#') else False

def process(text):

	# Do something with 'text' and return it.
	# You *must* return a string.
	# This is what will be finally typed.
```

Make one based on the sample above, and place it in `~/.config/textsuggest/processors/` (file must end with `.py` extension).

Processors in `~/.config/textsuggest/processors` take precedence over those in `/usr/share/textsuggest/processors`, in case of a name or match conflict.

You can set the order of loading of processors by creating a file called `load-order.txt` in the processor directory, which should have a newline-separated list of processors. The processors will then load in that order.

## Other languages

English and Bangla dictionaries are provided by default.

By default, only the English dictionary will be used.

You can change this by:

  - Auto-detect language from keyboard layout: Use the option `--auto-detect-language`. The mapping of layouts to languages is given below:
    - `bd` → Bangla
    - `us` → English
    - `uk` → English
    - `gb` → English
    - `cn` → Chinese
    - `ar` → Arabic
    - `tw` → Chinese
    - `de` → German
    - `jp` → Japanese
    - `ru` → Russian
    - `es` → Spanish
    - `se` → Swedish
    - `fi` → Finnish
    - `kr` → Korean
    - `pk` → Urdu
    - `fr` → French
    - `gr` → Greek
    - `ua` → Ukrainian

  - Manually specify the language(s) to use. For example, `--language English German`.

TextSuggest will then use `<language name>.txt` file(s) (if they exist) in `/usr/share/textsuggest/dictionaries`.


## Dictionary Credits

- English:
  Oxford 3k wordlist (filtered to only include words with >= 5 chars)

- Bangla:
  Contributed by @maateen