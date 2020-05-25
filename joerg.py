import logging
import random
import sys

from board import Board
from cards.cards import read_cards
from log import new_logger
from logo import print_logo
from order import Order

NUMBER_OF_WINNING_ROUNDS_NEEDED = 3
NUMBER_OF_PLAYERS = 4
STARTING_HAND_SIZE = NUMBER_OF_WINNING_ROUNDS_NEEDED + 1
LIBRARY_PATH = "./cards/cards.json"


def joerg_round(board: Board, victories):
    board.begin_round()

    for player in board.players:
        chosen_card = board.player_picks(player, player.hand)
        player.remove_card_from_hand(chosen_card)

        chosen_order = board.player_picks(player, [Order.attack, Order.defense])
        board.commit_card(player, chosen_card, chosen_order)

    LOGGER.info(f"{board}")

    board.resolve_on_reveal()
    board.resolve_before_power()

    for resolving_card in board.get_played_cards():
        LOGGER.info(f"{resolving_card}")

    winning_card = board.resolve_power()
    LOGGER.info("")
    LOGGER.info("")
    LOGGER.info(f"Winning card! {winning_card} played by {board.round_winner}")
    victories[board.round_winner] += 1
    if victories[board.round_winner] == NUMBER_OF_WINNING_ROUNDS_NEEDED:
        return

    for resolving_card in board.get_played_cards():
        if resolving_card.card == winning_card:
            resolving_card.on_win(board)
        elif resolving_card.card != winning_card:
            resolving_card.on_lose(board)

    board.add_to_graveyard(board.round_winner, board.round_winning_card)

    for active_card in board.losing_cards():
        active_card.player.add_card_to_hand(active_card.card)

    if victories[board.round_winner] == NUMBER_OF_WINNING_ROUNDS_NEEDED - 1:
        LOGGER.info(f"Cycle! {board.round_winner} has reached 2 wins.")
        LOGGER.info(" ")
        board.cycle_event(board.round_winner)

    board.progress_pole()


def end_of_game(victories):
    LOGGER.info("")
    winner = max(victories, key=lambda x: victories[x])
    LOGGER.info(f"Winning player: {winner}")
    LOGGER.info("")
    LOGGER.info("Victories")
    for player in victories:
        LOGGER.info(f"\t{player} won {victories[player]} sticks")


def init_game() -> Board:
    deck = read_cards(LIBRARY_PATH)

    board = Board(deck, number_of_players=NUMBER_OF_PLAYERS)
    board.randomly_assign_pole()
    board.shuffle_deck()
    board.deal_cards(STARTING_HAND_SIZE)

    return board


def main():
    board = init_game()

    victories = {p: 0 for p in board.players}
    round_number = 0
    while max(victories.values()) < NUMBER_OF_WINNING_ROUNDS_NEEDED:
        LOGGER.info(" ")
        LOGGER.info(f"Round {round_number} start!")
        LOGGER.info(" ")
        joerg_round(board, victories)
        LOGGER.info("")
        LOGGER.info("Round finished!")
        LOGGER.info("")
        LOGGER.info("-" * 80)
        round_number += 1

    end_of_game(victories)


if __name__ == "__main__":
    LOGGER = new_logger("joerg", logging.INFO)
    seed = random.randrange(sys.maxsize)
    random.seed(seed)
    LOGGER.warning(f"Seed was: {seed}")
    print_logo()
    main()
