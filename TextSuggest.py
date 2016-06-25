#!/usr/bin/env python3
# coding=utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>

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
from fonts import get_font_name
from languages import get_language_name

if '--noselect' in sys.argv:

	current_word = ''
	suggest_method = 'insert'

else:

	try:

		current_word = sys.argv[1]
		suggest_method = 'replace'

	except:

		current_word_p = sp.Popen(['xclip', '-o', '-sel'], stdout=sp.PIPE)
		current_word, err_curr_word = current_word_p.communicate()
		current_word = current_word.decode('utf-8').strip()

		suggest_method = 'replace'

script_cwd = os.path.abspath(os.path.join(__file__, os.pardir))

custom_words_file = os.path.expanduser('~/.config/textsuggest/Custom_Words.txt')

def remove_dups(s_list):

	seen = set()
	seen_add = seen.add

	return [x for x in s_list if not (x in seen or seen_add(x))]

def get_dict_dir():

    # Different dictionary for different language

    language = get_language_name()

    dict_dir = os.path.expanduser('~/.config/textsuggest/dictionaries')

    return os.path.join(dict_dir, '%s' % language)

def get_suggestions(string):

	orig_string = string
	suggestions = []
	language = get_language_name()

	if language == 'English':

		string = string.lower()

		alphabet = str(current_word[:1]).upper()

		dict_dir = get_dict_dir()

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

					if string in word:

						suggestions.append(word)

		except FileNotFoundError:

			pass

	with open(os.path.join(script_cwd, '~/.config/textsuggest/Extra_Words.txt')) as f:

		for word in f:

			if suggest_method == 'insert':

				suggestions.append(word)

			elif string in word:

				suggestions.append(word)

	# Apply history

	if os.path.isfile(os.path.expanduser('~/.config/textsuggest/textsuggest_history.txt')):

		with open(os.path.expanduser('~/.config/textsuggest/textsuggest_history.txt')) as f:

			for hist_word in f:

				if suggest_method == 'insert':

					suggestions.append(hist_word)

				if string in hist_word:

					suggestions.append(hist_word)

	# Applying Custom Words

	if os.path.isfile(custom_words_file):

		with open(custom_words_file) as f:

			for word in f:

				if suggest_method == 'insert':

					suggestions.append(word)

				elif string in word:

					suggestions.append(word)

	# Sort by frequency, since commonly-used words would appear more

	suggestions = sorted(suggestions, key=Counter(suggestions).get, reverse=True)
	suggestions = remove_dups(suggestions)

	return suggestions

def display_dialog_list(item_list):

	items_string = ''

	mouse_loc_raw, err_mouse_loc = sp.Popen(['xdotool getmouselocation --shell'], shell=True, stdout=sp.PIPE).communicate()
	mouse_loc_raw = mouse_loc_raw.decode('utf-8')

	x = mouse_loc_raw.split('\n')[0].replace('X=', '')
	y = mouse_loc_raw.split('\n')[1].replace('Y=', '')

	# Colors inspired by Arc theme (Dark)

	rofi_theme = '-lines 3 -width 20 -bg "#2b2e37" -separator-style "none" -hlbg "#5294e2" -fg "#fdfdfe" -hlfg "#282f39" -hide-scrollbar -padding 1'

	if '--plainrofi' in sys.argv:

		rofi_theme = ''

	if '--font' in sys.argv:

		# Font should be specified in Pango format: FontName {(optional) FontWeight} FontSize
		# must be double-quoted in shell arguments

		font = str(sys.argv[int(sys.argv.index('--font') + 1)])

	else:

		language = get_language_name()

		if language == 'English':

			font = 'Monospace 10'

		else:

			language = get_language_name()

			font = get_font_name(language)


	if item_list == [] or item_list == [''] or item_list is None:

		if '--showerrors' in sys.argv:

			sp.Popen(['echo "Nothing found! " | rofi -dmenu -p "> " -i %s -font "%s" -xoffset %s -yoffset %s -location 1' % (rofi_theme, font, x, y)], shell=True)

			time.sleep(1)

			sp.Popen(['xdotool key Escape'], shell=True)

			sys.exit(1)

		elif suggest_method == 'replace':

			# Restart in --noselect mode

			new_textsuggest_cmd = ''

			for i in sys.argv:

				new_textsuggest_cmd += ' ' + i

			sp.Popen(['python3 %s --noselect' % new_textsuggest_cmd], shell=True)

			sys.exit(0)

		else:

			print('No words found. Exiting.')

			sys.exit(1)

	for i in item_list:

		items_string += i

	popup_menu_cmd_str = 'echo "%s" | rofi -dmenu -p "> " -i %s -font "%s" -xoffset %s -yoffset %s -location 1' % (items_string, rofi_theme, font, x, y)

	if suggest_method == 'insert':

		# The argument list will be too long since it includes ALL dictionary
		# words.
		# subprocess can't handle it, and will raise OSError.
		# So we will write it to a script file.

		full_dict_script_path = os.path.expanduser('~/.textsuggest_full.sh')

		with open(full_dict_script_path, 'w') as f:

			f.write(popup_menu_cmd_str)

		full_dict_script_p = sp.Popen(['sh %s' % full_dict_script_path], shell=True, stdout=sp.PIPE)
		choice, err_choice = full_dict_script_p.communicate()

		return choice

	popup_menu_p = sp.Popen(popup_menu_cmd_str, shell=True, stdout=sp.PIPE)
	choice, err_choice = popup_menu_p.communicate()

	return choice

def apply_suggestion(suggestion):

	if suggestion is None:

		# User doesn't want any suggestion
		# exit

		sys.exit(0)

	else:

		# User wants any suggestion
		# Decode the suggestion string in utf-8 format

		suggestion = suggestion.decode('utf-8')

		if suggest_method == 'replace':

			# Erase current word

			sp.Popen(['xdotool key BackSpace'], shell=True)

			if current_word[:1].isupper():

				suggestion = suggestion.capitalize()

		# Write to history
		with open(os.path.expanduser('~/.config/textsuggest/textsuggest_history.txt'), 'a') as f:

			f.write(suggestion)

		# Type suggestion

		if '=' in suggestion:

			expand_suggestion = suggestion.split('=')[1]

			if '#' in expand_suggestion:

				command_suggestion = str(expand_suggestion.replace('#', ''))

				command_suggestion_p = sp.Popen([command_suggestion], shell=True, stdout=sp.PIPE)
				command_suggestion_out, command_suggestion_err = command_suggestion_p.communicate()
				command_suggestion_out = str(command_suggestion_out.strip()).replace('b', '', 1)

				sp.Popen(['xdotool type \'%s\'' % command_suggestion_out.rstrip()], shell=True)

				sys.exit(0)

			else:

				sp.Popen(['xdotool type \'%s\'' % expand_suggestion.rstrip()], shell=True)

				sys.exit(0)

		elif '#' in suggestion:

			command_suggestion = str(suggestion.replace('#', ''))

			command_suggestion_p = sp.Popen([command_suggestion], shell=True, stdout=sp.PIPE)
			command_suggestion_out, command_suggestion_err = command_suggestion_p.communicate()
			command_suggestion_out = str(command_suggestion_out.strip()).replace('b', '', 1)

			sp.Popen(['xdotool type %s' % command_suggestion_out], shell=True)

			sys.exit(0)

		else:

			sp.Popen(['xdotool type \'%s\'' % suggestion.rstrip()], shell=True)

			sys.exit(0)

def main(current_word):

	apply_suggestion(display_dialog_list(get_suggestions(current_word)))

if __name__ == '__main__':

	main(current_word)