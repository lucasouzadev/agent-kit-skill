---
name: performance-core
description: Stack-agnostic performance principles and public thresholds (Core Web Vitals, Android vitals, Apple hangs, RAIL). Use for any new feature with UI, lists, network or startup work, for performance regressions, and when setting budgets or CI gates.
---

# Performance core

Thresholds and budget template: [thresholds.md](thresholds.md).

1. **Measure before optimizing**, with field data (RUM) and lab data. Lab diagnoses, field tells the truth. Field telemetry segmented by device, network and version; every optimization has a baseline and a measured result. *Essential.*
2. **Percentiles, never averages.** p75 is the target (Core Web Vitals use it), p95/p99 show who suffers; mobile uses per-user rates (crash/ANR per DAU). *Essential.*
3. **Explicit budgets** for bundle/binary size, startup, INP/hangs, memory and initial requests; **CI fails** on violation. Otherwise every PR "only adds 30 KB". *Essential.*
4. **Protect the UI thread.** Respond ≤ ~100 ms, work in chunks ≤ ~50 ms, ~16 ms per frame. No I/O, network, large parsing, crypto or compression on it. Detect long tasks (> 50 ms); monitor hangs ≥ 250 ms and ANRs in production. *Essential.*
5. **Minimal critical path and startup.** Inventory what runs before the first useful frame; lazy-init SDKs, analytics and non-essential modules. Web: LCP resource discovered early and prioritized; no needless render blocking. *Essential.*
6. **Do less.** Remove dead code, heavy dependencies, needless polyfills; memoize only where measured; paginate instead of loading everything. *Essential.*
7. **Load on demand.** Rare routes/screens/features lazy; offscreen images deferred — the LCP element **never**. *Recommended.*
8. **Network:** fewer round trips and bytes, correct HTTP caching with validation, compression, modern sized images, lean API responses; timeouts, retry with backoff, idempotency; offline/degraded UI; test with throttling. *Essential.*
9. **Memory:** heap profiles on long flows; listeners/timers/observers unregistered; bounded caches; images decoded at display size. *Recommended.*
10. **Rendering and lists:** virtualize/recycle long lists; avoid forced synchronous layout and cascading re-renders; reserve space for media (CLS ≤ 0.1); animate only cheap properties (transform/opacity or native equivalents). *Essential.*
11. **App/bundle size** analysed every release against a budget; assets optimized; per-density/locale delivery when the platform allows. *Recommended.*
12. **Energy:** batch background work, push instead of polling, no needless wake locks or continuous location, stop animations/timers offscreen. *Recommended.*
13. **Test on modest hardware and networks:** at least one entry-level device (or 4–6× CPU throttling on web) and slow network profiles; field metrics segmented by device tier. *Essential.*
14. **Block regressions in CI:** benchmarks per PR (startup, size, critical interaction) with tolerance; anomaly alerts per version; staged rollout watches vitals before 100 %. *Essential.*

## Gotchas
- A passing lab score with bad field data is a failing app.
- Emulators and the team's phones are not the users' devices.
- Store thresholds are floors, not goals: set stricter internal targets.

Sources: web.dev (Web Vitals, "How the Core Web Vitals thresholds were defined", LCP, INP, CLS); Google RAIL model; Android Developers (Android vitals, App startup time); Apple WWDC23 "Analyze hangs with Instruments"; Xcode Organizer / MetricKit.
