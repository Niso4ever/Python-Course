# L02 — Defining Tools in the SDK

> **Metaphor:** In Phase 4 you wrote tool schemas as raw JSON dictionaries — like filling out
> a form by hand. The SDK's `@tool` decorator is a pre-printed form with labels and validation built in.

---

## The Shift

Phase 4 (Ph4-L03) tool definition — a raw dict the LLM reads:

```python
# Phase 4 style — raw schema dict
{"name": "calculate", "description": "...", "input_schema": {"type": "object", ...}}
```

SDK `@tool` — same three parts (name, description, schema) plus the function that runs:

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions

@tool(
    "calculate",
    "Evaluate a math expression. Use for any arithmetic.",
    {
        "type": "object",
        "properties": {"expression": {"type": "string", "description": "e.g. '2 + 2'"}},
        "required": ["expression"],
    },
)
async def calculate(args: dict) -> dict:
    return {"content": [{"type": "text", "text": str(eval(args["expression"]))}]}

server = create_sdk_mcp_server(name="tools", tools=[calculate])   # in-process MCP server
options = ClaudeAgentOptions(
    model="claude-sonnet-5-5",
    mcp_servers={"tools": server},
    allowed_tools=["mcp__tools__calculate"],     # names, as "mcp__<server key>__<tool>"
)
```

> **Corrected 2026-10-28.** Earlier versions of this lesson used `from claude_agent_sdk import Tool`,
> `Tool(name=..., description=..., input_schema=...)` and `allowed_tools=[tool_object]`. The SDK has no
> `Tool` class, and `allowed_tools` takes tool-name strings. The PASS files still show `Tool(...)` in places:
> read every `Tool(name, description, input_schema)` there as `@tool(name, description, input_schema)` on an
> async handler. Everything they teach about descriptions and schemas is unchanged.
> Source: code.claude.com/docs/en/agent-sdk/custom-tools.

---

## The Tool Lifecycle

```
1. You define @tool handlers and put them on an in-process MCP server
2. SDK converts them to Anthropic schema format
3. LLM reads descriptions → decides which tool to call
4. SDK executes the tool locally
5. Result injected into messages
6. Loop continues
```

---

## Writing Tool Descriptions That Work

The description IS the tool's interface with the LLM. Write it like an instruction card.

| Bad description | Good description |
|-----------------|-----------------|
| `"Calculates things"` | `"Evaluate a math expression. Use when the user asks for arithmetic, percentages, or conversions."` |
| `"Search tool"` | `"Search a knowledge base. Use when the user asks a factual question that needs a lookup."` |
| `"Analyze text"` | `"Count words, sentences, and detect the dominant language. Use for text statistics only."` |

**Rule:** If the LLM can't decide when to call your tool from the description alone, rewrite the description.

---

## Architect's Question

> "If the LLM can only see the tool name and description — no code — would it know when
> and how to call this tool correctly? If not, the description needs work."
