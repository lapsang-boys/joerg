from typing import TYPE_CHECKING, Callable, List

from cards.card import Card
from order import Order
from player import Player

if TYPE_CHECKING:
    from board import Board


def assert_same_handsizes(func: Callable[["PlayedCard", "Board"], None]):
    def wrapper_func(played_card: "PlayedCard", board: "Board"):
        old_hand_sizes: List[int] = [p.hand_size() for p in board.players]
        return_value = func(played_card, board)
        new_hand_sizes: List[int] = [p.hand_size() for p in board.players]

        assert (
            old_hand_sizes == new_hand_sizes
        ), f"Hand sizes have changed! func: {func.__name__} -- {old_hand_sizes} != {new_hand_sizes}"

        return return_value

    return wrapper_func


def assert_card_only_in_one_place(func: Callable[["PlayedCard", "Board"], None]):
    def wrapper_func(played_card: "PlayedCard", board: "Board"):
        return_value = func(played_card, board)

        for card in board.original_deck:
            card_in_player_hands = [
                any([c == card for c in p.hand]) for p in board.players
            ].count(True)
            card_is_played = [c.card == card for c in board.played_cards].count(True)
            card_in_deck = [c == card for c in board.deck].count(True)
            card_in_graveyard = sum(
                [
                    [c == card for c in graveyard].count(True)
                    for graveyard in board.graveyard.values()
                ]
            )
            assert (
                card_in_player_hands + card_is_played + card_in_deck + card_in_graveyard
                != 0
            ), f"Card has disappeared! {card}"
            assert (
                card_in_player_hands + card_is_played + card_in_deck + card_in_graveyard
                == 1
            ), f"Card is in multiple places at the same time! {card} -- Player Hands: {card_in_player_hands} | Played Cards: {card_is_played} | In Deck: {card_in_deck} | Graveyards: {card_in_graveyard}"

        return return_value

    return wrapper_func


def assert_same_deck_size(func: Callable[["PlayedCard", "Board"], None]):
    def wrapper_func(played_card: "PlayedCard", board: "Board"):
        old_deck_size = len(board.deck)
        return_value = func(played_card, board)
        assert old_deck_size == len(
            board.deck
        ), f"Deck has not same size! Old: {old_deck_size} == New: {len(board.deck)}"
        return return_value

    return wrapper_func


class PlayedCard:
    def __init__(self, player: Player, card: Card, order: Order, revealed=False):
        self.player: Player = player
        self.card: Card = card
        self.order: Order = order
        self.revealed: bool = revealed

    @assert_same_deck_size
    @assert_card_only_in_one_place
    @assert_same_handsizes
    def on_win(self, board: "Board") -> None:
        self.card.on_win(board, self.player, self.order)

    @assert_same_deck_size
    @assert_card_only_in_one_place
    @assert_same_handsizes
    def on_lose(self, board: "Board") -> None:
        self.card.on_lose(board, self.player, self.order)

    @assert_same_deck_size
    @assert_card_only_in_one_place
    @assert_same_handsizes
    def on_reveal(self, board: "Board") -> None:
        self.card.on_reveal(board, self.player, self.order)

    @assert_same_deck_size
    @assert_card_only_in_one_place
    @assert_same_handsizes
    def on_cycle(self, board: "Board") -> None:
        self.card.on_cycle(board, self.player)

    @assert_same_deck_size
    @assert_card_only_in_one_place
    @assert_same_handsizes
    def on_hand_enter(self) -> None:
        pass

    @assert_same_deck_size
    @assert_card_only_in_one_place
    @assert_same_handsizes
    def before_power(self, board: "Board") -> None:
        self.card.before_power(board, self.player, self.order)

    @assert_same_deck_size
    @assert_card_only_in_one_place
    @assert_same_handsizes
    def power_resolve(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"{self.player}: {self.card} {self.order}"
