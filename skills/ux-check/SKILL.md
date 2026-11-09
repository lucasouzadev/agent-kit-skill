---
name: ux-check
description: UX checklist for any task touching a screen, control, sheet, menu, list, player, form or animation. Use before planning and before saying Done on a UI change. Covers core UX laws, states, accessibility, responsiveness and UI performance; project design rules extend it.
---

# UX check

Project design system and UX laws (tokens, motion presets, platform materials) live in the docs listed in `AGENTS.md` §4 and **override** this list.

- No disabled "coming soon". Short choice = anchored menu; long flow = sheet that closes by dragging; destructive actions distinct by shape/icon (not only colour) with undo or confirmation.
- Never a blank screen: skeleton at real size; data already seen appears at once. Nothing appears/disappears in one frame; reduced motion falls back to a fade; only project motion presets.
- Frequent actions near the thumb; targets ≥ 44 pt/px; labels for screen readers; visible focus; works at 200 % text.
- Optimistic updates roll back with a message; drafts save themselves; OS permission asked only at the moment of use; links and notifications open the exact content; back preserves scroll.
- Lists: paginated (cursor), virtualized if they can grow, media lazy and sized; animate only cheap properties (transform/opacity).
- UI thread: response ~100 ms, tasks ≤ 50 ms, ~16 ms per frame.
- Every locale has the same keys: run `.claude/agent-kit/i18n_parity.py` (exit 1 on missing/extra keys).
- Proof: project viewport/device matrix, light/dark, every locale, no horizontal overflow, **screenshots opened and read**. Native without a real binary = BLOCKED, not PASS.
- Rule broken on purpose → say which and why in the handoff.
