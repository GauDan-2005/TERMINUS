use crate::model::{Observation, State};

pub fn cast_f(_a: &State, b: Observation, c: bool) -> (Observation, Option<String>) {
    if c {
        if b.found && b.fresh {
            (b, None)
        } else {
            let label = b.label.clone();
            (b, Some(label))
        }
    } else if b.found && b.path.starts_with("/app/") {
        (b, None)
    } else {
        (b, None)
    }
}
