def get_font_name(language):

    # This function will return the font name depending on the language

    fonts = {
                'Arabic' : 'Lateef 10',
                'Bangla' : 'SolaimanLipi 10',
                'Chinese' : 'MandarinFont 10',
                'Finnish' : '',
                'French' : '',
                'German' : '',
                'Greek' : '',
                'Japanese' : '',
                'Korean' : '',
                'Russian' : '',
                'Spanish' : '',
                'Swedish' : '',
                'Ukrainian' : '',
                'Urdu' : '',
            }

    if language in fonts:

        return fonts[language]
