from cards.card import Card


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

    def on_win(self):
        print("FOX WON!")


@name("Falken")
class Falcon(Card):
    def __init__(self):
        super().__init__()

    def on_win(self):
        print("FALCON WON!")

    def on_reveal(self):
        print("Falcon on_reveal")


@name("Biet")
class Bee(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self):
        print("BEE LOST!")


@name("Fjäril")
class Butterfly(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self):
        print("BUTTERFLY LOST!")


@name("Gamle älgen")
class OldElk(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self):
        print("OLDELK LOST!")


@name("Skatan")
class Magpie(Card):
    def __init__(self):
        super().__init__()

    def on_lose(self):
        print("MAGPIE LOST!")


@name("Förtryckt Aborre")
class SupressedPerch(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("SupressedPerch on_reveal")


@name("Pilgiftsgroda")
class PoisonDartFrog(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("PoisonDartFrog on_reveal")


@name("Igelkotten")
class Hedgehog(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("Hedgehog on_reveal")


@name("Myrslok")
class Anteater(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("Anteater on_reveal")


@name("Uttern")
class Otter(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("Otter on_reveal")


@name("Groda")
class Frog(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("Frog on_reveal")


@name("Sälspion")
class SpySeal(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("SpySeal on_reveal")


@name("Ekorren")
class Squirrel(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("Squirrel on_reveal")


@name("Fiskmås")
class Seagull(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("Seagull on_reveal")


@name("Vildsvinet")
class Boar(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("Boar on_reveal")


@name("Storbent hare")
class BigLeggedHare(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("BigLeggedHare on_reveal")


@name("Igelkotten 2 - The Return of Glen")
class Hedgehog2TheReturnofGlen(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("Hedgehog2TheReturnofGlen on_reveal")


@name("Vässlan")
class Weasel(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("Weasel on_reveal")


@name("Myggan")
class Mosquito(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("Mosquito on_reveal")


@name("Hungrig Varg")
class HungryWolf(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("HungryWolf on_reveal")


@name("Skogens Konung")
class KingoftheForest(Card):
    def __init__(self):
        super().__init__()

    def on_reveal(self):
        print("KingoftheForest on_reveal")


@name("Blodhund")
class Bloodhound(Card):
    def __init__(self):
        super().__init__()

    def on_cycle(self):
        print("Bloodhound cycle")


@name("Tuppen")
class Rooster(Card):
    def __init__(self):
        super().__init__()

    def on_hand_enter(self):
        print("Rooster on_hand_enter")


@name("Lilla Björn")
class UrsaMinor(Card):
    def __init__(self):
        super().__init__()

    def before_power(self):
        print("UrsaMinor before_power")


@name("Svan")
class Swan(Card):
    def __init__(self):
        super().__init__()

    def power_resolve(self):
        print("swan power_resolve")


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
