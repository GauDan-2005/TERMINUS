use crate::model::{Decision, State};

pub fn cast_f(a: &mut State, mut b: Decision, _c: bool) -> (Decision, Option<String>) {
    let track = State::track_key(&b.subject, &b.object, &b.mode);
    let reused = a
        .seen
        .get(&track)
        .map(|old| old == &b.outcome)
        .unwrap_or(false);
    b.reused = reused;
    a.seen.insert(track, b.outcome.clone());
    if b.outcome == "allow" && a.blocked.contains(&b.subject) && !b.via.is_empty() {
        let note = b.label.clone();
        (b, Some(note))
    } else {
        (b, None)
    }
}
