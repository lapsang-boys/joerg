package joerg

// PlayedCard records information about a card played by a given player.
type PlayedCard struct {
	// Player who played the card.
	Player *Player `json:"player"`
	// Card played.
	Card Carder `json:"card"`
	// Order in which the card is played (attack or defence).
	Order Order `json:"order"`
	// Specifies whether the card is revealed.
	Revealed bool `json:"revealed"`
}
