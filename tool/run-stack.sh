#!/bin/bash

set -e

toolDir=$(cd `dirname ${BASH_SOURCE}`; pwd)

# initialize state file
STATE_FILE_NAME=_state.json
echo '{}' > ./${STATE_FILE_NAME}

prefix="_x"
processingStart=$(date +%FT%T)
python ${toolDir}/state_rw.py write ${prefix}_processing_start $processingStart

sh ${toolDir}/prepare_scenes.sh

source ${toolDir}/00-init.sh
source ${toolDir}/01-setup.sh

for x in \
02-get-slcs.sh \
03-get-dems.sh \
04-make-run-scripts.sh \
05-make-run-scripts.sh \
06-run-01.sh \
06-run-02-0.sh \
06-run-02-5.sh \
06-run-02-9.sh \
06-run-03.sh \
06-run-04.sh \
06-run-05.sh \
06-run-06.sh \
06-run-07.sh \
06-run-xx.sh

do
    echo "# Run sh ${toolDir}/${x}"
    sh ${toolDir}/${x}
done

export PROCESSING_START=$(python ${toolDir}/state_rw.py read ${prefix}_processing_start)

x=07-create-datasets.sh
echo "# Run sh ${toolDir}/${x}"
sh ${toolDir}/${x}
