# Contributing

Contributions are welcome: new skills, platform modules, better defaults, translations of the owner-facing parts, bug fixes in the installer or hooks.

## Rules of the kit (keep them when contributing)
1. **Generic only.** No project names, personal data, internal hosts, secrets or company-specific rules. Project specifics belong in the adopting repo, linked from its `AGENTS.md`.
2. **Short core.** `templates/AGENTS.md` stays ≤ 120 lines; a skill body ≤ ~80 lines with detail in files one level deep; a standard doc ≤ ~2k tokens.
3. **Principle → why → how to verify.** Every rule says why it exists and how an agent proves it was followed (command, test, metric).
4. **Cite sources** for normative claims (standards, official platform docs) at the end of the skill or its reference file, never duplicated across skills.
5. **Hooks are read-only and offline.** No writes outside the session's own state, no network, small output.
6. **No silent behaviour change.** Defaults that change agent behaviour (compaction window, output style) go in the CHANGELOG with the reason.

## Process
- Open an issue for larger changes first.
- Run `bash tests/run.sh` (and `claude plugin validate .` if you have Claude Code) before the PR; CI runs the tests and actionlint **with shellcheck**: install both locally (`pip install actionlint-py shellcheck-py`) or you will miss what CI reports.
- New hook behaviour needs a test in `tests/run.sh`; hooks stay offline and never store prompt text.
- Bump `version` in `.claude-plugin/plugin.json` and `skills/agent-kit/VERSION`, and add a CHANGELOG entry.
