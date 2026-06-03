use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        eprintln!("usage: mhre_native <rev> <primary> <carry>");
        std::process::exit(2);
    }
    let rev = &args[1];
    let primary: i64 = args[2].parse().expect("primary number");
    let carry: i64 = args[3].parse().expect("carry number");
    println!("{}", mhre_native::r_d(rev, primary, carry));
}
