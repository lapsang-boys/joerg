package joerg

type RequestType string

const (
	RequestTypeNewGame    RequestType = "newGame"
	RequestTypeNextAction RequestType = "nextAction"
	RequestTypeChoice     RequestType = "choice"
)

type ResponseType string
type RpcType string

const (
	ResponseTypeBoard RpcType = "board"
	RpcTypeChoice     RpcType = "choice"
)

type NewGameRequest struct {
	Type             string `json:"type"`
	NumPlayers       uint   `json:"numPlayers"`
	StartingHandSize uint   `json:"startingHandSize"`
	WinsNeeded       uint   `json:"winsNeeded"`
}

type BoardResponse struct {
	Type    RpcType `json:"type"`
	Board   *Board  `json:"board"`
	BoardId int     `json:"boardId"`
}

type NextActionRequest struct {
	Type    string `json:"type"`
	BoardId int    `json:"boardId"`
}

type ChoiceResponse struct {
	Type     string `json:"type"`
	Choice   int    `json:"choice"`
	BoardId  int    `json:"boardId"`
	PlayerId int    `json:"playerId"`
}

type ServerRequestChoice struct {
	Type     RpcType       `json:"type"`
	Items    []interface{} `json:"items"`
	Context  string        `json:"context"`
	NumItems uint          `json:"numItems"`
}

type ErrorResponse struct {
	Type  string `json:"type"`
	Error string `json:"error"`
}
