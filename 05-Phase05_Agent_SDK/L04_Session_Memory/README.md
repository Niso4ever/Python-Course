# L04 — Session Memory

> **Metaphor:** Each `query()` call without a session_id is like calling a stranger.
> With a session_id, it's like calling a colleague who remembers your last conversation.

---

## The Shift

Each `query()` is stateless by default — fresh context every time:

```python
# Call 1 — no memory
async for msg in query(prompt="My name is Ahmed"):
    ...

# Call 2 — no memory of call 1
async for msg in query(prompt="What is my name?"):
    ...   # → "I don't know your name"
```

With `session_id` — the SDK links calls:

```python
session_id = None

# Call 1 — capture the session
async for msg in query(prompt="My name is Ahmed", options=ClaudeAgentOptions()):
    if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
        session_id = getattr(msg, 'session_id', session_id)

# Call 2 — resume the session
async for msg in query(prompt="What is my name?",
                       options=ClaudeAgentOptions(resume=session_id)):
    ...   # → "Your name is Ahmed"
```

---

## What session_id Does

Passing the captured ID as `resume=session_id` tells the SDK to load the conversation history from that session.
The SDK keeps the message list in a session file on local disk (under `~/.claude/projects/`) — you don't pass `messages=` manually.

> **Two option names, two jobs (checked 2026-10-28):** `resume=` continues an existing session. `session_id=` in `ClaudeAgentOptions` does something else: it assigns a chosen UUID to a *new* session. Earlier versions of this lesson used `session_id=` to resume; that was wrong. For a single-process chat, `ClaudeSDKClient` tracks the session for you with no ID handling.

This is the SDK equivalent of Phase 4's manual `messages.append()` pattern — but you don't write it.

---

## When to Use vs. Not Use

| Use session memory | Use stateless calls |
|-------------------|---------------------|
| Multi-turn chatbots | Single-question tools |
| Conversations that build context | Parallel independent tasks |
| User preferences that persist | Batch processing |
| Debugging sessions | Cheap, fast one-shot queries |

---

## Architect's Question

> "Does my agent need to remember what happened 3 turns ago to answer correctly now?
> If yes, use session_id. If every question is independent, stateless is cheaper and simpler."
