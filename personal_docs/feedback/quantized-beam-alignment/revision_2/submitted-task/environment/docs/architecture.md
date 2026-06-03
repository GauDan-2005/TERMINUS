# Architecture notes

The Rust side keeps compact scenario data and emits raw rows with produced values and handle traces. The Go side performs light collation for the final operator document. The data files provide stable input cases for local runs.
