import time
import asyncio
import websockets
import os
import json

robo = None

actSID = "localhost"
lastSeen = 0
delay = 200


async def runserver(websocket, path):
    global actSID
    global lastSeen
    assert robo, 'robo instance needed!'
    while True:
        data = await websocket.recv()

        print(data)
        try:
            allowed = False
            data_json = json.loads(data)
            tempSID = data_json['sid']
            forward = data_json['forward']
            turn = data_json['turn']
            sitetime = int(data_json['time'])
            comptime = time.time() * 1000
            tower = 0
            if actSID == "localhost" or lastSeen + 10 < time.time():
                print("new User")
                actSID = data_json['sid']
                lastSeen = time.time()
                allowed = True
            if lastSeen + 10 > time.time() and tempSID == actSID:
                if turn != 0 or forward != 0:
                    lastSeen = time.time()
                allowed = True
            if comptime < sitetime + abs(delay) and allowed:
                print("Moving allowed. Will call robo.move")
                robo.move(forward, turn, tower)
        except Exception as e:
            print("Exception: %s" % e)


def initwebserver(robo_inst, ip, port):

    global robo
    robo = robo_inst

    print("Webserver Initalizing")
    start_server = websockets.serve(runserver, str(ip), port)
    print("Webserver defined")
    asyncio.get_event_loop().run_until_complete(start_server)
    print("Webserver Eventloop set")
    asyncio.get_event_loop().run_forever()
