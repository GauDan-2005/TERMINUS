package e4

import (
	"bufio"
	"fmt"
	"os/exec"
	"strconv"
	"strings"
)

func NativeBytes(root string) (map[string]int, error) {
	cmd := exec.Command("/app/bin/fsmeasure", root)
	out, err := cmd.Output()
	if err != nil {
		return nil, err
	}
	rows := map[string]int{}
	scanner := bufio.NewScanner(strings.NewReader(string(out)))
	for scanner.Scan() {
		parts := strings.Split(scanner.Text(), "\t")
		if len(parts) != 2 {
			return nil, fmt.Errorf("bad native observation: %q", scanner.Text())
		}
		size, err := strconv.Atoi(parts[1])
		if err != nil {
			return nil, err
		}
		rows[parts[0]] = size
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}
	return rows, nil
}
