from abc import ABC
from typing import Any, Mapping, Optional, TYPE_CHECKING

from order import Order

if TYPE_CHECKING:
    from board import Board
    from player import Player


class Card(ABC):
    def __init__(self):
        self.name: str
        self.power: int
        self.ruling: str
        self.legendary: bool
        self.flavor: Optional[str]

    def from_json(self, payload: Mapping[str, Any]) -> "Card":
        assert payload.get("name") is not None, f"Missing name from payload: {payload}"
        assert payload.get("power") is not None, f"Missing power from payload {payload}"
        assert payload.get("ruling") is not None, f"Missing ruling from payload: {payload}"
        assert payload.get("legendary") is not None, f"Missing legendary from payload: {payload}"
        # Flavor is optional

        self.name = str(payload.get("name"))
        self.power = int(payload.get("power", 0))
        self.ruling = str(payload.get("ruling"))
        self.legendary = bool(payload.get("legendary", False))
        self.flavor = str(payload.get("flavor"))

        return self

    def on_win(self, board: "Board", player: "Player", order: Order) -> None:
        pass

    def on_lose(self, board: "Board", player: "Player", order: Order) -> None:
        pass

    def on_reveal(self, board: "Board", player: "Player", order: Order) -> None:
        pass

    def on_cycle(self, board: "Board", player: "Player") -> None:
        new_card = board.draw_card()
        player.add_card_to_hand(new_card)

    def on_hand_enter(self) -> None:
        pass

    def before_power(self, board: "Board", player: "Player", order: Order) -> None:
        pass

    def power_resolve(self) -> None:
        pass

    def __repr__(self):
        return f"<{self.power}> {self.name}"

    def copy(self) -> "Card":
        new_card = Card()
        new_card.name = self.name
        new_card.power = self.power
        new_card.ruling = self.ruling
        new_card.flavor = self.flavor
        return new_card

    # TODO(_): Has lots of fun collisions.
    def __hash__(self):
        return hash(self.name)

    # TODO(_): Has lots of fun collisions.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.name == other.name
