# L01 — Visual: Raw Loop vs. Agent SDK

## Side-by-Side Flow

```
RAW API (Phase 4)                        AGENT SDK (this course)
─────────────────────────────────        ──────────────────────────────────
You write:                               You write:

  client = anthropic.Anthropic()           from claude_agent_sdk import query
                                           options = ClaudeAgentOptions(
  TOOLS = [{...schema dict...}]               model="claude-sonnet-5-5",
                                              system_prompt="...",
  messages = [{"role":"user",...}]            allowed_tools=[my_tool]
                                           )
  iteration = 0
  while iteration < max_iter:            async for message in query(prompt=task, options):
      response = client.messages.create(     if isinstance(message, ResultMessage):
          tools=TOOLS,                           print(message.result)
          messages=messages
      )
      if response.stop_reason == "end_turn":
          return response.content[0].text
      tool_results = execute_tools(response)
      messages.append(assistant_msg)
      messages.append(tool_result_msg)
      iteration += 1

↑ You own every line                     ↑ SDK owns the shaded parts
```

---

## What the SDK Abstracts Away

```
┌─────────────────────────────────────────────────────────┐
│                     YOUR CODE                           │
│  task = "What is RAG?"                                  │
│  options = ClaudeAgentOptions(model=..., tools=[...])   │
│  async for msg in query(prompt=task, options): ...      │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│               CLAUDE AGENT SDK  (hidden)                │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  while True:                                    │   │
│  │      response = client.messages.create(...)     │   │
│  │      if stop_reason == "end_turn": break        │   │
│  │      tool_results = execute_tools(response)     │   │
│  │      messages.append(assistant_msg)             │   │
│  │      messages.append(tool_result_msg)           │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
         ResultMessage(result="...")
                   │
                   ▼
           Your code receives it
```

---

## Message Types You'll See

```
async for message in query(prompt=...):
    │
    ├── SystemMessage      ← session start info (Python: details in msg.data)
    ├── AssistantMessage   ← content blocks: TextBlock (text) or ToolUseBlock (tool call)
    ├── UserMessage        ← carries ToolResultBlock (what the tool returned)
    └── ResultMessage      ← ← ← THIS IS THE FINAL ANSWER (+ session_id, total_cost_usd)
```

---

## The Async Pattern

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def run(task: str) -> str:
    async for msg in query(prompt=task, options=ClaudeAgentOptions()):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

result = asyncio.run(run("What is RAG?"))
#        └── bridges sync code → async generator
```
