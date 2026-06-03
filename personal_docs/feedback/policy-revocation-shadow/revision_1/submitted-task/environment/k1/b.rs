use crate::model::State;

pub fn fold_b(a: &mut State, b: &str) -> Result<(), String> {
    let next = a.tick_for(b) + 1;
    a.ticks.insert(b.to_string(), next);
    a.blocked.insert(b.to_string());
    a.clock += 1;
    Ok(())
}
