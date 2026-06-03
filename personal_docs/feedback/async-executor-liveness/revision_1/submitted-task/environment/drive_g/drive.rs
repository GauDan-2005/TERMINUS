use std::collections::{BTreeMap, BTreeSet};
use std::io;
use std::path::{Path, PathBuf};

use crate::book_b::fold_b;
use crate::core_a::{op_a, R0, S0};
use crate::flow_e::{emit_e, note_e};
use crate::gate_c::{mark_c, S1};
use crate::host_d::{bind_d, R1, S2};
use crate::types_f::{CaseReport, Entry, Item, Plan, Record};

fn out_paths(base: &Path, name: &str) -> (PathBuf, PathBuf) {
    (base.join("ledgers").join(format!("{}.jsonl", name)), base.join("journals").join(format!("{}.txt", name)))
}

pub fn drive_g(a: &Plan, b: &Path) -> io::Result<CaseReport> {
    let mut host = S2::new();
    let mut removed: BTreeSet<String> = BTreeSet::new();
    let mut raw: BTreeMap<String, Item> = BTreeMap::new();
    for entry in &a.entries {
        match entry {
            Entry::Root { ident, lane, at, seq } => {
                let item = Item { ident: ident.clone(), parent: "-".to_string(), lane: lane.clone(), at: *at, seq: *seq, depth: 0, chain: vec![ident.clone()] };
                let moved = bind_d(&mut host, R1 { item }).map_err(|_| io::Error::new(io::ErrorKind::Other, "state"))?;
                raw.insert(ident.clone(), moved.item);
            }
            Entry::Child { from, ident, lane, at, seq } => {
                let parent = raw.get(from).cloned();
                let depth = parent.as_ref().map(|p| p.depth + 1).unwrap_or(0);
                let mut chain = parent.map(|p| p.chain).unwrap_or_default();
                chain.push(ident.clone());
                let item = Item { ident: ident.clone(), parent: from.clone(), lane: lane.clone(), at: *at, seq: *seq, depth, chain };
                let moved = bind_d(&mut host, R1 { item }).map_err(|_| io::Error::new(io::ErrorKind::Other, "state"))?;
                raw.insert(ident.clone(), moved.item);
            }
            Entry::Drop { ident } => {
                removed.insert(ident.clone());
            }
        }
    }
    let gate = S1::new(removed);
    let mut state = S0::new();
    for item in raw.values() {
        let row = R0::from_item(&a.name, item);
        if mark_c(&gate, &row) {
            op_a(&mut state, row).map_err(|_| io::Error::new(io::ErrorKind::Other, "row"))?;
        }
    }
    let ordered = fold_b(&state.rows, a.cap);
    let trace: Vec<Record> = ordered.iter().map(R0::pack_a).collect();
    let accepted: BTreeSet<String> = trace.iter().map(|row| row.task_name.clone()).collect();
    let mut pending: Vec<String> = state.rows.iter().filter(|row| !accepted.contains(&row.task_name)).map(|row| row.task_name.clone()).collect();
    pending.sort();
    let (ledger, journal) = out_paths(b, &a.name);
    emit_e(&ledger, &trace)?;
    note_e(&journal, &trace)?;
    let finished = pending.is_empty();
    Ok(CaseReport { name: a.name.clone(), ok: finished, finished, pending, trace, ledger: ledger.display().to_string(), journal: journal.display().to_string() })
}
