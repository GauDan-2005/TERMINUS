#!/bin/bash
set -euo pipefail

python3 <<'PY'
from pathlib import Path

Path("/app/internal/b1/cache.go").write_text(
    """package b1

import "fog.local/resume/internal/a0"

type CacheX struct {
	Obs map[string]bool
	Version uint64
}

func fold_b(a *CacheX, b a0.ItemY) error {
	a.Obs = map[string]bool{}
	for key, val := range b.Obs {
		if val {
			a.Obs[key] = true
		}
	}
	a.Version = uint64(b.Turn)
	return nil
}

func Merge(a *CacheX, blob a0.ItemY) {
	_ = fold_b(a, blob)
}

func Snapshot(a *CacheX) map[string]bool {
	out := map[string]bool{}
	for k, v := range a.Obs {
		out[k] = v
	}
	return out
}
"""
)

Path("/app/internal/c2/effect.go").write_text(
    """package c2

type EffectSnap struct {
	ID         string
	ExpiryTurn int
	Active     bool
}

type ProfileSnap struct {
	Blind     bool
	Epoch     bool
	CheckTurn int
}

type RowSnap struct {
	ID     string
	Active bool
	Epoch  int
}

type mapX struct {
	Items map[string]entryX
}

type entryX struct {
	ID         string
	ExpiryTurn int
	Active     bool
}

func mark_c(a *mapX, b uint64, c []entryX) error {
	if a.Items == nil {
		a.Items = map[string]entryX{}
	}
	for _, item := range c {
		a.Items[item.ID] = item
	}
	return nil
}

func SyncBoundary(effects []EffectSnap, savedTurn int, currentTurn int) []EffectSnap {
	store := &mapX{}
	entries := []entryX{}
	for _, eff := range effects {
		rem := eff.ExpiryTurn - savedTurn
		if rem < 0 {
			rem = 0
		}
		entries = append(entries, entryX{
			ID: eff.ID, ExpiryTurn: currentTurn + rem, Active: true,
		})
	}
	_ = mark_c(store, 0, entries)
	out := make([]EffectSnap, 0, len(store.Items))
	for _, item := range store.Items {
		out = append(out, EffectSnap{
			ID: item.ID, ExpiryTurn: item.ExpiryTurn,
			Active: currentTurn < item.ExpiryTurn,
		})
	}
	return out
}

func Seed(profile ProfileSnap, turn int) []EffectSnap {
	out := []EffectSnap{}
	if profile.Blind {
		out = append(out, EffectSnap{ID: "blind", ExpiryTurn: turn + 4, Active: true})
	}
	if profile.Epoch {
		out = append(out, EffectSnap{ID: "ward", ExpiryTurn: profile.CheckTurn + 2, Active: true})
	}
	return out
}

func ItemsFor(effects []EffectSnap, turn int) []RowSnap {
	rows := []RowSnap{}
	for _, eff := range effects {
		rows = append(rows, RowSnap{
			ID: eff.ID, Active: turn < eff.ExpiryTurn, Epoch: eff.ExpiryTurn,
		})
	}
	return rows
}
"""
)

Path("/app/internal/d3/plan.go").write_text(
    """package d3

import (
	"fog.local/resume/internal/e4"
	"fog.local/resume/internal/sim"
)

type tokenX string

type nodeX struct {
	Cache map[string]bool
}

func bind_d(a *nodeX, b tokenX, c []int) (int, int, bool) {
	if len(c) < 4 {
		return 0, 0, false
	}
	px, py, hx, hy := c[0], c[1], c[2], c[3]
	bestX, bestY := hx, hy
	best := 1 << 30
	for _, delta := range [][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
		nx, ny := hx+delta[0], hy+delta[1]
		d := (nx-px)*(nx-px) + (ny-py)*(ny-py)
		if d < best {
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
	if !e4.PlayerSees(w, h.X, h.Y) {
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
	legal := e4.StepLegal(w, h.X, h.Y, tx, ty) && e4.PlayerSees(w, tx, ty)
	row := sim.MoveRow{
		Turn: w.Turn, Actor: h.ID,
		FromX: h.X, FromY: h.Y, ToX: tx, ToY: ty,
		Kind: "step", Legal: legal,
	}
	h.X, h.Y = tx, ty
	w.Hostile[idx] = h
	return row, true
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
    if (abs_i(x1 - x0) + abs_i(y1 - y0) != 1) {
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
PY

sed -i 's/out\.Seen = make(\[\]bool, len(b\.Seen))/out.Seen = append([]bool(nil), st.Seen...)/' /app/internal/a0/pack.go
sed -i '/for k, v := range stale/,+2d' /app/internal/f5/run.go

python3 <<'PY2'
from pathlib import Path
path = Path("/app/internal/f5/run.go")
text = path.read_text()
old = """\tmoves := []MoveRow{}
\tfor _, step := range steps {
\t\tif step.Action != "save" {
\t\t\tcontinue
\t\t}
\t\tw.Turn = step.Turn
\t\te4.ApplyLit(w, radius, blindActive(w))
\t\tmoves = append(moves, advanceAll(w, merged)...)
\t}
\treturn moves
}"""
new = """\tmoves := []MoveRow{}
\tpastSave := false
\tfor _, step := range steps {
\t\tif step.Action == "save" {
\t\t\tpastSave = true
\t\t\tcontinue
\t\t}
\t\tif !pastSave {
\t\t\tcontinue
\t\t}
\t\tw.Turn = step.Turn
\t\tif step.Actor == "P" {
\t\t\tapplyPlayer(w, step.Arg)
\t\t\te4.ApplyLit(w, radius, blindActive(w))
\t\t}
\t\tif step.Actor == "H" {
\t\t\tmoves = append(moves, advanceAll(w, merged)...)
\t\t}
\t}
\treturn moves
}"""
if old not in text:
    raise SystemExit("runLoaded block not found")
path.write_text(text.replace(old, new, 1))
PY2

make -s -C /app build
bash /app/scripts/run-matrix.sh
