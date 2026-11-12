# Changelog

## 1.10.0 — 2026-11-12
- **`replica-*` pack (11 skills)** from Jakeschincariol/replica-skill (MIT): recon → architect → design → build → backend → test → diff → entrepreneur → brand → launch → deploy, with their stdlib-only Python tools (kept side by side: they call each other by sibling path). Clean-room limits travel with them.
- **`reverse-engineer-anything`** from morluto/rea (MIT): the agent skill and its references plus `DISCLAIMER.md`; the REA MCP server is not bundled (`npx rea-agents setup`). Notice line states: authorized analysis only, approval gate applies.
- `tools/sync_upstream_skills.py` now takes `replica` / `rea` sources; all imports carry `LICENSE.txt` and the precedence notice. Both packs are `full`-profile only and skipped for `--public-ci` repos. `00-MAP` gets rows for them; tests check licence, notice, disclaimer and tool syntax.
- 50 skills in total.

## 1.9.0 — 2026-11-12
- **Mandatory track** (`standard/TRACK.md`): Boot → Brief → Plan → Owner "yes" → Build → Self-heal → Verify → Push + watch CI → Close, each stage naming the skill to load. Why: agents treated the rules as optional reading and skipped most of them.
  - `SessionStart` hook prints the track on startup, resume and after every compaction.
  - `intent-brief` names the skills to load for the detected mode (only those installed).
  - New `Stop` hook `track-gate.sh`: a turn that changed files (Edit/Write/commit) and ends without evidence states is sent back once to verify, self-heal and report. Honours `stop_hook_active`, ignores sub-agent lines, logs counts only, fails open; `AGENT_KIT_TRACK_GATE=0` disables.
  - `templates/CLAUDE.md` is now an operating contract (MUST list); `templates/AGENTS.md` gets §0b (track) and the self-heal pre-approval in §1. The installer prints a `hint` when an existing `AGENTS.md`/`CLAUDE.md` predates the track.
- **Self-heal** skill + playbook: small, reversible, in-scope defects (lint/type/tests broken by the change, simulator/emulator boot or crash, caches, busy ports, flaky steps, red CI on the feature branch) are fixed without stopping or asking; 2 attempts per cause; never by weakening tests. `SAFEGUARDS`, `MODES`, `WORKFLOW`, `systematic-debug` aligned.
- **CI monitor** skill + `ci_watch.py` (read-only `gh` poller: green / defect / infra re-run candidate / no runs / no gh).
- **Light-model sub-agents** in `agents/` (plugin) and `.claude/agents/` (vendored): `fixer-lite` and `ci-watcher`, both `model: haiku`.
- **17 skills imported from addyosmani/agent-skills (MIT)** via `tools/sync_upstream_skills.py`: spec, planning, incremental implementation, TDD, code review, simplification, git workflow, CI/CD, API design, frontend UI, browser testing, observability, shipping, deprecation, ADRs, source-driven and doubt-driven development. Each carries `LICENSE.txt`, a precedence notice (AGENTS.md wins) and its checklists inside the skill folder; overlapping upstream skills map to the kit's own.
- Profiles: `lite` 13, `standard` 27, `full` 38 skills.
- Repository: banner and social-preview image, README rewrite (enforcement table, FAQ, keywords), plugin keywords, `SECURITY.md`, bug/feature issue templates.
- Tests: track banner, required skills, Stop gate (block, evidence, no edits, commit, no loop, opt-out, fail open, no text echo), sub-agents installed on the light model, `ci_watch.py` with a fake `gh`, imported-skill licence/notice/links.

## 1.8.0 — 2026-11-09
- `media-investigation` skill: when the owner attaches media, the agent reads all of it (video via `scripts/frames.py` + ffmpeg: frame grid, timestamps), answers the question, then reports extra findings in a separate block (SEEN vs INFERRED, severity, evidence, max 7), read-only until approved; privacy and budget limits. Media the owner attached but did not mention is analyzed anyway and cited explicitly.
- `triage` skill: several asks at once become a prioritized list (risk first, quick wins batched by area, large items get 2–3 spec/plan options, parked items with their blocking question).
- `intent-brief` hook: hints `media-investigation` when images/videos are attached (`[Image #N]` or media paths) and `triage` when the message lists 3+ items; counts only, never echoes text.
- Both skills are in the `lite` and `standard` profiles.
- From the owner's git history (rework hotspots, translation churn, reverts of stray files, device QA rounds):
  - `hotspots.py`: files with many fix commits (translations excluded as noise); a hotspot gets a regression test before another patch. Wired into `session-preflight` and `triage`.
  - `i18n_parity.py`: missing/extra translation keys across JSON locales (exit 1, never prints values). Wired into `ux-check` and `session-preflight`.
  - `triage` QA-round mode: stable IDs `R<round>.<n>`, retest and occurrence counters, second occurrence → `systematic-debug`, fixes grouped by shared cause.
  - `pr-gate` PreToolUse hook: runs the repo's PR checker on the body before an agent opens/edits a PR (GitHub MCP or `gh pr create/edit --body-file`); hard failures block, warnings pass, no checker → allow. `--pr-quality local` is now enforced, not advisory.
  - `CANARY.md`: choose a word that appears nowhere in the repos; the agent may check once and suggest another.
  - `hotspots.py` warns on shallow clones (cloud sessions) instead of under-counting silently.
  - Tests: README must list every skill; lite count follows `profiles.json`.
  - `pr_quality.py`: new "Generated / synced files" area (native sync output, Pods, build output, Xcode user state).

## 1.7.1 — 2026-11-08
- Tests: the tamper check now flips a bit instead of writing a fixed byte (it missed the tamper ~1 in 256 runs, which is what failed CI the second time); background-logging checks wait for the event instead of a fixed `sleep 1`.
- Fix: the kit's CI failed because the `actionlint` container ships `shellcheck` and flagged the shell inside the templates (my local run had no shellcheck). `ls | head` / unquoted globs / unquoted `$KID` in the iOS templates now use `find` and quotes; the CI guard loop no longer uses `ls | grep`. `actionlint` + `shellcheck` is clean on every template. CONTRIBUTING: run actionlint with shellcheck installed.

## 1.5.0 — 2026-11-08
- **Measure:** `metrics.py` logs counts only (sessions, prompts and likely mode, compactions, peak context, baton offers) to `~/.local/state/agent-kit/` — never prompt text; `metrics.py report` adds a git rework signal (files with ≥ 3 fix commits). `AGENT_KIT_METRICS=0` disables.
- **Hook integrity:** `verify.py` compares kit files with the install manifest; the SessionStart hook warns when hooks changed; optional `--with-guard` CI workflow fails PRs that change hooks outside the installer and checks hooks stay offline; CODEOWNERS hint.
- **Single source of truth:** `.claude/agent-kit/overrides` (`NAME.md=path`) marks a generic standard doc as overridden by the project's own, with a banner.
- **Kit CI:** `tests/run.sh` (syntax, JSON/YAML, frontmatter, versions, installer idempotency/overrides/guard, hooks, metrics privacy, verify, encryption, personal-data guard) + `ci` workflow with actionlint.
- Fixes: installer now ships `.py` assets; SessionStart hook resolves its folder before changing directory.

## 1.4.0 — 2026-11-08
- `intent-compiler` skill: the owner's plain message is compiled, invisibly, into a brief (goal, repo context, acceptance, constraints, mode, skills, ≤ 1 question) before acting; rubric with examples.
- `intent-brief` UserPromptSubmit hook: one-line reminder with a likely mode; silent for approvals, short acks and slash commands; never echoes the owner's text.
- Installer merges each hook command individually (a new hook on an existing event is no longer skipped).

## 1.3.0 — 2026-11-08
- `session-guide` skill + `standard/CONVERSATION.md`: the agent leads sessions from plain talk (briefing, goal + acceptance restatement, one question at a time, agenda, parking lot).
- `baton-pass` skill: self-contained continuation prompt for any IDE/model/platform; never includes secrets or the canary.
- Statusline now shows weekly/5-hour plan usage and caches it; new `UserPromptSubmit` hook `usage-guard` asks the agent to offer a baton at weekly ≥ 85 % (5-hour ≥ 90 %), once per level per session (`AGENT_KIT_BATON_PCT` to tune).

## 1.2.0 — 2026-11-08
- New skill `ci-device-lab`: GitHub Actions device lab for people without a Mac or spare devices — Android APK (Expo prebuild, React Native, Capacitor, native), iOS simulator build, Maestro E2E on emulator and simulator, Expo OTA, EAS build (cloud or `--local`), TestFlight without EAS; private-source + public-CI layout, read-only checkout script, AES-256-GCM artifact encryption, secret list by name, hardening checklist, owner-order guards on real builds.

## 1.1.0 — 2026-11-08
- Packaged as a Claude Code plugin + marketplace (`.claude-plugin/`), skills under `skills/`, plugin hooks in `hooks/hooks.json`.
- Security & performance skills: `security-core`, `identity-session`, `data-privacy`, `supply-chain`, `performance-core`, `platform-security`.
- Compaction: `autoCompactWindow` 200k (+ `CLAUDE_CODE_AUTO_COMPACT_WINDOW` fallback) replaces the percentage override; statusline shows context use and asks for a handoff from 70 %.
- Canary: form of address given by the owner at the start of each session; preserved through compaction; never stored.
- Installer rewritten in Python: hash manifest for safe re-installs, settings merge, `--no-vendor`, `--dry-run`.
- Removed all project-specific references.

## 1.0.0 — 2026-11-08
- Initial standard: AGENTS.md template, standard docs, caveman output style, SessionStart/PreCompact hooks, six workflow skills.
