pub fn r_d(a: &str, b: i64, c: i64) -> i64 {
    match a {
        "old" => b,
        "new" => b + c,
        _ => b,
    }
}

pub fn aux_r(a: i64) -> i64 {
    a * 2
}
