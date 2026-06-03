pub fn dx(a: &[i32], b: &[usize]) -> Vec<i32> {
    b.iter().map(|i| a[*i]).collect()
}

pub fn tag(a: &str, b: usize) -> String {
    format!("{}:{}", a, b)
}
