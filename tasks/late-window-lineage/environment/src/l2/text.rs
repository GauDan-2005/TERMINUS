pub fn clean_label(value: &str) -> String {
    value.chars().filter(|ch| ch.is_ascii_alphanumeric() || *ch == '-' || *ch == '_').collect()
}
