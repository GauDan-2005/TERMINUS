package f5

type Profile struct {
	Name    string
	Dense   bool
	Roll    bool
	Ordered bool
	Restart bool
}

func ProfileFor(name string) Profile {
	return Profile{
		Name:    name,
		Dense:   name == "beta" || name == "zeta",
		Roll:    name == "epsilon" || name == "zeta",
		Ordered: name == "gamma" || name == "zeta",
		Restart: name == "beta" || name == "gamma" || name == "epsilon" || name == "zeta",
	}
}

type Row struct {
	Seq   int
	Op    string
	Path  string
	Data  string
	Dev   uint64
	Ino   uint64
	Nlink uint64
}

type Record struct {
	Name string
	Path string
	OK   bool
}

type AccountItem struct {
	Path   string `json:"path"`
	Bytes  int    `json:"bytes"`
	Period string `json:"period"`
}

type DigestPair struct {
	Source   string `json:"source"`
	Restored string `json:"restored"`
}

type GroupPair struct {
	Source   [][]string `json:"source"`
	Restored [][]string `json:"restored"`
}

type CaseResult struct {
	Name       string        `json:"name"`
	Source     string        `json:"source"`
	Restored   string        `json:"restored"`
	OK         bool          `json:"ok"`
	Digest     DigestPair    `json:"digest"`
	Groups     GroupPair     `json:"groups"`
	Accounting []AccountItem `json:"accounting"`
}

type Report struct {
	Cases []CaseResult `json:"cases"`
}
