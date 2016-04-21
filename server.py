import time
import BaseHTTPServer
import json
import cgi

from robo import ScoutRobo

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
                print command
                if command == 'go':
                    s.wfile.write("Fahre...")
                    test_robo()
                    return
                else:
                    s.wfile.write("Das dumm.")
                    return

        s.wfile.write("Nein.")

def test_robo():
    print 'testing...'
    robo.go_forward(ftime = 1)

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
