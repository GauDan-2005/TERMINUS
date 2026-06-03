use crate::k4_e::mote_e;
use crate::model::{Decision, State};

pub fn lift_d(a: &mut State, b: &str, c: &str, d: &str, e: &str) -> Decision {
    let slot = State::slot_key(d, e);
    let tick = a.tick_for(c);
  if let Some(outcome) = a.group_slot.get(&slot) {
        let via = if outcome == "allow" {
            mote_e(a, c, d, e).1
        } else {
            String::new()
        };
        let mut row = Decision::blank(b, c, d, e, tick);
        row.outcome = outcome.clone();
        row.group = a.group_active.clone();
        row.via = via;
        return row;
    }
    let (outcome, via) = mote_e(a, c, d, e);
    a.group_slot.insert(slot, outcome.clone());
    let mut row = Decision::blank(b, c, d, e, tick);
    row.outcome = outcome;
    row.group = a.group_active.clone();
    row.via = via;
    row
}
