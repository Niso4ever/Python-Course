# L02 — Visual: Tool Lifecycle in the SDK

> **Correction (2026-10-28):** The SDK has no `Tool` class. Read each `Tool(name=..., description=..., input_schema=...)`
> below as `@tool(name, description, input_schema)` decorating an async handler that returns
> `{"content": [{"type": "text", "text": ...}]}`. Tools go on `create_sdk_mcp_server(name=..., tools=[...])`, which you pass as
> `mcp_servers={"key": server}`; `allowed_tools` then takes name strings like `"mcp__key__calculate"`, not objects.
> The lessons on descriptions and schemas below are unchanged. Source: code.claude.com/docs/en/agent-sdk/custom-tools.

## Tool Registration Flow

```
YOU DEFINE                  SDK CONVERTS              LLM READS
────────────                ────────────              ────────────────────
Tool(                       →  {                      "I have these tools:
  name="calculate",              "name": "calculate",  - calculate: Evaluate
  description="Evaluate          "description": "...",   a math expression...
    a math expression...",        "input_schema": {...}  - search: Search a
  input_schema={...}         }                           knowledge base..."
)
```

---

## The Full Tool Execution Loop

```
┌─────────────────────────────────────────────────────────────────┐
│  User task: "What is 15% of 240?"                               │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │   LLM THINKS     │
                    │  "I should use   │
                    │   the calculate  │
                    │   tool"          │
                    └────────┬─────────┘
                             │ tool_use: calculate("15/100 * 240")
                             ▼
                    ┌──────────────────┐
                    │  SDK EXECUTES    │  ← SDK calls your function locally
                    │  calculate(      │
                    │   "15/100 * 240" │
                    │  ) → 36.0        │
                    └────────┬─────────┘
                             │ tool_result: "36.0"
                             ▼
                    ┌──────────────────┐
                    │   LLM RESUMES    │
                    │  "15% of 240     │
                    │   is 36"         │
                    └────────┬─────────┘
                             │ stop_reason: "end_turn"
                             ▼
                    ResultMessage("15% of 240 is 36")
```

---

## Tool Description Quality: The Difference

```
VAGUE (LLM guesses when to use)         PRECISE (LLM knows exactly when)
────────────────────────────────        ──────────────────────────────────
Tool(                                   Tool(
  name="search",                          name="search_knowledge_base",
  description="searches things"           description=(
)                                           "Search the knowledge base "
                                            "for factual questions. Use "
                                            "when the user asks 'what is', "
                                            "'who is', or 'how does'."
                                          )
                                        )

Result: wrong tool calls                Result: correct tool selection
```

---

## Three Tool Schema Shapes

```
SIMPLE TOOL                   TOOL WITH OPTIONS              TOOL WITH NESTED SCHEMA
────────────────              ──────────────────             ────────────────────────
{                             {                              {
  "type": "object",             "type": "object",              "type": "object",
  "properties": {               "properties": {                "properties": {
    "query": {                    "query": {str},                "filters": {
      "type": "string",           "limit": {int},                 "type": "object",
      "description": "..."        "mode": {                       "properties": {
    }                               "type": "string",               "date": {str},
  },                                "enum":["fast","full"]          "source": {str}
  "required": ["query"]           }                               }
}                               },                             }
                                "required": ["query"]        }
                              }
```
