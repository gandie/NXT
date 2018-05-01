# Installation

-Download bluetooth driver header files (to compile python bluetooth bindings)
-Create virtualenv
-Install last stable release of nxt python bindings into virtualenv
-Keep the releasse for possible modifications
-Install rest of the requirements into virtualenv via pip
-Install this python module into virtualenv

Somehting like this in bash (not yet tested!):
```
sudo apt-get install libbluetooth-dev
virtualenv -p python2 venv2
. ./venv2/bin/activate
wget https://github.com/Eelviny/nxt-python/archive/v2.2.2.zip
unzip v2.2.2.zip
python nxt-python-2.2.2/setup.py install
pip install -r requirements.txt
python setup.py install
```

Modify motor.py of this driver (nxt-python-2.2.2) to achieve higher accuracy
using bluetooth.

# Bluetooth Pairing

Kudos to FancyChaos for the awesome nxt_pair module doing all the work!
