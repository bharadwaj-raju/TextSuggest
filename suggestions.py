# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>
# Contributor: Maksudur Rahman Maateen <ugcoderbd@gmail.com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

import subprocess as sp
import os

def get_suggestions(word, dict_files):

	'''Get a list of suggestions for 'word'

	Suggestions are taken from words in each file in the 'dict_files' list
	'''

	suggestions = []  # Store suggestions in this

	for dictionary in dict_files:
		if os.path.isfile(dictionary):
			try:
				suggestions.extend(sp.check_output(['grep', '-i', word, dictionary]).decode('utf-8').rstrip().split('\n'))

			except sp.CalledProcessError:
				# grep did not find word
				pass

	parsed_suggestions = []

	for i in suggestions:
		parsed_suggestions.append(i.replace('\n', r'\\\\n'))

	return parsed_suggestions
