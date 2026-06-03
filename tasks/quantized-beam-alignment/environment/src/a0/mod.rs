pub struct A0 {
    pub s: Vec<i32>,
    pub z: Vec<i32>,
}

impl A0 {
    pub fn new() -> Self {
        Self { s: vec![2, 3, 5], z: vec![1, -1, 2] }
    }
}

pub fn ax(a: &A0, b: &[i32], c: usize) -> Vec<i32> {
    let k = c % a.s.len();
    b.iter().map(|v| v * a.s[k] + a.z[k]).collect()
}

pub fn ax_ref(a: &A0, b: &[i32]) -> Vec<i32> {
    b.iter().enumerate().map(|(i, v)| v * a.s[i] + a.z[i]).collect()
}
