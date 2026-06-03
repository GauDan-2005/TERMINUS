use std::env;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

use executor_liveness_lab::drive_g::drive_g;
use executor_liveness_lab::read_h::read_plan;
use executor_liveness_lab::serde_f::report_json;
use executor_liveness_lab::types_f::CaseReport;

fn arg_value(args: &[String], key: &str) -> Option<String> {
    args.windows(2)
        .find(|w| w[0] == key)
        .map(|w| w[1].to_string())
}

fn plan_path(root: &Path, name: &str) -> PathBuf {
    root.join("data").join("cases").join(format!("{}.plan", name))
}

fn load_names(args: &[String]) -> Vec<String> {
    if let Some(name) = arg_value(args, "--case") {
        vec![name]
    } else {
        ["amber", "cobalt", "drake", "ember", "flint", "graphite"]
            .iter()
            .map(|s| s.to_string())
            .collect()
    }
}

fn drive_x(root: &Path, names: &[String], out: &Path, work: &Path) -> io::Result<Vec<CaseReport>> {
    let mut reports = Vec::new();
    for name in names {
        let plan = read_plan(&plan_path(root, name))?;
        reports.push(drive_g(&plan, work)?);
    }
    if let Some(parent) = out.parent() {
        fs::create_dir_all(parent)?;
    }
    fs::write(out, report_json(&reports))?;
    Ok(reports)
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let root = PathBuf::from(arg_value(&args, "--root").unwrap_or_else(|| "/app".to_string()));
    let out = PathBuf::from(arg_value(&args, "--out").unwrap_or_else(|| "/app/output/executor-audit.json".to_string()));
    let work = PathBuf::from(arg_value(&args, "--work").unwrap_or_else(|| "/app/output/runtime".to_string()));
    let names = load_names(&args);
    let _ = drive_x(&root, &names, &out, &work)?;
    Ok(())
}
