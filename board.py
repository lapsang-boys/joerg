import random
from typing import List, Any, Union, Deque

from active_card import ActiveCard
from cards.card import Card
from order import Order
from player import Player


class Board:
    def __init__(self, deck: Deque[Card], number_of_players: int):
        pole: Player
        self.deck: Deque[Card] = deck
        self.cards: List[ActiveCard] = []
        self.players: List[Player] = []
        for p in range(number_of_players):
            self.players.append(Player(p))

    def randomly_assign_pole(self) -> Player:
        pole_player = self.get_random_player()
        self.set_pole(pole_player)
        return pole_player

    def set_pole(self, player: Player) -> None:
        self.pole = player

    def shuffle_deck(self) -> None:
        random.shuffle(self.deck)

    def begin_round(self) -> None:
        # Flush old cards.
        self.cards = []

    def commit_card(self, player: Player, card: Card, order: Order):
        self.cards.append(ActiveCard(player, card, order))

    def number_of_players(self) -> int:
        return len(self.players)

    def player_picks(
        self, player: Player, items: List[Any], num: int = 1
    ) -> Union[List[Any], Any]:
        if num == 1:
            return random.choice(items)
        else:
            return random.sample(items, num)

    def get_previous_player(self, player: Player) -> Player:
        origin_player_index = self.players.index(player)
        return self.players[origin_player_index - 1 % self.number_of_players()]

    def get_played_cards(self):
        start_index = self.get_pole_index()
        for i in range(self.number_of_players()):
            yield self.cards[(start_index + i) % self.number_of_players()]

    def player_picks_opponent(self, player: Player) -> Player:
        opponents = self.get_opponents(player)
        return self.player_picks(player, opponents)

    def deal_cards(self, starting_hand_size: int) -> None:
        for player in self.players:
            for j in range(starting_hand_size):
                card = self.deck.pop()
                player.add_card_to_hand(card)

        assert len(player.hand) == starting_hand_size

    def draw_card(self) -> Card:
        # TODO(_): Undefined behavior when deck is empty.
        return self.deck.popleft()

    def get_opponents(self, player: Player) -> List[Player]:
        return [p for p in self.players if p != player]

    def get_random_player(self) -> Player:
        return random.choice(self.players)

    def get_random_opponent(self, player: Player) -> Player:
        return random.choice(self.get_opponents(player))

    def get_pole_index(self) -> int:
        return next(
            index for index, ac in enumerate(self.cards) if ac.player == self.pole
        )

    def get_pole(self):
        pole_index = self.get_pole_index()
        return self.cards[pole_index]

    def all_players_except_winner(self, winning_player: Player) -> List[Player]:
        return [p for p in self.players if p != winning_player]

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

    def get_pole_player(self) -> Player:
        return self.pole

    def get_opponent_played_cards(self, player: Player) -> List[ActiveCard]:
        return [ac for ac in self.get_played_cards() if ac.player != player]

    def get_next_player(self, player: Player) -> Player:
        start_index = self.players.index(player)
        return self.players[(start_index + 1) % self.number_of_players()]

    def resolve_power(self) -> ActiveCard:
        best_card = None

        def is_better(a: Card, b: Card):
            a.power_resolve()
            b.power_resolve()
            # Is card _a_ better than card _b_?
            if self.resolved_order() == Order.defense:
                # Lower is better.
                return a.power < b.power
            else:
                # Higher is better.
                return a.power > b.power

        for active_card in self.get_played_cards():
            if not best_card or is_better(active_card.card, best_card.card):
                best_card = active_card

        return best_card

    def add_cycled_cards_to_bottom_of_deck(self, cycled_cards: List[Card]):
        self.deck.extend(cycled_cards)

    def losing_cards(self) -> List[ActiveCard]:
        all_cards = self.cards
        winning_card = self.resolve_power()
        return [c for c in all_cards if c != winning_card]

    def trade(self, player1: Player, card1: Card, player2: Player, card2: Card) -> None:
        assert card1 in player1.hand
        assert card2 in player2.hand

        index1, _ = player1.remove_card_from_hand(card1)
        index2, _ = player2.remove_card_from_hand(card2)

        player1.add_card_to_hand(card2, index=index1)
        player2.add_card_to_hand(card1, index=index2)

        assert card2 in player1.hand
        assert card1 in player2.hand

    def __repr__(self):
        return f"Pole: {self.pole}\nResolved order: {self.resolved_order()}"
