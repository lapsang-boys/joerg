import logging
import random
from typing import List, Optional, Tuple

from cards.card import Card
from order import Order

_NAME_LOOKUP = ["Emil", "Henry", "Robin", "Bob"]


class Player:
    def __init__(self, num: int):
        self.num = num
        self.hand: List[Card] = []

    def remove_card_from_hand(self, card: Card) -> Tuple[int, Card]:
        assert card in self.hand
        index = self.hand.index(card)
        return (index, self.hand.pop(index))

    def select_order(self) -> Order:
        random_order = random.choice([Order.attack, Order.defense])
        return random_order

    def get_random_card_from_hand(self) -> Card:
        return random.choice(self.hand)

    def add_card_to_hand(self, card: Card, index: Optional[int] = None) -> None:
        card.on_hand_enter()
        if index is not None:
            self.hand.insert(index, card)
        else:
            self.hand.append(card)

    def pop_random_card(self) -> Tuple[int, Card]:
        assert len(self.hand) > 0
        card = self.hand[random.randint(0, self.hand_size() - 1)]
        return self.remove_card_from_hand(card)

    def hand_size(self) -> int:
        return len(self.hand)

    def set_card_visible(self, card: Card) -> None:
        logging.debug("not implemented: set_card_visible")

    def __repr__(self):
        return f"Player {_NAME_LOOKUP[self.num]}"
