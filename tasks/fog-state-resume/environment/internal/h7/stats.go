package h7

type Counter struct {
	Runs int
}

type BoundaryStat struct {
	SavedTurn   int
	CurrentTurn int
	Shift       int
}

func Bump(c *Counter) {
	c.Runs++
}

func RebaseEpoch(saved, current int) int {
	return current - saved
}

func SyncPreview(saved, current int) BoundaryStat {
	return BoundaryStat{SavedTurn: saved, CurrentTurn: current, Shift: RebaseEpoch(saved, current)}
}
