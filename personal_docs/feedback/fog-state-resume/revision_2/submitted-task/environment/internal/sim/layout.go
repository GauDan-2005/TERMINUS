package sim

import (
	"bufio"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

func LoadLayout(root, name string) (*World, error) {
	path := filepath.Join(root, "data", "layouts", name+".map")
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	lines := strings.Split(strings.TrimSpace(string(data)), "\n")
	height := len(lines)
	width := 0
	for _, line := range lines {
		if len(line) > width {
			width = len(line)
		}
	}
	w := &World{Width: width, Height: height, Walls: make([]bool, width*height)}
	for y, line := range lines {
		for x := 0; x < width; x++ {
			ch := byte('.')
			if x < len(line) {
				ch = line[x]
			}
			idx := w.Idx(x, y)
			switch ch {
			case '#':
				w.Walls[idx] = true
			case '@':
				w.PlayerX, w.PlayerY = x, y
			default:
				if ch >= '1' && ch <= '9' {
					id := string(ch)
					w.Hostile = append(w.Hostile, Hostile{ID: id, X: x, Y: y})
				}
			}
		}
	}
	return w, nil
}

type ScriptStep struct {
	Turn   int
	Actor  string
	Action string
	Arg    string
}

func LoadScript(root, name string) ([]ScriptStep, error) {
	path := filepath.Join(root, "data", "scripts", name+".tsv")
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	steps := []ScriptStep{}
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		line := strings.TrimSpace(sc.Text())
		if line == "" || strings.HasPrefix(line, "turn") {
			continue
		}
		parts := strings.Split(line, "\t")
		if len(parts) < 4 {
			continue
		}
		turn, _ := strconv.Atoi(parts[0])
		steps = append(steps, ScriptStep{
			Turn:   turn,
			Actor:  parts[1],
			Action: parts[2],
			Arg:    parts[3],
		})
	}
	return steps, sc.Err()
}

func LoadRadius(root, name string) (int, error) {
	path := filepath.Join(root, "config", "sight.tsv")
	data, err := os.ReadFile(path)
	if err != nil {
		return 3, err
	}
	for _, line := range strings.Split(string(data), "\n") {
		line = strings.TrimSpace(line)
		if line == "" || strings.HasPrefix(line, "case") {
			continue
		}
		parts := strings.Split(line, "\t")
		if len(parts) >= 2 && parts[0] == name {
			return strconv.Atoi(parts[1])
		}
	}
	return 3, nil
}
