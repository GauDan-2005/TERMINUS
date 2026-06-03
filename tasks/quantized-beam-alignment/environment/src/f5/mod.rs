pub fn view(a: &[i32]) -> String {
    a.iter().map(|x| x.to_string()).collect::<Vec<_>>().join("|")
}

pub fn lens(a: &[i32]) -> usize {
    a.len()
}
