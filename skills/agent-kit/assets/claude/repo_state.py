#!/usr/bin/env python3
"""agent-kit repo state: what is ALREADY true about branches, PRs and merges, before suggesting any of them.

  python3 .claude/agent-kit/repo_state.py [--no-fetch] [--branch NAME]

Read-only except `git fetch` (skip with --no-fetch). PRs come from the `gh` CLI when it is logged in;
without it the output says so and the agent uses the GitHub MCP tools (list_pull_requests) instead.
Never suggest opening, merging or closing a PR, or creating/deleting/rebasing a branch, without this
(or equivalent tool calls) in the same turn: owners lose trust when asked to do what is already done.

Squash and rebase merges are detected by patch id (git cherry), not only by ancestry.
Exit 0 always (it informs; it does not judge).
"""
import json
import shutil
import subprocess
import sys


def sh(*a, check=False):
    r = subprocess.run(list(a), capture_output=True, text=True)
    return r.stdout.strip() if (r.returncode == 0 or not check) else ""


def git(*a):
    return sh("git", *a)


def arg(name, default=None):
    a = sys.argv[1:]
    return a[a.index(name) + 1] if name in a and a.index(name) + 1 < len(a) else default


def in_default(ref, base):
    """Commits of ref not in base, and how many of them are already in base by patch id."""
    lines = [l for l in git("cherry", base, ref).splitlines() if l.strip()]
    return len(lines), sum(1 for l in lines if l.startswith("-"))


def main():
    if git("rev-parse", "--is-inside-work-tree") != "true":
        print("not a git repository")
        return 0
    fetched = "skipped"
    if "--no-fetch" not in sys.argv:
        r = subprocess.run(["git", "fetch", "--quiet", "--prune", "origin"], capture_output=True, text=True)
        fetched = "yes" if r.returncode == 0 else "FAILED (offline or no access: state below may be stale)"
    head = git("symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD") or ""
    default = head.split("/", 1)[1] if "/" in head else next(
        (b for b in ("main", "master") if git("rev-parse", "--verify", "--quiet", f"origin/{b}")), "main")
    base = f"origin/{default}"
    branch = arg("--branch") or git("branch", "--show-current") or "(detached)"
    print(f"default: {default} @ {git('rev-parse', '--short', base) or '?'}   fetch: {fetched}")
    dirty = len([l for l in git("status", "--porcelain").splitlines() if l.strip()])
    up = git("rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}")
    line = f"current: {branch}   uncommitted files: {dirty}"
    if branch != default and git("rev-parse", "--verify", "--quiet", branch):
        ahead = git("rev-list", "--count", f"{base}..{branch}") or "?"
        behind = git("rev-list", "--count", f"{branch}..{base}") or "?"
        total, landed = in_default(branch, base)
        line += f"   vs {base}: ahead {ahead}, behind {behind}"
        if total:
            line += f"   already in {default} by patch: {landed}/{total}"
            if landed == total:
                line += "  -> everything here is ALREADY merged; do not ask to merge it"
            elif landed:
                line += f"  -> only {total - landed} commit(s) still need a PR"
    if up:
        a = git("rev-list", "--count", f"{up}..{branch}") or "0"
        b = git("rev-list", "--count", f"{branch}..{up}") or "0"
        line += f"   upstream {up}: {'in sync' if a == b == '0' else f'unpushed {a}, unpulled {b}'}"
    elif branch not in (default, "(detached)"):
        line += "   upstream: none (never pushed)"
    print(line)
    if git("diff", "--name-only", "--diff-filter=U"):
        print("CONFLICTS: unmerged paths in the working tree")

    # PRs
    if shutil.which("gh") and subprocess.run(["gh", "auth", "status"], capture_output=True).returncode == 0:
        try:
            mine = json.loads(sh("gh", "pr", "list", "--state", "all", "--head", branch, "--limit", "5",
                                 "--json", "number,state,title,mergedAt,url,baseRefName") or "[]")
            opened = json.loads(sh("gh", "pr", "list", "--state", "open", "--limit", "20",
                                   "--json", "number,headRefName,baseRefName,isDraft,title") or "[]")
        except ValueError:
            mine, opened = [], []
        if mine:
            for p in mine:
                print(f"PR for {branch}: #{p['number']} {p['state']}{' ' + p['mergedAt'][:10] if p.get('mergedAt') else ''} -> {p['baseRefName']} \"{p['title'][:60]}\"")
            if all(p["state"] == "MERGED" for p in mine) and branch != default:
                total, landed = in_default(branch, base)
                if total > landed:
                    print(f"  -> PR merged, but {total - landed} newer commit(s) on {branch} are NOT in {default}: they need a NEW PR")
        elif branch != default:
            print(f"PR for {branch}: none")
        print(f"open PRs: {len(opened)}" + "".join(
            f"\n  #{p['number']} {p['headRefName']} -> {p['baseRefName']}{' (draft)' if p.get('isDraft') else ''} \"{p['title'][:50]}\"" for p in opened))
    else:
        print("PRs: unknown here (gh not logged in) -> check with the GitHub MCP tools (list_pull_requests / pull_request_read) before suggesting PR actions")

    # remote branches whose work is already in default (safe-to-delete candidates; deleting is still the owner's call)
    done, pending = [], []
    for rb in git("branch", "-r", "--format=%(refname:short)").splitlines()[:40]:
        if rb in (base, "origin/HEAD", "origin") or rb.endswith("/HEAD"):
            continue
        total, landed = in_default(rb, base)
        (done if total == landed else pending).append(f"{rb.split('/', 1)[1]}" + ("" if total == landed else f" ({total - landed} not merged)"))
    if done:
        print(f"remote branches fully merged into {default}: {', '.join(done)}")
    if pending:
        print(f"remote branches with unmerged work: {', '.join(pending)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
