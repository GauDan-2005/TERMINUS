use crate::io::{app_path, collect_entries};
use crate::model::State;

pub fn fold_b(a: &mut State, b: &str, c: &str) -> Result<(), String> {
    a.epoch += 1;
    let root = app_path(c);
    a.active.insert(b.to_string(), root);
    let mut found = collect_entries(a, b, c, a.epoch)?;
    a.entries.append(&mut found);
    Ok(())
}
