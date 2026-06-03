use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Debug)]
pub struct Event {
    pub kind: String,
    pub left: String,
    pub right: String,
}

#[derive(Clone, Debug)]
pub struct Decision {
    pub label: String,
    pub subject: String,
    pub object: String,
    pub mode: String,
    pub outcome: String,
    pub tick: u64,
    pub reused: bool,
    pub group: String,
    pub via: String,
}

#[derive(Clone, Debug)]
pub struct CaseReport {
    pub name: String,
    pub ok: bool,
    pub decisions: Vec<Decision>,
    pub stale: Vec<String>,
}

#[derive(Debug)]
pub struct State {
    pub direct: BTreeSet<(String, String, String)>,
    pub chain: BTreeMap<String, String>,
    pub ticks: BTreeMap<String, u64>,
    pub blocked: BTreeSet<String>,
    pub store: BTreeMap<String, String>,
    pub group_slot: BTreeMap<String, String>,
    pub group_active: String,
    pub seen: BTreeMap<String, String>,
    pub clock: u64,
}

impl State {
    pub fn new() -> Self {
        Self {
            direct: BTreeSet::new(),
            chain: BTreeMap::new(),
            ticks: BTreeMap::new(),
            blocked: BTreeSet::new(),
            store: BTreeMap::new(),
            group_slot: BTreeMap::new(),
            group_active: String::new(),
            seen: BTreeMap::new(),
            clock: 0,
        }
    }

    pub fn tick_for(&self, subject: &str) -> u64 {
        *self.ticks.get(subject).unwrap_or(&0)
    }

    pub fn slot_key(object: &str, mode: &str) -> String {
        format!("{object}|{mode}")
    }

    pub fn track_key(subject: &str, object: &str, mode: &str) -> String {
        format!("{subject}|{object}|{mode}")
    }
}

impl Decision {
    pub fn blank(label: &str, subject: &str, object: &str, mode: &str, tick: u64) -> Self {
        Self {
            label: label.to_string(),
            subject: subject.to_string(),
            object: object.to_string(),
            mode: mode.to_string(),
            outcome: String::new(),
            tick,
            reused: false,
            group: String::new(),
            via: String::new(),
        }
    }
}
