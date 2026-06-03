use std::collections::BTreeSet;
use std::io;
use std::path::{Path, PathBuf};

use crate::a0::core::fold_a;
use crate::b1::book::finish_b;
use crate::d3::host::{open_state, save_d};
use crate::e4::flow::{push_e, read_e};
use crate::f5::serde::write_report;
use crate::f5::types::{CaseReport, R0, R1, R2, S0, S1, View};
use crate::j9::cases::{load_case, names};
use crate::m3::check::same_view;

fn root_dir() -> PathBuf {
    PathBuf::from("/app")
}

fn state_path(name: &str, suffix: &str) -> PathBuf {
    PathBuf::from("/app/state").join(format!("{name}-{suffix}.rows"))
}

fn trace_path(name: &str, suffix: &str) -> PathBuf {
    PathBuf::from("/app/output/traces").join(format!("{name}-{suffix}.rows"))
}

fn base(origin: &str) -> S0 {
    S0 { origin: origin.to_string(), seen: BTreeSet::new() }
}

fn with_seen(origin: &str, rows: &[R1], seen: BTreeSet<String>) -> S0 {
    let mut joined = seen;
    for row in rows {
        for part in &row.line {
            joined.insert(part.clone());
        }
    }
    S0 { origin: origin.to_string(), seen: joined }
}

fn totals_from(rows: &[R2]) -> Vec<R2> {
    let mut totals: Vec<R2> = Vec::new();
    for row in rows {
        if let Some(existing) = totals.iter_mut().find(|item| item.part == row.part && item.bucket == row.bucket && item.name == row.name) {
            *existing = row.clone();
        } else {
            totals.push(row.clone());
        }
    }
    totals.sort_by(|a, b| a.part.cmp(&b.part).then(a.bucket.cmp(&b.bucket)).then(a.name.cmp(&b.name)));
    totals
}

fn view_from(name: &str, suffix: &str, rows: Vec<R2>) -> io::Result<View> {
    let path = trace_path(name, suffix);
    push_e(&path, &rows)?;
    let corrections = read_e(&path)?;
    Ok(View { totals: totals_from(&corrections), corrections })
}

fn direct_view(name: &str, rows: &[R0]) -> io::Result<View> {
    let folded = fold_a(rows, &base(name));
    let mut prior = S1 { prior: Vec::new() };
    view_from(name, "direct", finish_b(&mut prior, &folded))
}

fn replay_view(name: &str, rows: &[R0], suffix: &str) -> io::Result<View> {
    let split = rows.len() / 2;
    let first = fold_a(&rows[..split], &base(name));
    let path = state_path(name, suffix);
    save_d(&path, &first)?;
    let loaded = open_state(&path)?;
    let state = with_seen(name, &loaded.rows, loaded.seen);
    let rest = fold_a(rows, &state);
    let mut prior = S1 { prior: loaded.rows };
    view_from(name, suffix, finish_b(&mut prior, &rest))
}

fn report_case(root: &Path, name: &str) -> io::Result<CaseReport> {
    let rows = load_case(root, name)?;
    let direct = direct_view(name, &rows)?;
    let replay = replay_view(name, &rows, "replay")?;
    let second = replay_view(name, &rows, "again")?;
    let repeat = replay.corrections == second.corrections;
    let ok = same_view(&direct, &replay) && repeat;
    Ok(CaseReport { name: name.to_string(), ok, direct, replay, repeat })
}

pub fn write_all(path: &Path) -> io::Result<()> {
    let root = root_dir();
    let mut reports = Vec::new();
    for name in names() {
        reports.push(report_case(&root, name)?);
    }
    write_report(path, &reports)
}
