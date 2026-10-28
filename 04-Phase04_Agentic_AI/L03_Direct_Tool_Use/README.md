# Lesson 19: Direct Tool Use
## How LLMs Call Functions — No Framework Required

> **2026 Note:** In 2024, you defined tools through CrewAI decorators (`@tool`) or LangChain wrappers. By 2026 those abstractions are gone. Tools are JSON schemas passed directly to the API. This lesson teaches the raw pattern.

## Learning Materials
1. **PASS1_RECOGNITION.md** — Learn to read tool schemas and dispatch code (START HERE)
2. **PASS_C_VISUAL.md** — See the tool call flow as a diagram
3. **PASS3_TEMPLATES.md** — Copy-paste tool patterns

## Templates
4. **CHEATSHEET_L03.py** — Quick reference (KEEP OPEN while reading tool code)
5. **template_tool_caller.py** — Runnable demo: agent using 3 different tools

## The One Shape to Recognize

```python
# 1. DEFINE: tell the LLM what tools exist
tools = [{"name": "search", "description": "...", "input_schema": {...}}]

# 2. REGISTER: pass tools to the API
response = client.messages.create(tools=tools, messages=messages)

# 3. PARSE: find tool_use blocks in the response
for block in response.content:
    if block.type == "tool_use":          # ← tool was called
        result = my_function(**block.input)

# 4. RETURN: feed results back as user message
{"type": "tool_result", "tool_use_id": block.id, "content": result}
```

**3-second recognition:** See `input_schema` + `block.type == "tool_use"` + `tool_use_id` → you found direct tool use.

## Learning Path
**Step 1:** Read `PASS1_RECOGNITION.md` (30 min)
**Step 2:** Study `PASS_C_VISUAL.md` (15 min)
**Step 3:** Browse `PASS3_TEMPLATES.md` (10 min)
**Step 4:** Run `template_tool_caller.py` to see tool calls happen live
