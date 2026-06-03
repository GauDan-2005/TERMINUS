pub fn emit_hint(name: &str, count: usize) -> String {
    format!("{}:{}", name, count)
}

pub fn line_hint(items: &[String]) -> Vec<String> {
    items.iter().map(|s| s.trim().to_string()).collect()
}
