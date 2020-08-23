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

func (m Mosquito) OnReveal(b *Board, p *Player, order Order) {
	// Överraskning: Byt detta kort mot ett slumpmässigt kort i valfri spelares hand.
	// log.Printf("%s reveals %s", p.Name, m.Name())
	// opponent, err := p.PickPlayer(b.Opponents(p), fmt.Sprintf("Pick a player, %s will be swapped with a random card from their hand.", m.Name()))
	// if err != nil {
	// 	log.Println(err)
	// 	return
	// }

	// randomCard := opponent.RandomCardInHand()
	// opponent.RemoveCardFromHand(randomCard)

	// log.Printf("%s swapped with %s's %s", m.Name(), opponent.Name, randomCard.Name())
	// myggaAc := b.PlayersPlayedCard(p)
	// opponent.AddCardToHand(myggaAc.Card)
	// myggaAc.Card = randomCard
}
