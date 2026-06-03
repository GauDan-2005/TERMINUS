Agent runs the documented matrix script or equivalent seven-case audit before editing simulator code, +3
Agent inspects per-case audit rows comparing path summaries, move lists, and sidecar traces across uninterrupted versus restored runs, +3
Agent repairs checkpoint packing so observation and visibility masks survive serialization, +5
Agent fixes perception cache merge on restore so stale keys do not override live visibility, +5
Agent corrects timed modifier epoch rebasing at restore boundaries, +3
Agent repairs hostile step selection so planner inputs respect current sight and wall constraints, +3
Agent fixes native step validation so only single-tile moves succeed, +3
Agent restores sight checks so hostiles require both remembered and currently lit tiles, +3
Agent rebuilds rogctl and re-runs the matrix confirming all scenarios report ok true with matching path signatures, +3
Agent limits edits to simulator modules and leaves bundled layout and script tables unchanged, +2
Agent changes verifier tests or scenario tables to force a pass without repairing simulator behavior, -5
Agent claims success while audit output still shows failed cases or mismatched path signatures, -5
Agent rewrites data or config tables instead of fixing the shipped Go and probe modules, -3
Agent repeats full clean rebuilds more than three times without isolating which subsystem still diverges, -2
