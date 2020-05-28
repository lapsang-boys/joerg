import json
from collections import deque
from typing import Deque, List

from board import Board, PlayerStates
from cards.card import Card
from log import new_logger
from order import Order
from played_card import PlayedCard
from player import Player, HandCardState

LOGGER = new_logger("cards")


def name(n: str):
    def wrapper_name(func):
        def wrapper_func(*args, **kwargs):
            return (n, func(*args, **kwargs))

        return wrapper_func

    return wrapper_name


@name("Räv")
class Fox(Card):
    def __init__(self):
        super().__init__()

    def on_win(self, board: Board, player: Player, order: Order):
        opponents = board.get_opponents(player)
        a, b = player.player_picks(opponents, 2)
        a_card: Card = a.player_picks(a.hand)
        b_card: Card = b.player_picks(b.hand)
        board.trade(a, a_card, b, b_card)

        LOGGER.info(
            f"{player} won with {self.name}: Forced trade! {a} trades {a_card} for {b}'s {b_card}"
        )


@name("Falken")
class Falcon(Card):
    def __init__(self):
        super().__init__()

    def on_win(self, board: Board, player: Player, order: Order):
        opponent = player.player_picks_opponent()
        LOGGER.info(f"{player} won with {self.name}")
        for card in opponent.hand:
            LOGGER.info(f"\t{self.name} sees: {card}")

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- Falcon on_reveal")


@name("Biet")
class Bee(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        opponent = player.player_picks(board.get_opponents(player))
        random_card = opponent.get_random_card_from_hand()
        opponent.set_card_visible(random_card)
        LOGGER.info(
            f"{player} lost with {self.name}: {opponent}'s {random_card} is now visible!"
        )


@name("Fjäril")
class Butterfly(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        tmp_pole_player = board.get_previous_player(player)
        board.set_pole(tmp_pole_player)
        LOGGER.info(
            f"{player} lost with {self.name}: {player} will get pole next turn!"
        )


@name("Gamle älgen")
class OldElk(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        # On Lose: Byt detta kort mot en motspelares kort som också förlorade.
        opponent_played_cards = board.get_opponent_played_cards(player)
        opponent_losing_cards = [
            c for c in opponent_played_cards if board.is_losing_card(c.card)
        ]
        chosen_card: PlayedCard = player.player_picks(opponent_losing_cards)
        LOGGER.info(
            f"{player} lost with {self.name}: {self.name} swapped with another losing card: {chosen_card.player}'s {chosen_card.card}"
        )
        board.swap_ownage_of_played_cards(self, chosen_card.card)


@name("Skatan")
class Magpie(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        LOGGER.debug("MAGPIE LOST!")
        # On Lose: Cycle Skatan, and all players puts 1 card from their hand
        # into 1 pile. Owner of Skatan picks 1 card and returns the rest
        # randomly.

        pile: List[Card] = []
        index = board.get_card_index(self)
        magpie = board.played_cards[index]

        board.put_card_at_bottom_of_deck(magpie.card.copy())
        new_card = board.draw_card()
        pile.append(new_card)

        LOGGER.info(f"{player} lost with {self.name}!")
        for opponent in board.get_opponents(player):
            throw_away_card = opponent.player_picks(opponent.hand)
            opponent.remove_card_from_hand(throw_away_card)
            LOGGER.info(f"\t{opponent} throws away {throw_away_card}")
            pile.append(throw_away_card)

        LOGGER.info("Picking time!")
        for picking_player in board.players_in_pole_order_from_player(player):
            chosen_card = picking_player.player_picks(pile)
            LOGGER.info(f"\t{picking_player} picks {chosen_card}")
            if picking_player == player:
                board.played_cards[index].card = chosen_card
            else:
                picking_player.add_card_to_hand(chosen_card)

            pile.remove(chosen_card)

        assert len(pile) == 0, "Player didn't pick from magpie pile!"


@name("Mullvaden")
class Mole(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        def flatten(a):
            return sum(a, [])

        possible_cards = [
            c
            for c in flatten([cs for cs in board.graveyard.values()])
            if c.power < self.power
        ]
        LOGGER.info(f"{player} lost with {self.name}!")
        if not possible_cards:
            LOGGER.info(f"{self.name} has no valid targets!")
            return

        mole_index = board.get_card_index(self)
        chosen_card = player.player_picks(possible_cards)
        for p in board.graveyard:
            if chosen_card in board.graveyard[p]:
                index = board.graveyard[p].index(chosen_card)
                board.graveyard[p].pop(index)
                board.graveyard[p].insert(index, self)
                LOGGER.info(f"{self.name} swapped with {chosen_card}")
                break

        board.played_cards[mole_index].card = chosen_card


# HERE ---------------------------------------------------------------------------


@name("Förtryckt Aborre")
class SupressedPerch(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- SupressedPerch on_reveal")


@name("Paddan")
class Toad(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        # Överraskning: Välj ett av motståndare spelat kort, och välj sedan en
        # till spelare (får inte vara ägaren av kortet). Denna spelare byter ett
        # kort i sin hand mot the valda kortet.
        opponents_cards = board.get_opponent_played_cards(player)
        chosen_card: PlayedCard = player.player_picks(opponents_cards)

        not_chosen_cards_players = board.get_opponents(chosen_card.player)
        chosen_player: Player = player.player_picks(not_chosen_cards_players)

        chosen_card_from_hand: Card = chosen_player.player_picks(chosen_player.hand)
        chosen_player.remove_card_from_hand(chosen_card_from_hand)

        LOGGER.info(
            f"{player} played {self.name}: Swapping {chosen_card.player}'s {chosen_card.card} with {chosen_player}'s {chosen_card_from_hand}"
        )
        tmp_card = chosen_card.card.copy()
        chosen_card.card = chosen_card_from_hand
        chosen_player.add_card_to_hand(tmp_card)


@name("Igelkotten")
class Hedgehog(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- Hedgehog on_reveal")


@name("Myrslok")
class Anteater(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- Anteater on_reveal")


@name("Uttern")
class Otter(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- Otter on_reveal")


@name("Groda")
class Frog(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.info("Frog on_reveal")
        # Target opponent swaps card with one in their hand.
        opponent: Player = player.player_picks(board.get_opponents(player))

        chosen_card: Card = opponent.player_picks(opponent.hand)
        opponent.remove_card_from_hand(chosen_card)

        opponents_card = board.get_players_played_card(opponent)
        LOGGER.info(f"Swapping {opponents_card.card} with {chosen_card}")
        tmp_card = opponents_card.card.copy()
        opponents_card.card = chosen_card
        opponent.add_card_to_hand(tmp_card)


@name("Sälspion")
class SpySeal(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- SpySeal on_reveal")


@name("Ekorren")
class Squirrel(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- Squirrel on_reveal")


@name("Fiskmås")
class Seagull(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- Seagull on_reveal")


@name("Vildsvinet")
class Boar(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        # Överraskning: Du spelar nästa runda blint (korten upp och ner). Man
        # kan inte vinna sista sticket med detta kort.",
        LOGGER.info(f"{player} reveals {self.name}!")
        for card in player.hand:
            player.set_card_hidden(card)

        def restore_hand():
            for card in player.hand:
                # Only restore hidden cards, if they have changed in some other
                # way. They will keep being that way!
                if player.hand_states[card] == HandCardState.HiddenFromEveryone:
                    player.set_card_default(card)

        board.player_states[player].add_state(
            PlayerStates.HandFaceDown, 1, restore_hand
        )
        board.player_states[player].add_state(
            PlayerStates.UnableToWin, 0, lambda: print("UnableToWin cleared")
        )


@name("Storbent hare")
class BigLeggedHare(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- BigLeggedHare on_reveal")


@name("Igelkotten 2 - The Return of Glen")
class Hedgehog2TheReturnofGlen(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- Hedgehog2TheReturnofGlen on_reveal")


@name("Vässlan")
class Weasel(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- Weasel on_reveal")


@name("Myggan")
class Mosquito(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.info("Mosquito on_reveal")
        # Överraskning: Byt detta kort mot ett slumpmässigt kort i valfri spelares hand.
        opponents = board.get_opponents(player)
        opponent: Player = player.player_picks(opponents)

        random_card = opponent.get_random_card_from_hand()
        opponent.remove_card_from_hand(random_card)

        LOGGER.info(f"{self} swapped with {opponent}'s {random_card}")
        mygga_ac = board.get_players_played_card(player)
        tmp_card = mygga_ac.card.copy()
        mygga_ac.card = random_card
        opponent.add_card_to_hand(tmp_card)


@name("Hungrig Varg")
class HungryWolf(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- HungryWolf on_reveal")


@name("Skogens Konung")
class KingoftheForest(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self, board: Board, player: Player, order: Order):
        LOGGER.debug("NOT IMPLEMENTED -- KingoftheForest on_reveal")


@name("Blodhund")
class Bloodhound(Card):
    def __init__(self):
        super().__init__()

    def on_cycle(self, board: Board, player: Player) -> None:
        LOGGER.debug("Bloodhound cycle")
        chosen_card = player.player_picks(board.deck)
        board.deck.remove(chosen_card)
        LOGGER.debug(f"Chosen_card {chosen_card}")
        player.add_card_to_hand(chosen_card)


@name("Tuppen")
class Rooster(Card):
    def __init__(self):
        super().__init__()

    def on_hand_enter(self):
        LOGGER.debug("NOT IMPLEMENTED -- Rooster on_hand_enter")


@name("Lilla Björn")
class UrsaMinor(Card):
    def __init__(self):
        super().__init__()

    def before_power(self, board: Board, player: Player, order: Order):
        # Innan styrka tar effekt vid strid, välj en ny Polstjärneposition. Legendary.
        LOGGER.debug("UrsaMinor before_power")
        new_pole_player = player.player_picks(board.players)
        board.set_pole(new_pole_player)


@name("Svan")
class Swan(Card):
    def __init__(self):
        super().__init__()

    def power_resolve(self):
        LOGGER.debug("NOT IMPLEMENTED -- swan power_resolve")


@name("Myra")
class Ant(Card):
    def __init__(self):
        super().__init__()


@name("Järv")
class Wolverine(Card):
    def __init__(self):
        super().__init__()


@name("Ekoxe")
class StagBeetle(Card):
    def __init__(self):
        super().__init__()


@name("Blåmes")
class BlueTit(Card):
    def __init__(self):
        super().__init__()


_LOOKUP = dict(
    [
        Ant(),
        Anteater(),
        Bee(),
        BigLeggedHare(),
        Bloodhound(),
        BlueTit(),
        Boar(),
        Butterfly(),
        Falcon(),
        Fox(),
        Frog(),
        Hedgehog(),
        Hedgehog2TheReturnofGlen(),
        HungryWolf(),
        KingoftheForest(),
        Magpie(),
        Mole(),
        Mosquito(),
        OldElk(),
        Otter(),
        Rooster(),
        Seagull(),
        SpySeal(),
        Squirrel(),
        StagBeetle(),
        SupressedPerch(),
        Swan(),
        Toad(),
        UrsaMinor(),
        Weasel(),
        Wolverine(),
    ]
)


def json_read_card(payload):
    name = payload.get("name")
    assert name

    card_class = _LOOKUP.get(name)
    assert card_class, f"Missing in lookup: {name}"

    return card_class.from_json(payload)


class InvalidLibraryFileError(Exception):
    def __init__(self, msg="Unable to read 'cards' field from library."):
        super().__init__(msg)


def read_cards(library_path: str) -> Deque[Card]:
    with open(library_path, "r") as fp:
        raw_object = json.load(fp)

    raw_cards = raw_object.get("cards", None)
    if not raw_cards:
        raise InvalidLibraryFileError()

    cards = [json_read_card(rc) for rc in raw_cards]
    assert len(cards) == len(
        set(cards)
    ), "Name collision in library! Two cards with same name."

    return deque(cards)
