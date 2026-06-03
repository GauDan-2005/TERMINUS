pub fn arrange(a: &[usize]) -> Vec<usize> {
    let mut x = a.to_vec();
    x.sort();
    x
}

pub fn describe(a: &[usize]) -> String {
    arrange(a).iter().map(|x| x.to_string()).collect::<Vec<_>>().join("-")
}
