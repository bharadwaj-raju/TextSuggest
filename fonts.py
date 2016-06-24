def get_font_name(language):

    # This function will return the font name depending on the language

    fonts = {
                'Bangla' : 'SolaimanLipi 10',
            }

    if language in fonts:

        return fonts[language]
