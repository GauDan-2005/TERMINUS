use crate::model::State;

pub fn emit_c(a: &State, _b: &str, c: &str, d: &str) -> Option<String> {
    let key = State::slot_key(c, d);
    a.store.get(&key).cloned()
}
