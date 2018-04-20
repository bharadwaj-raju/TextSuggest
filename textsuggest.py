#!/usr/bin/env python3

# Copyright © 2018 Bharadwaj Raju <bharadwaj DOT raju777 AT gmail DOT com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

from PyQt5 import Qt
import dbus

import sys
import subprocess as sp
import argparse

__version__ = 2002 # Updated using git pre-commit hook

WINDOW_WIDTH = 200


class Index(int):
	
	def __new__(cls, value, maxval, *args, **kwargs):
		#self.maxval = maxval
		if value < 0:
			raise ValueError('positive types must not be less than zero')
		retclass = super(Index, cls).__new__(cls, value)
		retclass.maxval = maxval
		return retclass

	def __add__(self, other):
		res = super(Index, self).__add__(other)
		return self.__normalized__(res)

	def __sub__(self, other):
		res = super(Index, self).__sub__(other)
		return self.__normalized__(res)

	def __mul__(self, other):
		res = super(Index, self).__mul__(other)
		return self.__normalized__(res)

	def __div__(self, other):
		res = super(Index, self).__div__(other)
		return self.__normalized__(res)

	def __normalized__(self, val):
		if val > self.maxval:
			val = self.maxval
		return self.__class__(max(val, 0), self.maxval)


class QEventCatcherEntry(Qt.QLineEdit):

	def __init__(self, catcher_fn):
		super(QEventCatcherEntry, self).__init__()
		self.oldKeyPressEvent = super(QEventCatcherEntry, self).keyPressEvent
		self.catcher_fn = catcher_fn

	def keyPressEvent(self, e):

		self.oldKeyPressEvent(e)
		self.catcher_fn(e)

	
class TextSuggestUI(Qt.QApplication):
	
	def __init__(self, server, opts):
		super(TextSuggestUI, self).__init__(sys.argv)
		self.server = server
		self.opts = opts
		self.languages = self.determineLanguages()
		self.loadUI()

		if opts.word:
			if opts.custom_words_only:
				self.allwords = self.server.get_custom_words_only(opts.word)
			
			else:
				self.allwords = self.server.get_suggestions(opts.word, self.languages)
		
		else:		
			if opts.custom_words_only:
				self.allwords = self.server.get_custom_words_only('')
			
			else:
				self.allwords = self.server.get_all_words(self.languages)
		
		self.populateSuggestions(self.allwords)


	def determineLanguages(self):

		if self.opts.language:
			return self.opts.language

		elif self.opts.auto_detect_language:
			return [self.server.determine_language_from_keyboard_layout()]

		else:
			return ['English']

	
	def loadUI(self):

		self.win = Qt.QMainWindow()
		
		self.win.setWindowFlags(self.win.windowFlags() | Qt.Qt.Tool | Qt.Qt.FramelessWindowHint | Qt.Qt.Popup)
		#self.win.keyPressEvent = self.keyEventCatcher
		
		self.mainWidget = Qt.QWidget()
		self.layout = Qt.QVBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.mainWidget.setContentsMargins(0, 0, 0, 0)
		self.win.setContentsMargins(0, 0, 0, 0)

		self.timer = Qt.QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.filterSuggestions)

		# The timer provides a delay of 200ms between user typing and list filtering

		self.entry = QEventCatcherEntry(catcher_fn=self.keyEventCatcher)
		self.entry.textEdited.connect(self.textEdited)
		self.layout.addWidget(self.entry)

		self.suggestion_list = Qt.QListWidget()
		self.suggestion_list.setSortingEnabled(False)
		self.layout.addWidget(self.suggestion_list)

		self.currentlySelectedIndex = Index(0, maxval=0)

		self.layout.setSizeConstraint(Qt.QLayout.SetFixedSize)
		self.mainWidget.setLayout(self.layout)
		self.win.setCentralWidget(self.mainWidget)

		self.adjustSizes()

	
	def keyEventCatcher(self, e):

		key = e.key()
		modifiers = e.modifiers()

		if key == Qt.Qt.Key_Escape:
			self.quit()

		if key == Qt.Qt.Key_Down:
			self.currentlySelectedIndex += 1
			self.suggestion_list.setCurrentRow(self.currentlySelectedIndex)
			self.entry.setText(self.suggestion_list.currentItem().text())

		if key == Qt.Qt.Key_Up:
			self.currentlySelectedIndex -= 1
			self.suggestion_list.setCurrentRow(self.currentlySelectedIndex)
			self.entry.setText(self.suggestion_list.currentItem().text())

		if key in (Qt.Qt.Key_Enter, Qt.Qt.Key_Return):
			self.applySuggestion()

		if key == Qt.Qt.Key_Delete:
			print('Delete')
			if (modifiers & Qt.Qt.ShiftModifier) and (modifiers & Qt.Qt.ControlModifier):
				print('Ctrl+Shift+Delete')
				self.addSuggestionToIgnoreList()
			
			if (modifiers & Qt.Qt.ShiftModifier):
				print('Shift+Delete')
				self.removeSuggestionFromHistory()


	def adjustSizes(self):

		self.win.resize(WINDOW_WIDTH, self.mainWidget.minimumHeight())


	def textEdited(self, text):

		self.timer.start(200)  # milliseconds


	def populateSuggestions(self, seq):

		self.suggestion_list.clear()

		for x in seq:
			Qt.QListWidgetItem(x, parent=self.suggestion_list)
		
		self.currentlySelectedIndex.maxval = len(seq)
		self.suggestion_list.setCurrentRow(0)


	def filterSuggestions(self):

		if not self.entry.text():
			suggestions = self.allwords

		else:
			if self.opts.custom_words_only:
				suggestions = self.server.get_custom_words_only(self.entry.text())

			else:
				suggestions = self.server.get_suggestions(self.entry.text(), self.languages)
		
		self.populateSuggestions(suggestions)


	def getText(self):

		if not self.suggestion_list.currentItem():
			return self.entry.text()

		else:
			return self.suggestion_list.currentItem().text()


	def applySuggestion(self):

		self.win.hide()

		text = self.getText()

		if not text:
			self.quit()
		
		if not self.opts.no_history:
			self.server.history_increment(text)
		
		if not self.opts.no_processing:
			text = self.server.process_suggestion(text)
		
		self.server.type_text(text)
		self.server.reload_configs()

		self.quit()


	def removeSuggestionFromHistory(self):

		text = self.getText()

		if text:
			self.server.history_remove(text)
			print('Removed', text, 'from history')


	def addSuggestionToIgnoreList(self):

		text = self.getText()

		if text:
			self.server.add_to_ignore_list(text)
			print('Added', text, 'to ignore list')

	
	def showUI(self):

		self.win.show()
		self.win.raise_()
		self.win.activateWindow()


def is_server_running():

	bus = dbus.SessionBus()

	try:
		bus.get_object('org.textsuggest.server', '/org/textsuggest/server')

	except dbus.DBusException:
		return False

	return True


def start_server():

	try:
		proc = sp.Popen(['python3', '/usr/bin/textsuggest-server'])

	except sp.CalledProcessError:
		print('Cannot start server! Exiting…')
		sys.exit(1)

	print('Started textsuggest-server with PID:', proc.pid)
	
	while not is_server_running():
		pass  # do not return until server is running


def get_server_connection():

	if not is_server_running():
		start_server()

	bus = dbus.SessionBus()
	return bus.get_object('org.textsuggest.server', '/org/textsuggest/server')


def main():

	arg_parser_args = {
		'description': '''TextSuggest — universal autocomplete''',
		'formatter_class': argparse.RawTextHelpFormatter,
		'usage': '%(prog)s [options]',
		'allow_abbrev': False,
	}

	if sys.version_info.minor > 5:
		# allow_abbrev not supported in Python >3.5 
		del arg_parser_args['allow_abbrev']

	arg_parser = argparse.ArgumentParser(**arg_parser_args)

	arg_parser.add_argument(
		'--word', type=str,
		help='Specify word to give suggestions for. Default: all words. \n \n',
		nargs='+', required=False)

	arg_parser.add_argument(
		'--no-history', action='store_true',
		help='Disable the frequently-used words history (stored in ~/.config/textsuggest/history.json) \n \n',
		required=False)

	arg_parser.add_argument(
		'--language', type=str,
		help='Set language(s). Default: English. See also: --auto-detect-language. \n \n',
		nargs='+', required=False, metavar='languages')

	arg_parser.add_argument(
		'--auto-detect-language', action='store_true',
		help='Auto-detect language from keyboard layout. \n \n',
		required=False)

	arg_parser.add_argument(
		'--selection', action='store_true',
		help='Show suggestions for currently selected word. See also: --auto-selection \n \n',
		required=False)

	arg_parser.add_argument(
		'--auto-selection', type=str, nargs='?',
		help='Automatically select word under cursor and suggest. Ignored if --no-selection. \n \n',
		choices=['beginning', 'middle', 'end'], const='end', required=False, metavar='beginning|middle|end')

	arg_parser.add_argument(
		'--custom-words-only', action='store_true',
		help='Show custom words only. \n \n', required=False)

	arg_parser.add_argument(
		'--no-processing', action='store_true',
		help='Disable using of any processors. \n \n', required=False)

	arg_parser.add_argument(
		'-v', '--version', action='store_true',
		help='Print version and license information.',
		required=False)
	
	opts = arg_parser.parse_args()

	if opts.version:
		print('''\
TextSuggest release 2.0.2 (build %d)

Copyright © 2016-2018 Bharadwaj Raju, and others <https://github.com/bharadwaj-raju/TextSuggest/graphs/contributors>.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.''' % __version__)
		sys.exit(0)

	server = get_server_connection()

	if opts.auto_selection:
		server.autoselect_current_word(opts.auto_selection)
		opts.word = server.get_selected_word()

	elif opts.selection:
		opts.word = server.get_selected_word()
	
	app = TextSuggestUI(server, opts)
	app.showUI()
	app.exec_()


if __name__ == '__main__':
	main()
