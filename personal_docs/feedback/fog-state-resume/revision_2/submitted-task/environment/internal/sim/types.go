package sim

type Profile struct {
	Name      string
	Radius    int
	Blind     bool
	Dense     bool
	Epoch     bool
	Mixed     bool
	CheckTurn int
}

type MoveRow struct {
	Turn  int    `json:"turn"`
	Actor string `json:"actor"`
	FromX int    `json:"from_x"`
	FromY int    `json:"from_y"`
	ToX   int    `json:"to_x"`
	ToY   int    `json:"to_y"`
	Kind  string `json:"kind"`
	Legal bool   `json:"legal"`
}

type PathSummary struct {
	Sig     string `json:"sig"`
	Illegal int    `json:"illegal"`
	Steps   int    `json:"steps"`
}

type VisPair struct {
	FreshSeen  int `json:"fresh_seen"`
	ResumeSeen int `json:"resume_seen"`
}

type EffectRow struct {
	ID     string `json:"id"`
	Active bool   `json:"active"`
	Epoch  int    `json:"epoch"`
}

type CaseResult struct {
	Name       string      `json:"name"`
	OK         bool        `json:"ok"`
	Fresh      PathSummary `json:"fresh"`
	Resume     PathSummary `json:"resume"`
	Moves      []MoveRow   `json:"moves"`
	Visibility VisPair     `json:"visibility"`
	Effects    []EffectRow `json:"effects"`
	Records    string      `json:"records"`
	Log        string      `json:"log"`
}

type Report struct {
	Cases []CaseResult `json:"cases"`
}
