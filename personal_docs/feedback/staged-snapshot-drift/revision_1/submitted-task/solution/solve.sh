#!/bin/bash
set -euo pipefail

python3 <<'PY'
from pathlib import Path

Path('/app/internal/a0/core.go').write_text(r'''package a0

import (
	"os"
	"path/filepath"
	"sort"
	"strings"
	"syscall"

	"staged.local/snapshot/internal/b1"
	"staged.local/snapshot/internal/d3"
	"staged.local/snapshot/internal/f5"
)

type stateX struct {
	Rows   []itemY
	ByPath map[string]int
}

type itemY = f5.Row

func phase_a(a *stateX, b itemY) error {
	if a.ByPath == nil {
		a.ByPath = map[string]int{}
	}
	if b.Path == "" {
		return nil
	}
	if b.Op == "remove" {
		delete(a.ByPath, b.Path)
		a.Rows = append(a.Rows, b)
		return nil
	}
	if idx, ok := a.ByPath[b.Path]; ok {
		a.Rows[idx] = b
		return nil
	}
	a.ByPath[b.Path] = len(a.Rows)
	a.Rows = append(a.Rows, b)
	return nil
}

func emit_a(path string, data string) error {
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		return err
	}
	return os.WriteFile(path, []byte(data), 0o644)
}

func CreateTree(root string, profile f5.Profile) error {
	dirs := []string{"a", "b", "c"}
	if profile.Dense {
		dirs = append(dirs, "deep/x")
	}
	if profile.Roll {
		dirs = append(dirs, "d")
	}
	for _, dir := range dirs {
		if err := os.MkdirAll(filepath.Join(root, dir), 0o755); err != nil {
			return err
		}
	}
	if err := emit_a(filepath.Join(root, "a", "one.txt"), profile.Name+":one\n"); err != nil {
		return err
	}
	if err := emit_a(filepath.Join(root, "b", "two.txt"), profile.Name+":two\n"); err != nil {
		return err
	}
	if err := emit_a(filepath.Join(root, "c", "three.txt"), profile.Name+":three\n"); err != nil {
		return err
	}
	if profile.Dense {
		shared := filepath.Join(root, "deep", "x", "shared.dat")
		if err := emit_a(shared, profile.Name+":shared-payload\n"); err != nil {
			return err
		}
		for _, rel := range []string{"a/shared-a.dat", "b/shared-b.dat", "c/shared-c.dat"} {
			alias := filepath.Join(root, filepath.FromSlash(rel))
			_ = os.Remove(alias)
			if err := os.Link(shared, alias); err != nil {
				return err
			}
		}
	}
	if profile.Ordered {
		flow := filepath.Join(root, "a", "flow.txt")
		if err := emit_a(flow, "second\n"); err != nil {
			return err
		}
	}
	if profile.Roll {
		if err := emit_a(filepath.Join(root, "d", "roll.txt"), profile.Name+":period-one\n"); err != nil {
			return err
		}
	}
	return nil
}

func statIdentity(path string) (uint64, uint64, uint64, error) {
	info, err := os.Stat(path)
	if err != nil {
		return 0, 0, 0, err
	}
	st := info.Sys().(*syscall.Stat_t)
	return uint64(st.Dev), uint64(st.Ino), uint64(st.Nlink), nil
}

func RowsFromTree(root string, profile f5.Profile) ([]f5.Row, error) {
	paths := []string{}
	if err := filepath.WalkDir(root, func(path string, entry os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if entry.Type().IsRegular() {
			paths = append(paths, path)
		}
		return nil
	}); err != nil {
		return nil, err
	}
	sort.Strings(paths)
	state := &stateX{ByPath: map[string]int{}}
	seq := 0
	for _, path := range paths {
		rel, err := filepath.Rel(root, path)
		if err != nil {
			return nil, err
		}
		rel = filepath.ToSlash(rel)
		if profile.Ordered && rel == "a/flow.txt" {
			continue
		}
		dev, ino, nlink, err := statIdentity(path)
		if err != nil {
			return nil, err
		}
		data, err := os.ReadFile(path)
		if err != nil {
			return nil, err
		}
		if err := phase_a(state, f5.Row{Seq: seq, Op: "write", Path: rel, Data: string(data), Dev: dev, Ino: ino, Nlink: nlink}); err != nil {
			return nil, err
		}
		seq++
	}
	if profile.Ordered {
		flow := filepath.Join(root, "a", "flow.txt")
		dev, ino, nlink, err := statIdentity(flow)
		if err != nil {
			return nil, err
		}
		for _, row := range []f5.Row{
			{Seq: seq, Op: "write", Path: "a/flow.txt", Data: "first\n", Dev: dev, Ino: ino, Nlink: nlink},
			{Seq: seq + 1, Op: "remove", Path: "a/flow.txt", Dev: dev, Ino: ino, Nlink: nlink},
			{Seq: seq + 2, Op: "write", Path: "a/flow.txt", Data: "second\n", Dev: dev, Ino: ino, Nlink: nlink},
		} {
			if err := phase_a(state, row); err != nil {
				return nil, err
			}
		}
	}
	return append([]f5.Row(nil), state.Rows...), nil
}

func Materialize(rows []f5.Row, dst string, profile f5.Profile) error {
	replayRows, err := b1.FoldRows(rows, profile)
	if err != nil {
		return err
	}
	groups := map[string]string{}
	for _, row := range replayRows {
		target := filepath.Join(dst, filepath.FromSlash(row.Path))
		if row.Op == "remove" {
			_ = os.Remove(target)
			for key, value := range groups {
				if value == target {
					delete(groups, key)
				}
			}
			continue
		}
		if err := os.MkdirAll(filepath.Dir(target), 0o755); err != nil {
			return err
		}
		key := d3.KeyFor(row, profile)
		if existing, ok := groups[key]; ok {
			_ = os.Remove(target)
			if err := os.Link(existing, target); err != nil {
				return err
			}
			continue
		}
		if strings.TrimSpace(row.Op) == "" || row.Op == "write" {
			if err := emit_a(target, row.Data); err != nil {
				return err
			}
			groups[key] = target
		}
	}
	return nil
}
''', encoding='utf-8')

Path('/app/internal/b1/replay.go').write_text(r'''package b1

import (
	"sort"

	"staged.local/snapshot/internal/f5"
)

type rowX = f5.Row

func fold_b(a []rowX, b uint64) ([]rowX, error) {
	out := make([]rowX, len(a))
	copy(out, a)
	sort.SliceStable(out, func(i, j int) bool {
		if out[i].Seq == out[j].Seq {
			return out[i].Path < out[j].Path
		}
		return out[i].Seq < out[j].Seq
	})
	if b > 0 {
		filtered := out[:0]
		for _, row := range out {
			if row.Path == "" {
				continue
			}
			filtered = append(filtered, row)
		}
		out = append([]rowX(nil), filtered...)
	}
	return out, nil
}

func FoldRows(rows []f5.Row, profile f5.Profile) ([]f5.Row, error) {
	var flags uint64
	if profile.Restart && profile.Ordered {
		flags |= 1
	}
	return fold_b(rows, flags)
}
''', encoding='utf-8')

Path('/app/internal/c2/roll.go').write_text(r'''package c2

import (
	"sort"
	"strings"

	"staged.local/snapshot/internal/e4"
	"staged.local/snapshot/internal/f5"
)

type mapX struct {
	Items map[string]entryX
}

type entryX struct {
	Path   string
	Bytes  int
	Period string
}

func mark_c(a *mapX, b uint64, c []entryX) error {
	if a.Items == nil {
		a.Items = map[string]entryX{}
	}
	for _, item := range c {
		if item.Path == "" {
			continue
		}
		if item.Period == "" {
			item.Period = "p0"
		}
		if prior, ok := a.Items[item.Path]; ok && prior.Bytes > item.Bytes {
			item.Bytes = prior.Bytes
		}
		if b > 0 && item.Bytes < 0 {
			item.Bytes = 0
		}
		a.Items[item.Path] = item
	}
	return nil
}

func ItemsC(root string, profile f5.Profile) ([]f5.AccountItem, error) {
	bytesByPath, err := e4.NativeBytes(root)
	if err != nil {
		return nil, err
	}
	entries := []entryX{}
	for path, size := range bytesByPath {
		period := "p0"
		if profile.Roll && strings.HasPrefix(path, "d/") {
			period = "p1"
		}
		entries = append(entries, entryX{Path: path, Bytes: size, Period: period})
	}
	sort.Slice(entries, func(i, j int) bool { return entries[i].Path < entries[j].Path })
	store := &mapX{}
	var flags uint64
	if profile.Restart && profile.Roll {
		flags |= 1
	}
	if err := mark_c(store, flags, entries); err != nil {
		return nil, err
	}
	items := make([]f5.AccountItem, 0, len(store.Items))
	for _, item := range store.Items {
		items = append(items, f5.AccountItem{Path: item.Path, Bytes: item.Bytes, Period: item.Period})
	}
	sort.Slice(items, func(i, j int) bool { return items[i].Path < items[j].Path })
	return items, nil
}
''', encoding='utf-8')

Path('/app/internal/d3/pair.go').write_text(r'''package d3

import (
	"fmt"

	"staged.local/snapshot/internal/f5"
)

type tokenX string

type nodeX struct {
	Seen map[tokenX]bool
}

func bind_d(a *nodeX, b tokenX) bool {
	if a.Seen == nil {
		a.Seen = map[tokenX]bool{}
	}
	if b == "" {
		return false
	}
	if a.Seen[b] {
		return true
	}
	a.Seen[b] = true
	return true
}

func KeyFor(row f5.Row, profile f5.Profile) string {
	key := tokenX(fmt.Sprintf("%d:%d", row.Dev, row.Ino))
	state := &nodeX{}
	if !bind_d(state, key) {
		return row.Path
	}
	return string(key)
}
''', encoding='utf-8')

Path('/app/probe/measure.c').write_text(r'''#define _DEFAULT_SOURCE

#include "fswalk.h"

#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

static int emit_file(const char *path, const char *rel) {
    struct stat st;
    unsigned long size;
    if (stat(path, &st) != 0) {
        return 2;
    }
    size = (unsigned long)st.st_size;
    printf("%s\t%lu\n", rel, size);
    return 0;
}

static int scan_dir(const char *root, const char *rel) {
    char full[4096];
    DIR *dir;
    struct dirent *entry;
    if (rel[0] == '\0') {
        snprintf(full, sizeof(full), "%s", root);
    } else {
        snprintf(full, sizeof(full), "%s/%s", root, rel);
    }
    dir = opendir(full);
    if (!dir) {
        return 3;
    }
    while ((entry = readdir(dir)) != NULL) {
        char child_rel[4096];
        char child_full[4096];
        struct stat st;
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        if (rel[0] == '\0') {
            snprintf(child_rel, sizeof(child_rel), "%s", entry->d_name);
        } else {
            snprintf(child_rel, sizeof(child_rel), "%s/%s", rel, entry->d_name);
        }
        snprintf(child_full, sizeof(child_full), "%s/%s", root, child_rel);
        if (stat(child_full, &st) != 0) {
            closedir(dir);
            return 4;
        }
        if (S_ISDIR(st.st_mode)) {
            int rc = scan_dir(root, child_rel);
            if (rc != 0) {
                closedir(dir);
                return rc;
            }
        } else if (S_ISREG(st.st_mode)) {
            int rc = emit_file(child_full, child_rel);
            if (rc != 0) {
                closedir(dir);
                return rc;
            }
        }
    }
    closedir(dir);
    return 0;
}

int walk_e(struct qx *a, const char *root, unsigned long c) {
    if (!a || !root) {
        return 2;
    }
    a->seen += c;
    return scan_dir(root, "");
}
''', encoding='utf-8')
PY
