# TRACK — The mandatory work track

Why: agents skip rules they only "read about". The track is short, numbered and checked by hooks, so skipping a stage is visible (and, in Claude Code, blocked at the end of the turn). Every task walks it; a trivial task walks it in one line.

| # | Stage | Do | Required skill(s) | Exit criterion |
|---|---|---|---|---|
| 0 | **Boot** | Read `AGENTS.md` + handoff; `git fetch`; check branch/PR | `session-guide` | You can state where things stopped |
| 1 | **Brief** | Compile the owner message (goal, acceptance, constraints, mode) | `intent-compiler` (+ `triage` for lists, `media-investigation` for media) | Goal + acceptance in one line |
| 2 | **Plan** | Surface, risks, tests designed first (QUALITY-G1) | `session-preflight`; feature: `spec-driven-development`, `planning-and-task-breakdown`; bug: `systematic-debug` | Plan shown to the owner |
| 3 | **Approve** | Wait for an explicit "yes"; record it in the handoff | — | Approval recorded (date + what) |
| 4 | **Build** | Thin slices, test first, canonical checks after each slice | `incremental-implementation`, `test-driven-development` | Slice green |
| 5 | **Self-heal** | Small defects inside the approved scope are fixed **without stopping or asking** (lighter model when available) | `self-heal` | Green, or a stop condition reported |
| 6 | **Verify** | Self-review the diff; real checks; QUALITY-G2 states | `code-review-and-quality`, `pr-quality` | Every gate PASS / FAIL / BLOCKED / NOT RUN / N/A + evidence |
| 7 | **Ship & watch** | Push the feature branch; watch CI in the background (lighter model); self-heal red runs | `ci-monitor`, `git-workflow-and-versioning` | CI green, or FAIL with cause and next step |
| 8 | **Close** | Reply (caveman), AUTOMATED vs PHYSICAL test list, replace the handoff | `handoff` | Handoff replaced |

## Rules
1. **No stage is optional.** N/A is allowed with a reason ("Plan: N/A — one-line typo fix, approved in the message").
2. **Order matters.** No edit before stage 3, except inside the self-heal envelope of an already-approved task.
3. **A turn that changed files ends with evidence states.** In Claude Code the `track-gate` Stop hook sends the agent back once if the final reply has none.
4. **Skills are invoked, not remembered.** When a stage names a skill, load it (Claude Code: the `Skill` tool) before doing the stage. A skill not installed in this profile: do the stage from this table and say so in one line.
5. **Precedence.** `AGENTS.md` > this track > any skill (including imported ones). If a skill says "commit", "deploy" or "ask the user", the approval gate and self-heal envelope here still decide.

## Self-heal envelope (stage 5 and 7) — act, do not ask
Inside an approved task, fix on your own and report afterwards:
- lint, type, format, unit/E2E failures caused by the current change;
- simulator/emulator that will not boot, crashes, hangs or lost state; Metro/Gradle/Pods/DerivedData caches; port in use; stale dev server;
- flaky step on a feature branch: re-run once, then treat as a defect;
- CI red on the feature branch for one of the reasons above.

Budget: **2 attempts per root cause**, then stop and report (`systematic-debug` rule). Never: skip, disable or weaken a test; widen scope; touch secrets, production, migrations, releases or the default branch; force-push. Those are stop conditions (`SAFEGUARDS.md`).

## Lighter model (Claude Code)
Mechanical work goes to cheaper sub-agents shipped by the kit: `fixer-lite` (self-heal) and `ci-watcher` (CI monitoring), both on `model: haiku`. The main agent keeps the plan and reviews their diff, never their summary. Other tools: do the same steps yourself.
