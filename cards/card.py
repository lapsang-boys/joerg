from abc import ABC
from typing import Any, List, Mapping, Optional

from order import Order
from trigger import Trigger


class Card(ABC):
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
        # self.triggers = self.add_triggers(self.name)

        assert self.name, f"Missing name from payload: {payload}"
        assert self.power, f"Missing power from payload: {payload}"
        assert self.ruling, f"Missing ruling from payload: {payload}"
        # Flavor is optional

        return self

    def on_win(self, board: "Board", player: "Player", order: Order) -> None:
        pass

    def on_lose(self, board: "Board", player: "Player", order: Order) -> None:
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

    def __repr__(self):
        return f"<{self.power}> {self.name}"

    # TODO(_): Has lots of fun collisions.
    def __hash__(self):
        return hash(self.name)

    # TODO(_): Has lots of fun collisions.
    def __eq__(self, other: "Card") -> bool:
        return self.name == other.name
