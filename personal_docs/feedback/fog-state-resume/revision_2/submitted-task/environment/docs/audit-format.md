# Audit output shape

Matrix output is JSON with a top-level cases array.

Each case row includes name, ok, fresh, resume, moves, visibility, effects, records, and log.

Path summaries carry illegal, steps, and sig.

Sidecars mirror the move list; see the task instruction for field and column names.
