# NXT

Python Code to control a Lego NXT robot using various devices and technologies.

Featured ways to control robot:
+ Directly using gamepad
+ Gamepad via UDP server
+ HTTP based remote control
+ Flask based webinterface (Accelerometer and VirtualJoystick.js)

# Installation

## Beginners Guide

+ Download repo

```
git clone https://github.com/gandie/NXT
```

+ open Terminal in Repo

```
chmod +x build_env.sh
./build_env.sh
. ./venv3/bin/activate
```

Then you can start the Script with:

### Online version

```
nxt_start_server -w
```

Then open in your Webbrowser localhost:5000 and press Create Websocket


### Gamepad Version

If you want to use a PS3 Controller you can use the Command:

```
nxt_direct -m bluetooth -g
```

## Not recommended, only for advanced Users

+ Download bluetooth driver header files (to compile python bluetooth bindings)
+ Create virtualenv
+ Install last stable release of nxt python bindings into virtualenv
+ Keep the releasse for possible modifications
+ Install rest of the requirements into virtualenv via pip
+ Install this python module into virtualenv

Something like this in bash (not yet tested!):
```
sudo apt-get install libbluetooth-dev python-virtualenv
virtualenv -p python3 venv3
. ./venv3/bin/activate
wget https://github.com/bene017/nxt-python/archive/master.zip
unzip master.zip
cd nxt-python-master
python3 setup.py install
cd ..
pip3 install -r requirements.txt
python3 setup.py install
cd pf_nxt/website
chmod +x bash.sh
cd ../..
```

USB-Setup (udev-rule) and more:
https://github.com/Eelviny/nxt-python/wiki/Installation

Modify motor.py of this driver (nxt-python-2.2.2) to achieve higher accuracy
using bluetooth.

Test if everything works fine, from inside the repository:
```
nxt_direct -m bluetooth -g
```

Read the text from the console and follow instructions to continue.

###### Kudos to @FancyChaos for the awesome nxt_pair module doing all the work!
###### Kudos to @MagnusM1709 && @bene017 Max Starke for working Websocket!
