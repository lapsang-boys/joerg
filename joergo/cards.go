package joerg

import (
	"log"
)

type Ant struct{ Card }
type Anteater struct{ Card }
type Bee struct{ Card }
type BigLeggedHare struct{ Card }
type Bloodhound struct{ Card }
type BlueTit struct{ Card }
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
type StagBeetle struct{ Card }
type SupressedPerch struct{ Card }
type Swan struct{ Card }
type Toad struct{ Card }
type UrsaMinor struct{ Card }
type Weasel struct{ Card }
type Wolverine struct{ Card }

func (bt BlueTit) OnReveal(b *Board, p *Player, order Order) {
	log.Println("reveal")
}
