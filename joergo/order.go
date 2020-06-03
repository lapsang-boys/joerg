package joerg

//go:generate stringer -type Order -linecomment

// Order specifies the order of a played card (attack or defense).
type Order int

func (order Order) MarshalText() (text []byte, err error) {
	return []byte(order.String()), nil
}

// Card orders.
const (
	OrderAttack  Order = iota + 1 // Attack
	OrderDefense                  // Defense
)
