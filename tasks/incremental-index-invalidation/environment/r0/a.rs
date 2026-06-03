use crate::model::{CaseReport, Event, State};
use crate::r1_b::fold_b;
use crate::r2_c::emit_c;
use crate::r3_d::lift_d;
use crate::r4_e::mote_e;
use crate::r5_f::cast_f;

pub fn phase_a(a: &mut State, b: &Event, c: &mut CaseReport) -> Result<(), String> {
    match b.kind.as_str() {
        "slot" => {
            if b.left == "gen" {
                emit_c(a, &b.left, &b.right)?;
            } else if b.left == "pkg" {
                lift_d(a, &b.left, &b.right)?;
            } else {
                fold_b(a, &b.left, &b.right)?;
            }
        }
        "query" => {
            let item = mote_e(a, &b.right, true);
            let (item, note) = cast_f(a, item, true);
            c.observations.push(crate::model::Observation { label: b.left.clone(), ..item });
            if let Some(note) = note {
                c.stale.push(note);
            }
        }
        "miss" => {
            let item = mote_e(a, &b.right, false);
            let (item, note) = cast_f(a, item, false);
            c.observations.push(crate::model::Observation { label: b.left.clone(), ..item });
            if let Some(note) = note {
                c.stale.push(note);
            }
        }
        other => return Err(format!("unknown trace row {other}")),
    }
    Ok(())
}
