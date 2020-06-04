package joerg

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"math/rand"
)

//go:generate stringer -type HandCardState -linecomment

type HandCardState int

func (h HandCardState) MarshalText() (text []byte, err error) {
	return []byte(h.String()), nil
}

const (
	VisibleOnlyForPlayer HandCardState = iota + 1 // VisibleOnlyForPlayer
	VisibleForEveryone                            // VisibleForEveryone
	HiddenFromEveryone                            // HiddenFromEveryone
)

type Player struct {
	Num  int      `json:"num"`
	Name string   `json:"name"`
	Hand []Carder `json:"hand"`
	// Map from card name to hand card state.
	HandStates    map[string]HandCardState `json:"handStates"`
	receiveChoice chan []byte

	sendObject func(v interface{})
}

func NewPlayer(num int, name string, recvChoice chan []byte, sendObject func(v interface{})) *Player {
	return &Player{
		Num:           num,
		Name:          name,
		Hand:          make([]Carder, 0),
		HandStates:    make(map[string]HandCardState),
		receiveChoice: recvChoice,
		sendObject:    sendObject,
	}
}

func (p *Player) PickCard(cards []Carder, context string) (card Carder, err error) {
	var items []interface{}
	for _, card := range cards {
		items = append(items, card)
	}
	if p.Num != 0 {
		choice, err := p.RandomChoice(items, context, 1)
		return choice.(Carder), err
	}
	out := ServerRequestChoice{
		Type:     RpcTypeChoice,
		Items:    items,
		Context:  context,
		NumItems: 1,
	}
	fmt.Println("Sending choice!")
	p.sendObject(out)
	fmt.Println("In between!")
	respPayload := <-p.receiveChoice
	fmt.Println("Received choice")
	var choice ChoiceResponse
	err = json.Unmarshal(respPayload, &choice)
	if err != nil {
		return nil, err
	}
	return cards[choice.Choice], nil
}

func (p *Player) PickOrder(context string) (order Order, err error) {
	items := []interface{}{
		OrderAttack,
		OrderDefense,
	}
	if p.Num != 0 {
		choice, err := p.RandomChoice(items, context, 1)
		return choice.(Order), err
	}
	out := ServerRequestChoice{
		Type:     RpcTypeChoice,
		Items:    items,
		Context:  context,
		NumItems: 1,
	}
	fmt.Println("Sending choice!")
	p.sendObject(out)
	fmt.Println("In between!")
	respPayload := <-p.receiveChoice
	fmt.Println("Received choice")
	var choice ChoiceResponse
	err = json.Unmarshal(respPayload, &choice)
	if err != nil {
		return 0, err
	}
	return items[choice.Choice].(Order), nil
}

func (p *Player) RandomChoice(items []interface{}, context string, numItems uint) (v interface{}, err error) {
	fmt.Println(p.Name + ": Making random choice")
	fmt.Println(context)
	if len(items) == 0 {
		return nil, errors.New("choice: items list is empty")
	}
	randIdx := rand.Intn(len(items))
	return items[randIdx], nil
}

func (p *Player) AddCardToHand(c Carder) {
	p.Hand = append(p.Hand, c)
}

func (p *Player) RemoveCardFromHand(c Carder) {
	for i, hc := range p.Hand {
		if hc.Name() == c.Name() {
			// Remove element.
			p.Hand = append(p.Hand[:i], p.Hand[i+1:]...)
			return
		}
	}
	log.Println("Card to be removed not in player hand!")
}
