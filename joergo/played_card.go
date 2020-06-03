package joerg

type PlayedCard struct {
	Player   *Player `json:"player"`
	Card     Carder  `json:"card"`
	Order    Order   `json:"order"`
	Revealed bool    `json:"revealed"`
}
