---
name: self-heal
description: Fixes small defects on its own, without stopping the task or asking the owner - failing lint/types/tests caused by the current change, simulator or emulator crashes and boot failures, stale Metro/Gradle/Pods/DerivedData caches, busy ports, flaky steps, red CI on a feature branch. Delegates mechanical fixes to the lighter fixer-lite sub-agent. Use whenever a check, build, simulator, emulator or CI run fails during an approved task.
---

# Self-heal — fix small defects without stopping the operation

Why: an owner who must answer "the simulator crashed, may I restart it?" ten times a session stops trusting the agent. Small, reversible, in-scope defects are part of the job. Detail: `docs/agents/standard/TRACK.md` (envelope), `SAFEGUARDS.md` (stop conditions).

## 1. Classify in one line (before touching anything)
| Class | Examples | Action |
|---|---|---|
| **Heal** (act, report later) | lint/type/format error; test broken by *this* change; simulator/emulator won't boot, crashes, hangs; Metro/Gradle/Pods/DerivedData/Expo cache; port in use; dev server stale; flaky step (first time); CI red on the feature branch for one of these | fix now, no question |
| **Stop** (report, ask) | needs a secret, production, a migration, a release, the default branch or a force-push; would skip/disable/weaken a test; outside the approved scope; same root cause failed twice; data loss risk | stop condition: contain, report, ask |

Not sure? It is **Stop**.

## 2. Heal loop (max 2 attempts per root cause)
1. Capture the evidence: exact command, exit code, the **first** failing lines (not the whole log).
2. Smallest fix that removes the cause. Environment playbook: [playbook.md](playbook.md).
3. Re-run the same command. Green → run the canonical project checks once more (a heal must not break a neighbour).
4. Second failure on the same cause → switch to skill `systematic-debug`; still red → Stop.
5. Log it: one line in the final reply under **Self-healed** (`what failed → cause → fix → evidence`). Repeated heals of the same class → rework ledger.

## 3. Delegate to the lighter model (Claude Code)
Mechanical heals (cache resets, simulator reboots, lint/format, a test broken by a rename) go to the `fixer-lite` sub-agent (`model: haiku`), so the main agent keeps the plan and its context:
```
Agent(subagent_type="fixer-lite", prompt="Command: <cmd>\nFailure: <first failing lines>\nScope (files you may touch): <paths>\nAcceptance: <cmd> exits 0 and <project check> stays green")
```
Run it in the background when the main task can continue meanwhile. Read the **diff** it made, not its summary. It returns `HEALED`, `NOT HEALED` or `STOP` — never trust `HEALED` without re-running the command yourself.
Tools without sub-agents: apply the same loop yourself.

## 4. Never as a heal
Skip, `.only`, `xit`, `@Ignore`, lowered thresholds, deleted assertions, `--no-verify`, `|| true`, catching and swallowing the error, pinning a dependency to an untested version, touching `.env`/secrets, force-push, edits outside the approved scope. Each of these is a FAIL that must be reported.
