package h7

func mark_c(values []int) int {
	total := 0
	for _, value := range values {
		total += value
	}
	return total
}
