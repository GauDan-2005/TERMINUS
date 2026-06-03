# Local runtime architecture

This repository contains a small deterministic workload runner used for local audit exercises. Plan files under `data/cases` describe rows that are loaded into a local state graph, grouped by lane, and written to generated report surfaces under `/app/output`.

The source tree is split into short module roots. Each root owns one part of the local runtime: parsing, state transfer, ordering, row filtering, and line-oriented output. The split mirrors the production service that inspired this exercise, where generated JSON and append-only side files were checked by separate monitoring jobs.
