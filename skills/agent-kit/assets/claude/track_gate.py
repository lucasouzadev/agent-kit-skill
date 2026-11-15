#!/usr/bin/env python3
"""agent-kit Stop hook logic (called by track-gate.sh). See track-gate.sh for the rules."""
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
edited, last_text, cmds, names = False, "", [], []
for r in turn:
    for b in blocks(r):
        if not isinstance(b, dict): continue
        if b.get("type") == "tool_use":
            n = b.get("name", ""); cmd = str((b.get("input") or {}).get("command", ""))
            names.append(n); cmds.append(cmd)
            if n in EDIT or (n == "Bash" and re.search(r"\bgit\s+commit\b", cmd)): edited = True
            last_text = ""
        elif b.get("type") == "text":
            last_text += b.get("text", "") + "\n"
last_text = d.get("last_assistant_message") or last_text
env = os.environ.get
reasons, rules = [], []
if env("AGENT_KIT_TRACK_GATE", "1") != "0" and edited and not re.search(r"\b(PASS|FAIL|BLOCKED|NOT RUN|N/A)\b", last_text):
    rules.append("evidence")
    reasons.append("You changed files this turn but the reply has no evidence states. Run the canonical checks; fix small in-scope failures yourself "
                   "(skill self-heal, sub-agent fixer-lite) without asking; pushed? watch CI (skill ci-monitor). Close with PASS / FAIL / BLOCKED / NOT RUN / N/A "
                   "+ evidence per gate, the AUTOMATED vs PHYSICAL test list, and update the handoff. Only pausing for the owner? Mark checks NOT RUN with the reason.")
REPO_ACT = re.compile(r"\b(abr[aei]r?|abra|cri[ae]r?|fech[ae]r?|merg\w*|fa[cç]a o merge|delet\w*|apag\w*|exclu\w*|rebase\w*|open|create|close|merge|delete|rebase|crea[r]?|cierr\w*|borr\w*)\b[^.\n?]{0,60}\b(PR|PRs|pull request|branch|branches|merge|ramo|rama)\b", re.I)
LOOKED = re.compile(r"\bgit\s+(fetch|log|branch|status|ls-remote|cherry|rev-list|show-branch)\b|\bgh\s+(pr|api|run|repo)\b|repo_state\.py")
looked = any(LOOKED.search(c) for c in cmds) or any("github" in n.lower() for n in names)
if env("AGENT_KIT_REPO_GATE", "1") != "0" and REPO_ACT.search(last_text) and not looked:
    rules.append("repo")
    reasons.append("Your reply suggests a PR/branch/merge action but this turn never checked the real repository state. Run "
                   "`python3 .claude/agent-kit/repo_state.py` (or git fetch + gh pr list / the GitHub MCP list_pull_requests), then rewrite the "
                   "suggestion from the facts: never ask the owner to do what is already done (merged PR, existing branch, open PR).")
tail = last_text.strip()[-500:]
ASKY = re.compile(r"(quer que eu|voc[eê] prefere|prefere|devo |posso (seguir|abrir|fazer|criar)|qual (das|op[cç][aã]o|voc[eê])|escolh|do you want|want me to|should i|shall i|would you like|which (one|option)|do you prefer|¿?quieres|prefieres|te parece)", re.I)
OPTIONS = re.compile(r"(?m)^\s*(\d+[.)]|[A-D][).:]|[-*]\s+\*\*(op[cç][aã]o|option)|op[cç][aã]o [A-D1-4]|option [A-D1-4])", re.I)
asked = "AskUserQuestion" in names
if env("AGENT_KIT_ASK_GATE", "1") != "0" and not asked and "?" in tail and (ASKY.search(tail) or (OPTIONS.search(last_text) and "?" in tail)):
    rules.append("ask")
    reasons.append("You end with a decision for the owner written as prose. Ask it with the AskUserQuestion tool instead (1-4 questions, 2-4 options each, "
                   "recommended option first with '(Recommended)', short self-contained wording) so the owner answers with one click and nothing stays buried in the chat. "
                   "Open questions with no options ('what do you want to build?') may stay as text.")
if not reasons: sys.exit()
try:
    subprocess.Popen([sys.executable, os.path.join(os.environ.get("HERE", "."), "metrics.py"), "log", "trackgate", "decision=block", "rules=" + "+".join(rules), "session=" + str(d.get("session_id", ""))], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception: pass
print(json.dumps({"decision": "block", "reason": "agent-kit track: " + " ".join(f"({i + 1}) {r}" for i, r in enumerate(reasons))}))
