#include <iostream>
#include <string>

#include <unistd.h>

#include <dbus-c++/dbus.h>

#include "../lib/cxxopts.hpp"

#include "../common.hpp"
#include "TextSuggestServer.cpp"


DBus::BusDispatcher dispatcher;

int main(int argc, char ** argv) {

	cxxopts::Options options ("TextSuggest", "TextSuggest — universal autocomplete  (Server)");

	options.add_options()
	("h,help", "Print help")
	("v,version", "Print version and license information")
	;

	auto result = options.parse(argc, (const char**&)argv);

	if (result.count("help")) {
		std::cout << SERVER_HELP_MESSAGE << std::endl;
		return 0;
	}

	if (result.count("version")) {
		std::cout << "TextSuggest release " << VERSION[0]<<"."<<VERSION[1]<<"."<<VERSION[2] 
				  << " (build "<<BUILD<<")" << std::endl << std::endl;
		std::cout << VERSION_MESSAGE << std::endl;
		return 0;
	}
	
	DBus::default_dispatcher = &dispatcher;
	DBus::Connection bus = DBus::Connection::SessionBus();

	bus.request_name(SERVICE_NAME);

	TextSuggestServer server (bus);

	std::cout << "Started server at " << SERVICE_NAME << ", PID: " << getpid() << std::endl;

	dispatcher.enter();

	return 0;

}