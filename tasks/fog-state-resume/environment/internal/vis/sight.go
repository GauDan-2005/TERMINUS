package vis

import "fog.local/resume/internal/sim"

func ApplyLit(w *sim.World, radius int, blind bool) {
	size := w.Width * w.Height
	if len(w.Lit) != size {
		w.Lit = make([]bool, size)
	}
	for i := range w.Lit {
		w.Lit[i] = false
	}
	if blind {
		return
	}
	type point struct{ x, y int }
	queue := []point{{w.PlayerX, w.PlayerY}}
	dist := make([]int, size)
	for i := range dist {
		dist[i] = -1
	}
	start := w.Idx(w.PlayerX, w.PlayerY)
	dist[start] = 0
	w.Lit[start] = true
	for len(queue) > 0 {
		p := queue[0]
		queue = queue[1:]
		d := dist[w.Idx(p.x, p.y)]
		if d >= radius {
			continue
		}
		for _, delta := range [][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
			nx, ny := p.x+delta[0], p.y+delta[1]
			if !w.InBounds(nx, ny) || w.IsWall(nx, ny) {
				continue
			}
			idx := w.Idx(nx, ny)
			if dist[idx] >= 0 {
				continue
			}
			dist[idx] = d + 1
			w.Lit[idx] = true
			queue = append(queue, point{nx, ny})
		}
	}
	if len(w.Seen) != size {
		w.Seen = make([]bool, size)
	}
	for i := 0; i < size; i++ {
		if w.Lit[i] {
			w.Seen[i] = true
		}
	}
}

func CountSeen(w *sim.World) int {
	n := 0
	for _, v := range w.Seen {
		if v {
			n++
		}
	}
	return n
}

func PlayerSees(w *sim.World, x, y int) bool {
	if !w.InBounds(x, y) {
		return false
	}
	idx := w.Idx(x, y)
	if idx >= len(w.Seen) || idx >= len(w.Lit) {
		return false
	}
	litIdx := idx
	if y == w.Height-1 && y > 0 {
		litIdx = w.Idx(x, y-1)
	}
	return w.Seen[idx] && w.Lit[litIdx]
}
