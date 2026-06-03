#!/bin/bash
set -euo pipefail

cat > /app/core_a/core.rs <<'RS'
use std::collections::BTreeSet;

use crate::types_f::{Item, Record};

pub struct S0 {
    pub rows: Vec<R0>,
    pub names: BTreeSet<String>,
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
        Self { rows: Vec::new(), names: BTreeSet::new() }
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
    if a.names.contains(&b.task_name) {
        return Ok(());
    }
    a.names.insert(b.task_name.clone());
    a.rows.push(b);
    Ok(())
}
RS

cat > /app/book_b/book.rs <<'RS'
use std::collections::BTreeSet;

use crate::core_a::R0;

pub fn fold_b(a: &[R0], b: usize) -> Vec<R0> {
    let cap = b.max(1);
    let mut pending = a.to_vec();
    pending.sort_by_key(|row| (row.base_turn, row.seq));
    let mut out: Vec<R0> = Vec::new();
    let mut turn = pending.first().map(|row| row.base_turn).unwrap_or(0);
    while !pending.is_empty() {
        if pending.iter().all(|row| row.base_turn > turn) {
            turn = pending.iter().map(|row| row.base_turn).min().unwrap_or(turn);
            continue;
        }
        let lanes: BTreeSet<String> = pending
            .iter()
            .filter(|row| row.base_turn <= turn)
            .map(|row| row.lane_name.clone())
            .collect();
        let mut chosen: BTreeSet<String> = BTreeSet::new();
        for lane in lanes {
            let mut ready: Vec<R0> = pending
                .iter()
                .filter(|row| row.base_turn <= turn && row.lane_name == lane)
                .cloned()
                .collect();
            ready.sort_by_key(|row| (row.base_turn, row.seq));
            for mut row in ready.into_iter().take(cap) {
                row.turn = turn;
                chosen.insert(row.task_name.clone());
                out.push(row);
            }
        }
        pending = pending
            .into_iter()
            .filter(|row| !chosen.contains(&row.task_name))
            .collect();
        pending.sort_by_key(|row| (row.base_turn, row.seq));
        turn += 1;
    }
    out
}
RS

cat > /app/gate_c/gate.rs <<'RS'
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
    !b.chain.iter().any(|part| a.removed.contains(part))
}
RS

cat > /app/host_d/host.rs <<'RS'
use std::collections::BTreeMap;

use crate::core_a::E0;
use crate::types_f::Item;

pub struct S2 {
    pub items: BTreeMap<String, Item>,
}

pub struct R1 {
    pub item: Item,
}

pub struct R2 {
    pub item: Item,
}

impl S2 {
    pub fn new() -> Self {
        Self { items: BTreeMap::new() }
    }
}

pub fn bind_d(a: &mut S2, b: R1) -> Result<R2, E0> {
    if let Some(existing) = a.items.get(&b.item.ident).cloned() {
        return Ok(R2 { item: existing });
    }
    a.items.insert(b.item.ident.clone(), b.item.clone());
    Ok(R2 { item: b.item })
}
RS

perl -0pi -e 's/for row in b\.iter\(\)\.rev\(\) \{/for row in b {/g' /app/flow_e/flow.rs

cat > /app/drive_g/drive.rs <<'RS'
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

fn add_item(raw: &mut BTreeMap<String, Item>, order: &mut Vec<String>, ident: &str, item: Item) {
    if raw.contains_key(ident) {
        return;
    }
    order.push(ident.to_string());
    raw.insert(ident.to_string(), item);
}

pub fn drive_g(a: &Plan, b: &Path) -> io::Result<CaseReport> {
    let mut host = S2::new();
    let mut removed: BTreeSet<String> = BTreeSet::new();
    let mut raw: BTreeMap<String, Item> = BTreeMap::new();
    let mut order: Vec<String> = Vec::new();
    for entry in &a.entries {
        match entry {
            Entry::Root { ident, lane, at, seq } => {
                let item = Item { ident: ident.clone(), parent: "-".to_string(), lane: lane.clone(), at: *at, seq: *seq, depth: 0, chain: vec![ident.clone()] };
                let moved = bind_d(&mut host, R1 { item }).map_err(|_| io::Error::new(io::ErrorKind::Other, "state"))?;
                add_item(&mut raw, &mut order, ident, moved.item);
            }
            Entry::Child { from, ident, lane, at, seq } => {
                if raw.contains_key(ident) {
                    continue;
                }
                let parent = raw.get(from).cloned();
                let depth = parent.as_ref().map(|p| p.depth + 1).unwrap_or(0);
                let mut chain = parent.as_ref().map(|p| p.chain.clone()).unwrap_or_default();
                chain.push(ident.clone());
                let item = Item { ident: ident.clone(), parent: from.clone(), lane: lane.clone(), at: *at, seq: *seq, depth, chain };
                let moved = bind_d(&mut host, R1 { item }).map_err(|_| io::Error::new(io::ErrorKind::Other, "state"))?;
                add_item(&mut raw, &mut order, ident, moved.item);
            }
            Entry::Drop { ident } => {
                removed.insert(ident.clone());
            }
        }
    }
    let gate = S1::new(removed);
    let mut state = S0::new();
    for ident in &order {
        if let Some(item) = raw.get(ident) {
            let row = R0::from_item(&a.name, item);
            if mark_c(&gate, &row) {
                op_a(&mut state, row).map_err(|_| io::Error::new(io::ErrorKind::Other, "row"))?;
            }
        }
    }
    let ordered = fold_b(&state.rows, a.cap);
    let trace: Vec<Record> = ordered.iter().map(R0::pack_a).collect();
    let accepted: BTreeSet<String> = trace.iter().map(|row| row.task_name.clone()).collect();
    let mut pending: Vec<String> = state
        .rows
        .iter()
        .filter(|row| !accepted.contains(&row.task_name))
        .map(|row| row.task_name.clone())
        .collect();
    pending.sort();
    let (ledger, journal) = out_paths(b, &a.name);
    emit_e(&ledger, &trace)?;
    note_e(&journal, &trace)?;
    let finished = pending.is_empty();
    Ok(CaseReport { name: a.name.clone(), ok: finished, finished, pending, trace, ledger: ledger.display().to_string(), journal: journal.display().to_string() })
}
RS
