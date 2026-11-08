## Summary
- What changed and why (one or two lines):
- Task / spec / issue, and tested commit SHA:
- Adjacent flows and surfaces touched:

## QUALITY-G1 — before implementing
- [ ] Surface and states mapped (UI states, platforms, APIs, data, jobs, CI); N/A has a reason.
- [ ] Risks mapped: authorization (user A ⇏ user B), secrets, dependencies, concurrency, privacy, cost, performance.
- [ ] Tests and measurable acceptance defined before the solution; rollback and compatibility with clients in the field considered.
- [ ] The owner approved the plan (when the project requires it).

## QUALITY-G2 — before Done / merge / release
| Evidence | PASS / FAIL / BLOCKED / NOT RUN / N/A + reason | Command, SHA, run or link |
| --- | --- | --- |
| Lint, types, unit and integration tests | | |
| E2E / screenshots inspected (viewports, themes, locales) | | |
| Native / device validation (if a native surface changed) | | |
| Authorization, migrations, backend, worker | | |
| Dependencies, vulnerabilities, secrets, logs | | |
| Performance before / after | | |
| CI, staging, rollback and smoke after deploy | | |

- [ ] No executed test is reported as PASS without evidence; nothing NOT RUN is reported as PASS.
- [ ] No open P0/P1; no regression in overflow, clipping, safe areas or accessibility.
- [ ] I separated: implementation · PR/merge · deploy · confirmed in production.
**Delivery:** one of OTA / build / server / N/A
**Risks, blockers, decisions needed:**
