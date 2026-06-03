package d3

func newD() *nodeX {
	return &nodeX{Seen: map[tokenX]bool{}}
}
