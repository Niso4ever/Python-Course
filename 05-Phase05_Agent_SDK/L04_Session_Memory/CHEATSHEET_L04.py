"""
CHEATSHEET L04 — Session Memory
Link query() calls into a conversation.
"""
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage

# ── 1. FIRST CALL — capture session_id ───────────────────────────────────────
session_id: str | None = None

async def first_turn(message: str) -> str:
    global session_id
    async for msg in query(prompt=message, options=ClaudeAgentOptions()):
        if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
            session_id = getattr(msg, "session_id", session_id)
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

# ── 2. FOLLOW-UP — reuse session_id ─────────────────────────────────────────
async def follow_up(message: str) -> str:
    options = ClaudeAgentOptions(resume=session_id)
    async for msg in query(prompt=message, options=options):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

# ── 3. MULTI-TURN CHAT LOOP ──────────────────────────────────────────────────
async def chat_loop() -> None:
    session: str | None = None
    turns = [
        "My name is Ahmed",
        "I am an AI Architect",
        "Summarize what you know about me",
    ]
    for turn in turns:
        opts = ClaudeAgentOptions(resume=session)
        async for msg in query(prompt=turn, options=opts):
            if isinstance(msg, ResultMessage):  # session_id is on ResultMessage
                session = getattr(msg, "session_id", session)
            if isinstance(msg, ResultMessage):
                print(f"User: {turn}\nAgent: {msg.result}\n")

# ── 4. SESSION DECISION ──────────────────────────────────────────────────────
# Use session_id:  multi-turn chat, context building, "remember earlier..."
# Skip session_id: single-shot tasks, parallel independent queries, batch jobs

# ── 5. CONTEXT GROWS — SLIDE THE WINDOW ─────────────────────────────────────
# Turn 50+ → context limit approaching
# Solution: summarize old turns before they overflow
# summary = summarize(old_messages)
# ClaudeAgentOptions(system_prompt=f"Previous context: {summary}")
