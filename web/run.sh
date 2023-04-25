#!/usr/bin/env bash

BASE_DIR=$( dirname $( readlink -f "${BASH_SOURCE:-$0}" ) )
echo ${BASE_DIR}
cd ${BASE_DIR}

gnome-terminal -- bash -c "echo ${BASE_DIR}; python3 -m http.server 8080 --directory ${BASE_DIR} --cgi"
gnome-terminal -- bash -c "python3 -m pyftpdlib -w -u user -P user -d ${BASE_DIR}/res/ftp"

ip address show
python -c'import urllib.request as r
print("External IP:", r.urlopen("https://ident.me").read().decode("utf8"))'

cd -