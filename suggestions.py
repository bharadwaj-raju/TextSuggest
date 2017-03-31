# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>
# Contributor: Maksudur Rahman Maateen <ugcoderbd@gmail.com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

import subprocess as sp
import os
import json

def get_suggestions(word, dict_files):

	'''Get a list of suggestions for 'word'.

	Suggestions are taken from words in each file in the 'dict_files' list
	'''

	suggestions = []  # Store suggestions in this

	for dictionary in dict_files:
		if os.path.isfile(dictionary[1]):
			if dictionary[0] in ['REGULAR', 'EXTRA']:
				try:
					suggestions.extend(sp.check_output(['grep', '-i', '--', word, dictionary[1]]).decode('utf-8').rstrip().splitlines())

				except sp.CalledProcessError:
					# grep did not find word
					pass

			else:  # CUSTOM
				with open(dictionary[1]) as f:
					custom = json.load(f)

				if word:
					for cust in custom.keys():
						if word in cust:
							suggestions.append(cust)
							break

				else:
					suggestions.extend(custom.keys())

	return suggestions
