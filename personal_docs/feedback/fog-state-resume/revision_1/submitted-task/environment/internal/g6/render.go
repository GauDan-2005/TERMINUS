package g6

import "fmt"

func Preview(grid []string) string {
	out := ""
	for _, row := range grid {
		out += row + "\n"
	}
	return fmt.Sprintf("%d rows", len(grid))
}
