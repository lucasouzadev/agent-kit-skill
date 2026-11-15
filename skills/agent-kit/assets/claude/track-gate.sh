#!/usr/bin/env bash
# agent-kit Stop hook. Sends the agent back ONCE (never loops: honours stop_hook_active) when the turn
# ends with one of these, all checked from the transcript of this turn only:
#  1. evidence: files changed (Edit/Write/MultiEdit/NotebookEdit or git commit) but the final reply has
#     no evidence state (PASS / FAIL / BLOCKED / NOT RUN / N/A)            AGENT_KIT_TRACK_GATE=0 disables
#  2. repo state: the reply suggests opening/merging/closing a PR or creating/deleting/rebasing a branch
#     but nothing in the turn looked at the real state (git fetch/log/branch, gh pr, repo_state.py,
#     GitHub tools)                                                            AGENT_KIT_REPO_GATE=0 disables
#  3. ask: the reply ends with a decision for the owner written as prose (options, "want me to…?")
#     instead of the AskUserQuestion tool                                      AGENT_KIT_ASK_GATE=0 disables
# Logs counts, never text. Offline.
here="$(cd "$(dirname "$0")" && pwd)"
. "$here/lib.sh"
ak_require_py
input=""; [ -t 0 ] || input="$(cat 2>/dev/null)"
printf '%s' "$input" | HERE="$here" "$PY" "$here/track_gate.py"
exit 0
