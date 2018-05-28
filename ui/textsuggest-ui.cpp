#include <iostream>
#include <vector>
#include <string>

#include <dbus-c++/dbus.h>

#include "../lib/cxxopts.hpp"

#include "TextSuggestServerIFace.hpp"
#include "../common.hpp"
#include "TextSuggestApp.hpp"

DBus::BusDispatcher dispatcher;

int main(int argc, char ** argv) {

	cxxopts::Options options ("TextSuggest", "TextSuggest — universal autocomplete  (UI)");

	options.add_options()
	("h,help", "Print help")
	("word", "Show suggestions for WORD. Default: show all words", cxxopts::value<std::string>()->default_value(""))
	("history", "Enable/Disable frequently-used-words history", cxxopts::value<bool>()->default_value("true"))
	("l,language", "Set language(s). Default: English", cxxopts::value<std::vector<std::string>>()->default_value("English"))
	("auto-detect-language", "Auto-detect language from keyboard layout", cxxopts::value<bool>()->default_value("false"))
	("selection", "Show suggestions for currently selected word", cxxopts::value<bool>()->default_value("false"))
	("auto-selection", "Automatically select word under cursor and suggest", cxxopts::value<std::string>()->default_value("none"))
	("custom-words-only", "Show custom words only", cxxopts::value<bool>()->default_value("false"))
	("processing", "Enable/Disable processors (extensions)", cxxopts::value<bool>()->default_value("true"))
	("v,version", "Print version and license information")
	;

	auto result = options.parse(argc, (const char**&)argv);

	if (result.count("help")) {
		std::cout << UI_HELP_MESSAGE << std::endl;
		return 0;
	}

	if (result.count("version")) {
		std::cout << "TextSuggest release " << VERSION[0]<<"."<<VERSION[1]<<"."<<VERSION[2] 
				  << " (build "<<BUILD<<")" << std::endl << std::endl;
		std::cout << VERSION_MESSAGE << std::endl;
		return 0;
	}

	auto& opt_word = result["word"].as<std::string>();
	auto& opt_history = result["history"].as<bool>();
	auto& opt_languages = result["language"].as<std::vector<std::string>>();
	auto& opt_auto_detect_language = result["auto-detect-language"].as<bool>();
	auto& opt_selection = result["selection"].as<bool>();
	auto& opt_auto_selection = result["auto-selection"].as<std::string>();
	auto& opt_custom_words_only = result["custom-words-only"].as<bool>();
	auto& opt_processing = result["processing"].as<bool>();

	DBus::default_dispatcher = &dispatcher;
	DBus::Connection bus = DBus::Connection::SessionBus();

	try {
		TextSuggestServerIFace server (bus, OBJECT_PATH, SERVICE_NAME);
		server.get_clipboard_text();  // test calls
		TextSuggestApp * app;
		app = new TextSuggestApp(argc, argv, &server, opt_word, opt_history, opt_languages,
				opt_auto_detect_language, opt_selection, opt_auto_selection,
				opt_custom_words_only, opt_processing);
		app->loadUI();
		app->showUI();
		return app->exec();
		
	} catch (DBus::Error) {
		std::cout << "The TextSuggest server is (probably) not running!  (DBus service 'org.textsuggest.server' not found)" << std::endl;
		std::cout << std::endl;
		std::cout << "Start the server using the command 'textsuggest-server &', and run this again." << std::endl;
		return 1;
	}

	return 0;

}