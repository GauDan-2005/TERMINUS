use std::collections::BTreeSet;

use crate::f5::types::{R1, R2, S2};

pub fn mark_c(a: &mut S2, b: &R1) -> Option<R2> {
    let id = format!("{}:{}:{}:{}", b.origin, b.name, b.bucket, b.value);
    if a.seen.contains(&id) {
        return None;
    }
    a.seen.insert(id.clone());
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
    let mut seen = S2 { seen: BTreeSet::new() };
    rows.iter().filter_map(|row| mark_c(&mut seen, row)).collect()
}
