#!/usr/bin/env python3
"""Imports a curated set of skills from addyosmani/agent-skills (MIT) into skills/.

  git clone --depth 1 https://github.com/addyosmani/agent-skills /tmp/agent-skills
  python3 tools/sync_upstream_skills.py /tmp/agent-skills                       # addyosmani/agent-skills
  python3 tools/sync_upstream_skills.py replica /tmp/replica-skill              # Jakeschincariol/replica-skill
  python3 tools/sync_upstream_skills.py rea /tmp/rea                            # morluto/rea (skill only)

What it does, per skill: copies skills/<name>/ verbatim, copies every repo-level
`../../references/<file>` the skill links into the skill's own `references/` folder (so the
skill works when vendored into .claude/skills/), rewrites those links, and inserts one notice
line after the frontmatter (origin, licence, precedence of AGENTS.md). Skills that overlap a
kit skill are not imported (see SKIPPED). Re-run to update; review the diff before committing.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = "addyosmani/agent-skills"
IMPORT = [
    "spec-driven-development", "planning-and-task-breakdown", "incremental-implementation",
    "test-driven-development", "code-review-and-quality", "code-simplification",
    "git-workflow-and-versioning", "ci-cd-and-automation", "source-driven-development",
    "doubt-driven-development", "observability-and-instrumentation", "api-and-interface-design",
    "frontend-ui-engineering", "browser-testing-with-devtools", "deprecation-and-migration",
    "documentation-and-adrs", "shipping-and-launch",
]
SKIPPED = {  # upstream skill -> kit skill that already covers it
    "debugging-and-error-recovery": "systematic-debug", "security-and-hardening": "security-core",
    "performance-optimization": "performance-core", "context-engineering": "agent-kit (core)",
    "interview-me": "session-guide", "idea-refine": "session-guide + triage",
    "using-agent-skills": "TRACK.md", "constraint-driven-development": "QUALITY-GATES.md",
}
ALIAS = {  # upstream skill names the kit covers under another name (rewritten in imported text)
    "debugging-and-error-recovery": "systematic-debug", "security-and-hardening": "security-core",
    "performance-optimization": "performance-core",
    "skills/context-engineering/SKILL.md": "docs/agents/standard/CONTEXT-BUDGET.md", "context-engineering": "CONTEXT-BUDGET",
}
REF = re.compile(r"\.\./\.\./references/([A-Za-z0-9_.-]+\.md)")


def main(src):
    src = Path(src)
    sha = subprocess.run(["git", "-C", str(src), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "unknown"
    for name in IMPORT:
        s, d = src / "skills" / name, ROOT / "skills" / name
        if not (s / "SKILL.md").exists():
            print(f"missing upstream skill {name}"); continue
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(s, d)
        for f in d.rglob("*.md"):
            text = f.read_text()
            for ref in set(REF.findall(text)):
                (d / "references").mkdir(exist_ok=True)
                shutil.copy2(src / "references" / ref, d / "references" / ref)
            depth = len(f.relative_to(d).parts) - 1
            for a, b in ALIAS.items():
                text = re.sub(r"(?<![\w/-])" + re.escape(a) + r"(?![\w-])", b, text)
            text = REF.sub(lambda m: ("../" * depth) + "references/" + m.group(1), text)
            if f.name == "SKILL.md" and f.parent == d:
                head, sep, body = text.partition("\n---\n")
                note = (f"\n> Imported from [{UPSTREAM}](https://github.com/{UPSTREAM}) @ {sha} (MIT, see "
                        f"`LICENSE.txt` here). In agent-kit repos `AGENTS.md` and `docs/agents/standard/TRACK.md` "
                        f"take precedence: approval gate, evidence states, self-heal envelope, caveman output.\n")
                text = head + sep + note + body
            f.write_text(text)
        shutil.copy2(src / "LICENSE", d / "LICENSE.txt")
        print(f"import {name}")
    print(f"\n{len(IMPORT)} skills from {UPSTREAM}@{sha}; skipped (covered by the kit): {', '.join(SKIPPED)}")


def notice(repo, sha, extra=""):
    return (f"\n> Imported from [{repo}](https://github.com/{repo}) @ {sha} (MIT, see `LICENSE.txt` here). "
            f"In agent-kit repos `AGENTS.md` and `docs/agents/standard/TRACK.md` take precedence: approval gate, "
            f"evidence states, self-heal envelope, caveman output.{extra}\n")


def put_notice(skill_md, repo, sha, extra=""):
    text = skill_md.read_text()
    head, sep, body = text.partition("\n---\n")
    skill_md.write_text(head + sep + notice(repo, sha, extra) + body)


def sha_of(src):
    return subprocess.run(["git", "-C", str(src), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "unknown"


def replica(src):
    """Eleven replica-* skills: whole folders (SKILL.md + the small stdlib-only Python tools they call by
    sibling path, e.g. ../replica-design/contrast.py, so they must stay side by side)."""
    src = Path(src); sha = sha_of(src); n = 0
    for sd in sorted(src.glob("replica-*")):
        if not (sd / "SKILL.md").exists():
            continue
        d = ROOT / "skills" / sd.name
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(sd, d, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy2(src / "LICENSE", d / "LICENSE.txt")
        put_notice(d / "SKILL.md", "Jakeschincariol/replica-skill", sha,
                   " Clean-room only: rebuild what an app does, never its code, logo, copy or content.")
        n += 1; print(f"import {sd.name}")
    print(f"\n{n} skills from Jakeschincariol/replica-skill@{sha}")


def rea(src):
    """Only the agent skill of REA (SKILL.md + references) and its DISCLAIMER; not the MCP server (npm: rea-agents)."""
    src = Path(src); sha = sha_of(src)
    s = src / ".agents/skills/reverse-engineer-anything"
    d = ROOT / "skills/reverse-engineer-anything"
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(s, d)
    shutil.copy2(src / "LICENSE", d / "LICENSE.txt")
    shutil.copy2(src / "DISCLAIMER.md", d / "DISCLAIMER.md")
    put_notice(d / "SKILL.md", "morluto/rea", sha,
               " Needs the REA MCP server (`npx rea-agents setup`); read `DISCLAIMER.md` here first. "
               "Authorized, lawful analysis only; the approval gate applies before running anything against a target.")
    print(f"import reverse-engineer-anything\n\n1 skill from morluto/rea@{sha}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "replica":
        replica(a[1])
    elif len(a) == 2 and a[0] == "rea":
        rea(a[1])
    elif len(a) == 1:
        main(a[0])
    else:
        print(__doc__); sys.exit(2)
