#!/usr/bin/env python3
# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>
# Contributor: Maksudur Rahman Maateen <ugcoderbd@gmail.com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

# A simple linux tool to autocomplete text inputs in the GUI

# Uses the English Open Word List
# (http://dreamsteep.com/projects/the-english-open-word-list.html)
# Plus another set (in Extra_Words.txt) to include a few words that
# the EOWL doesn't.
# Also uses a Bangla dictionary from sarim/ibus-avro

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
from suggestions import get_suggestions

import argparse

script_cwd = os.path.abspath(os.path.join(__file__, os.pardir))

config_dir = os.path.expanduser('~/.config/textsuggest')

base_dict_dir = os.path.expanduser('/usr/share/textsuggest/dictionaries')

hist_file = os.path.expanduser('~/.config/textsuggest/history.txt')

extra_words_file = os.path.expanduser('~/.config/textsuggest/Extra_Words.txt')

custom_words_file = os.path.expanduser('~/.config/textsuggest/Custom_Words.txt')

# Arguments

arg_parser = argparse.ArgumentParser(
	description='''TextSuggest - X11 utility to autocomplete words in the GUI''',
	formatter_class=argparse.RawTextHelpFormatter,
	epilog='More information in the manual page: textsuggest(1)')

arg_parser.add_argument(
	'--word', type=str,
	help='Specify word to give suggestions for. Default: taken from X11 clipboard. Ignored if --no-selection. \n \n',
	nargs='+', required=False)

arg_parser.add_argument(
	'--no-selection', action='store_true',
	help='Give all words as suggestions, which you can then filter. \n \n',
	required=False)

arg_parser.add_argument(
	'--no-rofi-customization', action='store_true',
	help='Do not apply custom Rofi theme. \n \n',
	required=False)

arg_parser.add_argument(
	'--font', type=str,
	help='Specify font for Rofi. Must be in Pango format: FontName (Weight (optional) FontSize). \n \n',
	nargs='+', required=False)

arg_parser.add_argument(
	'--no-history', action='store_true',
	help='Disable the frequently-used words history (stored in ~/.config/textsuggest/history.txt) \n \n',
	required=False)

arg_parser.add_argument(
	'--language', type=str,
	help='Manually set language, in case script fails to auto-detect from keyboard layout. \n \n',
	required=False)

arg_parser.add_argument(
	'--auto-selection', type=str, nargs='?',
	help='Automatically select word under cursor and suggest. See --help-auto-selection for details. Ignored if --no-selection. \n \n',
	choices=['beginning', 'middle', 'end'], const='end', required=False)

arg_parser.add_argument(
	'--help-auto-selection', action='store_true',
	help='See help and documentation on the auto-selection option.',
	required=False)

args = arg_parser.parse_args()

if args.help_auto_selection:
	print('''This is the help and documentation for the --auto-selection option.

Automatically select word under cursor for you before suggestion, saving time and keystrokes. Ignored if --no-selection.

--auto-selection has three modes:

- 'beginning': Assumes text-cursor is at beginning of word.
- 'middle'   : Assumes text-cursor is somewhere in the middle of word.
- 'end'      : Assumes text-cursor is at end of word. Default.

The three choices help choose the keyboard shortcut to be pressed. It would be good to auto-detect the option
according to the text-cursor's position, but X11 does not provide this.

NOTE: The normal "you select text and textsuggests suggests on that" will not work with this enabled.''')

	sys.exit(0)


if not os.path.isdir(config_dir):
	os.mkdir(config_dir)

# Moving ~/.Custom_Words.txt to config_dir
prev_custom_words_file = os.path.expanduser('~/.Custom_Words.txt')

if os.path.isfile(prev_custom_words_file):
	os.rename(prev_custom_words_file, custom_words_file)

if args.language:
	if get_language_name != 'English':
		language = [args.language, 'English']
	else:
		language = ['English']
else:
	if get_language_name != 'English':
		language = [get_language_name(), 'English']
	else:
		language = ['English']

def restart_program(additional_args=[], remove_args=[]):

	# Restart, preserving all original arguments and optionally adding more

	new_cmd = ''

	for i in sys.argv:
		new_cmd += ' ' + i

	if remove_args != []:
		for arg in remove_args:
			if arg in new_cmd:
				new_cmd = new_cmd.replace(arg, '')

	if additional_args != []:
		for arg in additional_args:
			new_cmd += ' ' + arg

	with open('/tmp/restart.sh', 'w') as f:
		f.write('%s %s &' % (sys.executable, new_cmd))

	sp.Popen(['sh /tmp/restart.sh'], shell=True)
	time.sleep(1.5)  # Allow restart.sh to fully execute

	sys.exit(0)

if args.no_selection:
	current_word = ''
	suggest_method = 'insert'

else:
	if args.word:
		current_word = ' '.join(args.word)
		suggest_method = 'replace'

	else:
		if args.auto_selection:
			if args.auto_selection == 'beginning':
				# Ctrl + Shift + ->
				sp.Popen([
					'xdotool keydown Ctrl keydown Shift key Right keyup Shift keyup Ctrl > /dev/null'],
					shell=True)
			elif args.auto_selection == 'middle':
				# Ctrl + <- then Ctrl + Shift + ->
				sp.Popen([
					'sleep 0.5; xdotool key Ctrl+Left; xdotool key Ctrl+Shift+Right > /dev/null'],
					shell=True)
			else:
				# Ctrl + Shift + <-
				sp.Popen(['sleep 0.5; xdotool key Ctrl+Shift+Left > /dev/null'],
						 shell=True)

			time.sleep(1.5)
			# Otherwise restart_program restarts before selection is complete

			restart_program(remove_args=['auto-selection'])

		current_word = sp.check_output(['xsel'])

		current_word = current_word.decode('utf-8').strip()

		suggest_method = 'replace'

def remove_dups(s_list):

	seen = set()
	seen_add = seen.add

	return [x for x in s_list if not (x in seen or seen_add(x))]

def get_dictionaries():

	dictionaries = []

	for lang in language:
		for file in os.listdir(os.path.join(base_dict_dir, lang)):
			dictionaries.append(os.path.join(base_dict_dir, lang, file))

	dictionaries.append(custom_words_file)
	dictionaries.append(extra_words_file)

	return dictionaries

def type_command_output(command):

	command_out = sp.check_output([command], shell=True)
	command_out = command_out.decode('utf-8').rstrip()

	if '\n' in command_out:

		command_out_newl_list = command_out.split('\n')

		for i in command_out_newl_list:
			sp.Popen([
				'xdotool type --clearmodifiers "%s"; xdotool keydown Shift key Return keyup Shift' % i.strip(
					'\'').strip('"')], shell=True)

			time.sleep(0.5)

	else:

		sp.Popen(['xdotool type \'%s\'' % command_out], shell=True)

def display_dialog_list(item_list):

	items_string = ''

	mouse_loc_raw = sp.check_output(['xdotool getmouselocation --shell'], shell=True)
	mouse_loc_raw = mouse_loc_raw.decode('utf-8')

	x = mouse_loc_raw.split('\n')[0].replace('X=', '')
	y = mouse_loc_raw.split('\n')[1].replace('Y=', '')

	# Colors inspired by Arc theme (Dark)

	rofi_theme = '-lines 3 -width 20 -bg "#2b2e37" -separator-style "none" -hlbg "#5294e2" -fg "#fdfdfe" -hlfg "#fdfdfe" -hide-scrollbar -padding 1'

	if args.no_rofi_customization:
		rofi_theme = ''

	if args.font:
		# Font should be specified in Pango format: FontName {(optional) FontWeight} FontSize
		font = ' '.join(args.font)

	else:
		language = get_language_name()
		if language == ['English']:
			font = 'Monospace 10'
		else:
			font = get_font_name(language)
			if not font:
				# If returned empty, use default
				font = 'Monospace 10'

	if item_list == [] or item_list == [''] or item_list is None:
		if suggest_method == 'replace':
			restart_program(additional_args=['--no-selection'])
		else:
			print('No words found. Exiting.')
			sys.exit(1)

	for i in item_list:
		items_string += i

	popup_menu_cmd_str = 'echo "%s" | rofi -dmenu -fuzzy -sep "|" -p "> " -i %s -font "%s" -xoffset %s -yoffset %s -location 1' % (items_string, rofi_theme, font, x, y)

	# The argument list will sometimes be too long (too many words)
	# subprocess can't handle it, and will raise OSError.
	# So we will write it to a script file.

	full_dict_script_path = os.path.expanduser('/tmp/textsuggest_full.sh')

	with open(full_dict_script_path, 'w') as f:
		f.write(popup_menu_cmd_str)

	try:
		choice = sp.check_output(['sh %s' % full_dict_script_path], shell=True)
	except sp.CalledProcessError:
		sys.exit(2)

	return choice

def apply_suggestion(suggestion):

	if suggestion is None or suggestion == b'' or suggestion == []:
		# User doesn't want any suggestion
		# exit
		sys.exit(2)

	else:
		# User wants a suggestion

		suggestion = suggestion.decode('utf-8')

		if suggest_method == 'replace':
			# Erase current word
			sp.Popen(['xdotool key BackSpace'], shell=True)

			if current_word[:1].isupper():
				suggestion = suggestion.capitalize()

		if not args.no_history:
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

def main():

	words_list = get_suggestions(current_word, dict_files=get_dictionaries())

	# Apply history

	# How the history application works:
	# History is stored as plaintext
	# For each word in the history file,
	# we'll add it if it's already in the suggestions list (yes, duplicates)
	# The more times a word occurs in history, the more it will be
	# duplicated in the suggestions list.
	# Then we sort the suggestions list by frequency of elements.
	# Thus the word frequently-used is more towards the top of suggestions

	with open(hist_file) as f:
		for hist_word in f:
			if hist_word.rstrip('\r\n') in words_list:
				words_list.append(hist_word.rstrip('\r\n'))

	words_list = sorted(words_list, key=Counter(words_list).get, reverse=True)

	apply_suggestion(display_dialog_list('|'.join(get_suggestions(current_word, get_dictionaries()))))

if __name__ == '__main__':
	main()
