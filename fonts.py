def get_font_name(langugae):

    # This function will return the font name depending on the language

    fonts = {
                'Bangla' : 'SolaimanLipi 10',
            }

    if langugae in fonts:

        return fonts[langugae]