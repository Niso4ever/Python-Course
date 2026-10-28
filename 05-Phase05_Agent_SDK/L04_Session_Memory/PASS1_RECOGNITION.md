# L04 — Pass 1: RECOGNITION
## Learn to SEE Session Memory Patterns

**Goal:** When you see session-based code, instantly recognize how sessions are created, captured, and reused — without writing a single line.

> **2026 Note:** Session memory is the SDK's answer to the manual `messages.append()` pattern from Phase 4. Instead of you building and passing a growing message list, the SDK saves it to a session file on local disk and you return to it with `resume=session_id`. Same concept, less code.

---

## The Three Shapes of Session Memory

### Shape 1: Capturing session_id on First Turn
```python
async for msg in query(prompt="first message", options=ClaudeAgentOptions()):
    if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
        session_id = getattr(msg, "session_id", None)
```
**Recognize:** `ResultMessage` arrives last and always carries `session_id` (even on an error result). In Python the early `SystemMessage` keeps the ID nested inside `msg.data`, so read it from `ResultMessage`. `getattr` is a safe accessor — it won't crash if the attribute is absent.

### Shape 2: Resuming a Session
```python
options = ClaudeAgentOptions(resume=session_id)
async for msg in query(prompt="follow-up", options=options):
    ...
```
**Recognize:** `resume=session_id` inside `ClaudeAgentOptions` is the only difference from a fresh call. The SDK loads the full conversation history automatically.

### Shape 3: Stateless vs. Stateful Pattern
```python
# Stateless — no memory
query(prompt="What is my name?", options=ClaudeAgentOptions())

# Stateful — remembers previous turns
query(prompt="What is my name?", options=ClaudeAgentOptions(resume=saved_id))
```
**Recognize:** One line changes the entire behavior. The `session_id` is the memory switch.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: First Turn — Capture the session_id
```python
session_id: str | None = None

async for msg in query(prompt="My name is Ahmed", options=ClaudeAgentOptions()):
    if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
        session_id = getattr(msg, "session_id", session_id)
    if isinstance(msg, ResultMessage):
        print(msg.result)

print(f"Session: {session_id}")   # → "ses_abc123..."
```
**Recognize:** Session capture pattern — read `session_id` from the `ResultMessage`, the same message that carries the answer. Save `session_id` in a variable that persists between turns.

---

### Example 2: Second Turn — Resume the Session
```python
# session_id captured in Example 1
options = ClaudeAgentOptions(resume=session_id)

async for msg in query(prompt="What is my name?", options=options):
    if isinstance(msg, ResultMessage):
        print(msg.result)   # → "Your name is Ahmed."
```
**Recognize:** Same code structure as turn 1, only `resume=session_id` is added. The SDK carries the history.

---

### Example 3: Stateful Chat Function
```python
async def chat(message: str, state: ConversationState) -> str:
    options = ClaudeAgentOptions(resume=state.session_id)
    async for msg in query(prompt=message, options=options):
        if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
            state.session_id = getattr(msg, "session_id", state.session_id)
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""
```
**Recognize:** `ConversationState` is a dataclass holding `session_id`. Passed by reference so updates persist between calls. The `state.session_id` starts as `None` (first turn) and gets filled on first response.

---

### Example 4: Multi-Turn Loop
```python
session_id: str | None = None
turns = ["My name is Ahmed", "I work in AI", "What do you know about me?"]

for turn in turns:
    opts = ClaudeAgentOptions(resume=session_id)
    async for msg in query(prompt=turn, options=opts):
        if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
            session_id = getattr(msg, "session_id", session_id)
        if isinstance(msg, ResultMessage):
            print(f"Turn {turns.index(turn)+1}: {msg.result[:60]}...")
```
**Recognize:** Same `session_id` variable reused in every loop iteration. Gets set on turn 1, reused on turns 2 and 3. Pattern: `session_id = None` → first turn sets it → subsequent turns reuse it.

---

### Example 5: Session Reset (Start Fresh)
```python
# End of conversation — start a new session
session_id = None

# Next turn creates a new session
async for msg in query(prompt="Hello, I'm a new user", options=ClaudeAgentOptions()):
    if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
        session_id = getattr(msg, "session_id", None)   # new session_id
```
**Recognize:** Setting `session_id = None` resets the conversation. Next `query()` call gets a fresh session. Use for new users, new topics, or clearing context.

---

### Example 6: Multiple Concurrent Sessions (Different Users)
```python
user_sessions: dict[str, str | None] = {
    "user_1": None,
    "user_2": None,
}

async def chat_for_user(user_id: str, message: str) -> str:
    opts = ClaudeAgentOptions(resume=user_sessions[user_id])
    async for msg in query(prompt=message, options=opts):
        if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
            user_sessions[user_id] = getattr(msg, "session_id", user_sessions[user_id])
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""
```
**Recognize:** One `session_id` per user. Each user maintains independent conversation history. This is the multi-tenant chat pattern.

---

### Example 7: Session Memory vs Phase 4 Manual History
```python
# Phase 4 — you maintain the message list manually
messages = [{"role": "user", "content": "My name is Ahmed"}]
response = client.messages.create(messages=messages)
messages.append({"role": "assistant", "content": response.content[0].text})
messages.append({"role": "user", "content": "What is my name?"})

# Agent SDK — session_id handles it
opts = ClaudeAgentOptions(resume=session_id)
async for msg in query(prompt="What is my name?", options=opts):
    ...
```
**Recognize:** Phase 4 = you build and pass messages every call. SDK = you pass `session_id` and the SDK loads history. Same outcome, very different code.

---

### Example 8: Context Limit Approaching (Sliding Window Signal)
```python
with client.messages.create(model=..., messages=history) as resp:
    ...
# ValueError: "context_length_exceeded" or similar

# Solution: summarize old turns
if len(history) > 40:
    summary = summarize_history(history[:-10])
    history = [{"role": "user", "content": f"Previous context: {summary}"}] + history[-10:]
```
**Recognize:** When session grows long, context limits become a real issue. The fix: compress old turns into a summary message. Spot this pattern in production code managing long conversations.
