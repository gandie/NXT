#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import BaseHTTPServer
import json
import cgi
import thread

from robo import ScoutRobo
from lib.nxt_player import Nxt_Player

HOST_NAME = ''
PORT_NUMBER = 14242

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        args = {}
        idx = s.path.find('?')
        if idx >= 0:
            rpath = s.path[:idx]
            args = cgi.parse_qs(s.path[idx+1:])
        else:
            rpath = s.path

        if 'nxt' in rpath:
            if 'command' in args.keys():
                command = args['command'][0]
                if 'ftime' in args.keys():
                    ftime = float(args['ftime'][0])
                if (command == 'go_forward'):
                    go_forward(ftime)
                    s.wfile.write("Done")
                    return
                elif command == 'go_backward':
                    go_backward(ftime)
                    s.wfile.write("Done")
                    return
                elif command == 'turn_left':
                    turn_left(ftime)
                    s.wfile.write("Done")
                    return
                elif command == 'turn_right':
                    turn_right(ftime)
                    s.wfile.write("Done")
                    return
                elif command == 'stop':
                    stop()
                    s.wfile.write("Done")
                elif command == 'go_forward_forever':
                    go_forward_forever()
                    s.wfile.write("Done")
                elif command == 'go_backward_forever':
                    go_backward_forever()
                    s.wfile.write("Done")
                elif command == 'turn_left_forever':
                    turn_left_forever()
                    s.wfile.write("Done")
                elif command == 'turn_right_forever':
                    turn_right_forever()
                    s.wfile.write("Done")
                elif command == 'unlock':
                    unlock()
                    s.wfile.write("Done")
                else:
                    s.wfile.write("Command not found.")
                    return


# commands
def go_forward(ftime):
    print("Go forward..")
    robo.go_forward(ftime = ftime)

def go_backward(ftime):
    print("Go back..")
    robo.go_backward(ftime = ftime)

def turn_left(ftime):
    print("Turn right..")
    robo.turn_left(ftime = ftime)

def turn_right(ftime):
    print("Turn left..")
    robo.turn_right(ftime = ftime)

def stop():
    print("Stopping...")
    robo.stop()

def go_forward_forever():
    print 'Going forward...'
    robo.go_forward_forever()

def go_backward_forever():
    print 'Going forward...'
    robo.go_backward_forever()

def turn_left_forever():
    print 'Turning right'
    robo.turn_left_forever()

def turn_right_forever():
    print 'Turning right'
    robo.turn_right_forever()

def unlock():
    print 'Unlocking...'
    robo.unlock()

def music():
    if not self.player.playing_song:
        number = random.randint(0, 400)
        if number == 88:
            thread.start_new_thread(self.player.play_song,())


# Startpunkt
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    robo = ScoutRobo(bluetooth_only = True)
    try:
        print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
