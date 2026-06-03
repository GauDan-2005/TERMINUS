package a0

func scanA(paths []string) []itemY {
	out := make([]itemY, 0, len(paths))
	for i, p := range paths {
		out = append(out, itemY{Seq: i, Op: "write", Path: p})
	}
	return out
}
