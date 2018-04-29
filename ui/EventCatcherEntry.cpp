#include "EventCatcherEntry.hpp"

EventCatcherEntry::EventCatcherEntry(QWidget * parent) {}

void EventCatcherEntry::setCallback(std::function<void (QKeyEvent e)> user_fn) {
	callback_fn = user_fn;
}

void EventCatcherEntry::keyPressEvent(QKeyEvent *event) {
	QLineEdit::keyPressEvent(event);
	callback_fn(*(event));
}

EventCatcherEntry::~EventCatcherEntry() {}