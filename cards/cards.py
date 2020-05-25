import json
from collections import deque
from typing import Deque, List

from active_card import ActiveCard
from board import Board
from cards.card import Card
from log import new_logger
from order import Order
from player import Player

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
        a, b = board.player_picks(player, opponents, 2)
        a_card: Card = board.player_picks(a, a.hand)
        b_card: Card = board.player_picks(b, b.hand)
        board.trade(a, a_card, b, b_card)

        LOGGER.debug("FOX WON! Trade has been made!")


@name("Falken")
class Falcon(Card):
    def __init__(self):
        super().__init__()

    def on_win(self, board: Board, player: Player, order: Order):
        LOGGER.debug("FALCON WON!")
        opponent = board.player_picks_opponent(player)
        for card in opponent.hand:
            LOGGER.debug(f"FALCON SEES: {card}")

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Falcon on_reveal")


@name("Biet")
class Bee(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        LOGGER.debug("BEE LOST!")
        opponent = board.player_picks_opponent(player)
        random_card = opponent.get_random_card_from_hand()
        opponent.set_card_visible(random_card)


@name("Fjäril")
class Butterfly(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        LOGGER.debug("BUTTERFLY LOST!")
        tmp_pole_player = board.get_previous_player(player)
        board.set_pole(tmp_pole_player)
        LOGGER.debug(f"Make {player} pole next turn!")


@name("Gamle älgen")
class OldElk(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        LOGGER.debug("OLDELK LOST!")
        # On Lose: Byt detta kort mot en motspelares kort som också förlorade.
        opponent_played_cards = board.get_opponent_played_cards(player)
        opponent_losing_cards = [
            c for c in opponent_played_cards if board.is_losing_card(c.card)
        ]
        chosen_card: ActiveCard = board.player_picks(player, opponent_losing_cards)
        LOGGER.debug(f"Chosen card: {chosen_card}")
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

        for opponent in board.get_opponents(player):
            throw_away_card = board.player_picks(opponent, opponent.hand)
            opponent.remove_card_from_hand(throw_away_card)
            pile.append(throw_away_card)

        for picking_player in board.players_in_pole_order_from_player(player):
            chosen_card = board.player_picks(picking_player, pile)
            LOGGER.debug(chosen_card, picking_player, pile)
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

        LOGGER.debug("MOLE LOST!")
        possible_cards = [
            c
            for c in flatten([cs for cs in board.graveyard.values()])
            if c.power < self.power
        ]
        if not possible_cards:
            LOGGER.info("MOLE: No valid targets!")
            return

        mole_index = board.get_card_index(self)
        chosen_card = board.player_picks(player, possible_cards)
        for p in board.graveyard:
            if chosen_card in board.graveyard[p]:
                index = board.graveyard[p].index(chosen_card)
                board.graveyard[p].pop(index)
                board.graveyard[p].insert(index, self)
                LOGGER.debug(f"Swapped with card: {chosen_card}")
                break

        board.played_cards[mole_index].card = chosen_card


# HERE ---------------------------------------------------------------------------


@name("Förtryckt Aborre")
class SupressedPerch(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- SupressedPerch on_reveal")


@name("Paddan")
class Toad(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Toad on_reveal")


@name("Igelkotten")
class Hedgehog(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Hedgehog on_reveal")


@name("Myrslok")
class Anteater(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Anteater on_reveal")


@name("Uttern")
class Otter(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Otter on_reveal")


@name("Groda")
class Frog(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Frog on_reveal")


@name("Sälspion")
class SpySeal(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- SpySeal on_reveal")


@name("Ekorren")
class Squirrel(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Squirrel on_reveal")


@name("Fiskmås")
class Seagull(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Seagull on_reveal")


@name("Vildsvinet")
class Boar(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Boar on_reveal")


@name("Storbent hare")
class BigLeggedHare(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- BigLeggedHare on_reveal")


@name("Igelkotten 2 - The Return of Glen")
class Hedgehog2TheReturnofGlen(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Hedgehog2TheReturnofGlen on_reveal")


@name("Vässlan")
class Weasel(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Weasel on_reveal")


@name("Myggan")
class Mosquito(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- Mosquito on_reveal")


@name("Hungrig Varg")
class HungryWolf(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- HungryWolf on_reveal")


@name("Skogens Konung")
class KingoftheForest(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("NOT IMPLEMENTED -- KingoftheForest on_reveal")


@name("Blodhund")
class Bloodhound(Card):
    def __init__(self):
        super().__init__()

    def on_cycle(self, board: Board, player: Player) -> None:
        LOGGER.debug("Bloodhound cycle")
        chosen_card = board.player_picks(player, board.deck)
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
        new_pole_player = board.player_picks(player, board.players)
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
