# L02 — Pass 1: RECOGNITION
## Learn to SEE Tool Definitions in the SDK

> **Correction (2026-10-28):** The SDK has no `Tool` class. Read each `Tool(name=..., description=..., input_schema=...)`
> below as `@tool(name, description, input_schema)` decorating an async handler that returns
> `{"content": [{"type": "text", "text": ...}]}`. Tools go on `create_sdk_mcp_server(name=..., tools=[...])`, which you pass as
> `mcp_servers={"key": server}`; `allowed_tools` then takes name strings like `"mcp__key__calculate"`, not objects.
> The lessons on descriptions and schemas below are unchanged. Source: code.claude.com/docs/en/agent-sdk/custom-tools.

**Goal:** When you see SDK tool definitions, instantly recognize the shape — `Tool()` objects, schema patterns, and the description quality — without writing a single line.

> **2026 Note:** The `Tool()` object is how you communicate with the LLM about what it can do. A badly described tool is functionally invisible — the LLM won't call it correctly. Recognition skill: can you tell from the description alone when the LLM should call this tool?

---

## The Three Shapes of SDK Tools

### Shape 1: The Tool Object
```python
from claude_agent_sdk import Tool

my_tool = Tool(
    name="tool_name",
    description="When and why to call this. What it does. What to pass.",
    input_schema={"type": "object", "properties": {...}, "required": [...]}
)
```
**Recognize:** Three fields. `name` = identifier. `description` = LLM instructions. `input_schema` = JSON Schema for parameters.

### Shape 2: Registration
```python
options = ClaudeAgentOptions(allowed_tools=[tool_a, tool_b, tool_c])
```
**Recognize:** (Corrected) In the real SDK, `allowed_tools=` takes tool-name strings such as `"mcp__tools__search"`; the tool objects go on an MCP server passed as `mcp_servers=`. The SDK converts the schemas to Anthropic format automatically.

### Shape 3: The Schema Pattern
```python
"input_schema": {
    "type": "object",
    "properties": {"param": {"type": "string", "description": "..."}},
    "required": ["param"]
}
```
**Recognize:** Always `"type": "object"` at the root. `properties` = named parameters. `required` = which params are mandatory.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: Single Tool — Calculator
```python
from claude_agent_sdk import Tool

calculator = Tool(
    name="calculate",
    description="Evaluate a math expression. Use for arithmetic, percentages, unit conversions.",
    input_schema={
        "type": "object",
        "properties": {"expression": {"type": "string", "description": "e.g. '15/100 * 240'"}},
        "required": ["expression"]
    }
)
```
**Recognize:** Good description = tells LLM exactly when to use ("arithmetic, percentages, unit conversions"). Good schema = single required string param with example.

---

### Example 2: Tool With Enum Parameter
```python
search_tool = Tool(
    name="web_search",
    description="Search the web for current information. Use 'fast' for quick facts, 'deep' for research.",
    input_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "search query"},
            "mode":  {"type": "string", "enum": ["fast", "deep"], "description": "search depth"}
        },
        "required": ["query"]
    }
)
```
**Recognize:** `"enum": ["fast", "deep"]` limits valid values. `mode` not in `required` = optional with a default implied.

---

### Example 3: Tool With Nested Schema
```python
filter_tool = Tool(
    name="filter_results",
    description="Filter search results by date and source type.",
    input_schema={
        "type": "object",
        "properties": {
            "results": {"type": "array",  "items": {"type": "string"}},
            "filters": {
                "type": "object",
                "properties": {
                    "after_date": {"type": "string", "description": "YYYY-MM-DD"},
                    "source":     {"type": "string", "enum": ["arxiv", "github", "docs"]}
                }
            }
        },
        "required": ["results"]
    }
)
```
**Recognize:** Nested `"type": "object"` inside `properties`. Arrays use `"type": "array"` with `"items"`.

---

### Example 4: Three Tools Registered Together
```python
options = ClaudeAgentOptions(
    model="claude-sonnet-5-5",
    system_prompt="Use tools when needed. Be concise.",
    allowed_tools=[calculator, search_tool, analyzer],
)
```
**Recognize:** `allowed_tools` takes a flat list. The LLM sees all three and decides which one fits each situation.

---

### Example 5: Bad Description vs. Good Description (SPOT THE DIFFERENCE)
```python
# BAD — LLM can't decide when to use
bad_tool = Tool(name="search", description="searches things", input_schema={...})

# GOOD — LLM knows exactly when and how
good_tool = Tool(
    name="search_knowledge_base",
    description=(
        "Search for AI/ML concepts. Use for 'what is', 'explain', 'how does' questions. "
        "NOT for math or text analysis."
    ),
    input_schema={"type": "object", "properties": {"query": {"type": "string", "description": "search query"}}, "required": ["query"]}
)
```
**Recognize:** The bad tool will cause wrong-tool selection. The good tool tells the LLM three things: what it does, when to use it, and when NOT to use it.

---

### Example 6: Tool Built From Pydantic Schema
```python
from pydantic import BaseModel, Field
from claude_agent_sdk import Tool

class SearchInput(BaseModel):
    query: str = Field(description="The search query")
    limit: int = Field(default=5, description="Max results (1-20)")

search = Tool(
    name="search",
    description="Search the knowledge base for factual information.",
    input_schema=SearchInput.model_json_schema()
)
```
**Recognize:** `SearchInput.model_json_schema()` auto-generates the JSON Schema from the Pydantic model. Field `description=` becomes the parameter description the LLM sees.

---

### Example 7: Tool Dispatcher (The Other Half)
```python
TOOL_MAP: dict[str, callable] = {
    "calculate":   lambda args: calculate(args["expression"]),
    "search":      lambda args: search_kb(args["query"]),
    "analyze_text": lambda args: analyze(args["text"]),
}

def dispatch(tool_name: str, tool_input: dict) -> str:
    fn = TOOL_MAP.get(tool_name)
    return fn(tool_input) if fn else f"Unknown tool: {tool_name}"
```
**Recognize:** The dispatcher is the other half of every tool definition. Tool schema = what the LLM sees. Dispatcher = what actually executes.

---

### Example 8: Tool in Production Context
```python
db_tool = Tool(
    name="query_database",
    description=(
        "Run a read-only SQL query on the analytics database. "
        "Use for user counts, revenue metrics, event aggregations. "
        "Never use for mutations (INSERT, UPDATE, DELETE)."
    ),
    input_schema={
        "type": "object",
        "properties": {"sql": {"type": "string", "description": "SELECT query only"}},
        "required": ["sql"]
    }
)
options = ClaudeAgentOptions(allowed_tools=[db_tool], model="claude-opus-5-5")
```
**Recognize:** Production tool descriptions explicitly state what NOT to do ("Never use for mutations"). This is a safety guardrail written directly into the description.
