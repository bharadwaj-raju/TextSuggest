#ifndef EVENTCATCHERENTRY_H
#define EVENTCATCHERENTRY_H

#include <functional>

#include <QLineEdit>
#include <QKeyEvent>
#include <QWidget>

class EventCatcherEntry : public QLineEdit
{
	Q_OBJECT
public:
	explicit EventCatcherEntry(QWidget *parent = 0);
	~EventCatcherEntry();
	std::function<void (QKeyEvent)> callback_fn;
	void setCallback(std::function<void (QKeyEvent)> user_fn);

protected:
	virtual void keyPressEvent(QKeyEvent *event);

};

#endif // EVENTCATCHERENTRY_H