#!/bin/bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path

files = {
    Path("/app/r0/a.rs"): '''use crate::model::{CaseReport, Event, State};
use crate::r1_b::fold_b;
use crate::r2_c::emit_c;
use crate::r3_d::lift_d;
use crate::r4_e::mote_e;
use crate::r5_f::cast_f;

pub fn phase_a(a: &mut State, b: &Event, c: &mut CaseReport) -> Result<(), String> {
    match b.kind.as_str() {
        "slot" => {
            if b.left == "gen" {
                emit_c(a, &b.left, &b.right)?;
            } else if b.left == "pkg" {
                lift_d(a, &b.left, &b.right)?;
            } else {
                fold_b(a, &b.left, &b.right)?;
            }
        }
        "query" => {
            let mut item = mote_e(a, &b.right, true);
            item.label = b.left.clone();
            let (item, note) = cast_f(a, item, true);
            c.observations.push(item);
            if let Some(note) = note {
                c.stale.push(note);
            }
        }
        "miss" => {
            let mut item = mote_e(a, &b.right, false);
            item.label = b.left.clone();
            let (item, note) = cast_f(a, item, false);
            c.observations.push(item);
            if let Some(note) = note {
                c.stale.push(note);
            }
        }
        other => return Err(format!("unknown trace row {other}")),
    }
    Ok(())
}
''',
    Path("/app/r1/b.rs"): '''use crate::io::{app_path, collect_entries};
use crate::model::State;

pub fn fold_b(a: &mut State, b: &str, c: &str) -> Result<(), String> {
    a.epoch += 1;
    let root = app_path(c);
    a.entries.retain(|entry| entry.slot != b);
    let mut found = collect_entries(a, b, c, a.epoch)?;
    a.active.insert(b.to_string(), root);
    a.entries.append(&mut found);
    a.entries.sort_by(|left, right| {
        left.slot
            .cmp(&right.slot)
            .then(left.symbol.cmp(&right.symbol))
            .then(left.path.cmp(&right.path))
    });
    Ok(())
}
''',
    Path("/app/r2/c.rs"): '''use crate::io::{app_path, collect_entries};
use crate::model::State;

pub fn emit_c(a: &mut State, b: &str, c: &str) -> Result<(), String> {
    a.epoch += 1;
    let root = app_path(c);
    a.entries.retain(|entry| entry.slot != b);
    let mut found = collect_entries(a, b, c, a.epoch)?;
    a.active.insert(b.to_string(), root);
    for entry in &found {
        if !entry.source.starts_with("/app/") {
            return Err(format!("source outside app for {}", entry.symbol));
        }
    }
    a.entries.append(&mut found);
    a.entries.sort_by(|left, right| {
        left.slot
            .cmp(&right.slot)
            .then(left.symbol.cmp(&right.symbol))
            .then(left.source.cmp(&right.source))
    });
    Ok(())
}
''',
    Path("/app/r3/d.rs"): '''use crate::io::{collect_entries, resolve_target_root};
use crate::model::State;

pub fn lift_d(a: &mut State, b: &str, c: &str) -> Result<(), String> {
    a.epoch += 1;
    let actual = resolve_target_root(c)?;
    a.entries.retain(|entry| entry.slot != b);
    let mut found = collect_entries(a, b, &actual, a.epoch)?;
    a.active.insert(b.to_string(), actual.clone());
    for entry in &found {
        if !entry.path.starts_with(&actual) {
            return Err(format!("unmatched target for {}", entry.symbol));
        }
    }
    a.entries.append(&mut found);
    a.entries.sort_by(|left, right| {
        left.slot
            .cmp(&right.slot)
            .then(left.symbol.cmp(&right.symbol))
            .then(left.path.cmp(&right.path))
    });
    Ok(())
}
''',
    Path("/app/r4/e.rs"): '''use crate::model::{Observation, State};

pub fn mote_e(a: &mut State, b: &str, c: bool) -> Observation {
    let chosen = a
        .entries
        .iter()
        .filter(|entry| entry.symbol == b)
        .filter(|entry| {
            a.active
                .get(&entry.slot)
                .map(|root| entry.path.starts_with(root))
                .unwrap_or(false)
        })
        .max_by(|left, right| {
            left.epoch
                .cmp(&right.epoch)
                .then(left.path.cmp(&right.path))
        });

    if let Some(entry) = chosen {
        let reused = a
            .last_seen
            .get(b)
            .map(|old| *old == entry.handle)
            .unwrap_or(false);
        let handle = entry.handle;
        let result = Observation {
            label: String::new(),
            symbol: b.to_string(),
            found: true,
            path: entry.path.clone(),
            source: entry.source.clone(),
            line: entry.line,
            epoch: a.epoch,
            reused,
            fresh: true,
        };
        a.last_seen.insert(b.to_string(), handle);
        result
    } else {
        Observation::missing(b, b, a.epoch, !c)
    }
}
''',
    Path("/app/r5/f.rs"): '''use crate::model::{Observation, State};

pub fn cast_f(_a: &State, b: Observation, c: bool) -> (Observation, Option<String>) {
    let label = if b.label.is_empty() {
        b.symbol.clone()
    } else {
        b.label.clone()
    };
    if c {
        if b.found
            && b.fresh
            && b.path.starts_with("/app/")
            && b.source.starts_with("/app/")
            && b.line > 0
        {
            (b, None)
        } else {
            (b, Some(label))
        }
    } else if !b.found && b.path.is_empty() && b.source.is_empty() && b.line == 0 && b.fresh {
        (b, None)
    } else {
        (b, Some(label))
    }
}
''',
}

for path, text in files.items():
    path.write_text(text)
PY
