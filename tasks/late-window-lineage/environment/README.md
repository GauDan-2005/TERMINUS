# Local event audit lab

This repository contains a small Rust program that reads case files from `data/cases` and writes a JSON audit under `output`. The program compares uninterrupted processing with a restart-shaped path. The code is split into small modules because operators often inspect one layer at a time when a case report changes.

The shell wrapper in `scripts/run-matrix.sh` builds the binary and writes the audit file used by local checks.
