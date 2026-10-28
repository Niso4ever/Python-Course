"""
CHEATSHEET L01 — From Loop to SDK
The Agent SDK in 5 patterns.
"""

# ── 1. MINIMAL SDK AGENT ─────────────────────────────────────────────────────
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def run(task: str) -> str:
    async for msg in query(prompt=task, options=ClaudeAgentOptions()):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

# result = asyncio.run(run("What is RAG?"))

# ── 2. WITH SYSTEM PROMPT + MODEL ────────────────────────────────────────────
options = ClaudeAgentOptions(
    model="claude-sonnet-5-5",
    system_prompt="You are a concise AI tutor. Answer in 2 sentences max.",
)
# async for msg in query(prompt="What is RAG?", options=options): ...

# ── 3. COLLECT ALL MESSAGES ──────────────────────────────────────────────────
async def run_verbose(task: str) -> list:
    messages = []
    async for msg in query(prompt=task, options=ClaudeAgentOptions()):
        messages.append(msg)
    return messages
# SystemMessage, AssistantMessage (TextBlock / ToolUseBlock inside),
# UserMessage (ToolResultBlock inside), ResultMessage. There is no ToolUseMessage class.

# ── 4. WHAT THE SDK HIDES (vs. Phase 4 raw API) ──────────────────────────────
# SDK handles:                  You still control:
#   while True loop               model selection
#   stop_reason check             system prompt
#   tool dispatch                 tool definitions
#   messages.append()             task / user input
#   max iteration guard           response parsing (ResultMessage)

# ── 5. FULL ASYNC PATTERN ────────────────────────────────────────────────────
async def main() -> None:
    result = await run("Explain the agent loop in one sentence.")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
# Note: requires ANTHROPIC_API_KEY in environment or use the template (DEMO_MODE)
