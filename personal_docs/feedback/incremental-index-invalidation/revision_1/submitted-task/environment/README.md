# Local indexing harness

This repository models a small definition lookup service used by editor tooling. Trace files select fixture trees and ask for observations. The binary scans TypeScript files, records exported names, and writes a JSON report for the selected traces.

The code is intentionally small enough to run inside the verifier, but it keeps the same moving pieces as a larger workspace: normal source trees, generated files, package targets, and repeated observations over a single case timeline.
