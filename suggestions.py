# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>
# Contributor: Maksudur Rahman Maateen <ugcoderbd@gmail.com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

def get_suggestions(word, dict_files):

	'''Get a list of suggestions for 'word'

	Suggestions are taken from words in each file in the 'dict_files' list
	'''

	suggestions = []  # Store suggestions in this

	word = word.lower()

	for dictionary in dict_files:
		try:
			with open(dictionary) as f:
				dictionary_contents = f.read()
			
		except FileNotFoundError:
			dictionary_contents = ''

		for dict_word in dictionary_contents.split('\n'):
			if word in dict_word:
				suggestions.append(dict_word.rstrip('\r\n'))
			
			elif word.split(' ')[0] in dict_word:
				suggestions.append(dict_word.rstrip('\r\n'))

	return suggestions
