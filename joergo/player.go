package joerg

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"math/rand"
)

type HandCardState int

const (
	VisibleOnlyForPlayer HandCardState = iota
	VisibleForEveryone
	HiddenFromEveryone
)

type Player struct {
	Num              int
	Name             string
	Hand             []Carder
	HandStates       map[Carder]HandCardState
	ReceiveChoice    chan []byte
	OutgoingMessages chan []byte
}

func NewPlayer(num int, name string, recvChoice chan []byte, outgoingMessages chan []byte) *Player {
	return &Player{
		Num:              num,
		Name:             name,
		Hand:             make([]Carder, 0),
		HandStates:       make(map[Carder]HandCardState),
		ReceiveChoice:    recvChoice,
		OutgoingMessages: outgoingMessages,
	}
}

func (p *Player) MarshalJSON() ([]byte, error) {
	var out struct {
		Name       string
		Hand       []Carder
		HandStates map[string]HandCardState
	}
	out.Name = p.Name
	out.Hand = p.Hand
	for k, v := range p.HandStates {
		out.HandStates[k.Name()] = v
	}
	return json.Marshal(out)
}

// TODO(_): Implement multiple choice.
func (p *Player) Picks(items []interface{}, context string, numItems uint) (v interface{}, err error) {
	if p.Num != 0 {
		return p.RandomChoice(items, context, numItems)
	}
	var out struct {
		Items    []interface{} `json:"items"`
		Context  string        `json:"context"`
		NumItems uint          `json:"num_items"`
	}
	out.Items = items
	out.Context = context
	out.NumItems = numItems
	fmt.Println(json.Marshal(items))
	payload, err := json.Marshal(out)
	if err != nil {
		return nil, err
	}
	fmt.Println("Sending choice!")
	p.OutgoingMessages <- payload
	fmt.Println("In between!")
	respPayload := <-p.ReceiveChoice
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
