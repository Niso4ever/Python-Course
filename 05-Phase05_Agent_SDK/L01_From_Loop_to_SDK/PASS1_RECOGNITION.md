# L01 — Pass 1: RECOGNITION
## Learn to SEE the Agent SDK Pattern

**Goal:** When you see Agent SDK code, instantly recognize its structure — whether it's minimal, configured, or verbose — without writing a single line.

> **2026 Note:** The raw `while True` loop (Phase 4) is still running underneath every `query()` call. The SDK is the loop with the boilerplate removed. Once you recognize both forms, you can read any agentic code.

---

## The Three Shapes of the SDK Pattern

### Shape 1: The Import
```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
```
**Recognize:** These three imports together = Agent SDK in use. `query` is the entry point, `ClaudeAgentOptions` is the config, `ResultMessage` is the final output.

### Shape 2: The Async Generator
```python
async for message in query(prompt=task, options=options):
    ...
```
**Recognize:** `async for ... in query(prompt=...)` — this IS the loop. The SDK streams message objects back one by one. You iterate until the one you want arrives.

### Shape 3: The Result Extraction
```python
if isinstance(message, ResultMessage):
    return message.result
```
**Recognize:** Always at the bottom of the loop body. `ResultMessage` = final answer. Everything before it is metadata, tool events, or intermediate text.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: The Absolute Minimum
```python
import asyncio
from claude_agent_sdk import query, ResultMessage

async def ask(task: str) -> str:
    async for msg in query(prompt=task):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""
```
**Recognize:** No options, no config. Pure skeleton. `query(prompt=task)` uses defaults. Three lines of loop body.

---

### Example 2: With Model + System Prompt
```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

options = ClaudeAgentOptions(
    model="claude-sonnet-5-5",
    system_prompt="You are a concise tutor. Answer in 2 sentences.",
)
async for msg in query(prompt="What is RAG?", options=options):
    if isinstance(msg, ResultMessage):
        print(msg.result)
```
**Recognize:** `ClaudeAgentOptions` always takes `model=` and `system_prompt=`. These are the two knobs you turn most often.

---

### Example 3: Collecting All Message Types
```python
async for msg in query(prompt="Explain MCP", options=options):
    if isinstance(msg, SystemMessage):
        print(f"System: {msg}")          # session info, session_id
    elif isinstance(msg, AssistantMessage):
        for block in msg.content:        # TextBlock or ToolUseBlock
            if isinstance(block, ToolUseBlock):
                print(f"Tool called: {block.name}")   # agent called a tool
            elif isinstance(block, TextBlock):
                print(f"Text: {block.text}")          # intermediate text
    elif isinstance(msg, ResultMessage):
        print(f"Final: {msg.result}")    # ← the answer
```
**Recognize:** Three message types here (`UserMessage`, which carries `ToolResultBlock`s, is a fourth). A tool call is not its own message type: it is a `ToolUseBlock` inside an `AssistantMessage`. In practice you only need `ResultMessage`. The others are useful for debugging.

---

### Example 4: The asyncio.run() Entry Point
```python
async def main() -> None:
    result = ""
    async for msg in query(prompt="What is the agent loop?", options=ClaudeAgentOptions()):
        if isinstance(msg, ResultMessage):
            result = msg.result
    print(result)

asyncio.run(main())
```
**Recognize:** `asyncio.run(main())` at the bottom = standard Python async entry point. Every SDK script ends with this pattern.

---

### Example 5: Wrapped as a Synchronous Function
```python
def ask_sync(task: str, system: str = "") -> str:
    options = ClaudeAgentOptions(system_prompt=system)
    async def _run() -> str:
        async for msg in query(prompt=task, options=options):
            if isinstance(msg, ResultMessage):
                return msg.result
        return ""
    return asyncio.run(_run())

# Call it like a regular function:
answer = ask_sync("What is DSPy?")
```
**Recognize:** Wrapping `asyncio.run()` inside a sync function is a common pattern to make SDK calls feel synchronous from the caller's perspective.

---

### Example 6: Options Built From Config Object
```python
@dataclass
class AgentConfig:
    model: str = "claude-sonnet-5-5"
    system: str = "You are a helpful assistant."
    max_tokens: int = 512

def make_options(cfg: AgentConfig) -> ClaudeAgentOptions:
    return ClaudeAgentOptions(model=cfg.model, system_prompt=cfg.system)

cfg = AgentConfig(system="You are a concise explainer.")
async for msg in query(prompt="What is Pydantic?", options=make_options(cfg)):
    ...
```
**Recognize:** `ClaudeAgentOptions` built from a config object rather than inline. Cleaner for reuse across multiple agents.

---

### Example 7: SDK vs Raw API Side-by-Side
```python
# Phase 4 (raw API) — you write everything:
while True:
    response = client.messages.create(tools=TOOLS, messages=messages)
    if response.stop_reason == "end_turn":
        return response.content[0].text
    messages.append(...); messages.append(execute_tools(response))

# Agent SDK — SDK writes it for you:
async for msg in query(prompt=task, options=options):
    if isinstance(msg, ResultMessage):
        return msg.result
```
**Recognize:** Same outcome, radically different code. The SDK's `query()` contains the raw loop internally — you just don't see it.

---

### Example 8: In a Real Project (FastAPI endpoint)
```python
@app.post("/ask")
async def ask_endpoint(request: AskRequest) -> AskResponse:
    options = ClaudeAgentOptions(
        model="claude-sonnet-5-5",
        system_prompt=SYSTEM_PROMPT,
    )
    async for msg in query(prompt=request.question, options=options):
        if isinstance(msg, ResultMessage):
            return AskResponse(answer=msg.result)
    raise HTTPException(status_code=500, detail="No result")
```
**Recognize:** `query()` inside a FastAPI endpoint. The `async for` works naturally in async web frameworks. `ResultMessage` becomes the API response.
