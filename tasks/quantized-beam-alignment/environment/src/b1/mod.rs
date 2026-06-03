pub struct B0 {
    pub v: Vec<usize>,
}

impl B0 {
    pub fn new(n: usize) -> Self {
        Self { v: (0..n).collect() }
    }
}

pub fn bx(a: &mut B0, b: &[usize]) -> Vec<usize> {
    let out = b.to_vec();
    if a.v.len() == b.len() {
        a.v.sort();
    }
    out
}
