#!/bin/sh

# Generate groff manpage from markdown

curl -F page=@docs/textsuggest.1.md http://mantastic.herokuapp.com 2>/dev/null
