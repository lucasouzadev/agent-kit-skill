---
name: fundamentals-audit
description: Read-only audit of five engineering fundamentals - integration tests, never trust the client, race conditions, idempotency, separation of concerns. Use before touching money, quotas, invites, limited slots, webhooks, authorization rules or migrations, and when the same bug keeps returning.
---

# Fundamentals audit (read-only)

Do not edit files, run migrations or touch production. Deliver a report file in the project's QA folder (`<date>-fundamentals-audit.md`). Project anchors (paths, test harness) live in the project docs listed in `AGENTS.md` §4.

Order: 1 integration → 2 client trust → 3 race + idempotency → 4 separation.

- **Race:** every read-decide-write on a limited resource. Read the whole function (an early lock may already serialize) and **prove with a concurrency test** before listing it. Fix order: unique constraint → atomic conditional update (check rows affected) → row/advisory lock.
- **Idempotency:** webhooks verify the signature on the raw body and dedupe by event ID, order-independent; idempotency keys on payment-provider calls. Test: same event twice.
- **Client trust:** price/limit/permission recomputed on the server; no secret in client env vars; no allow-all policies; test user A ⇏ user B.
- **Separation:** longest files, what each mixes, the first candidate; characterization tests **before** refactoring.
- **Integration:** a critical flow covered only by mocks is a finding. A test failing on a real bug goes to the bug list; never skip, delete or loosen it.

No proof = "not verified" + reason. Each finding: file:line, risk, simplest fix, the test that proves it.
