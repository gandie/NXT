import socket
import RPi.GPIO as GPIO
import subprocess
import json
import traceback
from threading import Thread

def getip():
        ip = subprocess.check_output("hostname -I", shell=True).decode('utf-8')  # get ip
        ip = ip[:-2]  # eliminate unwanted characters
        return ip

def server_program():
        # get the hostname
        host = getip()
        port = 8092  # initiate port no above 1024
        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        print("listening on: {0}:{1}".format(host,port))
        server_socket.bind((host, port))  # bind host address and port together
        # configure how many client the server can listen simultaneously
        server_socket.listen(3)
        while True:
            conn, address = server_socket.accept()  # accept new connection
            print("Connection from: " + str(address))
            t = Thread(target=listen, args=(conn,))
            t.start()

def listen(conn):
        try:
            while True:
                # receive data stream. it won't accept data packet greater than 1024 bytes
                data = conn.recv(1024).decode()
                if not data:
                    # if data is not received break
                    break
                print("from connected user: " + str(data))
                data =  json.dumps(shocksDetect)
                conn.send(bytes(data,'utf-8'))  # send data to the client
        
        except Exception as e:
            conn.close()  # close the connection
            print(e)
            traceback.print_exc()
        conn.close()  # close the connection



shock = 33
GPIO.setmode(GPIO.BOARD)

GPIO.setup(shock, GPIO.IN, pull_up_down=GPIO.PUD_UP)

shocksDetect = 0

def p(ev=None):
        global shocksDetect
        shocksDetect +=1
        print("detect")

GPIO.add_event_detect(shock, GPIO.FALLING, callback=p, bouncetime=200) # wait for falling
server_program()
        
