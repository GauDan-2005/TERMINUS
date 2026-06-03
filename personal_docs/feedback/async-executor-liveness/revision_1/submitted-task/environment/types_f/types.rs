#[derive(Clone, Debug)]
pub enum Entry {
    Root { ident: String, lane: String, at: u64, seq: usize },
    Child { from: String, ident: String, lane: String, at: u64, seq: usize },
    Drop { ident: String },
}

#[derive(Clone, Debug)]
pub struct Plan {
    pub name: String,
    pub cap: usize,
    pub entries: Vec<Entry>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Item {
    pub ident: String,
    pub parent: String,
    pub lane: String,
    pub at: u64,
    pub seq: usize,
    pub depth: usize,
    pub chain: Vec<String>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Record {
    pub case_name: String,
    pub task_name: String,
    pub parent_name: String,
    pub depth: usize,
    pub lane_name: String,
    pub turn: u64,
}

#[derive(Clone, Debug)]
pub struct CaseReport {
    pub name: String,
    pub ok: bool,
    pub finished: bool,
    pub pending: Vec<String>,
    pub trace: Vec<Record>,
    pub ledger: String,
    pub journal: String,
}
