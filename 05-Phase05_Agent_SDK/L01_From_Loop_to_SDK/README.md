# L01 — From Loop to SDK

> **Metaphor:** Phase 4 taught you to build a car engine from scratch. The Agent SDK is a
> finished car. Same engine inside — you just don't assemble it by hand anymore.

---

## The Shift

Phase 4 (Ph4-L02) made you write every line of the agent loop:

```python
# Phase 4 style — you own everything
while iteration < max_iterations:
    response = client.messages.create(tools=TOOLS, messages=messages)
    if response.stop_reason == "end_turn":
        return response.content[0].text
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": execute_tools(response)})
```

The Agent SDK collapses this to:

```python
# SDK style — same logic, hidden
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async for message in query(prompt="What is RAG?", options=ClaudeAgentOptions()):
    if isinstance(message, ResultMessage):
        print(message.result)
```

The SDK handles: the loop, tool dispatch, message accumulation, retries.
You handle: what tools exist, what the system prompt says, what the task is.

---

## What the SDK Hides vs. What You Still Control

| Hidden by SDK | Still yours |
|---------------|-------------|
| `while True` loop | System prompt |
| `stop_reason` check | Tool definitions |
| Tool execution dispatch | Model selection |
| `messages.append()` | Task / user input |
| Max iteration guard | Response parsing |

---

## When to Use the SDK vs. Raw API

| Use SDK (`claude_agent_sdk`) | Use Raw API (`anthropic`) |
|-----------------------------|--------------------------|
| You want less boilerplate | You need fine-grained loop control |
| Standard tool → execute → loop | Custom message injection mid-loop |
| Prototyping quickly | Debugging exact API behavior |
| Teaching/demos | Phase 4 learning exercises |

---

## Key Imports

```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
import asyncio

options = ClaudeAgentOptions(model="claude-sonnet-5-5", system_prompt="...")
asyncio.run(main())
```

---

## Architect's Question

> "What does my agent need that the loop provides — and can the SDK handle it?
> If yes, use the SDK. If your agent needs to inject custom messages mid-loop, use the raw API."
