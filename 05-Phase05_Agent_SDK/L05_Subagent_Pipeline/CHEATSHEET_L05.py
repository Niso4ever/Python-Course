"""
CHEATSHEET L05 — Two-Agent Pipeline (Subagents)
Orchestrator delegates to a specialist.
"""
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

# ── 1. ORCHESTRATOR — can spawn subagents ─────────────────────────────────────
orchestrator_options = ClaudeAgentOptions(
    model="claude-sonnet-5-5",
    system_prompt=(
        "You are a research orchestrator. "
        "When given a complex task, use the Agent tool to delegate research "
        "to a specialist, then synthesize the result into a final answer."
    ),
    allowed_tools=["Agent"],   # ← the key permission to spawn subagents
)

# ── 2. SUBAGENT — focused specialist ─────────────────────────────────────────
researcher_options = ClaudeAgentOptions(
    model="claude-haiku-5-5",  # cheaper model for execution work
    system_prompt="You are a research specialist. Find facts and cite sources.",
)

# ── 3. SEQUENTIAL HANDOFF ────────────────────────────────────────────────────
async def research_and_write(topic: str) -> str:
    # Step 1: researcher finds information
    research = ""
    async for msg in query(prompt=f"Research: {topic}", options=researcher_options):
        if isinstance(msg, ResultMessage):
            research = msg.result

    # Step 2: pass research to writer
    async for msg in query(prompt=f"Write a summary using this research:\n{research}",
                           options=ClaudeAgentOptions(model="claude-sonnet-5-5")):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

# ── 4. FOUR PATTERNS ──────────────────────────────────────────────────────────
# Sequential:  A → B → C → result
# Parallel:    A → [B, C, D in parallel] → synthesizer → result
# Router:      A classifies → routes to B or C or D
# Hierarchical: manager → team_lead → workers (enterprise, defer)

# ── 5. MODEL SELECTION RULE ──────────────────────────────────────────────────
# Orchestrator: powerful model (decisions) → claude-opus-5-5 or claude-sonnet-5-5
# Subagent:     fast/cheap model (execution) → claude-haiku-5-5
