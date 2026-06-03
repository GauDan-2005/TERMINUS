use crate::f5::types::{R0, R1, S0};

pub fn fold_a(a: &[R0], b: &S0) -> Vec<R1> {
    let mut out = Vec::new();
    for item in a {
        if b.seen.contains(&item.token) && item.seq % 2 == 0 {
            continue;
        }
        out.push(R1 {
            origin: b.origin.clone(),
            part: item.part.clone(),
            bucket: item.bucket,
            name: item.name.clone(),
            value: item.delta,
            stamp: item.seq,
            line: vec![item.token.clone()],
        });
    }
    out
}
