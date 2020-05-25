import logging
import random
import sys

from board import Board
from cards.cards import read_cards
from log import new_logger

NUMBER_OF_WINNING_ROUNDS_NEEDED = 3
NUMBER_OF_PLAYERS = 4
STARTING_HAND_SIZE = NUMBER_OF_WINNING_ROUNDS_NEEDED + 1
LIBRARY_PATH = "./cards/cards.json"


def main():
    deck = read_cards(LIBRARY_PATH)

    board = Board(deck, number_of_players=NUMBER_OF_PLAYERS)
    pole_player = board.randomly_assign_pole()
    board.shuffle_deck()
    board.deal_cards(STARTING_HAND_SIZE)

    victories = {p: 0 for p in board.players}
    round_number = 0
    while max(victories.values()) < NUMBER_OF_WINNING_ROUNDS_NEEDED:
        LOGGER.info(" ")
        LOGGER.info(f"Round {round_number} start!")
        LOGGER.info(" ")

        board.begin_round()
        board.set_pole(pole_player)

        for player in board.players:
            _, random_card = player.pop_random_card()
            chosen_order = player.select_order()
            board.commit_card(player, random_card, chosen_order)

        LOGGER.info(f"{board}")

        for resolving_card in board.get_played_cards():
            resolving_card.card.on_reveal()

        for resolving_card in board.get_played_cards():
            resolving_card.card.before_power()

        for resolving_card in board.get_played_cards():
            LOGGER.info(f"{resolving_card}")

        winning_card = board.resolve_power()
        LOGGER.info("")
        LOGGER.info("")
        LOGGER.info("")
        LOGGER.info(f"Winning card! {winning_card} played by {board.round_winner}")
        LOGGER.info("")
        victories[board.round_winner] += 1
        if victories[board.round_winner] == NUMBER_OF_WINNING_ROUNDS_NEEDED:
            break

        for resolving_card in board.get_played_cards():
            if resolving_card.card == winning_card:
                resolving_card.on_win(board)
            elif resolving_card.card != winning_card:
                resolving_card.on_lose(board)

        for active_card in board.losing_cards():
            active_card.player.add_card_to_hand(active_card.card)

        if victories[board.round_winner] == NUMBER_OF_WINNING_ROUNDS_NEEDED - 1:
            cycled_cards = []
            LOGGER.info(f"Cycle! {board.round_winner} has reached 2 wins.")
            LOGGER.info(" ")
            for player in board.all_players_except_winner(
                winning_player=board.round_winner
            ):
                cycled_card_index, random_card = player.pop_random_card()
                random_card.on_cycle()
                cycled_cards.append(random_card)

                new_card = board.draw_card()
                player.add_card_to_hand(new_card, index=cycled_card_index)

            board.add_cycled_cards_to_bottom_of_deck(cycled_cards)

        pole_player = board.get_next_player(board.get_pole_player())
        LOGGER.info("Round finished!")
        LOGGER.info("")
        LOGGER.info("-" * 80)
        LOGGER.info("")
        round_number += 1

    LOGGER.info("")
    winner = max(victories, key=lambda x: victories[x])
    LOGGER.info(f"Winning player: {winner}")
    LOGGER.info("")
    LOGGER.info("Victories")
    for player in victories:
        LOGGER.info(f"\t{player} won {victories[player]} sticks")


if __name__ == "__main__":
    LOGGER = new_logger("joerg", logging.INFO)
    seed = random.randrange(sys.maxsize)
    random.seed(seed)
    LOGGER.warning(f"Seed was: {seed}")
    main()
