Difficulty Guidelines
Task difficulty is determined by accuracy when run against frontier AI models. This guide helps you design tasks at the right difficulty level.

Difficulty Levels
Difficulty is calculated from accuracy across two evaluation models. The threshold that applies depends on the tier:

Hard	Accuracy ≤ 20% on the best model, OR accuracy ≤ 20% on the worst model	Requires deep expertise, multi-step reasoning, or niche knowledge
Medium	20% < accuracy ≤ 60% on the worst model	Moderate complexity, some domain knowledge
Easy	60% < accuracy ≤ 80% on the worst model	Straightforward but still non-trivial
Important: Tasks where the worst model scores above 80% will not be accepted — they're too easy to be useful as training signal.

Why "best" vs "worst" model?
Both models are run against every task. The worst model sets the difficulty floor for most tasks: if even the weaker model can solve it most of the time, the task is Easy. The best model matters for the hardest tasks: a task where the strongest model still only scores ≤ 20% earns Hard difficulty even if the worst model also struggles, because the failure isn't just a weak-model artifact.

Evaluation Process
Each task is evaluated against:

GPT-5.5 with Codex agent
Claude Opus 4.8 with Claude Code agent
5 runs each to determine average accuracy
Designing for Difficulty
For Hard Tasks (≤ 20% on best or worst model)
Hard tasks require one or more of:

Deep domain expertise — Knowledge LLMs haven't seen much
Complex multi-step reasoning — 10+ sequential steps
Subtle debugging — Root cause analysis required
Niche tools/languages — Less common technologies
Techniques:

Use bespoke rules buried in common patterns
Require understanding of obscure documentation
Create debugging tasks where the root cause isn't obvious
Use domain-specific knowledge (blockchains, scientific computing)
For Medium Tasks (20–60% on worst model)
Medium tasks typically involve:

Moderate complexity — 5-10 steps
Some domain knowledge — Common but not trivial
Clear requirements — But non-obvious solution
Techniques:

Combine multiple familiar concepts
Add edge cases that require careful handling
Include configuration that's easy to miss
For Easy Tasks (60–80% on worst model)
Easy tasks should still be:

Non-trivial — Not one-liners
Multi-step — At least 3-5 steps
Testable — Clear success criteria
Techniques:

Standard tasks with one or two tricky aspects
Well-known problems with specific constraints
Setup tasks with multiple requirements
Common Mistakes
Making Tasks Too Easy
Single-step solutions	Agents solve immediately
Obvious debugging	Pattern matching succeeds
Common tutorials	In training data
Simple API usage	Well-documented
Making Tasks Unfair
Impossible requirements	No one can solve
Ambiguous instructions	Luck determines success
Time-dependent	Results vary randomly
External dependencies	Environment issues
Testing Your Difficulty
Before submitting, verify difficulty by:

1. Run Against Oracle Agent
bash

Copy
harbor run -a oracle -p <task-folder>
This should PASS. If it doesn't, your task may have issues.

2. Run Against Real Agents
bash

Copy
# GPT-5.5
stb harbor run -m @openai/gpt-5.5 -p <task-folder>

# Claude Opus 4.8
stb harbor run -m @anthropic/claude-opus-4-8 -p <task-folder>
Run at least 2-3 times against each model to gauge pass rate, and remember that the worst model's pass rate is what determines Easy/Medium for most tasks.

Standardized runner (recommended). `scripts/agent_test.sh` wraps the harbor runs and parses the pass rate into a difficulty band, so you don't eyeball raw job output:

    eval "$(stb keys show)"; export PATH="/tmp/opencode/harbor-venv/bin:$PATH"
    ./scripts/agent_test.sh run tasks/<task> --runs 5       # runs both frontier models, writes jobs/
    ./scripts/agent_test.sh report --latest --task <task>   # pass rates + HARD/MEDIUM/EASY verdict

Target ≤1/6 frontier pass for a comfortably-hard task. Make sure the runner targets the SAME models the platform evaluates with (currently GPT-5.5 + Claude Opus 4.8); `agent_test.py`'s `MODELS` is set to these — measuring against the wrong models gives a misleading verdict.

EMPIRICAL DIFFICULTY IS THE SOURCE OF TRUTH — PROXIES ARE NOT.
The local gates `hard_difficulty_predictor.py` and `reviewer_simulation.py` only ESTIMATE difficulty from the spec text, and they routinely report PASS / high confidence on tasks that real agents solve easily. Acceptance is decided by the real-agent pass rate, never by these proxies. Do not "defer" or skip the agent run and submit on proxy signals alone — that is exactly what produced the repeated NEEDS_REVISION "EASY/TRIVIAL — requires at least MEDIUM" bounces (frontier agents passed those tasks 4–5/5). A task whose difficulty was not measured by real frontier agents is not submittable. This requires live Portkey credits; if they are exhausted (Error Code 04), refill them before submitting rather than guessing.

3. Analyze Failures
When agents fail:

Is it for a good reason (task difficulty)?
Or a bad reason (unclear instructions)?
Good failures: Agent misunderstood complexity, missed edge case Bad failures: Ambiguous requirements, environment issues

Adjusting Difficulty
To Make Harder:
Add more steps
Include hidden requirements
Use niche knowledge
Create debugging scenarios
Add edge cases
To Make Easier:
Reduce step count
Make requirements more explicit
Use common technologies
Provide more hints in instructions
Simplify the environment