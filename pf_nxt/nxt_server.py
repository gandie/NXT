import socket
import json


class NxtServer(object):
    '''
    Simple server receiving JSON data to control robot via UDP
    '''
    def __init__(self, robo, ip='0.0.0.0', port=14242):
        self.ip = ip
        self.port = int(port)
        self.robo = robo
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM  # UDP
        )
        self.sock.bind((self.ip, self.port))

    def run(self):
        print('Starting main loop')
        while True:
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            print('received')
            try:
                data_json = json.loads(data)
                forward = data_json['forward']
                turn = data_json['turn']
                print('Got valid data, moving...', data_json)
                self.robo.move(forward, turn)
            except Exception as e:
                print('bad data or something', data)
                print(e)
