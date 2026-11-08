#!/usr/bin/env python3
"""agent-kit installer (stdlib only).

Usage:
  python3 install.py <target-repo> [--public-ci] [--no-vendor] [--profile lite|standard|full]
                             [--with-guard] [--cursor] [--dry-run]

What it does
  * docs/agents/standard/          kit-owned docs, always refreshed
  * .claude/agent-kit/             hooks + statusline, always refreshed
  * .claude/settings.json          merged: adds missing agent-kit keys, never overwrites yours
  * .claude/output-styles/caveman.md and .claude/skills/<kit skills>/   (unless --no-vendor)
  * AGENTS.md, CLAUDE.md, docs/agents/OWNER_DECISIONS.md   created only if missing

--profile: which skills to vendor (lite 7 · standard 15 · full 17+; default full or the last choice, kept in
.claude/agent-kit/profile). Skills already installed are never removed, only reported.
--cursor: also write .cursor/rules/agent-kit.mdc (automatic when .cursor/ exists).
--with-guard: adds .github/workflows/agent-kit-guard.yml (fails PRs that change kit hooks
without re-running the installer) and suggests a CODEOWNERS entry for .claude/.

Safe updates: every file the kit writes is recorded with its hash in
.claude/agent-kit/manifest.json. On re-install a file is replaced only if it is
unchanged since the kit wrote it; files you edited are reported as SKIP.
--no-vendor: use when the agent-kit plugin is installed (skills, output style and
hooks come from the plugin; only docs, settings keys and templates are written).
Point a generic standard doc to the project's own version: .claude/agent-kit/overrides,
one "NAME.md=path/from/repo/root.md" per line (adds a banner to the generic doc).
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
    guard = "--with-guard" in argv
    cursor = "--cursor" in argv or (target / ".cursor").is_dir()
    profile = next((argv[i + 1] for i, a in enumerate(argv) if a == "--profile" and i + 1 < len(argv)), None)
    pf = target / ".claude/agent-kit/profile"
    profile = profile or (pf.read_text().strip() if pf.exists() else "full")
    profiles = json.loads((SKILL_DIR / "profiles.json").read_text())
    if profile not in profiles:
        print(f"unknown profile {profile!r}; choose {', '.join(profiles)}")
        return 2
    chosen = profiles[profile]
    dry = "--dry-run" in argv
    manifest_path = target / ".claude/agent-kit/manifest.json"
    old = json.loads(manifest_path.read_text()).get("files", {}) if manifest_path.exists() else {}
    new = {}
    log = []

    def put(src: Path, rel: str, owned: bool, data: bytes = None):
        """owned=True: kit file, refreshed if untouched. owned=False: create only.
        data: write these bytes instead of src (e.g. a doc with an override banner)."""
        if data is not None:
            tmp = target / ".claude/agent-kit/.tmp-put"
            if not dry:
                tmp.parent.mkdir(parents=True, exist_ok=True)
                tmp.write_bytes(data)
                src = tmp
            else:
                import tempfile
                fd = tempfile.NamedTemporaryFile(delete=False); fd.write(data); fd.close(); src = Path(fd.name)
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

    # 1. standard docs (a project doc can override one: .claude/agent-kit/overrides, "NAME.md=path")
    ov_file = target / ".claude/agent-kit/overrides"
    overrides = {}
    if ov_file.exists():
        for line in ov_file.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                overrides[k.strip()] = v.strip()
    for f in sorted((SKILL_DIR / "standard").glob("*.md")):
        if f.name in overrides:
            banner = (f"> **Overridden in this project by [`{overrides[f.name]}`](../../../{overrides[f.name]}).** "
                      f"Follow that file; read this one only for what it does not cover.\n\n").encode()
            put(f, f"docs/agents/standard/{f.name}", True, banner + f.read_bytes())
        else:
            put(f, f"docs/agents/standard/{f.name}", True)
    # 2. hooks + statusline
    for f in sorted([*(SKILL_DIR / "assets/claude").glob("*.sh"), *(SKILL_DIR / "assets/claude").glob("*.py")]):
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
            if chosen != "*" and sd.name not in chosen:
                if (target / ".claude/skills" / sd.name).exists() and any(k.startswith(f".claude/skills/{sd.name}/") for k in old):
                    log.append(f"note   skill {sd.name} is outside profile '{profile}' (installed earlier; remove by hand if unwanted)")
                continue
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
                for e in entries:
                    existing = json.dumps(hooks.get(event, []))
                    missing = [h for h in e["hooks"] if h["command"].split("/")[-1] not in existing]
                    if missing:
                        hooks.setdefault(event, []).append({**e, "hooks": missing})
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
    # 4b. optional CI guard for the hooks
    if guard:
        put(SKILL_DIR / "assets/github/agent-kit-guard.yml", ".github/workflows/agent-kit-guard.yml", True)
        if not (target / ".github/CODEOWNERS").exists() and not (target / "CODEOWNERS").exists():
            log.append("hint   add a CODEOWNERS line so .claude/ changes need your review:  /.claude/ @<your-github-user>")
    if not dry and profile != "full" or pf.exists():
        if not dry:
            pf.parent.mkdir(parents=True, exist_ok=True)
            pf.write_text(profile + "\n")
    # 4c. rules for tools without hooks
    if cursor:
        put(SKILL_DIR / "templates/cursor-agent-kit.mdc", ".cursor/rules/agent-kit.mdc", True)
    # 5. entry points (create only)
    tpl = SKILL_DIR / "templates"
    put(tpl / ("AGENTS.public-ci.md" if public else "AGENTS.md"), "AGENTS.md", False)
    put(tpl / "CLAUDE.md", "CLAUDE.md", False)
    put(tpl / "OWNER_DECISIONS.md", "docs/agents/OWNER_DECISIONS.md", False)
    tmp = target / ".claude/agent-kit/.tmp-put"
    if tmp.exists():
        tmp.unlink()
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
