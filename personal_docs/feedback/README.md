# Task feedback archives

Each task gets its own subdirectory. Every platform feedback fetch creates a **new** `revision_N/` folder; do not overwrite prior snapshots.

Workflow prompt: [`../feedback.md`](../feedback.md)

## Current archive map

| Task archive folder | Revisions |
| --- | --- |
| `adaptive-mesh-conservation/` | `revision_1/` |
| `allocator-free-list-drift/` | `revision_1/`, `revision_2/` |
| `async-executor-liveness/` | `revision_1/` |
| `fog-state-resume/` | `revision_1/`, `revision_2/` |
| `incremental-index-invalidation/` | `revision_1/` |
| `module-hot-reload-epoch/` | `revision_1/` (old name for `module-state-propagation-epoch`) |
| `policy-revocation-shadow/` | `revision_1/` |
| `quantized-beam-alignment/` | `revision_1/`, `revision_2/`, `revision_3/` |
| `sparse-block-preconditioner/` | `revision_1/`, `revision_2/`, `revision_3/` |
| `staged-snapshot-drift/` | `revision_1/`, `revision_2/` |

See [`../STATUS.md`](../STATUS.md) for current platform state and which archives correspond to active NEEDS_REVISION rows.
