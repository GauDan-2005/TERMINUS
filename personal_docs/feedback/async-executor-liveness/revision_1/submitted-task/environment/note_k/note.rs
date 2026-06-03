pub fn tag_for(name: &str) -> String {
    name.chars().take(3).collect()
}

pub fn count_nonempty(lines: &[String]) -> usize {
    lines.iter().filter(|line| !line.trim().is_empty()).count()
}
