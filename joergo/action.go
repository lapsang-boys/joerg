package joerg

type ActionType string

const (
	ActionNewGameType    ActionType = "newGame"
	ActionNextActionType            = "nextAction"
	ActionChoiceType                = "choice"
)

type NewGame struct {
	PayloadType      string `json:"type"`
	NumPlayers       uint   `json:"numPlayers"`
	StartingHandSize uint   `json:"startingHandSize"`
	WinsNeeded       uint   `json:"winsNeeded"`
}

type NextAction struct {
	PayloadType string `json:"type"`
	BoardId     int    `json:"boardId"`
}

type ChoiceAction struct {
	PayloadType string `json:"type"`
	Choice      int    `json:"choice"`
	BoardId     int    `json:"boardId"`
	PlayerId    int    `json:"playerId"`
}

type Typer interface {
	Type() string
}

func (ng *NewGame) Type() string {
	return ng.PayloadType
}

func (na *NextAction) Type() string {
	return na.PayloadType
}
