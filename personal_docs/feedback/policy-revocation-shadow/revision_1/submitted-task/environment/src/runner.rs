use crate::io::read_trace;
use crate::k0_a::phase_a;
use crate::model::{CaseReport, State};
use crate::report::write_report;
use std::path::{Path, PathBuf};

pub fn run_all(out: &Path, traces: &[PathBuf]) -> Result<(), String> {
    let mut cases = Vec::new();
    for trace in traces {
        cases.push(run_one(trace)?);
    }
    write_report(out, &cases)
}

fn run_one(trace: &Path) -> Result<CaseReport, String> {
    let name = trace
        .file_stem()
        .and_then(|s| s.to_str())
        .ok_or_else(|| format!("trace name: {}", trace.display()))?
        .to_string();
    let events = read_trace(trace)?;
    let mut state = State::new();
    let mut case = CaseReport {
        name,
        ok: true,
        decisions: Vec::new(),
        stale: Vec::new(),
    };
    for event in events {
        phase_a(&mut state, &event, &mut case)?;
    }
    case.ok = case.stale.is_empty();
    Ok(case)
}
