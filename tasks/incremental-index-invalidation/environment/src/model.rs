use std::collections::BTreeMap;

#[derive(Clone, Debug)]
pub struct Entry {
    pub slot: String,
    pub symbol: String,
    pub path: String,
    pub source: String,
    pub line: usize,
    pub epoch: u64,
    pub handle: u64,
}

#[derive(Clone, Debug)]
pub struct Event {
    pub kind: String,
    pub left: String,
    pub right: String,
}

#[derive(Clone, Debug)]
pub struct Observation {
    pub label: String,
    pub symbol: String,
    pub found: bool,
    pub path: String,
    pub source: String,
    pub line: usize,
    pub epoch: u64,
    pub reused: bool,
    pub fresh: bool,
}

#[derive(Clone, Debug)]
pub struct CaseReport {
    pub name: String,
    pub ok: bool,
    pub observations: Vec<Observation>,
    pub stale: Vec<String>,
}

#[derive(Debug)]
pub struct State {
    pub entries: Vec<Entry>,
    pub active: BTreeMap<String, String>,
    pub handles: BTreeMap<String, u64>,
    pub last_seen: BTreeMap<String, u64>,
    pub next_handle: u64,
    pub epoch: u64,
}

impl State {
    pub fn new() -> Self {
        Self {
            entries: Vec::new(),
            active: BTreeMap::new(),
            handles: BTreeMap::new(),
            last_seen: BTreeMap::new(),
            next_handle: 1,
            epoch: 0,
        }
    }

    pub fn key_for(slot: &str, path: &str, symbol: &str) -> String {
        format!("{slot}|{path}|{symbol}")
    }

    pub fn handle_for(&mut self, slot: &str, path: &str, symbol: &str) -> u64 {
        let key = Self::key_for(slot, path, symbol);
        if let Some(value) = self.handles.get(&key) {
            *value
        } else {
            let value = self.next_handle;
            self.next_handle += 1;
            self.handles.insert(key, value);
            value
        }
    }
}

impl Observation {
    pub fn missing(label: &str, symbol: &str, epoch: u64, fresh: bool) -> Self {
        Self {
            label: label.to_string(),
            symbol: symbol.to_string(),
            found: false,
            path: String::new(),
            source: String::new(),
            line: 0,
            epoch,
            reused: false,
            fresh,
        }
    }
}
