package b1

func checkpointB(rows []rowX) int {
	last := 0
	for _, row := range rows {
		if row.Seq > last {
			last = row.Seq
		}
	}
	return last
}
