import logging
from typing import List

from board import Board
from cards.cards import read_cards
from player import Player

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
        logger.info(" ")
        logger.info(f"Round {round_number} start!")
        logger.info(" ")

        board.begin_round()
        board.set_pole(pole_player)

        for player in board.players:
            _, random_card = player.pop_random_card()
            chosen_order = player.select_order()
            board.commit_card(player, random_card, chosen_order)

        logger.info(f"{board}")

        for resolving_card in board.resolve_cards():
            resolving_card.card.on_reveal()

        for resolving_card in board.resolve_cards():
            resolving_card.card.before_power()

        for resolving_card in board.resolve_cards():
            logger.info(f"{resolving_card}")

        winning_card = board.resolve_power()
        logger.info("")
        logger.info("")
        logger.info("")
        logger.info(f"Winning card! {winning_card}")
        logger.info("")
        victories[winning_card.player] += 1
        if victories[winning_card.player] == NUMBER_OF_WINNING_ROUNDS_NEEDED:
            break

        for resolving_card in board.resolve_cards():
            if (
                "On Win" in resolving_card.card.ruling
                and resolving_card.card == winning_card.card
            ):
                resolving_card.on_win(board)
            elif (
                "On Lose" in resolving_card.card.ruling
                and resolving_card.card != winning_card.card
            ):
                resolving_card.on_lose(board)

        for active_card in board.losing_cards():
            active_card.player.add_card_to_hand(active_card.card)

        pole_player = board.get_next_player(pole_player)

        if victories[winning_card.player] == 2:
            cycled_cards = []
            logger.info(f"Cycle! {winning_card.player} has reached 2 wins.")
            logger.info(" ")
            for player in board.all_players_except_winner(
                winning_player=winning_card.player
            ):
                cycled_card_index, random_card = player.pop_random_card()
                random_card.on_cycle()
                cycled_cards.append(random_card)

                new_card = board.draw_card()
                player.add_card_to_hand(new_card, index=cycled_card_index)

            board.add_cycled_cards_to_bottom_of_deck(cycled_cards)

        logger.info("Round finished!")
        logger.info("")
        logger.info("-" * 80)
        logger.info("")
        round_number += 1

    logger.info("")
    winner = max(victories, key=lambda x: victories[x])
    logger.info(f"Winning player: {winner}")
    logger.info("Victories")
    for player in victories:
        logger.info(f"\t{player} won {victories[player]} sticks")


if __name__ == "__main__":
    logger = logging.getLogger("asdf")
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    main()
