# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# Contributor: Maksudur Rahman Maateen <ugcoderbd@gmail.com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

import subprocess as sp
import re

def get_language_name():

	# This function will return the language name
	# Reading keyboard layout from shell command

	# TODO: Add more definitions

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
			['setxkbmap', '-print'],
			universal_newlines=True)

	for i in xkb_map.splitlines():
		if 'xkb_symbols' in i:
			kbd_layout = i.strip().split()

	kbd_layout = kbd_layout[kbd_layout.index('include') + 1].split('+')[1]

	# Sometimes some text is included in brackets, remove that
	kbd_layout = re.sub(r'\(.*?\)', '', kbd_layout)


	# Language will be detected by layout

	if kbd_layout in languages:
		return languages[kbd_layout]

	else:
		return 'English'
