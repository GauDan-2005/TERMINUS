package collate

import "strings"

func Mix(a string) string {
    return strings.TrimSpace(a)
}

func Keep(a []string) []string {
    out := append([]string{}, a...)
    return out
}
