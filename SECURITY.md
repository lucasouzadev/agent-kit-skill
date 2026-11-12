# Security policy

Agent Kit ships hooks that run on every agent session, so their integrity matters.

## Reporting
Report vulnerabilities privately through **GitHub → Security → Report a vulnerability** on this repository. Do not open a public issue. Include the affected file, version and a minimal reproduction.

## Scope
- Hooks in `skills/agent-kit/assets/claude/` and `hooks/hooks.json` (must stay offline and read-only; `ci_watch.py` only reads via `gh` and is never run by a hook).
- The installer (`install.py`) and the update check (`update.py`, explicit network call only).
- Workflow templates in `skills/ci-device-lab/templates/` and `skills/agent-kit/assets/github/`.
- Sub-agent definitions in `agents/`.

## Design guarantees
- Hooks never store prompt or command text (counts only) and never call the network.
- `action-guard` is a seatbelt, not a sandbox; `ask` is not guaranteed in bypass permission modes.
- Kit files are hash-checked against the install manifest at session start (`verify.py`).
