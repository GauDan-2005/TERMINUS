# async-executor-liveness — rubric

**Status:** UNCHANGED in revision_1. This is the rubric exactly as submitted (submission
`7243aade-daa1-4513-96d0-7366734d930d`). The reviewer reported the *"rubric panel is fully
green,"* and the revision_1 fix is instruction-only (the root-`parent` sentinel sentence), so
**no rubric edit was made or required**. Recorded here because the local doc was previously empty.

**Provenance:** extracted verbatim from the submission metadata
(`personal_docs/feedback/async-executor-liveness/revision_1/metadata/submission_7243aade.json`
→ `task_documents[0].submission_document.test_rubrics`).

**Weights:** 9 positive criteria (+3 each) = **+27 positives** (within the required 10–40 cap);
4 negative criteria (−5, −3, −3, −2 = −13). The positives-only total governs the 10–40 cap.

## Positive criteria (sum = +27)

```
Agent inspects the Rust data-flow across parser, host state, gate, ordering, emission, and driver modules before editing, +3
Agent diagnoses that clean audit output depends on child ancestry metadata, branch removal, bounded lane draining, duplicate suppression, and aligned output surfaces together, +3
Agent updates the state-transfer path so child parent and depth information is preserved for accepted work, +3
Agent updates cancellation filtering so removed branches and their descendants stay out of accepted traces, +3
Agent updates bounded ordering so overflow work is delayed by lane capacity rather than dropped or reordered, +3
Agent suppresses duplicate logical child rows in the accepted trace, +3
Agent schedules child rows by arrival turn without requiring the named parent to be accepted first, +3
Agent keeps JSON, JSONL ledger, and text journal outputs aligned in identical record order, +3
Agent rebuilds the release binary and verifies both matrix and direct-case commands from /app, +3
```

## Negative criteria (sum = −13)

```
Agent hardcodes shipped case names, trace rows, or expected output files instead of deriving results from current inputs, -5
Agent weakens or edits verifier files, plan inputs, or scripts under /tests to make failures pass, -3
Agent fixes only the top-level JSON while leaving ledger or journal divergence unresolved, -3
Agent introduces nondeterministic ordering, timing-dependent behavior, or runtime network dependency, -2
```
