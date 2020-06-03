import random
import collections
import json
import asyncio
import websockets

random.seed(1)

from board import Board
from player import Player
from cards.cards import read_cards
from log import new_logger
from logo import print_logo


NUMBER_OF_WINNING_ROUNDS_NEEDED = 3
NUMBER_OF_PLAYERS = 4
STARTING_HAND_SIZE = NUMBER_OF_WINNING_ROUNDS_NEEDED + 1
LIBRARY_PATH = "./cards/cards.json"
NEW_GAME_ACTION = "new_game"


def init_game() -> Board:
    deck = read_cards(LIBRARY_PATH)
    board = Board(
        deck,
        number_of_players=NUMBER_OF_PLAYERS,
        starting_hand_size=STARTING_HAND_SIZE,
        wins_needed=NUMBER_OF_WINNING_ROUNDS_NEEDED,
    )
    board.randomly_assign_pole()
    board.shuffle_deck()
    board.deal_cards()

    return board


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, collections.deque):
            return list(o)
        if isinstance(o, Board):
            return o.serialize()
        if isinstance(o, Player):
            return o.serialize()
        return o.__dict__


def error(es: str) -> str:
    return json.dumps({"error": es})


def main():
    print_logo()
    BOARDS = {}
    LOGGER = new_logger("joerg")

    async def new_game(websocket, payload):
        board = init_game()
        board_id = random.randint(0, 100)
        BOARDS[board_id] = board
        LOGGER.info(f"Board {board_id} created!")
        await websocket.send(
            json.dumps(
                {"type": "board", "board_id": board_id, "board": board}, cls=MyEncoder
            )
        )

    async def hello(websocket, path):
        LOGGER.info(f"{websocket._host}: Connected!")
        while True:
            try:
                raw_payload = await websocket.recv()
            except websockets.exceptions.ConnectionClosedOK:
                LOGGER.info(f"{websocket._host}: left")
                break
            except websockets.exceptions.ConnectionClosedError:
                LOGGER.info(f"{websocket._host}: left")
                break

            try:
                payload = json.loads(raw_payload)
            except json.decoder.JSONDecodeError as jde:
                msg = f"! Malformed request: {jde}"
                LOGGER.info(msg)
                await websocket.send(error(msg))
                continue

            if not isinstance(payload, dict):
                msg = "! Malformed request, payload must be json object"
                LOGGER.info(msg)
                await websocket.send(error(msg))
                continue

            if "type" not in payload:
                msg = "! Missing key `type` in JSON payload"
                await websocket.send(error(msg))
                continue

            LOGGER.info(f"< {payload}")

            payload_type = payload["type"]
            LOGGER.info(f"New incoming payload: {payload_type}")
            if payload_type == NEW_GAME_ACTION:
                LOGGER.info("Here!")
                await new_game(websocket, payload)
                continue

            await websocket.send(
                json.dumps({"message": "type queried not yet implemented."})
            )

    start_server = websockets.serve(hello, "192.168.1.109", 8000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
