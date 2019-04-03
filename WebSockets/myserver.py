#!/usr/bin/env python

import asyncio
import websockets
import time
import json

async def hello(websocket, path):
    while True:
        name = await websocket.recv()
        print(f"< {name}")

        # time.sleep(5)
        try:
            print(json.loads(name))
        except:
            pass
        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        print(f"> {greeting}")

start_server = websockets.serve(hello, 'localhost', 9998)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
