use std::fs;
use std::io;
use std::path::Path;

use crate::f5::types::{CaseReport, R2, View};

fn esc(value: &str) -> String {
    value.replace('\\', "\\\\").replace('"', "\\\"")
}

fn line_json(items: &[String]) -> String {
    let inner = items.iter().map(|item| format!("\"{}\"", esc(item))).collect::<Vec<_>>().join(",");
    format!("[{}]", inner)
}

fn total_json(row: &R2) -> String {
    format!("{{\"partition\":\"{}\",\"window\":{},\"key\":\"{}\",\"value\":{}}}", esc(&row.part), row.bucket, esc(&row.name), row.value)
}

fn corr_json(row: &R2) -> String {
    format!("{{\"partition\":\"{}\",\"window\":{},\"key\":\"{}\",\"value\":{},\"id\":\"{}\",\"lineage\":{}}}", esc(&row.part), row.bucket, esc(&row.name), row.value, esc(&row.id), line_json(&row.line))
}

fn view_json(view: &View) -> String {
    let totals = view.totals.iter().map(total_json).collect::<Vec<_>>().join(",");
    let corrections = view.corrections.iter().map(corr_json).collect::<Vec<_>>().join(",");
    format!("{{\"totals\":[{}],\"corrections\":[{}]}}", totals, corrections)
}

fn case_json(case: &CaseReport) -> String {
    format!("{{\"name\":\"{}\",\"ok\":{},\"direct\":{},\"replay\":{},\"repeat\":{}}}", esc(&case.name), if case.ok { "true" } else { "false" }, view_json(&case.direct), view_json(&case.replay), if case.repeat { "true" } else { "false" })
}

pub fn write_report(path: &Path, cases: &[CaseReport]) -> io::Result<()> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let body = cases.iter().map(case_json).collect::<Vec<_>>().join(",");
    fs::write(path, format!("{{\"cases\":[{}]}}\n", body))
}
