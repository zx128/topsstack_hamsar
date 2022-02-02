#!/bin/bash

set -e

echo "# Start $0"; date

toolDir=$(cd `dirname ${BASH_SOURCE}`; pwd)
python ${toolDir}/prepare_scenes.py

sceneDirName=scenes

if [ ! -d ./${sceneDirName} ]; then
    echo dir ./${sceneDirName} does not exist. quit.
    exit -1
fi

# if ./scenes is created by prepare_scenes.py
echo "symlink each scene dir from ${sceneDirName} to current dir"
ln -sfv ./${sceneDirName}/* .

date; echo "# End $0"
