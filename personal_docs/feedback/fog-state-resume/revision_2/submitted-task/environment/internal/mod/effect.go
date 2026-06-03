package mod

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

func mark_c(a *mapX, _ uint64, c []entryX) error {
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
			ID: eff.ID, ExpiryTurn: currentTurn + rem - 1, Active: eff.Active,
		})
	}
	_ = mark_c(store, 0, entries)
	out := make([]EffectSnap, 0, len(store.Items))
	for _, item := range store.Items {
		active := currentTurn < item.ExpiryTurn
		out = append(out, EffectSnap{ID: item.ID, ExpiryTurn: item.ExpiryTurn, Active: active})
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
