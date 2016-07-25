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

	orig_word = word

	word = word.lower()

	for dictionary in dict_files:
		with open(dictionary) as f:
			for dict_word in f:
				if word == '':
					suggestions.append(dict_word)
				else:
					if word in dict_word:
						suggestions.append(dict_word.rstrip('\r\n'))
					elif dict_word.startswith(word):
						suggestions.append(dict_word.rstrip('\r\n'))

	return suggestions
