# Lesson 13 - Pass 1: RECOGNITION
## Learn to SEE Tool Use Patterns in AI Agent Code

**Goal:** By the end of this pass, you'll instantly recognize tool definitions, the tool use loop, and the ReAct pattern — WITHOUT writing any code.

---

## The Shape Recognition Method

Tool use code has distinctive VISUAL SHAPES. Learn to recognize them by sight.

> **Key insight:** Tool use is what transforms a chatbot into an agent. The LLM decides WHEN to use tools. Your code decides WHAT the tools do. The pattern is always the same loop — only the tools change.

### Shape 1: The Tool Definition

```python
{
    "name":         "tool_name",
    "description":  "What it does. When to use it. When NOT to use it.",
    "input_schema": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "..."}
        },
        "required": ["param"]
    }
}
```

**Visual Pattern:**
```
{
    "name":         ...   ← what LLM calls this tool
    "description":  ...   ← what LLM reads to decide when to use it
    "input_schema": {...} ← what parameters the tool accepts
}
```

### Shape 2: The Tool Use Loop

```python
while True:
    response = client.messages.create(...)

    if response.stop_reason == "end_turn":
        return response.content[0].text

    if response.stop_reason == "tool_use":
        # execute tools, add results
        messages.append(...)
        # loop continues
```

**Visual Pattern:**
```
while True:
    ask LLM
    if finished → return
    if needs tool → run tool → add result → loop
```

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: The Core Concept

```
WITHOUT TOOLS:
  User:  "What's the weather in Tokyo right now?"
  LLM:   "I don't have real-time weather data. As of my training..."
  ← Knows it can't answer

WITH TOOLS:
  User:  "What's the weather in Tokyo right now?"
  LLM:   "I need to call get_weather('Tokyo')"        ← DECIDES to use tool
  Code:  get_weather("Tokyo") → {"temp": 18, "condition": "cloudy"}  ← EXECUTES
  LLM:   "The current weather in Tokyo is 18°C and cloudy."          ← USES RESULT

The LLM orchestrates. Your code executes. Results feed back in.
```

**RECOGNIZE THIS:**
- LLM reasons about WHAT to do
- Your Python code does the actual work
- Result returned to LLM so it can continue reasoning

---

### Example 2: Three Tool Definitions

```python
TOOLS = [
    {
        "name": "web_search",
        "description": "Search the internet for current, real-time information. "
                       "Use when you need recent news, current prices, or live data. "
                       "Do NOT use for math calculations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Specific search query — be precise"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculator",
        "description": "Evaluate math expressions. Use for any calculation "
                       "involving numbers, percentages, or arithmetic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression, e.g. '(45 * 12) / 100'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "read_document",
        "description": "Read a local document by filename.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "e.g. 'report.txt'"},
                "section":  {"type": "string", "description": "Optional: specific section"}
            },
            "required": ["filename"]      # ← "section" is optional (not in required)
        }
    }
]
```

**RECOGNIZE THIS:**
- `TOOLS` is a list of 3 dictionaries (L02 pattern!)
- Each tool dict has `name`, `description`, `input_schema`
- `"required": ["filename"]` ← `section` is optional because it's not listed here
- The `description` field is what the LLM reads to decide when to use it

**What it does:** "Catalog of 3 tools — the LLM reads descriptions to pick the right one."

---

### Example 3: Tool Registry (The Lookup Table)

```python
# Python functions that actually do the work:
def web_search(query: str) -> str:
    return f"Search results for '{query}': [results here]"

def calculator(expression: str) -> str:
    result = eval(expression)
    return str(result)

# Map tool NAMES to tool FUNCTIONS (L01 dict pattern!):
TOOL_REGISTRY = {
    "web_search": web_search,
    "calculator": calculator,
}

# Lookup and call:
tool_name   = "calculator"
tool_input  = {"expression": "45 * 12"}
result      = TOOL_REGISTRY[tool_name](**tool_input)
# → calls calculator(expression="45 * 12")
```

**RECOGNIZE THIS:**
- `TOOL_REGISTRY` is a dict mapping name → function (L01!)
- `TOOL_REGISTRY[tool_name]` ← look up function by name
- `(**tool_input)` ← unpack dict as keyword arguments
- Pattern: receive tool name from LLM → look up → execute

**What it does:** "Router that maps LLM's tool request to the actual Python function."

---

### Example 4: The Full Tool Use Loop

```python
def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        # Step 1: Ask LLM
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1000,
            tools=TOOLS,
            messages=messages
        )

        # Step 2: Did LLM finish?
        if response.stop_reason == "end_turn":
            return response.content[0].text          # ← done, return answer

        # Step 3: LLM wants a tool
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name  = block.name
                    tool_input = block.input
                    result     = TOOL_REGISTRY[tool_name](**tool_input)

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": block.id,     # ← match result to request
                        "content":     result
                    })

            # Step 4: Send results back
            messages.append({"role": "user", "content": tool_results})
            # Loop continues — LLM gets results and reasons again
```

**RECOGNIZE THIS:**
- `while True:` ← infinite loop (exits only via `return`)
- `stop_reason == "end_turn"` ← LLM finished, exit the loop
- `stop_reason == "tool_use"` ← LLM wants a tool
- `block.type == "tool_use"` ← extract tool call from response
- `tool_use_id` ← matches the result to the request
- `messages.append(...)` ← conversation grows with each turn (L02!)

**What it does:** "The core agent loop — runs until LLM says it's done."

---

### Example 5: match/case for Stop Reason Routing (2026 Style)

```python
# Old pattern (if/elif):
if response.stop_reason == "end_turn":
    return response.content[0].text
elif response.stop_reason == "tool_use":
    execute_tools(response)

# Modern pattern (match/case — Python 3.10+):
match response.stop_reason:
    case "end_turn":
        return response.content[0].text
    case "tool_use":
        execute_tools(response)
    case "max_tokens":
        handle_truncation()
    case _:
        handle_unexpected()
```

**RECOGNIZE THIS:**
- `match/case` routing by NAME (not a threshold check) → L03 pattern
- `stop_reason` is a string like `"end_turn"` or `"tool_use"`
- Each `case` handles one specific outcome
- `case _:` ← catch-all for anything unexpected

**Rule:** `if/elif` for score thresholds. `match/case` for routing by name/type/status.

---

### Example 6: The ReAct Pattern — Reasoning Visible

```
Query: "What is 15% of the 2024 global AI market size?"

Thought:  I need to find the 2024 AI market size, then calculate 15% of it.
Action:   web_search
Input:    "global AI market size 2024"
Observe:  "Global AI market reached $638.23 billion in 2024"

Thought:  Now I need to calculate 15% of $638.23 billion.
Action:   calculator
Input:    "638.23 * 0.15"
Observe:  "95.7345"

Thought:  I have the answer now.
Final:    15% of the 2024 global AI market is approximately $95.7 billion.
```

**RECOGNIZE THIS:**
- ReAct = **Re**ason → **Act** → **Observe** → repeat
- LLM shows its thinking (Thought)
- LLM picks a tool (Action)
- Your code runs it and returns the result (Observe)
- LLM sees the result and reasons again

**What it does:** "The named pattern for the tool use loop — Thought/Action/Observation printed explicitly."

---

### Example 7: LangChain @tool Shortcut

```python
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_react_agent

# @tool decorator: converts a function into a tool definition automatically
@tool
def web_search(query: str) -> str:
    """Search the web for current information and real-time data."""
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions. Input: Python math expression."""
    return str(eval(expression))

llm    = ChatAnthropic(model="claude-sonnet-5-5")
tools  = [web_search, calculator]

agent  = create_react_agent(llm, tools, prompt)
runner = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

result = runner.invoke({"input": "What is 15% of Apple's market cap?"})
```

**RECOGNIZE THIS:**
- `@tool` ← decorator, converts function into tool definition (no JSON schema needed)
- Docstring `"""..."""` ← becomes the tool description the LLM reads
- `max_iterations=5` ← safety limit, prevents infinite loops
- `verbose=True` ← shows every Thought/Action/Observation step

**What it does:** "LangChain shortcut — turn any Python function into a tool with one line."

---

### Example 8: Good vs Bad Tool Description

```python
# BAD — LLM will use it wrong:
{
    "name": "search",
    "description": "Does a search.",   # too vague!
    ...
}

# GOOD — LLM will use it correctly:
{
    "name": "web_search",
    "description": "Search the internet for current, real-time information. "
                   "Use when you need: recent news, current prices, live data, "
                   "or facts that may have changed after your training cutoff. "
                   "Do NOT use for math calculations or reading local documents.",
    ...
}
```

**RECOGNIZE THIS — the 4-part description formula:**
1. What it does
2. When to use it (specific cases)
3. When NOT to use it
4. What good input looks like

**What it does:** "Description quality = tool selection quality. Vague = wrong tool chosen."

---

## Pattern Recognition Summary

When you see tool use code, ask:

### 1. What part of the pattern is it?
- List of dicts with `name`/`description`/`input_schema` → tool definitions
- `while True:` loop with `stop_reason` checks → tool use loop
- `TOOL_REGISTRY = {"name": function}` → tool lookup table
- `match stop_reason: case "end_turn":` → routing by outcome
- `@tool` decorator on a function → LangChain shortcut

### 2. What stops the loop?
- `stop_reason == "end_turn"` ← LLM finished
- `max_iterations=5` ← safety limit (LangChain)
- Exception raised ← error in tool execution

### 3. How do results get back to the LLM?
- `messages.append({"role": "user", "content": tool_results})` ← appended to message list
- `tool_use_id` ← matches result to the tool request that triggered it

---

## Common Tool Use Signals (Recognition Cheat Sheet)

| You See | It Means |
|:--------|:---------|
| `stop_reason == "tool_use"` | LLM wants to run a tool |
| `stop_reason == "end_turn"` | LLM is done, no more tools |
| `block.type == "tool_use"` | Extracting tool call from response |
| `tool_use_id` | Unique ID matching result to request |
| `@tool` decorator | LangChain auto-converts function to tool |
| `max_iterations=5` | Safety limit — prevents infinite loop |
| `**tool_input` | Unpack dict as keyword arguments |

---

## You've Completed Pass 1!

You can now:
✓ **Recognize** tool definition structure (name/description/input_schema)
✓ **Identify** the tool use loop by its `while True` shape
✓ **Read** `stop_reason` routing patterns
✓ **Spot** the tool registry (name → function dict)
✓ **Understand** the ReAct pattern (Thought/Action/Observe)
✓ **Know** why description quality matters

**Next:**
- **Pass C (Visual):** See the tool use loop as a flowchart
- **Pass 3 (Templates):** Copy ready-to-use tool definitions and the full loop

**Remember:** You're not memorizing. You're training your eyes to SEE patterns.

---

## Pro Tip: The 3-Second Rule

When you see unfamiliar tool use code:
1. **Second 1:** Is it a tool definition, the loop, or the registry?
2. **Second 2:** What `stop_reason` is being handled?
3. **Second 3:** Is the LLM deciding, or is your code executing?

That's it. Tool use is always the same loop. Only the tools change.
