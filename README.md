# Agent Kit

A portable documentation and workflow standard for AI coding agents (Claude Code, Codex, Cursor and any tool that reads `AGENTS.md`), packaged as a Claude Code plugin and as plain Agent Skills.

It was distilled from several production repositories (web + BaaS, React Native, native iOS/Android, public CI) where agents worked daily, and generalized so it fits any project.

## Why
- **Boot cost.** Agent docs grow until every session pays tens of thousands of tokens before work starts, and pays again after every compaction.
- **Rework.** The same bug "fixed" five times, "done" without evidence, plans lost to compaction.
- **Noise.** Long replies the owner has to read.

## What you get
- **Short core, modules on demand.** `AGENTS.md` (≤ 120 lines) is the only always-loaded file; the rest is a doc or a skill opened by task.
- **Meeting-style sessions.** The owner starts with a short message; the agent boots from `AGENTS.md` + the handoff and picks its mode. No kickoff prompt.
- **Terse output.** `caveman` output style: ≤ 15 lines, result first, nothing important dropped.
- **Early, lossless compaction.** Compaction at 200k tokens instead of near a 1M window; a `PreCompact` hook tells the summary to keep the active state; a `SessionStart` hook re-injects branch, commits and handoff after compaction; a statusline shows context use.
- **Evidence over claims.** PASS / FAIL / BLOCKED / NOT RUN / N/A; merged ≠ deployed ≠ verified; human approval gate before writes.
- **Device lab in CI.** No Mac or spare phones? Workflow templates build and test on hosted emulators/simulators, package APK/TestFlight builds, publish Expo OTA and run Maestro — with a safe secret list and public-repo hardening.
- **Security & performance skills** anchored on OWASP Top 10:2025, ASVS 5.0, MASVS v2.1, NIST SP 800-63-4, SSDF, SLSA, Core Web Vitals, Android vitals and Apple hang metrics.

## Install

### As a Claude Code plugin (skills, output style and hooks for every project)
```
/plugin install agent-kit --marketplace lucasouzadev/agent-kit-skill
```
or `/plugin marketplace add lucasouzadev/agent-kit-skill` then `/plugin install agent-kit@agent-kit`.
Then, inside a repository, ask: *"set up agent-kit in this repo"* — the `agent-kit` skill surveys the repo, proposes a plan and runs the installer with `--no-vendor`.

### Vendored into a repository (works where plugins are not installed: cloud sessions, teammates, other tools)
```bash
git clone https://github.com/lucasouzadev/agent-kit-skill
python3 agent-kit-skill/skills/agent-kit/scripts/install.py /path/to/repo --dry-run
python3 agent-kit-skill/skills/agent-kit/scripts/install.py /path/to/repo          # add --public-ci for public CI repos
grep -rn '{{' /path/to/repo/AGENTS.md                                               # fill placeholders
```
Use **either** the plugin hooks or the vendored hooks in a given repo, not both. Re-running the installer updates only files it wrote and you did not edit (hash manifest); everything else is reported as `SKIP`.

## Contents
| Path | Role |
|---|---|
| `skills/agent-kit/` | setup skill: `templates/`, `standard/` docs, `assets/claude/` (settings, hooks, statusline), `scripts/install.py` |
| `skills/caveman` | terse output |
| `skills/session-preflight` | session packet before acting |
| `skills/systematic-debug` | four-step root cause, two-attempt stop |
| `skills/fundamentals-audit` | race, idempotency, client trust, separation, integration tests |
| `skills/ux-check` | UX laws, states, a11y, responsiveness, UI performance |
| `skills/handoff` | session state file |
| `skills/security-core` · `identity-session` · `data-privacy` · `supply-chain` | security modules |
| `skills/performance-core` · `platform-security` | performance and per-platform (native, web, hybrid WebView, desktop web runtime) |
| `skills/ci-device-lab` | device lab in GitHub Actions: Android emulator, iOS simulator, APK/TestFlight builds, Expo OTA and EAS (cloud or local), Maestro E2E, private-source + public-CI pattern, secret list and hardening |
| `output-styles/caveman.md` | terse output style |
| `hooks/hooks.json` | plugin hooks (SessionStart, PreCompact) |

### `standard/` docs
`00-MAP` · `MODES` (Fixer, Builder, Product, Architect, Lens, Auditor) · `WORKFLOW` · `QUALITY-GATES` (G1/G2) · `DONE` · `SAFEGUARDS` · `TASK-CONTRACT` · `HANDOFF-TEMPLATE` · `REWORK-LEDGER` · `OWNER-DECISIONS-TEMPLATE` · `ORCHESTRATION` · `THREAT-MODEL` · `CHANGELOG-GUIDE` · `CONTEXT-BUDGET` · `CANARY` · `SECURITY-PERFORMANCE`

## Canary
Optional weak signal that the agent loaded the rules: the owner gives a form of address at the start of each session and the agent uses it in every reply. It is never written to any file.

## Notes
- `autoCompactWindow` / `CLAUDE_CODE_AUTO_COMPACT_WINDOW` (100k–1M). If a Claude Code version ignores them from project settings, put them in `~/.claude/settings.json`.
- Custom output styles need a recent Claude Code; unknown styles fall back to Default.
- Plugins cannot set `outputStyle`, `env` or `statusLine`; the installer writes those to the project settings.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). License: [MIT](LICENSE).
