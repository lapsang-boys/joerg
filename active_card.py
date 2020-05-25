from typing import TYPE_CHECKING

from cards.card import Card
from order import Order
from player import Player

if TYPE_CHECKING:
    from board import Board


class ActiveCard:
    def __init__(self, player: Player, card: Card, order: Order):
        self.player: Player = player
        self.card: Card = card
        self.order: Order = order

    def on_win(self, board: "Board") -> None:
        self.card.on_win(board, self.player, self.order)
        pass

    def on_lose(self, board: "Board") -> None:
        self.card.on_lose(board, self.player, self.order)
        pass

    def on_reveal(self) -> None:
        pass

    def on_cycle(self) -> None:
        pass

    def on_hand_enter(self) -> None:
        pass

    def before_power(self) -> None:
        pass

    def power_resolve(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"{self.player}: {self.card} {self.order}"
