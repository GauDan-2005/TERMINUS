use crate::model::{Entry, Event, State};
use std::fs;
use std::path::{Path, PathBuf};

pub fn read_trace(path: &Path) -> Result<Vec<Event>, String> {
    let text = fs::read_to_string(path).map_err(|e| format!("read {}: {e}", path.display()))?;
    let mut events = Vec::new();
    for raw in text.lines() {
        let line = raw.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() != 3 {
            return Err(format!("trace {} has malformed row: {line}", path.display()));
        }
        events.push(Event {
            kind: parts[0].to_string(),
            left: parts[1].to_string(),
            right: parts[2].to_string(),
        });
    }
    Ok(events)
}

pub fn app_path(value: &str) -> String {
    if value.starts_with("/app/") {
        value.to_string()
    } else if value == "/app" {
        value.to_string()
    } else {
        format!("/app/{}", value.trim_start_matches('/'))
    }
}

pub fn disk_path(value: &str) -> PathBuf {
    if let Some(rest) = value.strip_prefix("/app/") {
        PathBuf::from("/app").join(rest)
    } else if value == "/app" {
        PathBuf::from("/app")
    } else {
        PathBuf::from("/app").join(value)
    }
}

pub fn resolve_target_root(value: &str) -> Result<String, String> {
    let base = disk_path(value);
    let marker = base.join("link.target");
    if !marker.exists() {
        return Ok(app_path(value));
    }
    let raw = fs::read_to_string(&marker).map_err(|e| format!("read {}: {e}", marker.display()))?;
    let trimmed = raw.trim();
    let joined = base.join(trimmed);
    let absolute = joined
        .canonicalize()
        .map_err(|e| format!("resolve {}: {e}", joined.display()))?;
    let text = absolute.to_string_lossy().to_string();
    Ok(text)
}

pub fn collect_entries(state: &mut State, slot: &str, root: &str, epoch: u64) -> Result<Vec<Entry>, String> {
    let root_path = disk_path(root);
    let mut files = Vec::new();
    gather_ts(&root_path, &mut files)?;
    files.sort();
    let mut out = Vec::new();
    for file in files {
        let app_file = file_to_app(&file)?;
        let source = source_for(&file)?;
        let text = fs::read_to_string(&file).map_err(|e| format!("read {}: {e}", file.display()))?;
        for (line, symbol) in exported_symbols(&text) {
            let handle = state.handle_for(slot, &app_file, &symbol);
            out.push(Entry {
                slot: slot.to_string(),
                symbol,
                path: app_file.clone(),
                source: source.clone(),
                line,
                epoch,
                handle,
            });
        }
    }
    Ok(out)
}

fn gather_ts(dir: &Path, out: &mut Vec<PathBuf>) -> Result<(), String> {
    let entries = fs::read_dir(dir).map_err(|e| format!("scan {}: {e}", dir.display()))?;
    for item in entries {
        let path = item.map_err(|e| format!("scan {}: {e}", dir.display()))?.path();
        if path.is_dir() {
            gather_ts(&path, out)?;
        } else if path.extension().and_then(|s| s.to_str()) == Some("ts") {
            out.push(path);
        }
    }
    Ok(())
}

fn file_to_app(path: &Path) -> Result<String, String> {
    let abs = path
        .canonicalize()
        .map_err(|e| format!("resolve {}: {e}", path.display()))?;
    Ok(abs.to_string_lossy().to_string())
}

fn source_for(path: &Path) -> Result<String, String> {
    let text = fs::read_to_string(path).map_err(|e| format!("read {}: {e}", path.display()))?;
    for raw in text.lines().take(4) {
        let line = raw.trim();
        if let Some(rest) = line.strip_prefix("// origin:") {
            return Ok(app_path(rest.trim()));
        }
    }
    file_to_app(path)
}

fn exported_symbols(text: &str) -> Vec<(usize, String)> {
    let mut out = Vec::new();
    for (idx, raw) in text.lines().enumerate() {
        let line = raw.trim_start();
        for prefix in ["export const ", "export function "] {
            if let Some(rest) = line.strip_prefix(prefix) {
                let symbol: String = rest
                    .chars()
                    .take_while(|c| c.is_ascii_alphanumeric() || *c == '_')
                    .collect();
                if !symbol.is_empty() {
                    out.push((idx + 1, symbol));
                }
            }
        }
    }
    out
}
