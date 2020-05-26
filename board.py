import random
from collections import defaultdict
from typing import List, Any, Union, Deque, Optional, Dict, Set

from played_card import PlayedCard
from cards.card import Card
from order import Order
from player import Player


class Board:
    def __init__(
        self, deck: Deque[Card], number_of_players: int, starting_hand_size: int
    ):
        self.pole: Player
        self.original_deck: List[Card] = list(deck)
        self.deck: Deque[Card] = deck
        self.played_cards: List[PlayedCard] = []
        self.players: List[Player] = []
        self.round_winning_card: Optional[Card]
        self.round_winner: Optional[Player]
        self.graveyard: Dict[Player, List[Card]] = defaultdict(list)
        self.victories: Dict[Player, int] = defaultdict(int)

        # Card blocked for _int_ number of turns.
        self.blocked_cards: Dict[Card, int] = defaultdict(int)

        self.starting_hand_size: int = starting_hand_size

        for p in range(number_of_players):
            player = Player(p)
            self.players.append(player)
            self.graveyard[player] = []
            self.victories[player] = 0

    def randomly_assign_pole(self) -> Player:
        pole_player = self.get_random_player()
        self.set_pole(pole_player)
        return pole_player

    def set_pole(self, player: Player) -> None:
        self.pole = player

    def shuffle_deck(self) -> None:
        random.shuffle(self.deck)

    def progress_pole(self) -> None:
        next_player = self.get_next_player(self.get_pole_player())
        self.set_pole(next_player)

    def resolve_on_reveal(self) -> None:
        for resolving_card in self.get_played_cards():
            resolving_card.revealed = True
            resolving_card.on_reveal(self)

    def resolve_before_power(self) -> None:
        for resolving_card in self.get_played_cards():
            resolving_card.before_power(self)

    def begin_round(self) -> None:
        cleared_cards: Set[Card] = set()
        for c in self.blocked_cards:
            if self.blocked_cards[c] <= 0:
                cleared_cards.add(c)
            self.blocked_cards[c] -= 1

        for c in cleared_cards:
            del self.blocked_cards[c]

        # Flush old cards.
        self.played_cards = []
        self.round_winner = None
        self.round_winning_card = None

        for p in self.players:
            assert self.starting_hand_size - p.hand_size() == len(
                self.graveyard[p]
            ), f"Player does not have the right number of cards on hand! Starting hand size: {self.starting_hand_size} | {p} Hand: {p.hand} | Graveyard: {self.graveyard[p]} | "

    def commit_card(self, player: Player, card: Card, order: Order):
        if card.legendary:
            self.blocked_cards[card] = 1
        self.played_cards.append(PlayedCard(player, card, order))

    def number_of_players(self) -> int:
        return len(self.players)

    def valid_plays(self, cards: List[Card]) -> List[Card]:
        valid_cards = [c for c in cards if c not in self.blocked_cards]
        return valid_cards

    def player_picks(
        self, player: Player, items: List[Any], num: int = 1
    ) -> Union[List[Any], Any]:
        if num == 1:
            return random.choice(items)
        else:
            return random.sample(items, num)

    def get_players_played_card(self, player: Player) -> PlayedCard:
        for ac in self.played_cards:
            if ac.player != player:
                continue

            return ac

        raise RuntimeError("Player haven't played a card this round!")

    def get_previous_player(self, player: Player) -> Player:
        origin_player_index = self.players.index(player)
        return self.players[origin_player_index - 1 % self.number_of_players()]

    def get_played_cards(self):
        start_index = self.get_pole_index()
        for i in range(self.number_of_players()):
            yield self.played_cards[(start_index + i) % len(self.played_cards)]

    def player_picks_opponent(self, player: Player) -> Player:
        opponents = self.get_opponents(player)
        return self.player_picks(player, opponents)

    def deal_cards(self) -> None:
        for player in self.players:
            for _ in range(self.starting_hand_size):
                card = self.deck.pop()
                player.add_card_to_hand(card)

        assert player.hand_size() == self.starting_hand_size

    def draw_card(self) -> Card:
        # TODO(_): Undefined behavior when deck is empty.
        return self.deck.popleft()

    def get_opponents(self, player: Player) -> List[Player]:
        return [p for p in self.players if p != player]

    def get_random_player(self) -> Player:
        return random.choice(self.players)

    def get_random_opponent(self, player: Player) -> Player:
        return random.choice(self.get_opponents(player))

    def cycle_event(self, triggering_player: Player) -> None:
        falling_behind_players = self.all_players_except_winner(triggering_player)

        cycled_cards = []
        for player in falling_behind_players:
            cycled_card = self.cycle_for_player(player)
            cycled_cards.append(cycled_card)
        self.add_cycled_cards_to_bottom_of_deck(cycled_cards)

    def cycle_for_player(self, player: Player) -> Card:
        random_card = player.get_random_card_from_hand()

        self.player_cycle_card(player, random_card)

        return random_card

    def player_cycle_card(self, player: Player, card: Card):
        player.remove_card_from_hand(card)
        card.on_cycle(self, player)

    def put_card_at_bottom_of_deck(self, card: Card) -> None:
        self.deck.append(card)

    def players_in_pole_order_from_player(self, player: Player) -> List[Player]:
        start_index = self.players.index(player)
        for i in range(self.number_of_players()):
            yield self.players[(i + start_index) % self.number_of_players()]

    def get_pole_index(self) -> int:
        return next(
            index
            for index, ac in enumerate(self.played_cards)
            if ac.player == self.pole
        )

    def get_pole_card(self) -> PlayedCard:
        pole_index = self.get_pole_index()
        return self.played_cards[pole_index]

    def all_players_except_winner(self, winning_player: Player) -> List[Player]:
        return [p for p in self.players if p != winning_player]

    def resolved_order(self) -> Order:
        orders = [c.order for c in self.played_cards]
        num_attack = 0
        num_defense = 0
        for order in orders:
            if order == Order.attack:
                num_attack += 1
            elif order == Order.defense:
                num_defense += 1

        assert num_attack + num_defense == len(self.played_cards)

        # Tie
        if num_attack > num_defense:
            return Order.attack
        elif num_defense > num_attack:
            return Order.defense
        elif num_attack == num_defense:
            pole_played_card = self.get_pole_card()
            return pole_played_card.order

        raise RuntimeError("Unreachable")

    def get_pole_player(self) -> Player:
        return self.pole

    def get_opponent_played_cards(self, player: Player) -> List[PlayedCard]:
        return [ac for ac in self.get_played_cards() if ac.player != player]

    def get_next_player(self, player: Player) -> Player:
        start_index = self.players.index(player)
        return self.players[(start_index + 1) % self.number_of_players()]

    def get_card_index(self, card: Card) -> int:
        return next(idx for idx, ac in enumerate(self.played_cards) if ac.card == card)

    def swap_ownage_of_played_cards(self, card1: Card, card2: Card) -> None:
        index_card1 = self.get_card_index(card1)
        index_card2 = self.get_card_index(card2)

        tmp_card = self.played_cards[index_card1].card
        self.played_cards[index_card1].card = self.played_cards[index_card2].card
        self.played_cards[index_card2].card = tmp_card

        self.played_cards[index_card1]

    def resolve_power(self) -> PlayedCard:
        best_card = None

        def is_better(a: Card, b: Card):
            a.power_resolve()
            b.power_resolve()
            # Is card _a_ better than card _b_?
            if self.resolved_order() == Order.defense:
                # Lower is better.
                return a.power < b.power
            else:
                # Higher is better.
                return a.power > b.power

        for played_card in self.get_played_cards():
            if not best_card or is_better(played_card.card, best_card.card):
                best_card = played_card

        if not best_card:
            raise RuntimeError(f"Unable to find best card! Board: {self}")

        self.set_round_winner(best_card.player)
        self.set_round_winning_card(best_card.card.copy())
        self.victories[best_card.player] += 1

        return best_card.card

    def add_to_graveyard(self, player: Player, card: Card) -> None:
        self.graveyard[player].append(card)

    def set_round_winner(self, player: Player) -> None:
        self.round_winner = player

    def set_round_winning_card(self, card: Card) -> None:
        self.round_winning_card = card

    def is_losing_card(self, card: Card) -> bool:
        return self.round_winning_card != card

    def is_opponent_card(self, card: Card, player: Player) -> bool:
        ac = next(c for c in self.played_cards if c.card == card)
        return ac.player != player

    def add_cycled_cards_to_bottom_of_deck(self, cycled_cards: List[Card]):
        self.deck.extend(cycled_cards)

    def losing_cards(self) -> List[PlayedCard]:
        all_cards = self.played_cards
        return [c for c in all_cards if c.card != self.round_winning_card]

    def trade(self, player1: Player, card1: Card, player2: Player, card2: Card) -> None:
        assert card1 in player1.hand
        assert card2 in player2.hand

        index1, _ = player1.remove_card_from_hand(card1)
        index2, _ = player2.remove_card_from_hand(card2)

        player1.add_card_to_hand(card2, index=index1)
        player2.add_card_to_hand(card1, index=index2)

        assert card2 in player1.hand
        assert card1 in player2.hand

    def __repr__(self):
        return f"Pole: {self.pole}\nResolved order: {self.resolved_order()}"
