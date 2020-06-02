package joerg

type PlayedCard struct {
	Player   *Player
	Card     Carder
	Order    Order
	Revealed bool
}
