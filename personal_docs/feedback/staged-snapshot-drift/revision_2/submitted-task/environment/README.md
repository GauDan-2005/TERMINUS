# Local snapshot utility

This repository contains a small tree capture and materialization harness used by the operations team to compare restored data against generated source trees. The shell driver creates isolated workspaces under `/tmp`, runs each profile, and writes a JSON audit under `/app/output`.

The Go packages model the service state and record stream. The native probe records filesystem observations for diagnostics. The shell scripts bind the pieces together for local checks.
