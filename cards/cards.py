import json
from collections import deque
from typing import Deque

from board import Board
from cards.card import Card
from order import Order
from player import Player
from log import new_logger

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
        a_card = board.player_picks(a, a.hand)
        b_card = board.player_picks(b, b.hand)
        board.trade(a, a_card, b, b_card)

        LOGGER.info("FOX WON! Trade has been made!")


@name("Falken")
class Falcon(Card):
    def __init__(self):
        super().__init__()

    def on_win(self, board: Board, player: Player, order: Order):
        LOGGER.info("FALCON WON!")
        opponent = board.player_picks_opponent(player)
        for card in opponent.hand:
            LOGGER.info(f"FALCON SEES: {card}")

    def on_reveal(self):
        LOGGER.debug("Falcon on_reveal")


@name("Biet")
class Bee(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        LOGGER.info("BEE LOST!")
        opponent = board.player_picks_opponent(player)
        random_card = opponent.get_random_card_from_hand()
        opponent.set_card_visible(random_card)


@name("Fjäril")
class Butterfly(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        LOGGER.info("BUTTERFLY LOST!")
        tmp_pole_player = board.get_previous_player(player)
        board.set_pole(tmp_pole_player)
        LOGGER.info(f"Make {player} pole next turn!")


@name("Gamle älgen")
class OldElk(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        LOGGER.info("OLDELK LOST!")


@name("Skatan")
class Magpie(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self, board: Board, player: Player, order: Order):
        LOGGER.info("MAGPIE LOST!")


@name("Förtryckt Aborre")
class SupressedPerch(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("SupressedPerch on_reveal")


@name("Pilgiftsgroda")
class PoisonDartFrog(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("PoisonDartFrog on_reveal")


@name("Igelkotten")
class Hedgehog(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("Hedgehog on_reveal")


@name("Myrslok")
class Anteater(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("Anteater on_reveal")


@name("Uttern")
class Otter(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("Otter on_reveal")


@name("Groda")
class Frog(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("Frog on_reveal")


@name("Sälspion")
class SpySeal(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("SpySeal on_reveal")


@name("Ekorren")
class Squirrel(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("Squirrel on_reveal")


@name("Fiskmås")
class Seagull(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("Seagull on_reveal")


@name("Vildsvinet")
class Boar(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("Boar on_reveal")


@name("Storbent hare")
class BigLeggedHare(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("BigLeggedHare on_reveal")


@name("Igelkotten 2 - The Return of Glen")
class Hedgehog2TheReturnofGlen(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("Hedgehog2TheReturnofGlen on_reveal")


@name("Vässlan")
class Weasel(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("Weasel on_reveal")


@name("Myggan")
class Mosquito(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("Mosquito on_reveal")


@name("Hungrig Varg")
class HungryWolf(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("HungryWolf on_reveal")


@name("Skogens Konung")
class KingoftheForest(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        LOGGER.debug("KingoftheForest on_reveal")


@name("Blodhund")
class Bloodhound(Card):
    def __init__(self):
        super().__init__()

    def on_cycle(self):
        LOGGER.debug("Bloodhound cycle")


@name("Tuppen")
class Rooster(Card):
    def __init__(self):
        super().__init__()

    def on_hand_enter(self):
        LOGGER.debug("Rooster on_hand_enter")


@name("Lilla Björn")
class UrsaMinor(Card):
    def __init__(self):
        super().__init__()

    def before_power(self):
        LOGGER.debug("UrsaMinor before_power")


@name("Svan")
class Swan(Card):
    def __init__(self):
        super().__init__()

    def power_resolve(self):
        LOGGER.debug("swan power_resolve")


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
        Anteater(),
        Bee(),
        BigLeggedHare(),
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
        Mosquito(),
        OldElk(),
        Otter(),
        PoisonDartFrog(),
        Seagull(),
        SpySeal(),
        Squirrel(),
        SupressedPerch(),
        Weasel(),
        Bloodhound(),
        Rooster(),
        UrsaMinor(),
        Swan(),
        Ant(),
        Wolverine(),
        StagBeetle(),
        BlueTit(),
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
