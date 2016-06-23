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
from collections import Counter

if '--noselect' in sys.argv:

	current_word = ''
	suggest_method = 'insert'

else:

	current_word_p = sp.Popen(['xclip', '-o', '-sel'], stdout=sp.PIPE)
	current_word, err_curr_word = current_word_p.communicate()
	current_word = current_word.decode('utf-8').strip()

	suggest_method = 'replace'

script_cwd = os.path.abspath(os.path.join(__file__, os.pardir))

custom_words_file = os.path.expanduser('~/.Custom_Words.txt')

def get_dict_dir():

	# Reading keyboard layout from shell command

	keyboard_layout = os.popen("setxkbmap -print | awk -F\"+\" '/xkb_symbols/ {print $2}'").read()
	keyboard_layout = keyboard_layout[:2]

	# Different dictionary for different language
	# Language will be detected by layout

	language_layout_file = os.path.join(script_cwd, 'Language_Layout.txt')

	with open(language_layout_file,'r') as f:

		languages = eval(f.read())

	language = languages[keyboard_layout]

	return os.path.join(script_cwd, '%sOpenWordList' % language)

def remove_dups(s_list):

	seen = set()
	seen_add = seen.add

	return [x for x in s_list if not (x in seen or seen_add(x))]

def get_suggestions(string):

	orig_string = string
	string = string.lower()

	suggestions = []

	alphabet = str(current_word[:1]).upper()

	dict_dir = get_dict_dir()

	dict_file = os.path.join(dict_dir, '%s.txt' % alphabet)

	if suggest_method == 'insert':

		for file in os.listdir(dict_dir):

			file = os.path.join(dict_dir, file)

			with open(file) as f:

				for word in f:

					suggestions.append(word)

	else:

		try:

			with open(dict_file) as f:

				for word in f:

					if string in word:

						suggestions.append(word)

		except:
			pass

	with open(os.path.join(script_cwd, 'Extra_Words.txt')) as f:

		for word in f:

			if suggest_method == 'insert':

				suggestions.append(word)

			elif string in word:

				suggestions.append(word)

	# Apply history

	if os.path.isfile(os.path.expanduser('~/.textsuggest_history.txt')):

		with open(os.path.expanduser('~/.textsuggest_history.txt')) as f:

			for hist_word in f:

				if suggest_method == 'insert':

					suggestions.append(hist_word)

				if string in hist_word:

					suggestions.append(hist_word)

	if os.path.isfile(os.path.expanduser('~/.Custom_Words.txt')):

		with open(os.path.expanduser('~/.Custom_Words.txt')) as f:

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

	dmenu_string = ''

	if item_list == [] or item_list == ['']:

		return None

	for i in item_list:

		dmenu_string += i

	if '--olddmenu' in sys.argv:

		# Compatibility with old dmenu

		dmenu_cmd_str = 'echo ' + str('"%s"' % dmenu_string) + ' | dmenu -b -i -p "Type to search >"'

	else:

		# Make use of advanced dmenu2 features. Requires dmenu2 (fork of dmenu)
		# to be installed. (https://bitbucket.org/melek/dmenu2)

		mouse_loc_raw, err_mouse_loc = sp.Popen(['xdotool getmouselocation --shell'], shell=True, stdout=sp.PIPE).communicate()
		mouse_loc_raw = mouse_loc_raw.decode('utf-8')

		x = mouse_loc_raw.split('\n')[0].replace('X=', '')
		y = mouse_loc_raw.split('\n')[1].replace('Y=', '')

		dmenu_cmd_str = 'echo ' + str('"%s"' % dmenu_string) + ' | dmenu -i -p "Type to search >" -l 5 -w 320 -h 20 -x %s -y %s' % (x, y)

	if suggest_method == 'insert':

		# The argument list will be too long since it includes ALL dictionary
		# words.
		# subprocess can't handle it, and will raise OSError.
		# So we will write it to a script file.

		full_dict_dmenu_script_path = os.path.expanduser('~/.textsuggest_full.sh')

		with open(full_dict_dmenu_script_path, 'w') as f:

			f.write(dmenu_cmd_str)

		full_dict_dmenu_script_p = sp.Popen(['sh %s' % full_dict_dmenu_script_path], shell=True, stdout=sp.PIPE)
		choice, err_choice = full_dict_dmenu_script_p.communicate()

		return choice

	dmenu_p = sp.Popen(dmenu_cmd_str, shell=True, stdout=sp.PIPE)
	choice, err_choice = dmenu_p.communicate()

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
		with open(os.path.expanduser('~/.textsuggest_history.txt'), 'a') as f:

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

apply_suggestion(display_dialog_list(get_suggestions(current_word)))
