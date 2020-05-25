from typing import TYPE_CHECKING, Callable, List

from cards.card import Card
from order import Order
from player import Player

if TYPE_CHECKING:
    from board import Board


def assert_same_handsizes(func: Callable[["Board"], None]):
    def wrapper_func(active_card: "ActiveCard", board: "Board"):
        old_hand_sizes: List[int] = [len(p.hand) for p in board.players]
        return_value = func(active_card, board)
        new_hand_sizes: List[int] = [len(p.hand) for p in board.players]

        assert (
            old_hand_sizes == new_hand_sizes
        ), f"Hand sizes have changed! func: {func.__name__} -- {old_hand_sizes} != {new_hand_sizes}"

        return return_value

    return wrapper_func


class ActiveCard:
    def __init__(self, player: Player, card: Card, order: Order):
        self.player: Player = player
        self.card: Card = card
        self.order: Order = order

    @assert_same_handsizes
    def on_win(self, board: "Board") -> None:
        self.card.on_win(board, self.player, self.order)
        pass

    @assert_same_handsizes
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
