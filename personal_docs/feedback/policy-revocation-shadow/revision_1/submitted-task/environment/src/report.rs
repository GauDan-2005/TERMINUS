use crate::model::CaseReport;
use serde::Serialize;
use std::fs;
use std::path::Path;

#[derive(Serialize)]
struct RowOut {
    label: String,
    principal: String,
    resource: String,
    action: String,
    verdict: String,
    epoch: u64,
    reused: bool,
    batch_id: String,
    delegated_from: String,
}

#[derive(Serialize)]
struct CaseOut {
    name: String,
    ok: bool,
    decisions: Vec<RowOut>,
    stale: Vec<String>,
}

#[derive(Serialize)]
struct RootOut {
    cases: Vec<CaseOut>,
}

pub fn write_report(path: &Path, cases: &[CaseReport]) -> Result<(), String> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(|e| format!("mkdir {}: {e}", parent.display()))?;
    }
    let payload = RootOut {
        cases: cases
            .iter()
            .map(|case| CaseOut {
                name: case.name.clone(),
                ok: case.ok,
                stale: case.stale.clone(),
                decisions: case
                    .decisions
                    .iter()
                    .map(|row| RowOut {
                        label: row.label.clone(),
                        principal: row.subject.clone(),
                        resource: row.object.clone(),
                        action: row.mode.clone(),
                        verdict: row.outcome.clone(),
                        epoch: row.tick,
                        reused: row.reused,
                        batch_id: row.group.clone(),
                        delegated_from: row.via.clone(),
                    })
                    .collect(),
            })
            .collect(),
    };
    let text = serde_json::to_string_pretty(&payload).map_err(|e| e.to_string())?;
    fs::write(path, text).map_err(|e| format!("write {}: {e}", path.display()))
}
