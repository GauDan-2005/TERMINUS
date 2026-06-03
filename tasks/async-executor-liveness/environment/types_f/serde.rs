use crate::types_f::{CaseReport, Record};

fn esc(s: &str) -> String {
    s.replace('\\', "\\\\").replace('"', "\\\"")
}

pub fn row_json(row: &Record) -> String {
    format!(
        "{{\"case\":\"{}\",\"task\":\"{}\",\"parent\":\"{}\",\"depth\":{},\"lane\":\"{}\",\"turn\":{}}}",
        esc(&row.case_name),
        esc(&row.task_name),
        esc(&row.parent_name),
        row.depth,
        esc(&row.lane_name),
        row.turn
    )
}

fn string_array(items: &[String]) -> String {
    format!(
        "[{}]",
        items
            .iter()
            .map(|s| format!("\"{}\"", esc(s)))
            .collect::<Vec<_>>()
            .join(",")
    )
}

pub fn case_json(case: &CaseReport) -> String {
    let trace = case.trace.iter().map(row_json).collect::<Vec<_>>().join(",");
    format!(
        "{{\"name\":\"{}\",\"ok\":{},\"finished\":{},\"pending\":{},\"trace\":[{}],\"ledger\":\"{}\",\"journal\":\"{}\"}}",
        esc(&case.name),
        if case.ok { "true" } else { "false" },
        if case.finished { "true" } else { "false" },
        string_array(&case.pending),
        trace,
        esc(&case.ledger),
        esc(&case.journal)
    )
}

pub fn report_json(cases: &[CaseReport]) -> String {
    let body = cases.iter().map(case_json).collect::<Vec<_>>().join(",");
    format!("{{\"cases\":[{}]}}\n", body)
}
