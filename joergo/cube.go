package joerg

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
)

// Cube is a custom deck of cards, often composed with a specific theme.
type Cube struct {
	// Cards contained within cube.
	Cards []Carder `json:"cards"`
}

// lookup returns the underlying implementation of the given card, which handles
// reveal actions and other card specific rules.
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
	default:
		panic(fmt.Errorf("support for card %q has not been implemented yet", card.Name()))
	}
}

// ReadCube reads the custom deck of cards specified in the given JSON file.
func ReadCube(jsonPath string) (*Cube, error) {
	buf, err := ioutil.ReadFile(jsonPath)
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
