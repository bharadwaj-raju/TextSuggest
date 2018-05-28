#include <iostream>
#include <string>
#include <sstream>

#include "../../lib/subprocess.hpp"

namespace sp = subprocess;

int main(int argc, char ** argv) {
	
	std::vector<std::string> args(argv, argv+argc);

	std::string op = args[1];
	std::string text = args[2];

	if (op == "matches") {
		if (text.substr(0, 1) == "=") {
			return 0;
		} else {
			return 1;
		}
	} else if (op == "process") {
		text.erase(0, 1);
		std::string python_cmd = "from math import *;print(";
		python_cmd += text + ")";
		sp::popen proc ("python3", {"-c", python_cmd});
		std::cout << proc.stdout().rdbuf();
	}
	
	return 0;

}