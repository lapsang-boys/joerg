import logging
import random
from typing import List, Optional, Tuple

from cards.card import Card
from log import new_logger

_NAME_LOOKUP = ["Emil", "Henry", "Robin", "Bob"]
LOGGER = new_logger("player", logging.DEBUG)


class Player:
    def __init__(self, num: int):
        self.num = num
        self.hand: List[Card] = []

    def remove_card_from_hand(self, card: Card) -> Tuple[int, Card]:
        assert card in self.hand
        index = self.hand.index(card)
        return (index, self.hand.pop(index))

    def get_random_card_from_hand(self) -> Card:
        return random.choice(self.hand)

    def add_card_to_hand(self, card: Card, index: Optional[int] = None) -> None:
        card.on_hand_enter()
        if index is not None:
            self.hand.insert(index, card)
        else:
            self.hand.append(card)

    def hand_size(self) -> int:
        return len(self.hand)

    def set_card_visible(self, card: Card) -> None:
        print(f"{self} shows {card}")
        LOGGER.debug("not implemented: set_card_visible")

    def __repr__(self):
        return f"Player {_NAME_LOOKUP[self.num]}"
