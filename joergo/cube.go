package joerg

import (
	"encoding/json"
	"io/ioutil"
)

type Cube struct {
	Cards []Carder `json:"cards"`
}

func lookup(card Card) Carder {
	switch card.Name() {
	case "Biet":
		return Bee{card}
	case "Blodhund":
		return Bloodhound{card}
	case "Blåmes":
		return BlueTit{card}
	case "Ekorren":
		return Squirrel{card}
	case "Ekoxe":
		return StagBeetle{card}
	case "Falken":
		return Falcon{card}
	case "Fiskmås":
		return Seagull{card}
	case "Fjäril":
		return Butterfly{card}
	case "Förtryckt Aborre":
		return SupressedPerch{card}
	case "Gamle älgen":
		return OldElk{card}
	case "Groda":
		return Frog{card}
	case "Hungrig Varg":
		return HungryWolf{card}
	case "Igelkotten 2 - The Return of Glen":
		return Hedgehog2TheReturnofGlen{card}
	case "Igelkotten":
		return Hedgehog{card}
	case "Järv":
		return Wolverine{card}
	case "Lilla Björn":
		return UrsaMinor{card}
	case "Mullvaden":
		return Mole{card}
	case "Myggan":
		return Mosquito{card}
	case "Myra":
		return Ant{card}
	case "Myrslok":
		return Anteater{card}
	case "Paddan":
		return Toad{card}
	case "Räv":
		return Fox{card}
	case "Skatan":
		return Magpie{card}
	case "Skogens Konung":
		return KingoftheForest{card}
	case "Storbent hare":
		return BigLeggedHare{card}
	case "Svan":
		return Swan{card}
	case "Sälspion":
		return SpySeal{card}
	case "Tuppen":
		return Rooster{card}
	case "Uttern":
		return Otter{card}
	case "Vildsvinet":
		return Boar{card}
	case "Vässlan":
		return Weasel{card}
	}
	panic("Unmapped card:" + card.Name())
}

func ReadCube(path string) (*Cube, error) {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var cards struct {
		Cards []Card
	}
	err = json.Unmarshal(buf, &cards)
	if err != nil {
		return nil, err
	}
	var cube = Cube{Cards: make([]Carder, 0, len(cards.Cards))}
	for _, c := range cards.Cards {
		card := lookup(c)
		cube.Cards = append(cube.Cards, card)
	}
	return &cube, nil
}
