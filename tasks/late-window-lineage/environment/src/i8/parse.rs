use std::io;

use crate::f5::types::R0;

pub fn parse_row(origin: &str, text: &str) -> io::Result<Option<R0>> {
    let trimmed = text.trim();
    if trimmed.is_empty() || trimmed.starts_with('#') {
        return Ok(None);
    }
    let parts: Vec<&str> = trimmed.split(',').map(str::trim).collect();
    if parts.len() != 6 {
        return Err(io::Error::new(io::ErrorKind::InvalidData, format!("bad row: {trimmed}")));
    }
    let seq: u64 = parts[0].parse().map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "bad seq"))?;
    let slot: i64 = parts[2].parse().map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "bad slot"))?;
    let delta: i64 = parts[4].parse().map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "bad delta"))?;
    Ok(Some(R0 {
        origin: origin.to_string(),
        seq,
        part: parts[1].to_string(),
        bucket: (slot / 10) * 10,
        name: parts[3].to_string(),
        delta,
        token: parts[5].to_string(),
    }))
}
