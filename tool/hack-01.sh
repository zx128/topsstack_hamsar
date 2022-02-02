#!/bin/bash

set -e

# amend _context.json
pgeBase=$(cd `dirname ${BASH_SOURCE}`; pwd)
python ${pgeBase}/amend_context.py

# download slcs
mkdir -p ./slcs

aws s3 sync s3://soamc-dev-lts-fwd/products/xing/test/slcs/S1A_IW_SLC__1SDV_20201005T233859_20201005T233926_034668_0409B0_2533 ./slcs/S1A_IW_SLC__1SDV_20201005T233859_20201005T233926_034668_0409B0_2533
aws s3 sync s3://soamc-dev-lts-fwd/products/xing/test/slcs/S1A_IW_SLC__1SDV_20201017T233859_20201017T233926_034843_040FD4_E029 ./slcs/S1A_IW_SLC__1SDV_20201017T233859_20201017T233926_034843_040FD4_E029

ln -sf ./slcs/* .

mkdir -p ./zip
cd ./zip
ln -sf ../slcs/*/*.zip .
