package order

type Order int

const (
	Attack Order = iota
	Defense
)

func (o Order) String() string {
	switch o {
	case Attack:
		return "Attack"
	case Defense:
		return "Defense"
	}
	panic("Unreachable")
}
