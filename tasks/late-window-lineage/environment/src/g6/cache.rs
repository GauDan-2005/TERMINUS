use std::collections::BTreeMap;

#[derive(Default)]
pub struct DisplayBag {
    items: BTreeMap<String, String>,
}

impl DisplayBag {
    pub fn put(&mut self, a: &str, b: &str) {
        self.items.insert(a.to_string(), b.to_string());
    }

    pub fn get(&self, a: &str) -> Option<&str> {
        self.items.get(a).map(String::as_str)
    }
}
