#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <functional>
#include <chrono>
#include <ctime>

#include "dbus-adaptor.hpp"

#include "Processors.hpp"
#include "Util.hpp"
#include "Files.hpp"
#include "DataBase.hpp"
#include "../lib/subprocess.hpp"
#include "../lib/clip/clip.h"
#include "../lib/fts.hpp"
#include "../lib/json.hpp"
#include "../lib/prettyprint.hpp"

using json = nlohmann::json;

Files files = Files();

std::vector<std::pair<std::string, int>> fuzzy_finder(std::string pattern, std::vector<std::string> seq) {

	std::vector<std::pair<std::string, int>> scored_results;

	for (std::string word : seq) {
		int score;
		if (fts::fuzzy_match(pattern.c_str(), word.c_str(), score)) {
			// matched
			scored_results.push_back({word, score});
		}
	}

	typedef std::function<bool(std::pair<std::string, int>, std::pair<std::string, int>)> Comparator;
 
	Comparator compare_fn = [](std::pair<std::string, int> entry1, std::pair<std::string, int> entry2) {
		return entry1.second < entry2.second;
	};

	std::sort(scored_results.begin(), scored_results.end(), compare_fn);

	return scored_results;

}

const char * SERVER_NAME = "org.textsuggest.server";
const char * SERVER_PATH = "/org/textsuggest/server";

class TextSuggestServer
: public org::textsuggest::server_adaptor,
  public DBus::IntrospectableAdaptor,
  public DBus::ObjectAdaptor
{
public:
	TextSuggestServer(DBus::Connection &connection)
	: DBus::ObjectAdaptor(connection, SERVER_PATH) {

		custom_words.load(files.custom_words_file);
		history.load(files.history_file);
		ignore_list.load(files.ignore_list_file);
		
		load_dictionaries();
	
	};
	
	std::map<std::string, std::vector<std::string>> dictionaries;
	JSONDataBase custom_words;
	JSONDataBase history;
	JSONDataBase ignore_list;

	typedef std::function<bool(std::pair<std::string, int>, std::pair<std::string, int>)> Comparator;
	typedef std::function<bool(std::string, std::string)> HistoryOnlyComparator;
 
	Comparator compare_fn = [this](std::pair<std::string, int> entry1, std::pair<std::string, int> entry2) {
		// implement history score support directly in the comparison function
		// to avoid unnecessary iteration over scored_suggestions
		return (entry1.second + this->history_score(entry1.first)) >
				(entry2.second + this->history_score(entry2.first));
	};

	HistoryOnlyComparator history_only_compare_fn = [this](std::string entry1, std::string entry2) {
		// no individual scores for words
		// all depends on history score
		return (this->history_score(entry1)) > (this->history_score(entry2));
	};

	virtual void load_dictionaries() {
		
		for (std::pair<std::string, std::string> entry : files.dictionary_files) {
			
			// entry = {display_name, file_path}
			std::string line;
			std::ifstream dict_f;
			dict_f.open(entry.second);

			std::vector<std::string> dictionary;

			while (std::getline(dict_f, line, '\n')) {
				line.erase(line.find_last_not_of(" \n\r\t")+1);
				if ((line != "") && 
					(std::find(ignore_list.db.begin(), ignore_list.db.end(), line) == ignore_list.db.end())) {
						dictionary.push_back(line);
				}
			}

			dict_f.close();

			dictionaries[entry.first] = dictionary;
			
		}
	
	};

	virtual void load_custom_words() {
		custom_words.load(files.custom_words_file);	
	};
	virtual void load_ignore_list() {
		ignore_list.load(files.ignore_list_file);
	};

	virtual void reload_configs() {
	
		custom_words.load(files.custom_words_file);
		ignore_list.load(files.ignore_list_file);
	
	};

	virtual void type_text(const std::string &text) {

		std::cout << "type_text(" << text << ")" << std::endl;

		std::string old_clipboard_text = get_clipboard_text();
		set_clipboard_text(text);
		get_clipboard_text();
		sp::popen proc ("xdotool", {"key", "--clearmodifiers", "Control_L+v"});
		proc.wait();
		get_clipboard_text();
		//set_clipboard_text(old_clipboard_text);

	};

	virtual std::vector<std::string> get_suggestions(const std::string &word, const std::vector<std::string> &languages) {

		std::vector<std::string> suggestions;
		std::vector<std::pair<std::string, int>> scored_suggestions;
		auto start = std::chrono::steady_clock::now();

		for (std::pair<std::string, std::vector<std::string>> dictionary : dictionaries) {
			// dictionary = {display_name, words[]}
			if (std::find(languages.begin(), languages.end(), dictionary.first) != languages.end()) {
				std::vector<std::pair<std::string, int>> dict_suggestions;
				dict_suggestions = fuzzy_finder(word, dictionary.second);
				scored_suggestions.reserve(scored_suggestions.size() + dict_suggestions.size());
				scored_suggestions.insert(scored_suggestions.end(), dict_suggestions.begin(), dict_suggestions.end());
			}
		}

		for (auto entry : custom_words.db.items()) {
			// entry = {word, expansion}
			int score;
			if (fts::fuzzy_match(word.c_str(), entry.key().c_str(), score)) {
				if (std::find(ignore_list.db.begin(), ignore_list.db.end(), entry.key()) == ignore_list.db.end()) {
					scored_suggestions.push_back({entry.key(), score});
				}
			}
		}

		std::sort(scored_suggestions.begin(), scored_suggestions.end(), compare_fn);
		
		suggestions.reserve(suggestions.size() + scored_suggestions.size());
		for (std::pair<std::string, int> scored_suggestion : scored_suggestions) {
			suggestions.push_back(scored_suggestion.first);
		}

		auto end = std::chrono::steady_clock::now();
		auto duration = end - start;
		auto seconds = std::chrono::duration_cast<std::chrono::duration<float>>(duration);

		std::cout << "time get_suggestions("<<word<<", "<<languages<<") = " << seconds.count() << std::endl;

		return suggestions;

	};

	virtual std::vector<std::string> get_custom_words_only(const std::string &word) {

		std::vector<std::string> suggestions;
		std::vector<std::pair<std::string, int>> scored_suggestions;
		auto start = std::chrono::steady_clock::now();

		for (auto entry : custom_words.db.items()) {
			// entry = {word, expansion}
			if (word == "") {
				scored_suggestions.push_back({entry.key(), 0});
			} else {
				int score;
				if (fts::fuzzy_match(word.c_str(), entry.key().c_str(), score)) {
					if (std::find(ignore_list.db.begin(), ignore_list.db.end(), entry.key()) == ignore_list.db.end()) {
						scored_suggestions.push_back({entry.key(), score});
					}
				}
			}
		}

		std::sort(scored_suggestions.begin(), scored_suggestions.end(), compare_fn);
		
		suggestions.reserve(suggestions.size() + scored_suggestions.size());
		for (std::pair<std::string, int> scored_suggestion : scored_suggestions) {
			suggestions.push_back(scored_suggestion.first);
		}

		auto end = std::chrono::steady_clock::now();
		auto duration = end - start;
		auto seconds = std::chrono::duration_cast<std::chrono::duration<float>>(duration);

		std::cout << "time get_custom_words_only("<<word<<") = " << seconds.count() << std::endl;

		return suggestions;
	
	};

	virtual std::vector<std::string> get_all_words(const std::vector<std::string> &languages) {

		std::vector<std::string> words;
		auto start = std::chrono::steady_clock::now();

		for (auto entry : custom_words.db.items()) {
			// entry = {word, expansion}
			// make custom words be higher in results than dictionary words
			if (std::find(ignore_list.db.begin(), ignore_list.db.end(), entry.key()) == ignore_list.db.end()) {
				words.push_back(entry.key());
			}
		}

		for (std::pair<std::string, std::vector<std::string>> dictionary : dictionaries) {
			// dictionary = {display_name, words[]}
			if (std::find(languages.begin(), languages.end(), dictionary.first) != languages.end()) {
				words.reserve(words.size() + dictionary.second.size());
				words.insert(words.end(), dictionary.second.begin(), dictionary.second.end());
			}
		}

		std::sort(words.begin(), words.end(), history_only_compare_fn);

		auto end = std::chrono::steady_clock::now();
		auto duration = end - start;
		auto seconds = std::chrono::duration_cast<std::chrono::duration<float>>(duration);

		std::cout << "time get_all_words("<<languages<<") = " << seconds.count() << std::endl;

		return words;

	};

	virtual std::string process_suggestion(const std::string &suggestion) {
		
		std::string final (suggestion);
		auto start = std::chrono::steady_clock::now();
		
		std::cout << "Processing '" << suggestion << "'" << std::endl;

		for (auto custom_word : custom_words.db.items()) {
			if (custom_word.key() == final) {
				final = custom_word.value().get<std::string>();
			}
		}

		std::map<std::string, std::string> processors = Processors::find_processors();
		for (auto entry : processors) {
			// each entry is (basename, filepath)
			if (Processors::matches(entry.second, final)) {
				std::cout << "    Using processor '" << entry.first << "' from '" << entry.second << "'" << std::endl;
				final = Processors::process(entry.second, final);
			}
		}

		std::cout << "    Result: '" << final << "'" << std::endl;

		auto end = std::chrono::steady_clock::now();
		auto duration = end - start;
		auto seconds = std::chrono::duration_cast<std::chrono::duration<float>>(duration);

		std::cout << "time process_suggestion("<<suggestion<<") = " << seconds.count() << std::endl;

		return final;

	};

	virtual void autoselect_current_word(const std::string &mode) {

		if (mode == "beginning") {
			sp::popen proc ("xdotool", {"key", "Control_L+Shift+Right"});
			proc.wait();
		} else if (mode == "middle") {
			sp::popen proc1 ("xdotool", {"key", "Control_L+Left"});
			proc1.wait();
			sp::popen proc2 ("xdotool", {"key", "Control_L+Shift+Right"});
			proc2.wait();
		} else {
			// mode "end" (default)
			sp::popen proc ("xdotool", {"key", "Control_L+Shift+Left"});
			proc.wait();
		}

	};

	virtual std::string get_selected_word() {

		std::string curr_window = get_focused_window_id();
		sp::popen proc1 ("xdotool", {"windowactivate", curr_window});
		proc1.wait();

		std::string old_clipboard_text = get_clipboard_text();
		sp::popen proc2 ("xdotool", {"windowactivate", curr_window, "key", "--window", curr_window, "--clearmodifiers", "Control_L+c"});
		proc2.wait();

		std::string selected_word = get_clipboard_text();
		set_clipboard_text(old_clipboard_text);

		return selected_word;

	};

	virtual std::string get_focused_window_id() {

		sp::popen proc ("xdotool", {"getwindowfocus"});
		proc.wait();
		std::string stdout (std::istreambuf_iterator<char>(proc.stdout()), {});
		stdout.erase(stdout.find_last_not_of(" \n\r\t")+1);

		return stdout;

	};

	virtual int history_score(const std::string &text) {

		if (history.db.count(text) != 0) {
			return history.db[text].get<int>();
		} else {
			return 0;
		}

	}

	virtual void history_increment(const std::string &word) {

		if (history.db.count(word) != 0) {
			// cannot use direct ++ increment on json objs
			history.db[word] = history.db[word].get<int>() + 1;
			history.write();
		} else {
			// automatically add to custom_words
			custom_words.db[word] = word;
			custom_words.write();
		}

	};

	virtual void history_remove(const std::string &word) {

		if (history.db.count(word) != 0) {
			history.db.erase(word);
			history.write();
		}

	};

	virtual void ignore_list_add(const std::string &word) {

		ignore_list.db.push_back(word);
		ignore_list.write();

	};

	virtual std::string get_clipboard_text() {

		std::string text;
		clip::get_text(text);

		return text;

	};

	virtual void set_clipboard_text(const std::string &text) {
		
		clip::set_text(text);
	
	};

	virtual std::string determine_language_from_keyboard_layout() {
		
		std::map<std::string, std::string> layout_to_languages = {
			{"bd", "Bangla"}, {"us", "English"},
			{"uk", "English"}, {"gb", "English"},
			{"ara", "Arabic"}, {"cn", "Chinese"},
			{"tw", "Chinese"}, {"de", "German"},
			{"jp", "Japanese"}, {"ru", "Russian"},
			{"es", "Spanish"}, {"se", "Swedish"},
			{"fi", "Finnish"}, {"kr", "Korean"},
			{"pk", "Urdu"}, {"fr", "French"},
			{"gr", "Greek"}, {"ua", "Ukrainian"}
		};

		sp::popen proc ("setxkbmap", {"-print"});
		proc.wait();
		std::string stdout (std::istreambuf_iterator<char>(proc.stdout()), {});
		std::stringstream stdout_stream (stdout);

		std::string line;
		std::vector<std::string> line_split;
		std::string kbd_layout = "en";
		while (std::getline(stdout_stream, line, '\n')) {
			if (line.find("xkb_symbols") != std::string::npos) {
				line.erase(line.find_last_not_of(" \n\r\t")+1);
				line_split = utl::split(line, ' ');
				int pos = utl::index<std::string>(line_split, "include") + 1;
				if (pos >= line_split.size()) {
					// out of bounds (not found etc)
					continue; // skip this iteration
				}
				kbd_layout = utl::split(line_split[utl::index<std::string>(line_split, "include")], '+')[1];
			}
		}

		if (layout_to_languages.count(kbd_layout) != 0) {
			return layout_to_languages[kbd_layout];
		} else {
			std::cout << "Could not determine language from keyboard layout '" << kbd_layout << "'" << std::endl;
			std::cout << "    Defaulting to English" << std::endl;
			return "English";
		}

	};

private:
	
};