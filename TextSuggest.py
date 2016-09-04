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
import collections
import traceback

from languages import get_language_name
from fonts import get_font_name
from suggestions import get_suggestions

import argparse

__version__ = 133  # Updated using git pre-commit hook

script_cwd = os.path.abspath(os.path.join(__file__, os.pardir))
config_dir = os.path.expanduser('~/.config/textsuggest')
base_dict_dir = '/usr/share/textsuggest/dictionaries'
extra_words_file = '/usr/share/textsuggest/Extra_Words.txt'
custom_words_file = os.path.expanduser('~/.config/textsuggest/Custom_Words.txt')
hist_file = os.path.expanduser('~/.config/textsuggest/history.txt')

# Arguments

arg_parser = argparse.ArgumentParser(
	description='''TextSuggest - X11 utility to autocomplete words in the GUI''',
	formatter_class=argparse.RawTextHelpFormatter,
	epilog='''More information in the manual page: textsuggest(1). \n
	Return codes:
	0 : Success
	1 : No words found
	2 : Cancelled by user
	3 : Math expression error'''.replace('\t', ''))

arg_parser.add_argument(
	'--word', type=str,
	help='Specify word to give suggestions for. Default: taken from X11 clipboard. Ignored if --no-selection. \n \n',
	nargs='+', required=False)

arg_parser.add_argument(
	'--no-selection', action='store_true',
	help='Give all words as suggestions, which you can then filter. \n \n',
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
	'--exit-on-no-words-found', action='store_true',
	help='Exit if no words are found (instead of restarting in --no-selection mode) \n \n',
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
	help='See help and documentation on the auto-selection option. \n \n',
	required=False)

arg_parser.add_argument(
	'--version', action='store_true',
	help='Print version and license information.',
	required=False)

args = arg_parser.parse_args()

if args.version:
	print('''TextSuggest %d
			Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>
			License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
			This is free software; you are free to change and redistribute it.
			There is NO WARRANTY, to the extent permitted by law.'''.replace('\t', '').replace('    ', '') % __version__)

	sys.exit(0)

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
	language = [args.language, 'English']
else:
	if get_language_name() != 'English':
		language = [get_language_name(), 'English']
	else:
		language = ['English']

def freq_sort(lst):
	counts = collections.Counter(lst)
	sorted_lst = sorted(lst, key=counts.get, reverse=True)

	return sorted_lst

def uniq(seq):
	seen = set()
	seen_add = seen.add
	return [x for x in seq if not (x in seen or seen_add(x))]

def restart_program(additional_args=[], remove_args=[]):

	# Restart, preserving all original arguments and optionally adding more

	new_cmd = ''

	for i in sys.argv:
		new_cmd += ' ' + i

	if remove_args != []:
		for arg in remove_args:
			for i in sys.argv:
				if arg in i:
					new_cmd = new_cmd.replace(i, '')
					removed = True

	if additional_args != []:
		for arg in additional_args:
			new_cmd += ' ' + arg

	with open('/tmp/restart.sh', 'w') as f:
		f.write('%s %s' % (sys.executable, new_cmd))

	restart_proc = sp.Popen(['sh /tmp/restart.sh'], shell=True)
	restart_proc.wait()  # Allow restart.sh to fully execute

	sys.exit(restart_proc.returncode)

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
					'xdotool key Ctrl+Shift+Right > /dev/null'],
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

			restart_program(remove_args=['--auto-selection', 'beginning', 'middle', 'end'])

		current_word = sp.check_output(['xsel']).decode('utf-8').strip()

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

	if os.path.isfile(custom_words_file):
		dictionaries.append(custom_words_file)
	if os.path.isfile(extra_words_file):
		dictionaries.append(extra_words_file)

	return dictionaries

def type_text(text):

	if '\n' in text:
		newline_list = text.split('\n')

		for i in command_out_newl_list:
			type_proc = sp.Popen(['xdotool', 'type', '--clearmodifiers', '--', i])

			type_proc.wait()
			sp.Popen(['xdotool', 'key', 'Shift+Return'])

			time.sleep(0.5)

	else:
		sp.Popen(['xdotool', 'type', '--', text])

def display_dialog_list(items_list):

	mouse_loc_raw = sp.check_output(['xdotool', 'getmouselocation', '--shell'])
	mouse_loc_raw = mouse_loc_raw.decode('utf-8')

	x = mouse_loc_raw.split('\n')[0].replace('X=', '')
	y = mouse_loc_raw.split('\n')[1].replace('Y=', '')

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
				# use default
				font = 'Monospace 10'

	history = '-disable-history' if args.no_history else '-no-disable-history'

	popup_menu_cmd_str = 'echo "%s" | rofi -dmenu %s -fuzzy -glob -sep "|" -p "> " -i -font "%s" -xoffset %s -yoffset %s -location 1' % (items_list, history, font, x, y)

	# The argument list will sometimes be too long (too many words)
	# subprocess can't handle it, and will raise OSError.
	# So we will write it to a script file.

	full_dict_script_path = os.path.expanduser('/tmp/textsuggest_full.sh')

	with open(full_dict_script_path, 'w') as f:
		f.write(popup_menu_cmd_str)

	choice_proc = sp.Popen(['sh', full_dict_script_path], stdout=sp.PIPE)
	choice = choice_proc.communicate()[0].decode('utf-8').rstrip('\n')
	choice_proc.wait()

	if choice_proc.returncode != 0:
		# No suggestion wanted
		sys.stderr.write('ERR_REJECTED: User doesn\'t want any suggestion.')
		sys.stdout.flush()
		sys.exit(2)
		print('fjh')

	return choice

def process_suggestion(suggestion):

	if not args.no_history:
		with open(hist_file, 'a') as f:
			f.write(suggestion)

	if suggest_method == 'replace':
		# Erase current word
		sp.Popen(['xdotool', 'key', 'BackSpace'])

		if current_word[:1].isupper():
			suggestion = suggestion.capitalize()

	if '=' in suggestion:
		suggestion = suggestion.split('=', 1)[1]

	if suggestion.startswith('#'):
		# Command output
		suggestion = sp.check_output(suggestion[1:], shell=True).decode('utf-8').rstrip()

	elif suggestion.startswith('%'):
		# Math
		try:
			suggestion = str(eval(suggestion[1:]))
		except:
			sys.stderr.write(traceback.format_exc())
			sys.stderr.flush()
			sys.stderr.write('ERR_EXPRESSION: Math expression %s was invalid.' % suggestion)
			sys.exit(3)

	return suggestion

def main():

	print('Running in %s mode.' % suggest_method)

	if suggest_method == 'replace':
		print('Getting suggestions for word:', current_word)

	words_list = get_suggestions(current_word, dict_files=get_dictionaries())

	if not words_list or words_list == ['']:
		if not args.exit_on_no_words_found:
			print('WARN_NOWORDS: Restarting in --no-selection mode. To prevent restarting, use --exit-on-no-words-found.')
			restart_program(additional_args=['--no-selection'])
		else:
			sys.stderr.write('ERR_NOWORDS: No words found.')
			sys.exit(1)

	if not args.no_history:
		words_list.extend(get_suggestions(current_word, dict_files=[hist_file]))

		# Frequency sort + Remove duplicates
		words_list = uniq(freq_sort(words_list))

	words_list = '|'.join(words_list)

	chosen_word = display_dialog_list(words_list)

	print('Chosen word:', chosen_word)

	processed_chosen_word = process_suggestion(chosen_word)

	print('Processed:', processed_chosen_word)

	type_text(processed_chosen_word)

if __name__ == '__main__':
	main()
