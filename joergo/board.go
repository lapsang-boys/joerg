package joerg

import (
	"errors"
	"fmt"
	"log"
	"math/rand"
)

const (
	LIBRARY_PATH    = "../cards.json"
	MINIMUM_PLAYERS = 3
	MAXIMUM_PLAYERS = 6
)

// https://play.golang.org/p/i1BGlRsP19
type Board struct {
	Players          []*Player    `json:"players"`
	Pole             *Player      `json:"pole"`
	Cube             *Cube        `json:"cube"`
	Deck             []Carder     `json:"deck"` // Make private later.
	PlayedCards      []PlayedCard `json:"playedCards"`
	RoundWinner      *Player      `json:"roundWinner"`
	RoundWinningCard Carder       `json:"roundWinningCard"`
	NumPlayers       uint         `json:"numPlayers"`
	StartingHandSize uint         `json:"startingHandSize"`
	WinsNeeded       uint         `json:"winsNeeded"`
	BestCard         *PlayedCard  `json:"bestCard"` // Make private later.
	Victories        map[int]int  `json:"victories"`
}

func NewBoard(
	startingHandSize uint,
	winsNeeded uint,
	players []*Player,
) (*Board, error) {
	numPlayers := len(players)
	cube, err := ReadCube(LIBRARY_PATH)
	if err != nil {
		return nil, err
	}

	if numPlayers < MINIMUM_PLAYERS || numPlayers > MAXIMUM_PLAYERS {
		return nil, errors.New("illegal number of numPlayers")
	}
	if winsNeeded == 0 || winsNeeded > startingHandSize {
		return nil, errors.New("illegal winsNeeded")
	}
	if int(startingHandSize)*numPlayers > len(cube.Cards)-int(numPlayers) {
		return nil, errors.New("illegal startingHandSize")
	}

	victories := make(map[int]int)
	for _, p := range players {
		victories[p.Num] = 0
	}

	b := Board{
		Players:          players,
		NumPlayers:       uint(numPlayers),
		StartingHandSize: startingHandSize,
		WinsNeeded:       winsNeeded,
		Cube:             cube,
		Deck:             cube.Cards,
		Victories:        victories,
	}
	return &b, nil
}

func (b *Board) AddPlayer(p *Player) (err error) {
	if len(b.Players) == int(b.NumPlayers) {
		return errors.New("unable to add any more players(!)")
	}
	b.Players = append(b.Players, p)
	return nil
}

func (b *Board) AddBotPlayer() (err error) {
	return nil
}

func (b *Board) Next() {
	fmt.Println("Board next called!")
}

func (b *Board) RandomlyAssignPole() {
	b.Pole = b.Players[rand.Intn(len(b.Players))]
}

func (b *Board) ShuffleDeck() {
	rand.Shuffle(len(b.Deck), func(i, j int) {
		b.Deck[i], b.Deck[j] = b.Deck[j], b.Deck[i]
	})
}

func (b *Board) DealCards() {
	for _, p := range b.Players {
		p.Hand = b.Deck[:b.StartingHandSize]
		b.Deck = b.Deck[b.StartingHandSize:]
	}
}

func (b *Board) ResolveOnReveal() {
	log.Println("ResolveOnReveal")
	for _, pc := range b.PlayedCards {
		pc.Revealed = true
		pc.Card.OnReveal(b, pc.Player)
		log.Println(pc.Card)
	}
}

func (b *Board) ResolveWinLose() {
	log.Println("ResolveOnReveal")
	for _, pc := range b.PlayedCards {
		if pc.Card.Name() == b.RoundWinningCard.Name() {
			pc.Card.OnWin()
		} else {
			pc.Card.OnLose()
		}
	}
}

func (b *Board) EndResolvePhase() {
	b.ReturnLosingCards()
	b.PlayedCards = []PlayedCard{}
}

func (b *Board) LosingCards() (pcs []PlayedCard) {
	for _, pc := range b.PlayedCards {
		if pc.Card.Name() == b.RoundWinningCard.Name() {
			continue
		}
		pcs = append(pcs, pc)
	}
	return pcs
}

func (b *Board) ReturnLosingCards() {
	for _, pc := range b.LosingCards() {
		pc.Player.AddCardToHand(pc.Card)
	}
}

func (b *Board) AllPlayersExceptWinner() (ps []*Player) {
	for _, p := range b.Players {
		if p.Name == b.RoundWinner.Name {
			continue
		}
		ps = append(ps, p)
	}
	return ps
}

func (b *Board) AddCycledCardsToBottomOfDeck(cycledCards []Carder) {
	b.Deck = append(b.Deck, cycledCards...)
}

func (b *Board) cycleEvent(trgP *Player) error {
	fallingBehind := b.AllPlayersExceptWinner()

	cycledCards := []Carder{}
	for _, p := range fallingBehind {
		cycledCard, err := b.cycleForPlayer(p)
		if err != nil {
			return err
		}
		cycledCards = append(cycledCards, cycledCard)
	}
	b.AddCycledCardsToBottomOfDeck(cycledCards)
	return nil
}

func (b *Board) cycleForPlayer(p *Player) (Carder, error) {
	selection := make([]interface{}, 0, len(p.Hand))
	for _, c := range p.Hand {
		selection = append(selection, c)
	}
	chosenCardInt, err := p.Picks(selection, "Chose card to cycle.", 1)
	if err != nil {
		return nil, err
	}
	chosenCard, ok := chosenCardInt.(Carder)
	if !ok {
		return nil, errors.New("unable to type assert cycled card")
	}

	p.RemoveCardFromHand(chosenCard)

	newCard := b.DrawCard()
	p.AddCardToHand(newCard)

	return chosenCard, nil
}

func (b *Board) DrawCard() Carder {
	if len(b.Deck) < 1 {
		panic("DrawCard: no cards to draw!")
	}
	tmp := b.Deck[0]
	b.Deck = b.Deck[1:]
	return tmp
}

// def cycle_for_player(self, player: Player) -> Card:
//     chosen_card = player_picks(player.hand, "Chose card to cycle.")

//     self.player_cycle_card(player, chosen_card)

//     return chosen_card

// def player_cycle_card(self, player: Player, card: Card):
//     player.remove_card_from_hand(card)
//     card.on_cycle(self, player)

func (b *Board) PlayerWillWinNextRound(p *Player) bool {
	return b.Victories[p.Num] == int(b.WinsNeeded)-1
}

func (b *Board) CyclePhase() error {
	if b.RoundWinner != nil && b.PlayerWillWinNextRound(b.RoundWinner) {
		if err := b.cycleEvent(b.RoundWinner); err != nil {
			return err
		}
	}
	return nil
}

func (b *Board) ProgressPole() {
	b.Pole = b.NextPlayer(b.Pole)
}

func (b *Board) NextPlayer(p *Player) *Player {
	return b.Players[(p.Num+1)%len(b.Players)]
}

func (b *Board) EndRound() {
	// Update blocked cards.
	// Update player statuses.
}

func (b *Board) ResolveBeforePower() {
	log.Println("ResolveBeforePower")
	for _, pc := range b.PlayedCards {
		log.Println(pc)
	}
}

func (b *Board) PoleCard() PlayedCard {
	fmt.Println(b.PlayedCards)
	return b.PlayedCards[b.Pole.Num]
}

func (b *Board) ResolveOrder() Order {
	atk, def := 0, 0
	for _, pc := range b.PlayedCards {
		if pc.Order == OrderAttack {
			atk += 1
		} else if pc.Order == OrderDefense {
			def += 1
		}
	}

	if atk+def != len(b.PlayedCards) {
		log.Println("Something went wrong!")
	}

	if atk > def {
		return OrderAttack
	} else if def > atk {
		return OrderDefense
	} else if atk == def {
		polePc := b.PoleCard()
		return polePc.Order
	}
	panic("Unreachable")
}

func (b *Board) PlayedCardsInOrder() []PlayedCard {
	cards := make([]PlayedCard, 0, len(b.Players))
	for i := 0; i < len(b.Players); i++ {
		c := b.PlayedCards[(i+b.Pole.Num)%len(b.Players)]
		cards = append(cards, c)
	}
	return cards
}

func (b *Board) ResolvePower() {
	var bestCard *PlayedCard
	log.Println("ResolvePower")
	defCmp := func(a Carder, b Carder) bool {
		return a.Power() > b.Power()
	}
	atkCmp := func(a Carder, b Carder) bool {
		return a.Power() > b.Power()
	}
	var isBetter func(Carder, Carder) bool
	resolvedOrder := b.ResolveOrder()
	if resolvedOrder == OrderAttack {
		// Higher is better.
		isBetter = atkCmp
	} else {
		// Lower is better.
		isBetter = defCmp
	}

	for _, pc := range b.PlayedCardsInOrder() {
		if bestCard == nil || isBetter(pc.Card, bestCard.Card) {
			bestCard = &pc
		}
	}
	if bestCard == nil {
		panic("Unable to find best card!")
	}

	b.BestCard = bestCard
}

func (b *Board) ResolveWinner() {
	// if self.player_will_win_next_round(
	//     self.best_card.player
	// ) and self.player_states[self.best_card.player].has_state(
	//     PlayerStates.UnableToWin
	// ):
	//     return

	b.RoundWinner = b.BestCard.Player
	b.RoundWinningCard = b.BestCard.Card
	b.Victories[b.RoundWinner.Num] += 1

	log.Println("Winning card!", b.RoundWinningCard.Name())
	if b.Victories[b.RoundWinner.Num] == int(b.WinsNeeded) {
		panic(fmt.Sprintf("Player %s wins the game!", b.RoundWinner.Name))
	}
}

func (b *Board) BeginRound() {
	b.PlayedCards = make([]PlayedCard, 0, len(b.Players))
	b.RoundWinner = nil
	b.RoundWinningCard = nil
}

func (b *Board) commitCard(p *Player, c Carder, o Order) {
	pc := PlayedCard{
		Player:   p,
		Card:     c,
		Order:    o,
		Revealed: false,
	}
	b.PlayedCards = append(b.PlayedCards, pc)
}

func (b *Board) CommitPhase() (err error) {
	for _, p := range b.Players {
		selection := make([]interface{}, 0, len(p.Hand))
		for _, c := range p.Hand {
			selection = append(selection, c)
		}
		chosenCardInt, err := p.Picks(selection, p.Name+": Choose a card to commit!", 1)
		if err != nil {
			return err
		}
		chosenCard, ok := chosenCardInt.(Carder)
		if !ok {
			return errors.New("Type assertion failed")
		}

		p.RemoveCardFromHand(chosenCard)

		selection = make([]interface{}, 0, 2)
		selection = append(selection, OrderAttack)
		selection = append(selection, OrderDefense)
		chosenOrderInt, err := p.Picks(selection, p.Name+": Choose card's order!", 1)
		if err != nil {
			return err
		}
		chosenOrder, ok := chosenOrderInt.(Order)
		if !ok {
			return errors.New("Type assertion failed")
		}
		fmt.Println("Chosen card: \n", chosenCard)
		fmt.Printf("Chosen card: %#v\n", chosenCard)
		fmt.Printf("Chosen order: %s\n", chosenOrder)
		b.commitCard(p, chosenCard, chosenOrder)
	}
	return nil
}
