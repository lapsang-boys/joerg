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

const (
	VisibleOnlyForPlayer HandCardState = iota // VisibleOnlyForPlayer
	VisibleForEveryone                        // VisibleForEveryone
	HiddenFromEveryone                        // HiddenFromEveryone
)

func (h HandCardState) MarshalText() (text []byte, err error) {
	return []byte(h.String()), nil
}

type Player struct {
	Num  int      `json:"num"`
	Name string   `json:"name"`
	Hand []Carder `json:"hand"`
	// Map from card name to hand card state.
	HandStates    map[string]HandCardState `json:"handStates"`
	receiveChoice chan []byte

	sendObject func(typ string, v interface{})
}

func NewPlayer(num int, name string, recvChoice chan []byte, sendObject func(typ string, v interface{})) *Player {
	return &Player{
		Num:           num,
		Name:          name,
		Hand:          make([]Carder, 0),
		HandStates:    make(map[string]HandCardState),
		receiveChoice: recvChoice,
		sendObject:    sendObject,
	}
}

// TODO(_): Implement multiple choice.
func (p *Player) Picks(items []interface{}, context string, numItems uint) (v interface{}, err error) {
	if p.Num != 0 {
		return p.RandomChoice(items, context, numItems)
	}
	var out struct {
		Items    []interface{} `json:"items"`
		Context  string        `json:"context"`
		NumItems uint          `json:"numItems"`
	}
	out.Items = items
	out.Context = context
	out.NumItems = numItems
	fmt.Println("Sending choice!")
	p.sendObject("choice", out)
	fmt.Println("In between!")
	respPayload := <-p.receiveChoice
	fmt.Println("Received choice")
	var choice ChoiceAction
	err = json.Unmarshal(respPayload, &choice)
	if err != nil {
		return nil, err
	}
	return items[choice.Choice], nil
}

func (p *Player) RandomChoice(items []interface{}, context string, numItems uint) (v interface{}, err error) {
	fmt.Println(p.Name + ": Making random choice")
	fmt.Println(context)
	if len(items) == 0 {
		return nil, errors.New("choice: items list is empty.")
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
