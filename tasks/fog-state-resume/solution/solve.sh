#!/bin/bash
set -euo pipefail

sed -i 's/out\.Seen = append(\[\]bool(nil), st\.Lit\.\.\.)/out.Seen = append([]bool(nil), st.Seen...)/' /app/internal/store/pack.go

sed -i 's/ExpiryTurn: currentTurn + rem - 1/ExpiryTurn: currentTurn + rem/' /app/internal/mod/effect.go

sed -i 's/if d <= best/if d < best/' /app/internal/slot/plan.go

sed -i '/for k, v := range stale/,+2d' /app/internal/exec/run.go

python3 <<'PY'
from pathlib import Path

Path("/app/internal/mem/cache.go").write_text(
    """package mem

import "fog.local/resume/internal/store"

type CacheX struct {
\tObs     map[string]bool
\tVersion uint64
}

func fold_b(a *CacheX, b store.ItemY) error {
\ta.Obs = map[string]bool{}
\tfor key, val := range b.Obs {
\t\tif val {
\t\t\ta.Obs[key] = true
\t\t}
\t}
\ta.Version = uint64(b.Turn)
\treturn nil
}

func Merge(a *CacheX, blob store.ItemY) {
\t_ = fold_b(a, blob)
}

func Snapshot(a *CacheX) map[string]bool {
\tout := map[string]bool{}
\tfor k, v := range a.Obs {
\t\tout[k] = v
\t}
\treturn out
}
"""
)

Path("/app/internal/vis/sight.go").write_text(
    """package vis

import "fog.local/resume/internal/sim"

func ApplyLit(w *sim.World, radius int, blind bool) {
\tsize := w.Width * w.Height
\tif len(w.Lit) != size {
\t\tw.Lit = make([]bool, size)
\t}
\tfor i := range w.Lit {
\t\tw.Lit[i] = false
\t}
\tif blind {
\t\treturn
\t}
\ttype point struct{ x, y int }
\tqueue := []point{{w.PlayerX, w.PlayerY}}
\tdist := make([]int, size)
\tfor i := range dist {
\t\tdist[i] = -1
\t}
\tstart := w.Idx(w.PlayerX, w.PlayerY)
\tdist[start] = 0
\tw.Lit[start] = true
\tfor len(queue) > 0 {
\t\tp := queue[0]
\t\tqueue = queue[1:]
\t\td := dist[w.Idx(p.x, p.y)]
\t\tif d >= radius {
\t\t\tcontinue
\t\t}
\t\tfor _, delta := range [][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
\t\t\tnx, ny := p.x+delta[0], p.y+delta[1]
\t\t\tif !w.InBounds(nx, ny) || w.IsWall(nx, ny) {
\t\t\t\tcontinue
\t\t\t}
\t\t\tidx := w.Idx(nx, ny)
\t\t\tif dist[idx] >= 0 {
\t\t\t\tcontinue
\t\t\t}
\t\t\tdist[idx] = d + 1
\t\t\tw.Lit[idx] = true
\t\t\tqueue = append(queue, point{nx, ny})
\t\t}
\t}
\tif len(w.Seen) != size {
\t\tw.Seen = make([]bool, size)
\t}
\tfor i := 0; i < size; i++ {
\t\tif w.Lit[i] {
\t\t\tw.Seen[i] = true
\t\t}
\t}
}

func CountSeen(w *sim.World) int {
\tn := 0
\tfor _, v := range w.Seen {
\t\tif v {
\t\t\tn++
\t\t}
\t}
\treturn n
}

func PlayerSees(w *sim.World, x, y int) bool {
\tif !w.InBounds(x, y) {
\t\treturn false
\t}
\tidx := w.Idx(x, y)
\tif idx >= len(w.Seen) || idx >= len(w.Lit) {
\t\treturn false
\t}
\treturn w.Seen[idx] && w.Lit[idx]
}
"""
)

Path("/app/probe/legality.c").write_text(
    """#include "legality.h"

static int abs_i(int v) {
    return v < 0 ? -v : v;
}

int walk_e(struct qx *a, int x0, int y0, int x1, int y1) {
    if (!a || !a->grid) {
        return 0;
    }
    if (x0 == x1 && y0 == y1) {
        return 1;
    }
    int dx = x1 - x0;
    int dy = y1 - y0;
    int adx = abs_i(dx);
    int ady = abs_i(dy);
    if (adx + ady != 1) {
        return 0;
    }
    if (x1 < 0 || y1 < 0 || x1 >= a->width || y1 >= a->height) {
        return 0;
    }
    if (a->grid[y1 * a->width + x1]) {
        return 0;
    }
    return 1;
}
"""
)

run = Path("/app/internal/exec/run.go")
rtext = run.read_text()
old = """\t\tif step.Actor == \"H\" {
\t\t\tmoves = append(moves, advanceAll(w, merged)...)
\t\t}"""
new = """\t\tif step.Actor == \"H\" {
\t\t\tvis.ApplyLit(w, radius, blindNow(w))
\t\t\tmoves = append(moves, advanceAll(w, merged)...)
\t\t}"""
if old not in rtext:
    raise SystemExit("runLoaded hostile block missing")
run.write_text(rtext.replace(old, new, 1))
PY

make -s -C /app build
bash /app/scripts/run-matrix.sh
