import time
import asyncio
import websockets
import os
import json

robot = 0

actSID = "localhost"
lastSeen = 0


async def hello(websocket, path):
    global actSID
    global lastSeen
    while True:
        name = await websocket.recv()

        print (name)
        try:
            allowed = False
            data_json = json.loads(name)
            tempSID = data_json['sid']
            forward = 0.02 * int(data_json['forward'])
            turn = 0.02 * int(data_json['turn'])
            sitetime = int(data_json['time'])
            if actSID == "localhost" or lastSeen + 10 < time.time():
                print("new User")
                actSID = data_json['sid']
                lastSeen = time.time()
                allowed = True
            if lastSeen + 10 > time.time() and tempSID == actSID:
                if turn != 0 or forward != 0:
                    lastSeen = time.time()
                allowed = True
            forward = 0.02 * int(data_json['forward'])
            turn = 0.02 * int(data_json['turn'])
            sitetime = int(data_json['time'])
            tower = 0
            comptime = time.time() * 1000
            if comptime < sitetime + abs(delay) and allowed:
                print ("Moving")
                robo.move(forward, turn, tower)
        except Exception:
            data_json = json.loads(name)
            print("except")


def initwebserver(robo, actSID, lastSeen, ip, port):
    print("Webserver Initalizing")
    start_server = websockets.serve(hello, str(ip), port)
    print("Webserver defined")
    asyncio.get_event_loop().run_until_complete(start_server)
    print("Webserver Eventloop set")
    asyncio.get_event_loop().run_forever()
