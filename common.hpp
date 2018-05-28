#ifndef TEXTSUGGEST_COMMON_H
#define TEXTSUGGEST_COMMON_H

#include <string>

const int BUILD = 4000;
const int VERSION[3] = {4, 0, 0};  // x.y.z

static const char * SERVICE_NAME = "org.textsuggest.server";
static const char * OBJECT_PATH = "/org/textsuggest/server";

std::string VERSION_MESSAGE = R"TEXT(Copyright © 2016-2018 Bharadwaj Raju, and others <https://github.com/bharadwaj-raju/TextSuggest/graphs/contributors>.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.)TEXT";

std::string UI_HELP_MESSAGE = R"TEXT(usage: textsuggest [options]
TextSuggest — universal autocomplete  (UI)

	optional arguments:
	  
	  -h, --help            show this help message and exit
	  
	  --word WORD           Specify word to give suggestions for. Default: show all words. 
	                         
	  --history [true|false]
	                        Enable/Disable the frequently-used-words history (stored in ~/.config/textsuggest/history.json) 
	                         
	  -l, --language LANGUAGE [--language LANGUAGE_2 ...]
                            Set language(s). Default: English. See also: --auto-detect-language. 
	                         
	  --auto-detect-language
	                        Auto-detect language from keyboard layout. 
	                         
	  --selection           Show suggestions for currently selected word. See also: --auto-selection 
	                         
	  --auto-selection [beginning|middle|end]
	                        Automatically select word under cursor and suggest. Ignored if --no-selection.
	                         
	  --custom-words-only [true|false]
	                        Show custom words only (true = custom words only | false = all words)
	                         
	  --processing [true|false]
	                        Enable/Disable using of processors (extensions). 
	                         
	  -v, --version         Print version and license information.)TEXT";

std::string SERVER_HELP_MESSAGE = R"TEXT(usage: textsuggest-server [options]
TextSuggest — universal autocomplete  (Server)

	optional arguments:
	  
	  -h, --help            show this help message and exit
	                         
	  -v, --version         Print version and license information.)TEXT";

#endif // TEXTSUGGEST_COMMON_H