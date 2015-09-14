#!/bin/sh

# Author: Jakub Svoboda
# License: To the extent possible under law, the person who associated CC0 with this work has waived all copyright and related or neighboring rights to this work.

# Converts cs_CZ.dic to list of nouns. Creates files nouns_all.txt and nouns.txt.
# You can get cs_CZ.dic by extracting dict-cs-2.0.oxt. You can get dict-cs-2.0.oxt from http://extensions.services.openoffice.org/en/project/czech-dictionary-pack-%C4%8Desk%C3%A9-slovn%C3%ADky under GNU GPL.

# http://www.davidpashley.com/articles/writing-robust-shell-scripts/
set -e 

# file name of cs_CZ.dic
CSCZDIC="cs_CZ.dic"

# check that CSCZDIC exists and exit if not
if [ ! -e "$CSCZDIC" ]; then
	echo >&2 "The $CSCZDIC file was not found. Aborting."
	exit 1
fi

# check that the shuf program is available
command -v shuf >/dev/null 2>&1 || { echo >&2 "The shuf program is required but is not available. Aborting."; exit 1; }

# get nouns from CSCZDIC
cat "$CSCZDIC" | grep "\/MQ\|\/S\|\/PV\|\/ZQ\|\/PI\|\/Z$\|\/UV\|\/Q$\|\/H$" | sed "s/\([^\/]*\).*/\1/g" | sed 's/.*/\L&/' > nouns_all.txt

# select random 15000 words so that the resulting word list is not too large
cat nouns_all.txt | shuf | head -n 15000 > nouns.txt

