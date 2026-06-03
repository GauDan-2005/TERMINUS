use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

use crate::f5::types::R2;

pub fn push_e(a: &Path, b: &[R2]) -> io::Result<()> {
    if let Some(parent) = a.parent() {
        fs::create_dir_all(parent)?;
    }
    let mut file = File::create(a)?;
    for row in b {
        writeln!(file, "{}|{}|{}|{}|{}|{}|{}", row.origin, row.part, row.bucket, row.name, row.value, row.id, row.line.join(","))?;
    }
    Ok(())
}

pub fn read_e(path: &Path) -> io::Result<Vec<R2>> {
    if !path.exists() {
        return Ok(Vec::new());
    }
    let mut rows = Vec::new();
    let file = File::open(path)?;
    for line in BufReader::new(file).lines() {
        let line = line?;
        let parts: Vec<&str> = line.split('|').collect();
        if parts.len() != 7 {
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
    Ok(rows)
}
