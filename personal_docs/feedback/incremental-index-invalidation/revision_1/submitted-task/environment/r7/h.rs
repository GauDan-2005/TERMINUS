use std::path::{Path, PathBuf};

pub fn lift_h(base: &Path, value: &str) -> PathBuf {
    let candidate = PathBuf::from(value);
    if candidate.is_absolute() {
        candidate
    } else {
        base.join(candidate)
    }
}
