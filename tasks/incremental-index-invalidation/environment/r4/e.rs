use crate::model::{Observation, State};

pub fn mote_e(a: &mut State, b: &str, c: bool) -> Observation {
    if let Some(entry) = a.entries.iter().find(|entry| entry.symbol == b) {
        let reused = a.last_seen.get(b).map(|old| *old == entry.handle).unwrap_or(false);
        a.last_seen.insert(b.to_string(), entry.handle);
        let fresh = a
            .active
            .get(&entry.slot)
            .map(|root| entry.path.starts_with(root))
            .unwrap_or(false);
        Observation {
            label: String::new(),
            symbol: b.to_string(),
            found: true,
            path: entry.path.clone(),
            source: entry.source.clone(),
            line: entry.line,
            epoch: entry.epoch,
            reused,
            fresh,
        }
    } else {
        Observation::missing(b, b, a.epoch, !c)
    }
}
