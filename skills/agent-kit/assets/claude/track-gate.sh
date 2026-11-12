#!/usr/bin/env bash
# agent-kit Stop hook: enforces track stage 6/8. If this turn changed files (Edit/Write/MultiEdit/
# NotebookEdit or a git commit) and the final reply carries no evidence state
# (PASS / FAIL / BLOCKED / NOT RUN / N/A), the agent is sent back ONCE to verify (self-healing small
# failures) and close with evidence. Never loops (honours stop_hook_active). Reads the transcript
# only; logs counts, never text. Offline. AGENT_KIT_TRACK_GATE=0 disables.
here="$(cd "$(dirname "$0")" && pwd)"
. "$here/lib.sh"
ak_require_py
input=""; [ -t 0 ] || input="$(cat 2>/dev/null)"
[ "${AGENT_KIT_TRACK_GATE:-1}" = 0 ] && exit 0
printf '%s' "$input" | HERE="$here" "$PY" -c '
import json, os, re, subprocess, sys
try: d = json.load(sys.stdin) or {}
except Exception: sys.exit()
if d.get("stop_hook_active"): sys.exit()
path = d.get("transcript_path") or ""
if not path or not os.path.isfile(path): sys.exit()
recs = []
try:
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try: r = json.loads(line)
            except Exception: continue
            if isinstance(r, dict) and not r.get("isSidechain"): recs.append(r)
except Exception: sys.exit()

def blocks(r):
    c = (r.get("message") or {}).get("content")
    if isinstance(c, str): return [{"type": "text", "text": c}]
    return c if isinstance(c, list) else []

def real_user(r):
    if r.get("type") != "user" or r.get("isMeta"): return False
    b = blocks(r)
    return bool(b) and not any(x.get("type") == "tool_result" for x in b if isinstance(x, dict))

start = max((i for i, r in enumerate(recs) if real_user(r)), default=-1)
turn = [r for r in recs[start + 1:] if r.get("type") == "assistant"]
EDIT = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
edited, last_text = False, ""
for r in turn:
    for b in blocks(r):
        if not isinstance(b, dict): continue
        if b.get("type") == "tool_use":
            n = b.get("name", ""); cmd = str((b.get("input") or {}).get("command", ""))
            if n in EDIT or (n == "Bash" and re.search(r"\bgit\s+commit\b", cmd)): edited = True
            last_text = ""
        elif b.get("type") == "text":
            last_text += b.get("text", "") + "\n"
last_text = d.get("last_assistant_message") or last_text
if not edited: sys.exit()
if re.search(r"\b(PASS|FAIL|BLOCKED|NOT RUN|N/A)\b", last_text): sys.exit()
try:
    subprocess.Popen([sys.executable, os.path.join(os.environ.get("HERE", "."), "metrics.py"), "log", "trackgate", "decision=block", "session=" + str(d.get("session_id", ""))], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception: pass
print(json.dumps({"decision": "block", "reason":
  "agent-kit track (stages 5-8): you changed files this turn but the reply has no evidence states. "
  "Run the canonical checks now; fix small in-scope failures yourself (skill self-heal, sub-agent fixer-lite) without asking; "
  "pushed? watch CI (skill ci-monitor). Then close with PASS / FAIL / BLOCKED / NOT RUN / N/A + evidence per gate, "
  "the AUTOMATED vs PHYSICAL test list, and update the handoff. If you are only pausing for the owner (plan or question), mark the checks NOT RUN with the reason."}))
'
exit 0
