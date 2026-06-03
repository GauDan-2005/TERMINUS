use std::env;
use std::path::PathBuf;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.len() < 2 {
        eprintln!("usage: idxlab <report> <trace> [trace ...]");
        std::process::exit(2);
    }
    let out = PathBuf::from(&args[0]);
    let traces: Vec<PathBuf> = args[1..].iter().map(PathBuf::from).collect();
    if let Err(err) = idxlab::runner::run_all(&out, &traces) {
        eprintln!("{err}");
        std::process::exit(1);
    }
}
