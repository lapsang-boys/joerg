package joerg

import (
	"github.com/lapsang-boys/joerg/card"
	"github.com/lapsang-boys/joerg/order"
	"github.com/lapsang-boys/joerg/player"
)

type PlayedCard struct {
	Player   *player.Player
	Card     card.Carder
	Order    order.Order
	Revealed bool
}
