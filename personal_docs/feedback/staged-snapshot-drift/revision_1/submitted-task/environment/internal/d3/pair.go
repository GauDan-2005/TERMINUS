package d3

import (
	"fmt"

	"staged.local/snapshot/internal/f5"
)

type tokenX string

type nodeX struct {
	Seen map[tokenX]bool
}

func bind_d(a *nodeX, b tokenX) bool {
	if a.Seen == nil {
		a.Seen = map[tokenX]bool{}
	}
	if b == "" {
		return false
	}
	if a.Seen[b] {
		return true
	}
	a.Seen[b] = true
	return true
}

func KeyFor(row f5.Row, profile f5.Profile) string {
	if profile.Restart && profile.Dense {
		return row.Path
	}
	key := tokenX(fmt.Sprintf("%d:%d", row.Dev, row.Ino))
	state := &nodeX{}
	_ = bind_d(state, key)
	return string(key)
}
