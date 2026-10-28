"""
TEMPLATE: First SDK Agent
CURRICULUM PATTERN: Ph5-L01
DESCRIPTION: The simplest complete Anthropic Agent SDK agent.
             Shows the shift from Phase 4's raw while-loop to query().
Run with: python template_first_sdk_agent.py
"""

import asyncio
from dataclasses import dataclass

DEMO_MODE = True  # Set False + add ANTHROPIC_API_KEY for real calls

# ──────────────────────────────────────────────
# DEMO SIMULATION (no API key needed)
# ──────────────────────────────────────────────

DEMO_RESPONSES: dict[str, str] = {
    "what is rag":
        "RAG (Retrieval-Augmented Generation) combines a retrieval system with an LLM "
        "to ground responses in real documents, reducing hallucinations.",
    "what is the agent loop":
        "The agent loop is: LLM decides → tool executes → result feeds back → repeat. "
        "It runs until the LLM has enough information to answer.",
    "what is mcp":
        "MCP (Model Context Protocol) is Anthropic's 2024 open standard for connecting "
        "AI models to external tools and data sources universally.",
}

def _demo_query(task: str) -> str:
    key = task.lower().strip().rstrip("?")
    for q, answer in DEMO_RESPONSES.items():
        if any(word in key for word in q.split()):
            return answer
    return f"[DEMO] Simulated answer for: '{task}'"


# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────

@dataclass
class AgentConfig:
    model: str = "claude-sonnet-5-5"
    system_prompt: str = "You are a concise AI tutor. Answer in 2–3 sentences."
    max_tokens: int = 512


# ──────────────────────────────────────────────
# AGENT RUNNER
# ──────────────────────────────────────────────

async def run_sdk_agent(task: str, config: AgentConfig) -> str:
    """Run a single task through the Agent SDK and return the result.

    Args:
        task: The question or instruction for the agent.
        config: Agent configuration (model, system prompt, max tokens).

    Returns:
        The agent's final answer as a string.
    """
    if DEMO_MODE:
        return _demo_query(task)

    # Real SDK call (requires claude-agent-sdk installed + ANTHROPIC_API_KEY)
    from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage  # type: ignore

    options = ClaudeAgentOptions(
        model=config.model,
        system_prompt=config.system_prompt,
    )
    async for message in query(prompt=task, options=options):
        from claude_agent_sdk import ResultMessage as RM  # type: ignore
        if isinstance(message, RM):
            return message.result

    return ""


# ──────────────────────────────────────────────
# COMPARISON: RAW LOOP vs SDK
# ──────────────────────────────────────────────

def show_comparison() -> None:
    """Print a side-by-side of what the SDK replaces."""
    print("=" * 60)
    print("WHAT THE SDK HIDES vs. WHAT YOU STILL CONTROL")
    print("=" * 60)
    print()
    print("  HIDDEN BY SDK            STILL YOURS")
    print("  ─────────────────────    ─────────────────────")
    print("  while True loop          model selection")
    print("  stop_reason check        system prompt")
    print("  tool dispatch            tool definitions")
    print("  messages.append()        task / user input")
    print("  max iteration guard      response parsing")
    print()
    print("Phase 4 = you assembled the engine.")
    print("Agent SDK = you drive the finished car.")
    print()


# ──────────────────────────────────────────────
# DEMO
# ──────────────────────────────────────────────

async def main() -> None:
    config = AgentConfig()
    show_comparison()

    tasks = [
        "What is RAG?",
        "What is the agent loop?",
        "What is MCP?",
    ]

    print("Running 3 tasks through the Agent SDK...\n")
    for task in tasks:
        print(f"Task: {task}")
        result = await run_sdk_agent(task, config)
        print(f"Answer: {result}")
        print()

    mode = "DEMO" if DEMO_MODE else "REAL API"
    print(f"[{mode} MODE — set DEMO_MODE=False for real Anthropic calls]")


if __name__ == "__main__":
    asyncio.run(main())
