package e4

import (
	"crypto/sha256"
	"encoding/hex"
	"os"
	"path/filepath"
	"sort"
	"syscall"
)

func Digest(root string) (string, error) {
	hash := sha256.New()
	paths := []string{}
	if err := filepath.WalkDir(root, func(path string, entry os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		paths = append(paths, path)
		return nil
	}); err != nil {
		return "", err
	}
	sort.Strings(paths)
	for _, path := range paths {
		if path == root {
			continue
		}
		rel, err := filepath.Rel(root, path)
		if err != nil {
			return "", err
		}
		rel = filepath.ToSlash(rel)
		info, err := os.Stat(path)
		if err != nil {
			return "", err
		}
		if info.IsDir() {
			hash.Write([]byte("D " + rel + "\n"))
			continue
		}
		if info.Mode().IsRegular() {
			data, err := os.ReadFile(path)
			if err != nil {
				return "", err
			}
			hash.Write([]byte("F " + rel + "\x00"))
			hash.Write(data)
			hash.Write([]byte("\n"))
		}
	}
	return hex.EncodeToString(hash.Sum(nil)), nil
}

func Groups(root string) ([][]string, error) {
	byIdentity := map[[2]uint64][]string{}
	if err := filepath.WalkDir(root, func(path string, entry os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if !entry.Type().IsRegular() {
			return nil
		}
		info, err := os.Stat(path)
		if err != nil {
			return err
		}
		st := info.Sys().(*syscall.Stat_t)
		rel, err := filepath.Rel(root, path)
		if err != nil {
			return err
		}
		key := [2]uint64{uint64(st.Dev), uint64(st.Ino)}
		byIdentity[key] = append(byIdentity[key], filepath.ToSlash(rel))
		return nil
	}); err != nil {
		return nil, err
	}
	groups := [][]string{}
	for _, group := range byIdentity {
		if len(group) > 1 {
			sort.Strings(group)
			groups = append(groups, group)
		}
	}
	sort.Slice(groups, func(i, j int) bool { return groups[i][0] < groups[j][0] })
	return groups, nil
}
