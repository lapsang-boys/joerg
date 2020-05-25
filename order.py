from enum import Enum


class Order(Enum):
    attack = 1
    defense = 2

    def __repr__(self):
        return self.name
