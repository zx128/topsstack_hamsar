#!/bin/bash

set -e

echo "# Start $0"; date

sceneDirName=scenes

echo "create dir ./zip and symlink *.zip from ${sceneDirName} to it"
mkdir -p ./zip
cd ./zip
ln -sfv ../${sceneDirName}/*/*.zip .

date; echo "# End $0"
