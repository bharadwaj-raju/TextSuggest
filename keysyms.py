# NOTE: dictionary further modified by Bharadwaj Raju <bharadwaj.raju@keemail.me>
# to use names instead of hexadecimal codes.
# The original can be found here:
# https://github.com/wavexx/screenkey/blob/master/Screenkey/keysyms.py


# https://www.cl.cam.ac.uk/~mgk25/ucs/keysyms.txt
# Mapping of X11 keysyms to ISO 10646 / Unicode
#
# The "X11 Window System Protocol" standard (Release 6.4) defines in
# Appendix A the keysym codes. These 29-bit integer values identify
# characters or functions associated with each key (e.g., via the
# visible engraving) of a keyboard layout. In addition, mnemonic macro
# names are provided for the keysyms in the C header file
# <X11/keysymdef.h>. These are compiled (by xc/lib/X11/util/
# makekeys.c) into a hash table that can be accessed with X11 library
# functions such as XStringToKeysym() and XKeysymToString().
#
# The creation of the keysym codes predates ISO 10646 / Unicode, but
# they represent a similar attempt to merge several existing coded
# character sets (mostly early drafts of ISO 8859, as well as some --
# long since forgotten -- DEC font encodings). X.Org and XFree86 have
# agreed that for any future extension of the keysyms with characters
# already found in ISO 10646 / Unicode, the following algorithm will
# be used. The new keysym code position will simply be the character's
# Unicode number plus 0x01000000. The keysym codes in the range
# 0x01000100 0x0110ffff are now reserved to represent Unicode
# characters in the range U0100 to U10FFFF. (Note that the ISO 8859-1
# characters that make up Unicode positions below U0100 are excluded
# from this rule, as they are already covered by the keysyms of the
# same value.)
#
# While most newer Unicode-based X11 clients do already accept
# Unicode-mapped keysyms in the range 0x01000100 to 0x0110ffff, it
# will remain necessary for clients -- in the interest of
# compatibility with existing servers -- to also understand the
# existing keysym values. Clients can use the table below to map the
# pre-Unicode keysym values (0x0100 to 0x20ff) to the corresponding
# Unicode characters for further processing.
#
# The following fields are used in this mapping table:
#
# 1    The hexadecimal X11 keysym number (as defined in Appendix A of
#      the X11 protocol specification and as listed in <X11/keysymdef.h>)
#
# 2    The corresponding Unicode position
#      (U0000 means that there is no equivalent Unicode character)
#
# 3    Status of this keysym and its Unicode mapping
#
#         .  regular -- This is a regular well-established keysym with
#            a straightforward Unicode equivalent (e.g., any keysym
#            derived from ISO 8859). There can be at most one regular
#            keysym associated with each Unicode character.
#
#         d  duplicate -- This keysym has the same Unicode mapping as
#            another one with status 'regular'. It represents a case
#            where keysyms distinguish between several characters that
#            Unicode has unified into a single one (examples are
#            several APL symbols)
#
#         o  obsolete -- While it may be possible to find a Unicode of
#            similar name, the exact semantics of this keysym are
#            unclear, because the font or character set from which it
#            came has never been widely used. Examples are various
#            symbols from the DEC Publishing character set, which may
#            have been used in a special font shipped with the
#            DECwrite product. Where no similar Unicode character
#            can be identified, U0000 is used in column 2.
#
#         f  function -- While it may be possible to find a Unicode
#            of similar name, this keysym differs semantically
#            substantially from the corresponding Unicode character,
#            because it describes a particular function key or will
#            first have to be processed by an input method that will
#            translate it into a proper stream of Unicode characters.
#
#         r  remove -- This is a bogus keysym that was added in error,
#            is not used in any known keyboard layout, and should be
#            removed from both <X11/keysymdef.h> and the standard.
#
#         u  unicode-remap -- This keysym was added rather recently to
#            the <X11/keysymdef.h> of XFree86, but into a number range
#            reserved for future extensions of the standard by
#            X.Org. It is not widely used at present, but its name
#            appears to be sufficiently useful and it should therefore
#            be directly mapped to Unicode in the 0x1xxxxxx range in
#            future versions of <X11/keysymdef.h>. This way, the macro
#            name will be preserved, but the standard will not have to
#            be extended.
#
#      Recommendations for using the keysym status:
#
#        - All keysyms with status regular, duplicate, obsolete and
#          function should be listed in Appendix A of the X11 protocol
#          spec.
#
#        - All keysyms except for those with status remove should be
#          listed in <X11/keysymdef.h>.
#
#        - Keysyms with status duplicate, obsolete, and remove should
#          not be used in future keyboard layouts, as there are other
#          keysyms with status regular, function and unicode-remap
#          that give access to the same Unicode characters.
#
#        - Keysym to Unicode conversion tables in clients should include
#          all mappings except those with status function and those
#          with U0000.
#
# #    comment marker
#
# 4    the name of the X11 keysym macro without the leading XK_,
#      as defined in <X11/keysymdef.h>
#
# The last columns may be followed by comments copied from <X11/keysymdef.h>.
# A keysym may be listed several times, if there are several macro names
# associated with it in <X11/keysymdef.h>.
#
# Author: Markus Kuhn <http://www.cl.cam.ac.uk/~mgk25/>
# Date:   2004-08-08
#
# This table evolved out of an earlier one by Richard Verhoeven, TU Eindhoven.

KEYSYMS = {
'space': [u'\u0020',	 '.'],	 # space
'exclam': [u'\u0021',	 '.'],	 # exclam
'quotedbl': [u'\u0022',	 '.'],	 # quotedbl
'numbersign': [u'\u0023',	 '.'],	 # numbersign
'dollar': [u'\u0024',	 '.'],	 # dollar
'percent': [u'\u0025',	 '.'],	 # percent
'ampersand': [u'\u0026',	 '.'],	 # ampersand
'apostrophe': [u'\u0027',	 '.'],	 # apostrophe
'quoteright': [u'\u0027',	 '.'],	 # quoteright	/* deprecated */
'parenleft': [u'\u0028',	 '.'],	 # parenleft
'parenright': [u'\u0029',	 '.'],	 # parenright
'asterisk': [u'\u002a',	 '.'],	 # asterisk
'plus': [u'\u002b',	 '.'],	 # plus
'comma': [u'\u002c',	 '.'],	 # comma
'minus': [u'\u002d',	 '.'],	 # minus
'period': [u'\u002e',	 '.'],	 # period
'slash': [u'\u002f',	 '.'],	 # slash
'0': [u'\u0030',	 '.'],	 # 0
'1': [u'\u0031',	 '.'],	 # 1
'2': [u'\u0032',	 '.'],	 # 2
'3': [u'\u0033',	 '.'],	 # 3
'4': [u'\u0034',	 '.'],	 # 4
'5': [u'\u0035',	 '.'],	 # 5
'6': [u'\u0036',	 '.'],	 # 6
'7': [u'\u0037',	 '.'],	 # 7
'8': [u'\u0038',	 '.'],	 # 8
'9': [u'\u0039',	 '.'],	 # 9
'colon': [u'\u003a',	 '.'],	 # colon
'semicolon': [u'\u003b',	 '.'],	 # semicolon
'less': [u'\u003c',	 '.'],	 # less
'equal': [u'\u003d',	 '.'],	 # equal
'greater': [u'\u003e',	 '.'],	 # greater
'question': [u'\u003f',	 '.'],	 # question
'at': [u'\u0040',	 '.'],	 # at
'A': [u'\u0041',	 '.'],	 # A
'B': [u'\u0042',	 '.'],	 # B
'C': [u'\u0043',	 '.'],	 # C
'D': [u'\u0044',	 '.'],	 # D
'E': [u'\u0045',	 '.'],	 # E
'F': [u'\u0046',	 '.'],	 # F
'G': [u'\u0047',	 '.'],	 # G
'H': [u'\u0048',	 '.'],	 # H
'I': [u'\u0049',	 '.'],	 # I
'J': [u'\u004a',	 '.'],	 # J
'K': [u'\u004b',	 '.'],	 # K
'L': [u'\u004c',	 '.'],	 # L
'M': [u'\u004d',	 '.'],	 # M
'N': [u'\u004e',	 '.'],	 # N
'O': [u'\u004f',	 '.'],	 # O
'P': [u'\u0050',	 '.'],	 # P
'Q': [u'\u0051',	 '.'],	 # Q
'R': [u'\u0052',	 '.'],	 # R
'S': [u'\u0053',	 '.'],	 # S
'T': [u'\u0054',	 '.'],	 # T
'U': [u'\u0055',	 '.'],	 # U
'V': [u'\u0056',	 '.'],	 # V
'W': [u'\u0057',	 '.'],	 # W
'X': [u'\u0058',	 '.'],	 # X
'Y': [u'\u0059',	 '.'],	 # Y
'Z': [u'\u005a',	 '.'],	 # Z
'bracketleft': [u'\u005b',	 '.'],	 # bracketleft
'backslash': [u'\u005c',	 '.'],	 # backslash
'bracketright': [u'\u005d',	 '.'],	 # bracketright
'asciicircum': [u'\u005e',	 '.'],	 # asciicircum
'underscore': [u'\u005f',	 '.'],	 # underscore
'grave': [u'\u0060',	 '.'],	 # grave
'quoteleft': [u'\u0060',	 '.'],	 # quoteleft	/* deprecated */
'a': [u'\u0061',	 '.'],	 # a
'b': [u'\u0062',	 '.'],	 # b
'c': [u'\u0063',	 '.'],	 # c
'd': [u'\u0064',	 '.'],	 # d
'e': [u'\u0065',	 '.'],	 # e
'f': [u'\u0066',	 '.'],	 # f
'g': [u'\u0067',	 '.'],	 # g
'h': [u'\u0068',	 '.'],	 # h
'i': [u'\u0069',	 '.'],	 # i
'j': [u'\u006a',	 '.'],	 # j
'k': [u'\u006b',	 '.'],	 # k
'l': [u'\u006c',	 '.'],	 # l
'm': [u'\u006d',	 '.'],	 # m
'n': [u'\u006e',	 '.'],	 # n
'o': [u'\u006f',	 '.'],	 # o
'p': [u'\u0070',	 '.'],	 # p
'q': [u'\u0071',	 '.'],	 # q
'r': [u'\u0072',	 '.'],	 # r
's': [u'\u0073',	 '.'],	 # s
't': [u'\u0074',	 '.'],	 # t
'u': [u'\u0075',	 '.'],	 # u
'v': [u'\u0076',	 '.'],	 # v
'w': [u'\u0077',	 '.'],	 # w
'x': [u'\u0078',	 '.'],	 # x
'y': [u'\u0079',	 '.'],	 # y
'z': [u'\u007a',	 '.'],	 # z
'braceleft': [u'\u007b',	 '.'],	 # braceleft
'bar': [u'\u007c',	 '.'],	 # bar
'braceright': [u'\u007d',	 '.'],	 # braceright
'asciitilde': [u'\u007e',	 '.'],	 # asciitilde
'nobreakspace': [u'\u00a0',	 '.'],	 # nobreakspace
'exclamdown': [u'\u00a1',	 '.'],	 # exclamdown
'cent': [u'\u00a2',	 '.'],	 # cent
'sterling': [u'\u00a3',	 '.'],	 # sterling
'currency': [u'\u00a4',	 '.'],	 # currency
'yen': [u'\u00a5',	 '.'],	 # yen
'brokenbar': [u'\u00a6',	 '.'],	 # brokenbar
'section': [u'\u00a7',	 '.'],	 # section
'diaeresis': [u'\u00a8',	 '.'],	 # diaeresis
'copyright': [u'\u00a9',	 '.'],	 # copyright
'ordfeminine': [u'\u00aa',	 '.'],	 # ordfeminine
'guillemotleft': [u'\u00ab',	 '.'],	 # guillemotleft	/* left angle quotation mark */
'notsign': [u'\u00ac',	 '.'],	 # notsign
'hyphen': [u'\u00ad',	 '.'],	 # hyphen
'registered': [u'\u00ae',	 '.'],	 # registered
'macron': [u'\u00af',	 '.'],	 # macron
'degree': [u'\u00b0',	 '.'],	 # degree
'plusminus': [u'\u00b1',	 '.'],	 # plusminus
'twosuperior': [u'\u00b2',	 '.'],	 # twosuperior
'threesuperior': [u'\u00b3',	 '.'],	 # threesuperior
'acute': [u'\u00b4',	 '.'],	 # acute
'mu': [u'\u00b5',	 '.'],	 # mu
'paragraph': [u'\u00b6',	 '.'],	 # paragraph
'periodcentered': [u'\u00b7',	 '.'],	 # periodcentered
'cedilla': [u'\u00b8',	 '.'],	 # cedilla
'onesuperior': [u'\u00b9',	 '.'],	 # onesuperior
'masculine': [u'\u00ba',	 '.'],	 # masculine
'guillemotright': [u'\u00bb',	 '.'],	 # guillemotright	/* right angle quotation mark */
'onequarter': [u'\u00bc',	 '.'],	 # onequarter
'onehalf': [u'\u00bd',	 '.'],	 # onehalf
'threequarters': [u'\u00be',	 '.'],	 # threequarters
'questiondown': [u'\u00bf',	 '.'],	 # questiondown
'Agrave': [u'\u00c0',	 '.'],	 # Agrave
'Aacute': [u'\u00c1',	 '.'],	 # Aacute
'Acircumflex': [u'\u00c2',	 '.'],	 # Acircumflex
'Atilde': [u'\u00c3',	 '.'],	 # Atilde
'Adiaeresis': [u'\u00c4',	 '.'],	 # Adiaeresis
'Aring': [u'\u00c5',	 '.'],	 # Aring
'AE': [u'\u00c6',	 '.'],	 # AE
'Ccedilla': [u'\u00c7',	 '.'],	 # Ccedilla
'Egrave': [u'\u00c8',	 '.'],	 # Egrave
'Eacute': [u'\u00c9',	 '.'],	 # Eacute
'Ecircumflex': [u'\u00ca',	 '.'],	 # Ecircumflex
'Ediaeresis': [u'\u00cb',	 '.'],	 # Ediaeresis
'Igrave': [u'\u00cc',	 '.'],	 # Igrave
'Iacute': [u'\u00cd',	 '.'],	 # Iacute
'Icircumflex': [u'\u00ce',	 '.'],	 # Icircumflex
'Idiaeresis': [u'\u00cf',	 '.'],	 # Idiaeresis
'ETH': [u'\u00d0',	 '.'],	 # ETH
'Eth': [u'\u00d0',	 '.'],	 # Eth	/* deprecated */
'Ntilde': [u'\u00d1',	 '.'],	 # Ntilde
'Ograve': [u'\u00d2',	 '.'],	 # Ograve
'Oacute': [u'\u00d3',	 '.'],	 # Oacute
'Ocircumflex': [u'\u00d4',	 '.'],	 # Ocircumflex
'Otilde': [u'\u00d5',	 '.'],	 # Otilde
'Odiaeresis': [u'\u00d6',	 '.'],	 # Odiaeresis
'multiply': [u'\u00d7',	 '.'],	 # multiply
'Ooblique': [u'\u00d8',	 '.'],	 # Ooblique
'Ugrave': [u'\u00d9',	 '.'],	 # Ugrave
'Uacute': [u'\u00da',	 '.'],	 # Uacute
'Ucircumflex': [u'\u00db',	 '.'],	 # Ucircumflex
'Udiaeresis': [u'\u00dc',	 '.'],	 # Udiaeresis
'Yacute': [u'\u00dd',	 '.'],	 # Yacute
'THORN': [u'\u00de',	 '.'],	 # THORN
'Thorn': [u'\u00de',	 '.'],	 # Thorn	/* deprecated */
'ssharp': [u'\u00df',	 '.'],	 # ssharp
'agrave': [u'\u00e0',	 '.'],	 # agrave
'aacute': [u'\u00e1',	 '.'],	 # aacute
'acircumflex': [u'\u00e2',	 '.'],	 # acircumflex
'atilde': [u'\u00e3',	 '.'],	 # atilde
'adiaeresis': [u'\u00e4',	 '.'],	 # adiaeresis
'aring': [u'\u00e5',	 '.'],	 # aring
'ae': [u'\u00e6',	 '.'],	 # ae
'ccedilla': [u'\u00e7',	 '.'],	 # ccedilla
'egrave': [u'\u00e8',	 '.'],	 # egrave
'eacute': [u'\u00e9',	 '.'],	 # eacute
'ecircumflex': [u'\u00ea',	 '.'],	 # ecircumflex
'ediaeresis': [u'\u00eb',	 '.'],	 # ediaeresis
'igrave': [u'\u00ec',	 '.'],	 # igrave
'iacute': [u'\u00ed',	 '.'],	 # iacute
'icircumflex': [u'\u00ee',	 '.'],	 # icircumflex
'idiaeresis': [u'\u00ef',	 '.'],	 # idiaeresis
'eth': [u'\u00f0',	 '.'],	 # eth
'ntilde': [u'\u00f1',	 '.'],	 # ntilde
'ograve': [u'\u00f2',	 '.'],	 # ograve
'oacute': [u'\u00f3',	 '.'],	 # oacute
'ocircumflex': [u'\u00f4',	 '.'],	 # ocircumflex
'otilde': [u'\u00f5',	 '.'],	 # otilde
'odiaeresis': [u'\u00f6',	 '.'],	 # odiaeresis
'division': [u'\u00f7',	 '.'],	 # division
'oslash': [u'\u00f8',	 '.'],	 # oslash
'ugrave': [u'\u00f9',	 '.'],	 # ugrave
'uacute': [u'\u00fa',	 '.'],	 # uacute
'ucircumflex': [u'\u00fb',	 '.'],	 # ucircumflex
'udiaeresis': [u'\u00fc',	 '.'],	 # udiaeresis
'yacute': [u'\u00fd',	 '.'],	 # yacute
'thorn': [u'\u00fe',	 '.'],	 # thorn
'ydiaeresis': [u'\u00ff',	 '.'],	 # ydiaeresis
'Aogonek': [u'\u0104',	 '.'],	 # Aogonek
'breve': [u'\u02d8',	 '.'],	 # breve
'Lstroke': [u'\u0141',	 '.'],	 # Lstroke
'Lcaron': [u'\u013d',	 '.'],	 # Lcaron
'Sacute': [u'\u015a',	 '.'],	 # Sacute
'Scaron': [u'\u0160',	 '.'],	 # Scaron
'Scedilla': [u'\u015e',	 '.'],	 # Scedilla
'Tcaron': [u'\u0164',	 '.'],	 # Tcaron
'Zacute': [u'\u0179',	 '.'],	 # Zacute
'Zcaron': [u'\u017d',	 '.'],	 # Zcaron
'Zabovedot': [u'\u017b',	 '.'],	 # Zabovedot
'aogonek': [u'\u0105',	 '.'],	 # aogonek
'ogonek': [u'\u02db',	 '.'],	 # ogonek
'lstroke': [u'\u0142',	 '.'],	 # lstroke
'lcaron': [u'\u013e',	 '.'],	 # lcaron
'sacute': [u'\u015b',	 '.'],	 # sacute
'caron': [u'\u02c7',	 '.'],	 # caron
'scaron': [u'\u0161',	 '.'],	 # scaron
'scedilla': [u'\u015f',	 '.'],	 # scedilla
'tcaron': [u'\u0165',	 '.'],	 # tcaron
'zacute': [u'\u017a',	 '.'],	 # zacute
'doubleacute': [u'\u02dd',	 '.'],	 # doubleacute
'zcaron': [u'\u017e',	 '.'],	 # zcaron
'zabovedot': [u'\u017c',	 '.'],	 # zabovedot
'Racute': [u'\u0154',	 '.'],	 # Racute
'Abreve': [u'\u0102',	 '.'],	 # Abreve
'Lacute': [u'\u0139',	 '.'],	 # Lacute
'Cacute': [u'\u0106',	 '.'],	 # Cacute
'Ccaron': [u'\u010c',	 '.'],	 # Ccaron
'Eogonek': [u'\u0118',	 '.'],	 # Eogonek
'Ecaron': [u'\u011a',	 '.'],	 # Ecaron
'Dcaron': [u'\u010e',	 '.'],	 # Dcaron
'Dstroke': [u'\u0110',	 '.'],	 # Dstroke
'Nacute': [u'\u0143',	 '.'],	 # Nacute
'Ncaron': [u'\u0147',	 '.'],	 # Ncaron
'Odoubleacute': [u'\u0150',	 '.'],	 # Odoubleacute
'Rcaron': [u'\u0158',	 '.'],	 # Rcaron
'Uring': [u'\u016e',	 '.'],	 # Uring
'Udoubleacute': [u'\u0170',	 '.'],	 # Udoubleacute
'Tcedilla': [u'\u0162',	 '.'],	 # Tcedilla
'racute': [u'\u0155',	 '.'],	 # racute
'abreve': [u'\u0103',	 '.'],	 # abreve
'lacute': [u'\u013a',	 '.'],	 # lacute
'cacute': [u'\u0107',	 '.'],	 # cacute
'ccaron': [u'\u010d',	 '.'],	 # ccaron
'eogonek': [u'\u0119',	 '.'],	 # eogonek
'ecaron': [u'\u011b',	 '.'],	 # ecaron
'dcaron': [u'\u010f',	 '.'],	 # dcaron
'dstroke': [u'\u0111',	 '.'],	 # dstroke
'nacute': [u'\u0144',	 '.'],	 # nacute
'ncaron': [u'\u0148',	 '.'],	 # ncaron
'odoubleacute': [u'\u0151',	 '.'],	 # odoubleacute
'rcaron': [u'\u0159',	 '.'],	 # rcaron
'uring': [u'\u016f',	 '.'],	 # uring
'udoubleacute': [u'\u0171',	 '.'],	 # udoubleacute
'tcedilla': [u'\u0163',	 '.'],	 # tcedilla
'abovedot': [u'\u02d9',	 '.'],	 # abovedot
'Hstroke': [u'\u0126',	 '.'],	 # Hstroke
'Hcircumflex': [u'\u0124',	 '.'],	 # Hcircumflex
'Iabovedot': [u'\u0130',	 '.'],	 # Iabovedot
'Gbreve': [u'\u011e',	 '.'],	 # Gbreve
'Jcircumflex': [u'\u0134',	 '.'],	 # Jcircumflex
'hstroke': [u'\u0127',	 '.'],	 # hstroke
'hcircumflex': [u'\u0125',	 '.'],	 # hcircumflex
'idotless': [u'\u0131',	 '.'],	 # idotless
'gbreve': [u'\u011f',	 '.'],	 # gbreve
'jcircumflex': [u'\u0135',	 '.'],	 # jcircumflex
'Cabovedot': [u'\u010a',	 '.'],	 # Cabovedot
'Ccircumflex': [u'\u0108',	 '.'],	 # Ccircumflex
'Gabovedot': [u'\u0120',	 '.'],	 # Gabovedot
'Gcircumflex': [u'\u011c',	 '.'],	 # Gcircumflex
'Ubreve': [u'\u016c',	 '.'],	 # Ubreve
'Scircumflex': [u'\u015c',	 '.'],	 # Scircumflex
'cabovedot': [u'\u010b',	 '.'],	 # cabovedot
'ccircumflex': [u'\u0109',	 '.'],	 # ccircumflex
'gabovedot': [u'\u0121',	 '.'],	 # gabovedot
'gcircumflex': [u'\u011d',	 '.'],	 # gcircumflex
'ubreve': [u'\u016d',	 '.'],	 # ubreve
'scircumflex': [u'\u015d',	 '.'],	 # scircumflex
'kra': [u'\u0138',	 '.'],	 # kra
'Rcedilla': [u'\u0156',	 '.'],	 # Rcedilla
'Itilde': [u'\u0128',	 '.'],	 # Itilde
'Lcedilla': [u'\u013b',	 '.'],	 # Lcedilla
'Emacron': [u'\u0112',	 '.'],	 # Emacron
'Gcedilla': [u'\u0122',	 '.'],	 # Gcedilla
'Tslash': [u'\u0166',	 '.'],	 # Tslash
'rcedilla': [u'\u0157',	 '.'],	 # rcedilla
'itilde': [u'\u0129',	 '.'],	 # itilde
'lcedilla': [u'\u013c',	 '.'],	 # lcedilla
'emacron': [u'\u0113',	 '.'],	 # emacron
'gcedilla': [u'\u0123',	 '.'],	 # gcedilla
'tslash': [u'\u0167',	 '.'],	 # tslash
'ENG': [u'\u014a',	 '.'],	 # ENG
'eng': [u'\u014b',	 '.'],	 # eng
'Amacron': [u'\u0100',	 '.'],	 # Amacron
'Iogonek': [u'\u012e',	 '.'],	 # Iogonek
'Eabovedot': [u'\u0116',	 '.'],	 # Eabovedot
'Imacron': [u'\u012a',	 '.'],	 # Imacron
'Ncedilla': [u'\u0145',	 '.'],	 # Ncedilla
'Omacron': [u'\u014c',	 '.'],	 # Omacron
'Kcedilla': [u'\u0136',	 '.'],	 # Kcedilla
'Uogonek': [u'\u0172',	 '.'],	 # Uogonek
'Utilde': [u'\u0168',	 '.'],	 # Utilde
'Umacron': [u'\u016a',	 '.'],	 # Umacron
'amacron': [u'\u0101',	 '.'],	 # amacron
'iogonek': [u'\u012f',	 '.'],	 # iogonek
'eabovedot': [u'\u0117',	 '.'],	 # eabovedot
'imacron': [u'\u012b',	 '.'],	 # imacron
'ncedilla': [u'\u0146',	 '.'],	 # ncedilla
'omacron': [u'\u014d',	 '.'],	 # omacron
'kcedilla': [u'\u0137',	 '.'],	 # kcedilla
'uogonek': [u'\u0173',	 '.'],	 # uogonek
'utilde': [u'\u0169',	 '.'],	 # utilde
'umacron': [u'\u016b',	 '.'],	 # umacron
'overline': [u'\u203e',	 '.'],	 # overline
'kana_fullstop': [u'\u3002',	 '.'],	 # kana_fullstop
'kana_openingbracket': [u'\u300c',	 '.'],	 # kana_openingbracket
'kana_closingbracket': [u'\u300d',	 '.'],	 # kana_closingbracket
'kana_comma': [u'\u3001',	 '.'],	 # kana_comma
'kana_conjunctive': [u'\u30fb',	 '.'],	 # kana_conjunctive
'kana_WO': [u'\u30f2',	 '.'],	 # kana_WO
'kana_a': [u'\u30a1',	 '.'],	 # kana_a
'kana_i': [u'\u30a3',	 '.'],	 # kana_i
'kana_u': [u'\u30a5',	 '.'],	 # kana_u
'kana_e': [u'\u30a7',	 '.'],	 # kana_e
'kana_o': [u'\u30a9',	 '.'],	 # kana_o
'kana_ya': [u'\u30e3',	 '.'],	 # kana_ya
'kana_yu': [u'\u30e5',	 '.'],	 # kana_yu
'kana_yo': [u'\u30e7',	 '.'],	 # kana_yo
'kana_tsu': [u'\u30c3',	 '.'],	 # kana_tsu
'prolongedsound': [u'\u30fc',	 '.'],	 # prolongedsound
'kana_A': [u'\u30a2',	 '.'],	 # kana_A
'kana_I': [u'\u30a4',	 '.'],	 # kana_I
'kana_U': [u'\u30a6',	 '.'],	 # kana_U
'kana_E': [u'\u30a8',	 '.'],	 # kana_E
'kana_O': [u'\u30aa',	 '.'],	 # kana_O
'kana_KA': [u'\u30ab',	 '.'],	 # kana_KA
'kana_KI': [u'\u30ad',	 '.'],	 # kana_KI
'kana_KU': [u'\u30af',	 '.'],	 # kana_KU
'kana_KE': [u'\u30b1',	 '.'],	 # kana_KE
'kana_KO': [u'\u30b3',	 '.'],	 # kana_KO
'kana_SA': [u'\u30b5',	 '.'],	 # kana_SA
'kana_SHI': [u'\u30b7',	 '.'],	 # kana_SHI
'kana_SU': [u'\u30b9',	 '.'],	 # kana_SU
'kana_SE': [u'\u30bb',	 '.'],	 # kana_SE
'kana_SO': [u'\u30bd',	 '.'],	 # kana_SO
'kana_TA': [u'\u30bf',	 '.'],	 # kana_TA
'kana_CHI': [u'\u30c1',	 '.'],	 # kana_CHI
'kana_TSU': [u'\u30c4',	 '.'],	 # kana_TSU
'kana_TE': [u'\u30c6',	 '.'],	 # kana_TE
'kana_TO': [u'\u30c8',	 '.'],	 # kana_TO
'kana_NA': [u'\u30ca',	 '.'],	 # kana_NA
'kana_NI': [u'\u30cb',	 '.'],	 # kana_NI
'kana_NU': [u'\u30cc',	 '.'],	 # kana_NU
'kana_NE': [u'\u30cd',	 '.'],	 # kana_NE
'kana_NO': [u'\u30ce',	 '.'],	 # kana_NO
'kana_HA': [u'\u30cf',	 '.'],	 # kana_HA
'kana_HI': [u'\u30d2',	 '.'],	 # kana_HI
'kana_FU': [u'\u30d5',	 '.'],	 # kana_FU
'kana_HE': [u'\u30d8',	 '.'],	 # kana_HE
'kana_HO': [u'\u30db',	 '.'],	 # kana_HO
'kana_MA': [u'\u30de',	 '.'],	 # kana_MA
'kana_MI': [u'\u30df',	 '.'],	 # kana_MI
'kana_MU': [u'\u30e0',	 '.'],	 # kana_MU
'kana_ME': [u'\u30e1',	 '.'],	 # kana_ME
'kana_MO': [u'\u30e2',	 '.'],	 # kana_MO
'kana_YA': [u'\u30e4',	 '.'],	 # kana_YA
'kana_YU': [u'\u30e6',	 '.'],	 # kana_YU
'kana_YO': [u'\u30e8',	 '.'],	 # kana_YO
'kana_RA': [u'\u30e9',	 '.'],	 # kana_RA
'kana_RI': [u'\u30ea',	 '.'],	 # kana_RI
'kana_RU': [u'\u30eb',	 '.'],	 # kana_RU
'kana_RE': [u'\u30ec',	 '.'],	 # kana_RE
'kana_RO': [u'\u30ed',	 '.'],	 # kana_RO
'kana_WA': [u'\u30ef',	 '.'],	 # kana_WA
'kana_N': [u'\u30f3',	 '.'],	 # kana_N
'voicedsound': [u'\u309b',	 '.'],	 # voicedsound
'semivoicedsound': [u'\u309c',	 '.'],	 # semivoicedsound
'Arabic_comma': [u'\u060c',	 '.'],	 # Arabic_comma
'Arabic_semicolon': [u'\u061b',	 '.'],	 # Arabic_semicolon
'Arabic_question_mark': [u'\u061f',	 '.'],	 # Arabic_question_mark
'Arabic_hamza': [u'\u0621',	 '.'],	 # Arabic_hamza
'Arabic_maddaonalef': [u'\u0622',	 '.'],	 # Arabic_maddaonalef
'Arabic_hamzaonalef': [u'\u0623',	 '.'],	 # Arabic_hamzaonalef
'Arabic_hamzaonwaw': [u'\u0624',	 '.'],	 # Arabic_hamzaonwaw
'Arabic_hamzaunderalef': [u'\u0625',	 '.'],	 # Arabic_hamzaunderalef
'Arabic_hamzaonyeh': [u'\u0626',	 '.'],	 # Arabic_hamzaonyeh
'Arabic_alef': [u'\u0627',	 '.'],	 # Arabic_alef
'Arabic_beh': [u'\u0628',	 '.'],	 # Arabic_beh
'Arabic_tehmarbuta': [u'\u0629',	 '.'],	 # Arabic_tehmarbuta
'Arabic_teh': [u'\u062a',	 '.'],	 # Arabic_teh
'Arabic_theh': [u'\u062b',	 '.'],	 # Arabic_theh
'Arabic_jeem': [u'\u062c',	 '.'],	 # Arabic_jeem
'Arabic_hah': [u'\u062d',	 '.'],	 # Arabic_hah
'Arabic_khah': [u'\u062e',	 '.'],	 # Arabic_khah
'Arabic_dal': [u'\u062f',	 '.'],	 # Arabic_dal
'Arabic_thal': [u'\u0630',	 '.'],	 # Arabic_thal
'Arabic_ra': [u'\u0631',	 '.'],	 # Arabic_ra
'Arabic_zain': [u'\u0632',	 '.'],	 # Arabic_zain
'Arabic_seen': [u'\u0633',	 '.'],	 # Arabic_seen
'Arabic_sheen': [u'\u0634',	 '.'],	 # Arabic_sheen
'Arabic_sad': [u'\u0635',	 '.'],	 # Arabic_sad
'Arabic_dad': [u'\u0636',	 '.'],	 # Arabic_dad
'Arabic_tah': [u'\u0637',	 '.'],	 # Arabic_tah
'Arabic_zah': [u'\u0638',	 '.'],	 # Arabic_zah
'Arabic_ain': [u'\u0639',	 '.'],	 # Arabic_ain
'Arabic_ghain': [u'\u063a',	 '.'],	 # Arabic_ghain
'Arabic_tatweel': [u'\u0640',	 '.'],	 # Arabic_tatweel
'Arabic_feh': [u'\u0641',	 '.'],	 # Arabic_feh
'Arabic_qaf': [u'\u0642',	 '.'],	 # Arabic_qaf
'Arabic_kaf': [u'\u0643',	 '.'],	 # Arabic_kaf
'Arabic_lam': [u'\u0644',	 '.'],	 # Arabic_lam
'Arabic_meem': [u'\u0645',	 '.'],	 # Arabic_meem
'Arabic_noon': [u'\u0646',	 '.'],	 # Arabic_noon
'Arabic_ha': [u'\u0647',	 '.'],	 # Arabic_ha
'Arabic_waw': [u'\u0648',	 '.'],	 # Arabic_waw
'Arabic_alefmaksura': [u'\u0649',	 '.'],	 # Arabic_alefmaksura
'Arabic_yeh': [u'\u064a',	 '.'],	 # Arabic_yeh
'Arabic_fathatan': [u'\u064b',	 '.'],	 # Arabic_fathatan
'Arabic_dammatan': [u'\u064c',	 '.'],	 # Arabic_dammatan
'Arabic_kasratan': [u'\u064d',	 '.'],	 # Arabic_kasratan
'Arabic_fatha': [u'\u064e',	 '.'],	 # Arabic_fatha
'Arabic_damma': [u'\u064f',	 '.'],	 # Arabic_damma
'Arabic_kasra': [u'\u0650',	 '.'],	 # Arabic_kasra
'Arabic_shadda': [u'\u0651',	 '.'],	 # Arabic_shadda
'Arabic_sukun': [u'\u0652',	 '.'],	 # Arabic_sukun
'Serbian_dje': [u'\u0452',	 '.'],	 # Serbian_dje
'Macedonia_gje': [u'\u0453',	 '.'],	 # Macedonia_gje
'Cyrillic_io': [u'\u0451',	 '.'],	 # Cyrillic_io
'Ukrainian_ie': [u'\u0454',	 '.'],	 # Ukrainian_ie
'Macedonia_dse': [u'\u0455',	 '.'],	 # Macedonia_dse
'Ukrainian_i': [u'\u0456',	 '.'],	 # Ukrainian_i
'Ukrainian_yi': [u'\u0457',	 '.'],	 # Ukrainian_yi
'Cyrillic_je': [u'\u0458',	 '.'],	 # Cyrillic_je
'Cyrillic_lje': [u'\u0459',	 '.'],	 # Cyrillic_lje
'Cyrillic_nje': [u'\u045a',	 '.'],	 # Cyrillic_nje
'Serbian_tshe': [u'\u045b',	 '.'],	 # Serbian_tshe
'Macedonia_kje': [u'\u045c',	 '.'],	 # Macedonia_kje
'Byelorussian_shortu': [u'\u045e',	 '.'],	 # Byelorussian_shortu
'Cyrillic_dzhe': [u'\u045f',	 '.'],	 # Cyrillic_dzhe
'numerosign': [u'\u2116',	 '.'],	 # numerosign
'Serbian_DJE': [u'\u0402',	 '.'],	 # Serbian_DJE
'Macedonia_GJE': [u'\u0403',	 '.'],	 # Macedonia_GJE
'Cyrillic_IO': [u'\u0401',	 '.'],	 # Cyrillic_IO
'Ukrainian_IE': [u'\u0404',	 '.'],	 # Ukrainian_IE
'Macedonia_DSE': [u'\u0405',	 '.'],	 # Macedonia_DSE
'Ukrainian_I': [u'\u0406',	 '.'],	 # Ukrainian_I
'Ukrainian_YI': [u'\u0407',	 '.'],	 # Ukrainian_YI
'Cyrillic_JE': [u'\u0408',	 '.'],	 # Cyrillic_JE
'Cyrillic_LJE': [u'\u0409',	 '.'],	 # Cyrillic_LJE
'Cyrillic_NJE': [u'\u040a',	 '.'],	 # Cyrillic_NJE
'Serbian_TSHE': [u'\u040b',	 '.'],	 # Serbian_TSHE
'Macedonia_KJE': [u'\u040c',	 '.'],	 # Macedonia_KJE
'Byelorussian_SHORTU': [u'\u040e',	 '.'],	 # Byelorussian_SHORTU
'Cyrillic_DZHE': [u'\u040f',	 '.'],	 # Cyrillic_DZHE
'Cyrillic_yu': [u'\u044e',	 '.'],	 # Cyrillic_yu
'Cyrillic_a': [u'\u0430',	 '.'],	 # Cyrillic_a
'Cyrillic_be': [u'\u0431',	 '.'],	 # Cyrillic_be
'Cyrillic_tse': [u'\u0446',	 '.'],	 # Cyrillic_tse
'Cyrillic_de': [u'\u0434',	 '.'],	 # Cyrillic_de
'Cyrillic_ie': [u'\u0435',	 '.'],	 # Cyrillic_ie
'Cyrillic_ef': [u'\u0444',	 '.'],	 # Cyrillic_ef
'Cyrillic_ghe': [u'\u0433',	 '.'],	 # Cyrillic_ghe
'Cyrillic_ha': [u'\u0445',	 '.'],	 # Cyrillic_ha
'Cyrillic_i': [u'\u0438',	 '.'],	 # Cyrillic_i
'Cyrillic_shorti': [u'\u0439',	 '.'],	 # Cyrillic_shorti
'Cyrillic_ka': [u'\u043a',	 '.'],	 # Cyrillic_ka
'Cyrillic_el': [u'\u043b',	 '.'],	 # Cyrillic_el
'Cyrillic_em': [u'\u043c',	 '.'],	 # Cyrillic_em
'Cyrillic_en': [u'\u043d',	 '.'],	 # Cyrillic_en
'Cyrillic_o': [u'\u043e',	 '.'],	 # Cyrillic_o
'Cyrillic_pe': [u'\u043f',	 '.'],	 # Cyrillic_pe
'Cyrillic_ya': [u'\u044f',	 '.'],	 # Cyrillic_ya
'Cyrillic_er': [u'\u0440',	 '.'],	 # Cyrillic_er
'Cyrillic_es': [u'\u0441',	 '.'],	 # Cyrillic_es
'Cyrillic_te': [u'\u0442',	 '.'],	 # Cyrillic_te
'Cyrillic_u': [u'\u0443',	 '.'],	 # Cyrillic_u
'Cyrillic_zhe': [u'\u0436',	 '.'],	 # Cyrillic_zhe
'Cyrillic_ve': [u'\u0432',	 '.'],	 # Cyrillic_ve
'Cyrillic_softsign': [u'\u044c',	 '.'],	 # Cyrillic_softsign
'Cyrillic_yeru': [u'\u044b',	 '.'],	 # Cyrillic_yeru
'Cyrillic_ze': [u'\u0437',	 '.'],	 # Cyrillic_ze
'Cyrillic_sha': [u'\u0448',	 '.'],	 # Cyrillic_sha
'Cyrillic_e': [u'\u044d',	 '.'],	 # Cyrillic_e
'Cyrillic_shcha': [u'\u0449',	 '.'],	 # Cyrillic_shcha
'Cyrillic_che': [u'\u0447',	 '.'],	 # Cyrillic_che
'Cyrillic_hardsign': [u'\u044a',	 '.'],	 # Cyrillic_hardsign
'Cyrillic_YU': [u'\u042e',	 '.'],	 # Cyrillic_YU
'Cyrillic_A': [u'\u0410',	 '.'],	 # Cyrillic_A
'Cyrillic_BE': [u'\u0411',	 '.'],	 # Cyrillic_BE
'Cyrillic_TSE': [u'\u0426',	 '.'],	 # Cyrillic_TSE
'Cyrillic_DE': [u'\u0414',	 '.'],	 # Cyrillic_DE
'Cyrillic_IE': [u'\u0415',	 '.'],	 # Cyrillic_IE
'Cyrillic_EF': [u'\u0424',	 '.'],	 # Cyrillic_EF
'Cyrillic_GHE': [u'\u0413',	 '.'],	 # Cyrillic_GHE
'Cyrillic_HA': [u'\u0425',	 '.'],	 # Cyrillic_HA
'Cyrillic_I': [u'\u0418',	 '.'],	 # Cyrillic_I
'Cyrillic_SHORTI': [u'\u0419',	 '.'],	 # Cyrillic_SHORTI
'Cyrillic_KA': [u'\u041a',	 '.'],	 # Cyrillic_KA
'Cyrillic_EL': [u'\u041b',	 '.'],	 # Cyrillic_EL
'Cyrillic_EM': [u'\u041c',	 '.'],	 # Cyrillic_EM
'Cyrillic_EN': [u'\u041d',	 '.'],	 # Cyrillic_EN
'Cyrillic_O': [u'\u041e',	 '.'],	 # Cyrillic_O
'Cyrillic_PE': [u'\u041f',	 '.'],	 # Cyrillic_PE
'Cyrillic_YA': [u'\u042f',	 '.'],	 # Cyrillic_YA
'Cyrillic_ER': [u'\u0420',	 '.'],	 # Cyrillic_ER
'Cyrillic_ES': [u'\u0421',	 '.'],	 # Cyrillic_ES
'Cyrillic_TE': [u'\u0422',	 '.'],	 # Cyrillic_TE
'Cyrillic_U': [u'\u0423',	 '.'],	 # Cyrillic_U
'Cyrillic_ZHE': [u'\u0416',	 '.'],	 # Cyrillic_ZHE
'Cyrillic_VE': [u'\u0412',	 '.'],	 # Cyrillic_VE
'Cyrillic_SOFTSIGN': [u'\u042c',	 '.'],	 # Cyrillic_SOFTSIGN
'Cyrillic_YERU': [u'\u042b',	 '.'],	 # Cyrillic_YERU
'Cyrillic_ZE': [u'\u0417',	 '.'],	 # Cyrillic_ZE
'Cyrillic_SHA': [u'\u0428',	 '.'],	 # Cyrillic_SHA
'Cyrillic_E': [u'\u042d',	 '.'],	 # Cyrillic_E
'Cyrillic_SHCHA': [u'\u0429',	 '.'],	 # Cyrillic_SHCHA
'Cyrillic_CHE': [u'\u0427',	 '.'],	 # Cyrillic_CHE
'Cyrillic_HARDSIGN': [u'\u042a',	 '.'],	 # Cyrillic_HARDSIGN
'Greek_ALPHAaccent': [u'\u0386',	 '.'],	 # Greek_ALPHAaccent
'Greek_EPSILONaccent': [u'\u0388',	 '.'],	 # Greek_EPSILONaccent
'Greek_ETAaccent': [u'\u0389',	 '.'],	 # Greek_ETAaccent
'Greek_IOTAaccent': [u'\u038a',	 '.'],	 # Greek_IOTAaccent
'Greek_IOTAdiaeresis': [u'\u03aa',	 '.'],	 # Greek_IOTAdiaeresis
'Greek_OMICRONaccent': [u'\u038c',	 '.'],	 # Greek_OMICRONaccent
'Greek_UPSILONaccent': [u'\u038e',	 '.'],	 # Greek_UPSILONaccent
'Greek_UPSILONdieresis': [u'\u03ab',	 '.'],	 # Greek_UPSILONdieresis
'Greek_OMEGAaccent': [u'\u038f',	 '.'],	 # Greek_OMEGAaccent
'Greek_accentdieresis': [u'\u0385',	 '.'],	 # Greek_accentdieresis
'Greek_horizbar': [u'\u2015',	 '.'],	 # Greek_horizbar
'Greek_alphaaccent': [u'\u03ac',	 '.'],	 # Greek_alphaaccent
'Greek_epsilonaccent': [u'\u03ad',	 '.'],	 # Greek_epsilonaccent
'Greek_etaaccent': [u'\u03ae',	 '.'],	 # Greek_etaaccent
'Greek_iotaaccent': [u'\u03af',	 '.'],	 # Greek_iotaaccent
'Greek_iotadieresis': [u'\u03ca',	 '.'],	 # Greek_iotadieresis
'Greek_iotaaccentdieresis': [u'\u0390',	 '.'],	 # Greek_iotaaccentdieresis
'Greek_omicronaccent': [u'\u03cc',	 '.'],	 # Greek_omicronaccent
'Greek_upsilonaccent': [u'\u03cd',	 '.'],	 # Greek_upsilonaccent
'Greek_upsilondieresis': [u'\u03cb',	 '.'],	 # Greek_upsilondieresis
'Greek_upsilonaccentdieresis': [u'\u03b0',	 '.'],	 # Greek_upsilonaccentdieresis
'Greek_omegaaccent': [u'\u03ce',	 '.'],	 # Greek_omegaaccent
'Greek_ALPHA': [u'\u0391',	 '.'],	 # Greek_ALPHA
'Greek_BETA': [u'\u0392',	 '.'],	 # Greek_BETA
'Greek_GAMMA': [u'\u0393',	 '.'],	 # Greek_GAMMA
'Greek_DELTA': [u'\u0394',	 '.'],	 # Greek_DELTA
'Greek_EPSILON': [u'\u0395',	 '.'],	 # Greek_EPSILON
'Greek_ZETA': [u'\u0396',	 '.'],	 # Greek_ZETA
'Greek_ETA': [u'\u0397',	 '.'],	 # Greek_ETA
'Greek_THETA': [u'\u0398',	 '.'],	 # Greek_THETA
'Greek_IOTA': [u'\u0399',	 '.'],	 # Greek_IOTA
'Greek_KAPPA': [u'\u039a',	 '.'],	 # Greek_KAPPA
'Greek_LAMBDA': [u'\u039b',	 '.'],	 # Greek_LAMBDA
'Greek_LAMDA': [u'\u039b',	 '.'],	 # Greek_LAMDA
'Greek_MU': [u'\u039c',	 '.'],	 # Greek_MU
'Greek_NU': [u'\u039d',	 '.'],	 # Greek_NU
'Greek_XI': [u'\u039e',	 '.'],	 # Greek_XI
'Greek_OMICRON': [u'\u039f',	 '.'],	 # Greek_OMICRON
'Greek_PI': [u'\u03a0',	 '.'],	 # Greek_PI
'Greek_RHO': [u'\u03a1',	 '.'],	 # Greek_RHO
'Greek_SIGMA': [u'\u03a3',	 '.'],	 # Greek_SIGMA
'Greek_TAU': [u'\u03a4',	 '.'],	 # Greek_TAU
'Greek_UPSILON': [u'\u03a5',	 '.'],	 # Greek_UPSILON
'Greek_PHI': [u'\u03a6',	 '.'],	 # Greek_PHI
'Greek_CHI': [u'\u03a7',	 '.'],	 # Greek_CHI
'Greek_PSI': [u'\u03a8',	 '.'],	 # Greek_PSI
'Greek_OMEGA': [u'\u03a9',	 '.'],	 # Greek_OMEGA
'Greek_alpha': [u'\u03b1',	 '.'],	 # Greek_alpha
'Greek_beta': [u'\u03b2',	 '.'],	 # Greek_beta
'Greek_gamma': [u'\u03b3',	 '.'],	 # Greek_gamma
'Greek_delta': [u'\u03b4',	 '.'],	 # Greek_delta
'Greek_epsilon': [u'\u03b5',	 '.'],	 # Greek_epsilon
'Greek_zeta': [u'\u03b6',	 '.'],	 # Greek_zeta
'Greek_eta': [u'\u03b7',	 '.'],	 # Greek_eta
'Greek_theta': [u'\u03b8',	 '.'],	 # Greek_theta
'Greek_iota': [u'\u03b9',	 '.'],	 # Greek_iota
'Greek_kappa': [u'\u03ba',	 '.'],	 # Greek_kappa
'Greek_lambda': [u'\u03bb',	 '.'],	 # Greek_lambda
'Greek_mu': [u'\u03bc',	 '.'],	 # Greek_mu
'Greek_nu': [u'\u03bd',	 '.'],	 # Greek_nu
'Greek_xi': [u'\u03be',	 '.'],	 # Greek_xi
'Greek_omicron': [u'\u03bf',	 '.'],	 # Greek_omicron
'Greek_pi': [u'\u03c0',	 '.'],	 # Greek_pi
'Greek_rho': [u'\u03c1',	 '.'],	 # Greek_rho
'Greek_sigma': [u'\u03c3',	 '.'],	 # Greek_sigma
'Greek_finalsmallsigma': [u'\u03c2',	 '.'],	 # Greek_finalsmallsigma
'Greek_tau': [u'\u03c4',	 '.'],	 # Greek_tau
'Greek_upsilon': [u'\u03c5',	 '.'],	 # Greek_upsilon
'Greek_phi': [u'\u03c6',	 '.'],	 # Greek_phi
'Greek_chi': [u'\u03c7',	 '.'],	 # Greek_chi
'Greek_psi': [u'\u03c8',	 '.'],	 # Greek_psi
'Greek_omega': [u'\u03c9',	 '.'],	 # Greek_omega
'leftradical': [u'\u23b7',	 '.'],	 # leftradical
'topleftradical': [u'\u250c',	 'd'],	 # topleftradical
'horizconnector': [u'\u2500',	 'd'],	 # horizconnector
'topintegral': [u'\u2320',	 '.'],	 # topintegral
'botintegral': [u'\u2321',	 '.'],	 # botintegral
'vertconnector': [u'\u2502',	 'd'],	 # vertconnector
'topleftsqbracket': [u'\u23a1',	 '.'],	 # topleftsqbracket
'botleftsqbracket': [u'\u23a3',	 '.'],	 # botleftsqbracket
'toprightsqbracket': [u'\u23a4',	 '.'],	 # toprightsqbracket
'botrightsqbracket': [u'\u23a6',	 '.'],	 # botrightsqbracket
'topleftparens': [u'\u239b',	 '.'],	 # topleftparens
'botleftparens': [u'\u239d',	 '.'],	 # botleftparens
'toprightparens': [u'\u239e',	 '.'],	 # toprightparens
'botrightparens': [u'\u23a0',	 '.'],	 # botrightparens
'leftmiddlecurlybrace': [u'\u23a8',	 '.'],	 # leftmiddlecurlybrace
'rightmiddlecurlybrace': [u'\u23ac',	 '.'],	 # rightmiddlecurlybrace
'topleftsummation': [None		 ,	 'o'],	 # topleftsummation
'botleftsummation': [None		 ,	 'o'],	 # botleftsummation
'topvertsummationconnector': [None		 ,	 'o'],	 # topvertsummationconnector
'botvertsummationconnector': [None		 ,	 'o'],	 # botvertsummationconnector
'toprightsummation': [None		 ,	 'o'],	 # toprightsummation
'botrightsummation': [None		 ,	 'o'],	 # botrightsummation
'rightmiddlesummation': [None		 ,	 'o'],	 # rightmiddlesummation
'lessthanequal': [u'\u2264',	 '.'],	 # lessthanequal
'notequal': [u'\u2260',	 '.'],	 # notequal
'greaterthanequal': [u'\u2265',	 '.'],	 # greaterthanequal
'integral': [u'\u222b',	 '.'],	 # integral
'therefore': [u'\u2234',	 '.'],	 # therefore
'variation': [u'\u221d',	 '.'],	 # variation
'infinity': [u'\u221e',	 '.'],	 # infinity
'nabla': [u'\u2207',	 '.'],	 # nabla
'approximate': [u'\u223c',	 '.'],	 # approximate
'similarequal': [u'\u2243',	 '.'],	 # similarequal
'ifonlyif': [u'\u21d4',	 '.'],	 # ifonlyif
'implies': [u'\u21d2',	 '.'],	 # implies
'identical': [u'\u2261',	 '.'],	 # identical
'radical': [u'\u221a',	 '.'],	 # radical
'includedin': [u'\u2282',	 '.'],	 # includedin
'includes': [u'\u2283',	 '.'],	 # includes
'intersection': [u'\u2229',	 '.'],	 # intersection
'union': [u'\u222a',	 '.'],	 # union
'logicaland': [u'\u2227',	 '.'],	 # logicaland
'logicalor': [u'\u2228',	 '.'],	 # logicalor
'partialderivative': [u'\u2202',	 '.'],	 # partialderivative
'function': [u'\u0192',	 '.'],	 # function
'leftarrow': [u'\u2190',	 '.'],	 # leftarrow
'uparrow': [u'\u2191',	 '.'],	 # uparrow
'rightarrow': [u'\u2192',	 '.'],	 # rightarrow
'downarrow': [u'\u2193',	 '.'],	 # downarrow
'blank': [None		 ,	 'o'],	 # blank
'soliddiamond': [u'\u25c6',	 '.'],	 # soliddiamond
'checkerboard': [u'\u2592',	 '.'],	 # checkerboard
'ht': [u'\u2409',	 '.'],	 # ht
'ff': [u'\u240c',	 '.'],	 # ff
'cr': [u'\u240d',	 '.'],	 # cr
'lf': [u'\u240a',	 '.'],	 # lf
'nl': [u'\u2424',	 '.'],	 # nl
'vt': [u'\u240b',	 '.'],	 # vt
'lowrightcorner': [u'\u2518',	 '.'],	 # lowrightcorner
'uprightcorner': [u'\u2510',	 '.'],	 # uprightcorner
'upleftcorner': [u'\u250c',	 '.'],	 # upleftcorner
'lowleftcorner': [u'\u2514',	 '.'],	 # lowleftcorner
'crossinglines': [u'\u253c',	 '.'],	 # crossinglines
'horizlinescan1': [u'\u23ba',	 '.'],	 # horizlinescan1
'horizlinescan3': [u'\u23bb',	 '.'],	 # horizlinescan3
'horizlinescan5': [u'\u2500',	 '.'],	 # horizlinescan5
'horizlinescan7': [u'\u23bc',	 '.'],	 # horizlinescan7
'horizlinescan9': [u'\u23bd',	 '.'],	 # horizlinescan9
'leftt': [u'\u251c',	 '.'],	 # leftt
'rightt': [u'\u2524',	 '.'],	 # rightt
'bott': [u'\u2534',	 '.'],	 # bott
'topt': [u'\u252c',	 '.'],	 # topt
'vertbar': [u'\u2502',	 '.'],	 # vertbar
'emspace': [u'\u2003',	 '.'],	 # emspace
'enspace': [u'\u2002',	 '.'],	 # enspace
'em3space': [u'\u2004',	 '.'],	 # em3space
'em4space': [u'\u2005',	 '.'],	 # em4space
'digitspace': [u'\u2007',	 '.'],	 # digitspace
'punctspace': [u'\u2008',	 '.'],	 # punctspace
'thinspace': [u'\u2009',	 '.'],	 # thinspace
'hairspace': [u'\u200a',	 '.'],	 # hairspace
'emdash': [u'\u2014',	 '.'],	 # emdash
'endash': [u'\u2013',	 '.'],	 # endash
'signifblank': [u'\u2423',	 'o'],	 # signifblank
'ellipsis': [u'\u2026',	 '.'],	 # ellipsis
'doubbaselinedot': [u'\u2025',	 '.'],	 # doubbaselinedot
'onethird': [u'\u2153',	 '.'],	 # onethird
'twothirds': [u'\u2154',	 '.'],	 # twothirds
'onefifth': [u'\u2155',	 '.'],	 # onefifth
'twofifths': [u'\u2156',	 '.'],	 # twofifths
'threefifths': [u'\u2157',	 '.'],	 # threefifths
'fourfifths': [u'\u2158',	 '.'],	 # fourfifths
'onesixth': [u'\u2159',	 '.'],	 # onesixth
'fivesixths': [u'\u215a',	 '.'],	 # fivesixths
'careof': [u'\u2105',	 '.'],	 # careof
'figdash': [u'\u2012',	 '.'],	 # figdash
'leftanglebracket': [u'\u27e8',	 'o'],	 # leftanglebracket
'decimalpoint': [u'\u002e',	 'o'],	 # decimalpoint
'rightanglebracket': [u'\u27e9',	 'o'],	 # rightanglebracket
'marker': [None		 ,	 'o'],	 # marker
'oneeighth': [u'\u215b',	 '.'],	 # oneeighth
'threeeighths': [u'\u215c',	 '.'],	 # threeeighths
'fiveeighths': [u'\u215d',	 '.'],	 # fiveeighths
'seveneighths': [u'\u215e',	 '.'],	 # seveneighths
'trademark': [u'\u2122',	 '.'],	 # trademark
'signaturemark': [u'\u2613',	 'o'],	 # signaturemark
'trademarkincircle': [None		 ,	 'o'],	 # trademarkincircle
'leftopentriangle': [u'\u25c1',	 'o'],	 # leftopentriangle
'rightopentriangle': [u'\u25b7',	 'o'],	 # rightopentriangle
'emopencircle': [u'\u25cb',	 'o'],	 # emopencircle
'emopenrectangle': [u'\u25af',	 'o'],	 # emopenrectangle
'leftsinglequotemark': [u'\u2018',	 '.'],	 # leftsinglequotemark
'rightsinglequotemark': [u'\u2019',	 '.'],	 # rightsinglequotemark
'leftdoublequotemark': [u'\u201c',	 '.'],	 # leftdoublequotemark
'rightdoublequotemark': [u'\u201d',	 '.'],	 # rightdoublequotemark
'prescription': [u'\u211e',	 '.'],	 # prescription
'minutes': [u'\u2032',	 '.'],	 # minutes
'seconds': [u'\u2033',	 '.'],	 # seconds
'latincross': [u'\u271d',	 '.'],	 # latincross
'hexagram': [None		 ,	 'o'],	 # hexagram
'filledrectbullet': [u'\u25ac',	 'o'],	 # filledrectbullet
'filledlefttribullet': [u'\u25c0',	 'o'],	 # filledlefttribullet
'filledrighttribullet': [u'\u25b6',	 'o'],	 # filledrighttribullet
'emfilledcircle': [u'\u25cf',	 'o'],	 # emfilledcircle
'emfilledrect': [u'\u25ae',	 'o'],	 # emfilledrect
'enopencircbullet': [u'\u25e6',	 'o'],	 # enopencircbullet
'enopensquarebullet': [u'\u25ab',	 'o'],	 # enopensquarebullet
'openrectbullet': [u'\u25ad',	 'o'],	 # openrectbullet
'opentribulletup': [u'\u25b3',	 'o'],	 # opentribulletup
'opentribulletdown': [u'\u25bd',	 'o'],	 # opentribulletdown
'openstar': [u'\u2606',	 'o'],	 # openstar
'enfilledcircbullet': [u'\u2022',	 'o'],	 # enfilledcircbullet
'enfilledsqbullet': [u'\u25aa',	 'o'],	 # enfilledsqbullet
'filledtribulletup': [u'\u25b2',	 'o'],	 # filledtribulletup
'filledtribulletdown': [u'\u25bc',	 'o'],	 # filledtribulletdown
'leftpointer': [u'\u261c',	 'o'],	 # leftpointer
'rightpointer': [u'\u261e',	 'o'],	 # rightpointer
'club': [u'\u2663',	 '.'],	 # club
'diamond': [u'\u2666',	 '.'],	 # diamond
'heart': [u'\u2665',	 '.'],	 # heart
'maltesecross': [u'\u2720',	 '.'],	 # maltesecross
'dagger': [u'\u2020',	 '.'],	 # dagger
'doubledagger': [u'\u2021',	 '.'],	 # doubledagger
'checkmark': [u'\u2713',	 '.'],	 # checkmark
'ballotcross': [u'\u2717',	 '.'],	 # ballotcross
'musicalsharp': [u'\u266f',	 '.'],	 # musicalsharp
'musicalflat': [u'\u266d',	 '.'],	 # musicalflat
'malesymbol': [u'\u2642',	 '.'],	 # malesymbol
'femalesymbol': [u'\u2640',	 '.'],	 # femalesymbol
'telephone': [u'\u260e',	 '.'],	 # telephone
'telephonerecorder': [u'\u2315',	 '.'],	 # telephonerecorder
'phonographcopyright': [u'\u2117',	 '.'],	 # phonographcopyright
'caret': [u'\u2038',	 '.'],	 # caret
'singlelowquotemark': [u'\u201a',	 '.'],	 # singlelowquotemark
'doublelowquotemark': [u'\u201e',	 '.'],	 # doublelowquotemark
'cursor': [None		 ,	 'o'],	 # cursor
'leftcaret': [u'\u003c',	 'd'],	 # leftcaret
'rightcaret': [u'\u003e',	 'd'],	 # rightcaret
'downcaret': [u'\u2228',	 'd'],	 # downcaret
'upcaret': [u'\u2227',	 'd'],	 # upcaret
'overbar': [u'\u00af',	 'd'],	 # overbar
'downtack': [u'\u22a5',	 '.'],	 # downtack
'upshoe': [u'\u2229',	 'd'],	 # upshoe
'downstile': [u'\u230a',	 '.'],	 # downstile
'underbar': [u'\u005f',	 'd'],	 # underbar
'jot': [u'\u2218',	 '.'],	 # jot
'quad': [u'\u2395',	 '.'],	 # quad
'uptack': [u'\u22a4',	 '.'],	 # uptack
'circle': [u'\u25cb',	 '.'],	 # circle
'upstile': [u'\u2308',	 '.'],	 # upstile
'downshoe': [u'\u222a',	 'd'],	 # downshoe
'rightshoe': [u'\u2283',	 'd'],	 # rightshoe
'leftshoe': [u'\u2282',	 'd'],	 # leftshoe
'lefttack': [u'\u22a2',	 '.'],	 # lefttack
'righttack': [u'\u22a3',	 '.'],	 # righttack
'hebrew_doublelowline': [u'\u2017',	 '.'],	 # hebrew_doublelowline
'hebrew_aleph': [u'\u05d0',	 '.'],	 # hebrew_aleph
'hebrew_bet': [u'\u05d1',	 '.'],	 # hebrew_bet
'hebrew_beth': [u'\u05d1',	 '.'],	 # hebrew_beth	/* deprecated */
'hebrew_gimel': [u'\u05d2',	 '.'],	 # hebrew_gimel
'hebrew_gimmel': [u'\u05d2',	 '.'],	 # hebrew_gimmel	/* deprecated */
'hebrew_dalet': [u'\u05d3',	 '.'],	 # hebrew_dalet
'hebrew_daleth': [u'\u05d3',	 '.'],	 # hebrew_daleth	/* deprecated */
'hebrew_he': [u'\u05d4',	 '.'],	 # hebrew_he
'hebrew_waw': [u'\u05d5',	 '.'],	 # hebrew_waw
'hebrew_zain': [u'\u05d6',	 '.'],	 # hebrew_zain
'hebrew_zayin': [u'\u05d6',	 '.'],	 # hebrew_zayin	/* deprecated */
'hebrew_chet': [u'\u05d7',	 '.'],	 # hebrew_chet
'hebrew_het': [u'\u05d7',	 '.'],	 # hebrew_het	/* deprecated */
'hebrew_tet': [u'\u05d8',	 '.'],	 # hebrew_tet
'hebrew_teth': [u'\u05d8',	 '.'],	 # hebrew_teth	/* deprecated */
'hebrew_yod': [u'\u05d9',	 '.'],	 # hebrew_yod
'hebrew_finalkaph': [u'\u05da',	 '.'],	 # hebrew_finalkaph
'hebrew_kaph': [u'\u05db',	 '.'],	 # hebrew_kaph
'hebrew_lamed': [u'\u05dc',	 '.'],	 # hebrew_lamed
'hebrew_finalmem': [u'\u05dd',	 '.'],	 # hebrew_finalmem
'hebrew_mem': [u'\u05de',	 '.'],	 # hebrew_mem
'hebrew_finalnun': [u'\u05df',	 '.'],	 # hebrew_finalnun
'hebrew_nun': [u'\u05e0',	 '.'],	 # hebrew_nun
'hebrew_samech': [u'\u05e1',	 '.'],	 # hebrew_samech
'hebrew_samekh': [u'\u05e1',	 '.'],	 # hebrew_samekh	/* deprecated */
'hebrew_ayin': [u'\u05e2',	 '.'],	 # hebrew_ayin
'hebrew_finalpe': [u'\u05e3',	 '.'],	 # hebrew_finalpe
'hebrew_pe': [u'\u05e4',	 '.'],	 # hebrew_pe
'hebrew_finalzade': [u'\u05e5',	 '.'],	 # hebrew_finalzade
'hebrew_finalzadi': [u'\u05e5',	 '.'],	 # hebrew_finalzadi	/* deprecated */
'hebrew_zade': [u'\u05e6',	 '.'],	 # hebrew_zade
'hebrew_zadi': [u'\u05e6',	 '.'],	 # hebrew_zadi	/* deprecated */
'hebrew_kuf': [u'\u05e7',	 '.'],	 # hebrew_kuf	/* deprecated */
'hebrew_qoph': [u'\u05e7',	 '.'],	 # hebrew_qoph
'hebrew_resh': [u'\u05e8',	 '.'],	 # hebrew_resh
'hebrew_shin': [u'\u05e9',	 '.'],	 # hebrew_shin
'hebrew_taf': [u'\u05ea',	 '.'],	 # hebrew_taf	/* deprecated */
'hebrew_taw': [u'\u05ea',	 '.'],	 # hebrew_taw
'Thai_kokai': [u'\u0e01',	 '.'],	 # Thai_kokai
'Thai_khokhai': [u'\u0e02',	 '.'],	 # Thai_khokhai
'Thai_khokhuat': [u'\u0e03',	 '.'],	 # Thai_khokhuat
'Thai_khokhwai': [u'\u0e04',	 '.'],	 # Thai_khokhwai
'Thai_khokhon': [u'\u0e05',	 '.'],	 # Thai_khokhon
'Thai_khorakhang': [u'\u0e06',	 '.'],	 # Thai_khorakhang
'Thai_ngongu': [u'\u0e07',	 '.'],	 # Thai_ngongu
'Thai_chochan': [u'\u0e08',	 '.'],	 # Thai_chochan
'Thai_choching': [u'\u0e09',	 '.'],	 # Thai_choching
'Thai_chochang': [u'\u0e0a',	 '.'],	 # Thai_chochang
'Thai_soso': [u'\u0e0b',	 '.'],	 # Thai_soso
'Thai_chochoe': [u'\u0e0c',	 '.'],	 # Thai_chochoe
'Thai_yoying': [u'\u0e0d',	 '.'],	 # Thai_yoying
'Thai_dochada': [u'\u0e0e',	 '.'],	 # Thai_dochada
'Thai_topatak': [u'\u0e0f',	 '.'],	 # Thai_topatak
'Thai_thothan': [u'\u0e10',	 '.'],	 # Thai_thothan
'Thai_thonangmontho': [u'\u0e11',	 '.'],	 # Thai_thonangmontho
'Thai_thophuthao': [u'\u0e12',	 '.'],	 # Thai_thophuthao
'Thai_nonen': [u'\u0e13',	 '.'],	 # Thai_nonen
'Thai_dodek': [u'\u0e14',	 '.'],	 # Thai_dodek
'Thai_totao': [u'\u0e15',	 '.'],	 # Thai_totao
'Thai_thothung': [u'\u0e16',	 '.'],	 # Thai_thothung
'Thai_thothahan': [u'\u0e17',	 '.'],	 # Thai_thothahan
'Thai_thothong': [u'\u0e18',	 '.'],	 # Thai_thothong
'Thai_nonu': [u'\u0e19',	 '.'],	 # Thai_nonu
'Thai_bobaimai': [u'\u0e1a',	 '.'],	 # Thai_bobaimai
'Thai_popla': [u'\u0e1b',	 '.'],	 # Thai_popla
'Thai_phophung': [u'\u0e1c',	 '.'],	 # Thai_phophung
'Thai_fofa': [u'\u0e1d',	 '.'],	 # Thai_fofa
'Thai_phophan': [u'\u0e1e',	 '.'],	 # Thai_phophan
'Thai_fofan': [u'\u0e1f',	 '.'],	 # Thai_fofan
'Thai_phosamphao': [u'\u0e20',	 '.'],	 # Thai_phosamphao
'Thai_moma': [u'\u0e21',	 '.'],	 # Thai_moma
'Thai_yoyak': [u'\u0e22',	 '.'],	 # Thai_yoyak
'Thai_rorua': [u'\u0e23',	 '.'],	 # Thai_rorua
'Thai_ru': [u'\u0e24',	 '.'],	 # Thai_ru
'Thai_loling': [u'\u0e25',	 '.'],	 # Thai_loling
'Thai_lu': [u'\u0e26',	 '.'],	 # Thai_lu
'Thai_wowaen': [u'\u0e27',	 '.'],	 # Thai_wowaen
'Thai_sosala': [u'\u0e28',	 '.'],	 # Thai_sosala
'Thai_sorusi': [u'\u0e29',	 '.'],	 # Thai_sorusi
'Thai_sosua': [u'\u0e2a',	 '.'],	 # Thai_sosua
'Thai_hohip': [u'\u0e2b',	 '.'],	 # Thai_hohip
'Thai_lochula': [u'\u0e2c',	 '.'],	 # Thai_lochula
'Thai_oang': [u'\u0e2d',	 '.'],	 # Thai_oang
'Thai_honokhuk': [u'\u0e2e',	 '.'],	 # Thai_honokhuk
'Thai_paiyannoi': [u'\u0e2f',	 '.'],	 # Thai_paiyannoi
'Thai_saraa': [u'\u0e30',	 '.'],	 # Thai_saraa
'Thai_maihanakat': [u'\u0e31',	 '.'],	 # Thai_maihanakat
'Thai_saraaa': [u'\u0e32',	 '.'],	 # Thai_saraaa
'Thai_saraam': [u'\u0e33',	 '.'],	 # Thai_saraam
'Thai_sarai': [u'\u0e34',	 '.'],	 # Thai_sarai
'Thai_saraii': [u'\u0e35',	 '.'],	 # Thai_saraii
'Thai_saraue': [u'\u0e36',	 '.'],	 # Thai_saraue
'Thai_sarauee': [u'\u0e37',	 '.'],	 # Thai_sarauee
'Thai_sarau': [u'\u0e38',	 '.'],	 # Thai_sarau
'Thai_sarauu': [u'\u0e39',	 '.'],	 # Thai_sarauu
'Thai_phinthu': [u'\u0e3a',	 '.'],	 # Thai_phinthu
'Thai_maihanakat_maitho': [None		 ,	 'o'],	 # Thai_maihanakat_maitho
'Thai_baht': [u'\u0e3f',	 '.'],	 # Thai_baht
'Thai_sarae': [u'\u0e40',	 '.'],	 # Thai_sarae
'Thai_saraae': [u'\u0e41',	 '.'],	 # Thai_saraae
'Thai_sarao': [u'\u0e42',	 '.'],	 # Thai_sarao
'Thai_saraaimaimuan': [u'\u0e43',	 '.'],	 # Thai_saraaimaimuan
'Thai_saraaimaimalai': [u'\u0e44',	 '.'],	 # Thai_saraaimaimalai
'Thai_lakkhangyao': [u'\u0e45',	 '.'],	 # Thai_lakkhangyao
'Thai_maiyamok': [u'\u0e46',	 '.'],	 # Thai_maiyamok
'Thai_maitaikhu': [u'\u0e47',	 '.'],	 # Thai_maitaikhu
'Thai_maiek': [u'\u0e48',	 '.'],	 # Thai_maiek
'Thai_maitho': [u'\u0e49',	 '.'],	 # Thai_maitho
'Thai_maitri': [u'\u0e4a',	 '.'],	 # Thai_maitri
'Thai_maichattawa': [u'\u0e4b',	 '.'],	 # Thai_maichattawa
'Thai_thanthakhat': [u'\u0e4c',	 '.'],	 # Thai_thanthakhat
'Thai_nikhahit': [u'\u0e4d',	 '.'],	 # Thai_nikhahit
'Thai_leksun': [u'\u0e50',	 '.'],	 # Thai_leksun
'Thai_leknung': [u'\u0e51',	 '.'],	 # Thai_leknung
'Thai_leksong': [u'\u0e52',	 '.'],	 # Thai_leksong
'Thai_leksam': [u'\u0e53',	 '.'],	 # Thai_leksam
'Thai_leksi': [u'\u0e54',	 '.'],	 # Thai_leksi
'Thai_lekha': [u'\u0e55',	 '.'],	 # Thai_lekha
'Thai_lekhok': [u'\u0e56',	 '.'],	 # Thai_lekhok
'Thai_lekchet': [u'\u0e57',	 '.'],	 # Thai_lekchet
'Thai_lekpaet': [u'\u0e58',	 '.'],	 # Thai_lekpaet
'Thai_lekkao': [u'\u0e59',	 '.'],	 # Thai_lekkao
'Hangul_Kiyeog': [u'\u3131',	 'f'],	 # Hangul_Kiyeog
'Hangul_SsangKiyeog': [u'\u3132',	 'f'],	 # Hangul_SsangKiyeog
'Hangul_KiyeogSios': [u'\u3133',	 'f'],	 # Hangul_KiyeogSios
'Hangul_Nieun': [u'\u3134',	 'f'],	 # Hangul_Nieun
'Hangul_NieunJieuj': [u'\u3135',	 'f'],	 # Hangul_NieunJieuj
'Hangul_NieunHieuh': [u'\u3136',	 'f'],	 # Hangul_NieunHieuh
'Hangul_Dikeud': [u'\u3137',	 'f'],	 # Hangul_Dikeud
'Hangul_SsangDikeud': [u'\u3138',	 'f'],	 # Hangul_SsangDikeud
'Hangul_Rieul': [u'\u3139',	 'f'],	 # Hangul_Rieul
'Hangul_RieulKiyeog': [u'\u313a',	 'f'],	 # Hangul_RieulKiyeog
'Hangul_RieulMieum': [u'\u313b',	 'f'],	 # Hangul_RieulMieum
'Hangul_RieulPieub': [u'\u313c',	 'f'],	 # Hangul_RieulPieub
'Hangul_RieulSios': [u'\u313d',	 'f'],	 # Hangul_RieulSios
'Hangul_RieulTieut': [u'\u313e',	 'f'],	 # Hangul_RieulTieut
'Hangul_RieulPhieuf': [u'\u313f',	 'f'],	 # Hangul_RieulPhieuf
'Hangul_RieulHieuh': [u'\u3140',	 'f'],	 # Hangul_RieulHieuh
'Hangul_Mieum': [u'\u3141',	 'f'],	 # Hangul_Mieum
'Hangul_Pieub': [u'\u3142',	 'f'],	 # Hangul_Pieub
'Hangul_SsangPieub': [u'\u3143',	 'f'],	 # Hangul_SsangPieub
'Hangul_PieubSios': [u'\u3144',	 'f'],	 # Hangul_PieubSios
'Hangul_Sios': [u'\u3145',	 'f'],	 # Hangul_Sios
'Hangul_SsangSios': [u'\u3146',	 'f'],	 # Hangul_SsangSios
'Hangul_Ieung': [u'\u3147',	 'f'],	 # Hangul_Ieung
'Hangul_Jieuj': [u'\u3148',	 'f'],	 # Hangul_Jieuj
'Hangul_SsangJieuj': [u'\u3149',	 'f'],	 # Hangul_SsangJieuj
'Hangul_Cieuc': [u'\u314a',	 'f'],	 # Hangul_Cieuc
'Hangul_Khieuq': [u'\u314b',	 'f'],	 # Hangul_Khieuq
'Hangul_Tieut': [u'\u314c',	 'f'],	 # Hangul_Tieut
'Hangul_Phieuf': [u'\u314d',	 'f'],	 # Hangul_Phieuf
'Hangul_Hieuh': [u'\u314e',	 'f'],	 # Hangul_Hieuh
'Hangul_A': [u'\u314f',	 'f'],	 # Hangul_A
'Hangul_AE': [u'\u3150',	 'f'],	 # Hangul_AE
'Hangul_YA': [u'\u3151',	 'f'],	 # Hangul_YA
'Hangul_YAE': [u'\u3152',	 'f'],	 # Hangul_YAE
'Hangul_EO': [u'\u3153',	 'f'],	 # Hangul_EO
'Hangul_E': [u'\u3154',	 'f'],	 # Hangul_E
'Hangul_YEO': [u'\u3155',	 'f'],	 # Hangul_YEO
'Hangul_YE': [u'\u3156',	 'f'],	 # Hangul_YE
'Hangul_O': [u'\u3157',	 'f'],	 # Hangul_O
'Hangul_WA': [u'\u3158',	 'f'],	 # Hangul_WA
'Hangul_WAE': [u'\u3159',	 'f'],	 # Hangul_WAE
'Hangul_OE': [u'\u315a',	 'f'],	 # Hangul_OE
'Hangul_YO': [u'\u315b',	 'f'],	 # Hangul_YO
'Hangul_U': [u'\u315c',	 'f'],	 # Hangul_U
'Hangul_WEO': [u'\u315d',	 'f'],	 # Hangul_WEO
'Hangul_WE': [u'\u315e',	 'f'],	 # Hangul_WE
'Hangul_WI': [u'\u315f',	 'f'],	 # Hangul_WI
'Hangul_YU': [u'\u3160',	 'f'],	 # Hangul_YU
'Hangul_EU': [u'\u3161',	 'f'],	 # Hangul_EU
'Hangul_YI': [u'\u3162',	 'f'],	 # Hangul_YI
'Hangul_I': [u'\u3163',	 'f'],	 # Hangul_I
'Hangul_J_Kiyeog': [u'\u11a8',	 'f'],	 # Hangul_J_Kiyeog
'Hangul_J_SsangKiyeog': [u'\u11a9',	 'f'],	 # Hangul_J_SsangKiyeog
'Hangul_J_KiyeogSios': [u'\u11aa',	 'f'],	 # Hangul_J_KiyeogSios
'Hangul_J_Nieun': [u'\u11ab',	 'f'],	 # Hangul_J_Nieun
'Hangul_J_NieunJieuj': [u'\u11ac',	 'f'],	 # Hangul_J_NieunJieuj
'Hangul_J_NieunHieuh': [u'\u11ad',	 'f'],	 # Hangul_J_NieunHieuh
'Hangul_J_Dikeud': [u'\u11ae',	 'f'],	 # Hangul_J_Dikeud
'Hangul_J_Rieul': [u'\u11af',	 'f'],	 # Hangul_J_Rieul
'Hangul_J_RieulKiyeog': [u'\u11b0',	 'f'],	 # Hangul_J_RieulKiyeog
'Hangul_J_RieulMieum': [u'\u11b1',	 'f'],	 # Hangul_J_RieulMieum
'Hangul_J_RieulPieub': [u'\u11b2',	 'f'],	 # Hangul_J_RieulPieub
'Hangul_J_RieulSios': [u'\u11b3',	 'f'],	 # Hangul_J_RieulSios
'Hangul_J_RieulTieut': [u'\u11b4',	 'f'],	 # Hangul_J_RieulTieut
'Hangul_J_RieulPhieuf': [u'\u11b5',	 'f'],	 # Hangul_J_RieulPhieuf
'Hangul_J_RieulHieuh': [u'\u11b6',	 'f'],	 # Hangul_J_RieulHieuh
'Hangul_J_Mieum': [u'\u11b7',	 'f'],	 # Hangul_J_Mieum
'Hangul_J_Pieub': [u'\u11b8',	 'f'],	 # Hangul_J_Pieub
'Hangul_J_PieubSios': [u'\u11b9',	 'f'],	 # Hangul_J_PieubSios
'Hangul_J_Sios': [u'\u11ba',	 'f'],	 # Hangul_J_Sios
'Hangul_J_SsangSios': [u'\u11bb',	 'f'],	 # Hangul_J_SsangSios
'Hangul_J_Ieung': [u'\u11bc',	 'f'],	 # Hangul_J_Ieung
'Hangul_J_Jieuj': [u'\u11bd',	 'f'],	 # Hangul_J_Jieuj
'Hangul_J_Cieuc': [u'\u11be',	 'f'],	 # Hangul_J_Cieuc
'Hangul_J_Khieuq': [u'\u11bf',	 'f'],	 # Hangul_J_Khieuq
'Hangul_J_Tieut': [u'\u11c0',	 'f'],	 # Hangul_J_Tieut
'Hangul_J_Phieuf': [u'\u11c1',	 'f'],	 # Hangul_J_Phieuf
'Hangul_J_Hieuh': [u'\u11c2',	 'f'],	 # Hangul_J_Hieuh
'Hangul_RieulYeorinHieuh': [u'\u316d',	 'f'],	 # Hangul_RieulYeorinHieuh
'Hangul_SunkyeongeumMieum': [u'\u3171',	 'f'],	 # Hangul_SunkyeongeumMieum
'Hangul_SunkyeongeumPieub': [u'\u3178',	 'f'],	 # Hangul_SunkyeongeumPieub
'Hangul_PanSios': [u'\u317f',	 'f'],	 # Hangul_PanSios
'Hangul_KkogjiDalrinIeung': [u'\u3181',	 'f'],	 # Hangul_KkogjiDalrinIeung
'Hangul_SunkyeongeumPhieuf': [u'\u3184',	 'f'],	 # Hangul_SunkyeongeumPhieuf
'Hangul_YeorinHieuh': [u'\u3186',	 'f'],	 # Hangul_YeorinHieuh
'Hangul_AraeA': [u'\u318d',	 'f'],	 # Hangul_AraeA
'Hangul_AraeAE': [u'\u318e',	 'f'],	 # Hangul_AraeAE
'Hangul_J_PanSios': [u'\u11eb',	 'f'],	 # Hangul_J_PanSios
'Hangul_J_KkogjiDalrinIeung': [u'\u11f0',	 'f'],	 # Hangul_J_KkogjiDalrinIeung
'Hangul_J_YeorinHieuh': [u'\u11f9',	 'f'],	 # Hangul_J_YeorinHieuh
'Korean_Won': [u'\u20a9',	 'o'],	 # Korean_Won
'OE': [u'\u0152',	 '.'],	 # OE
'oe': [u'\u0153',	 '.'],	 # oe
'Ydiaeresis': [u'\u0178',	 '.'],	 # Ydiaeresis
'EcuSign': [u'\u20a0',	 'u'],	 # EcuSign
'ColonSign': [u'\u20a1',	 'u'],	 # ColonSign
'CruzeiroSign': [u'\u20a2',	 'u'],	 # CruzeiroSign
'FFrancSign': [u'\u20a3',	 'u'],	 # FFrancSign
'LiraSign': [u'\u20a4',	 'u'],	 # LiraSign
'MillSign': [u'\u20a5',	 'u'],	 # MillSign
'NairaSign': [u'\u20a6',	 'u'],	 # NairaSign
'PesetaSign': [u'\u20a7',	 'u'],	 # PesetaSign
'RupeeSign': [u'\u20a8',	 'u'],	 # RupeeSign
'WonSign': [u'\u20a9',	 'u'],	 # WonSign
'NewSheqelSign': [u'\u20aa',	 'u'],	 # NewSheqelSign
'DongSign': [u'\u20ab',	 'u'],	 # DongSign
'EuroSign': [u'\u20ac',	 '.'],	 # EuroSign
'3270_Duplicate': [None		 ,	 'f'],	 # 3270_Duplicate
'3270_FieldMark': [None		 ,	 'f'],	 # 3270_FieldMark
'3270_Right2': [None		 ,	 'f'],	 # 3270_Right2
'3270_Left2': [None		 ,	 'f'],	 # 3270_Left2
'3270_BackTab': [None		 ,	 'f'],	 # 3270_BackTab
'3270_EraseEOF': [None		 ,	 'f'],	 # 3270_EraseEOF
'3270_EraseInput': [None		 ,	 'f'],	 # 3270_EraseInput
'3270_Reset': [None		 ,	 'f'],	 # 3270_Reset
'3270_Quit': [None		 ,	 'f'],	 # 3270_Quit
'3270_PA1': [None		 ,	 'f'],	 # 3270_PA1
'3270_PA2': [None		 ,	 'f'],	 # 3270_PA2
'3270_PA3': [None		 ,	 'f'],	 # 3270_PA3
'3270_Test': [None		 ,	 'f'],	 # 3270_Test
'3270_Attn': [None		 ,	 'f'],	 # 3270_Attn
'3270_CursorBlink': [None		 ,	 'f'],	 # 3270_CursorBlink
'3270_AltCursor': [None		 ,	 'f'],	 # 3270_AltCursor
'3270_KeyClick': [None		 ,	 'f'],	 # 3270_KeyClick
'3270_Jump': [None		 ,	 'f'],	 # 3270_Jump
'3270_Ident': [None		 ,	 'f'],	 # 3270_Ident
'3270_Rule': [None		 ,	 'f'],	 # 3270_Rule
'3270_Copy': [None		 ,	 'f'],	 # 3270_Copy
'3270_Play': [None		 ,	 'f'],	 # 3270_Play
'3270_Setup': [None		 ,	 'f'],	 # 3270_Setup
'3270_Record': [None		 ,	 'f'],	 # 3270_Record
'3270_ChangeScreen': [None		 ,	 'f'],	 # 3270_ChangeScreen
'3270_DeleteWord': [None		 ,	 'f'],	 # 3270_DeleteWord
'3270_ExSelect': [None		 ,	 'f'],	 # 3270_ExSelect
'3270_CursorSelect': [None		 ,	 'f'],	 # 3270_CursorSelect
'3270_PrintScreen': [None		 ,	 'f'],	 # 3270_PrintScreen
'3270_Enter': [None		 ,	 'f'],	 # 3270_Enter
'ISO_Lock': [None		 ,	 'f'],	 # ISO_Lock
'ISO_Level2_Latch': [None		 ,	 'f'],	 # ISO_Level2_Latch
'ISO_Level3_Shift': [None		 ,	 'f'],	 # ISO_Level3_Shift
'ISO_Level3_Latch': [None		 ,	 'f'],	 # ISO_Level3_Latch
'ISO_Level3_Lock': [None		 ,	 'f'],	 # ISO_Level3_Lock
'ISO_Group_Latch': [None		 ,	 'f'],	 # ISO_Group_Latch
'ISO_Group_Lock': [None		 ,	 'f'],	 # ISO_Group_Lock
'ISO_Next_Group': [None		 ,	 'f'],	 # ISO_Next_Group
'ISO_Next_Group_Lock': [None		 ,	 'f'],	 # ISO_Next_Group_Lock
'ISO_Prev_Group': [None		 ,	 'f'],	 # ISO_Prev_Group
'ISO_Prev_Group_Lock': [None		 ,	 'f'],	 # ISO_Prev_Group_Lock
'ISO_First_Group': [None		 ,	 'f'],	 # ISO_First_Group
'ISO_First_Group_Lock': [None		 ,	 'f'],	 # ISO_First_Group_Lock
'ISO_Last_Group': [None		 ,	 'f'],	 # ISO_Last_Group
'ISO_Last_Group_Lock': [None		 ,	 'f'],	 # ISO_Last_Group_Lock
'ISO_Left_Tab': [None		 ,	 'f'],	 # ISO_Left_Tab
'ISO_Move_Line_Up': [None		 ,	 'f'],	 # ISO_Move_Line_Up
'ISO_Move_Line_Down': [None		 ,	 'f'],	 # ISO_Move_Line_Down
'ISO_Partial_Line_Up': [None		 ,	 'f'],	 # ISO_Partial_Line_Up
'ISO_Partial_Line_Down': [None		 ,	 'f'],	 # ISO_Partial_Line_Down
'ISO_Partial_Space_Left': [None		 ,	 'f'],	 # ISO_Partial_Space_Left
'ISO_Partial_Space_Right': [None		 ,	 'f'],	 # ISO_Partial_Space_Right
'ISO_Set_Margin_Left': [None		 ,	 'f'],	 # ISO_Set_Margin_Left
'ISO_Set_Margin_Right': [None		 ,	 'f'],	 # ISO_Set_Margin_Right
'ISO_Release_Margin_Left': [None		 ,	 'f'],	 # ISO_Release_Margin_Left
'ISO_Release_Margin_Right': [None		 ,	 'f'],	 # ISO_Release_Margin_Right
'ISO_Release_Both_Margins': [None		 ,	 'f'],	 # ISO_Release_Both_Margins
'ISO_Fast_Cursor_Left': [None		 ,	 'f'],	 # ISO_Fast_Cursor_Left
'ISO_Fast_Cursor_Right': [None		 ,	 'f'],	 # ISO_Fast_Cursor_Right
'ISO_Fast_Cursor_Up': [None		 ,	 'f'],	 # ISO_Fast_Cursor_Up
'ISO_Fast_Cursor_Down': [None		 ,	 'f'],	 # ISO_Fast_Cursor_Down
'ISO_Continuous_Underline': [None		 ,	 'f'],	 # ISO_Continuous_Underline
'ISO_Discontinuous_Underline': [None		 ,	 'f'],	 # ISO_Discontinuous_Underline
'ISO_Emphasize': [None		 ,	 'f'],	 # ISO_Emphasize
'ISO_Center_Object': [None		 ,	 'f'],	 # ISO_Center_Object
'ISO_Enter': [None		 ,	 'f'],	 # ISO_Enter
'dead_grave': [u'\u0300',	 'f'],	 # dead_grave
'dead_acute': [u'\u0301',	 'f'],	 # dead_acute
'dead_circumflex': [u'\u0302',	 'f'],	 # dead_circumflex
'dead_tilde': [u'\u0303',	 'f'],	 # dead_tilde
'dead_macron': [u'\u0304',	 'f'],	 # dead_macron
'dead_breve': [u'\u0306',	 'f'],	 # dead_breve
'dead_abovedot': [u'\u0307',	 'f'],	 # dead_abovedot
'dead_diaeresis': [u'\u0308',	 'f'],	 # dead_diaeresis
'dead_abovering': [u'\u030a',	 'f'],	 # dead_abovering
'dead_doubleacute': [u'\u030b',	 'f'],	 # dead_doubleacute
'dead_caron': [u'\u030c',	 'f'],	 # dead_caron
'dead_cedilla': [u'\u0327',	 'f'],	 # dead_cedilla
'dead_ogonek': [u'\u0328',	 'f'],	 # dead_ogonek
'dead_iota': [u'\u0345',	 'f'],	 # dead_iota
'dead_voiced_sound': [u'\u3099',	 'f'],	 # dead_voiced_sound
'dead_semivoiced_sound': [u'\u309a',	 'f'],	 # dead_semivoiced_sound
'AccessX_Enable': [None		 ,	 'f'],	 # AccessX_Enable
'AccessX_Feedback_Enable': [None		 ,	 'f'],	 # AccessX_Feedback_Enable
'RepeatKeys_Enable': [None		 ,	 'f'],	 # RepeatKeys_Enable
'SlowKeys_Enable': [None		 ,	 'f'],	 # SlowKeys_Enable
'BounceKeys_Enable': [None		 ,	 'f'],	 # BounceKeys_Enable
'StickyKeys_Enable': [None		 ,	 'f'],	 # StickyKeys_Enable
'MouseKeys_Enable': [None		 ,	 'f'],	 # MouseKeys_Enable
'MouseKeys_Accel_Enable': [None		 ,	 'f'],	 # MouseKeys_Accel_Enable
'Overlay1_Enable': [None		 ,	 'f'],	 # Overlay1_Enable
'Overlay2_Enable': [None		 ,	 'f'],	 # Overlay2_Enable
'AudibleBell_Enable': [None		 ,	 'f'],	 # AudibleBell_Enable
'First_Virtual_Screen': [None		 ,	 'f'],	 # First_Virtual_Screen
'Prev_Virtual_Screen': [None		 ,	 'f'],	 # Prev_Virtual_Screen
'Next_Virtual_Screen': [None		 ,	 'f'],	 # Next_Virtual_Screen
'Last_Virtual_Screen': [None		 ,	 'f'],	 # Last_Virtual_Screen
'Terminate_Server': [None		 ,	 'f'],	 # Terminate_Server
'Pointer_Left': [None		 ,	 'f'],	 # Pointer_Left
'Pointer_Right': [None		 ,	 'f'],	 # Pointer_Right
'Pointer_Up': [None		 ,	 'f'],	 # Pointer_Up
'Pointer_Down': [None		 ,	 'f'],	 # Pointer_Down
'Pointer_UpLeft': [None		 ,	 'f'],	 # Pointer_UpLeft
'Pointer_UpRight': [None		 ,	 'f'],	 # Pointer_UpRight
'Pointer_DownLeft': [None		 ,	 'f'],	 # Pointer_DownLeft
'Pointer_DownRight': [None		 ,	 'f'],	 # Pointer_DownRight
'Pointer_Button_Dflt': [None		 ,	 'f'],	 # Pointer_Button_Dflt
'Pointer_Button1': [None		 ,	 'f'],	 # Pointer_Button1
'Pointer_Button2': [None		 ,	 'f'],	 # Pointer_Button2
'Pointer_Button3': [None		 ,	 'f'],	 # Pointer_Button3
'Pointer_Button4': [None		 ,	 'f'],	 # Pointer_Button4
'Pointer_Button5': [None		 ,	 'f'],	 # Pointer_Button5
'Pointer_DblClick_Dflt': [None		 ,	 'f'],	 # Pointer_DblClick_Dflt
'Pointer_DblClick1': [None		 ,	 'f'],	 # Pointer_DblClick1
'Pointer_DblClick2': [None		 ,	 'f'],	 # Pointer_DblClick2
'Pointer_DblClick3': [None		 ,	 'f'],	 # Pointer_DblClick3
'Pointer_DblClick4': [None		 ,	 'f'],	 # Pointer_DblClick4
'Pointer_DblClick5': [None		 ,	 'f'],	 # Pointer_DblClick5
'Pointer_Drag_Dflt': [None		 ,	 'f'],	 # Pointer_Drag_Dflt
'Pointer_Drag1': [None		 ,	 'f'],	 # Pointer_Drag1
'Pointer_Drag2': [None		 ,	 'f'],	 # Pointer_Drag2
'Pointer_Drag3': [None		 ,	 'f'],	 # Pointer_Drag3
'Pointer_Drag4': [None		 ,	 'f'],	 # Pointer_Drag4
'Pointer_EnableKeys': [None		 ,	 'f'],	 # Pointer_EnableKeys
'Pointer_Accelerate': [None		 ,	 'f'],	 # Pointer_Accelerate
'Pointer_DfltBtnNext': [None		 ,	 'f'],	 # Pointer_DfltBtnNext
'Pointer_DfltBtnPrev': [None		 ,	 'f'],	 # Pointer_DfltBtnPrev
'Pointer_Drag5': [None		 ,	 'f'],	 # Pointer_Drag5
'BackSpace': [u'\u0008',	 'f'],	 # BackSpace	/* back space, back char */
'Tab': [u'\u0009',	 'f'],	 # Tab
'Linefeed': [u'\u000a',	 'f'],	 # Linefeed	/* Linefeed, LF */
'Clear': [u'\u000b',	 'f'],	 # Clear
'Return': [u'\u000d',	 'f'],	 # Return	/* Return, enter */
'Pause': [u'\u0013',	 'f'],	 # Pause	/* Pause, hold */
'Scroll_Lock': [u'\u0014',	 'f'],	 # Scroll_Lock
'Sys_Req': [u'\u0015',	 'f'],	 # Sys_Req
'Escape': [u'\u001b',	 'f'],	 # Escape
'Multi_key': [None		 ,	 'f'],	 # Multi_key
'Kanji': [None		 ,	 'f'],	 # Kanji
'Muhenkan': [None		 ,	 'f'],	 # Muhenkan
'Henkan_Mode': [None		 ,	 'f'],	 # Henkan_Mode
'Romaji': [None		 ,	 'f'],	 # Romaji
'Hiragana': [None		 ,	 'f'],	 # Hiragana
'Katakana': [None		 ,	 'f'],	 # Katakana
'Hiragana_Katakana': [None		 ,	 'f'],	 # Hiragana_Katakana
'Zenkaku': [None		 ,	 'f'],	 # Zenkaku
'Hankaku': [None		 ,	 'f'],	 # Hankaku
'Zenkaku_Hankaku': [None		 ,	 'f'],	 # Zenkaku_Hankaku
'Touroku': [None		 ,	 'f'],	 # Touroku
'Massyo': [None		 ,	 'f'],	 # Massyo
'Kana_Lock': [None		 ,	 'f'],	 # Kana_Lock
'Kana_Shift': [None		 ,	 'f'],	 # Kana_Shift
'Eisu_Shift': [None		 ,	 'f'],	 # Eisu_Shift
'Eisu_toggle': [None		 ,	 'f'],	 # Eisu_toggle
'Hangul': [None		 ,	 'f'],	 # Hangul
'Hangul_Start': [None		 ,	 'f'],	 # Hangul_Start
'Hangul_End': [None		 ,	 'f'],	 # Hangul_End
'Hangul_Hanja': [None		 ,	 'f'],	 # Hangul_Hanja
'Hangul_Jamo': [None		 ,	 'f'],	 # Hangul_Jamo
'Hangul_Romaja': [None		 ,	 'f'],	 # Hangul_Romaja
'Codeinput': [None		 ,	 'f'],	 # Codeinput
'Hangul_Jeonja': [None		 ,	 'f'],	 # Hangul_Jeonja
'Hangul_Banja': [None		 ,	 'f'],	 # Hangul_Banja
'Hangul_PreHanja': [None		 ,	 'f'],	 # Hangul_PreHanja
'Hangul_PostHanja': [None		 ,	 'f'],	 # Hangul_PostHanja
'SingleCandidate': [None		 ,	 'f'],	 # SingleCandidate
'MultipleCandidate': [None		 ,	 'f'],	 # MultipleCandidate
'PreviousCandidate': [None		 ,	 'f'],	 # PreviousCandidate
'Hangul_Special': [None		 ,	 'f'],	 # Hangul_Special
'Home': [None		 ,	 'f'],	 # Home
'Left': [None		 ,	 'f'],	 # Left
'Up': [None		 ,	 'f'],	 # Up
'Right': [None		 ,	 'f'],	 # Right
'Down': [None		 ,	 'f'],	 # Down
'Prior': [None		 ,	 'f'],	 # Prior
'Next': [None		 ,	 'f'],	 # Next
'End': [None		 ,	 'f'],	 # End
'Begin': [None		 ,	 'f'],	 # Begin
'Select': [None		 ,	 'f'],	 # Select
'Print': [None		 ,	 'f'],	 # Print
'Execute': [None		 ,	 'f'],	 # Execute
'Insert': [None		 ,	 'f'],	 # Insert
'Undo': [None		 ,	 'f'],	 # Undo
'Redo': [None		 ,	 'f'],	 # Redo
'Menu': [None		 ,	 'f'],	 # Menu
'Find': [None		 ,	 'f'],	 # Find
'Cancel': [None		 ,	 'f'],	 # Cancel
'Help': [None		 ,	 'f'],	 # Help
'Break': [None		 ,	 'f'],	 # Break
'Mode_switch': [None		 ,	 'f'],	 # Mode_switch
'Num_Lock': [None		 ,	 'f'],	 # Num_Lock
'KP_Space': [u'\u0020',	 'f'],	 # KP_Space	/* space */
'KP_Tab': [u'\u0009',	 'f'],	 # KP_Tab
'KP_Enter': [u'\u000d',	 'f'],	 # KP_Enter	/* enter */
'KP_F1': [None		 ,	 'f'],	 # KP_F1
'KP_F2': [None		 ,	 'f'],	 # KP_F2
'KP_F3': [None		 ,	 'f'],	 # KP_F3
'KP_F4': [None		 ,	 'f'],	 # KP_F4
'KP_Home': [None		 ,	 'f'],	 # KP_Home
'KP_Left': [None		 ,	 'f'],	 # KP_Left
'KP_Up': [None		 ,	 'f'],	 # KP_Up
'KP_Right': [None		 ,	 'f'],	 # KP_Right
'KP_Down': [None		 ,	 'f'],	 # KP_Down
'KP_Prior': [None		 ,	 'f'],	 # KP_Prior
'KP_Next': [None		 ,	 'f'],	 # KP_Next
'KP_End': [None		 ,	 'f'],	 # KP_End
'KP_Begin': [None		 ,	 'f'],	 # KP_Begin
'KP_Insert': [None		 ,	 'f'],	 # KP_Insert
'KP_Delete': [None		 ,	 'f'],	 # KP_Delete
'KP_Multiply': [u'\u002a',	 'f'],	 # KP_Multiply
'KP_Add': [u'\u002b',	 'f'],	 # KP_Add
'KP_Separator': [u'\u002c',	 'f'],	 # KP_Separator	/* separator, often comma */
'KP_Subtract': [u'\u002d',	 'f'],	 # KP_Subtract
'KP_Decimal': [u'\u002e',	 'f'],	 # KP_Decimal
'KP_Divide': [u'\u002f',	 'f'],	 # KP_Divide
'KP_0': [u'\u0030',	 'f'],	 # KP_0
'KP_1': [u'\u0031',	 'f'],	 # KP_1
'KP_2': [u'\u0032',	 'f'],	 # KP_2
'KP_3': [u'\u0033',	 'f'],	 # KP_3
'KP_4': [u'\u0034',	 'f'],	 # KP_4
'KP_5': [u'\u0035',	 'f'],	 # KP_5
'KP_6': [u'\u0036',	 'f'],	 # KP_6
'KP_7': [u'\u0037',	 'f'],	 # KP_7
'KP_8': [u'\u0038',	 'f'],	 # KP_8
'KP_9': [u'\u0039',	 'f'],	 # KP_9
'KP_Equal': [u'\u003d',	 'f'],	 # KP_Equal	/* equals */
'F1': [None		 ,	 'f'],	 # F1
'F2': [None		 ,	 'f'],	 # F2
'F3': [None		 ,	 'f'],	 # F3
'F4': [None		 ,	 'f'],	 # F4
'F5': [None		 ,	 'f'],	 # F5
'F6': [None		 ,	 'f'],	 # F6
'F7': [None		 ,	 'f'],	 # F7
'F8': [None		 ,	 'f'],	 # F8
'F9': [None		 ,	 'f'],	 # F9
'F10': [None		 ,	 'f'],	 # F10
'F11': [None		 ,	 'f'],	 # F11
'F12': [None		 ,	 'f'],	 # F12
'F13': [None		 ,	 'f'],	 # F13
'F14': [None		 ,	 'f'],	 # F14
'F15': [None		 ,	 'f'],	 # F15
'F16': [None		 ,	 'f'],	 # F16
'F17': [None		 ,	 'f'],	 # F17
'F18': [None		 ,	 'f'],	 # F18
'F19': [None		 ,	 'f'],	 # F19
'F20': [None		 ,	 'f'],	 # F20
'F21': [None		 ,	 'f'],	 # F21
'F22': [None		 ,	 'f'],	 # F22
'F23': [None		 ,	 'f'],	 # F23
'F24': [None		 ,	 'f'],	 # F24
'F25': [None		 ,	 'f'],	 # F25
'F26': [None		 ,	 'f'],	 # F26
'F27': [None		 ,	 'f'],	 # F27
'F28': [None		 ,	 'f'],	 # F28
'F29': [None		 ,	 'f'],	 # F29
'F30': [None		 ,	 'f'],	 # F30
'F31': [None		 ,	 'f'],	 # F31
'F32': [None		 ,	 'f'],	 # F32
'F33': [None		 ,	 'f'],	 # F33
'F34': [None		 ,	 'f'],	 # F34
'F35': [None		 ,	 'f'],	 # F35
'Shift_L': [None		 ,	 'f'],	 # Shift_L
'Shift_R': [None		 ,	 'f'],	 # Shift_R
'Control_L': [None		 ,	 'f'],	 # Control_L
'Control_R': [None		 ,	 'f'],	 # Control_R
'Caps_Lock': [None		 ,	 'f'],	 # Caps_Lock
'Shift_Lock': [None		 ,	 'f'],	 # Shift_Lock
'Meta_L': [None		 ,	 'f'],	 # Meta_L
'Meta_R': [None		 ,	 'f'],	 # Meta_R
'Alt_L': [None		 ,	 'f'],	 # Alt_L
'Alt_R': [None		 ,	 'f'],	 # Alt_R
'Super_L': [None		 ,	 'f'],	 # Super_L
'Super_R': [None		 ,	 'f'],	 # Super_R
'Hyper_L': [None		 ,	 'f'],	 # Hyper_L
'Hyper_R': [None		 ,	 'f'],	 # Hyper_R
'Delete': [None		 ,	 'f'],	 # Delete
'VoidSymbol': [None		 ,	 'f'],	 # VoidSymbol
'Ukrainian_ghe_with_upturn': [u'\u0491',	 '.'],	 # Ukrainian_ghe_with_upturn
'Ukrainian_GHE_WITH_UPTURN': [u'\u0490',	 '.'],	 # Ukrainian_GHE_WITH_UPTURN
'Armenian_eternity': [None		 ,	 'r'],	 # Armenian_eternity
'Armenian_ligature_ew': [u'\u0587',	 'u'],	 # Armenian_ligature_ew
'Armenian_verjaket': [u'\u0589',	 'u'],	 # Armenian_verjaket
'Armenian_parenright': [u'\u0029',	 'r'],	 # Armenian_parenright
'Armenian_parenleft': [u'\u0028',	 'r'],	 # Armenian_parenleft
'Armenian_guillemotright': [u'\u00bb',	 'r'],	 # Armenian_guillemotright
'Armenian_guillemotleft': [u'\u00ab',	 'r'],	 # Armenian_guillemotleft
'Armenian_em_dash': [u'\u2014',	 'r'],	 # Armenian_em_dash
'Armenian_mijaket': [u'\u002e',	 'r'],	 # Armenian_mijaket
'Armenian_but': [u'\u055d',	 'u'],	 # Armenian_but
'Armenian_comma': [u'\u002c',	 'r'],	 # Armenian_comma
'Armenian_en_dash': [u'\u2013',	 'r'],	 # Armenian_en_dash
'Armenian_yentamna': [u'\u058a',	 'u'],	 # Armenian_yentamna
'Armenian_ellipsis': [u'\u2026',	 'r'],	 # Armenian_ellipsis
'Armenian_amanak': [u'\u055c',	 'u'],	 # Armenian_amanak
'Armenian_shesht': [u'\u055b',	 'u'],	 # Armenian_shesht
'Armenian_paruyk': [u'\u055e',	 'u'],	 # Armenian_paruyk
'Armenian_AYB': [u'\u0531',	 'u'],	 # Armenian_AYB
'Armenian_ayb': [u'\u0561',	 'u'],	 # Armenian_ayb
'Armenian_BEN': [u'\u0532',	 'u'],	 # Armenian_BEN
'Armenian_ben': [u'\u0562',	 'u'],	 # Armenian_ben
'Armenian_GIM': [u'\u0533',	 'u'],	 # Armenian_GIM
'Armenian_gim': [u'\u0563',	 'u'],	 # Armenian_gim
'Armenian_DA': [u'\u0534',	 'u'],	 # Armenian_DA
'Armenian_da': [u'\u0564',	 'u'],	 # Armenian_da
'Armenian_YECH': [u'\u0535',	 'u'],	 # Armenian_YECH
'Armenian_yech': [u'\u0565',	 'u'],	 # Armenian_yech
'Armenian_ZA': [u'\u0536',	 'u'],	 # Armenian_ZA
'Armenian_za': [u'\u0566',	 'u'],	 # Armenian_za
'Armenian_E': [u'\u0537',	 'u'],	 # Armenian_E
'Armenian_e': [u'\u0567',	 'u'],	 # Armenian_e
'Armenian_AT': [u'\u0538',	 'u'],	 # Armenian_AT
'Armenian_at': [u'\u0568',	 'u'],	 # Armenian_at
'Armenian_TO': [u'\u0539',	 'u'],	 # Armenian_TO
'Armenian_to': [u'\u0569',	 'u'],	 # Armenian_to
'Armenian_ZHE': [u'\u053a',	 'u'],	 # Armenian_ZHE
'Armenian_zhe': [u'\u056a',	 'u'],	 # Armenian_zhe
'Armenian_INI': [u'\u053b',	 'u'],	 # Armenian_INI
'Armenian_ini': [u'\u056b',	 'u'],	 # Armenian_ini
'Armenian_LYUN': [u'\u053c',	 'u'],	 # Armenian_LYUN
'Armenian_lyun': [u'\u056c',	 'u'],	 # Armenian_lyun
'Armenian_KHE': [u'\u053d',	 'u'],	 # Armenian_KHE
'Armenian_khe': [u'\u056d',	 'u'],	 # Armenian_khe
'Armenian_TSA': [u'\u053e',	 'u'],	 # Armenian_TSA
'Armenian_tsa': [u'\u056e',	 'u'],	 # Armenian_tsa
'Armenian_KEN': [u'\u053f',	 'u'],	 # Armenian_KEN
'Armenian_ken': [u'\u056f',	 'u'],	 # Armenian_ken
'Armenian_HO': [u'\u0540',	 'u'],	 # Armenian_HO
'Armenian_ho': [u'\u0570',	 'u'],	 # Armenian_ho
'Armenian_DZA': [u'\u0541',	 'u'],	 # Armenian_DZA
'Armenian_dza': [u'\u0571',	 'u'],	 # Armenian_dza
'Armenian_GHAT': [u'\u0542',	 'u'],	 # Armenian_GHAT
'Armenian_ghat': [u'\u0572',	 'u'],	 # Armenian_ghat
'Armenian_TCHE': [u'\u0543',	 'u'],	 # Armenian_TCHE
'Armenian_tche': [u'\u0573',	 'u'],	 # Armenian_tche
'Armenian_MEN': [u'\u0544',	 'u'],	 # Armenian_MEN
'Armenian_men': [u'\u0574',	 'u'],	 # Armenian_men
'Armenian_HI': [u'\u0545',	 'u'],	 # Armenian_HI
'Armenian_hi': [u'\u0575',	 'u'],	 # Armenian_hi
'Armenian_NU': [u'\u0546',	 'u'],	 # Armenian_NU
'Armenian_nu': [u'\u0576',	 'u'],	 # Armenian_nu
'Armenian_SHA': [u'\u0547',	 'u'],	 # Armenian_SHA
'Armenian_sha': [u'\u0577',	 'u'],	 # Armenian_sha
'Armenian_VO': [u'\u0548',	 'u'],	 # Armenian_VO
'Armenian_vo': [u'\u0578',	 'u'],	 # Armenian_vo
'Armenian_CHA': [u'\u0549',	 'u'],	 # Armenian_CHA
'Armenian_cha': [u'\u0579',	 'u'],	 # Armenian_cha
'Armenian_PE': [u'\u054a',	 'u'],	 # Armenian_PE
'Armenian_pe': [u'\u057a',	 'u'],	 # Armenian_pe
'Armenian_JE': [u'\u054b',	 'u'],	 # Armenian_JE
'Armenian_je': [u'\u057b',	 'u'],	 # Armenian_je
'Armenian_RA': [u'\u054c',	 'u'],	 # Armenian_RA
'Armenian_ra': [u'\u057c',	 'u'],	 # Armenian_ra
'Armenian_SE': [u'\u054d',	 'u'],	 # Armenian_SE
'Armenian_se': [u'\u057d',	 'u'],	 # Armenian_se
'Armenian_VEV': [u'\u054e',	 'u'],	 # Armenian_VEV
'Armenian_vev': [u'\u057e',	 'u'],	 # Armenian_vev
'Armenian_TYUN': [u'\u054f',	 'u'],	 # Armenian_TYUN
'Armenian_tyun': [u'\u057f',	 'u'],	 # Armenian_tyun
'Armenian_RE': [u'\u0550',	 'u'],	 # Armenian_RE
'Armenian_re': [u'\u0580',	 'u'],	 # Armenian_re
'Armenian_TSO': [u'\u0551',	 'u'],	 # Armenian_TSO
'Armenian_tso': [u'\u0581',	 'u'],	 # Armenian_tso
'Armenian_VYUN': [u'\u0552',	 'u'],	 # Armenian_VYUN
'Armenian_vyun': [u'\u0582',	 'u'],	 # Armenian_vyun
'Armenian_PYUR': [u'\u0553',	 'u'],	 # Armenian_PYUR
'Armenian_pyur': [u'\u0583',	 'u'],	 # Armenian_pyur
'Armenian_KE': [u'\u0554',	 'u'],	 # Armenian_KE
'Armenian_ke': [u'\u0584',	 'u'],	 # Armenian_ke
'Armenian_O': [u'\u0555',	 'u'],	 # Armenian_O
'Armenian_o': [u'\u0585',	 'u'],	 # Armenian_o
'Armenian_FE': [u'\u0556',	 'u'],	 # Armenian_FE
'Armenian_fe': [u'\u0586',	 'u'],	 # Armenian_fe
'Armenian_apostrophe': [u'\u055a',	 'u'],	 # Armenian_apostrophe
'Armenian_section_sign': [u'\u00a7',	 'r'],	 # Armenian_section_sign
'Georgian_an': [u'\u10d0',	 'u'],	 # Georgian_an
'Georgian_ban': [u'\u10d1',	 'u'],	 # Georgian_ban
'Georgian_gan': [u'\u10d2',	 'u'],	 # Georgian_gan
'Georgian_don': [u'\u10d3',	 'u'],	 # Georgian_don
'Georgian_en': [u'\u10d4',	 'u'],	 # Georgian_en
'Georgian_vin': [u'\u10d5',	 'u'],	 # Georgian_vin
'Georgian_zen': [u'\u10d6',	 'u'],	 # Georgian_zen
'Georgian_tan': [u'\u10d7',	 'u'],	 # Georgian_tan
'Georgian_in': [u'\u10d8',	 'u'],	 # Georgian_in
'Georgian_kan': [u'\u10d9',	 'u'],	 # Georgian_kan
'Georgian_las': [u'\u10da',	 'u'],	 # Georgian_las
'Georgian_man': [u'\u10db',	 'u'],	 # Georgian_man
'Georgian_nar': [u'\u10dc',	 'u'],	 # Georgian_nar
'Georgian_on': [u'\u10dd',	 'u'],	 # Georgian_on
'Georgian_par': [u'\u10de',	 'u'],	 # Georgian_par
'Georgian_zhar': [u'\u10df',	 'u'],	 # Georgian_zhar
'Georgian_rae': [u'\u10e0',	 'u'],	 # Georgian_rae
'Georgian_san': [u'\u10e1',	 'u'],	 # Georgian_san
'Georgian_tar': [u'\u10e2',	 'u'],	 # Georgian_tar
'Georgian_un': [u'\u10e3',	 'u'],	 # Georgian_un
'Georgian_phar': [u'\u10e4',	 'u'],	 # Georgian_phar
'Georgian_khar': [u'\u10e5',	 'u'],	 # Georgian_khar
'Georgian_ghan': [u'\u10e6',	 'u'],	 # Georgian_ghan
'Georgian_qar': [u'\u10e7',	 'u'],	 # Georgian_qar
'Georgian_shin': [u'\u10e8',	 'u'],	 # Georgian_shin
'Georgian_chin': [u'\u10e9',	 'u'],	 # Georgian_chin
'Georgian_can': [u'\u10ea',	 'u'],	 # Georgian_can
'Georgian_jil': [u'\u10eb',	 'u'],	 # Georgian_jil
'Georgian_cil': [u'\u10ec',	 'u'],	 # Georgian_cil
'Georgian_char': [u'\u10ed',	 'u'],	 # Georgian_char
'Georgian_xan': [u'\u10ee',	 'u'],	 # Georgian_xan
'Georgian_jhan': [u'\u10ef',	 'u'],	 # Georgian_jhan
'Georgian_hae': [u'\u10f0',	 'u'],	 # Georgian_hae
'Georgian_he': [u'\u10f1',	 'u'],	 # Georgian_he
'Georgian_hie': [u'\u10f2',	 'u'],	 # Georgian_hie
'Georgian_we': [u'\u10f3',	 'u'],	 # Georgian_we
'Georgian_har': [u'\u10f4',	 'u'],	 # Georgian_har
'Georgian_hoe': [u'\u10f5',	 'u'],	 # Georgian_hoe
'Georgian_fi': [u'\u10f6',	 'u'],	 # Georgian_fi
'Babovedot': [u'\u1e02',	 'u'],	 # Babovedot
'babovedot': [u'\u1e03',	 'u'],	 # babovedot
'Dabovedot': [u'\u1e0a',	 'u'],	 # Dabovedot
'Wgrave': [u'\u1e80',	 'u'],	 # Wgrave
'Wacute': [u'\u1e82',	 'u'],	 # Wacute
'dabovedot': [u'\u1e0b',	 'u'],	 # dabovedot
'Ygrave': [u'\u1ef2',	 'u'],	 # Ygrave
'Fabovedot': [u'\u1e1e',	 'u'],	 # Fabovedot
'fabovedot': [u'\u1e1f',	 'u'],	 # fabovedot
'Mabovedot': [u'\u1e40',	 'u'],	 # Mabovedot
'mabovedot': [u'\u1e41',	 'u'],	 # mabovedot
'Pabovedot': [u'\u1e56',	 'u'],	 # Pabovedot
'wgrave': [u'\u1e81',	 'u'],	 # wgrave
'pabovedot': [u'\u1e57',	 'u'],	 # pabovedot
'wacute': [u'\u1e83',	 'u'],	 # wacute
'Sabovedot': [u'\u1e60',	 'u'],	 # Sabovedot
'ygrave': [u'\u1ef3',	 'u'],	 # ygrave
'Wdiaeresis': [u'\u1e84',	 'u'],	 # Wdiaeresis
'wdiaeresis': [u'\u1e85',	 'u'],	 # wdiaeresis
'sabovedot': [u'\u1e61',	 'u'],	 # sabovedot
'Wcircumflex': [u'\u0174',	 'u'],	 # Wcircumflex
'Tabovedot': [u'\u1e6a',	 'u'],	 # Tabovedot
'Ycircumflex': [u'\u0176',	 'u'],	 # Ycircumflex
'wcircumflex': [u'\u0175',	 'u'],	 # wcircumflex
'tabovedot': [u'\u1e6b',	 'u'],	 # tabovedot
'ycircumflex': [u'\u0177',	 'u'],	 # ycircumflex
'Farsi_0': [u'\u06f0',	 'u'],	 # Farsi_0
'Farsi_1': [u'\u06f1',	 'u'],	 # Farsi_1
'Farsi_2': [u'\u06f2',	 'u'],	 # Farsi_2
'Farsi_3': [u'\u06f3',	 'u'],	 # Farsi_3
'Farsi_4': [u'\u06f4',	 'u'],	 # Farsi_4
'Farsi_5': [u'\u06f5',	 'u'],	 # Farsi_5
'Farsi_6': [u'\u06f6',	 'u'],	 # Farsi_6
'Farsi_7': [u'\u06f7',	 'u'],	 # Farsi_7
'Farsi_8': [u'\u06f8',	 'u'],	 # Farsi_8
'Farsi_9': [u'\u06f9',	 'u'],	 # Farsi_9
'Arabic_percent': [u'\u066a',	 'u'],	 # Arabic_percent
'Arabic_superscript_alef': [u'\u0670',	 'u'],	 # Arabic_superscript_alef
'Arabic_tteh': [u'\u0679',	 'u'],	 # Arabic_tteh
'Arabic_peh': [u'\u067e',	 'u'],	 # Arabic_peh
'Arabic_tcheh': [u'\u0686',	 'u'],	 # Arabic_tcheh
'Arabic_ddal': [u'\u0688',	 'u'],	 # Arabic_ddal
'Arabic_rreh': [u'\u0691',	 'u'],	 # Arabic_rreh
'Arabic_fullstop': [u'\u06d4',	 'u'],	 # Arabic_fullstop
'Arabic_0': [u'\u0660',	 'u'],	 # Arabic_0
'Arabic_1': [u'\u0661',	 'u'],	 # Arabic_1
'Arabic_2': [u'\u0662',	 'u'],	 # Arabic_2
'Arabic_3': [u'\u0663',	 'u'],	 # Arabic_3
'Arabic_4': [u'\u0664',	 'u'],	 # Arabic_4
'Arabic_5': [u'\u0665',	 'u'],	 # Arabic_5
'Arabic_6': [u'\u0666',	 'u'],	 # Arabic_6
'Arabic_7': [u'\u0667',	 'u'],	 # Arabic_7
'Arabic_8': [u'\u0668',	 'u'],	 # Arabic_8
'Arabic_9': [u'\u0669',	 'u'],	 # Arabic_9
'Arabic_madda_above': [u'\u0653',	 'u'],	 # Arabic_madda_above
'Arabic_hamza_above': [u'\u0654',	 'u'],	 # Arabic_hamza_above
'Arabic_hamza_below': [u'\u0655',	 'u'],	 # Arabic_hamza_below
'Arabic_jeh': [u'\u0698',	 'u'],	 # Arabic_jeh
'Arabic_veh': [u'\u06a4',	 'u'],	 # Arabic_veh
'Arabic_keheh': [u'\u06a9',	 'u'],	 # Arabic_keheh
'Arabic_gaf': [u'\u06af',	 'u'],	 # Arabic_gaf
'Arabic_noon_ghunna': [u'\u06ba',	 'u'],	 # Arabic_noon_ghunna
'Arabic_heh_doachashmee': [u'\u06be',	 'u'],	 # Arabic_heh_doachashmee
'Farsi_yeh': [u'\u06cc',	 'u'],	 # Farsi_yeh
'Arabic_yeh_baree': [u'\u06d2',	 'u'],	 # Arabic_yeh_baree
'Arabic_heh_goal': [u'\u06c1',	 'u'],	 # Arabic_heh_goal
'Cyrillic_GHE_bar': [u'\u0492',	 'u'],	 # Cyrillic_GHE_bar
'Cyrillic_ZHE_descender': [u'\u0496',	 'u'],	 # Cyrillic_ZHE_descender
'Cyrillic_KA_descender': [u'\u049a',	 'u'],	 # Cyrillic_KA_descender
'Cyrillic_KA_vertstroke': [u'\u049c',	 'u'],	 # Cyrillic_KA_vertstroke
'Cyrillic_EN_descender': [u'\u04a2',	 'u'],	 # Cyrillic_EN_descender
'Cyrillic_U_straight': [u'\u04ae',	 'u'],	 # Cyrillic_U_straight
'Cyrillic_U_straight_bar': [u'\u04b0',	 'u'],	 # Cyrillic_U_straight_bar
'Cyrillic_HA_descender': [u'\u04b2',	 'u'],	 # Cyrillic_HA_descender
'Cyrillic_CHE_descender': [u'\u04b6',	 'u'],	 # Cyrillic_CHE_descender
'Cyrillic_CHE_vertstroke': [u'\u04b8',	 'u'],	 # Cyrillic_CHE_vertstroke
'Cyrillic_SHHA': [u'\u04ba',	 'u'],	 # Cyrillic_SHHA
'Cyrillic_SCHWA': [u'\u04d8',	 'u'],	 # Cyrillic_SCHWA
'Cyrillic_I_macron': [u'\u04e2',	 'u'],	 # Cyrillic_I_macron
'Cyrillic_O_bar': [u'\u04e8',	 'u'],	 # Cyrillic_O_bar
'Cyrillic_U_macron': [u'\u04ee',	 'u'],	 # Cyrillic_U_macron
'Cyrillic_ghe_bar': [u'\u0493',	 'u'],	 # Cyrillic_ghe_bar
'Cyrillic_zhe_descender': [u'\u0497',	 'u'],	 # Cyrillic_zhe_descender
'Cyrillic_ka_descender': [u'\u049b',	 'u'],	 # Cyrillic_ka_descender
'Cyrillic_ka_vertstroke': [u'\u049d',	 'u'],	 # Cyrillic_ka_vertstroke
'Cyrillic_en_descender': [u'\u04a3',	 'u'],	 # Cyrillic_en_descender
'Cyrillic_u_straight': [u'\u04af',	 'u'],	 # Cyrillic_u_straight
'Cyrillic_u_straight_bar': [u'\u04b1',	 'u'],	 # Cyrillic_u_straight_bar
'Cyrillic_ha_descender': [u'\u04b3',	 'u'],	 # Cyrillic_ha_descender
'Cyrillic_che_descender': [u'\u04b7',	 'u'],	 # Cyrillic_che_descender
'Cyrillic_che_vertstroke': [u'\u04b9',	 'u'],	 # Cyrillic_che_vertstroke
'Cyrillic_shha': [u'\u04bb',	 'u'],	 # Cyrillic_shha
'Cyrillic_schwa': [u'\u04d9',	 'u'],	 # Cyrillic_schwa
'Cyrillic_i_macron': [u'\u04e3',	 'u'],	 # Cyrillic_i_macron
'Cyrillic_o_bar': [u'\u04e9',	 'u'],	 # Cyrillic_o_bar
'Cyrillic_u_macron': [u'\u04ef',	 'u'],	 # Cyrillic_u_macron
'Ccedillaabovedot': [None		 ,	 'r'],	 # Ccedillaabovedot
'Xabovedot': [u'\u1e8a',	 'u'],	 # Xabovedot
'Qabovedot': [None		 ,	 'r'],	 # Qabovedot
'Ibreve': [u'\u012c',	 'u'],	 # Ibreve
'IE': [None		 ,	 'r'],	 # IE
'UO': [None		 ,	 'r'],	 # UO
'Zstroke': [u'\u01b5',	 'u'],	 # Zstroke
'Gcaron': [u'\u01e6',	 'u'],	 # Gcaron
'Obarred': [u'\u019f',	 'u'],	 # Obarred
'ccedillaabovedot': [None		 ,	 'r'],	 # ccedillaabovedot
'xabovedot': [u'\u1e8b',	 'u'],	 # xabovedot
'Ocaron': [None		 ,	 'r'],	 # Ocaron
'qabovedot': [None		 ,	 'r'],	 # qabovedot
'ibreve': [u'\u012d',	 'u'],	 # ibreve
'ie': [None		 ,	 'r'],	 # ie
'uo': [None		 ,	 'r'],	 # uo
'zstroke': [u'\u01b6',	 'u'],	 # zstroke
'gcaron': [u'\u01e7',	 'u'],	 # gcaron
'ocaron': [u'\u01d2',	 'u'],	 # ocaron
'obarred': [u'\u0275',	 'u'],	 # obarred
'SCHWA': [u'\u018f',	 'u'],	 # SCHWA
'schwa': [u'\u0259',	 'u'],	 # schwa
'Lbelowdot': [u'\u1e36',	 'u'],	 # Lbelowdot
'Lstrokebelowdot': [None		 ,	 'r'],	 # Lstrokebelowdot
'Gtilde': [None		 ,	 'r'],	 # Gtilde
'lbelowdot': [u'\u1e37',	 'u'],	 # lbelowdot
'lstrokebelowdot': [None		 ,	 'r'],	 # lstrokebelowdot
'gtilde': [None		 ,	 'r'],	 # gtilde
'Abelowdot': [u'\u1ea0',	 'u'],	 # Abelowdot
'abelowdot': [u'\u1ea1',	 'u'],	 # abelowdot
'Ahook': [u'\u1ea2',	 'u'],	 # Ahook
'ahook': [u'\u1ea3',	 'u'],	 # ahook
'Acircumflexacute': [u'\u1ea4',	 'u'],	 # Acircumflexacute
'acircumflexacute': [u'\u1ea5',	 'u'],	 # acircumflexacute
'Acircumflexgrave': [u'\u1ea6',	 'u'],	 # Acircumflexgrave
'acircumflexgrave': [u'\u1ea7',	 'u'],	 # acircumflexgrave
'Acircumflexhook': [u'\u1ea8',	 'u'],	 # Acircumflexhook
'acircumflexhook': [u'\u1ea9',	 'u'],	 # acircumflexhook
'Acircumflextilde': [u'\u1eaa',	 'u'],	 # Acircumflextilde
'acircumflextilde': [u'\u1eab',	 'u'],	 # acircumflextilde
'Acircumflexbelowdot': [u'\u1eac',	 'u'],	 # Acircumflexbelowdot
'acircumflexbelowdot': [u'\u1ead',	 'u'],	 # acircumflexbelowdot
'Abreveacute': [u'\u1eae',	 'u'],	 # Abreveacute
'abreveacute': [u'\u1eaf',	 'u'],	 # abreveacute
'Abrevegrave': [u'\u1eb0',	 'u'],	 # Abrevegrave
'abrevegrave': [u'\u1eb1',	 'u'],	 # abrevegrave
'Abrevehook': [u'\u1eb2',	 'u'],	 # Abrevehook
'abrevehook': [u'\u1eb3',	 'u'],	 # abrevehook
'Abrevetilde': [u'\u1eb4',	 'u'],	 # Abrevetilde
'abrevetilde': [u'\u1eb5',	 'u'],	 # abrevetilde
'Abrevebelowdot': [u'\u1eb6',	 'u'],	 # Abrevebelowdot
'abrevebelowdot': [u'\u1eb7',	 'u'],	 # abrevebelowdot
'Ebelowdot': [u'\u1eb8',	 'u'],	 # Ebelowdot
'ebelowdot': [u'\u1eb9',	 'u'],	 # ebelowdot
'Ehook': [u'\u1eba',	 'u'],	 # Ehook
'ehook': [u'\u1ebb',	 'u'],	 # ehook
'Etilde': [u'\u1ebc',	 'u'],	 # Etilde
'etilde': [u'\u1ebd',	 'u'],	 # etilde
'Ecircumflexacute': [u'\u1ebe',	 'u'],	 # Ecircumflexacute
'ecircumflexacute': [u'\u1ebf',	 'u'],	 # ecircumflexacute
'Ecircumflexgrave': [u'\u1ec0',	 'u'],	 # Ecircumflexgrave
'ecircumflexgrave': [u'\u1ec1',	 'u'],	 # ecircumflexgrave
'Ecircumflexhook': [u'\u1ec2',	 'u'],	 # Ecircumflexhook
'ecircumflexhook': [u'\u1ec3',	 'u'],	 # ecircumflexhook
'Ecircumflextilde': [u'\u1ec4',	 'u'],	 # Ecircumflextilde
'ecircumflextilde': [u'\u1ec5',	 'u'],	 # ecircumflextilde
'Ecircumflexbelowdot': [u'\u1ec6',	 'u'],	 # Ecircumflexbelowdot
'ecircumflexbelowdot': [u'\u1ec7',	 'u'],	 # ecircumflexbelowdot
'Ihook': [u'\u1ec8',	 'u'],	 # Ihook
'ihook': [u'\u1ec9',	 'u'],	 # ihook
'Ibelowdot': [u'\u1eca',	 'u'],	 # Ibelowdot
'ibelowdot': [u'\u1ecb',	 'u'],	 # ibelowdot
'Obelowdot': [u'\u1ecc',	 'u'],	 # Obelowdot
'obelowdot': [u'\u1ecd',	 'u'],	 # obelowdot
'Ohook': [u'\u1ece',	 'u'],	 # Ohook
'ohook': [u'\u1ecf',	 'u'],	 # ohook
'Ocircumflexacute': [u'\u1ed0',	 'u'],	 # Ocircumflexacute
'ocircumflexacute': [u'\u1ed1',	 'u'],	 # ocircumflexacute
'Ocircumflexgrave': [u'\u1ed2',	 'u'],	 # Ocircumflexgrave
'ocircumflexgrave': [u'\u1ed3',	 'u'],	 # ocircumflexgrave
'Ocircumflexhook': [u'\u1ed4',	 'u'],	 # Ocircumflexhook
'ocircumflexhook': [u'\u1ed5',	 'u'],	 # ocircumflexhook
'Ocircumflextilde': [u'\u1ed6',	 'u'],	 # Ocircumflextilde
'ocircumflextilde': [u'\u1ed7',	 'u'],	 # ocircumflextilde
'Ocircumflexbelowdot': [u'\u1ed8',	 'u'],	 # Ocircumflexbelowdot
'ocircumflexbelowdot': [u'\u1ed9',	 'u'],	 # ocircumflexbelowdot
'Ohornacute': [u'\u1eda',	 'u'],	 # Ohornacute
'ohornacute': [u'\u1edb',	 'u'],	 # ohornacute
'Ohorngrave': [u'\u1edc',	 'u'],	 # Ohorngrave
'ohorngrave': [u'\u1edd',	 'u'],	 # ohorngrave
'Ohornhook': [u'\u1ede',	 'u'],	 # Ohornhook
'ohornhook': [u'\u1edf',	 'u'],	 # ohornhook
'Ohorntilde': [u'\u1ee0',	 'u'],	 # Ohorntilde
'ohorntilde': [u'\u1ee1',	 'u'],	 # ohorntilde
'Ohornbelowdot': [u'\u1ee2',	 'u'],	 # Ohornbelowdot
'ohornbelowdot': [u'\u1ee3',	 'u'],	 # ohornbelowdot
'Ubelowdot': [u'\u1ee4',	 'u'],	 # Ubelowdot
'ubelowdot': [u'\u1ee5',	 'u'],	 # ubelowdot
'Uhook': [u'\u1ee6',	 'u'],	 # Uhook
'uhook': [u'\u1ee7',	 'u'],	 # uhook
'Uhornacute': [u'\u1ee8',	 'u'],	 # Uhornacute
'uhornacute': [u'\u1ee9',	 'u'],	 # uhornacute
'Uhorngrave': [u'\u1eea',	 'u'],	 # Uhorngrave
'uhorngrave': [u'\u1eeb',	 'u'],	 # uhorngrave
'Uhornhook': [u'\u1eec',	 'u'],	 # Uhornhook
'uhornhook': [u'\u1eed',	 'u'],	 # uhornhook
'Uhorntilde': [u'\u1eee',	 'u'],	 # Uhorntilde
'uhorntilde': [u'\u1eef',	 'u'],	 # uhorntilde
'Uhornbelowdot': [u'\u1ef0',	 'u'],	 # Uhornbelowdot
'uhornbelowdot': [u'\u1ef1',	 'u'],	 # uhornbelowdot
'Ybelowdot': [u'\u1ef4',	 'u'],	 # Ybelowdot
'ybelowdot': [u'\u1ef5',	 'u'],	 # ybelowdot
'Yhook': [u'\u1ef6',	 'u'],	 # Yhook
'yhook': [u'\u1ef7',	 'u'],	 # yhook
'Ytilde': [u'\u1ef8',	 'u'],	 # Ytilde
'ytilde': [u'\u1ef9',	 'u'],	 # ytilde
'Ohorn': [u'\u01a0',	 'u'],	 # Ohorn
'ohorn': [u'\u01a1',	 'u'],	 # ohorn
'Uhorn': [u'\u01af',	 'u'],	 # Uhorn
'uhorn': [u'\u01b0',	 'u'],	 # uhorn
'combining_tilde': [u'\u0303',	 'r'],	 # combining_tilde
'combining_grave': [u'\u0300',	 'r'],	 # combining_grave
'combining_acute': [u'\u0301',	 'r'],	 # combining_acute
'combining_hook': [u'\u0309',	 'r'],	 # combining_hook
'combining_belowdot': [u'\u0323',	 'r'],	 # combining_belowdot
'dead_belowdot': [u'\u0323',	 'f'],	 # dead_belowdot
'dead_hook': [u'\u0309',	 'f'],	 # dead_hook
'dead_horn': [u'\u031b',	 'f'],	 # dead_horn
}
