# L01 — Pass 3: TEMPLATES
## Your SDK Agent Copy-Paste Library

**Goal:** Five ready-to-use Agent SDK patterns. Copy, configure, run.

> **2026 Note:** All templates use `from claude_agent_sdk import` — Anthropic's official SDK that handles the loop internally. Set `DEMO_MODE = False` and add `ANTHROPIC_API_KEY` for real calls.

---

## How to Use These Templates

1. Pick the template that fits your need
2. Copy it into your project
3. Replace `system_prompt` and `task` with your content
4. Run `asyncio.run(main())`

---

## Template 1: Minimal One-Shot Agent
**Use when:** Simple question, no tools, fastest possible path

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def ask(task: str) -> str:
    async for msg in query(prompt=task, options=ClaudeAgentOptions()):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

# Call:
answer = asyncio.run(ask("What is RAG?"))
print(answer)
# → "RAG (Retrieval-Augmented Generation) combines a retrieval system..."
```

---

## Template 2: Configured Agent (System Prompt + Model)
**Use when:** You need a specific persona, expertise, or output style

```python
import asyncio
from dataclasses import dataclass
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

@dataclass
class AgentConfig:
    model: str = "claude-sonnet-5-5"
    system: str = "You are a concise technical explainer. Use plain English."

async def run(task: str, cfg: AgentConfig) -> str:
    options = ClaudeAgentOptions(model=cfg.model, system_prompt=cfg.system)
    async for msg in query(prompt=task, options=options):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

# Call:
cfg = AgentConfig(system="You are a senior AI architect. Be direct and precise.")
answer = asyncio.run(run("Explain the agent loop", cfg))
print(answer)
```

---

## Template 3: Safe Agent (With Timeout + Error Handling)
**Use when:** Production code — never let an agent call hang or crash silently

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def run_safe(
    task: str,
    system: str = "",
    timeout_s: float = 30.0,
) -> dict:
    """Run agent with timeout and error capture.

    Returns:
        Dict with 'result', 'status' ('ok' | 'timeout' | 'error'), 'error' (if any).
    """
    options = ClaudeAgentOptions(system_prompt=system)

    async def _run() -> str:
        async for msg in query(prompt=task, options=options):
            if isinstance(msg, ResultMessage):
                return msg.result
        return ""

    try:
        result = await asyncio.wait_for(_run(), timeout=timeout_s)
        return {"result": result, "status": "ok", "error": None}
    except asyncio.TimeoutError:
        return {"result": "", "status": "timeout", "error": f"Exceeded {timeout_s}s"}
    except Exception as e:
        return {"result": "", "status": "error", "error": str(e)}

# Call:
response = asyncio.run(run_safe("Summarize AI trends", timeout_s=20.0))
if response["status"] == "ok":
    print(response["result"])
else:
    print(f"Failed: {response['error']}")
```

---

## Template 4: Verbose Agent (All Message Types)
**Use when:** Debugging, learning what the SDK sends back, building observability

```python
import asyncio
from claude_agent_sdk import (
    query, ClaudeAgentOptions,
    SystemMessage, AssistantMessage, ResultMessage
)

async def run_verbose(task: str) -> str:
    options = ClaudeAgentOptions(model="claude-sonnet-5-5")
    result = ""

    async for msg in query(prompt=task, options=options):
        if isinstance(msg, SystemMessage):
            sid = getattr(msg, "session_id", "none")
            print(f"[System] session_id={sid}")
        elif isinstance(msg, AssistantMessage):
            print(f"[Thinking] {str(msg)[:80]}...")
        elif isinstance(msg, ResultMessage):
            result = msg.result
            print(f"[Result] {result[:100]}...")

    return result

# Call:
asyncio.run(run_verbose("Explain MCP in one sentence"))
# → [System] session_id=ses_abc123...
# → [Thinking] ...
# → [Result] MCP (Model Context Protocol) is Anthropic's universal...
```

---

## Template 5: Sync Wrapper (Call SDK from Non-Async Code)
**Use when:** Script, CLI, or existing synchronous codebase that can't use `await`

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

def ask_sync(task: str, system: str = "") -> str:
    """Synchronous wrapper around the async SDK. Safe for script use.

    Args:
        task: The question or instruction for the agent.
        system: Optional system prompt.

    Returns:
        Agent's final answer as a string.
    """
    async def _inner() -> str:
        options = ClaudeAgentOptions(system_prompt=system)
        async for msg in query(prompt=task, options=options):
            if isinstance(msg, ResultMessage):
                return msg.result
        return ""

    return asyncio.run(_inner())

# Call — no async needed:
answer = ask_sync("What is DSPy?", system="Answer in one sentence.")
print(answer)
answer2 = ask_sync("What is Pydantic?")
print(answer2)
```

---

## Quick Selection Guide

| Need | Template |
|------|----------|
| Simple question, no setup | Template 1: Minimal |
| Specific persona or style | Template 2: Configured |
| Production, can't crash | Template 3: Safe |
| Debugging / learning | Template 4: Verbose |
| Non-async script or CLI | Template 5: Sync Wrapper |
