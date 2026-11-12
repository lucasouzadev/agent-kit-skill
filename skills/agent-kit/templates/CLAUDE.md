@AGENTS.md

# Claude Code — operating contract (MUST, every session and every sub-agent)

These are not suggestions. Hooks check them; skipping one is a defect you report, not a shortcut.

1. **Walk the track** in `docs/agents/standard/TRACK.md` for every task: Boot → Brief → Plan → Owner "yes" → Build → Self-heal → Verify → Push + watch CI → Close. The `SessionStart` hook prints it; the `UserPromptSubmit` hook names the skills for the detected mode.
2. **Invoke skills, do not paraphrase them.** When the track or the hook names a skill, call the `Skill` tool before that stage. If it is not installed, say so in one line and do the stage from `TRACK.md`.
3. **Approval gate** before the first edit/commit/migration/deploy (AGENTS.md §1). The `action-guard` hook asks before risky commands; never retry around it.
4. **Self-heal without asking** inside an approved task (skill `self-heal`): lint/type/test failures from your change, simulator/emulator crashes or boot failures, caches, busy ports, flaky steps. Mechanical fixes go to the sub-agent `fixer-lite` (`model: haiku`) via `Agent(subagent_type="fixer-lite", …)`; read its diff. Max 2 attempts per cause, then stop and report.
5. **After every push, watch CI** in the background: `Agent(subagent_type="ci-watcher", run_in_background=true, …)` (skill `ci-monitor`). Keep working; act on its verdict; report `CI: <state> <url>`.
6. **Close with evidence.** A turn that changed files ends with PASS / FAIL / BLOCKED / NOT RUN / N/A per gate; the `track-gate` Stop hook sends you back once if not. Then the AUTOMATED vs PHYSICAL test list and the handoff.
7. **Sub-agents** inherit all of this (they load `CLAUDE.md` too). Brief them with paths, scope and acceptance (`docs/agents/standard/ORCHESTRATION.md`); prefer the light model for mechanical work; never trust a summary without the diff.

## Claude Code notes
- Project config in `.claude/`: output style `caveman`, hooks (session state + track, intent brief, action guard, PR gate, track gate, compaction), earlier auto-compaction, skills in `.claude/skills/`, sub-agents in `.claude/agents/`.
- Long context: write the active state to the handoff file before it fills; after `/compact` the hook re-reads it. Use `/compact <focus>` to steer a manual compaction.
- Change the light model: edit `model:` in `.claude/agents/fixer-lite.md` / `ci-watcher.md` (`haiku`, `sonnet`, or `inherit`).
