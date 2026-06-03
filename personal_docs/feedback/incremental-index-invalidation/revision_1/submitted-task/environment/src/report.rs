use crate::model::{CaseReport, Observation};
use std::fs;
use std::path::Path;

pub fn write_report(out: &Path, cases: &[CaseReport]) -> Result<(), String> {
    if let Some(parent) = out.parent() {
        fs::create_dir_all(parent).map_err(|e| format!("create {}: {e}", parent.display()))?;
    }
    let mut text = String::new();
    text.push_str("{\n  \"cases\": [\n");
    for (idx, case) in cases.iter().enumerate() {
        if idx > 0 {
            text.push_str(",\n");
        }
        text.push_str(&case_json(case));
    }
    text.push_str("\n  ]\n}\n");
    fs::write(out, text).map_err(|e| format!("write {}: {e}", out.display()))
}

fn case_json(case: &CaseReport) -> String {
    let mut text = String::new();
    text.push_str("    {\n");
    text.push_str(&format!("      \"name\": {},\n", quoted(&case.name)));
    text.push_str(&format!("      \"ok\": {},\n", bool_text(case.ok)));
    text.push_str("      \"observations\": [\n");
    for (idx, obs) in case.observations.iter().enumerate() {
        if idx > 0 {
            text.push_str(",\n");
        }
        text.push_str(&observation_json(obs));
    }
    text.push_str("\n      ],\n");
    text.push_str("      \"stale\": [");
    for (idx, item) in case.stale.iter().enumerate() {
        if idx > 0 {
            text.push_str(", ");
        }
        text.push_str(&quoted(item));
    }
    text.push_str("]\n");
    text.push_str("    }");
    text
}

fn observation_json(obs: &Observation) -> String {
    format!(
        "        {{\"label\": {}, \"symbol\": {}, \"found\": {}, \"path\": {}, \"source\": {}, \"line\": {}, \"epoch\": {}, \"reused\": {}, \"fresh\": {}}}",
        quoted(&obs.label),
        quoted(&obs.symbol),
        bool_text(obs.found),
        quoted(&obs.path),
        quoted(&obs.source),
        obs.line,
        obs.epoch,
        bool_text(obs.reused),
        bool_text(obs.fresh),
    )
}

fn bool_text(value: bool) -> &'static str {
    if value {
        "true"
    } else {
        "false"
    }
}

fn quoted(value: &str) -> String {
    let mut out = String::from("\"");
    for ch in value.chars() {
        match ch {
            '\\' => out.push_str("\\\\"),
            '"' => out.push_str("\\\""),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            _ => out.push(ch),
        }
    }
    out.push('"');
    out
}
