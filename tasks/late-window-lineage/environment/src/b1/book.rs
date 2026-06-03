use crate::c2::gate::collect_c;
use crate::f5::types::{R1, R2, S1};

pub fn merge_b(a: &mut S1, b: &[R1]) -> Vec<R1> {
    let mut out = a.prior.clone();
    out.extend_from_slice(b);
    out.sort_by(|left, right| left.name.cmp(&right.name).then(left.stamp.cmp(&right.stamp)));
    out
}

pub fn finish_b(a: &mut S1, b: &[R1]) -> Vec<R2> {
    let rows = merge_b(a, b);
    collect_c(&rows)
}
