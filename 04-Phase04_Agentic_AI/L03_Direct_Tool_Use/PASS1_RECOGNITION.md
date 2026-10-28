# Lesson 19 — Pass 1: RECOGNITION
## Learn to SEE Tool Use in AI Code

**Goal:** Recognize how tools are defined, registered, called, and returned — in raw API code, without any framework wrapper.

> **2026 Note:** CrewAI's `@tool` decorator and LangChain's `Tool()` class both compile down to this JSON schema format before hitting the API. This is what the API actually sees. Read this and you can read any framework's tool code.

---

## The Four Shapes of Direct Tool Use

### Shape 1: Tool Schema (the definition)
```python
{
    "name": "tool_name",
    "description": "What this tool does — the LLM reads this to decide when to use it",
    "input_schema": {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "What this parameter is"},
            "param2": {"type": "integer", "description": "What this number means"}
        },
        "required": ["param1"]          # ← param2 is optional (not in required list)
    }
}
```
**Recognize:** A dict with `name` + `description` + `input_schema`.

---

### Shape 2: Tool Registration
```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    tools=[tool1, tool2, tool3],        # ← the list of tool schemas
    messages=messages
)
```
**Recognize:** `tools=[...]` passed alongside `messages`.

---

### Shape 3: Tool Call Detection
```python
for block in response.content:
    if block.type == "tool_use":        # ← LLM chose to call a tool
        print(block.name)               # ← which tool
        print(block.input)             # ← what arguments (dict)
        print(block.id)                 # ← unique id to match the result to
```
**Recognize:** Loop through `response.content`, filter `type == "tool_use"`.

---

### Shape 4: Tool Result Format
```python
{
    "type": "tool_result",
    "tool_use_id": block.id,            # ← MUST match the block.id from Shape 3
    "content": "The result as a string"
}
```
**Recognize:** A dict with `type: "tool_result"` and `tool_use_id`.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: Single Tool — Web Search

```python
# DEFINE the tool (what the LLM sees)
search_tool = {
    "name": "search_web",
    "description": "Search the web for current information on any topic.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to look up"
            }
        },
        "required": ["query"]
    }
}

# CALL with the tool registered
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[search_tool],
    messages=[{"role": "user", "content": "What is the current AI news?"}]
)

# PARSE the response
for block in response.content:
    if block.type == "tool_use":
        print(block.name)    # "search_web"
        print(block.input)   # {"query": "current AI news 2026"}
        print(block.id)      # "toolu_01XYZ..."
```

**RECOGNIZE THIS:**
- `"name": "search_web"` ← tool identity
- `"description":` ← natural language — LLM reads this to decide when to use the tool
- `"required": ["query"]` ← query is mandatory
- `block.type == "tool_use"` ← LLM decided to use this tool
- `block.input` ← the arguments the LLM filled in automatically

**What it does:** "Define a search tool, give it to the LLM, read back which query it chose."

---

### Example 2: Multiple Tools + Dispatcher

```python
# Two tools with different input shapes
calculator_tool = {
    "name": "calculate",
    "description": "Perform a mathematical calculation.",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "Math expression like '2 + 2'"}
        },
        "required": ["expression"]
    }
}

lookup_tool = {
    "name": "lookup_fact",
    "description": "Look up a specific fact from the knowledge base.",
    "input_schema": {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "Topic to look up"},
            "detail": {"type": "string", "description": "Specific aspect to retrieve"}
        },
        "required": ["topic"]       # ← detail is optional
    }
}

# Register both tools
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[calculator_tool, lookup_tool],
    messages=[{"role": "user", "content": "What is 15% of 240?"}]
)

# Dispatcher: routes to the right function
def handle_tool_call(block):
    if block.name == "calculate":
        return str(eval(block.input["expression"]))
    elif block.name == "lookup_fact":
        return knowledge_base.get(block.input["topic"], "Not found")
    return "Unknown tool"

# Execute all tool calls
for block in response.content:
    if block.type == "tool_use":
        result = handle_tool_call(block)
        print(f"{block.name} → {result}")
# calculate → "36.0"
```

**RECOGNIZE THIS:**
- Two schemas in `tools=[...]` ← LLM picks the right one automatically
- `"required": ["topic"]` but not `"detail"` ← optional parameter pattern
- `handle_tool_call(block)` ← dispatcher routing by `block.name`

**What it does:** "Register two tools. LLM picks which one to call. Dispatcher routes to the right function."

---

### Example 3: Returning Tool Results to the LLM

```python
# After detecting tool_use in the response:
messages = [{"role": "user", "content": "What is the weather in Tokyo?"}]

response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024,
    tools=[weather_tool], messages=messages
)

# Agent requested: get_weather(city="Tokyo")
tool_results = []
for block in response.content:
    if block.type == "tool_use":
        weather_data = get_weather(block.input["city"])   # call real function
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,          # ← must match exactly
            "content": weather_data           # ← the actual result string
        })

# Feed results back — agent sees both its request AND the result
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user",      "content": tool_results})

# Now call the LLM again with the results
final_response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024,
    tools=[weather_tool], messages=messages
)
print(final_response.content[0].text)
# "The current weather in Tokyo is 22°C with partly cloudy skies."
```

**RECOGNIZE THIS:**
- `"tool_use_id": block.id` ← the id pairing — LLM uses this to know which result goes where
- `messages.append({"role": "assistant"...})` then `messages.append({"role": "user"...})` ← the double append pattern
- `final_response` ← calling LLM a SECOND time after adding results

**What it does:** "Execute the tool, pack result with matching id, call LLM again to compose the answer."

---

### Example 4: Tool Schema with Optional + Enum Parameters

```python
filter_tool = {
    "name": "filter_results",
    "description": "Filter a list of search results by criteria.",
    "input_schema": {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of results to filter"
            },
            "min_score": {
                "type": "number",
                "description": "Minimum score threshold (0.0 to 1.0)",
                "default": 0.8                    # ← default value hint for LLM
            },
            "sort_by": {
                "type": "string",
                "description": "How to sort the output",
                "enum": ["score", "date", "relevance"]  # ← only these values allowed
            }
        },
        "required": ["results"]                   # ← only results is required
    }
}
```

**Example call (what LLM produces after reading the schema):**
```python
# LLM generates this tool_use block automatically:
# block.name  = "filter_results"
# block.input = {"results": ["doc1", "doc2", "doc3"], "sort_by": "score"}
# (LLM chose not to include min_score — uses default)
```

**RECOGNIZE THIS:**
- `"array"` ← list input
- `"default": 0.8` ← hint to LLM about what to use if not specified
- `"enum": [...]` ← restricts LLM to only valid values
- `"required": ["results"]` ← only one required field; others optional

**What it does:** "Define a flexible tool with optional parameters and constrained choices."

---

### Example 5: Tool with Error Handling

```python
def safe_dispatch(block) -> str:
    """Execute a tool call safely — always return a string."""
    try:
        fn = TOOL_MAP.get(block.name)
        if not fn:
            return f"Error: Tool '{block.name}' not found."

        result = fn(**block.input)
        return str(result)

    except KeyError as e:
        return f"Error: Missing required parameter {e}"
    except Exception as e:
        return f"Error executing {block.name}: {str(e)}"

# Full flow with error handling:
tool_results = []
for block in response.content:
    if block.type == "tool_use":
        result = safe_dispatch(block)         # ← always returns a string, never crashes
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": result
        })
```

**Example calls:**
```python
result = safe_dispatch(MockBlock(name="search_web", input={"query": "AI news"}))
print(result)   # "Latest AI news: ..."  (success)

result = safe_dispatch(MockBlock(name="unknown_tool", input={}))
print(result)   # "Error: Tool 'unknown_tool' not found."

result = safe_dispatch(MockBlock(name="search_web", input={}))
print(result)   # "Error: Missing required parameter 'query'"
```

**RECOGNIZE THIS:**
- `try/except` wrapping the dispatch ← tool calls can fail
- `return f"Error: ..."` ← returning the error AS a string result (not raising)
- The LLM sees the error string and can decide what to do next

**What it does:** "Wrap every tool call so errors become messages, not crashes."

---

### Example 6: tool_choice — Forcing a Specific Tool

> **Model restriction (checked 2026-10-28):** `tool_choice={"type": "any"}` and `{"type": "tool", "name": ...}`
> return a 400 error on claude-opus-5-5, claude-sonnet-5-5 and claude-fable-5-1. On those models use the default
> `{"type": "auto"}` and say in the prompt which tool to use; add `"strict": True` to the tool definition for
> schema-exact arguments; or use structured outputs (L04) when you only wanted JSON back. `"none"` still works.
> Source: platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use

```python
# Force the LLM to use a specific tool (not its choice)
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[search_tool, calculator_tool],
    tool_choice={"type": "tool", "name": "search_tool"},   # ← forced
    messages=messages
)
# LLM MUST call search_tool — no "end_turn" option

# Force the LLM to use ANY tool (but it picks which one)
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[search_tool, calculator_tool],
    tool_choice={"type": "any"},                           # ← any tool, but required
    messages=messages
)

# Default: LLM decides (may or may not call a tool)
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[search_tool, calculator_tool],
    # tool_choice not set → LLM decides
    messages=messages
)
```

**RECOGNIZE THIS:**
- `"type": "tool", "name": "..."` ← force a specific tool
- `"type": "any"` ← force a tool call, any tool
- No `tool_choice` ← LLM's discretion (default)

**What it does:** "Control whether and which tool the LLM calls — useful for structured pipelines."

---

### Example 7: Reading Tool Use Inside CrewAI (Framework Recognition)

```python
# CrewAI hides this, but underneath it generates this same schema:
# CrewAI @tool decorator:
from crewai.tools import tool

@tool("Web Searcher")
def search_web(query: str) -> str:
    """Search the web for current information."""
    return web_search_api(query)

# What CrewAI sends to the API (the raw schema it generates):
# {
#     "name": "Web Searcher",
#     "description": "Search the web for current information.",
#     "input_schema": {
#         "type": "object",
#         "properties": {
#             "query": {"type": "string"}
#         },
#         "required": ["query"]
#     }
# }
# IDENTICAL to what you write by hand in this lesson.
```

**RECOGNIZE THIS:**
- The `@tool` decorator reads the Python docstring → becomes `"description"`
- The function signature `query: str` → becomes the `input_schema`
- At the API level, it is the same JSON you've been reading

**What it does:** "Framework decorators are just schema generators. Underneath: same JSON."

---

### Example 8: Full Tool Use Flow — End to End

```python
import anthropic

client = anthropic.Anthropic()

# Step 1: Define tools
tools = [
    {
        "name": "search_web",
        "description": "Search the web for information.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Search query"}},
            "required": ["query"]
        }
    }
]

# Step 2: Start with user question
messages = [{"role": "user", "content": "What AI models did Anthropic release in 2026?"}]

# Step 3: First LLM call — LLM decides to search
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024,
    tools=tools, messages=messages
)
# response.stop_reason = "tool_use"
# response.content[1].name = "search_web"
# response.content[1].input = {"query": "Anthropic AI models released 2026"}

# Step 4: Execute the tool
tool_results = []
for block in response.content:
    if block.type == "tool_use":
        search_result = web_search(block.input["query"])
        tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": search_result})

# Step 5: Feed results back
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user",      "content": tool_results})

# Step 6: Second LLM call — LLM now has the search result
final = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024,
    tools=tools, messages=messages
)
# final.stop_reason = "end_turn"
print(final.content[0].text)
# "In 2026, Anthropic released Claude Opus 5.5, Claude Sonnet 5.5, and Claude Haiku 5.5..."
```

**RECOGNIZE THIS:**
- 6 steps total: Define → Start → First Call → Execute → Feed Back → Final Call
- Only 2 LLM calls for a 1-tool-use answer (more tools = more calls)
- `messages.append(...)` twice before the second LLM call

**What it does:** "The complete direct tool use flow. No framework. Raw API."

---

## Tool Schema Anatomy Reference

| Field | Required | What it does |
|:------|:---------|:-------------|
| `name` | Yes | Tool identity — LLM uses this to identify which tool to call |
| `description` | Yes | Natural language — LLM reads this to know WHEN to call the tool |
| `input_schema.type` | Yes | Always `"object"` |
| `input_schema.properties` | Yes | Each parameter — name, type, description |
| `input_schema.required` | Yes | Which parameters must be provided |
| `default` (inside property) | No | Hint to LLM for optional parameters |
| `enum` (inside property) | No | Restrict values to a specific list |

---

## You've Completed Pass 1!

You can now:
✓ **Read** a tool schema and understand what the LLM sees
✓ **Identify** `block.type == "tool_use"` in response parsing code
✓ **Trace** the id from `block.id` → `tool_use_id` in results
✓ **Recognize** the double append pattern (assistant + user)
✓ **Spot** tool schemas hidden inside framework decorators
✓ **Understand** `tool_choice` for forcing specific tool calls

**Next:**
- **Pass C (Visual):** See the tool call message flow as a diagram
- **Pass 3 (Templates):** Copy ready-to-use tool patterns
