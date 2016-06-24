import os

def get_language_name():

    # This function will return the language name
    # Reading keyboard layout from shell command

    languages = {
                    'bd(probhat)' : 'Bangla',
                    'us' : 'English',
                    'uk' : 'English',
                }

    keyboard_layout = os.popen("setxkbmap -print | awk -F\"+\" '/xkb_symbols/ {print $2}'").read()
    keyboard_layout = keyboard_layout[:2]

    # Language will be detected by layout

    if keyboard_layout in languages:

        return languages[keyboard_layout]

    else:

        return 'English'