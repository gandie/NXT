#!/bin/bash
set -e
virtualenv -p python3 venv3
. ./venv3/bin/activate
wget https://github.com/Eelviny/nxt-python/archive/master.zip
unzip master.zip
cd nxt-python-master
python3 setup.py install
cd ..
pip install -r requirements.txt
python3 setup.py install
cd pf_nxt/website
chmod +x run_flaskapp.sh
cd ..
cd ..
