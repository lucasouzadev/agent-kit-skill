#!/usr/bin/env bash
# agent-kit welcome (called by session-context.sh on a fresh startup): the first time a person opens a
# project with the kit, tells the agent to greet in 3 lines, in the language of their FIRST message,
# and ask ONE open question - no commands, no skill names, no jargon. It detects what kind of folder
# this is so the agent leads the next step. Shown once per project per user: the marker lives in the
# kit's state dir (outside the repo), never in the project. Read-only except that marker. Offline.
# AGENT_KIT_WELCOME=0 disables. Never prints file names or contents.
here="$(cd "$(dirname "$0")" && pwd)"
. "$here/lib.sh"
[ "${AGENT_KIT_WELCOME:-1}" = 0 ] && exit 0
proj="${CLAUDE_PROJECT_DIR:-$PWD}"
state="${AGENT_KIT_STATE:-$HOME/.local/state/agent-kit}"
marker="$state/welcomed-$(printf '%s' "$proj" | cksum | cut -d' ' -f1)"
[ -e "$marker" ] && exit 0
cd "$proj" 2>/dev/null || exit 0
# What is this folder? new = (almost) empty and not a repo · adopt = has work but no kit · ready = kit present
files="$(find . -maxdepth 2 -not -path './.git*' -not -path './.claude*' -type f 2>/dev/null | head -6 | wc -l | tr -d ' ')"
if [ -f AGENTS.md ] || [ -d .claude/agent-kit ]; then kind=ready
elif [ "$files" -le 1 ]; then kind=new
else kind=adopt; fi
mkdir -p "$state" 2>/dev/null && : > "$marker" 2>/dev/null
cat <<TXT
[agent-kit] FIRST MEETING (project kind: $kind). Your first reply is a welcome, not work. Rules:
- Language: the language of the owner's first message; if it is only a greeting, the language they greet in.
- 3 short lines: who you are (their coding partner who leads the work), that they can just talk normally (no commands, no special phrases), and ONE open question: what do they want to build or fix today?
- Plain words. Do not mention skills, hooks, tracks, stages, models, slash commands or file names.
- Follow skill guide-for-beginners for tone and flow; if they write like a developer (code, paths, jargon), switch to normal terse mode.
TXT
case "$kind" in
  new) echo "- Folder is empty: after their answer, lead a short interview (one question at a time, options with a recommendation), then ASK which name the project folder should have; create it only after they say yes (skill guide-for-beginners, section New project).";;
  adopt) echo "- Existing work without the kit: after greeting, ask ONCE whether you may organize the project so you can work better (it adds files; nothing is deleted). On yes, run the installer (skill agent-kit). On no, work normally and do not ask again.";;
  ready) echo "- The kit is already set up: greet, give the usual 3-line briefing from the handoff (skill session-guide) and ask what to do today.";;
esac
