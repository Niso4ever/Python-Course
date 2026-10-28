# Lesson 19 — Pass 3: TEMPLATES
## Your Direct Tool Use Copy-Paste Library

**Goal:** Ready-to-use tool schemas and dispatcher patterns. Copy, rename, connect your real functions.

---

## Template 1: Single Tool — Search
**Use when:** Agent needs to look something up

```python
search_tool = {
    "name": "search_web",
    "description": "Search the web for current information on any topic. Use this when you need facts, news, or data you don't already know.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The specific question or topic to search for"
            }
        },
        "required": ["query"]
    }
}
```

**Example call:**
```python
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024,
    tools=[search_tool],
    messages=[{"role": "user", "content": "What AI models launched in 2026?"}]
)
# response.content[0] → TextBlock("Let me search for that.")
# response.content[1] → ToolUseBlock(name="search_web", input={"query": "AI models launched 2026"})
```

---

## Template 2: Tool with Optional Parameters
**Use when:** Tool has sensible defaults but caller can override them

```python
filter_tool = {
    "name": "filter_results",
    "description": "Filter a list of results by quality score. Returns only high-quality matches.",
    "input_schema": {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of results to filter"
            },
            "threshold": {
                "type": "number",
                "description": "Minimum quality score from 0.0 to 1.0. Default is 0.8.",
                "default": 0.8
            },
            "max_items": {
                "type": "integer",
                "description": "Maximum number of results to return. Default is 5.",
                "default": 5
            }
        },
        "required": ["results"]      # ← threshold and max_items are optional
    }
}
```

**Example calls:**
```python
# Minimal — LLM only provides required field, uses defaults
# LLM generates: block.input = {"results": ["doc1", "doc2", "doc3"]}

# Full — LLM overrides defaults when it needs stricter filtering
# LLM generates: block.input = {"results": [...], "threshold": 0.95, "max_items": 3}
```

---

## Template 3: Tool with Enum Constraint
**Use when:** Parameter must be one of a fixed set of values

```python
format_tool = {
    "name": "format_output",
    "description": "Format text in a specific style for the user.",
    "input_schema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "The text content to format"
            },
            "style": {
                "type": "string",
                "description": "Output format style",
                "enum": ["bullet_points", "numbered_list", "paragraph", "table"]
            },
            "max_length": {
                "type": "integer",
                "description": "Maximum character length of the output"
            }
        },
        "required": ["content", "style"]
    }
}
```

**Example calls:**
```python
# LLM picks from the enum:
# block.input = {"content": "AI news...", "style": "bullet_points"}
# block.input = {"content": "Steps: ...", "style": "numbered_list", "max_length": 500}
# LLM CANNOT generate: {"style": "table_format"} — enum blocks invalid values
```

---

## Template 4: Complete Dispatcher (Required for All Templates)
**Use when:** Need to route tool calls to real Python functions

```python
import json

# Your real tool functions (replace with actual implementations)
def search_web(query: str) -> str:
    return f"[Search result for: {query}]"      # ← replace with real search

def filter_results(results: list, threshold: float = 0.8, max_items: int = 5) -> list:
    return results[:max_items]                   # ← replace with real filter

def format_output(content: str, style: str, max_length: int = 2000) -> str:
    if style == "bullet_points":
        return "\n".join(f"• {line}" for line in content.split(". "))
    return content[:max_length]                  # ← replace with real formatter

# Map names to functions
TOOL_MAP = {
    "search_web":     search_web,
    "filter_results": filter_results,
    "format_output":  format_output,
}

def execute_tools(content_blocks: list) -> list:
    """Process all tool_use blocks. Returns list of tool_result dicts."""
    tool_results = []
    for block in content_blocks:
        if block.type == "tool_use":
            try:
                fn = TOOL_MAP.get(block.name)
                if fn:
                    result = fn(**block.input)
                else:
                    result = f"Error: Unknown tool '{block.name}'"
            except Exception as e:
                result = f"Error in {block.name}: {str(e)}"

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result)
            })
    return tool_results
```

**Example calls:**
```python
results = execute_tools(response.content)
print(results)
# [{"type": "tool_result", "tool_use_id": "toolu_01", "content": "[Search result for: AI news]"}]

# Multiple tools in one response:
results = execute_tools([block1, block2])
print(len(results))   # 2
```

---

## Template 5: Toolkit — Register Multiple Tools
**Use when:** Agent needs access to a suite of tools

```python
# Define all tools for an AI research assistant
RESEARCH_TOOLS = [
    {
        "name": "search_web",
        "description": "Search the internet for current facts, news, and research papers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query":    {"type": "string",  "description": "Search query"},
                "max_results": {"type": "integer", "description": "Max results to return", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "summarize_text",
        "description": "Summarize a long piece of text into a concise version.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text":   {"type": "string",  "description": "Text to summarize"},
                "length": {"type": "string",  "description": "Desired length", "enum": ["short", "medium", "detailed"]}
            },
            "required": ["text", "length"]
        }
    },
    {
        "name": "save_to_report",
        "description": "Save a finding to the research report being compiled.",
        "input_schema": {
            "type": "object",
            "properties": {
                "section": {"type": "string", "description": "Report section name"},
                "content": {"type": "string", "description": "Content to add to that section"}
            },
            "required": ["section", "content"]
        }
    }
]
```

**Example call:**
```python
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=4096,
    tools=RESEARCH_TOOLS,
    messages=[{"role": "user", "content": "Research and write a report on LLM benchmarks in 2026."}]
)
# LLM will use all three tools across multiple loop iterations:
# → search_web("LLM benchmarks 2026") → summarize_text(results) → save_to_report(section="Overview", ...)
```

---

## Template 6: tool_choice Patterns

> **Model restriction (checked 2026-10-28):** `tool_choice={"type": "any"}` and `{"type": "tool", "name": ...}`
> return a 400 error on claude-opus-5-5, claude-sonnet-5-5 and claude-fable-5-1. On those models use the default
> `{"type": "auto"}` and say in the prompt which tool to use; add `"strict": True` to the tool definition for
> schema-exact arguments; or use structured outputs (L04) when you only wanted JSON back. `"none"` still works.
> Source: platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use
**Use when:** You need to control which tool the LLM calls

```python
# Pattern A: LLM chooses (default behavior — no tool_choice)
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024,
    tools=RESEARCH_TOOLS,
    messages=messages
    # no tool_choice → LLM decides
)

# Pattern B: Force LLM to call some tool (any tool)
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024,
    tools=RESEARCH_TOOLS,
    tool_choice={"type": "any"},          # ← must use a tool
    messages=messages
)

# Pattern C: Force a specific tool (useful for structured extraction)
response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024,
    tools=RESEARCH_TOOLS,
    tool_choice={"type": "tool", "name": "save_to_report"},   # ← only this tool
    messages=messages
)
```

**Example calls:**
```python
# Pattern B — guaranteed tool call, great for pipelines
response = client.messages.create(
    tools=[extract_tool], tool_choice={"type": "any"}, messages=messages
)
print(response.stop_reason)  # always "tool_use"

# Pattern C — guaranteed specific tool, great for data extraction
response = client.messages.create(
    tools=[extract_tool], tool_choice={"type": "tool", "name": "extract_data"}, messages=messages
)
print(response.content[0].name)  # always "extract_data"
```

---

## Quick Selection Guide

| Need | Template |
|:-----|:---------|
| Simple lookup tool | Template 1: Single Tool |
| Tool with defaults | Template 2: Optional Parameters |
| Restricted input values | Template 3: Enum Constraint |
| Route calls to functions | Template 4: Complete Dispatcher |
| Agent with many tools | Template 5: Toolkit |
| Control tool selection | Template 6: tool_choice Patterns |
