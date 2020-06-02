package card

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

func (bt BlueTit) OnReveal() {
	log.Println("reveal")
}

type Carder interface {
	Power() int
	Name() string
	OnReveal()
	OnLose()
	OnWin()
	OnCycle()
	OnHandEnter()
	OnBeforePower()
}

type Card struct {
	Nam string `json:"name"`
	Pow int    `json:"power"`
	Rul string `json:"ruling"`
	Leg bool   `json:"legendary"`
	Fla string `json:"flavor"`
	Img string `json:"imgSrc"`
}

func (c Card) Power() int {
	return c.Pow
}
func (c Card) Name() string {
	return c.Nam
}

func (c Card) OnReveal()      {}
func (c Card) OnWin()         {}
func (c Card) OnLose()        {}
func (c Card) OnCycle()       {}
func (c Card) OnHandEnter()   {}
func (c Card) OnBeforePower() {}
