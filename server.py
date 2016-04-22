#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import BaseHTTPServer
import json
import cgi

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
                ftime = float(args['ftime'][0])
                print("#####################################################------------")
                print command
                print ftime
                if (command == 'go_forward'):
                    s.wfile.write("Vorwaerts fahren..")
                    music()
                    go_forward(ftime)
                    return
                elif command == 'go_backward':
                	s.wfile.write("Rueckwaerts fahren..")
                	go_backward(ftime)
                	return
                elif command == 'turn_left':
                    s.wfile.write("Links drehen..")
                    turn_left(ftime)
                    return
                elif command == 'turn_right':
                	s.wfile.write("Rechts drehen..")
                	turn_right(ftime)
                	return
                else:
                    s.wfile.write("Das dumm.")
                    return

        s.wfile.write("Argumente unbekannt \
					<form action='nxt' method='get'> \
                        <input type='text' name='command' placeholder='Befehl'>\
                        <input type='text' name='ftime' placeholder='Zeit[s]'>\
                        <input type='submit' value='Abschicken'>\
                    </form>")


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

def music():
    if not self.player.playing_song:
        number = random.randint(0, 400)
        if number == 88:
            thread.start_new_thread(self.player.play_song,())


# Startpunkt
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    robo = ScoutRobo()
    try:
        print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
