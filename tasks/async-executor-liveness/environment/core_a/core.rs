use crate::types_f::{Item, Record};

pub struct S0 {
    pub rows: Vec<R0>,
    pub names: Vec<String>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct R0 {
    pub case_name: String,
    pub task_name: String,
    pub parent_name: String,
    pub depth: usize,
    pub lane_name: String,
    pub base_turn: u64,
    pub turn: u64,
    pub seq: usize,
    pub chain: Vec<String>,
}

#[derive(Debug)]
pub enum E0 {
    Halt,
}

impl S0 {
    pub fn new() -> Self {
        Self { rows: Vec::new(), names: Vec::new() }
    }
}

impl R0 {
    pub fn from_item(case_name: &str, item: &Item) -> Self {
        Self {
            case_name: case_name.to_string(),
            task_name: item.ident.clone(),
            parent_name: item.parent.clone(),
            depth: item.depth,
            lane_name: item.lane.clone(),
            base_turn: item.at,
            turn: item.at,
            seq: item.seq,
            chain: item.chain.clone(),
        }
    }

    pub fn pack_a(&self) -> Record {
        Record {
            case_name: self.case_name.clone(),
            task_name: self.task_name.clone(),
            parent_name: self.parent_name.clone(),
            depth: self.depth,
            lane_name: self.lane_name.clone(),
            turn: self.turn,
        }
    }
}

pub fn op_a(a: &mut S0, b: R0) -> Result<(), E0> {
    a.names.push(b.task_name.clone());
    a.rows.push(b);
    Ok(())
}
