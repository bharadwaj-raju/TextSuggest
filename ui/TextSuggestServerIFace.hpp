#ifndef TEXTSUGGESTSERVERIFACE_H
#define TEXTSUGGESTSERVERIFACE_H

#include <dbus-c++/dbus.h>
#include "dbus-interface.hpp"

class TextSuggestServerIFace
: public org::textsuggest::server_proxy,
  public DBus::IntrospectableProxy,
  public DBus::ObjectProxy
{
	public:
		TextSuggestServerIFace(DBus::Connection &connection, const char * path, const char * name)
			: DBus::ObjectProxy(connection, path, name) {

			};
};

#endif // TEXTSUGGESTSERVERIFACE_H