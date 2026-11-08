# agent-kit

A portable documentation and configuration standard for AI coding agents (Claude Code, Codex, Cursor).
Built from the strongest practices of five working repositories (Dialetto, Monologue, Arke and two public CI repos) and meant to drop into any new or existing project.

## Design

- **Short core, modules on demand.** `AGENTS.md` (≤ 120 lines) is the only thing loaded every session. Everything else is a doc or a skill opened by task (`standard/00-MAP.md`).
- **Meeting-style sessions.** The owner starts with a short message; agents boot from `AGENTS.md` + the handoff and detect their mode. No kickoff prompt.
- **Automatic economy (Claude Code):** terse output style, earlier auto-compaction, hooks that steer the compaction summary and re-inject the session state afterwards.
- **Evidence over claims:** PASS / FAIL / BLOCKED / NOT RUN / N/A; merged ≠ deployed ≠ verified.
- **Human approval gate** before any write; builds and releases only on explicit order.

## Contents

| Path | Role |
|---|---|
| `templates/AGENTS.md` | Entry point for app repos (placeholders `{{...}}`) |
| `templates/AGENTS.public-ci.md` | Entry point for public CI/build repos |
| `templates/CLAUDE.md` | `@AGENTS.md` + Claude Code notes |
| `standard/` | Generic rules, installed to `docs/agents/standard/` |
| `.claude/settings.json` | `outputStyle`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, hooks |
| `.claude/output-styles/caveman.md` | Terse replies (≤ 15 lines), keeps coding instructions |
| `.claude/hooks/` | `session-context.sh` (SessionStart startup/resume/compact), `precompact.sh` (PreCompact) — read-only |
| `.claude/skills/` | `caveman`, `session-preflight`, `systematic-debug`, `fundamentals-audit`, `ux-check`, `handoff` |

### `standard/`
`00-MAP` (what to read when) · `MODES` (Fixer, Builder, Product, Architect, Lens, Auditor) · `WORKFLOW` · `QUALITY-GATES` (G1/G2) · `DONE` · `SAFEGUARDS` · `TASK-CONTRACT` · `HANDOFF-TEMPLATE` · `REWORK-LEDGER` · `OWNER-DECISIONS-TEMPLATE` · `ORCHESTRATION` · `THREAT-MODEL` · `CHANGELOG-GUIDE` · `CONTEXT-BUDGET` · `CANARY` · `SECURITY-PERFORMANCE`

## Install

```bash
git clone https://github.com/lucasouzadev/agent-kit-skill agent-kit
./agent-kit/install.sh /path/to/project            # app repo
./agent-kit/install.sh /path/to/ci-repo --public-ci # public CI repo
grep -n '{{' /path/to/project/AGENTS.md             # fill placeholders
```

- Existing files are never overwritten without `--force`; the script lists every `SKIP` so you can merge by hand (or ask an agent to).
- Existing project skills with the same name win; keep project-specific detail in project docs and point to it from `AGENTS.md` §4.
- Session state file elsewhere than `HANDOFF.md`? List the paths (files or folders) in `.claude/handoff-paths`.
- **Canary:** set your form of address once in each tool's *personal* settings (e.g. `~/.claude/CLAUDE.md`: `Address me as <name> in every reply.`). It is never stored in a repository.

## Update a project
Re-run `install.sh`; `docs/agents/standard/` is kit-owned and refreshed; everything else is reported as `SKIP` if it diverged.

## Provenance
| Practice | From |
|---|---|
| Task contract, evidence states, safeguards, threat model, authority order, untrusted-input rule, public changelog guide, private canary | Arke |
| Modes, approval gate, QUALITY-G1/G2, definition of done, session packet, context budget, sub-agent orchestration, "do not reopen", merged ≠ production | Dialetto |
| Reading map by tiers, rework ledger, caveman, owner decisions log, handoff fields, "tests must not fake the platform" | Monologue |
| Public CI rules (no secrets/artifacts, dispatch-only, BLOCKED ≠ PASS) | dialetto-builds, monologue-builds |
| Security & performance invariants | "Guia agnóstico de stack de Performance e Segurança" (phase 3 turns it into skills) |

## Notes
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` can only lower the compaction threshold. If a Claude Code version ignores it from project `env`, nothing breaks; use `/autocompact` manually.
- The output style needs a recent Claude Code; unknown styles fall back to Default.
