use std::fs::{self, File};
use std::io::{self, Write};
use std::path::Path;

use crate::serde_f::row_json;
use crate::types_f::Record;

pub struct S3 {
    pub count: usize,
}

pub fn walk_e(a: &[Record], b: &mut S3) {
    b.count += a.len();
}

pub fn emit_e(a: &Path, b: &[Record]) -> io::Result<()> {
    if let Some(parent) = a.parent() {
        fs::create_dir_all(parent)?;
    }
    let mut file = File::create(a)?;
    for row in b {
        writeln!(file, "{}", row_json(row))?;
    }
    Ok(())
}

pub fn note_e(a: &Path, b: &[Record]) -> io::Result<()> {
    if let Some(parent) = a.parent() {
        fs::create_dir_all(parent)?;
    }
    let mut file = File::create(a)?;
    for row in b.iter().rev() {
        writeln!(file, "{} {} {} {} {} {}", row.case_name, row.task_name, row.parent_name, row.depth, row.lane_name, row.turn)?;
    }
    Ok(())
}
