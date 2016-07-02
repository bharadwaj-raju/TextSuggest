#!/usr/bin/env python3
# coding=utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# Contributor: Maksudur Rahman Maateen <ugcoderbd@gmail.com>

# Licensed under the GNU General Public License 3 (https://www.gnu.org/licenses/gpl.txt)

# A simple linux tool to autocomplete text inputs in the GUI

# Uses the English Open Word List (http://dreamsteep.com/projects/the-english-open-word-list.html)
# Plus another set (in Extra_Words.txt) to include a few words that
# the EOWL doesn't.

# Inspired by zsh's smart tab completion

# Bind this script to a keyboard shortcut and press it to show
# a list of suggested words.

import os
import subprocess as sp
import sys
import time
from collections import Counter
from languages import get_language_name
from fonts import get_font_name
import argparse
import string

# Arguments

arg_parser = argparse.ArgumentParser(
	description='''TextSuggest - X11 utility to autocomplete words in the GUI''',
	formatter_class=argparse.RawTextHelpFormatter)

arg_parser.add_argument(
	'--word', type=str,
	help='Specify word to give suggestions for. Default: taken from X11 clipboard. Ignored if --noselect. \n \n',
	nargs='+', required=False)

arg_parser.add_argument(
	'--noselect', action='store_true',
	help='Give all words as suggestions, which you can then filter. \n \n',
	required=False)

arg_parser.add_argument(
	'--plainrofi', action='store_true',
	help='Do not apply custom Rofi theme. \n \n',
	required=False)

arg_parser.add_argument(
	'--font', type=str,
	help='Specify font for Rofi. Must be in Pango format: FontName (Weight (optional) FontSize). \n \n',
	nargs='+', required=False)

arg_parser.add_argument(
	'--nohistory', action='store_true',
	help='Disable the frequently-used words history (stored in ~/.config/textsuggest/history.txt) \n \n',
	required=False)

arg_parser.add_argument(
	'--language', type=str,
	help='Manually set language, in case script fails to auto-detect from keyboard layout. \n \n',
	required=False)

arg_parser.add_argument(
	'--autosel', type=str, nargs='?',
	help='Automatically select word under cursor and suggest. See --help-autosel for details. Ignored if --noselect. \n \n',
	choices=['beginning', 'middle', 'end'], const='end', required=False)

arg_parser.add_argument(
	'--help-autosel', action='store_true',
	help='See help and documentation on the --autosel option.',
	required=False)

args = arg_parser.parse_args()

if args.help_autosel:

	print('''This is the help and documentation for the --autosel option.

Automatically select word under cursor for you before suggestion, saving time and keystrokes. Ignored if --noselect.

--autosel has three modes:

- 'beginning': Assumes text-cursor is at beginning of word.
- 'middle'   : Assumes text-cursor is somewhere in the middle of word.
- 'end'      : Assumes text-cursor is at end of word. Default.

The three choices help choose the keyboard shortcut to be pressed. It would be good to auto-detect the option
according to the text-cursor's position, but X11 does not provide this.

NOTE: The normal "you select text and textsuggests suggests on that" will not work with this enabled.''')

	sys.exit(0)

def restart_program(additional_args=[], remove_args=[]):

	# Restart, preserving all original arguments and optionally adding more

	new_cmd = ''

	for i in sys.argv:

		new_cmd += ' ' + i

	if not remove_args == []:

		for arg in remove_args:

			if arg in new_cmd:

				new_cmd = new_cmd.replace(arg, '')

	if not additional_args == []:

		for arg in additional_args:

			new_cmd += ' ' + arg

	with open('/tmp/restart.sh', 'w') as f:

		f.write('python3 %s &' % new_cmd)

	sp.Popen(['sh /tmp/restart.sh'], shell=True)

	time.sleep(1.5)  # Allow restart.sh to fully execute

	sys.exit(0)

if args.noselect:

	current_word = ''
	suggest_method = 'insert'

else:

	if args.word:

		current_word = ' '.join(args.word)
		suggest_method = 'replace'

	else:

		if args.autosel:

			if args.autosel == 'beginning':

				# Ctrl + Shift + ->
				sp.Popen(['xdotool keydown Ctrl keydown Shift key Right keyup Shift keyup Ctrl > /dev/null'], shell=True)

			elif args.autosel == 'middle':

				# Ctrl + <- then Ctrl + Shift + ->
				sp.Popen(['sleep 0.5; xdotool key Ctrl+Left; xdotool key Ctrl+Shift+Right > /dev/null'], shell=True)

			else:

				# Ctrl + Shift + <-
				sp.Popen(['sleep 0.5; xdotool key Ctrl+Shift+Left > /dev/null'], shell=True)

			time.sleep(1.5)  # Otherwise restart_program() restarts before selection is complete

			restart_program(remove_args=['--autosel'])

		current_word = sp.check_output(['xclip', '-o', '-sel'])

		current_word = current_word.decode('utf-8').strip()

		suggest_method = 'replace'

config_dir = os.path.expanduser('~/.config/textsuggest')

base_dict_dir = os.path.expanduser('/usr/share/textsuggest/dictionaries')

hist_file = os.path.expanduser('~/.config/textsuggest/history.txt')

extra_words_file = os.path.expanduser('/usr/share/textsuggest/Extra_Words.txt')

custom_words_file = os.path.expanduser('~/.config/textsuggest/Custom_Words.txt')

if not os.path.isdir(config_dir):

	os.mkdir(config_dir)

# Moving ~/.Custom_Words.txt to config_dir

prev_custom_words_file = os.path.expanduser('~/.Custom_Words.txt')

if os.path.isfile(prev_custom_words_file):

	os.rename(prev_custom_words_file, custom_words_file)

if args.language:

	language = args.language

else:

	language = get_language_name()

def remove_dups(s_list):

	seen = set()
	seen_add = seen.add

	return [x for x in s_list if not (x in seen or seen_add(x))]

def get_dict_dir():

	# Different dictionary for different language

	return os.path.join(base_dict_dir, language)

def type_command_output(command):

	command_out = sp.check_output([command], shell=True)
	command_out = command_out.decode('utf-8').rstrip()

	if '\n' in command_out:

		command_out_newl_list = command_out.split('\n')

		for i in command_out_newl_list:

			sp.Popen(['xdotool type --clearmodifiers "%s"; xdotool keydown Shift key Return keyup Shift' % i.strip('\'').strip('"')], shell=True)

			time.sleep(0.5)

	else:

		sp.Popen(['xdotool type \'%s\'' % command_out], shell=True)

def get_suggestions(suggestion_string):

	suggestions = []

	if language == 'English':

		suggestion_string = suggestion_string.lower()

		dict_dir = get_dict_dir()

		# Check for special characters

		suggestion_string_list_to_mod = list(suggestion_string)

		for i in list(suggestion_string):

			if i in string.punctuation:

				suggestion_string_list_to_mod.remove(i)

		suggestion_string = ''.join(suggestion_string_list_to_mod)

		alphabet = suggestion_string[:1].upper()

		dict_file = os.path.join(dict_dir, '%s.txt' % alphabet)

	else:

		alphabet = str(current_word[:1])

		dict_dir = get_dict_dir()

		dict_file = os.path.join(dict_dir, 'dict.txt')

	if suggest_method == 'insert':

		try:

			for file in os.listdir(dict_dir):

				file = os.path.join(dict_dir, file)

				with open(file) as f:

					for word in f:

						suggestions.append(word)

		except FileNotFoundError:

			pass

	else:

		try:

			with open(dict_file) as f:

				for word in f:

					if word.startswith(suggestion_string):

						suggestions.append(word)

					elif suggestion_string in word:

						suggestions.append(word)

		except FileNotFoundError:

			try:

				for file in os.listdir(dict_dir):

					with open(os.path.join(dict_dir, file)) as f:

						for word in f:

							if word.startswith(alphabet) or word.startswith(alphabet.lower) and string in word:

								suggestions.append(word)

			except FileNotFoundError:

				pass

	with open(extra_words_file) as f:

		for word in f:

			if suggest_method == 'insert':

				suggestions.append(word)

			elif suggestion_string in word:

				suggestions.append(word)

	# If language != English, display English and language suggestions

	if not language == 'English':

		eng_dict_dir = os.path.join(base_dict_dir, 'English')

		dict_file = os.path.join(eng_dict_dir, '%s.txt' % alphabet)

		if suggest_method == 'insert':

			try:

				for file in os.listdir(eng_dict_dir):

					file = os.path.join(eng_dict_dir, file)

					with open(file) as f:

						for word in f:

							suggestions.append(word)

			except FileNotFoundError:

				pass

		else:

			try:

				with open(dict_file) as f:

					for word in f:

						if suggestion_string in word:

							suggestions.append(word)

			except FileNotFoundError:

				try:

					for file in os.listdir(eng_dict_dir):

						with open(os.path.join(eng_dict_dir, file)) as f:

							for word in f:

								if word.startswith(alphabet) or word.startswith(alphabet.lower):

									if suggestion_string in word:

										suggestions.append(word)

				except FileNotFoundError:

					pass


	# Apply history

	if not args.nohistory:

		if os.path.isfile(hist_file):

			with open(hist_file) as f:

				for hist_word in f:

					if suggest_method == 'insert':

						suggestions.append(hist_word)

					elif suggestion_string in hist_word:

						suggestions.append(hist_word)

	# Applying Custom Words

	if os.path.isfile(custom_words_file):

		with open(custom_words_file) as f:

			for word in f:

				if suggest_method == 'insert':

					suggestions.append(word)

				elif suggestion_string in word:

					suggestions.append(word)

	# Sort by frequency, since commonly-used words would appear more

	suggestions = sorted(suggestions, key=Counter(suggestions).get, reverse=True)
	suggestions = remove_dups(suggestions)

	return suggestions

def display_dialog_list(item_list):

	items_string = ''

	mouse_loc_raw = sp.check_output(['xdotool getmouselocation --shell'], shell=True)
	mouse_loc_raw = mouse_loc_raw.decode('utf-8')

	x = mouse_loc_raw.split('\n')[0].replace('X=', '')
	y = mouse_loc_raw.split('\n')[1].replace('Y=', '')

	# Colors inspired by Arc theme (Dark)

	rofi_theme = '-lines 3 -width 20 -bg "#2b2e37" -separator-style "none" -hlbg "#5294e2" -fg "#fdfdfe" -hlfg "#fdfdfe" -hide-scrollbar -padding 1'

	if args.plainrofi:

		rofi_theme = ''

	if args.font:

		# Font should be specified in Pango format: FontName {(optional) FontWeight} FontSize

		font = ' '.join(args.font)

	else:

		language = get_language_name()

		if language == 'English':

			font = 'Monospace 10'

		else:

			font = get_font_name(language)

			if not font:

				# If returned empty, use default

				font = 'Monospace 10'

	if item_list == [] or item_list == [''] or item_list is None:

		if suggest_method == 'replace':

			restart_program(additional_args=['--noselect'])

		else:

			print('No words found. Exiting.')

			sys.exit(1)

	for i in item_list:

		items_string += i

	popup_menu_cmd_str = 'echo "%s" | rofi -dmenu -fuzzy -p "> " -i %s -font "%s" -xoffset %s -yoffset %s -location 1' % (items_string, rofi_theme, font, x, y)

	# The argument list will sometimes be too long (too many words)
	# subprocess can't handle it, and will raise OSError.
	# So we will write it to a script file.

	full_dict_script_path = os.path.expanduser('/tmp/textsuggest_full.sh')

	with open(full_dict_script_path, 'w') as f:

		f.write(popup_menu_cmd_str)

	choice = sp.check_output(['sh %s' % full_dict_script_path], shell=True)

	return choice

def apply_suggestion(suggestion):

	if suggestion is None or suggestion == b'' or suggestion == []:

		# User doesn't want any suggestion
		# exit

		sys.exit(0)

	else:

		# User wants a suggestion
		# Decode the suggestion string in utf-8 format

		suggestion = suggestion.decode('utf-8')

		if suggest_method == 'replace':

			# Erase current word

			sp.Popen(['xdotool key BackSpace'], shell=True)

			if current_word[:1].isupper():

				suggestion = suggestion.capitalize()

		if not args.nohistory:

			# Write to history
			with open(hist_file, 'a') as f:

				f.write(suggestion)

		# Type suggestion

		if '=' in suggestion:

			expand_suggestion = suggestion.split('=')[1]

			if '#' in expand_suggestion:

				command_suggestion = str(expand_suggestion.replace('#', ''))

				type_command_output(command_suggestion)

				sys.exit(0)

			else:

				sp.Popen(['xdotool type \'%s\'' % expand_suggestion.rstrip()], shell=True)

				sys.exit(0)

		elif '#' in suggestion:

			command_suggestion = str(suggestion.replace('#', ''))

			type_command_output(command_suggestion)

			sys.exit(0)

		else:

			sp.Popen(['xdotool type \'%s\'' % suggestion.rstrip()], shell=True)

			sys.exit(0)

if __name__ == '__main__':

	apply_suggestion(display_dialog_list(get_suggestions(current_word)))
