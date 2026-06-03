use crate::f5::types::R2;

pub fn summarize(rows: &[R2]) -> String {
    let mut parts = Vec::new();
    for row in rows.iter().take(8) {
        parts.push(format!("{}:{}:{}", row.part, row.bucket, row.name));
    }
    parts.join(" ")
}
