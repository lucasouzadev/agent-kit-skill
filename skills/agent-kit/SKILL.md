---
name: agent-kit
description: Sets up or upgrades a repository's AI-agent documentation standard - a short AGENTS.md entry point, on-demand rule docs, session handoff, owner-decisions log, terse output, early compaction with state re-injection, and security/performance skills. Use when asked to "set up agents", "add AGENTS.md", standardize or slim agent docs, upgrade agent-kit in a repo, or when a repo has no agent documentation.
---

# agent-kit — adopt the standard in a repository

Principle: a short core loaded every session, everything else opened by task. The owner starts sessions with a short message; agents boot from `AGENTS.md` + the handoff, with no kickoff prompt.

## Steps (the approval gate applies: present the plan before writing)

1. **Survey** the repo: existing `AGENTS.md`, `CLAUDE.md`, `.cursor/`, `docs/agents/`, handoff/status files, `.claude/`. Measure their size (bytes/4 ≈ tokens). Note owner decisions, project invariants, commands, build/release rules.
2. **Plan** what moves where and show it to the owner: nothing is deleted; dated owner instructions move to `docs/agents/OWNER_DECISIONS.md`; long history moves out of the boot path; project docs stay authoritative and are linked from `AGENTS.md` §4.
3. **Install** (after approval):
   `python3 ${CLAUDE_SKILL_DIR}/scripts/install.py <repo> [--public-ci] [--no-vendor] [--dry-run]`
   (`CLAUDE_SKILL_DIR` = this skill's folder; outside Claude Code use the path where the kit lives). Run with `--dry-run` first. Use `--no-vendor` when the agent-kit plugin is installed; vendor (default) when sessions run where plugins are not installed, e.g. cloud sessions or teammates.
4. **Fill** every `{{PLACEHOLDER}}` in `AGENTS.md` (project summary, commands, invariants, map, do-not-reopen, owner language, build rules). Keep it ≤ 120 lines.
5. **Resolve** every `SKIP` line by diffing by hand; keep project-specific variants of skills.
6. **Handoff path** not at `HANDOFF.md` / `docs/agents/HANDOFF.md`? Write the paths (files or folders) to `.claude/agent-kit/handoff-paths`.
7. **Verify:** `bash .claude/agent-kit/session-context.sh startup` prints the state; `.claude/settings.json` is valid JSON; relative links in new files resolve; no secret, personal data or canary value in the diff.

## What gets installed
| Path | Role |
|---|---|
| `AGENTS.md`, `CLAUDE.md` (`@AGENTS.md`) | entry points (created only if missing) |
| `docs/agents/standard/` | generic rules: map, modes, workflow, quality gates, done, safeguards, contracts, handoff, rework ledger, orchestration, threat model, context budget, canary, security/performance invariants |
| `docs/agents/OWNER_DECISIONS.md` | dated log of standing owner instructions |
| `.claude/settings.json` (merged) | `outputStyle: caveman`, `autoCompactWindow` 200k + env fallback, statusline, hooks |
| `.claude/agent-kit/` | `session-context.sh` (SessionStart), `precompact.sh` (PreCompact), `usage-guard.sh` (UserPromptSubmit), `statusline.sh` (context + plan usage), `manifest.json` |
| `.claude/skills/`, `.claude/output-styles/` | vendored copies (skip with `--no-vendor`) |

## Options
- `--pr-quality local|ci`: PR template, `.github/pr-quality.json` and `.github/scripts/pr_quality.py` (agents lint the PR body offline); `ci` adds the check workflow. Choose `local` on private repos with scarce Actions minutes. Keep the project's own PR template if it has one (create-only) and mirror its headings in `pr-quality.json`.
- Check for updates: `python3 .claude/agent-kit/update.py check` (explicit network call).
- `--profile lite|standard|full`: how many kit skills to vendor (7 / 15 / all). Recommend **lite** to newcomers and small projects, **standard** for apps with real users, **full** when the project builds in CI. Remembered in `.claude/agent-kit/profile`.
- `--cursor`: write `.cursor/rules/agent-kit.mdc` (automatic when `.cursor/` exists). Tools without hooks follow `docs/agents/standard/NO-HOOKS.md`.
- `guard-allow` / `guard-extra` in `.claude/agent-kit/`: standing authorizations (e.g. `eas build .*simulator`) and project-specific risky commands for the `action-guard` hook.
- `--with-guard`: CI workflow that fails PRs changing kit hooks outside the installer; add CODEOWNERS for `.claude/`. Skip it on private repos without Actions minutes.
- `.claude/agent-kit/overrides`: `NAME.md=path` per line when the project has its own version of a standard doc (one source of truth).
- `.claude/agent-kit/skip-skills`: kit skills the project replaces with its own.

## Measure
`python3 .claude/agent-kit/metrics.py report [--days N]` — sessions, prompts/session, compactions, peak context, modes, baton offers, git rework hotspots. Counts only; data stays in `~/.local/state/agent-kit/`. Run it weekly and cut what does not pay off.

## Compaction defaults (why 200k)
Large-context models otherwise compact near their full window, after quality has already degraded. 200k keeps sessions sharp and cheap; tune `autoCompactWindow` (100k–1M). The statusline shows `ctx used/window` and asks for a handoff from 70 %. If a Claude Code version ignores the project value, set it in `~/.claude/settings.json`.
