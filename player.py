import logging
import random
from enum import Enum
from typing import List, Optional, Tuple, Any, Union, Dict

from cards.card import Card
from log import new_logger

_NAME_LOOKUP = ["Emil", "Henry", "Robin", "Bob"]
LOGGER = new_logger("player", logging.DEBUG)


class HandCardState(Enum):
    VisibleOnlyForPlayer = 1
    VisibleForEveryone = 2
    HiddenFromEveryone = 3


class Player:
    def __init__(self, num: int):
        self.num = num
        self.hand: List[Card] = []
        self.hand_states: Dict[Card, HandCardState] = {}

    def remove_card_from_hand(self, card: Card) -> Tuple[int, Card]:
        assert card in self.hand
        assert card in self.hand_states

        index = self.hand.index(card)
        removed_card = self.hand.pop(index)
        del self.hand_states[removed_card]

        assert card not in self.hand
        assert card not in self.hand_states
        return (index, removed_card)

    def get_random_card_from_hand(self) -> Card:
        return random.choice(self.hand)

    def add_card_to_hand(
        self,
        card: Card,
        index: Optional[int] = None,
        state: HandCardState = HandCardState.VisibleOnlyForPlayer,
    ) -> None:
        assert card not in self.hand
        assert card not in self.hand_states

        card.on_hand_enter()
        if index is not None:
            self.hand.insert(index, card)
        else:
            self.hand.append(card)
        self.hand_states[card] = state

        assert card in self.hand
        assert card in self.hand_states

    def hand_size(self) -> int:
        return len(self.hand)

    def set_card_visible(self, card: Card) -> None:
        self.hand_states[card] = HandCardState.VisibleForEveryone
        LOGGER.info(f"{self} shows {card}")

    def set_card_hidden(self, card: Card) -> None:
        self.hand_states[card] = HandCardState.HiddenFromEveryone
        LOGGER.info(f"{self} hides {card}")

    def set_card_default(self, card: Card) -> None:
        self.hand_states[card] = HandCardState.VisibleOnlyForPlayer
        LOGGER.info(f"{self} returns {card} to normal (only visible for player)")

    def player_picks(self, items: List[Any], num: int = 1) -> Union[List[Any], Any]:
        if num == 1:
            return random.choice(items)
        else:
            return random.sample(items, num)

    def __repr__(self):
        return f"Player {_NAME_LOOKUP[self.num]}"
