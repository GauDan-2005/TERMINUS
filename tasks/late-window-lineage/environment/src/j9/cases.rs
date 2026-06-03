use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::{Path, PathBuf};

use crate::f5::types::R0;
use crate::i8::parse::parse_row;

const NAMES: &[&str] = &["aurora", "boreal", "cirrus", "drift", "ember", "flux"];

pub fn names() -> &'static [&'static str] {
    NAMES
}

pub fn case_path(root: &Path, name: &str) -> PathBuf {
    root.join("data").join("cases").join(format!("{name}.csv"))
}

pub fn load_case(root: &Path, name: &str) -> io::Result<Vec<R0>> {
    let file = File::open(case_path(root, name))?;
    let mut rows = Vec::new();
    for line in BufReader::new(file).lines() {
        if let Some(row) = parse_row(name, &line?)? {
            rows.push(row);
        }
    }
    Ok(rows)
}
