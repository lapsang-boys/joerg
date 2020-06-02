package joerg

type Order int

const (
	OrderAttack Order = iota
	OrderDefense
)

func (o Order) String() string {
	switch o {
	case OrderAttack:
		return "Attack"
	case OrderDefense:
		return "Defense"
	}
	panic("Unreachable")
}
