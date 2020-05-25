from typing import Any, List, Mapping, Optional

from cards import (
    ON_WIN_CARDS,
    ON_LOSE_CARDS,
    ON_REVEAL_CARDS,
    ON_CYCLE_CARDS,
    ON_HAND_ENTER_CARDS,
    BEFORE_POWER_CARDS,
)
from trigger import Trigger


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

    # TODO(_): Has lots of fun collisions.
    def __hash__(self):
        return hash(self.name)

    # TODO(_): Has lots of fun collisions.
    def __eq__(self, other: "Card") -> bool:
        return self.name == other.name
