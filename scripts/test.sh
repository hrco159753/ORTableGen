#!/usr/bin/env bash

BASE_DIR=$( dirname $( readlink -f "${BASH_SOURCE:-$0}" ) )

cd ${BASE_DIR}/..

python -m venv env
source env/bin/activate
pip install -r requirements.txt

rm -rf build && \
mkdir build && \
./src/orgen.py gengcpname -n 7 | ./src/orgen.py gengcp -o build/gcp.json && \
./src/orgen.py gengcplabel -i build/gcp.json -o build/labels.pdf && \
./src/orgen.py genteam -i web/res/ftp/teamNames.txt -o build/teams.json && \
./src/orgen.py gencp -igcp build/gcp.json -igcpa res/tmp_ex.gpx -o build/cps.json && \
./src/orgen.py genacqtable -icp build/cps.json -it build/teams.json -o build/acqtable.pdf && \
./src/orgen.py genworkbook -icp build/cps.json -it build/teams.json -o build/ORWorkbook.xls -map 10

deactivate

cd -