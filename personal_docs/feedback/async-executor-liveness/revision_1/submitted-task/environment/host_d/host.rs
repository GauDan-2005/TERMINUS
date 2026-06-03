use std::collections::BTreeMap;

use crate::core_a::E0;
use crate::types_f::Item;

pub struct S2 {
    pub items: BTreeMap<String, Item>,
}

pub struct R1 {
    pub item: Item,
}

pub struct R2 {
    pub item: Item,
}

impl S2 {
    pub fn new() -> Self {
        Self { items: BTreeMap::new() }
    }
}

pub fn bind_d(a: &mut S2, b: R1) -> Result<R2, E0> {
    let mut item = b.item.clone();
    if item.parent != "-" {
        item.parent = "-".to_string();
        item.depth = 0;
        item.chain = vec![item.ident.clone()];
    }
    a.items.insert(item.ident.clone(), item.clone());
    Ok(R2 { item })
}
