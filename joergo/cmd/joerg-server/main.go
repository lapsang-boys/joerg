package main

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"log"
	"math/rand"
	"net/http"

	"github.com/lapsang-boys/joerg"

	"github.com/gorilla/websocket"
	"go.uber.org/zap"
	//"go.uber.org/zap/zapcore"
)

var (
	//logger, _ = zap.NewDevelopment(zap.IncreaseLevel(zapcore.WarnLevel))
	logger, _ = zap.NewDevelopment()
	sugar     = logger.Sugar()
)

func (srv *Server) newGame(message []byte, c Connection) {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("Recovered in f", r)
		}
	}()

	var ng joerg.ClientNewGameRequest
	err := json.Unmarshal(message, &ng)
	if err != nil {
		c.sendError(err)
		return
	}
	sugar.Info("NewGame", ng)

	var (
		names = []string{"Bob", "Emil", "Henry", "Robin"}
	)

	players := make([]*joerg.Player, int(ng.NumPlayers))
	for i := range players {
		players[i] = joerg.NewPlayer(
			i,
			names[i],
			c.recvChoice,
			c.sendObject,
		)
	}

	b, err := joerg.NewBoard(ng.StartingHandSize, ng.WinsNeeded, players)
	if err != nil {
		sugar.Info("err", err)
		c.sendError(err)
		return
	}
	boardId := rand.Intn(100)
	sugar.Info("board_id", boardId)
	sugar.Info("board", b)
	srv.boards[boardId] = b

	commitWrapped := func() {
		err = b.CommitPhase()
		if err != nil {
			c.sendError(err)
			return
		}
	}

	cycleWrapped := func() {
		err = b.CyclePhase()
		if err != nil {
			c.sendError(err)
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
	for {
		for _, step := range steps {
			log.Println(i)
			step()
			out := joerg.ServerBoardResponse{
				Type:    joerg.ResponseTypeBoard,
				Board:   b,
				BoardId: boardId,
			}
			c.sendObject(out)
			i += 1
			if i >= 200 {
				break outer
			}
		}
	}
}

func (c Connection) sendError(err error) {
	if err == nil {
		return
	}
	out := joerg.ErrorResponse{
		Type:  "error",
		Error: err.Error(),
	}
	buf, err := json.Marshal(out)
	if err != nil {
		sugar.Warn("unable to marshal error", zap.Error(err))
		return
	}
	sugar.Info("Sending Error!")
	c.outgoingMessages <- buf
}

func (c Connection) sendObject(v interface{}) {
	buf, err := json.MarshalIndent(v, "", "\t")
	if err != nil {
		sugar.Warn("send object", zap.Error(err))
		c.sendError(err)
		return
	}
	sugar.Info(string(buf))
	log.Println("Sending Object!")
	c.outgoingMessages <- buf
}

func (srv *Server) nextAction(message []byte, c Connection) {
	var na joerg.ClientNextActionRequest
	err := json.Unmarshal(message, &na)
	c.sendError(err)
	sugar.Info("NextAction", na)
	b, ok := srv.boards[na.BoardId]
	if !ok {
		c.sendError(errors.New("invalid board_id"))
		return
	}
	b.Next()

	c.sendObject(b)
}

func (srv *Server) choice(message []byte, c Connection) {
	sugar.Debug("choice: sending choice message into recvChoice")
	c.recvChoice <- message
}

func (srv *Server) handleMessage(message []byte, c Connection) (err error) {
	var m map[string]interface{}
	err = json.Unmarshal(message, &m)
	if err != nil {
		return err
	}
	sugar.Info("raw payload", m)
	typ, ok := m["type"]
	if !ok {
		return errors.New("not typer json payload(!)")
	}
	t, ok := typ.(string)
	if !ok {
		return errors.New("type not string")
	}
	sugar.Info("Choosing message request type")
	switch joerg.RequestType(t) {
	case joerg.RequestTypeNewGame:
		go srv.newGame(message, c)
	case joerg.RequestTypeNextAction:
		go srv.nextAction(message, c)
	case joerg.RequestTypeChoice:
		go srv.choice(message, c)
	default:
		return fmt.Errorf("unknown type: %s", t)
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

func (c Connection) Send() {
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

func (c Connection) Recv() {
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

func (srv *Server) Handle(c Connection) {
	for msg := range c.incomingMessages {
		sugar.Info("Handler: handling message")
		err := srv.handleMessage(msg, c)
		if err != nil {
			sugar.Info("handle:", zap.Error(err))
			sugar.Info("Handler: Sending error!")
			c.sendError(err)
			continue
		}
	}
}

type Server struct {
	upgrader websocket.Upgrader // use default options
	boards   map[int]*joerg.Board
}

func NewServer() *Server {
	return &Server{
		upgrader: websocket.Upgrader{}, // use default options
		boards:   make(map[int]*joerg.Board),
	}
}

func (srv *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	srv.upgrader.CheckOrigin = func(*http.Request) bool {
		return true
	}
	ws, err := srv.upgrader.Upgrade(w, r, nil)
	if err != nil {
		sugar.Info("upgrade:", zap.Error(err))
		return
	}

	conn := NewConnection(ws)

	go conn.Send()
	go conn.Recv()
	go srv.Handle(conn)
}

func main() {
	var addr string
	flag.StringVar(&addr, "addr", ":8080", "address to listen on")
	flag.Parse()
	srv := NewServer()
	sugar.Fatal(http.ListenAndServe(addr, srv))
}
