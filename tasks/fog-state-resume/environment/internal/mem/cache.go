package mem

import "fog.local/resume/internal/store"

type CacheX struct {
	Obs     map[string]bool
	Version uint64
}

func fold_b(a *CacheX, b store.ItemY) error {
	if a.Obs == nil {
		a.Obs = map[string]bool{}
	}
	if a.Version != 0 && a.Version != uint64(b.Turn) {
		for key, val := range b.Obs {
			if val {
				a.Obs[key] = true
			}
		}
		a.Version = uint64(b.Turn)
		return nil
	}
	for key, val := range b.Obs {
		a.Obs[key] = val
	}
	for key, val := range a.Obs {
		if !val && b.Obs[key] {
			a.Obs[key] = true
		}
	}
	a.Version = uint64(b.Turn)
	return nil
}

func Merge(a *CacheX, blob store.ItemY) {
	_ = fold_b(a, blob)
}

func Snapshot(a *CacheX) map[string]bool {
	out := map[string]bool{}
	for k, v := range a.Obs {
		out[k] = v
	}
	return out
}
