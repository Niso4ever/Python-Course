"""
TEMPLATE: Session Memory Agent
CURRICULUM PATTERN: Ph5-L04
DESCRIPTION: Links query() calls into a multi-turn conversation via session_id.
             DEMO_MODE simulates session state with a local dict.
Run with: python template_session_memory.py
"""

import asyncio
from dataclasses import dataclass, field

DEMO_MODE = True

# ──────────────────────────────────────────────
# DEMO SESSION STORE
# ──────────────────────────────────────────────

_demo_sessions: dict[str, list[dict]] = {}

def _demo_turn(session_id: str | None, message: str) -> tuple[str, str]:
    """Simulate a multi-turn conversation with local history.

    Returns:
        Tuple of (new_or_existing_session_id, response_text).
    """
    sid = session_id or f"ses_demo_{len(_demo_sessions) + 1:03d}"
    if sid not in _demo_sessions:
        _demo_sessions[sid] = []

    history = _demo_sessions[sid]
    history.append({"role": "user", "content": message})

    # Build a context-aware demo response
    all_user_msgs = [m["content"] for m in history if m["role"] == "user"]
    response = _generate_demo_response(message, all_user_msgs)

    history.append({"role": "assistant", "content": response})
    return sid, response


def _generate_demo_response(current: str, history: list[str]) -> str:
    """Generate a demo response that shows context awareness."""
    c = current.lower()

    if "name" in c and len(history) == 1:
        name = current.split()[-1].rstrip(".")
        return f"Hello {name}! Nice to meet you."

    if "name" in c and "what" in c:
        for msg in history:
            words = msg.split()
            for i, w in enumerate(words):
                if w.lower() in ("is", "am") and i + 1 < len(words):
                    return f"Your name is {words[i + 1].rstrip('.')}."
        return "I don't have your name yet. What is your name?"

    if "role" in c or "architect" in c or "do" in c:
        return "You mentioned you are an AI Architect. That's a great role for 2026!"

    if "remember" in c or "know" in c or "tell" in c or "summarize" in c:
        facts = [m for m in history[:-1] if m != current]
        if facts:
            return f"From our conversation, I know: {'; '.join(facts[:3])}."
        return "We just started talking — I don't have much context yet."

    return f"[DEMO turn {len(history)}] Received: '{current}'. Context has {len(history)} messages."


# ──────────────────────────────────────────────
# SESSION AGENT
# ──────────────────────────────────────────────

@dataclass
class ConversationState:
    session_id: str | None = None
    turn_count: int = 0
    history: list[dict] = field(default_factory=list)


async def chat(message: str, state: ConversationState) -> str:
    """Send one message in a conversation, maintaining session state.

    Args:
        message: The user's message for this turn.
        state: Mutable conversation state (session_id, turn_count, history).

    Returns:
        The agent's response for this turn.
    """
    state.turn_count += 1

    if DEMO_MODE:
        state.session_id, response = _demo_turn(state.session_id, message)
        state.history.append({"role": "user", "content": message})
        state.history.append({"role": "assistant", "content": response})
        return response

    # Real SDK call
    from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage  # type: ignore

    options = ClaudeAgentOptions(
        model="claude-sonnet-5-5",
        resume=state.session_id,
    )
    async for msg in query(prompt=message, options=options):
        if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
            state.session_id = getattr(msg, "session_id", state.session_id)
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""


# ──────────────────────────────────────────────
# DEMO
# ──────────────────────────────────────────────

async def main() -> None:
    print("Session Memory Agent Demo")
    print("=" * 50)
    print("3 turns — each turn builds on the previous.\n")

    state = ConversationState()

    turns = [
        "My name is Ahmed",
        "I am an AI Architect",
        "What do you remember about me?",
    ]

    for turn in turns:
        print(f"Turn {state.turn_count + 1}")
        print(f"  You:   {turn}")
        response = await chat(turn, state)
        print(f"  Agent: {response}")
        print(f"  [session_id: {state.session_id}]")
        print()

    print(f"Total turns: {state.turn_count}")
    print(f"Session preserved across all {state.turn_count} calls via session_id")
    print(f"\n[{'DEMO' if DEMO_MODE else 'REAL API'} MODE]")


if __name__ == "__main__":
    asyncio.run(main())
