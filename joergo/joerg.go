package main

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"log"
	"math/rand"
	"net/http"

	"github.com/lapsang-boys/joerg/action"
	"github.com/lapsang-boys/joerg/board"

	"github.com/gorilla/websocket"
	"go.uber.org/zap"
)

var (
	upgrader  = websocket.Upgrader{} // use default options
	boards    = map[int]*board.Board{}
	logger, _ = zap.NewDevelopment()
	sugar     = logger.Sugar()
)

func newGame(message []byte, recvChoice, outgoingMessages chan []byte) {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("Recovered in f", r)
		}
	}()

	var ng action.NewGame
	err := json.Unmarshal(message, &ng)
	if err != nil {
		outgoingMessages <- []byte(err.Error())
		return
	}
	sugar.Info("NewGame", ng)
	b, err := board.New(ng.NumPlayers, ng.StartingHandSize, ng.WinsNeeded, recvChoice, outgoingMessages)
	if err != nil {
		sugar.Info("err", err)
		outgoingMessages <- []byte(err.Error())
		return
	}
	boardId := rand.Intn(100)
	sugar.Info("board_id", boardId)
	sugar.Info("board", b)
	boards[boardId] = b

	commitWrapped := func() {
		err = b.CommitPhase()
		if err != nil {
			outgoingMessages <- []byte(err.Error())
			return
		}
	}

	cycleWrapped := func() {
		err = b.CyclePhase()
		if err != nil {
			outgoingMessages <- []byte(err.Error())
			return
		}
	}

	b.RandomlyAssignPole()
	b.ShuffleDeck()
	b.DealCards()

	steps := []func(){
		b.BeginRound,
		commitWrapped,
		b.ResolveOnReveal,
		b.ResolveBeforePower,
		b.ResolvePower,
		b.ResolveWinner,
		b.ResolveWinLose,
		b.EndResolvePhase,
		cycleWrapped,
		b.ProgressPole,
		b.EndRound,
	}
	i := 0
outer:
	for true {
		for _, step := range steps {
			log.Println(i, step)
			step()
			sendBoard(b, outgoingMessages)
			i += 1
			if i >= 200 {
				break outer
			}
		}
	}
}

func sendBoard(b *board.Board, outgoingMessages chan []byte) {
	buf, err := json.Marshal(b)
	if err != nil {
		outgoingMessages <- []byte(err.Error())
		return
	}
	log.Println("Sending Board!")
	outgoingMessages <- buf
}

func nextAction(message []byte, outgoingMessages chan []byte) {
	var na action.NextAction
	err := json.Unmarshal(message, &na)
	if err != nil {
		outgoingMessages <- []byte(err.Error())
		return
	}
	sugar.Info("NextAction", na)
	b, ok := boards[na.BoardId]
	if !ok {
		outgoingMessages <- []byte("Invalid board_id")
		return
	}
	b.Next()

	buf, err := json.Marshal(b)
	if err != nil {
		outgoingMessages <- []byte("Invalid board_id")
		return
	}
	outgoingMessages <- buf
}

func choice(message []byte, recvChoice chan []byte, outgoingMessages chan []byte) {
	sugar.Debug("choice: sending choice message into recvChoice")
	recvChoice <- message
}

func handleMessage(message []byte, recvChoice chan []byte, outgoingMessages chan []byte) (err error) {
	var v interface{}
	err = json.Unmarshal(message, &v)
	if err != nil {
		return err
	}
	sugar.Info("raw payload", v)
	m, ok := v.(map[string]interface{})
	if !ok {
		return errors.New("json is not object ")
	}
	var typ interface{}
	if typ, ok = m["type"]; !ok {
		return errors.New("not typer json payload!")
	}
	t, ok := typ.(string)
	if !ok {
		return errors.New("type not string")
	}
	sugar.Info("Chosing message action")
	switch action.ActionType(t) {
	case action.NewGameType:
		go newGame(message, recvChoice, outgoingMessages)
	case action.NextActionType:
		go nextAction(message, outgoingMessages)
	case action.ChoiceType:
		go choice(message, recvChoice, outgoingMessages)
	default:
		return fmt.Errorf("Unknown type: %s", t)
	}
	return nil
}

type Connection struct {
	ws               *websocket.Conn
	outgoingMessages chan []byte
	incomingMessages chan []byte
	recvChoice       chan []byte
}

func NewConnection(ws *websocket.Conn) Connection {
	var outgoingMessages = make(chan []byte)
	var incomingMessages = make(chan []byte)
	var recvChoice = make(chan []byte)

	return Connection{
		ws:               ws,
		outgoingMessages: outgoingMessages,
		incomingMessages: incomingMessages,
		recvChoice:       recvChoice,
	}
}

func (c *Connection) Send() {
	defer c.ws.Close()
	for msg := range c.outgoingMessages {
		sugar.Info("Sender: got message sending!")
		err := c.ws.WriteMessage(websocket.TextMessage, msg)
		if err != nil {
			sugar.Info("Send:", zap.Error(err))
			break
		}
	}
}

func (c *Connection) Recv() {
	defer c.ws.Close()
	for {
		_, msg, err := c.ws.ReadMessage()
		if err != nil {
			sugar.Info("Recv", zap.Error(err))
			break
		}
		sugar.Info("Recv: got message from wire!")
		c.incomingMessages <- msg
	}
}

func (c *Connection) Handle() {
	for msg := range c.incomingMessages {
		sugar.Info("Handler: handling message")
		err := handleMessage(msg, c.recvChoice, c.outgoingMessages)
		if err != nil {
			sugar.Info("handle:", zap.Error(err))
			sugar.Info("Handler: Sending error!")
			c.outgoingMessages <- []byte(err.Error())
			continue
		}
	}
}

func server(w http.ResponseWriter, r *http.Request) {
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		sugar.Info("upgrade:", zap.Error(err))
		return
	}

	conn := NewConnection(ws)

	go conn.Send()
	go conn.Recv()
	go conn.Handle()
}

func main() {
	flag.Parse()
	http.HandleFunc("/", server)
	sugar.Fatal(http.ListenAndServe("localhost:8080", nil))
}
