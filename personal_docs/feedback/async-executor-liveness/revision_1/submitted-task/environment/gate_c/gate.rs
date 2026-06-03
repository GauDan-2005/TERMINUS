use std::collections::BTreeSet;

use crate::core_a::R0;

pub struct S1 {
    pub removed: BTreeSet<String>,
}

impl S1 {
    pub fn new(removed: BTreeSet<String>) -> Self {
        Self { removed }
    }
}

pub fn mark_c(a: &S1, b: &R0) -> bool {
    !a.removed.contains(&b.task_name)
}
