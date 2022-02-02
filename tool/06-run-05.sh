#!/bin/bash

set -e

echo "# Start $0"; date

## STEP 5 ##
start=`date +%s`
echo "cat run_files/run_05_fullBurst_resample  | parallel ${gnuParallelOptions}"
cat run_files/run_05_fullBurst_resample  | parallel ${gnuParallelOptions}
end=`date +%s`
runtime5=$((end-start))
echo $runtime5

date; echo "# End $0"
