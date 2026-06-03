# Reviewer appendix — allocator-free-list-drift

## Concept check

Single-container C debugging task. Symptom: heap stress audit diverges under split/coalesce/realloc scripts while short sequences may appear fine. Fix is distributed across boundary tags, free-list splice, relocation copy, and accounting.

## Residual risks

- If bugs are too obvious in one file, collapse on discoverability — verify opaque names and no correctional comments.
- If Python model drifts from C semantics, oracle/NOP integrity breaks — keep model aligned with headers.

## Empirical hardness

Target ≤1/6 frontier passes after oracle 10/10. If 100% pass, deepen cross-case coupling without instruction cause disclosure.
