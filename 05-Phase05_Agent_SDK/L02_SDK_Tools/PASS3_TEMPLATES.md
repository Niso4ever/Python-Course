# L02 — Pass 3: TEMPLATES
## Your SDK Tool Copy-Paste Library

> **Correction (2026-10-28):** The SDK has no `Tool` class. Read each `Tool(name=..., description=..., input_schema=...)`
> below as `@tool(name, description, input_schema)` decorating an async handler that returns
> `{"content": [{"type": "text", "text": ...}]}`. Tools go on `create_sdk_mcp_server(name=..., tools=[...])`, which you pass as
> `mcp_servers={"key": server}`; `allowed_tools` then takes name strings like `"mcp__key__calculate"`, not objects.
> The lessons on descriptions and schemas below are unchanged. Source: code.claude.com/docs/en/agent-sdk/custom-tools.

**Goal:** Five ready-to-use tool patterns. Copy, rename the function, adjust the schema, use.

> **2026 Note:** The tool description IS the interface between you and the LLM. A vague description is a broken tool. Copy these templates, then rewrite the description for your specific tool — that's the only part that truly matters.

---

## Template 1: Single Tool Agent
**Use when:** Agent needs exactly one capability

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, Tool, ResultMessage

def calculate(expression: str) -> str:
    try:
        return str(round(eval(expression), 6))  # noqa: S307
    except Exception as e:
        return f"Error: {e}"

calc_tool = Tool(
    name="calculate",
    description="Evaluate a math expression. Use for arithmetic, percentages, conversions.",
    input_schema={
        "type": "object",
        "properties": {"expression": {"type": "string", "description": "e.g. '15/100 * 240'"}},
        "required": ["expression"]
    }
)

async def math_agent(task: str) -> str:
    options = ClaudeAgentOptions(allowed_tools=[calc_tool])
    async for msg in query(prompt=task, options=options):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""

# Call:
print(asyncio.run(math_agent("What is 15% of 240?")))
# → "15% of 240 is 36."
```

---

## Template 2: Multi-Tool Agent (3 Tools)
**Use when:** Agent needs to choose between multiple capabilities

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, Tool, ResultMessage

# Define tools
calculator = Tool(
    name="calculate",
    description="Math expressions. Use for arithmetic, percentages, conversions.",
    input_schema={"type":"object","properties":{"expression":{"type":"string","description":"math expression"}},"required":["expression"]}
)
searcher = Tool(
    name="search_kb",
    description="Search knowledge base for AI/ML concepts. Use for 'what is' questions.",
    input_schema={"type":"object","properties":{"query":{"type":"string","description":"search query"}},"required":["query"]}
)
analyzer = Tool(
    name="analyze_text",
    description="Count words and sentences. Use for text statistics only.",
    input_schema={"type":"object","properties":{"text":{"type":"string","description":"text to analyze"}},"required":["text"]}
)

# Tool dispatcher
TOOL_MAP = {"calculate": calculate, "search_kb": search_kb, "analyze_text": analyze_text}

async def multi_tool_agent(task: str) -> str:
    options = ClaudeAgentOptions(allowed_tools=[calculator, searcher, analyzer])
    async for msg in query(prompt=task, options=options):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""
```

---

## Template 3: Tool With Enum + Optional Params
**Use when:** Tool has a limited set of valid modes or optional configuration

```python
from claude_agent_sdk import Tool

search_tool = Tool(
    name="web_search",
    description=(
        "Search the web for current information. "
        "Use 'deep' for research tasks, 'fast' for quick facts. "
        "Optionally filter by time_range for recent results."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "concise search query (a few keywords)"
            },
            "depth": {
                "type": "string",
                "enum": ["fast", "deep"],
                "description": "fast=quick lookup, deep=thorough research"
            },
            "time_range": {
                "type": "string",
                "enum": ["day", "week", "month", "year"],
                "description": "optional: only return results from this time window"
            }
        },
        "required": ["query"]
    }
)
# depth and time_range are optional — LLM fills them based on context
```

---

## Template 4: Tool Built From Pydantic Schema
**Use when:** You already have Pydantic models — auto-generate the schema

```python
from pydantic import BaseModel, Field
from claude_agent_sdk import Tool

class DatabaseQueryInput(BaseModel):
    sql: str = Field(description="SELECT query only — no mutations allowed")
    limit: int = Field(default=10, description="Max rows to return (1–100)")
    format: str = Field(default="json", description="Output format: 'json' or 'csv'")

class DatabaseQueryOutput(BaseModel):
    rows: list[dict] = Field(description="Query results")
    row_count: int = Field(description="Number of rows returned")
    query_time_ms: float = Field(description="Query execution time in milliseconds")

db_tool = Tool(
    name="query_database",
    description=(
        "Run a read-only SQL query. Use for data lookups, aggregations, metrics. "
        "Never use for INSERT, UPDATE, DELETE."
    ),
    input_schema=DatabaseQueryInput.model_json_schema()
)
# ↑ Pydantic generates the JSON Schema automatically — Field descriptions become parameter docs
```

---

## Template 5: Tool Dispatcher (Required Companion)
**Use when:** Building a custom agent loop (raw API) or testing tools independently

```python
from typing import Any

TOOL_IMPLEMENTATIONS: dict[str, callable] = {
    "calculate":    lambda args: calculate(args["expression"]),
    "search_kb":    lambda args: search_kb(args["query"]),
    "analyze_text": lambda args: analyze_text(args["text"]),
    "query_db":     lambda args: query_db(args["sql"], args.get("limit", 10)),
}

def dispatch_tool(tool_name: str, tool_input: dict[str, Any]) -> str:
    """Execute a tool by name and return the result as a string.

    Args:
        tool_name: The tool's registered name.
        tool_input: Dict of parameters matching the tool's input_schema.

    Returns:
        Tool result as a string (or error message).
    """
    fn = TOOL_IMPLEMENTATIONS.get(tool_name)
    if fn is None:
        return f"Error: Unknown tool '{tool_name}'"
    try:
        result = fn(tool_input)
        return str(result)
    except Exception as e:
        return f"Error executing {tool_name}: {e}"

# Test any tool directly:
print(dispatch_tool("calculate", {"expression": "15/100 * 240"}))   # → "36.0"
print(dispatch_tool("search_kb", {"query": "what is RAG"}))         # → "RAG is..."
```

---

## Quick Selection Guide

| Need | Template |
|------|----------|
| Agent with one capability | Template 1: Single Tool |
| Agent that picks between tools | Template 2: Multi-Tool |
| Tool with limited valid modes | Template 3: Enum Params |
| Already have Pydantic models | Template 4: Pydantic Schema |
| Testing tools or raw loop | Template 5: Dispatcher |

---

## Tool Description Checklist

Before registering a tool, verify:
- [ ] Does the description say WHEN to use it?
- [ ] Does it say what NOT to use it for (if relevant)?
- [ ] Does it describe the expected input format (with an example)?
- [ ] Is it 1–4 sentences? (longer = LLM ignores it)
- [ ] Would a non-technical person understand when to call it?
