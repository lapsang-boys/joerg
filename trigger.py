from enum import Enum


class Trigger(Enum):
    on_win = 1
    on_lose = 2
    on_reveal = 3
    on_cycle = 4
    on_hand_enter = 5
    before_power = 6

    def __repr__(self):
        return self.name
