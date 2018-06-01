#ifndef DATABASE_H
#define DATABASE_H

#include <iostream>
#include <fstream>
#include <string>
#include <map>

#include "../lib/json.hpp"

using json = nlohmann::json;

class JSONDataBase {
public:
	JSONDataBase() {};
	~JSONDataBase() {};

	std::string fname;
	json db = {};

	void load(std::string fname) {
		
		this->fname = fname;
		
		std::ifstream file (fname);
		
		if (file.good()) {
			db = json::parse(file);
		} else {
			std::cout << "File '" << fname << "' does not exist or is inaccessible!" << std::endl;
			std::cout << "    Creating empty '" << fname << "'." << std::endl;
			db = json::parse("{}");
			write();	
		}

		file.close();

	};

	void write() {
		
		std::ofstream file;
		
		file.open(fname, std::ofstream::out | std::ofstream::trunc);
		file << db.dump(4);

		file.close();
		
	};

};

#endif // DATABASE_H