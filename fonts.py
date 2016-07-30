# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>
# Contributor: Maksudur Rahman Maateen <ugcoderbd@gmail.com>

# This file is part of TextSuggest.

# TextSuggest is free software.
# Licensed under the GNU General Public License 3
# See included LICENSE file or visit https://www.gnu.org/licenses/gpl.txt

def get_font_name(language):

	'''Return appropriate font name for 'language' '''

	fonts = {
				'Arabic'	: 'Lateef 10',
				'Bangla'	: 'SolaimanLipi 10',
				'Chinese'   : 'Monospace 10',
				'Finnish'   : 'Monospace 10',
				'French'	: 'Monospace 10',
				'German'	: 'Monospace 10',
				'Greek'	 	: 'Monospace 10',
				'Japanese'  : 'Monospace 10',
				'Korean'	: 'Monospace 10',
				'Russian'   : 'Monospace 10',
				'Spanish'   : 'Monospace 10',
				'Swedish'   : 'Monospace 10',
				'Ukrainian' : 'Monospace 10',
				'Urdu'	  	: 'Lateef 10',
			}

	# NOTE: Why so many 'Monospace 10's?
	# Because it supports all the unicode characters needed for them.

	if language in fonts:

		return fonts[language]
