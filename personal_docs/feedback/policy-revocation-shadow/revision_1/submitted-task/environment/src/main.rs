use pollab::runner::run_all;
use std::env;
use std::path::PathBuf;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        eprintln!("usage: pollab <out.json> <trace>...");
        std::process::exit(2);
    }
    let out = PathBuf::from(&args[1]);
    let traces: Vec<PathBuf> = args[2..].iter().map(PathBuf::from).collect();
    if let Err(err) = run_all(&out, &traces) {
        eprintln!("{err}");
        std::process::exit(1);
    }
}
