#ifndef PROCESSORS_H
#define PROCESSORS_H

#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <fstream>

#include <cstdlib>
#include <sys/stat.h>
#include <sys/types.h>

#include "Files.hpp"
#include "../lib/subprocess.hpp"

namespace sp = subprocess;

namespace Processors {

std::map<std::string, std::string> find_processors() {

	Files files = Files();
	
	std::map<std::string, std::string> processors;

	for (std::string processor_dir : files.processor_dirs) {
		for (std::string processor_file : Files::list_dir(processor_dir)) {
			if (processors.find(processor_file) == processors.end()) {
				/* Files::processor_dirs is in order of preference
		   	   	   so if a certain processor is "provided" by a file 
		      	   located in a dir which comes earlier in processor_dirs
		      	   it will be taken instead of later ones with the same name
		      	*/
		      	std::string full_path = Files::path_join({processor_dir, processor_file});
				struct stat file_stat;
				if (stat(full_path.c_str(), &file_stat) == 0 && file_stat.st_mode & S_IXUSR) {
					// is file executable?
					//processors.insert(std::pair<std::string, std::string>(
					//	processor_file, Files::path_join({processor_dir, processor_file})));
					processors[processor_file] = full_path;
				}
			}
		}
	}

	return processors;

}

bool matches(std::string processor_file, std::string text) {

	sp::popen proc (processor_file, {"matches", text});
	int retcode = proc.wait();
	return (retcode == 0);

}

std::string process(std::string processor_file, std::string text) {

	sp::popen proc (processor_file, {"process", text});
	std::string result (std::istreambuf_iterator<char>(proc.stdout()), {});

	if (result.substr(result.length()-1, result.length()) == "\n") {
		result.pop_back();
	}

	return result;
}

}

#endif // PROCESSORS_H