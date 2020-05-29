import random
import collections
import json
random.seed(1)

from uuid import uuid4
from typing import Dict, Any

from board import Board
from cards.cards import read_cards
from log import new_logger
from logo import print_logo
from order import Order

from flask import Flask, abort, jsonify, request

NUMBER_OF_WINNING_ROUNDS_NEEDED = 3
NUMBER_OF_PLAYERS = 4
STARTING_HAND_SIZE = NUMBER_OF_WINNING_ROUNDS_NEEDED + 1
LIBRARY_PATH = "./cards/cards.json"


# def main(analysis_file_path=None, port=4747):
#     print_logo()
#     LOGGER = new_logger("joerg")

#     app = Flask(__name__)
#     boards: Dict[str, Board] = {}

#     @app.route("/")
#     def serve_root():
#         return "asdf"

#     @app.errorhandler(400)
#     def resource_not_found(e):
#         return jsonify(error=str(e)), 400

#     @app.route('/new-game', methods=['GET', 'POST'])
#     def start_game():
#         new_game_settings: Dict[Any, Any] = request.get_json()
#         if not new_game_settings:
#             new_game_settings = {}

#         number_of_players = new_game_settings.get("number_of_players", NUMBER_OF_PLAYERS)
#         starting_hand_size = new_game_settings.get("starting_hand_size", STARTING_HAND_SIZE)
#         wins_needed = new_game_settings.get("wins_needed", NUMBER_OF_WINNING_ROUNDS_NEEDED)

#         print(new_game_settings)
#         print(number_of_players, starting_hand_size, wins_needed)

#         deck = read_cards(LIBRARY_PATH)
#         board = Board(
#             deck,
#             number_of_players=number_of_players,
#             starting_hand_size=starting_hand_size,
#             wins_needed=wins_needed,
#         )

#         board.randomly_assign_pole()
#         board.shuffle_deck()
#         board.deal_cards()

#         board_id = str(random.randint(0, 100))
#         boards[board_id] = board

#         return board_id

#     @app.route("/begin-round/<board_id>")
#     def begin_round(board_id: str):
#         if board_id not in boards:
#             abort(400, description=f"Unknown board_id: {board_id}")

#         board: Board = boards[board_id]
#         board.begin_round()
#         return "Round begun"

#     @app.route("/player-hand/<board_id>/<int:player_num>")
#     def show_player_hand(board_id: str, player_num: int):
#         if board_id not in boards:
#             abort(400, description=f"Unknown board_id: {board_id}")
#         board: Board = boards[board_id]

#         player = board.players[player_num]
#         return {
#             "card_states": {c.name: s.name for c, s in player.hand_states.items()},
#             "cards": [c.to_json() for c in player.hand]
#         }

#     app.config["JSON_SORT_KEYS"] = False
#     app.run(port=port)

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

NEW_GAME_ACTION = "new_game"
class MyEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, collections.deque):
                return list(o)
            return o.__dict__

def main():
    print_logo()
    LOGGER = new_logger("joerg")
    import asyncio
    import websockets
    boards = {}
    board = init_game()
    # print(board)

    async def hello(websocket, path):
        print(f"{websocket._host}: Connected!")
        while True:
            try:
                raw_payload = await websocket.recv()
            except websockets.exceptions.ConnectionClosedOK:
                print(f"{websocket._host}: left")
                break
            except websockets.exceptions.ConnectionClosedError:
                print(f"{websocket._host}: left")
                break

#             try:
#                 payload = json.loads(raw_payload)
#             except json.decoder.JSONDecodeError as jde:
#                 msg = f"! Malformed request: {jde}"
#                 print(msg)
#                 await websocket.send(msg)
#                 continue

#             if not isinstance(payload, dict):
#                 msg = "! Malformed request, payload must be json object"
#                 print(msg)
#                 await websocket.send(msg)
#                 continue

#             if "action" not in payload:
#                 msg = "! Missing action in JSON payload"
#                 await websocket.send(msg)
#                 continue

#             print(f"< {payload}")

#             action = payload["action"]
#             if action == NEW_GAME_ACTION:
#                 board = init_game()
#                 board_id = random.randint(0, 100)
#                 boards[board_id] = board
#                 print(f"Board {board_id} created!")
#                 await websocket.send(json.dumps({"board_id": board_id}))
#                 await websocket.send(json.dumps(board, cls=MyEncoder))
#                 # {"action": "new_game"}
#                 continue

# #             print(f"< {name}")

            greeting = f"{websocket._host} sent: {raw_payload}"

            await websocket.send(greeting)
            print(f"> {greeting}")

    start_server = websockets.serve(hello, "192.168.1.109", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
