#ifndef FILES_H
#define FILES_H

#include <string>
#include <vector>
#include <iostream>
#include <utility>

#include <cstdlib>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>

#include "Util.hpp"

class Files {

public:

	std::string home;
	std::string config_home;
	std::string config_dir;
	std::string dictionaries_dir;
	std::string runtime_dir;
	std::string custom_words_file;
	std::string history_file;
	std::string ignore_list_file;
	std::vector<std::string> processor_dirs;
	std::vector<std::pair<std::string, std::string>> dictionary_files;

	Files() {

		home = get_env_var("HOME");
		
		config_home = get_env_var("XDG_CONFIG_HOME");
		if (config_home == "") {
			config_home = path_join({home, ".config"});
		}

		config_dir = path_join({config_home, "textsuggest"});
		mkdir_p(config_dir);

		dictionaries_dir = "/usr/share/textsuggest/dictionaries";

		runtime_dir = get_env_var("XDG_RUNTIME_DIR");
		if (runtime_dir == "") {
			runtime_dir = get_env_var("TMPDIR");
			if (runtime_dir == "") {
				runtime_dir = "/var";
			}
		}
		runtime_dir = path_join({runtime_dir, "textsuggest"});
		mkdir_p(runtime_dir);

		custom_words_file = path_join({config_dir, "custom-words.json"});
		history_file = path_join({config_dir, "history.json"});
		ignore_list_file = path_join({config_dir, "ignore.json"});

		processor_dirs.push_back(path_join({config_dir, "processors"}));
		processor_dirs.push_back("/usr/share/textsuggest/processors");

		for (std::string dict_file : Files::list_dir(dictionaries_dir)) {
			std::pair<std::string, std::string> entry;
			entry = {utl::replace(dict_file, ".txt", ""), Files::path_join({dictionaries_dir, dict_file})};
			dictionary_files.push_back(entry);
		}
	
	};
	
	~Files() {};

	static std::string _path_join(std::string path1, std::string path2) {
		
		char sep = '/';
		
		if (path1 == "") {
			return path2;
		}
		
		if (path1[path1.length()-1] != sep) {
			return path1 + sep + path2;
		} else {
			return path1 + path2;
		}
	
	};

	static std::string path_join(std::initializer_list<std::string> paths) {

		/* Usage: path_join({path1, path2, ..., pathN}) */
		
		std::string result = "";
		
		for (std::string path : paths) {
			result = _path_join(result, path);
		}
		
		return result;
	
	};

	static std::vector<std::string> path_split(std::string str){
		
		std::string token = "/";
		bool slash_first_elem = (bool) (str.substr(0, 1) == token);
		bool rm_last_elem = (bool) (str.substr(str.length()-1) == token);
		std::vector<std::string> result;
	   
		while (str.size()) {
			int index = str.find(token);
			if (index != std::string::npos) {
				result.push_back(str.substr(0, index));
				str = str.substr(index+token.size());
				if (str.size() == 0) {
					result.push_back(str);
				}
			} else {
				result.push_back(str);
				str = "";
			}
		}

		if (slash_first_elem) {
			result[0] = "/" + result[0];
		}

		if (rm_last_elem) {
			result.erase(result.begin()+result.size()-1);
		}

		return result;
	
	};

	static void mkdir_p(std::string path) {

		/* Like "mkdir -p" -- makes all intermediate-level directories 
		   needed to contain the leaf directory. */
		
		std::vector<std::string> split_path = path_split(path);
		std::string done_path;
		
		for (std::string path_seg : split_path) {
			
			std::string full_path_seg = path_join({done_path, path_seg});
			
			if (! exists(full_path_seg)) {
				mkdir(full_path_seg.c_str(), S_IRWXU);
			}
			
			done_path = path_join({done_path, path_seg});
		
		}
	
	};

	static std::vector<std::string> list_dir(std::string dirname) {
		
		std::vector<std::string> listing;
		
		DIR * dp;
		struct dirent * ep;
		dp = opendir(dirname.c_str());
		
		if (dp != NULL) {
			while ((ep = readdir(dp))) {
				std::string name (ep->d_name);
				if ((name != ".") && (name != "..")) {
					listing.push_back(name);
				}
			}
			(void) closedir(dp);
		}
		
		return listing;
	
	};

	static bool exists(std::string fname) {
		struct stat buffer;
		return (stat(fname.c_str(), &buffer) == 0);
	};

	static std::string get_env_var(std::string varname) {
		// sane getenv
		char * env = getenv(varname.c_str());
		if (env != NULL) {
			return std::string (env);
		} else {
			return "";
		}
	};

};

#endif // FILES_H