# ONBOARDING — Chat for people who do not code

Goal: from the first message the person talks and the agent leads. No `/commands`, no prompts, no jargon, nothing to remember halfway through.

## What runs automatically (Claude Code)
| When | Mechanism | Effect |
|---|---|---|
| First session in a project, per user | `SessionStart` → `welcome.sh` | Agent greets in 3 lines, in the language of the person's first message, with one open question. Kind of folder detected: `new` (empty), `adopt` (work, no kit), `ready` (kit present). Shown once; marker in `~/.local/state/agent-kit/` (outside the repo). `AGENT_KIT_WELCOME=0` disables |
| Every message | `UserPromptSubmit` → `intent-brief.sh` | One line: if the person writes in everyday words, follow skill `guide-for-beginners`. `.claude/agent-kit/audience` = `beginner` (always plain), `dev` (never), `auto` (default) |
| Always | track + self-heal | Process runs underneath; the person sees human stages and results |

## Flows
- **New (empty folder):** short interview → restate → ask the folder name → create after yes → track.
- **Existing without kit:** ask once to organize (installer); on no, never again.
- **Kit present:** usual briefing from the handoff.

## Without hooks (Codex, Cursor, others)
At the first message of a session: if `AGENTS.md` shows no earlier session in the handoff, greet as above yourself; apply `guide-for-beginners` whenever the person writes in everyday words.

## Getting the kit without commands
The person (or whoever sets up the project once) needs one action; after that everything is automatic:
1. Project template: commit `.claude/settings.json` with the marketplace and plugin enabled (`extraKnownMarketplaces` + `enabledPlugins`) so opening the project installs the kit after one trust prompt. See `templates/claude-settings.beginner.json`.
2. Vendored: `install.py <repo>` copies hooks, skills and agents into the repo; teammates and cloud sessions need nothing.
3. One-line paste in a chat (without a repo): "Use github.com/lucasouzadev/agent-kit-skill as your way of working".
Claude Code never loads skills from repositories the person has not approved.
