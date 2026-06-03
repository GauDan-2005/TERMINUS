use std::fs;
use std::io;
use std::path::Path;

use crate::types_f::{Entry, Plan};

pub fn read_plan(path: &Path) -> io::Result<Plan> {
    let text = fs::read_to_string(path)?;
    let mut cap = 1usize;
    let mut entries = Vec::new();
    let name = path
        .file_stem()
        .and_then(|s| s.to_str())
        .unwrap_or("case")
        .to_string();
    for raw in text.lines() {
        let line = raw.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let parts: Vec<&str> = line.split_whitespace().collect();
        match parts.as_slice() {
            ["CAP", value] => cap = value.parse().unwrap_or(1),
            ["ROOT", ident, lane, at] => {
                let seq = entries.len();
                entries.push(Entry::Root { ident: (*ident).to_string(), lane: (*lane).to_string(), at: at.parse().unwrap_or(0), seq });
            }
            ["CHILD", from, ident, lane, at] => {
                let seq = entries.len();
                entries.push(Entry::Child { from: (*from).to_string(), ident: (*ident).to_string(), lane: (*lane).to_string(), at: at.parse().unwrap_or(0), seq });
            }
            ["DROP", ident] => entries.push(Entry::Drop { ident: (*ident).to_string() }),
            _ => {}
        }
    }
    Ok(Plan { name, cap, entries })
}
