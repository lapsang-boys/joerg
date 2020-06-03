package joerg

type Carder interface {
	Power() int
	Name() string
	OnReveal(b *Board, p *Player, order Order)
	OnLose(b *Board, p *Player, order Order)
	OnWin(b *Board, p *Player, order Order)
	OnCycle(b *Board, p *Player, order Order)
	OnHandEnter(b *Board, p *Player, order Order)
	OnBeforePower(b *Board, p *Player, order Order)
}

type Card struct {
	Nam string `json:"name"`
	Pow int    `json:"power"`
	Rul string `json:"ruling"`
	Leg bool   `json:"legendary"`
	Fla string `json:"flavor"`
	Img string `json:"imgSrc"`
}

func (c Card) Power() int {
	return c.Pow
}
func (c Card) Name() string {
	return c.Nam
}

func (c Card) OnReveal(b *Board, p *Player, order Order)      {}
func (c Card) OnWin(b *Board, p *Player, order Order)         {}
func (c Card) OnLose(b *Board, p *Player, order Order)        {}
func (c Card) OnCycle(b *Board, p *Player, order Order)       {}
func (c Card) OnHandEnter(b *Board, p *Player, order Order)   {}
func (c Card) OnBeforePower(b *Board, p *Player, order Order) {}
