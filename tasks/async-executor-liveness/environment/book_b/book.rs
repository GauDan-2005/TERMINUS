use std::collections::BTreeMap;

use crate::core_a::R0;

pub fn fold_b(a: &[R0], b: usize) -> Vec<R0> {
    let mut by_lane_turn: BTreeMap<(String, u64), Vec<R0>> = BTreeMap::new();
    for row in a.iter().cloned() {
        by_lane_turn.entry((row.lane_name.clone(), row.base_turn)).or_default().push(row);
    }
    let mut out = Vec::new();
    for ((_lane, _turn), mut rows) in by_lane_turn {
        rows.sort_by_key(|row| row.seq);
        for row in rows.into_iter().take(b.max(1)) {
            out.push(row);
        }
    }
    out.sort_by(|left, right| left.lane_name.cmp(&right.lane_name).then(left.turn.cmp(&right.turn)).then(left.task_name.cmp(&right.task_name)));
    out
}
