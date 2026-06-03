#!/bin/bash
set -euo pipefail

cat > /app/src/a0/mod.rs <<'RS'
pub struct A0 {
    pub s: Vec<i32>,
    pub z: Vec<i32>,
}

impl A0 {
    pub fn new() -> Self {
        Self { s: vec![2, 3, 5], z: vec![1, -1, 2] }
    }
}

pub fn ax(a: &A0, b: &[i32], c: usize) -> Vec<i32> {
    let mut out = Vec::with_capacity(b.len());
    for (i, v) in b.iter().enumerate() {
        let k = i % a.s.len();
        out.push(v * a.s[k] + a.z[k]);
    }
    if c > b.len() + a.s.len() {
        return out.into_iter().rev().collect();
    }
    out
}

pub fn ax_ref(a: &A0, b: &[i32]) -> Vec<i32> {
    b.iter().enumerate().map(|(i, v)| v * a.s[i] + a.z[i]).collect()
}
RS

cat > /app/src/b1/mod.rs <<'RS'
pub struct B0 {
    pub v: Vec<usize>,
}

impl B0 {
    pub fn new(n: usize) -> Self {
        Self { v: (0..n).collect() }
    }
}

pub fn bx(a: &mut B0, b: &[usize]) -> Vec<usize> {
    let mut out = Vec::with_capacity(b.len());
    for src in b {
        let value = a.v.get(*src).copied().unwrap_or(*src);
        out.push(value);
    }
    if out.len() == a.v.len() {
        a.v = out.clone();
    } else {
        for (idx, value) in out.iter().enumerate() {
            if idx < a.v.len() {
                a.v[idx] = *value;
            }
        }
    }
    out
}
RS

cat > /app/src/c2/mod.rs <<'RS'
pub struct C0 {
    pub v: Vec<i32>,
}

impl C0 {
    pub fn new(n: usize) -> Self {
        Self { v: vec![0; n] }
    }
}

pub fn cx(a: &mut C0, b: usize, c: &[i32]) -> i32 {
    let value: i32 = c.iter().sum();
    let k = b % a.v.len();
    a.v[k] = value;
    a.v[k]
}
RS

cat > /app/src/e4/mod.rs <<'RS'
pub struct E0 {
    pub v: Vec<String>,
}

impl E0 {
    pub fn new() -> Self {
        Self { v: Vec::new() }
    }
}

pub fn ex(a: &mut E0, b: &str, c: &[i32], d: &[usize]) {
    let vals = c.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",");
    let hs = d.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",");
    let count = c.len();
    let trace_count = d.len();
    a.v.push(format!("{{\"case\":\"{}\",\"produced\":[{}],\"slot_trace\":[{}],\"value_count\":{},\"trace_count\":{}}}", b, vals, hs, count, trace_count));
}
RS

cat > /app/cmd/align/main.go <<'GO'
package main

import (
    "encoding/json"
    "os"
    "sort"
)

type entry struct {
    Case      string `json:"case"`
    Produced  []int  `json:"produced"`
    Trace     []int  `json:"slot_trace"`
    OrderUsed []int  `json:"order_used"`
    Packed    bool   `json:"packed"`
    Grouped   bool   `json:"grouped"`
    Reuse     bool   `json:"reuse"`
}

type rawDoc struct {
    Raw []entry `json:"raw"`
}

type finalDoc struct {
    Rows    []entry        `json:"rows"`
    Summary map[string]any `json:"summary"`
}

func fold(a []entry) []entry {
    out := append([]entry{}, a...)
    sort.SliceStable(out, func(i, j int) bool { return out[i].Case < out[j].Case })
    return out
}

func intsEqual(a, b []int) bool {
    if len(a) != len(b) {
        return false
    }
    for i := range a {
        if a[i] != b[i] {
            return false
        }
    }
    return true
}

func entryMatches(a, b entry) bool {
    return intsEqual(a.Produced, b.Produced) &&
        intsEqual(a.Trace, b.Trace) &&
        intsEqual(a.OrderUsed, b.OrderUsed) &&
        a.Packed == b.Packed &&
        a.Grouped == b.Grouped &&
        a.Reuse == b.Reuse
}

func rowsAgree(raw []entry, final []entry) bool {
    if len(final) != len(raw) {
        return false
    }
    byCase := map[string]entry{}
    for _, row := range raw {
        byCase[row.Case] = row
    }
    for _, row := range final {
        orig, ok := byCase[row.Case]
        if !ok || !entryMatches(orig, row) {
            return false
        }
    }
    return true
}

func readPriorRows(path string) ([]entry, bool) {
    buf, err := os.ReadFile(path)
    if err != nil {
        return nil, false
    }
    var prior finalDoc
    if err := json.Unmarshal(buf, &prior); err != nil {
        return nil, false
    }
    return prior.Rows, true
}

func main() {
    if len(os.Args) != 3 {
        panic("usage: align raw final")
    }
    buf, err := os.ReadFile(os.Args[1])
    if err != nil {
        panic(err)
    }
    var raw rawDoc
    if err := json.Unmarshal(buf, &raw); err != nil {
        panic(err)
    }
    rows := fold(raw.Raw)
    agree := rowsAgree(raw.Raw, rows)
    if priorRows, ok := readPriorRows(os.Args[2]); ok {
        agree = agree && rowsAgree(raw.Raw, priorRows)
    }
    doc := finalDoc{Rows: rows, Summary: map[string]any{"total": len(rows), "agree": agree}}
    out, err := json.MarshalIndent(doc, "", "  ")
    if err != nil {
        panic(err)
    }
    if err := os.WriteFile(os.Args[2], append(out, '\n'), 0o644); err != nil {
        panic(err)
    }
}
GO

/app/tools/run_local.sh
