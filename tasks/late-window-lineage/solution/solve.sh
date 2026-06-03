#!/bin/bash
set -euo pipefail

python3 <<'PY'
from pathlib import Path

Path('/app/src/a0/core.rs').write_text(r'''use crate::f5::types::{R0, R1, S0};

pub fn fold_a(a: &[R0], b: &S0) -> Vec<R1> {
    let mut seen = b.seen.clone();
    let mut rows = a.to_vec();
    rows.sort_by(|left, right| left.seq.cmp(&right.seq).then(left.token.cmp(&right.token)));
    let mut out = Vec::new();
    for item in rows {
        if !seen.insert(item.token.clone()) {
            continue;
        }
        out.push(R1 {
            origin: b.origin.clone(),
            part: item.part,
            bucket: item.bucket,
            name: item.name,
            value: item.delta,
            stamp: item.seq,
            line: vec![item.token],
        });
    }
    out
}
''', encoding='utf-8')

Path('/app/src/b1/book.rs').write_text(r'''use std::collections::BTreeMap;

use crate::c2::gate::collect_c;
use crate::f5::types::{R1, R2, S1};

pub fn merge_b(a: &mut S1, b: &[R1]) -> Vec<R1> {
    let mut by_token: BTreeMap<String, R1> = BTreeMap::new();
    for row in a.prior.iter().chain(b.iter()) {
        if let Some(first) = row.line.first() {
            by_token.entry(first.clone()).or_insert_with(|| row.clone());
        }
    }
    let mut rows: Vec<R1> = by_token.into_values().collect();
    rows.sort_by(|left, right| {
        left.part
            .cmp(&right.part)
            .then(left.bucket.cmp(&right.bucket))
            .then(left.name.cmp(&right.name))
            .then(left.stamp.cmp(&right.stamp))
            .then(left.line.cmp(&right.line))
    });

    let mut out = Vec::new();
    let mut current: Option<(String, i64, String)> = None;
    let mut total = 0i64;
    let mut trail: Vec<String> = Vec::new();
    for row in rows {
        let group = (row.part.clone(), row.bucket, row.name.clone());
        if current.as_ref() != Some(&group) {
            current = Some(group);
            total = 0;
            trail.clear();
        }
        total += row.value;
        for item in &row.line {
            if !trail.contains(item) {
                trail.push(item.clone());
            }
        }
        out.push(R1 {
            origin: row.origin.clone(),
            part: row.part.clone(),
            bucket: row.bucket,
            name: row.name.clone(),
            value: total,
            stamp: row.stamp,
            line: trail.clone(),
        });
    }
    out
}

pub fn finish_b(a: &mut S1, b: &[R1]) -> Vec<R2> {
    let rows = merge_b(a, b);
    collect_c(&rows)
}
''', encoding='utf-8')

Path('/app/src/c2/gate.rs').write_text(r'''use std::collections::BTreeSet;

use crate::f5::types::{R1, R2, S2};

pub fn mark_c(a: &mut S2, b: &R1) -> Option<R2> {
    let mut parts = vec![
        b.origin.clone(),
        b.part.clone(),
        b.bucket.to_string(),
        b.name.clone(),
        b.value.to_string(),
    ];
    parts.extend(b.line.iter().cloned());
    let id = parts.join(":");
    if !a.seen.insert(id.clone()) {
        return None;
    }
    Some(R2 {
        origin: b.origin.clone(),
        part: b.part.clone(),
        bucket: b.bucket,
        name: b.name.clone(),
        value: b.value,
        id,
        line: b.line.clone(),
    })
}

pub fn collect_c(rows: &[R1]) -> Vec<R2> {
    let mut state = S2 { seen: BTreeSet::new() };
    let mut out: Vec<R2> = rows.iter().filter_map(|row| mark_c(&mut state, row)).collect();
    out.sort_by(|left, right| {
        left.part
            .cmp(&right.part)
            .then(left.bucket.cmp(&right.bucket))
            .then(left.name.cmp(&right.name))
            .then(left.line.cmp(&right.line))
            .then(left.id.cmp(&right.id))
    });
    out
}
''', encoding='utf-8')

Path('/app/src/d3/host.rs').write_text(r'''use std::collections::BTreeSet;
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

use crate::f5::types::{R1, S3};

pub fn load_d(a: &Path) -> io::Result<S3> {
    if !a.exists() {
        return Ok(S3 { rows: Vec::new(), seen: BTreeSet::new() });
    }
    let file = File::open(a)?;
    let mut rows = Vec::new();
    let mut seen = BTreeSet::new();
    for line in BufReader::new(file).lines() {
        let line = line?;
        let parts: Vec<&str> = line.split('\t').collect();
        if parts.len() != 7 {
            continue;
        }
        let token = parts[6].to_string();
        if token.is_empty() || !seen.insert(token.clone()) {
            continue;
        }
        rows.push(R1 {
            origin: parts[0].to_string(),
            part: parts[1].to_string(),
            bucket: parts[2].parse().unwrap_or(0),
            name: parts[3].to_string(),
            value: parts[5].parse().unwrap_or(0),
            stamp: parts[4].parse().unwrap_or(0),
            line: vec![token],
        });
    }
    rows.sort_by(|left, right| {
        left.part
            .cmp(&right.part)
            .then(left.bucket.cmp(&right.bucket))
            .then(left.name.cmp(&right.name))
            .then(left.stamp.cmp(&right.stamp))
            .then(left.line.cmp(&right.line))
    });
    Ok(S3 { rows, seen })
}

pub fn save_d(path: &Path, rows: &[R1]) -> io::Result<()> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let mut unique: BTreeSet<String> = BTreeSet::new();
    let mut file = File::create(path)?;
    let mut rows = rows.to_vec();
    rows.sort_by(|left, right| {
        left.part
            .cmp(&right.part)
            .then(left.bucket.cmp(&right.bucket))
            .then(left.name.cmp(&right.name))
            .then(left.stamp.cmp(&right.stamp))
            .then(left.line.cmp(&right.line))
    });
    for row in rows {
        let first = row.line.first().cloned().unwrap_or_default();
        if first.is_empty() || !unique.insert(first.clone()) {
            continue;
        }
        writeln!(file, "{}\t{}\t{}\t{}\t{}\t{}\t{}", row.origin, row.part, row.bucket, row.name, row.stamp, row.value, first)?;
    }
    Ok(())
}

pub fn open_state(path: &Path) -> io::Result<S3> {
    load_d(path)
}
''', encoding='utf-8')

Path('/app/src/e4/flow.rs').write_text(r'''use std::collections::BTreeSet;
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

use crate::f5::types::R2;

fn sort_rows(rows: &mut [R2]) {
    rows.sort_by(|left, right| {
        left.part
            .cmp(&right.part)
            .then(left.bucket.cmp(&right.bucket))
            .then(left.name.cmp(&right.name))
            .then(left.line.cmp(&right.line))
            .then(left.id.cmp(&right.id))
    });
}

pub fn push_e(a: &Path, b: &[R2]) -> io::Result<()> {
    if let Some(parent) = a.parent() {
        fs::create_dir_all(parent)?;
    }
    let mut rows = b.to_vec();
    sort_rows(&mut rows);
    let mut written = BTreeSet::new();
    let mut file = File::create(a)?;
    for row in rows {
        if !written.insert(row.id.clone()) {
            continue;
        }
        writeln!(file, "{}\t{}\t{}\t{}\t{}\t{}\t{}", row.origin, row.part, row.bucket, row.name, row.value, row.id, row.line.join(","))?;
    }
    Ok(())
}

pub fn read_e(path: &Path) -> io::Result<Vec<R2>> {
    if !path.exists() {
        return Ok(Vec::new());
    }
    let mut rows = Vec::new();
    let file = File::open(path)?;
    let mut seen = BTreeSet::new();
    for line in BufReader::new(file).lines() {
        let line = line?;
        let parts: Vec<&str> = line.split('\t').collect();
        if parts.len() != 7 {
            continue;
        }
        if !seen.insert(parts[5].to_string()) {
            continue;
        }
        rows.push(R2 {
            origin: parts[0].to_string(),
            part: parts[1].to_string(),
            bucket: parts[2].parse().unwrap_or(0),
            name: parts[3].to_string(),
            value: parts[4].parse().unwrap_or(0),
            id: parts[5].to_string(),
            line: if parts[6].is_empty() { Vec::new() } else { parts[6].split(',').map(str::to_string).collect() },
        });
    }
    sort_rows(&mut rows);
    Ok(rows)
}
''', encoding='utf-8')
PY
