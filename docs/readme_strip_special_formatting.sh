#!/bin/sh

# Strip README.md of special formatting used to make it look nice online.

perl -pe 's/\(.*\)|\[|\]//g' < README.md |  perl -pe 's/<.*> //g' | perl -pe 's/!Arch Linux |!Ubuntu //g'
