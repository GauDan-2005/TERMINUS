package b1

import "fog.local/resume/internal/a0"

type CacheX struct {
	Obs map[string]bool
	Version uint64
}

func fold_b(a *CacheX, b a0.ItemY) error {
	if a.Obs == nil {
		a.Obs = map[string]bool{}
	}
	for key, val := range b.Obs {
		a.Obs[key] = val
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
