#!/usr/bin/env python

# WS client example

import random
import json
import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"type": "newGame", "winsNeeded": 3, "numPlayers": 3, "startingHandSize": 4}))

        while True:
            raw_payload = await websocket.recv()
            obj = json.loads(raw_payload)
            if "items" in obj:
                print("Incoming", json.dumps(json.loads(raw_payload), indent=4))
                print("")
                choice = random.randint(0, len(obj["items"])-1)
                answer = json.dumps({"type": "choice", "choice": choice})
                print("Answer", json.dumps(json.loads(answer), indent=4))
                print("")
                await websocket.send(answer)
                print("-"*80)
                print("")



asyncio.get_event_loop().run_until_complete(hello())
