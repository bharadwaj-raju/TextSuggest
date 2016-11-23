#!/usr/bin/env python3
# coding: utf-8

# TextSuggest
# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>, Maksudur Rahman Maateen <ugcoderbg@gmail.com>,
# and other contributors (see https://github.com/bharadwaj-raju/TextSuggest/graphs/contributors)

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3 (or any later version)
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

# A simple linux tool to autocomplete text inputs in the GUI

# Bind this script to a keyboard shortcut and press it to show
# a list of suggested words.

import os
import subprocess as sp
import sys
import time
import collections

from languages import get_language_name
from fonts import get_font_name
from suggestions import get_suggestions

import argparse

__version__ = 1570  # Updated using git pre-commit hook

script_cwd = os.path.abspath(os.path.join(__file__, os.pardir))
config_dir = os.path.expanduser('~/.config/textsuggest')
dict_dir = '/usr/share/textsuggest/dictionaries'
extra_words_file = '/usr/share/textsuggest/Extra_Words.txt'
custom_words_file = os.path.expanduser('~/.config/textsuggest/Custom_Words.txt')
hist_file = os.path.expanduser('~/.config/textsuggest/history.txt')

processor_dirs = [os.path.expanduser('~/.config/textsuggest/processors'),
				'/usr/share/textsuggest/processors']

for processor_dir in processor_dirs:
	sys.path.insert(0, processor_dir)

# Arguments

arg_parser = argparse.ArgumentParser(
	description='''TextSuggest - X11 utility to autocomplete words in the GUI''',
	formatter_class=argparse.RawTextHelpFormatter,
	usage='%(prog)s [options]',
	allow_abbrev=False,
	epilog='''More information:\n

	  - Manual page: man textsuggest
	  - Full README: /usr/share/doc/textsuggest/README'''.replace('\t', '').replace('    ', ''))

arg_parser.add_argument(
	'--word', type=str,
	help='Specify word to give suggestions for. Default: taken from X11 clipboard. Ignored if --no-selection. \n \n',
	nargs='+', required=False)

arg_parser.add_argument(
	'--all-words', '--no-selection', action='store_true',
	help='Give all words as suggestions, which you can then filter. \n \n',
	required=False)

arg_parser.add_argument(
	'--font', type=str,
	help='Specify font for Rofi. Format: FontName Weight Size. \n \n',
	nargs='+', required=False)

arg_parser.add_argument(
	'--no-history', action='store_true',
	help='Disable the frequently-used words history (stored in ~/.config/textsuggest/history.txt) \n \n',
	required=False)

arg_parser.add_argument(
	'--exit-if-no-words-found', action='store_true',
	help='Exit if no words are found (instead of restarting in --no-selection mode) \n \n',
	required=False)

arg_parser.add_argument(
	'--language', type=str,
	help='Manually set language(s), in case script fails to auto-detect from keyboard layout. \n \n',
	nargs='+', required=False, metavar='languages')

arg_parser.add_argument(
	'--auto-selection', type=str, nargs='?',
	help='Automatically select word under cursor and suggest. Ignored if --no-selection. \n \n',
	choices=['beginning', 'middle', 'end'], const='end', required=False, metavar='beginning|middle|end')

arg_parser.add_argument(
	'--no-processing', action='store_true',
	help='Disable using of any processors. \n \n', required=False)

arg_parser.add_argument(
	'--rofi-options', type=str,
	help='Specify additonal options to pass to Rofi. \n \n',
	nargs='+', required=False, metavar='options for rofi')

arg_parser.add_argument(
	'--force-gtk3-fix', action='store_true',
	help='Always use the GTK+ 3 workaround. If not set, tries to detect the current program\'s GTK+ version. \n \n',
	required=False)

arg_parser.add_argument(
	'--log', type=str, metavar='LOG_FILE',
	help='Log all output to a file. Useful when debugging. \n \n',
	required=False)

arg_parser.add_argument(
	'-v', '--version', action='store_true',
	help='Print version and license information.',
	required=False)

args, unknown_args = arg_parser.parse_known_args()

# Get the runtime/tmp dir
if os.getenv('XDG_RUNTIME_DIR'):
	runtime_dir = os.path.join(os.getenv('XDG_RUNTIME_DIR'), 'textsuggest')

elif os.getenv('TMPDIR'):
	runtime_dir = os.path.join(os.getenv('TMPDIR'), 'textsuggest')

else:
	runtime_dir = '/tmp/textsuggest'

if not os.path.isdir(runtime_dir):
	os.mkdir(runtime_dir)

menu_script = os.path.join(runtime_dir, 'menu_script.sh')
restart_script = os.path.join(runtime_dir, 'restart_auto_sel.sh')

def print_error(error):

	# Wrapper around sys.stderr

	if not error.endswith('\n'):
		error += '\n'

	sys.stderr.write(error)
	sys.stderr.flush()

for arg in unknown_args:
	print_error('Unknown option: %s. Ignoring.' % arg)

if args.version:
	print('''TextSuggest %d

			Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>
			License GPLv3+: GNU GPL (General Public License) version 3 or later <https://gnu.org/licenses/gpl.html>
			This is free software; you are free to change and redistribute it.
			There is NO WARRANTY, to the extent permitted by law.'''.replace('\t', '').replace('	', '') % __version__)

	sys.exit(0)

if not os.path.isdir(config_dir):
	os.mkdir(config_dir)

sp.Popen(['xsel', '--keep'])  # Make selection persist

if args.language:
	language = args.language
else:
	language = [get_language_name()]

def freq_sort(lst):
	counts = collections.Counter(lst)
	sorted_lst = sorted(lst, key=counts.get, reverse=True)

	return sorted_lst

def uniq(seq):
	seen = set()
	seen_add = seen.add
	return [x for x in seq if not (x in seen or seen_add(x))]

def get_cmd_out(program, suppress_stderr=False):

	run_in_shell = not isinstance(program, list)

	if suppress_stderr:
		return sp.check_output(program, stderr=sp.PIPE, shell=run_in_shell).decode('utf-8').rstrip('\n').replace('\\n', '\n')

	else:
		return sp.check_output(program, shell=run_in_shell).decode('utf-8').rstrip('\n').replace('\\n', '\n')

def restart_program(additional_args=None, remove_args=None):

	# Restart, preserving all original arguments and optionally adding/removing

	if not additional_args:
		additional_args = []

	if not remove_args:
		remove_args = []

	new_cmd = ''

	for i in sys.argv:
		new_cmd += ' ' + i

	if remove_args != []:
		for arg in remove_args:
			for i in sys.argv:
				if arg in i:
					new_cmd = new_cmd.replace(i, '')

	if additional_args != []:
		for arg in additional_args:
			new_cmd += ' ' + arg

	print('Restarting as:', new_cmd)

	with open(restart_script, 'w') as f:
		f.write('%s %s' % (sys.executable, new_cmd))

	restart_proc = sp.Popen(['sh', restart_script])
	restart_proc.wait()  # Allow restart.sh to fully execute

	sys.exit(restart_proc.returncode)

if args.all_words:
	current_word = ''
	suggest_method = 'insert'

else:
	if args.word:
		current_word = ' '.join(args.word)

	else:
		if args.auto_selection:
			if args.auto_selection == 'beginning':
				# Ctrl + Shift + ->
				sp.Popen([
					'sleep 0.5; xdotool key Ctrl+Shift+Right > /dev/null'],
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

			time.sleep(1)

		current_word = get_cmd_out(['xsel'])

	suggest_method = 'replace'

if current_word.endswith('.'):
	current_word = current_word[:-1]

if args.log:
	sys.stdout = open(args.log, 'a')
	sys.stderr = open(args.log, 'a')
	print('TextSuggest version {}, running on {}, with application {}.'.format(
		__version__,
		os.getenv('XDG_CURRENT_DESKTOP'),
		get_cmd_out('xdotool getwindowfocus getwindowname')))


def remove_dups(s_list):

	seen = set()
	seen_add = seen.add

	return [x for x in s_list if not (x in seen or seen_add(x))]

def get_dictionaries():

	dictionaries = []

	for lang in language:
		dictionaries.append(os.path.join(dict_dir, lang + '.txt'))

	if os.path.isfile(custom_words_file):
		dictionaries.append(custom_words_file)
	if os.path.isfile(extra_words_file):
		dictionaries.append(extra_words_file)

	return dictionaries

def get_focused_window():

	raw = get_cmd_out(['xdotool', 'getwindowfocus', 'getwindowname']).lower().split()

	try:
		return raw[len(raw) - 1]

	except:
		return ''

def is_program_gtk3(program):

	gtk3_apps = ['gedit', 'mousepad', 'abiword']

	if args.force_gtk3_fix:
		return True

	try:
		program_ldd = get_cmd_out('ldd $(which %s 2>/dev/null)' % program, suppress_stderr=True)

		return bool('libgtk-3' in program_ldd)

	except sp.CalledProcessError:
		# Not a dynamic executable
		pass

	try:
		with open(get_cmd_out('$(which %s 2>/dev/null)' % program), 'r') as f:
			contents = f.read()
			if 'require_version' in contents and 'Gtk' in contents and '3.0' in contents:
				return True

			elif 'from gi.repository import Gtk' in contents:
				return True

			elif 'require' in contents and 'gtk3' in contents:
				return True

	except:
		pass

	return bool(program.lower() in gtk3_apps)

def type_text(text):

	if '\n' in text:
		newline_list = text.split('\n')

		for i in newline_list:
			type_proc = sp.Popen(['xdotool', 'type', '--clearmodifiers', '--', i])

			type_proc.wait()
			sp.Popen(['xdotool', 'key', 'Shift+Return'])

			time.sleep(0.2)

	else:
		sp.Popen(['xdotool', 'type', '--', text])

def display_menu(items_list):

	mouse_loc_raw = get_cmd_out(['xdotool', 'getmouselocation', '--shell'])

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

	rofi_opts = ' '.join(args.rofi_options) if args.rofi_options else ''

	popup_menu_cmd_str = 'echo "%s" | rofi -dmenu -fuzzy -glob -matching glob -p "> " -i -font "%s" -xoffset %s -yoffset %s -location 1 %s' % (items_list, font, x, y, rofi_opts)

	# The argument list will sometimes be too long (too many words)
	# subprocess can't handle it, and will raise OSError.
	# So we will write it to a script file.

	with open(menu_script, 'w') as f:
		f.write(popup_menu_cmd_str)
	try:
		choice = get_cmd_out(['sh', menu_script])

	except sp.CalledProcessError:
		# No suggestion wanted
		print_error('ERR_REJECTED: User doesn\'t want any suggestion.')
		sys.stdout.flush()
		sys.exit(2)

	return choice

def process_suggestion(suggestion):

	if not args.no_history:
		with open(hist_file, 'a') as f:
			f.write('\n' + suggestion.replace('\n', '\\n'))

	if suggest_method == 'replace':
		if is_program_gtk3(get_focused_window()):
			print('Using GTK+ 3 workaround.')
			gtk3_fix = sp.Popen(['sleep 0.5; xdotool key Ctrl+Shift+Right; sleep 0.5'], shell=True)
			gtk3_fix.wait()
		# Erase current word
		sp.Popen(['xdotool', 'key', 'BackSpace'])

		if current_word[:1].isupper():
			suggestion = suggestion.capitalize()

	if '=' in suggestion:
		suggestion = suggestion.split('=', 1)[1]

	if args.no_processing:
		print('Processors disabled.')
		return suggestion

	processor_list = []

	for processor_dir in processor_dirs:
		if 'load-order.txt' in os.listdir(processor_dir):
			with open(os.path.join(processor_dir, 'load-order.txt')) as f:
				for line in f:
					if line.rstrip().endswith('.py'):
						line = line.rstrip('\n').rstrip('.py')

					processor_list.append(line)

		else:
			processor_list = [x.rstrip('.py') for x in os.listdir(processor_dir)]

		for processor_name in processor_list:
			processor = __import__(processor_name)

			processor_name_formatted = processor.__name__ + ' from ' + processor.__file__

			if processor.matches(suggestion):
				print('Using processor', processor_name_formatted)

				suggestion = processor.process(suggestion)

	return suggestion

def main():

	print('Running in %s mode.' % suggest_method)

	if suggest_method == 'replace':
		print('Getting suggestions for word:', current_word)

	words_list = get_suggestions(current_word, dict_files=get_dictionaries())

	if not words_list or words_list == ['']:
		if not args.exit_if_no_words_found:
			print('WARN_NOWORDS: Restarting in --no-selection mode. To prevent restarting, use --exit-on-no-words-found.')
			restart_program(additional_args=['--no-selection'])
		else:
			print_error('ERR_NOWORDS: No words found.')
			sys.exit(1)

	if args.no_history:
		print('History is disabled.')

	if not args.no_history:
		words_list.extend(get_suggestions(current_word, dict_files=[hist_file]))

		# Frequency sort + Remove duplicates
		words_list = uniq(freq_sort(words_list))

	words_list = '\n'.join(words_list)

	chosen_word = display_menu(words_list)

	print('Chosen word:', chosen_word)

	processed_chosen_word = process_suggestion(chosen_word)

	print('Processed:', processed_chosen_word)

	type_text(processed_chosen_word)

if __name__ == '__main__':
	main()
