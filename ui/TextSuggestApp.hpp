#ifndef TEXTSUGGESTAPP_H
#define TEXTSUGGESTAPP_H

#include <vector>
#include <string>

// NOTE: One *must* include DBus *before* the Qt libraries
// The following header includes in turn the DBus header
#include "TextSuggestServerIFace.hpp"

#include <QApplication>
#include <QMainWindow>
#include <QWidget>
#include <QKeyEvent>
#include <QTimer>
#include <QVBoxLayout>
#include <QListWidget>
#include <QListWidgetItem>
#include <QString>

#include "EventCatcherEntry.hpp"
#include "Index.hpp"

#define TYPE_SUGGEST_DELAY 200

class TextSuggestApp : public QApplication
{
	Q_OBJECT
public:
	explicit TextSuggestApp(int &argc, char ** argv, TextSuggestServerIFace * server,
		std::string tmp_word, bool opt_history, std::vector<std::string> tmp_languages,
		bool opt_auto_detect_language, bool tmp_selection, std::string opt_auto_selection,
		bool opt_custom_words_only, bool opt_processing);
	~TextSuggestApp();
	void loadUI();
	void showUI();

protected:

private:
	void populateSuggestions(std::vector<std::string> suggestions);
	void filterSuggestions();
	std::string getCurrentSuggestion();
	void applySuggestion();
	void removeSuggestionFromHistory();
	void addSuggestionToIgnoreList();
	void textEdited(const QString &text);
	void keyEventCatcher(QKeyEvent event);
	void adjustSizes();
	
	TextSuggestServerIFace * server;
	Index currentlySelectedIndex;
	std::vector<std::string> allWords;
	
	std::string opt_word;
	bool opt_history;
	std::vector<std::string> opt_languages;
	bool opt_auto_detect_language;
	bool opt_selection;
	bool opt_auto_selection;
	bool opt_custom_words_only;
	bool opt_processing;
	
	QMainWindow * window;
	QWidget * mainWidget;
	QVBoxLayout * layout;
	QTimer * timer;
	QListWidget * suggestionList;
	EventCatcherEntry * entry;

};

#endif // TEXTSUGGESTAPP_H