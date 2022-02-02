#!/bin/bash

set -e

echo "# Start $0"; date

## STEP 3 ##
start=`date +%s`
echo "cat run_files/run_03_average_baseline | parallel ${gnuParallelOptions}"
cat run_files/run_03_average_baseline | parallel ${gnuParallelOptions}
end=`date +%s`
runtime3=$((end-start))
echo $runtime3

date; echo "# End $0"
