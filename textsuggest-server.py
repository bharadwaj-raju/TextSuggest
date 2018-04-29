#!/usr/bin/env python3

# Copyright © 2018 Bharadwaj Raju <bharadwaj DOT raju777 AT gmail DOT com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

import subprocess as sp
import os
import sys
import json
import time
import re
import traceback

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GObject

import pyperclip


class DataBase(object):

	'''Simple "database", i.e. a wrapper over a dict/list + features to load-from/save-to disk'''

	def __init__(self, path, list_=False):

		self.path = path

		if list_:
			self.defaultobj = list
		else:
			self.defaultobj = dict

		self.load()


	def load(self):

		try:
			with open(self.path) as f:
				try:
					self.db = json.load(f)

				except json.JSONDecodeError:
					if not f.read():  # file is empty
						self.db = self.defaultobj()
						self.write()
					else:
						raise

		except FileNotFoundError:
			with open(self.path, 'w') as f:
				f.write(json.dumps(self.defaultobj()))

			self.db = self.defaultobj()

		try:
			self.clear = self.db.clear
			self.copy = self.db.copy
			self.items = self.db.items
			self.keys = self.db.keys
			self.values = self.db.values

		except AttributeError:  # list DB
			pass


	def write(self):

		with open(self.path, 'w') as f:
			json.dump(self.db, f, ensure_ascii=False)

	def __repr__(self):
		return 'DataBase(\'%s\')' % self.path

	def __getitem__(self, key):
		return self.db[key]

	def __setitem__(self, key, item):
		if self.defaultobj is list:
			self.defaultobj.insert(key, item)

		else:
			self.db[key] = item

	def __len__(self):
		return len(self.db)

	def __delitem__(self, key):
		del self.db[key]

	def __iter__(self):
		return iter(self.db)

	def pop(self, *args):
		return self.db.pop(*args)

	def has_key(self, key):
		return key in self.db


class SuggestionsCounter(dict):

	'''Dict that adds to existing entries on attempts to set them, instead of overwriting'''

	def __init__(self, *args):
		dict.__init__(self, *args)

	def __setitem__(self, key, item):
		# Add to existing entry else create new
		dict.__setitem__(self, key, dict.get(self, key, 0)+item)


class IncrementingDataBase(DataBase):

	def __setitem__(self, key, item):
		self.db[key] = self.db.get(key, 0) + item


class Service(dbus.service.Object):

	def __init__(self):
		pass


	def run(self):

		if os.getenv('XDG_RUNTIME_DIR'):
			self.runtime_dir = os.path.join(os.getenv('XDG_RUNTIME_DIR'), 'textsuggest')

		elif os.getenv('TMPDIR'):
			self.runtime_dir = os.path.join(os.getenv('TMPDIR'), 'textsuggest')

		else:
			self.runtime_dir = '/tmp/textsuggest'

		if not os.path.isdir(self.runtime_dir):
			os.mkdir(self.runtime_dir)

		self.script_cwd = os.path.abspath(os.path.join(__file__, os.pardir))
		self.config_home = os.getenv('XDG_CONFIG_HOME') or os.path.expanduser('~/.config')
		self.config_dir = os.path.join(self.config_home, 'textsuggest')
		self.dict_dir = '/usr/share/textsuggest/dictionaries'
		self.custom_words_file = os.path.join(self.config_dir, 'custom-words.json')
		self.history_file = os.path.join(self.config_dir, 'history.json')
		self.ignore_list_file = os.path.join(self.config_dir, 'ignore.json')
		self.processor_dirs = [os.path.join(self.config_dir, 'processors'),
							   '/usr/share/textsuggest/processors']

		self.dictionaries = {}
		self.dictionary_files = [(x.replace('.txt', ''), os.path.join(self.dict_dir, x)) for x in os.listdir(self.dict_dir)]

		self.history = IncrementingDataBase(self.history_file)

		for dict_file in self.dictionary_files:
			with open(dict_file[1]) as f:
				self.dictionaries[dict_file[0]] = f.read().splitlines()

		self.load_custom_words()
		self.load_ignore_list()

		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		bus_name = dbus.service.BusName("org.textsuggest.server", dbus.SessionBus())
		dbus.service.Object.__init__(self, bus_name, "/org/textsuggest/server")

		self._loop = GObject.MainLoop()
		self._loop.run()


	@dbus.service.method('org.textsuggest.server')
	def load_custom_words(self):

		try:
			with open(self.custom_words_file) as f:
				self.custom_words = json.load(f)

		except (json.JSONDecodeError, FileNotFoundError):
			print('Failed to open custom words file, or custom words file was empty.')
			self.custom_words = {}


	@dbus.service.method('org.textsuggest.server')
	def load_ignore_list(self):

		self.ignore_list = DataBase(self.ignore_list_file, list_=True)


	@dbus.service.method('org.textsuggest.server')
	def reload_configs(self):

		self.load_custom_words()
		self.load_ignore_list()

	def regex_search(self, regex, collection):

		suggestions = []

		for item in collection:
			match = regex.search(item)   # Checks if the current item matches the regex.
			if match:
				suggestions.append((len(match.group()), match.start(), item))

		return [x for _, _, x in sorted(suggestions)]


	@dbus.service.method('org.textsuggest.server', in_signature='sas', out_signature='as')
	def get_suggestions(self, word, languages):

		t1 = time.time()

		suggestions = SuggestionsCounter()

		# Format: {"word": points, …}
		# Each word has "points"
		# More points == higher ranking in results

		# SuggestionsCounter has the '=' operator overloaded to sort-of '+='
		# basically whenever you 'assign' some value to a key,
		# it actually appends value to existing value of the key

		installed_languages = [x for x in languages if x in self.dictionaries]

		sanitised_word = re.compile('[\(\)\+,\.!?]').sub('', word)

		pattern = '.*?'.join(sanitised_word)   # Converts 'abc' to 'a.*?b.*?c' so that 'abc' matches 'a_b_c' etc
		regex = re.compile(pattern)

		for lang in installed_languages:
			search_results = self.regex_search(regex, self.dictionaries[lang])
			search_results.reverse()
			# Best results go last, thus having a higher index
			for idx, dictword in enumerate(search_results):
				suggestions[dictword] = idx


		search_results = self.regex_search(regex, self.custom_words)
		search_results.reverse()
		# Best results go last, thus having a higher index
		for idx, custword in enumerate(search_results):
			suggestions[custword] = idx


		for histword in self.history:
			if histword in suggestions:
				if self.history[histword] > 1:
					suggestions[histword] = self.history[histword]

			elif word in histword:
				suggestions[histword] = self.history[histword]

		sorted_suggestions = [x for x in sorted(suggestions, key=suggestions.get, reverse=True) \
							  if x not in self.ignore_list]

		t2 = time.time()
		print('time get_suggestions(%s, %s) =' % (word, languages), t2-t1)

		return sorted_suggestions


	@dbus.service.method('org.textsuggest.server', in_signature='as', out_signature='as')
	def get_all_words(self, languages):

		t1 = time.time()

		suggestions = SuggestionsCounter()

		# Format: {"word": points, …}
		# Each word has "points"
		# More points == higher ranking in results

		installed_languages = [x for x in languages if x in self.dictionaries]

		for lang in installed_languages:
			suggestions.update({}.fromkeys(self.dictionaries[lang], 0))

		suggestions.update({}.fromkeys(self.custom_words, 0.5))

		for hist_word in self.history:
			if hist_word in suggestions:
				if self.history[hist_word] > 1:
					suggestions[hist_word] = self.history[hist_word]
			else:
				suggestions[hist_word] = self.history[hist_word]

		sorted_suggestions = [x for x in sorted(suggestions, key=suggestions.get, reverse=True) \
							  if x not in self.ignore_list]

		t2 = time.time()
		print('time get_all_words(%s) =' % languages, t2-t1)

		return sorted_suggestions


	@dbus.service.method('org.textsuggest.server', in_signature='s', out_signature='as')
	def get_custom_words_only(self, word):

		suggestions = SuggestionsCounter()

		if word:
			suggestions.update({}.fromkeys([x for x in self.custom_words if word in x], 0.5))
			suggestions.update({}.fromkeys([x for x in self.custom_words if x.startswith(word)], 1))

		else:
			suggestions.update({}.fromkeys(self.custom_words, 0.5))

		sorted_suggestions = [x for x in sorted(suggestions, key=suggestions.get, reverse=True) \
							  if x not in self.ignore_list]

		return sorted_suggestions


	@dbus.service.method('org.textsuggest.server', in_signature='s')
	def type_text(self, text):

		old_clipboard_text = self.get_clipboard_text()
		self.set_clipboard_text(text)
		sp.Popen(['xdotool', 'key', 'Control_L+v']).wait()
		self.set_clipboard_text(old_clipboard_text)


	@dbus.service.method('org.textsuggest.server', in_signature='s')
	def history_increment(self, word):

		self.history[word] = 1
		self.history.write()


	@dbus.service.method('org.textsuggest.server', in_signature='s')
	def history_remove(self, word):

		try:
			del self.history[word]

		except KeyError:
			pass

		self.history.write()


	@dbus.service.method('org.textsuggest.server', in_signature='s')
	def add_to_ignore_list(self, word):

		if word not in self.ignored:
			self.ignored.append(word)

		self.ignored.write()


	@dbus.service.method('org.textsuggest.server', in_signature='s', out_signature='s')
	def process_suggestion(self, suggestion):

		if suggestion in self.custom_words:
			suggestion = self.custom_words[suggestion]

		processor_list = []

		old_sys_path = sys.path[:]

		for processor_dir in self.processor_dirs:
			sys.path.insert(0, processor_dir)
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

				try:
					if processor.matches(suggestion):
						print('Using processor %s from %s' % (processor.__name__, processor.__file__))
						suggestion = processor.process(suggestion)

				except Exception as e:
					print(traceback.format_exc())

		sys.path = old_sys_path

		return suggestion


	@dbus.service.method('org.textsuggest.server', out_signature='s')
	def get_clipboard_text(self):

		return pyperclip.paste()


	@dbus.service.method('org.textsuggest.server', in_signature='s')
	def set_clipboard_text(self, text):

		return pyperclip.copy(text)


	@dbus.service.method('org.textsuggest.server', out_signature='s')
	def get_focused_window_id(self):

		return sp.check_output(['xdotool', 'getwindowfocus']).strip()


	@dbus.service.method('org.textsuggest.server', in_signature='s')
	def autoselect_current_word(self, mode):

		if mode == 'beginning':
			# Ctrl + Shift + ->
			sp.Popen([
				'xdotool key Control_L+Shift+Right'],
				shell=True).wait()
		elif mode == 'middle':
			# Ctrl + <- then Ctrl + Shift + ->
			sp.Popen([
				'xdotool key Control_L+Left; xdotool key Ctrl+Shift+Right'],
				shell=True).wait()
		else:
			# Ctrl + Shift + <-
			sp.Popen(['xdotool key Control_L+Shift+Left'],
					shell=True).wait()

	@dbus.service.method('org.textsuggest.server', out_signature='s')
	def get_selected_word(self):

		focused_window_id = self.get_focused_window_id()

		sp.Popen(['xdotool', 'windowactivate', focused_window_id])

		old_clipboard_text = self.get_clipboard_text()
		sp.Popen(['xdotool', 'windowactivate', focused_window_id, 'key', '--window', focused_window_id, '--clearmodifiers', 'Control_L+c']).wait()

		current_word = self.get_clipboard_text()
		self.set_clipboard_text(old_clipboard_text)

		return current_word


	@dbus.service.method('org.textsuggest.server', out_signature='s')
	def determine_language_from_keyboard_layout(self):

		languages = {
			'bd' : 'Bangla',
			'us' : 'English',
			'uk' : 'English',
			'gb' : 'English',
			'ara': 'Arabic',
			'cn' : 'Chinese',
			'tw' : 'Chinese',
			'de' : 'German',
			'jp' : 'Japanese',
			'ru' : 'Russian',
			'es' : 'Spanish',
			'se' : 'Swedish',
			'fi' : 'Finnish',
			'kr' : 'Korean',
			'pk' : 'Urdu',
			'fr' : 'French',
			'gr' : 'Greek',
			'ua' : 'Ukrainian'
		}

		xkb_map = sp.check_output(
				['setxkbmap', '-print'], universal_newlines=True)

		for i in xkb_map.splitlines():
			if 'xkb_symbols' in i:
				kbd_layout = i.strip().split()

		kbd_layout = kbd_layout[kbd_layout.index('include') + 1].split('+')[1]

		# Sometimes some text is included in brackets, remove that
		kbd_layout = re.sub(r'\(.*?\)', '', kbd_layout)

		return languages.get(kbd_layout, 'English')

	@dbus.service.method('org.textsuggest.server', in_signature='s', out_signature='i')
	def history_score(self, text):

		return self.history.get(text, 0)


	@dbus.service.method('org.textsuggest.server', in_signature='s', out_signature='b')
	def history_score(self, text):

		return text in self.custom_words



def main():

	pyperclip.set_clipboard('xclip')

	srv = Service()
	print('Started DBus service at org.textsuggest.server, PID %d' % os.getpid())
	srv.run()

if __name__ == '__main__':
	try:
		main()

	except KeyboardInterrupt:
		print('\nExiting…')
		sys.exit(1)
