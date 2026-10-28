# Lesson 19 — Pass C: VISUAL PATTERNS
## See the Tool Call Flow as a Diagram

**Goal:** Visualize the message flow when an LLM calls a tool. See where the schema lives, where the call happens, and how results come back.

---

## Visual 1: The Tool Schema — What the LLM Reads

### Code:
```python
search_tool = {
    "name": "search_web",
    "description": "Search the web for current information on any topic.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query"
            }
        },
        "required": ["query"]
    }
}
```

**Example call (what the LLM produces after reading this):**
```python
# LLM generates tool_use block automatically:
# block.name  = "search_web"
# block.input = {"query": "current AI news 2026"}
```

### Visual — Schema layers:
```
┌─────────────────────────────────────────────┐
│              TOOL SCHEMA                    │
│                                             │
│  "name"        → "search_web"              │  ← LLM uses this name to call it
│  "description" → "Search the web..."       │  ← LLM reads this to decide WHEN
│                                             │
│  "input_schema"                             │
│  └── "properties"                           │
│       └── "query"                           │
│            ├── "type": "string"             │  ← what kind of value to provide
│            └── "description": "The query"  │  ← how to fill it in
│                                             │
│  "required": ["query"]                      │  ← must always be provided
│                                             │
└─────────────────────────────────────────────┘
          ↓ LLM reads this and produces:
┌─────────────────────────────────────────────┐
│              TOOL USE BLOCK                 │
│                                             │
│  block.type  = "tool_use"                   │
│  block.name  = "search_web"                 │
│  block.id    = "toolu_01XYZ..."             │
│  block.input = {"query": "AI news 2026"}    │
│                                             │
└─────────────────────────────────────────────┘
```

**Pattern:** Schema = instruction to LLM. Tool use block = LLM's response to those instructions.

---

## Visual 2: The Tool Call Message Flow

### Code:
```python
# Step 1: User asks
messages = [{"role": "user", "content": "What is the weather in Tokyo?"}]

# Step 2: LLM sees the question + tools → decides to call a tool
response = client.messages.create(tools=[weather_tool], messages=messages)

# Step 3: Execute the tool
tool_result = get_weather("Tokyo")

# Step 4: Feed results back
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user",      "content": [{"type": "tool_result", ...}]})

# Step 5: LLM sees the result → composes final answer
final = client.messages.create(tools=[weather_tool], messages=messages)
```

**Example call:**
```python
# After step 5:
print(final.content[0].text)  # "The current weather in Tokyo is 22°C, partly cloudy."
print(len(messages))          # 3 (original + assistant request + user result)
```

### Visual — Message list after each step:
```
STEP 1 — Start:
  messages = [
    {role: "user",  content: "What is the weather in Tokyo?"}
  ]

STEP 2 — After LLM call (tool_use):
  response.content = [
    TextBlock("Let me check the weather..."),
    ToolUseBlock(id="tu_01", name="get_weather", input={"city": "Tokyo"})
  ]

STEP 3 — Tool executed:
  weather_result = "22°C, partly cloudy"

STEP 4 — Messages updated:
  messages = [
    {role: "user",      content: "What is the weather in Tokyo?"}
    {role: "assistant", content: [TextBlock, ToolUseBlock]}       ← agent's request
    {role: "user",      content: [{type:"tool_result",            ← the answer
                                   tool_use_id:"tu_01",
                                   content:"22°C, partly cloudy"}]}
  ]

STEP 5 — Final LLM call:
  final.content[0].text = "The current weather in Tokyo is 22°C, partly cloudy."
```

**Pattern:** User → LLM (decides) → Tool (executes) → LLM (composes answer).

---

## Visual 3: Multiple Tools in One Response

Sometimes the LLM calls more than one tool in a single response:

### Code:
```python
# LLM response.content might contain:
[
    TextBlock("I'll look up both items..."),
    ToolUseBlock(id="tu_01", name="search_web", input={"query": "Tokyo weather"}),
    ToolUseBlock(id="tu_02", name="search_web", input={"query": "Tokyo population"})
]
```

**Example call:**
```python
results = execute_tools(response.content)
print(len(results))   # 2 — one result per tool_use block
print(results[0]["tool_use_id"])  # "tu_01"
print(results[1]["tool_use_id"])  # "tu_02"
```

### Visual:
```
response.content = [
  TextBlock    ← skip (not a tool call)
  ToolUseBlock (id="tu_01", name="search_web", input={"query": "Tokyo weather"})
  ToolUseBlock (id="tu_02", name="search_web", input={"query": "Tokyo population"})
]
       │
       ▼ for block in response.content: if block.type == "tool_use":
       │
  ┌────────────┐    ┌────────────┐
  │ Execute    │    │ Execute    │
  │ search_web │    │ search_web │
  │ "weather"  │    │"population"│
  └────────────┘    └────────────┘
        │                 │
        ▼                 ▼
  tool_result       tool_result
  (id="tu_01")     (id="tu_02")
        │                 │
        └────────┬─────────┘
                 ▼
          messages.append([result1, result2])
```

**Pattern:** One response → multiple tool calls → multiple results → one message back.

---

## Visual 4: The id Pairing System

```
LLM GENERATES:                         YOU RETURN:
┌────────────────────────┐             ┌────────────────────────┐
│ ToolUseBlock           │             │ tool_result dict       │
│   id = "toolu_01XYZ"  │ ←── MATCH → │   tool_use_id:         │
│   name = "search_web"  │             │     "toolu_01XYZ"      │
│   input = {"query":..} │             │   content: "result..."  │
└────────────────────────┘             └────────────────────────┘
```

**Why:** If the LLM calls 3 tools, it needs to know which result belongs to which call.
The `id` is the link. **Miss it → LLM gets confused.**

---

## Visual 5: Tool Choice Options

> **Model restriction (checked 2026-10-28):** `tool_choice={"type": "any"}` and `{"type": "tool", "name": ...}`
> return a 400 error on claude-opus-5-5, claude-sonnet-5-5 and claude-fable-5-1. On those models use the default
> `{"type": "auto"}` and say in the prompt which tool to use; add `"strict": True` to the tool definition for
> schema-exact arguments; or use structured outputs (L04) when you only wanted JSON back. `"none"` still works.
> Source: platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use

```
NO tool_choice (default):
  User question → LLM decides → may or may not call a tool
                                         ↓
                                  if simple → "end_turn"
                                  if needs info → "tool_use"

tool_choice = {"type": "any"}:
  User question → LLM MUST call a tool → picks which one
                           ↑ always "tool_use" stop_reason

tool_choice = {"type": "tool", "name": "search_web"}:
  User question → LLM MUST call search_web specifically
                           ↑ always "tool_use", always search_web
```

**Example calls:**
```python
# Force any tool (useful for structured pipelines)
response = client.messages.create(
    tools=tools, tool_choice={"type": "any"}, messages=messages
)
print(response.stop_reason)  # always "tool_use"

# Force specific tool (useful for guaranteed extraction)
response = client.messages.create(
    tools=tools, tool_choice={"type": "tool", "name": "extract_data"}, messages=messages
)
print(response.content[0].name)  # always "extract_data"
```

**Pattern:** Control how much freedom the LLM has to choose tools.

---

## Visual 6: Schema Types Reference

```
SIMPLE TYPES:
  "type": "string"   → any text
  "type": "integer"  → whole number (1, 2, 100)
  "type": "number"   → decimal (0.5, 3.14)
  "type": "boolean"  → True or False

COLLECTION TYPES:
  "type": "array"
  "items": {"type": "string"}   → list of strings  ["a", "b", "c"]
  "items": {"type": "integer"}  → list of numbers  [1, 2, 3]

CONSTRAINED:
  "enum": ["option1", "option2"]   → only these values allowed
  "default": "value"               → hint for optional params

REQUIRED:
  "required": ["param1", "param2"]   → these must always be provided
  (any param NOT in required list is optional)
```

**Example call with various types:**
```python
# LLM calls a tool with mixed input types
block.input = {
    "query": "AI news",          # string
    "max_results": 5,            # integer
    "min_score": 0.85,           # number (float)
    "include_images": False,     # boolean
    "topics": ["AI", "LLMs"],   # array of strings
    "sort_by": "date"            # enum
}
```

---

## Visual 7: Framework vs Direct Comparison

```
CREWAI:
  @tool("Search Web")
  def search(query: str) -> str:
      """Search the internet for current info."""
      return web_search(query)
                    ↓ (framework generates this internally)
DIRECT API:
  {
      "name": "Search Web",
      "description": "Search the internet for current info.",
      "input_schema": {
          "type": "object",
          "properties": {
              "query": {"type": "string"}
          },
          "required": ["query"]
      }
  }

BOTH hit the same API. The framework just writes the JSON for you.
Once frameworks are deprecated, you write the JSON directly.
```

---

## You've Completed Pass C!

You can now:
✓ **Visualize** the schema → tool_use block transformation
✓ **See** the message list grow through a tool call cycle
✓ **Understand** why `id` pairing is critical
✓ **Map** `tool_choice` to the three options
✓ **Read** framework tool decorators as JSON schemas
✓ **Know** all the input schema types

**Next:** Pass 3 — Copy ready-to-use tool definition and dispatch templates.
