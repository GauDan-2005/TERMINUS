# allocator-free-list-drift — Step 6 empirical hardness

## Oracle baseline

- `harbor run -a oracle -k 10 -n 10`: Mean **1.000** (10/10 trials reward 1.0)
- `harbor run -a nop`: Mean **0.000**

## Frontier probes (terminus-2)

| Job                                | Model                    | Result                                      |
| ---------------------------------- | ------------------------ | ------------------------------------------- |
| `allocator-free-list-drift-gpt-1`  | `openai/gpt-5.2`         | **APIError** — Portkey usage limit exceeded |
| `allocator-free-list-drift-opus-1` | `openai/claude-opus-4-6` | **APIError** — Portkey usage limit exceeded |

Probes could not measure frontier pass rate. Task remains `difficulty = hard` by design (four independent flip points, distributed C bugs, audit contract).

## Rubric

External file: `personal_docs/rubrics/allocator-free-list-drift-rubric.txt` (27 positive, 4 negative; not shipped in zip).
