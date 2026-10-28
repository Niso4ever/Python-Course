# Lesson 13: Tool Use Pattern
## The Swiss Army Knife Theory

> **Version note (checked 2026-10-28):** The LangChain agent code in this lesson is LangChain 0.x style (`from langchain.agents import AgentExecutor, create_react_agent`). You will still meet it in older repos. In LangChain 1.x those legacy pieces live in the separate `langchain-classic` package (`from langchain_classic.agents import AgentExecutor, create_react_agent`), and new code builds agents with `from langchain.agents import create_agent`. The loop you are learning to read is the same.

An LLM without tools is a brilliant person locked in a room with no windows, no internet, no calculator, no phone. They can think and reason perfectly — but only about what they already know, from training data that ended months ago.

**Tools give the LLM hands.** The LLM decides WHEN and HOW to use them. You define WHAT tools exist.

This is the most transformative pattern in AI engineering. Everything you've built so far — classes (L06), functions (L05), logic (L03), loops (L04) — comes together here.

---

## 1. The Core Concept — How Tool Use Works

```
USER:  "What's the weather in Tokyo right now?"

WITHOUT TOOLS:
  LLM: "I don't have real-time weather data. As of my training..."
  ← Knows it can't answer, gives outdated info

WITH TOOLS:
  LLM: "I need to call get_weather('Tokyo')"           ← DECIDES to use tool
  YOUR CODE: get_weather("Tokyo") → {"temp": 18, "condition": "cloudy"}  ← EXECUTES
  LLM: "The current weather in Tokyo is 18°C and cloudy."  ← USES RESULT

The LLM orchestrates. Your code executes. Results feed back in.
```

---

## 2. The Tool Definition Format (JSON Schema)

Every tool is described in a JSON schema that the LLM reads to understand what each tool does:

```python
TOOLS = [
    {
        "name": "web_search",                    # ← What the LLM calls it
        "description": "Search the web for current information. Use when you need "
                       "real-time data, recent news, or facts you're unsure about.",
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
    },
    {
        "name": "calculator",
        "description": "Evaluate mathematical expressions. Use for any calculation "
                       "involving numbers, percentages, or arithmetic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate, e.g. '(45 * 12) / 100'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "read_document",
        "description": "Read the contents of a local document by filename.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The document filename, e.g. 'report.txt'"
                },
                "section": {
                    "type": "string",
                    "description": "Optional: specific section to read"
                }
            },
            "required": ["filename"]     # ← "section" is optional (not in required)
        }
    }
]
```

**The insight:** The `description` field is everything. The LLM reads it to decide when to use the tool. Vague description = wrong tool selection. Precise description = correct tool selection.

---

## 3. The Tool Use Loop — Full Pattern

```python
import anthropic
import json

client = anthropic.Anthropic()

# Your actual tool implementations (L3 functions):
def web_search(query: str) -> str:
    # In reality: call DuckDuckGo, Serper, etc.
    return f"Search results for '{query}': [example results here]"

def calculator(expression: str) -> str:
    try:
        result = eval(expression)   # caution: only use with trusted input
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# Map tool names to functions (L1 dict pattern):
TOOL_REGISTRY = {
    "web_search": web_search,
    "calculator": calculator,
}

def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        # Step 1: Ask LLM (may ask to use a tool)
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1000,
            tools=TOOLS,
            messages=messages
        )

        # Step 2: Did LLM finish? Return the answer.
        if response.stop_reason == "end_turn":
            return response.content[0].text

        # Step 3: LLM wants to use a tool
        if response.stop_reason == "tool_use":
            # Add LLM's response to history
            messages.append({"role": "assistant", "content": response.content})

            # Process each tool call
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name   = block.name
                    tool_input  = block.input

                    print(f"→ Using tool: {tool_name}({tool_input})")

                    # Execute the tool (L2: look up in registry)
                    if tool_name in TOOL_REGISTRY:
                        result = TOOL_REGISTRY[tool_name](**tool_input)
                    else:
                        result = f"Unknown tool: {tool_name}"

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": block.id,
                        "content":     result
                    })

            # Step 4: Send tool results back to LLM
            messages.append({"role": "user", "content": tool_results})
            # Loop continues — LLM now has the result and can reason further
```

**The loop:**
1. User asks question
2. LLM reasons: "do I need a tool?" → If no: return answer → If yes: request tool
3. Your code executes the tool
4. Result sent back to LLM
5. LLM reasons again with the new information
6. Repeat until `stop_reason == "end_turn"`

---

## 2026 Update: match/case for Stop Reason Routing

In 2026 AI agent code you will see `match/case` replacing `if/elif` wherever the code is routing based on **what something IS** (a name, a status, a type) — not checking a threshold.

**Old pattern (if/elif):**
```python
if response.stop_reason == "end_turn":
    return response.content[0].text
elif response.stop_reason == "tool_use":
    execute_tools(response)
```

**Modern pattern (match/case — Python 3.10+):**
```python
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

**Rule:** `if/elif` for thresholds and conditions. `match/case` for routing by name/type/status.

---

## 4. The ReAct Pattern — Reason → Act → Observe

The ReAct pattern formalizes the tool loop into explicit steps:

```
QUERY: "What is 15% of the 2024 global AI market size?"

Thought:  I need to find the 2024 AI market size, then calculate 15% of it.
Action:   web_search
Input:    "global AI market size 2024"
Observe:  "Global AI market reached $638.23 billion in 2024"

Thought:  Now I need to calculate 15% of $638.23 billion.
Action:   calculator
Input:    "638.23 * 0.15"
Observe:  "95.7345"

Thought:  I have the answer now.
Final:    15% of the 2024 global AI market ($638.23 billion) is approximately $95.7 billion.
```

**In LangChain, this is built in:**
```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic

@tool
def web_search(query: str) -> str:
    """Search the web for current information and real-time data."""
    return f"Results for: {query}"   # replace with real search API

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions. Input should be a Python math expression."""
    return str(eval(expression))

llm    = ChatAnthropic(model="claude-sonnet-5-5")
tools  = [web_search, calculator]

# The prompt template for ReAct — LangChain Hub has standard ones:
from langchain import hub
prompt = hub.pull("hwchase17/react")

agent  = create_react_agent(llm, tools, prompt)
runner = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

result = runner.invoke({"input": "What is 15% of the 2024 global AI market size?"})
print(result["output"])
```

---

## 5. Tool Design — The Insight That Changes Everything

**Bad tool (LLM will use it wrong):**
```python
{
    "name": "search",
    "description": "Does a search.",   # ← too vague!
    "input_schema": {
        "properties": {"query": {"type": "string"}},
        "required": ["query"]
    }
}
```

**Good tool (LLM will use it correctly):**
```python
{
    "name": "web_search",
    "description": "Search the internet for current, real-time information. "
                   "Use this when you need: recent news, current prices, live data, "
                   "or any information that may have changed after your training cutoff. "
                   "Do NOT use for mathematical calculations or document reading.",
    "input_schema": {
        "properties": {
            "query": {
                "type": "string",
                "description": "Specific search query. Be precise — include names, dates, "
                               "and specifics. Example: 'anthropic claude 4 release date 2025'"
            }
        },
        "required": ["query"]
    }
}
```

**The golden rule:** Write the description as if you're explaining the tool to a very smart but literal person who has never seen the tool before. Tell them:
- What it does
- When to use it
- When NOT to use it
- What the input should look like

---

## 6. Parallel Tool Calls

Modern Claude models can call multiple tools simultaneously:

```python
# LLM response might contain MULTIPLE tool_use blocks:
for block in response.content:
    if block.type == "tool_use":
        # Could be: web_search AND calculator at the same time
        print(f"Parallel tool: {block.name}({block.input})")
```

**Real example — Claude decides both are needed simultaneously:**
```
Query: "What is 15% of Apple's current market cap?"

Claude calls in parallel:
  tool_use: web_search(query="Apple market cap 2025")
  tool_use: calculator(expression="PLACEHOLDER * 0.15")
→ Your code runs both
→ Claude gets both results
→ Claude substitutes the real market cap and finalizes the calculation
```

---

## 7. Pattern Recognition in Tool-Use Code

**When you see `stop_reason == "tool_use"`:**
→ LLM wants to run a tool. The code will execute a function and loop back.

**When you see `block.type == "tool_use"`:**
→ Extracting a specific tool call from the LLM response.

**When you see `tool_use_id`:**
→ Every tool call has a unique ID — used to match results back to requests.

**When you see `@tool` decorator:**
→ LangChain shortcut — converts a Python function into a tool definition automatically.

**When you see `max_iterations=5`:**
→ Safety limit — prevents infinite loops if LLM keeps calling tools.

---

## 8. Key Takeaways

✓ **Tools = LLM's hands** — you define them, the LLM decides when to use them
✓ **Tool definition = JSON schema** with name, description, input_schema
✓ **Description quality = tool selection quality** — write it precisely
✓ **The loop:** LLM requests tool → your code runs it → result returned → LLM reasons → repeat
✓ **`stop_reason == "end_turn"`** = LLM finished, no more tools needed
✓ **`stop_reason == "tool_use"`** = LLM wants to call something
✓ **ReAct = Reason → Act → Observe** — the named pattern for this loop
✓ **`@tool` decorator** (LangChain) = shortcut to turn any function into a tool

**Phase 1B Insight:** Tool use is the bridge from "chatbot" to "agent." The moment your system can call real APIs, search the web, read files, and run code — it becomes genuinely useful for real-world tasks. The architecture is always the same loop; only the tools change.

---

## Templates Available

See this lesson folder ([./](./)) for:
- `CHEATSHEET_L13.py` — tool patterns quick reference
- `template_tool_definition.py` — 6 ready-to-use tool definitions with excellent descriptions
- `template_tool_executor.py` — complete tool use loop (Anthropic direct)
