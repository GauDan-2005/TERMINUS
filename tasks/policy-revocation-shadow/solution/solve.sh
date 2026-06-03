#!/bin/bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path

files = {
    Path("/app/k0/a.rs"): '''use crate::io::split_subject_object_mode;
use crate::k1_b::fold_b;
use crate::k2_c::{emit_c, store_cache};
use crate::k3_d::lift_d;
use crate::k4_e::mote_e;
use crate::k5_f::cast_f;
use crate::model::{CaseReport, Decision, Event, State};

pub fn phase_a(a: &mut State, b: &Event, c: &mut CaseReport) -> Result<(), String> {
    match b.kind.as_str() {
        "grant" => {
            let (object, mode) = b
                .right
                .split_once('/')
                .ok_or_else(|| format!("bad grant row {}", b.right))?;
            a.direct
                .insert((b.left.clone(), object.to_string(), mode.to_string()));
            let prefix = format!("{}|{}|{}|", b.left, object, mode);
            a.store.retain(|key, _| !key.starts_with(&prefix));
            a.clock += 1;
            Ok(())
        }
        "delegate" => {
            a.chain.insert(b.right.clone(), b.left.clone());
            a.clock += 1;
            Ok(())
        }
        "revoke" => fold_b(a, &b.left),
        "batch" => {
            a.group_active = b.left.clone();
            a.group_slot.clear();
            Ok(())
        }
        "end" => {
            a.group_active.clear();
            a.group_slot.clear();
            Ok(())
        }
        "check" => {
            let (subject, object, mode) = split_subject_object_mode(&b.right)?;
            let row = if a.group_active.is_empty() {
                wrap_g(a, &b.left, &subject, &object, &mode)
            } else {
                lift_d(a, &b.left, &subject, &object, &mode)
            };
            let (row, note) = cast_f(a, row, true);
            c.decisions.push(row);
            if let Some(note) = note {
                c.stale.push(note);
            }
            Ok(())
        }
        other => Err(format!("unknown trace row {other}")),
    }
}

fn wrap_g(a: &mut State, label: &str, subject: &str, object: &str, mode: &str) -> Decision {
    let tick = a.tick_for(subject);
    if let Some(outcome) = emit_c(a, subject, object, mode) {
        let via = if outcome == "allow" {
            mote_e(a, subject, object, mode).1
        } else {
            String::new()
        };
        let mut row = Decision::blank(label, subject, object, mode, tick);
        row.outcome = outcome;
        row.via = via;
        return row;
    }
    let (outcome, via) = mote_e(a, subject, object, mode);
    store_cache(a, subject, object, mode, &outcome);
    let mut row = Decision::blank(label, subject, object, mode, tick);
    row.outcome = outcome;
    row.via = via;
    row
}
''',
    Path("/app/k1/b.rs"): '''use crate::model::State;

pub fn fold_b(a: &mut State, b: &str) -> Result<(), String> {
    let next = a.tick_for(b) + 1;
    a.ticks.insert(b.to_string(), next);
    a.blocked.insert(b.to_string());
    let prefix = format!("{b}|");
    a.store.retain(|key, _| !key.starts_with(&prefix));
    a.seen.retain(|key, _| !key.starts_with(&prefix));
    a.group_slot.clear();
    a.clock += 1;
    Ok(())
}
''',
    Path("/app/k2/c.rs"): '''use crate::model::State;

pub fn cache_key(a: &State, subject: &str, object: &str, mode: &str) -> String {
    format!("{}|{}|{}|{}", subject, object, mode, a.tick_for(subject))
}

pub fn emit_c(a: &State, subject: &str, object: &str, mode: &str) -> Option<String> {
    let key = cache_key(a, subject, object, mode);
    a.store.get(&key).cloned()
}

pub fn store_cache(a: &mut State, subject: &str, object: &str, mode: &str, outcome: &str) {
    let key = cache_key(a, subject, object, mode);
    a.store.insert(key, outcome.to_string());
}
''',
    Path("/app/k3/d.rs"): '''use crate::k4_e::mote_e;
use crate::model::{Decision, State};

pub fn lift_d(a: &mut State, label: &str, subject: &str, object: &str, mode: &str) -> Decision {
    let tick = a.tick_for(subject);
    let (outcome, via) = mote_e(a, subject, object, mode);
    let mut row = Decision::blank(label, subject, object, mode, tick);
    row.outcome = outcome;
    row.group = a.group_active.clone();
    row.via = via;
    row
}
''',
    Path("/app/k4/e.rs"): '''use crate::model::State;

pub fn mote_e(a: &State, subject: &str, object: &str, mode: &str) -> (String, String) {
    let mut current = subject.to_string();
    loop {
        if a.blocked.contains(&current) {
            return ("deny".to_string(), String::new());
        }
        if a.direct.contains(&(current.clone(), object.to_string(), mode.to_string())) {
            let via = if current == subject {
                String::new()
            } else {
                current.clone()
            };
            return ("allow".to_string(), via);
        }
        match a.chain.get(&current) {
            Some(parent) => current = parent.clone(),
            None => return ("deny".to_string(), String::new()),
        }
    }
}
''',
    Path("/app/k5/f.rs"): '''use crate::model::{Decision, State};

pub fn cast_f(a: &mut State, mut row: Decision, _c: bool) -> (Decision, Option<String>) {
    let track = format!(
        "{}|{}|{}|{}",
        row.subject, row.object, row.mode, row.tick
    );
    let reused = a
        .seen
        .get(&track)
        .map(|old| old == &row.outcome)
        .unwrap_or(false);
    row.reused = reused;
    a.seen.insert(track, row.outcome.clone());
    if row.outcome == "allow" && a.blocked.contains(&row.subject) && !row.via.is_empty() {
        let note = row.label.clone();
        (row, Some(note))
    } else {
        (row, None)
    }
}
''',
}

for path, content in files.items():
    path.write_text(content, encoding="utf-8")
    print(f"wrote {path}")
PY

cd /app && cargo build --offline --locked --quiet
bash /app/scripts/run-matrix.sh
