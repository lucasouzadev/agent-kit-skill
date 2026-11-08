# Changelog

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
