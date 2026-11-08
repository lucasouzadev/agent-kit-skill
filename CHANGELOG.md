# Changelog

## 1.1.0 — 2026-11-08
- Packaged as a Claude Code plugin + marketplace (`.claude-plugin/`), skills under `skills/`, plugin hooks in `hooks/hooks.json`.
- Security & performance skills: `security-core`, `identity-session`, `data-privacy`, `supply-chain`, `performance-core`, `platform-security`.
- Compaction: `autoCompactWindow` 200k (+ `CLAUDE_CODE_AUTO_COMPACT_WINDOW` fallback) replaces the percentage override; statusline shows context use and asks for a handoff from 70 %.
- Canary: form of address given by the owner at the start of each session; preserved through compaction; never stored.
- Installer rewritten in Python: hash manifest for safe re-installs, settings merge, `--no-vendor`, `--dry-run`.
- Removed all project-specific references.

## 1.0.0 — 2026-11-08
- Initial standard: AGENTS.md template, standard docs, caveman output style, SessionStart/PreCompact hooks, six workflow skills.
