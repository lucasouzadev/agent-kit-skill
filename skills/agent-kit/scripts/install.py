#!/usr/bin/env python3
"""agent-kit installer (stdlib only).

Usage:
  python3 install.py <target-repo> [--public-ci] [--no-vendor] [--dry-run]

What it does
  * docs/agents/standard/          kit-owned docs, always refreshed
  * .claude/agent-kit/             hooks + statusline, always refreshed
  * .claude/settings.json          merged: adds missing agent-kit keys, never overwrites yours
  * .claude/output-styles/caveman.md and .claude/skills/<kit skills>/   (unless --no-vendor)
  * AGENTS.md, CLAUDE.md, docs/agents/OWNER_DECISIONS.md   created only if missing

Safe updates: every file the kit writes is recorded with its hash in
.claude/agent-kit/manifest.json. On re-install a file is replaced only if it is
unchanged since the kit wrote it; files you edited are reported as SKIP.
--no-vendor: use when the agent-kit plugin is installed (skills, output style and
hooks come from the plugin; only docs, settings keys and templates are written).
Opt out of a kit skill (e.g. the project has its own variant): list its name in
.claude/agent-kit/skip-skills, one per line.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent          # skills/agent-kit
KIT_ROOT = SKILL_DIR.parent.parent                           # repo root when used from the plugin repo
VERSION = (SKILL_DIR / "VERSION").read_text().strip() if (SKILL_DIR / "VERSION").exists() else "dev"
CI_SKIP_SKILLS = {"ux-check", "fundamentals-audit", "performance-core", "platform-security"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    target = Path(argv[0]).resolve()
    public = "--public-ci" in argv
    vendor = "--no-vendor" not in argv
    dry = "--dry-run" in argv
    manifest_path = target / ".claude/agent-kit/manifest.json"
    old = json.loads(manifest_path.read_text()).get("files", {}) if manifest_path.exists() else {}
    new = {}
    log = []

    def put(src: Path, rel: str, owned: bool):
        """owned=True: kit file, refreshed if untouched. owned=False: create only."""
        dst = target / rel
        if dst.exists():
            same = sha(src) == sha(dst)
            if same:
                new[rel] = sha(src)
                return
            if not owned:
                log.append(f"keep   {rel} (yours)")
                return
            if rel in old and old[rel] != sha(dst):
                log.append(f"SKIP   {rel} (edited since kit wrote it; diff by hand)")
                new[rel] = old[rel]
                return
            if rel not in old:
                log.append(f"SKIP   {rel} (exists, not written by kit; diff by hand)")
                return
        log.append(f"write  {rel}")
        if not dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        new[rel] = sha(src)

    # 1. standard docs
    for f in sorted((SKILL_DIR / "standard").glob("*.md")):
        put(f, f"docs/agents/standard/{f.name}", True)
    # 2. hooks + statusline
    for f in sorted((SKILL_DIR / "assets/claude").glob("*.sh")):
        put(f, f".claude/agent-kit/{f.name}", True)
    # 3. vendored skills + output style
    if vendor:
        style = KIT_ROOT / "output-styles/caveman.md"
        if style.exists():
            put(style, ".claude/output-styles/caveman.md", True)
        skip_file = target / ".claude/agent-kit/skip-skills"
        skip = set(skip_file.read_text().split()) if skip_file.exists() else set()
        skills_root = KIT_ROOT / "skills"
        for sd in sorted(p for p in skills_root.iterdir() if p.is_dir() and p.name != "agent-kit"):
            if (public and sd.name in CI_SKIP_SKILLS) or sd.name in skip:
                continue
            for f in sorted(sd.rglob("*")):
                if f.is_file():
                    put(f, f".claude/skills/{sd.name}/{f.relative_to(sd)}", True)
    # 4. settings merge
    settings_src = json.loads((SKILL_DIR / "assets/claude/settings.json").read_text())
    if not vendor:
        settings_src.pop("hooks", None)  # the plugin ships the hooks
    sp = target / ".claude/settings.json"
    cur = json.loads(sp.read_text()) if sp.exists() else {}
    changed = False
    for k, v in settings_src.items():
        if k == "hooks":
            hooks = cur.setdefault("hooks", {})
            for event, entries in v.items():
                existing = json.dumps(hooks.get(event, []))
                for e in entries:
                    if json.dumps(e["hooks"]) not in existing and ".claude/agent-kit/" not in existing:
                        hooks.setdefault(event, []).append(e)
                        changed = True
        elif k == "env":
            env = cur.setdefault("env", {})
            for ek, ev in v.items():
                if ek not in env:
                    env[ek] = ev
                    changed = True
        elif k not in cur:
            cur[k] = v
            changed = True
    if changed:
        log.append("merge  .claude/settings.json (added missing agent-kit keys)")
        if not dry:
            sp.parent.mkdir(parents=True, exist_ok=True)
            sp.write_text(json.dumps(cur, indent=2, ensure_ascii=False) + "\n")
    # 5. entry points (create only)
    tpl = SKILL_DIR / "templates"
    put(tpl / ("AGENTS.public-ci.md" if public else "AGENTS.md"), "AGENTS.md", False)
    put(tpl / "CLAUDE.md", "CLAUDE.md", False)
    put(tpl / "OWNER_DECISIONS.md", "docs/agents/OWNER_DECISIONS.md", False)
    # 6. manifest
    if not dry:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps({"version": VERSION, "files": new}, indent=2) + "\n")
    # 7. warn when git would not track the shared config (other sessions would never get it)
    import subprocess
    for rel in (".claude/settings.json", ".claude/agent-kit/session-context.sh", ".claude/output-styles/caveman.md", "AGENTS.md"):
        if (target / rel).exists():
            r = subprocess.run(["git", "-C", str(target), "check-ignore", "-q", rel], capture_output=True)
            if r.returncode == 0:
                log.append(f"WARN   {rel} is git-ignored: add a '!{rel}' (or its folder) exception to .gitignore")
    print("\n".join(log) or "up to date")
    print(f"\nagent-kit {VERSION} -> {target}{' (dry run)' if dry else ''}")
    print("Next: fill {{PLACEHOLDERS}} (grep -rn '{{' AGENTS.md docs/agents/OWNER_DECISIONS.md); resolve every SKIP by hand.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
