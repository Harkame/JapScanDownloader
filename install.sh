#!/bin/bash

REPOSRC="https://github.com/VeNoMouS/cloudflare-scrape-js2py.git"
LOCALREPO="cloudflare-scrape-js2py"

git clone "$REPOSRC" "$LOCALREPO" 2> /dev/null || (cd "$LOCALREPO" ; git pull)

cd $LOCALREPO

python setup.py install

cd ..

pip install -r requirements.txt
