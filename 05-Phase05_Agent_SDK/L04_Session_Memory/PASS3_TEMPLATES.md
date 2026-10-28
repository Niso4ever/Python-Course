# L04 — Pass 3: TEMPLATES
## Your Session Memory Copy-Paste Library

**Goal:** Five session memory patterns. Copy, configure the system prompt, run.

> **2026 Note:** Session memory is what separates a chatbot from a tool. Without sessions, every call is stateless — cheap but forgetful. With sessions, context builds across turns — richer but more expensive. Choose based on your use case.

---

## Template 1: Two-Turn Conversation (Minimal)
**Use when:** Testing that session memory works, learning the pattern

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage

async def two_turn_demo() -> None:
    session_id: str | None = None

    # Turn 1
    async for msg in query(prompt="My name is Ahmed", options=ClaudeAgentOptions()):
        if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
            session_id = getattr(msg, "session_id", session_id)
        if isinstance(msg, ResultMessage):
            print(f"Turn 1: {msg.result}")

    # Turn 2 — uses session_id to remember turn 1
    async for msg in query(prompt="What is my name?",
                           options=ClaudeAgentOptions(resume=session_id)):
        if isinstance(msg, ResultMessage):
            print(f"Turn 2: {msg.result}")
            # → "Your name is Ahmed."

asyncio.run(two_turn_demo())
```

---

## Template 2: Stateful Chat Function
**Use when:** Building a reusable chat component with persistent state

```python
import asyncio
from dataclasses import dataclass
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage

@dataclass
class ChatState:
    session_id: str | None = None
    turn_count: int = 0

async def chat(message: str, state: ChatState, system: str = "") -> str:
    """Send one message, update state, return response.

    Args:
        message: User's message for this turn.
        state: Mutable state object (session_id persists across calls).
        system: Optional system prompt (only used on first turn).

    Returns:
        Agent's response as a string.
    """
    state.turn_count += 1
    options = ClaudeAgentOptions(resume=state.session_id, system_prompt=system)

    async for msg in query(prompt=message, options=options):
        if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
            state.session_id = getattr(msg, "session_id", state.session_id)
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

# Usage:
async def main() -> None:
    state = ChatState()
    system = "You are a helpful assistant with a good memory."
    print(await chat("My name is Ahmed", state, system))
    print(await chat("I am an AI Architect", state))
    print(await chat("What do you know about me?", state))

asyncio.run(main())
```

---

## Template 3: Multi-User Session Manager
**Use when:** Web app serving multiple users, each with their own conversation

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage

class SessionManager:
    """Manage independent sessions for multiple users."""

    def __init__(self) -> None:
        self._sessions: dict[str, str | None] = {}

    async def chat(self, user_id: str, message: str) -> str:
        """Send a message for a specific user's session.

        Args:
            user_id: Unique identifier for this user.
            message: The user's message.

        Returns:
            Agent's response.
        """
        session_id = self._sessions.get(user_id)
        options = ClaudeAgentOptions(resume=session_id)

        async for msg in query(prompt=message, options=options):
            if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
                self._sessions[user_id] = getattr(msg, "session_id", session_id)
            if isinstance(msg, ResultMessage):
                return msg.result
        return ""

    def reset(self, user_id: str) -> None:
        """Clear a user's session (start fresh)."""
        self._sessions.pop(user_id, None)

# Usage:
async def main() -> None:
    mgr = SessionManager()
    print(await mgr.chat("user_1", "My name is Ahmed"))
    print(await mgr.chat("user_2", "My name is Sara"))
    print(await mgr.chat("user_1", "What is my name?"))   # → "Ahmed"
    print(await mgr.chat("user_2", "What is my name?"))   # → "Sara"

asyncio.run(main())
```

---

## Template 4: Session With Sliding Window (Long Conversations)
**Use when:** Conversations expected to exceed 30–50 turns (context limit protection)

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

MAX_TURNS_BEFORE_SUMMARY = 20

async def summarize_context(history_text: str) -> str:
    """Compress conversation history into a brief summary."""
    prompt = f"Summarize this conversation in 3 bullet points:\n\n{history_text}"
    async for msg in query(prompt=prompt, options=ClaudeAgentOptions()):
        if isinstance(msg, ResultMessage):
            return msg.result
    return history_text[:500]

async def chat_with_sliding_window(message: str, state: dict) -> str:
    """Chat with automatic context compression at the turn limit.

    state dict keys: 'session_id', 'turn_count', 'history_text'
    """
    state["turn_count"] = state.get("turn_count", 0) + 1
    state.setdefault("history_text", "")

    # Compress when approaching context limit
    if state["turn_count"] % MAX_TURNS_BEFORE_SUMMARY == 0:
        summary = await summarize_context(state["history_text"])
        # Start fresh session with summary as context
        state["session_id"] = None
        message = f"[Context summary: {summary}]\n\nUser: {message}"

    options = ClaudeAgentOptions(resume=state.get("session_id"))
    async for msg in query(prompt=message, options=options):
        if hasattr(msg, "session_id"):
            state["session_id"] = getattr(msg, "session_id", state.get("session_id"))
        if isinstance(msg, ResultMessage):
            state["history_text"] += f"\nUser: {message}\nAgent: {msg.result}"
            return msg.result
    return ""
```

---

## Template 5: Session Reset + Restart
**Use when:** End of conversation, new topic, or explicit "forget everything" request

```python
import asyncio
from dataclasses import dataclass, field
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage

@dataclass
class ResettableChat:
    system_prompt: str = "You are a helpful assistant."
    session_id: str | None = None
    turn_count: int = 0
    history: list[str] = field(default_factory=list)

    def reset(self) -> None:
        """Start a completely fresh conversation."""
        self.session_id = None
        self.turn_count = 0
        self.history.clear()
        print("[Session reset — starting fresh]")

    async def send(self, message: str) -> str:
        self.turn_count += 1
        options = ClaudeAgentOptions(
            resume=self.session_id,
            system_prompt=self.system_prompt
        )
        async for msg in query(prompt=message, options=options):
            if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
                self.session_id = getattr(msg, "session_id", self.session_id)
            if isinstance(msg, ResultMessage):
                self.history.append(f"User: {message}\nAgent: {msg.result}")
                return msg.result
        return ""

# Usage:
async def main() -> None:
    chat = ResettableChat()
    print(await chat.send("My name is Ahmed"))
    print(await chat.send("What is my name?"))   # → "Ahmed"
    chat.reset()
    print(await chat.send("What is my name?"))   # → "I don't know"

asyncio.run(main())
```

---

## Quick Selection Guide

| Need | Template |
|------|----------|
| Learning / testing sessions | Template 1: Two-Turn Demo |
| Reusable chat component | Template 2: Stateful Chat |
| Multi-user web app | Template 3: Session Manager |
| Very long conversations | Template 4: Sliding Window |
| Need to restart mid-conversation | Template 5: Reset + Restart |
