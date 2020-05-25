import json
import random
from collections import deque
from typing import Any, Deque, List, Mapping, Optional, Tuple

from cards import (
    ON_WIN_CARDS,
    ON_LOSE_CARDS,
    ON_REVEAL_CARDS,
    ON_CYCLE_CARDS,
    ON_HAND_ENTER_CARDS,
    BEFORE_POWER_CARDS,
)
from order import Order
from trigger import Trigger

NUMBER_OF_WINNING_ROUNDS_NEEDED = 3
NUM_PLAYERS = 4
STARTING_HAND_SIZE = 3


class InvalidLibraryFileError(Exception):
    def __init__(self, msg="Unable to read 'cards' field from library."):
        super().__init__(msg)


class Card:
    def __init__(self):
        self.name: str
        self.power: int
        self.ruling: str
        self.flavor: Optional[str]
        self.triggers: List[Trigger]

    def from_json(self, payload: Mapping[str, Any]) -> "Card":
        self.name = payload.get("name")
        self.power = payload.get("power")
        self.ruling = payload.get("ruling")
        self.flavor = payload.get("flavor")
        self.triggers = self.add_triggers(self.name)

        assert self.name, f"Missing name from payload: {payload}"
        assert self.power, f"Missing power from payload: {payload}"
        assert self.ruling, f"Missing ruling from payload: {payload}"
        # Flavor is optional

        return self

    def add_triggers(self, name: str) -> List[Trigger]:
        triggers: List[Trigger] = []
        if name in ON_WIN_CARDS:
            triggers.append(Trigger.on_win)
        if name in ON_LOSE_CARDS:
            triggers.append(Trigger.on_lose)
        if name in ON_REVEAL_CARDS:
            triggers.append(Trigger.on_reveal)
        if name in ON_CYCLE_CARDS:
            triggers.append(Trigger.on_cycle)
        if name in ON_HAND_ENTER_CARDS:
            triggers.append(Trigger.on_hand_enter)
        if name in BEFORE_POWER_CARDS:
            triggers.append(Trigger.before_power)

        return triggers

    def __repr__(self):
        return f"<{self.power}> {self.name}"

    # Has lots of fun collisions.
    def __hash__(self):
        return hash(self.name)

    # Has lots of fun collisions.
    def __eq__(self, other: "Card") -> bool:
        return self.name == other.name


class Player:
    def __init__(self, num: int):
        self.num = num
        self.hand: List[Card] = []

    def remove_card_from_hand(self, card: Card) -> Tuple[int, Card]:
        assert card in self.hand
        index = self.hand.index(card)
        return (index, self.hand.pop(index))

    def add_card_to_hand(self, card: Card, index: Optional[int] = None) -> None:
        if index is not None:
            self.hand.insert(index, card)
        else:
            self.hand.append(card)

    def pop_random_card(self) -> Tuple[int, Card]:
        assert len(self.hand) > 0
        card = self.hand[random.randint(0, self.hand_size() - 1)]
        return self.remove_card_from_hand(card)

    def hand_size(self) -> int:
        return len(self.hand)

    def __repr__(self):
        return f"Player {self.num}"


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


class ActiveCard:
    def __init__(self, player: Player, card: Card, order: Order):
        self.player: Player = player
        self.card: Card = card
        self.order: Order = order

    def __repr__(self) -> str:
        return f"{self.player}: {self.card} {self.order}"


class Board:
    def __init__(self, player_order: List[Player]):
        pole: Player
        self.cards: List[ActiveCard] = []
        self.player_order: List[Player] = player_order

    def set_pole(self, player: Player) -> None:
        self.pole = player

    def begin_round(self) -> None:
        # Flush old cards.
        self.cards = []

    def commit_card(self, player: Player, card: Card, order: Order):
        self.cards.append(ActiveCard(player, card, order))

    def resolve_cards(self):
        start_index = self.get_pole_index()
        for i in range(NUM_PLAYERS):
            yield self.cards[(start_index + i) % NUM_PLAYERS]

    def get_pole_index(self) -> int:
        return next(
            index for index, ac in enumerate(self.cards) if ac.player == self.pole
        )

    def get_pole(self):
        pole_index = self.get_pole_index()
        return self.cards[pole_index]

    def resolved_order(self) -> Order:
        orders = [c.order for c in self.cards]
        num_attack = 0
        num_defense = 0
        for order in orders:
            if order == Order.attack:
                num_attack += 1
            elif order == Order.defense:
                num_defense += 1

        assert num_attack + num_defense == len(self.cards)

        # Tie
        if num_attack > num_defense:
            return Order.attack
        elif num_defense > num_attack:
            return Order.defense
        elif num_attack == num_defense:
            pole_active_card = self.get_pole()
            return pole_active_card.order

    def locked_order_cards(self) -> List[ActiveCard]:
        return list(self.resolve_cards())

    def get_next_player(self, player: Player) -> Player:
        start_index = self.player_order.index(player)
        return self.player_order[(start_index + 1) % NUM_PLAYERS]

    def resolve_power(self) -> ActiveCard:
        best_card = None
        lower_better = lambda x, y: x < y
        higher_better = lambda x, y: x > y
        is_better = (
            lower_better if self.resolved_order() == Order.defense else higher_better
        )
        for active_card in self.locked_order_cards():
            if not best_card or is_better(active_card.card.power, best_card.card.power):
                best_card = active_card

        return best_card

    def losing_cards(self) -> List[ActiveCard]:
        all_cards = self.cards
        winning_card = self.resolve_power()
        return [c for c in all_cards if c != winning_card]

    def __repr__(self):
        return f"Pole: {self.pole}\nResolved order: {self.resolved_order()}"


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
