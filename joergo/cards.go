package joerg

import (
	"log"
)

type Ant struct{ Card }
type Anteater struct{ Card }
type Bee struct{ Card }
type BigLeggedHare struct{ Card }
type Bloodhound struct{ Card }
type BlueTit struct{ Card } // Done.
type Boar struct{ Card }
type Butterfly struct{ Card }
type Falcon struct{ Card }
type Fox struct{ Card }
type Frog struct{ Card }
type Hedgehog struct{ Card }
type Hedgehog2TheReturnofGlen struct{ Card }
type HungryWolf struct{ Card }
type KingoftheForest struct{ Card }
type Magpie struct{ Card }
type Mole struct{ Card }
type Mosquito struct{ Card }
type OldElk struct{ Card }
type Otter struct{ Card }
type Rooster struct{ Card }
type Seagull struct{ Card }
type SpySeal struct{ Card }
type Squirrel struct{ Card }
type StagBeetle struct{ Card } // Done.
type SupressedPerch struct{ Card }
type Swan struct{ Card }
type Toad struct{ Card }
type UrsaMinor struct{ Card }
type Weasel struct{ Card }
type Wolverine struct{ Card } // Done.

func (um UrsaMinor) OnBeforePower(b *Board, p *Player, order Order) {
	// Innan styrka tar effekt vid strid, välj en ny Polstjärneposition. Legendary.
	log.Printf("%s's %s resolves before power", p.Name, um.Name())
	chosenPlayer, err := p.PickPlayer(b.Players, "Pick player to receive pole _before_ power is resolved.")
	if err != nil {
		log.Println(err)
		return
	}
	b.SetPole(chosenPlayer)
	log.Printf("%s chose %s to gain pole before power resolves", p.Name, chosenPlayer.Name)
}
}
