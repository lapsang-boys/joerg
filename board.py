from typing import List

from active_card import ActiveCard
from cards.card import Card
from order import Order
from player import Player


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

    def number_of_players(self) -> int:
        return len(self.player_order)

    def resolve_cards(self):
        start_index = self.get_pole_index()
        for i in range(self.number_of_players()):
            yield self.cards[(start_index + i) % self.number_of_players()]

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
        return self.player_order[(start_index + 1) % self.number_of_players()]

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

        for active_card in self.locked_order_cards():
            if not best_card or is_better(active_card.card, best_card.card):
                best_card = active_card

        return best_card

    def losing_cards(self) -> List[ActiveCard]:
        all_cards = self.cards
        winning_card = self.resolve_power()
        return [c for c in all_cards if c != winning_card]

    def __repr__(self):
        return f"Pole: {self.pole}\nResolved order: {self.resolved_order()}"
