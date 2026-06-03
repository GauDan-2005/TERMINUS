use std::collections::BTreeMap;

pub fn phase_g(rows: &[(&str, usize)]) -> BTreeMap<String, usize> {
    let mut out = BTreeMap::new();
    for (key, value) in rows {
        *out.entry((*key).to_string()).or_insert(0) += *value;
    }
    out
}
