package sim

func ProfileFor(name string) Profile {
	switch name {
	case "rook":
		return Profile{Name: "rook", Radius: 3, CheckTurn: 2}
	case "bishop":
		return Profile{Name: "bishop", Radius: 3, Blind: true, CheckTurn: 2}
	case "knight":
		return Profile{Name: "knight", Radius: 2, Dense: true, CheckTurn: 2}
	case "lancer":
		return Profile{Name: "lancer", Radius: 3, Dense: true, CheckTurn: 2}
	case "sentinel":
		return Profile{Name: "sentinel", Radius: 3, Epoch: true, CheckTurn: 4}
	case "warden":
		return Profile{Name: "warden", Radius: 3, Blind: true, Dense: true, Epoch: true, Mixed: true, CheckTurn: 4}
	case "ranger":
		return Profile{Name: "ranger", Radius: 3, Epoch: true, CheckTurn: 4}
	default:
		return Profile{Name: name, Radius: 3, CheckTurn: 2}
	}
}

func AllCases() []string {
	return []string{"rook", "bishop", "knight", "lancer", "sentinel", "warden", "ranger"}
}
