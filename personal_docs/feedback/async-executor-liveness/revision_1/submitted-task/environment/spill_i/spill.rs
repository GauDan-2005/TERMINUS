pub fn fold_hint(values: &[usize], cap: usize) -> Vec<usize> {
    values.iter().copied().filter(|v| *v <= cap).collect()
}

pub fn bucket_hint(values: &[usize]) -> usize {
    values.iter().fold(0usize, |acc, v| acc.saturating_add(*v))
}
