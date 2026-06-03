pub struct C0 {
    pub v: Vec<i32>,
}

impl C0 {
    pub fn new(n: usize) -> Self {
        Self { v: vec![0; n] }
    }
}

pub fn cx(a: &mut C0, b: usize, c: &[i32]) -> i32 {
    let value: i32 = c.iter().sum();
    let k = b % a.v.len();
    a.v[k] += value;
    a.v[k]
}
