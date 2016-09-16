#!/bin/sh

# Strip README.md of special formatting used to make it look nice online.

cat README.md | perl -pe 's/\(.*\)|\[|\]//g' |  perl -pe 's/<.*> //g' | perl -pe 's/!Arch Linux |!Ubuntu //g'
