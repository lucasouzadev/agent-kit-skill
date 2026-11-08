#!/usr/bin/env bash
# agent-kit installer. Usage: ./install.sh <target-repo> [--public-ci] [--force]
# Never overwrites an existing file without --force; prints what it skipped so you can diff.
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:?usage: install.sh <target-repo> [--public-ci] [--force]}"; shift || true
PUBLIC=0; FORCE=0
for a in "$@"; do case "$a" in --public-ci) PUBLIC=1;; --force) FORCE=1;; esac; done
VERSION="$(cat "$KIT/VERSION")"
put() { # src dst
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -e "$dst" ] && [ "$FORCE" -ne 1 ]; then
    if ! cmp -s "$src" "$dst"; then echo "SKIP (exists, differs): ${dst#$TARGET/}"; fi
    return
  fi
  cp "$src" "$dst"; echo "write: ${dst#$TARGET/}"
}
# 1. Generic docs (always refreshed: they are kit-owned, projects extend them elsewhere)
mkdir -p "$TARGET/docs/agents/standard"
for f in "$KIT"/standard/*.md; do cp "$f" "$TARGET/docs/agents/standard/"; done
echo "$VERSION" > "$TARGET/docs/agents/standard/VERSION"
echo "write: docs/agents/standard/ (agent-kit $VERSION)"
# 2. Claude Code config
put "$KIT/.claude/settings.json" "$TARGET/.claude/settings.json"
put "$KIT/.claude/output-styles/caveman.md" "$TARGET/.claude/output-styles/caveman.md"
for h in "$KIT"/.claude/hooks/*.sh; do put "$h" "$TARGET/.claude/hooks/$(basename "$h")"; done
chmod +x "$TARGET"/.claude/hooks/*.sh
for s in "$KIT"/.claude/skills/*/; do n="$(basename "$s")"
  if [ "$PUBLIC" -eq 1 ] && { [ "$n" = ux-check ] || [ "$n" = fundamentals-audit ]; }; then continue; fi
  put "$s/SKILL.md" "$TARGET/.claude/skills/$n/SKILL.md"; done
# 3. Entry points (templates with {{PLACEHOLDERS}} to fill by hand or by an agent)
if [ "$PUBLIC" -eq 1 ]; then put "$KIT/templates/AGENTS.public-ci.md" "$TARGET/AGENTS.md"
else put "$KIT/templates/AGENTS.md" "$TARGET/AGENTS.md"; fi
put "$KIT/templates/CLAUDE.md" "$TARGET/CLAUDE.md"
[ -e "$TARGET/docs/agents/OWNER_DECISIONS.md" ] || put "$KIT/templates/OWNER_DECISIONS.md" "$TARGET/docs/agents/OWNER_DECISIONS.md"
echo; echo "Next: fill {{PLACEHOLDERS}} in AGENTS.md (grep -n '{{' AGENTS.md); review every SKIP line with diff."
