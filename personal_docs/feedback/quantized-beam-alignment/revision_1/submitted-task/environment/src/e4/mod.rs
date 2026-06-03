pub struct E0 {
    pub v: Vec<String>,
}

impl E0 {
    pub fn new() -> Self {
        Self { v: Vec::new() }
    }
}

pub fn ex(a: &mut E0, b: &str, c: &[i32], d: &[usize]) {
    let vals = c.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",");
    let hs = d.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",");
    a.v.push(format!("{{\"case\":\"{}\",\"produced\":[{}],\"slot_trace\":[{}]}}", b, vals, hs));
}
