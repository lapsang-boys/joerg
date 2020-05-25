import random
from typing import List, Optional, Tuple

from card import Card


class Player:
    def __init__(self, num: int):
        self.num = num
        self.hand: List[Card] = []

    def remove_card_from_hand(self, card: Card) -> Tuple[int, Card]:
        assert card in self.hand
        index = self.hand.index(card)
        return (index, self.hand.pop(index))

    def add_card_to_hand(self, card: Card, index: Optional[int] = None) -> None:
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

    def __repr__(self):
        return f"Player {self.num}"
