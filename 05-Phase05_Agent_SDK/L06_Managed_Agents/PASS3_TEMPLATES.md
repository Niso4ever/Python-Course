# L06 — Pass 3: TEMPLATES
## Your Managed Agents Copy-Paste Library

**Goal:** Five Managed Agents patterns. Copy, replace the system prompt and task, run.

> **2026 Note:** In production, Steps 1 and 2 (agent + environment creation) run ONCE at setup time. Only Step 3 (session) runs per request. These templates show both the setup and the per-request patterns clearly separated.

> **Correction (2026-10-28):** Where an example below streams with `session.stream(input=...)` and checks
> `session_start` / `text_delta` / `tool_call` / `session_complete` or `event.text`, that event model does not exist.
> The real loop opens `client.beta.sessions.events.stream(session.id)`, sends the task with
> `client.beta.sessions.events.send(session.id, events=[{"type": "user.message", "content": [{"type": "text", "text": task}]}])`,
> and reads `agent.message` (text in `event.content` blocks), `agent.tool_use`, and `session.status_idle` (finished).
> See the code block in `README.md` and `template_managed_agent.py`. Source: platform.claude.com/docs/en/managed-agents/quickstart.

---

## Template 1: Minimal Three-Step (Learning)
**Use when:** Understanding the pattern, first time running Managed Agents

```python
import anthropic

DEMO_MODE = True
BETA = "managed-agents-2026-04-01"

def run_managed_agent(task: str) -> str:
    """Complete three-step Managed Agents pattern in one function."""
    if DEMO_MODE:
        return f"[DEMO] Managed agent response for: '{task}'"

    client = anthropic.Anthropic()

    # Step 1: Define agent (do once)
    agent = client.beta.agents.create(
        name="Assistant",
        model={"id": "claude-sonnet-5-5"},
        system="You are a helpful assistant.",
        betas=[BETA]
    )

    # Step 2: Create environment (do once)
    env = client.beta.environments.create(name="research-env")

    # Step 3: Run session (each conversation)
    session = client.beta.sessions.create(agent=agent.id, environment_id=env.id)
    result = ""
    for event in session.stream(input=task):
        if hasattr(event, "text"):
            result += event.text
    return result

# Call:
print(run_managed_agent("Summarize AI trends in 2026"))
```

---

## Template 2: Production Pattern (Reuse IDs)
**Use when:** Real deployment — agent and environment already created, just run sessions

```python
import os, anthropic

# These are set at deploy time — never recreated per request
AGENT_ID = os.getenv("MANAGED_AGENT_ID", "agt_your_agent_id")
ENV_ID   = os.getenv("MANAGED_ENV_ID",   "env_your_env_id")
BETA     = "managed-agents-2026-04-01"

client = anthropic.Anthropic()

def run_session(task: str, verbose: bool = False) -> str:
    """Run one session using pre-created agent and environment.

    Args:
        task: The instruction or question to send to the agent.
        verbose: If True, print events as they arrive.

    Returns:
        Complete agent response as a string.
    """
    session = client.beta.sessions.create(
        agent=AGENT_ID,   
        environment_id=ENV_ID
    )
    result = ""
    for event in session.stream(input=task):
        if hasattr(event, "text") and event.text:
            if verbose:
                print(event.text, end="", flush=True)
            result += event.text
    if verbose:
        print()
    return result

# Call (agent and env IDs come from env vars):
answer = run_session("Research quantum error correction advances", verbose=True)
print(f"\nTotal: {len(answer)} chars")
```

---

## Template 3: Setup Script (Run Once)
**Use when:** First-time deployment — create agent and environment, save IDs

```python
import anthropic, json, os
from pathlib import Path

BETA = "managed-agents-2026-04-01"

def setup_managed_agent(
    name: str,
    model_id: str,
    system_prompt: str,
    save_path: str = ".managed_agent_ids.json"
) -> dict:
    """Create agent + environment once. Save IDs for reuse.

    Args:
        name: Human-readable agent name.
        model_id: Anthropic model ID to use.
        system_prompt: The agent's system instructions.
        save_path: Where to save the IDs for later use.

    Returns:
        Dict with 'agent_id' and 'env_id'.
    """
    client = anthropic.Anthropic()

    print(f"Creating agent '{name}'...")
    agent = client.beta.agents.create(
        name=name, model={"id": model_id}, system=system_prompt, betas=[BETA]
    )
    print(f"  ✓ agent_id = {agent.id}")

    print("Creating environment...")
    env = client.beta.environments.create(name="research-env")
    print(f"  ✓ env_id   = {env.id}")

    ids = {"agent_id": agent.id, "env_id": env.id}
    Path(save_path).write_text(json.dumps(ids, indent=2))
    print(f"  ✓ Saved to {save_path}")
    return ids

# Run ONCE at setup:
# ids = setup_managed_agent(
#     name="Research Assistant",
#     model_id="claude-sonnet-5-5",
#     system_prompt="You are a research assistant. Be accurate and cite sources."
# )
# Then set: MANAGED_AGENT_ID=ids["agent_id"], MANAGED_ENV_ID=ids["env_id"]
```

---

## Template 4: Session With Event Handling
**Use when:** You need to handle different event types (text, tools, errors) explicitly

```python
import anthropic
from dataclasses import dataclass, field

BETA = "managed-agents-2026-04-01"

@dataclass
class SessionResult:
    text: str = ""
    tool_calls: list[str] = field(default_factory=list)
    event_count: int = 0
    completed: bool = False

def run_session_verbose(task: str, agent_id: str, env_id: str) -> SessionResult:
    """Run session and capture all event types.

    Args:
        task: The task to send to the managed agent.
        agent_id: Pre-created agent ID.
        env_id: Pre-created environment ID.

    Returns:
        SessionResult with text, tool_calls, and completion status.
    """
    client = anthropic.Anthropic()
    result = SessionResult()

    session = client.beta.sessions.create(agent=agent_id, environment_id=env_id)

    for event in session.stream(input=task):
        result.event_count += 1

        etype = getattr(event, "event_type", "")
        if etype == "session_start":
            print("  Agent started...")
        elif etype == "text_delta" and hasattr(event, "text"):
            print(event.text, end="", flush=True)
            result.text += event.text
        elif etype == "tool_call":
            tool_name = getattr(event, "tool_name", "unknown")
            result.tool_calls.append(tool_name)
            print(f"\n  [Tool: {tool_name}]")
        elif etype == "session_complete":
            result.completed = True
            print("\n  Session complete.")

    return result

# Call:
# r = run_session_verbose("Research MCP protocol", AGENT_ID, ENV_ID)
# print(f"Tools called: {r.tool_calls}, Events: {r.event_count}")
```

---

## Template 5: Compare All Three Tiers
**Use when:** Teaching, documentation, or choosing between tiers for a project

```python
import asyncio, anthropic
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

TASK = "What is RAG? Answer in one sentence."
DEMO = True  # set False + add keys for real calls

# TIER 1: Raw API — you write the loop
def tier1_raw(task: str) -> str:
    if DEMO: return "[DEMO Tier 1] Raw API response."
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-5-5", max_tokens=256,
        messages=[{"role": "user", "content": task}]
    )
    return response.content[0].text

# TIER 2: Agent SDK — SDK handles the loop
async def tier2_sdk(task: str) -> str:
    if DEMO: return "[DEMO Tier 2] Agent SDK response."
    async for msg in query(prompt=task, options=ClaudeAgentOptions()):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

# TIER 3: Managed Agents — Anthropic runs the loop
def tier3_managed(task: str, agent_id: str, env_id: str) -> str:
    if DEMO: return "[DEMO Tier 3] Managed Agent response."
    client = anthropic.Anthropic()
    session = client.beta.sessions.create(agent=agent_id, environment_id=env_id)
    result = ""
    for event in session.stream(input=task):
        if hasattr(event, "text"):
            result += event.text
    return result

async def compare_tiers() -> None:
    print("TIER 1 (Raw API):")
    print(f"  {tier1_raw(TASK)}\n")
    print("TIER 2 (Agent SDK):")
    print(f"  {await tier2_sdk(TASK)}\n")
    print("TIER 3 (Managed Agents):")
    print(f"  {tier3_managed(TASK, 'agt_demo', 'env_demo')}\n")

asyncio.run(compare_tiers())
```

---

## Quick Selection Guide

| Need | Template |
|------|----------|
| First time / learning | Template 1: Minimal Three-Step |
| Production deployment | Template 2: Reuse IDs |
| First-time setup | Template 3: Setup Script |
| Full event visibility | Template 4: Event Handling |
| Choosing between tiers | Template 5: Compare All Three |

---

## Managed Agents Checklist

Before going live with Managed Agents:
- [ ] `ANTHROPIC_API_KEY` set in environment
- [ ] Beta header included: `betas=["managed-agents-2026-04-01"]`
- [ ] Agent ID and Environment ID saved — not recreated per request
- [ ] Event stream iterated completely before returning
- [ ] `session_complete` event handled (confirms agent finished)
