from player import Player
from card import Card
from order import Order


class ActiveCard:
    def __init__(self, player: Player, card: Card, order: Order):
        self.player: Player = player
        self.card: Card = card
        self.order: Order = order

    def __repr__(self) -> str:
        return f"{self.player}: {self.card} {self.order}"
