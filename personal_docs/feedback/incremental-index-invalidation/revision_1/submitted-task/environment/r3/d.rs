use crate::io::{app_path, collect_entries, resolve_target_root};
use crate::model::State;

pub fn lift_d(a: &mut State, b: &str, c: &str) -> Result<(), String> {
    a.epoch += 1;
    let shown = app_path(c);
    let actual = resolve_target_root(c)?;
    a.active.insert(b.to_string(), shown);
    let mut found = collect_entries(a, b, &actual, a.epoch)?;
    a.entries.append(&mut found);
    Ok(())
}
