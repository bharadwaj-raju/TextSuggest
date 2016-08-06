# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# Contributor: Maksudur Rahman Maateen <ugcoderbd@gmail.com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

import subprocess as sp

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
					'fi'  : 'Finnish',
					'kr' : 'Korean',
					'pk' : 'Urdu',
					'fr' : 'French',
					'gr' : 'Greek',
					'ua' : 'Ukrainian'
				}

	keyboard_layout_cmd_str = r"setxkbmap -print | awk -F '(+|\\()' '/xkb_symbols/ {print $2}'"

	keyboard_layout = sp.check_output(keyboard_layout_cmd_str, shell=True).decode('utf-8').rstrip()

	# Language will be detected by layout

	if keyboard_layout in languages:
		return languages[keyboard_layout]

	else:
		return 'English'
