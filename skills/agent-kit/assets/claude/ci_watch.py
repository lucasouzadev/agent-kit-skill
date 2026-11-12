#!/usr/bin/env python3
"""agent-kit CI watcher: follows the GitHub Actions runs of one commit until they finish.

Read-only (uses the `gh` CLI the session is already logged into; never re-runs, cancels or dispatches).
Meant to run in the background, ideally from the `ci-watcher` sub-agent on a light model.

  python3 .claude/agent-kit/ci_watch.py [--sha SHA] [--wait] [--timeout 1800] [--interval 30] [--logs 60]

Prints one line per run, then, for failed runs, the failed jobs, a class (infra = re-run candidate,
defect = fix it) and the last --logs lines of the failed steps.
Exit: 0 all green · 1 a run failed · 2 still running at timeout / no runs found · 3 gh unavailable.
"""
import json
import re
import shutil
import subprocess
import sys
import time

INFRA = re.compile(
    r"runner has received a shutdown signal|lost communication with the server|ECONNRESET|ETIMEDOUT|"
    r"EAI_AGAIN|socket hang up|50[234] (Bad Gateway|Service Unavailable|Gateway Time-?out)|"
    r"rate limit exceeded|No space left on device|The operation was canceled|"
    r"Could not resolve host|TLS handshake timeout|toomanyrequests|exceeded the maximum execution time",
    re.I,
)
FIELDS = "databaseId,name,status,conclusion,url,headSha,event,workflowName"


def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1:] or ["gh failed"])
    return r.stdout


def arg(name, default):
    a = sys.argv[1:]
    return a[a.index(name) + 1] if name in a and a.index(name) + 1 < len(a) else default


def main():
    if not shutil.which("gh"):
        print("gh CLI not found. Use the GitHub MCP tools instead (actions_list / get_job_logs) or ask the owner to install gh.")
        return 3
    sha = arg("--sha", None)
    if not sha:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    wait = "--wait" in sys.argv
    timeout = int(arg("--timeout", "1800"))
    interval = max(5, int(arg("--interval", "30")))
    nlogs = min(200, int(arg("--logs", "60")))
    start = time.time()
    runs = []
    while True:
        try:
            runs = json.loads(gh("run", "list", "--commit", sha, "--json", FIELDS, "--limit", "30") or "[]")
        except Exception as e:  # auth, network, not a GitHub repo
            print(f"gh error: {e}")
            return 3
        pending = [r for r in runs if r.get("status") != "completed"]
        if not wait or (runs and not pending) or time.time() - start > timeout:
            break
        time.sleep(interval)
    if not runs:
        print(f"no workflow runs for {sha[:10]} yet (pushed? workflows on this branch/event?)")
        return 2
    failed = []
    for r in runs:
        state = r.get("conclusion") or r.get("status")
        print(f"{state:<11} {r.get('workflowName') or r.get('name')} [{r.get('event')}] {r.get('url')}")
        if r.get("status") == "completed" and r.get("conclusion") not in ("success", "skipped", "neutral"):
            failed.append(r)
    if any(r.get("status") != "completed" for r in runs):
        print("still running" + (" at timeout" if wait else "") + "; watch again later")
        if not failed:
            return 2
    for r in failed:
        rid = str(r["databaseId"])
        try:
            jobs = json.loads(gh("run", "view", rid, "--json", "jobs")).get("jobs", [])
            bad = [j.get("name") for j in jobs if j.get("conclusion") not in ("success", "skipped", "neutral", None)]
        except Exception:
            bad = []
        try:
            log = gh("run", "view", rid, "--log-failed")
        except Exception:
            log = ""
        cls = "infra (re-run candidate)" if INFRA.search(log) else ("cancelled" if r.get("conclusion") == "cancelled" else "defect (fix it)")
        print(f"\nFAILED {r.get('workflowName')} #{rid}: jobs {', '.join(bad) or '?'} -> {cls}")
        tail = [re.sub(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ", "", l.split("\t")[-1]) for l in log.splitlines()[-nlogs:]]
        if tail:
            print("--- last failed-step lines ---")
            print("\n".join(tail))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
