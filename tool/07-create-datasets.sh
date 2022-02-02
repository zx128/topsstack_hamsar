#!/bin/bash

set -e

echo "# Start $0"; date

# Publishing dataset after stack processor completes
#
#python ${PGE_BASE}/create_dataset.py -b "$MINLAT,$MAXLAT,$MINLON,$MAXLON"
python ${PGE_BASE}/make_dataset.py -b "$MINLAT $MAXLAT $MINLON $MAXLON"

date; echo "# End $0"
