use std::env;
use std::path::PathBuf;

fn main() {
    let out = env::args().nth(1).map(PathBuf::from).unwrap_or_else(|| PathBuf::from("/app/output/window-audit.json"));
    if let Err(err) = late_window_lab::k1::run::write_all(&out) {
        eprintln!("run failed: {err}");
        std::process::exit(1);
    }
}
