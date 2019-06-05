from flask import Flask
from flask import render_template
import subprocess
import random
import traceback
import socket
import time
app = Flask(__name__)

        

@app.route('/detect')
def detect(name=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    s.connect((getip(),8092))
    s.sendall(bytes("shock",'utf-8'))
    try:
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = s.recv(1024).decode()
            if not data:
                # if data is not received break

                break
            return data
    except Exception as e:
            print(e)
            traceback.print_exc()
                                                
                                                                        

@app.route('/')
def hello(name=None):
    lip = getip()
    sid = getSID()
    return render_template('index.html', ip=str(lip), sessionID=str(sid))


def getip():
    ip = subprocess.check_output("hostname -I", shell=True).decode('utf-8')  # get ip
    ip = ip[:-2]  # eliminate unwanted characters
    return ip


def getSID():
    return random.randint(0, 9223372036854775807)


@app.route('/accelerometer.html')
def accelo():
    sid = getSID()
    return render_template('accelerometer.html', ip=str(getip()), sessionID=str(sid))


@app.route('/joystick.html')
def joystick():
    sid = getSID()
    ip = getip()
    ws_url = "ws://%s:9998" % ip
    return render_template(
        'joystick.html',
        ip=ip,
        ws_url=ws_url,
        sessionID=str(sid)
    )


@app.route('/gamepad.html')
def gamepad():
    sid = getSID()
    ip = getip()
    ws_url = "ws://%s:9998" % ip
    return render_template(
        'gamepad.html',
        ip=ip,
        ws_url=ws_url,
        sessionID=str(sid)
    )
