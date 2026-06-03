package slot

import (
	"fog.local/resume/internal/sim"
	"fog.local/resume/internal/vis"
)

type tokenX string

type nodeX struct {
	Cache map[string]bool
}

func bind_d(a *nodeX, _ tokenX, c []int) (int, int, bool) {
	if len(c) < 4 {
		return 0, 0, false
	}
	px, py, hx, hy := c[0], c[1], c[2], c[3]
	bestX, bestY := hx, hy
	best := 1 << 30
	for _, delta := range [][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
		nx, ny := hx+delta[0], hy+delta[1]
		d := (nx-px)*(nx-px) + (ny-py)*(ny-py)
		if d <= best {
			best = d
			bestX, bestY = nx, ny
		}
	}
	return bestX, bestY, best < 1<<29
}

func PlanSlot(w *sim.World, cache map[string]bool, idx int) (sim.MoveRow, bool) {
	if idx >= len(w.Hostile) {
		return sim.MoveRow{}, false
	}
	h := w.Hostile[idx]
	if !vis.PlayerSees(w, h.X, h.Y) {
		return sim.MoveRow{}, false
	}
	node := &nodeX{Cache: cache}
	tx, ty, ok := bind_d(node, tokenX(h.ID), []int{w.PlayerX, w.PlayerY, h.X, h.Y})
	if !ok {
		return sim.MoveRow{}, false
	}
	if w.IsWall(tx, ty) {
		return sim.MoveRow{}, false
	}
	legal := vis.StepLegal(w, h.X, h.Y, tx, ty) && vis.PlayerSees(w, tx, ty)
	row := sim.MoveRow{
		Turn: w.Turn, Actor: h.ID,
		FromX: h.X, FromY: h.Y, ToX: tx, ToY: ty,
		Kind: "step", Legal: legal,
	}
	h.X, h.Y = tx, ty
	w.Hostile[idx] = h
	return row, true
}
