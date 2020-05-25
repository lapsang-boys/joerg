import json
import random
from collections import deque
from typing import Deque, List

from card import Card
from order import Order
from player import Player


NUMBER_OF_WINNING_ROUNDS_NEEDED = 3
NUM_PLAYERS = 4
STARTING_HAND_SIZE = 3


class InvalidLibraryFileError(Exception):
    def __init__(self, msg="Unable to read 'cards' field from library."):
        super().__init__(msg)


def shuffle_deck(cards: Deque[Card]) -> None:
    random.shuffle(cards)


def deal_cards(cards: Deque[Card], players: List[Player]) -> None:
    for player in players:
        for j in range(STARTING_HAND_SIZE):
            card = cards.pop()
            player.add_card_to_hand(card)

    assert len(player.hand) == STARTING_HAND_SIZE


def read_cards() -> Deque[Card]:
    with open("./cards.json", "r") as fp:
        raw_object = json.load(fp)

    raw_cards = raw_object.get("cards", None)
    if not raw_cards:
        raise InvalidLibraryFileError()

    cards = [Card().from_json(rc) for rc in raw_cards]
    assert len(cards) == len(
        set(cards)
    ), "Name collision in library! Two cards with same name."

    return deque(cards)


def randomly_assign_pole(players: List[Player]) -> Player:
    return random.choice(players)


def trade(card1: Card, player1: Player, card2, player2) -> None:
    assert card1 in player1.hand
    assert card2 in player2.hand

    index1, _ = player1.remove_card_from_hand(card1)
    index2, _ = player2.remove_card_from_hand(card2)

    player1.add_card_to_hand(card2, index=index1)
    player2.add_card_to_hand(card1, index=index2)

    assert card2 in player1.hand
    assert card1 in player2.hand


def all_players_except_winner(
    players: List[Player], winning_player: Player
) -> List[Player]:
    return [p for p in players if p != winning_player]


def main():
    cards = read_cards()
    shuffle_deck(cards)

    players: List[Player] = []

    for p in range(NUM_PLAYERS):
        players.append(Player(p))

    deal_cards(cards, players)
    pole_player = randomly_assign_pole(players)

    board = Board(players)

    victories = {p: 0 for p in players}
    while max(victories.values()) < NUMBER_OF_WINNING_ROUNDS_NEEDED:
        board.begin_round()
        board.set_pole(pole_player)

        # trade phase
        # pick card, pick player
        # trade(players[0].hand[2], players[0], players[1].hand[2], players[1])

        # commit phase
        # choose card, choose position

        for player in players:
            _, random_card = player.pop_random_card()
            random_order = random.choice([Order.attack, Order.defense])
            board.commit_card(player, random_card, random_order)

        # reveal phase
        # beginning from pole, reveal card
        # trigger abilities

        print(board)

        # resolve phase
        # from pole, find the winning power (lowest for defense, highest for attack), in case of multiple cards with the same power, the card closest from pole wins (linearly, not bilinearly).
        for resolving_card in board.resolve_cards():
            print(resolving_card)

        winning_card = board.resolve_power()
        for resolving_card in board.resolve_cards():
            if (
                "On Win" in resolving_card.card.ruling
                and resolving_card.card == winning_card.card
            ):
                print("Trigger On Win!", resolving_card.card)
            elif (
                "On Lose" in resolving_card.card.ruling
                and resolving_card.card != winning_card.card
            ):
                print("Trigger On Lose!", resolving_card.card)

        print("")
        print("Winning card!", winning_card)
        print("")
        victories[winning_card.player] += 1
        for active_card in board.losing_cards():
            active_card.player.add_card_to_hand(active_card.card)

        pole_player = board.get_next_player(pole_player)

        # Cycle
        # When any player recieves their second victory, all other players cycles 1 card.
        if victories[winning_card.player] == 2:
            cycled_cards = []
            for player in all_players_except_winner(
                players, winning_player=winning_card.player
            ):
                cycled_card_index, random_card = player.pop_random_card()
                cycled_cards.append(random_card)
                new_card = cards.popleft()
                player.add_card_to_hand(new_card, index=cycled_card_index)

            print("CYCLE!")

    print("")
    print(victories)
    print([len(p.hand) for p in players])
    print("")


if __name__ == "__main__":
    main()
