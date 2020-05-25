import logging
from typing import List

from board import Board
from cards.cards import read_cards
from player import Player

NUMBER_OF_WINNING_ROUNDS_NEEDED = 3
NUM_PLAYERS = 4
STARTING_HAND_SIZE = NUMBER_OF_WINNING_ROUNDS_NEEDED + 1
LIBRARY_PATH = "./cards/cards.json"


def main():
    deck = read_cards(LIBRARY_PATH)

    players: List[Player] = []
    for p in range(NUM_PLAYERS):
        players.append(Player(p))

    board = Board(players, deck)
    pole_player = board.randomly_assign_pole()
    board.shuffle_deck()
    board.deal_cards(STARTING_HAND_SIZE)

    victories = {p: 0 for p in players}
    round_number = 0
    while max(victories.values()) < NUMBER_OF_WINNING_ROUNDS_NEEDED:
        logger.debug(" ")
        logger.debug(f"Round {round_number} start!")
        logger.debug(" ")
        board.begin_round()
        board.set_pole(pole_player)

        # trade phase
        # pick card, pick player

        # commit phase
        # choose card, choose position

        for player in players:
            _, random_card = player.pop_random_card()
            chosen_order = player.select_order()
            board.commit_card(player, random_card, chosen_order)

        # reveal phase
        # beginning from pole, reveal card
        # trigger abilities

        logger.debug(f"{board}")

        # resolve phase
        # from pole, find the winning power (lowest for defense, highest for attack), in case of multiple cards with the same power, the card closest from pole wins (linearly, not bilinearly).
        for resolving_card in board.resolve_cards():
            # logger.debug(f"{resolving_card}")
            resolving_card.card.on_reveal()

        # Before power
        for resolving_card in board.resolve_cards():
            # logger.debug(f"{resolving_card}")
            resolving_card.card.before_power()

        for resolving_card in board.resolve_cards():
            logger.debug(f"{resolving_card}")
        winning_card = board.resolve_power()
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

        logger.debug("")
        logger.debug("")
        logger.debug("")
        logger.debug(f"Winning card! {winning_card}")
        logger.debug("")
        victories[winning_card.player] += 1
        for active_card in board.losing_cards():
            active_card.player.add_card_to_hand(active_card.card)

        pole_player = board.get_next_player(pole_player)

        # Cycle
        # When any player recieves their second victory, all other players cycles 1 card.
        if victories[winning_card.player] == 2:
            cycled_cards = []
            logger.debug("CYCLE!")
            logger.debug(" ")
            for player in board.all_players_except_winner(
                winning_player=winning_card.player
            ):
                cycled_card_index, random_card = player.pop_random_card()
                random_card.on_cycle()
                cycled_cards.append(random_card)

                new_card = board.draw_card()
                player.add_card_to_hand(new_card, index=cycled_card_index)

            board.add_cycled_cards_to_bottom_of_deck(cycled_cards)

        logger.debug("Round finished!")
        logger.debug("")
        logger.debug("-"*80)
        logger.debug("")
        round_number += 1

    logger.debug(f"Victories {victories}")


if __name__ == "__main__":
    logger = logging.getLogger("asdf")
    logger.propagate = False
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    main()
