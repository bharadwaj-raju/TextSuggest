#include "TextSuggestApp.hpp"


TextSuggestApp::TextSuggestApp(int &argc, char ** argv, TextSuggestServerIFace * server,
	std::string tmp_word, bool opt_history, std::vector<std::string> tmp_languages,
	bool opt_auto_detect_language, bool tmp_selection, std::string opt_auto_selection,
	bool opt_custom_words_only, bool opt_processing)
: QApplication(argc, argv), currentlySelectedIndex(0, 0) {

	this->server = server;

	std::string opt_word = "";
	bool opt_selection = false;

	opt_selection = (bool) tmp_selection;
	opt_word = std::string(tmp_word);
	std::vector<std::string> opt_languages (tmp_languages);

	this->opt_history = opt_history;
	this->opt_processing = opt_processing;

	if (opt_auto_selection != "none") {
		server->autoselect_current_word(opt_auto_selection);
		opt_selection = true;
	}

	if (opt_selection) {
		opt_word = server->get_selected_word();
	}

	if (opt_word != "") {
		if (opt_custom_words_only) {
			allWords = server->get_custom_words_only(opt_word);
		} else {
			allWords = server->get_suggestions(opt_word, opt_languages);
		}
	} else {
		if (opt_custom_words_only) {
			allWords = server->get_custom_words_only("");
		} else {
			allWords = server->get_all_words(opt_languages);
		}
	}

	if (opt_auto_detect_language) {
		opt_languages.clear();
		opt_languages.push_back(server->determine_language_from_keyboard_layout());
	}

}

void TextSuggestApp::loadUI() {
	
	window = new QMainWindow();
	
	window->setWindowFlags(window->windowFlags() | Qt::Tool | Qt::FramelessWindowHint | Qt::Popup);
	
	mainWidget = new QWidget();
	layout = new QVBoxLayout();
	layout->setContentsMargins(0, 0, 0, 0);
	layout->setSpacing(0);
	mainWidget->setContentsMargins(0, 0, 0, 0);
	window->setContentsMargins(0, 0, 0, 0);

	timer = new QTimer();
	timer->setSingleShot(true);
	connect(timer, &QTimer::timeout, this, &TextSuggestApp::filterSuggestions);
	//timer.timeout.connect(filterSuggestions);


	// The timer provides a delay of 200ms between user typing and list filtering

	entry = new EventCatcherEntry();
	entry->setCallback([&](QKeyEvent event) { this->keyEventCatcher(event); });
	connect(entry, &EventCatcherEntry::textEdited, this, &TextSuggestApp::textEdited);
	layout->addWidget(entry);

	suggestionList = new QListWidget();
	suggestionList->setSortingEnabled(false);
	layout->addWidget(suggestionList);

	populateSuggestions(allWords);

	layout->setSizeConstraint(QLayout::SetFixedSize);
	mainWidget->setLayout(layout);
	window->setCentralWidget(mainWidget);

}

void TextSuggestApp::showUI() {
	window->show();
	window->raise();
	window->activateWindow();
}

void TextSuggestApp::keyEventCatcher(QKeyEvent e) {
	
	int key = e.key();
	Qt::KeyboardModifiers modifiers = e.modifiers();

	if (key == Qt::Key_Escape) {
		quit();
	}

	if (key == Qt::Key_Down) {
		currentlySelectedIndex.set(currentlySelectedIndex.get() + 1);
		suggestionList->setCurrentRow(currentlySelectedIndex.get());
		entry->setText(suggestionList->currentItem()->text());
	}

	if (key == Qt::Key_Up) {
		currentlySelectedIndex.set(currentlySelectedIndex.get() - 1);
		suggestionList->setCurrentRow(currentlySelectedIndex.get());
		entry->setText(suggestionList->currentItem()->text());
	}

	if (key == Qt::Key_Enter || key == Qt::Key_Return) {
		applySuggestion();
	}

	if (key == Qt::Key_Delete) {
		if ((modifiers & Qt::ShiftModifier) && (modifiers & Qt::ControlModifier)) {
			// Ctrl+Shift+Delete
			addSuggestionToIgnoreList();
		}
		
		if (modifiers & Qt::ShiftModifier) {
			//Shift+Delete
			removeSuggestionFromHistory();
		}
	}

}

void TextSuggestApp::textEdited(const QString &text) {
	timer->start(TYPE_SUGGEST_DELAY);
}

void TextSuggestApp::populateSuggestions(std::vector<std::string> suggestions) {

		suggestionList->clear();

		for (std::string &x : suggestions) {
			suggestionList->addItem(QString::fromStdString(x));
			//QListWidgetItem(QString::fromStdString(x), suggestionList);
		}

		currentlySelectedIndex.setMax(suggestions.size());
		currentlySelectedIndex.set(0);
		suggestionList->setCurrentRow(0);

}

void TextSuggestApp::filterSuggestions() {
	
	std::string text = entry->text().toStdString();
	if (text == "") {
		populateSuggestions(allWords);
	} else {
		if (opt_custom_words_only) {
			populateSuggestions(server->get_custom_words_only(text));
		} else {
			populateSuggestions(server->get_suggestions(text, opt_languages));
		}
	}

}

std::string TextSuggestApp::getCurrentSuggestion() {
	
	if (suggestionList->currentItem()) {
		return entry->text().toStdString();
	} else {
		return suggestionList->currentItem()->text().toStdString();
	}

}

void TextSuggestApp::applySuggestion() {

	window->hide();

	std::string text = getCurrentSuggestion();

	if (text == "") {
		quit();
	}
	
	if (opt_history) {
		server->history_increment(text);
	}

	std::cout << opt_processing;
	
	if (opt_processing) {
		text = server->process_suggestion(text);
	}
	
	server->type_text(text);
	server->reload_configs();

	quit();

}

void TextSuggestApp::removeSuggestionFromHistory() {
	server->history_remove(getCurrentSuggestion());
}

void TextSuggestApp::addSuggestionToIgnoreList() {	
	server->add_to_ignore_list(getCurrentSuggestion());
}

TextSuggestApp::~TextSuggestApp() {}