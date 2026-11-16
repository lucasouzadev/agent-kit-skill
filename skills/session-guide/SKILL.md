---
name: session-guide
description: Conversation-led sessions - the agent leads the developer through the work from plain talk, without the developer writing prompts. Use at the start of every session, when the owner's message is short, casual or feedback-like ("vamos ver o login", "aquilo ficou estranho"), when the owner seems unsure what to do next, and when closing a session.
---

# Session guide (the agent leads, the owner talks)

The owner gives context like in a short meeting; the agent turns it into work. Detail: `docs/agents/standard/CONVERSATION.md`.

## Opening (first reply of a session)
1. Silently boot: `AGENTS.md`, handoff, git state. Do not ask what the repo answers.
2. Run `python3 .claude/agent-kit/repo_state.py` (what really merged, which PRs are open), then reply with a **3-line briefing**: where we stopped · what is pending (owner decisions first) · 2–3 options for today, recommendation first.
3. Ask for the canary form of address if not given.

## During the session
- Compile every owner message into an invisible brief first (skill `intent-compiler`; the `intent-brief` hook reminds you each turn).
- Restate each owner message as a one-line goal + acceptance before acting ("Entendi: X; pronto quando Y. Sigo?"). Silence on details = use the recommended default and say which.
- Decisions through the AskUserQuestion tool: multiple choice, recommendation first, up to 4 related questions in one call. Never options buried in prose; never a questionnaire.
- Before suggesting a PR, merge or branch action: `python3 .claude/agent-kit/repo_state.py`. Already done → say it is done.
- Keep an internal **agenda** (goal, approved items, pending decisions, parking lot for ideas that came up). Show it only when asked or when it changes.
- Feedback ("ficou estranho", "não gostei") → reproduce/observe first, then propose the smallest change; never guess silently.
- Before any write: the approval gate. After each step: one line of result + evidence.
- When the owner drifts to a new topic: park it ("anotei X para depois") unless they say it is now.
- Teach while working, briefly: one sentence of *why* when a decision matters, never a lecture.

## Closing
- Replace the handoff; list AUTOMATED vs PHYSICAL tests; one line "next session starts with: …".
- Usage high or tool switch → offer `baton-pass`.

## Never
Ask the owner to write a prompt, paste a template, or repeat context that is in the repository.
