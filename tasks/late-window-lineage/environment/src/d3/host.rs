use std::collections::BTreeSet;
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
    for line in BufReader::new(file).lines() {
        let line = line?;
        let parts: Vec<&str> = line.split('|').collect();
        if parts.len() != 7 {
            continue;
        }
        rows.push(R1 {
            origin: parts[0].to_string(),
            part: parts[1].to_string(),
            bucket: parts[2].parse().unwrap_or(0),
            name: parts[3].to_string(),
            value: parts[5].parse().unwrap_or(0),
            stamp: parts[4].parse().unwrap_or(0),
            line: vec![parts[6].to_string()],
        });
    }
    Ok(S3 { rows, seen: BTreeSet::new() })
}

pub fn save_d(path: &Path, rows: &[R1]) -> io::Result<()> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let mut file = File::create(path)?;
    for row in rows {
        let first = row.line.first().cloned().unwrap_or_default();
        writeln!(file, "{}|{}|{}|{}|{}|{}|{}", row.origin, row.part, row.bucket, row.name, row.stamp, row.value, first)?;
    }
    Ok(())
}

pub fn open_state(path: &Path) -> io::Result<S3> {
    load_d(path)
}
