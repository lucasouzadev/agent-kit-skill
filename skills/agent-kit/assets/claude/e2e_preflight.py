#!/usr/bin/env python3
"""agent-kit E2E / build preflight: checks the repository BEFORE a build or a Maestro run, so a run never
fails for a reason the repo already shows (conflict, stale lockfile, wrong appId, selector that does not
exist, missing sub-flow, env var nobody sets, workflow pointing at a missing path).

  python3 .claude/agent-kit/e2e_preflight.py [--flows DIR] [--fetch]

Read-only (only `git fetch` with --fetch). Prints PASS / WARN / FAIL per check, then NEEDS (what the owner
or CI must provide: env var and secret NAMES, never values). Exit 1 when any FAIL: fix those before running.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

SKIP_DIRS = {"node_modules", ".git", "build", "dist", "Pods", ".expo", ".gradle", "DerivedData", "vendor", ".next", "coverage"}
SRC_EXT = (".js", ".jsx", ".ts", ".tsx", ".swift", ".m", ".mm", ".kt", ".java", ".xml", ".dart", ".vue", ".html")
results, needs = [], set()


def res(state, check, detail=""):
    results.append((state, check, detail))


def git(*a):
    r = subprocess.run(["git", *a], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def walk(root, exts):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith(".") or x in (".maestro", ".github")]
        for f in files:
            if f.endswith(exts):
                yield os.path.join(d, f)


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def git_checks(fetch):
    if git("rev-parse", "--is-inside-work-tree") != "true":
        res("WARN", "git", "not a git repository")
        return
    if fetch:
        subprocess.run(["git", "fetch", "--quiet", "origin"], capture_output=True)
    if git("diff", "--name-only", "--diff-filter=U"):
        res("FAIL", "git conflicts", "unmerged paths: finish the merge/rebase first")
    marks = git("grep", "-n", "-I", "-E", r"^(<<<<<<< |>>>>>>> )", "--", ".", ":!*.md")
    if marks:
        res("FAIL", "conflict markers", "; ".join(marks.splitlines()[:3]))
    dirty = [l for l in git("status", "--porcelain").splitlines() if l.strip()]
    res("WARN" if dirty else "PASS", "working tree", f"{len(dirty)} uncommitted file(s): CI builds the pushed commit, not these" if dirty else "clean")
    up = git("rev-parse", "--abbrev-ref", "@{upstream}")
    if up:
        behind = git("rev-list", "--count", "HEAD..@{upstream}") or "0"
        ahead = git("rev-list", "--count", "@{upstream}..HEAD") or "0"
        if behind != "0":
            res("WARN", "branch", f"{behind} commit(s) behind {up}: pull before testing")
        if ahead != "0":
            res("WARN", "branch", f"{ahead} commit(s) not pushed: a CI run would test older code")
    head = git("symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD")
    if head:
        behind = git("rev-list", "--count", f"HEAD..{head}") or "0"
        if behind != "0":
            res("WARN", "default branch", f"{behind} commit(s) of {head} not in this branch: possible conflicts or already-fixed bugs")


def dep_checks():
    if not os.path.exists("package.json"):
        return
    locks = [f for f in ("package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "bun.lock") if os.path.exists(f)]
    if not locks:
        res("FAIL", "lockfile", "package.json without a lockfile: CI installs differ from local")
    elif len(locks) > 1:
        res("WARN", "lockfile", f"several lockfiles ({', '.join(locks)}): pick one package manager")
    else:
        pj = git("log", "-1", "--format=%ct", "--", "package.json")
        lk = git("log", "-1", "--format=%ct", "--", locks[0])
        stale = pj and lk and int(pj) > int(lk)
        res("WARN" if stale else "PASS", "lockfile", f"{locks[0]} older than package.json in git: run the install and commit the lockfile" if stale else locks[0])
    want = ""
    for f in (".nvmrc", ".node-version"):
        if os.path.exists(f):
            want = read(f).strip().lstrip("v")
    if not want:
        try:
            want = (json.loads(read("package.json")).get("engines") or {}).get("node", "")
        except ValueError:
            pass
    m = re.search(r"\d+", want or "")
    if m and shutil.which("node"):
        have = subprocess.run(["node", "-v"], capture_output=True, text=True).stdout.strip().lstrip("v")
        ok = have.split(".")[0] == m.group(0) or (want.startswith(">=") and int(have.split(".")[0]) >= int(m.group(0)))
        res("PASS" if ok else "WARN", "node version", f"want {want}, have {have}")


def app_ids():
    ids = set()
    for f in ("app.json", "app.config.json"):
        try:
            e = json.loads(read(f)).get("expo", {}) if os.path.exists(f) else {}
        except ValueError:
            e = {}
        ids |= {v for v in ((e.get("ios") or {}).get("bundleIdentifier"), (e.get("android") or {}).get("package")) if v}
    for f in ("app.config.js", "app.config.ts"):
        ids |= set(re.findall(r"(?:bundleIdentifier|package)\s*:\s*['\"]([\w.]+)['\"]", read(f)))
    for f in glob.glob("android/app/build.gradle*"):
        ids |= set(re.findall(r"applicationId\s*[= ]\s*['\"]([\w.]+)['\"]", read(f)))
    for f in glob.glob("ios/*.xcodeproj/project.pbxproj"):
        ids |= {v for v in re.findall(r"PRODUCT_BUNDLE_IDENTIFIER = \"?([\w.\-]+)\"?;", read(f)) if "$(" not in v}
    return ids


def source_ids():
    found = set()
    pat = re.compile(r"""(?:testID|accessibilityIdentifier|testTag|data-testid|resource-id|nativeID)\s*[=:(]\s*\{?\s*["'`]([\w.:/\-]+)["'`]|@\+id/([\w]+)""")
    for p in walk(".", SRC_EXT):
        for a, b in pat.findall(read(p)):
            found.add(a or b)
    return found


def flow_checks(flows_dir):
    dirs = [flows_dir] if flows_dir else [d for d in (".maestro", "maestro", "e2e/maestro", "e2e", "maestro/flows") if os.path.isdir(d)]
    flows = sorted({f for d in dirs for f in glob.glob(os.path.join(d, "**", "*.y*ml"), recursive=True) if not f.endswith("config.yaml")})
    if not flows:
        if flows_dir:
            res("FAIL", "maestro flows", f"no flows in {flows_dir}")
        return
    ids, known = app_ids(), source_ids()
    env_in_repo = "\n".join(read(f) for f in glob.glob(".github/workflows/*.y*ml") + glob.glob("**/run.sh", recursive=True) + glob.glob(".maestro/config.yaml") + glob.glob(".env.example"))
    missing_ids, missing_runs, bad_app, text_sel, id_sel, placeholders, env_vars = {}, [], [], 0, 0, [], set()
    for f in flows:
        t = read(f)
        m = re.search(r"(?m)^appId:\s*['\"]?([^'\"\s#]+)", t)
        if m and not m.group(1).startswith("${") and ids and m.group(1) not in ids:
            bad_app.append(f"{f}: {m.group(1)}")
        for sel in re.findall(r"""(?m)^\s*(?:-\s*)?(?:tapOn:\s*\{?\s*)?id:\s*["']?([\w.:/\-]+)["']?""", t):
            id_sel += 1
            if known and sel not in known and not sel.startswith("${"):
                missing_ids.setdefault(sel, f)
        text_sel += len(re.findall(r"""(?m)^\s*(?:-\s*)?(?:tapOn|assertVisible|assertNotVisible):\s*["'][^"']+["']|^\s*text:\s*["']""", t))
        for sub in re.findall(r"(?m)runFlow:\s*(?:\n\s*file:\s*)?['\"]?([\w./\-]+\.ya?ml)", t):
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), sub))):
                missing_runs.append(f"{f} -> {sub}")
        if re.search(r"""visible:\s*["']\.\*["']""", t):
            placeholders.append(f)
        env_vars |= set(re.findall(r"\$\{(\w+)\}", t))
    res("PASS", "maestro flows", f"{len(flows)} flow(s) in {', '.join(dirs) or flows_dir}")
    if bad_app:
        res("FAIL", "appId", f"flow appId not in the app config ({', '.join(sorted(ids))}): " + "; ".join(bad_app[:3]))
    if missing_ids:
        res("FAIL", "selectors", f"{len(missing_ids)} id(s) used by flows but not found in source (testID/accessibilityIdentifier): "
            + ", ".join(f"{k} ({v})" for k, v in list(missing_ids.items())[:5]))
    elif id_sel:
        res("PASS", "selectors", f"{id_sel} id selector(s) found in source")
    if text_sel and text_sel > id_sel:
        res("WARN", "selectors", f"{text_sel} text selector(s) vs {id_sel} id: text breaks with copy/locale changes; prefer testID")
    if missing_runs:
        res("FAIL", "runFlow", "missing sub-flow file(s): " + "; ".join(missing_runs[:3]))
    if placeholders:
        res("WARN", "placeholder", "flows still wait for visible '.*' (template value): " + ", ".join(placeholders[:3]))
    for v in sorted(env_vars):
        if v not in env_in_repo and v not in os.environ:
            needs.add(f"env {v} (used by flows; pass with -e {v}=... or set it in the workflow)")


def workflow_checks():
    for wf in glob.glob(".github/workflows/*.y*ml"):
        t = read(wf)
        if "maestro" not in t.lower():
            continue
        for p in re.findall(r"(?:FLOWS:\s*|maestro\s+test\s+)['\"]?([\w./\-]+)", t):
            if not p.startswith("$") and not os.path.exists(p) and "/" in p:
                res("FAIL", "workflow paths", f"{wf} points at missing {p}")
        for s in set(re.findall(r"secrets\.(\w+)", t)):
            needs.add(f"secret {s} (GitHub → Settings → Secrets → Actions; name only)")


def tool_checks():
    have = [t for t in ("maestro", "adb", "xcrun", "emulator") if shutil.which(t)]
    res("PASS" if have else "WARN", "local tools", ", ".join(have) if have else "no maestro/adb/xcrun here: run in CI (skill ci-device-lab) or on the owner's machine")


def main():
    a = sys.argv[1:]
    flows = a[a.index("--flows") + 1] if "--flows" in a and a.index("--flows") + 1 < len(a) else None
    git_checks("--fetch" in a)
    dep_checks()
    flow_checks(flows)
    workflow_checks()
    tool_checks()
    for s, c, d in results:
        print(f"{s:<5} {c}: {d}")
    if needs:
        print("NEEDS (from the owner or CI, names only):")
        for n in sorted(needs):
            print(f"  - {n}")
    fails = sum(1 for r in results if r[0] == "FAIL")
    print(f"\npreflight: {'FAIL' if fails else 'PASS'} ({fails} fail, {sum(1 for r in results if r[0] == 'WARN')} warn)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
