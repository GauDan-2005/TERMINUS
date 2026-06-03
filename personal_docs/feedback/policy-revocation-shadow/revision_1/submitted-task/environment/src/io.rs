use crate::model::Event;
use std::fs;
use std::path::Path;

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

pub fn split_subject_object_mode(value: &str) -> Result<(String, String, String), String> {
    let (subject, rest) = value
        .split_once(':')
        .ok_or_else(|| format!("bad check target {value}"))?;
    let (object, mode) = rest
        .split_once('/')
        .ok_or_else(|| format!("bad check target {value}"))?;
    Ok((subject.to_string(), object.to_string(), mode.to_string()))
}
