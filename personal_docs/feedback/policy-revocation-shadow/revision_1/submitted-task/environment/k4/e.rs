use crate::model::State;

pub fn mote_e(a: &State, b: &str, c: &str, d: &str) -> (String, String) {
    let mut current = b.to_string();
    loop {
        if a.direct.contains(&(current.clone(), c.to_string(), d.to_string())) {
            if a.blocked.contains(b) {
                return ("deny".to_string(), String::new());
            }
            let via = if current == b {
                String::new()
            } else {
                current.clone()
            };
            return ("allow".to_string(), via);
        }
        match a.chain.get(&current) {
            Some(parent) => current = parent.clone(),
            None => return ("deny".to_string(), String::new()),
        }
    }
}
