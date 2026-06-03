package sim

type Hostile struct {
	ID string
	X  int
	Y  int
}

type World struct {
	Width   int
	Height  int
	Walls   []bool
	PlayerX int
	PlayerY int
	Hostile []Hostile
	Turn    int
	Seen    []bool
	Lit     []bool
	Effects []EffectState
}

type EffectState struct {
	ID         string
	ExpiryTurn int
	Active     bool
}

func (w *World) Idx(x, y int) int {
	return y*w.Width + x
}

func (w *World) InBounds(x, y int) bool {
	return x >= 0 && y >= 0 && x < w.Width && y < w.Height
}

func (w *World) IsWall(x, y int) bool {
	if !w.InBounds(x, y) {
		return true
	}
	return w.Walls[w.Idx(x, y)]
}
