# WORKFLOW — From a short owner message to a verified handoff

The stages and their required skills are fixed in `TRACK.md`; this file details them.

## 1. Intake
- Owner messages are short, like a meeting or feedback. Turn them into a **session packet** (skill `session-preflight`):
  `GOAL · ACCEPTANCE (numbers) · SURFACE · OUT OF SCOPE · MODE · GATES (N/A + reason) · EVIDENCE · DELIVERY · BUDGET`
- If GOAL or ACCEPTANCE does not fit one line, ask **one** question with 2–3 options, recommendation first. Never ask what the repo answers.
- Verify state yourself: git, PRs, plan checkboxes, live config. Status cells and handoffs age.

## 2. Plan (QUALITY-G1)
Surface map, risks, tests designed before the solution, delivery channel, rollback. See `QUALITY-GATES.md`. Present the plan and **stop** until the owner approves. Record the approval in the handoff ("approved <date>: <what>") so compaction cannot lose it.

## 3. Execute
- Small, verified steps; one root cause per round; the canonical project checks after each step.
- Parallel work only on disjoint files or isolated worktrees (`ORCHESTRATION.md`).
- A check, simulator or CI step fails inside the approved scope → skill `self-heal` (light sub-agent `fixer-lite`), no question to the owner; max 2 attempts per cause.
- No "while I was here". Useful-but-not-required → defer; future milestone → do not implement; architectural change → decision record first.

## 4. Verify (QUALITY-G2)
Self-review the diff, run the real checks, open and read screenshots, record PASS/FAIL/BLOCKED/NOT RUN/N/A with evidence. A gate that is FAIL or BLOCKED means not Done.

## 5. Deliver
- Commit: imperative mood, explain *why*. Branch/PR per the session's instructions; never merge on your own; never force-push a shared branch.
- After the push, watch CI in the background (skill `ci-monitor`, sub-agent `ci-watcher`); heal red runs on the feature branch.
- Declare the delivery channel when the project has more than one (e.g. OTA / build / server).
- Replace the handoff file (`HANDOFF-TEMPLATE.md`), update plan checkboxes, changelog if user-visible.
- Reply to the owner in caveman form, ending with the AUTOMATED vs PHYSICAL test list.

## 6. Recurrence
Same behaviour fixed before, or a fix failed: record the defect class in the project's rework ledger (`REWORK-LEDGER.md` template), name one owner module, add a guard test, and use `systematic-debug`. Two failed attempts on one item → stop and bring evidence plus a recommendation.
