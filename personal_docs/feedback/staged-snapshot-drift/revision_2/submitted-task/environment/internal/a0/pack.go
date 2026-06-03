package a0

func packA(rows []itemY) map[string]string {
	out := map[string]string{}
	for _, row := range rows {
		out[row.Path] = row.Op
	}
	return out
}
