# Contributing to TextSuggest

## Reporting issues, bugs or feature requests

**Please use the *latest* version.** It is likely that the issue has already been fixed. You can download it [here](https://github.com/bharadwaj-raju/TextSuggest/archive/master.zip).

If it *hasn't* been fixed yet, please report it and include the following:

- Your desktop environment
- Your keyboard layout (US, UK, Arabic, Spanish, etc.)

If you're reporting a bug, include:

- What input triggers it?
- What was expected?
- What happened instead?
- What are the options used?
- The *complete* output of running it on the command line

## Development

Do you want to contribute code?

NOTE: The place where most development is needed is [textsuggestd](https://github.com/bharadwaj-raju/TextSuggest#textsuggestd).

Please read the following:

### Code style

Mostly follows [PEP8](https://pep8.org/) but a few exceptions:

- Use tabs. Not spaces. Tabs, as in `\t`.


### Structure

TextSuggest's flow is simple:

- Get a word (through `--word` or selection) (or no words, as with `--all-words`)
- Get matching words from `/usr/share/textsuggest/dictionaries`
- Display a menu of the words using Rofi
- Process the choice (more: [Processors](https://github.com/bharadwaj-raju/TextSuggest#extensions))
- Type it out

TextSuggest is mostly a convenience layer over these processes.

The `main()` function delegates this work to `get_suggestions()`, `display_menu()`, `process_suggestion()` and `type_text()`.
