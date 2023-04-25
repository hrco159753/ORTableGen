#!/usr/bin/env bash

gnome-terminal -- bash -c "python3 -m http.server 8080 --cgi -d $( dirname $0 )"
gnome-terminal -- bash -c "python3 -m pyftpdlib -w -u user -P user -d $( dirname $0 )/res/ftp"

ip address show
python -c'import urllib.request as r
print("External IP:", r.urlopen("https://ident.me").read().decode("utf8"))'
