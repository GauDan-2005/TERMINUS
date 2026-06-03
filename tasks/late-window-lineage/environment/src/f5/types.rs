use std::collections::BTreeSet;

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct R0 {
    pub origin: String,
    pub seq: u64,
    pub part: String,
    pub bucket: i64,
    pub name: String,
    pub delta: i64,
    pub token: String,
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct R1 {
    pub origin: String,
    pub part: String,
    pub bucket: i64,
    pub name: String,
    pub value: i64,
    pub stamp: u64,
    pub line: Vec<String>,
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct R2 {
    pub origin: String,
    pub part: String,
    pub bucket: i64,
    pub name: String,
    pub value: i64,
    pub id: String,
    pub line: Vec<String>,
}

#[derive(Clone, Debug)]
pub struct S0 {
    pub origin: String,
    pub seen: BTreeSet<String>,
}

#[derive(Clone, Debug)]
pub struct S1 {
    pub prior: Vec<R1>,
}

#[derive(Clone, Debug)]
pub struct S2 {
    pub seen: BTreeSet<String>,
}

#[derive(Clone, Debug)]
pub struct S3 {
    pub rows: Vec<R1>,
    pub seen: BTreeSet<String>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct View {
    pub totals: Vec<R2>,
    pub corrections: Vec<R2>,
}

#[derive(Clone, Debug)]
pub struct CaseReport {
    pub name: String,
    pub ok: bool,
    pub direct: View,
    pub replay: View,
    pub repeat: bool,
}
