---
name: e2e-flow
description: The one flow for builds, E2E and Maestro runs (local or CI) - repository preflight first, every requirement stated up front in one block, build once, smoke before suite, read the failure artifacts before any re-run, classify the cause, heal within budget, codify the fix so it never comes back, and never report an empty result. Use before any app build, simulator/emulator run, Maestro or Playwright E2E, test dispatch in CI, or when tests keep failing.
---

# E2E flow — no wasted runs, no empty answers, no eternal fixes

Why: most failed device runs fail for reasons the repository already showed (wrong appId, a selector that does not exist, a missing sub-flow, a stale lockfile, an unpushed commit, a secret nobody set), and each blind re-run costs 10–30 minutes. Detail: [maestro.md](maestro.md); CI layout: skill `ci-device-lab`; failures: skill `self-heal`.

## The flow (in order; a step may be N/A only with a reason)
1. **Repo state.** `python3 .claude/agent-kit/repo_state.py` — right branch, nothing unpushed (CI tests the pushed commit), not behind the default branch, no conflicts, the PR/merge the run depends on really exists.
2. **Preflight.** `python3 .claude/agent-kit/e2e_preflight.py [--flows DIR]`. Every **FAIL** is fixed before any build or device run (self-heal when in scope). WARNs are read and either fixed or named in the report.
3. **Requirements, all at once.** Before the first run, one block listing everything the run needs and its source: device/simulator + OS · build type (debug / dev-client / release) and which commit · test account · env vars and secrets (names only, from preflight NEEDS) · backend/environment URL · seed data · which flows. Anything only the owner can give → **one** AskUserQuestion with all of it; never drip-feed questions run after run.
4. **Build once.** One build per commit; reuse it for every flow. Record the commit, build id or artifact name. A native change needs a new build; a JS-only change does not.
5. **Smoke first.** Run the smoke flow alone. Red → stop and diagnose; never launch the full suite on a broken launch.
6. **Full suite**, once, with junit output and artifacts (`maestro test … --format junit --output report.xml --test-output-dir artifacts`).
7. **Read before re-running.** For every failure open the screenshot, the view hierarchy and the log lines around it. Re-running without reading is forbidden; one re-run is allowed only for a classified infra flake.
8. **Classify** each failure: `selector` (id/text changed) · `timing` (waited too little) · `state` (leftover login/data) · `data` (account/seed missing) · `env` (device, network, secret) · `app bug` (real defect). The class decides the fix: test fix for the first four, environment fix for env, code fix (with a test) for app bug.
9. **Heal within budget** (skill `self-heal`): 2 attempts per root cause, then Stop with evidence. Never weaken a flow: no deleted assertions, no `optional: true` on what the acceptance needs, no longer sleeps instead of waits.
10. **Codify the fix** so it never returns: add the `testID` to the component instead of matching text, add the wait to the flow, add the cause to the project's rework ledger (and to `docs/agents/E2E-NOTES.md` if the project keeps one). A fix that lives only in the chat will be "fixed" again next week.
11. **Report** — never an empty result. Per flow: PASS / FAIL (class + first failing step + screenshot path) / BLOCKED (cause) / NOT RUN (why). The run produced no report, no flows, or no output? That is **BLOCKED**, with the log tail and the next step; never "it ran".

## Rules
- Local first when possible: one failing flow with `maestro test path/flow.yaml` beats a 20-minute CI round-trip.
- One run per platform in flight. Dispatching CI that builds or publishes stays behind the approval gate.
- Real builds/store uploads only on the owner's order for that execution (AGENTS.md §1).
- Logs and screenshots of public repos are public: synthetic accounts and data only; encrypt or scrub evidence (`ci-device-lab`).
