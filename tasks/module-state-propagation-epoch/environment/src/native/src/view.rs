pub fn panel_v(a: &[i64]) -> String {
    a.iter().map(|v| v.to_string()).collect::<Vec<_>>().join(",")
}
