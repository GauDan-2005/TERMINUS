use crate::f5::types::View;

pub fn same_view(left: &View, right: &View) -> bool {
    left.totals == right.totals && left.corrections == right.corrections
}
