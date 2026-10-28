"""
═══════════════════════════════════════════════════════════════════
LESSON 13 CHEATSHEET: Tool Use Pattern
═══════════════════════════════════════════════════════════════════
Function calling, ReAct loop, tool definitions.

2026 update: match/case replaces if/elif for stop_reason routing.
═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. THE TOOL USE LOOP (3 PHASES)
# ═══════════════════════════════════════════════════════════
"""
PHASE 1: DEFINE
  Tools = JSON schema (name + description + input_schema)
  Tool Registry = dict mapping name → actual function

PHASE 2: LOOP (2026 pattern — match/case for stop_reason)
  while True:
      response = client.messages.create(tools=TOOLS, messages=messages)

      match response.stop_reason:
          case "end_turn":
              return response.content[0].text   ← DONE
          case "tool_use":
              for each tool_use block:
                  result = REGISTRY[block.name](**block.input)
              send results back to LLM
              continue loop
          case "max_tokens":
              handle_truncation()
          case _:
              handle_unexpected()

  (Old style still works: if stop_reason == "end_turn": ...)

PHASE 3: RESULT
  LLM uses tool results to compose final answer
"""

# ═══════════════════════════════════════════════════════════
# 2. TOOL DEFINITION SKELETON
# ═══════════════════════════════════════════════════════════
TOOL_SKELETON = {
    "name": "tool_name",                    # snake_case, descriptive
    "description": (
        "What it does. When to use it. When NOT to use it."
        # ↑ The most important field. LLM reads this to decide.
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "required_param": {
                "type": "string",           # string, integer, boolean, array, object
                "description": "What this input means and example values"
            },
            "optional_param": {
                "type": "integer",
                "description": "Optional parameter with default behavior"
            }
        },
        "required": ["required_param"]      # optional_param is NOT listed → optional
    }
}

# ═══════════════════════════════════════════════════════════
# 3. STOP REASON MEANINGS
# ═══════════════════════════════════════════════════════════
"""
response.stop_reason == "end_turn"   → LLM finished. Return the text.
response.stop_reason == "tool_use"   → LLM wants a tool. Execute, loop back.
response.stop_reason == "max_tokens" → Hit token limit. Increase max_tokens.
response.stop_reason == "stop_sequence" → Hit a custom stop string.
"""

# ═══════════════════════════════════════════════════════════
# 4. EXTRACTING TOOL CALLS FROM RESPONSE
# ═══════════════════════════════════════════════════════════
"""
for block in response.content:
    if block.type == "tool_use":
        tool_name  = block.name       # e.g. "web_search"
        tool_input = block.input      # e.g. {"query": "AI news"}
        tool_id    = block.id         # unique ID — needed for result

# Return result to LLM:
tool_results.append({
    "type":        "tool_result",
    "tool_use_id": block.id,     # ← must match the request ID
    "content":     str(result)   # ← always stringify the result
})
messages.append({"role": "user", "content": tool_results})
"""

# ═══════════════════════════════════════════════════════════
# 5. LANGCHAIN @tool SHORTCUT
# ═══════════════════════════════════════════════════════════
"""
from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    \"\"\"Search the internet for current information. Use for real-time data.\"\"\"
    return search_api(query)

# The docstring becomes the tool description!
# The function signature becomes the input schema!
# No need to write JSON schema manually.

Usage:
  tools  = [web_search, calculator]
  agent  = create_react_agent(llm, tools, prompt)
  runner = AgentExecutor(agent=agent, tools=tools)
"""

# ═══════════════════════════════════════════════════════════
# 6. REACT PATTERN
# ═══════════════════════════════════════════════════════════
"""
ReAct = Reason → Act → Observe (loop until done)

Thought:  "I need current weather in Tokyo"
Action:   web_search
Input:    "Tokyo weather right now"
Observe:  "18°C, cloudy"

Thought:  "I have the answer"
Final:    "Current weather in Tokyo: 18°C and cloudy"

LangChain builds this loop automatically.
Anthropic direct: you build the loop in Python.
"""

# ═══════════════════════════════════════════════════════════
# 7. TOOL DESCRIPTION QUALITY GUIDE
# ═══════════════════════════════════════════════════════════
"""
BAD (LLM picks wrong tool):
  "description": "Does a search."

GOOD (LLM picks correctly):
  "description": (
      "Search the internet for current, real-time information. "
      "Use when you need: recent news, live prices, current events. "
      "Do NOT use for: calculations, reading local files, things you already know."
  )

RULE: Describe it like you're training a new employee who's never seen the tool.
Include: what it does + when to use it + when NOT to use it + input example.
"""

# ═══════════════════════════════════════════════════════════
# 8. PATTERN RECOGNITION GUIDE
# ═══════════════════════════════════════════════════════════
"""
You see                              You understand
────────────────────────────────     ────────────────────────────────────────
stop_reason == "tool_use"            LLM wants to call a function
block.type == "tool_use"             Extract tool name + input from this block
tool_use_id                          Unique ID to match result back to request
return_exceptions=True               Gather won't crash if one tool fails
max_iterations=5 in AgentExecutor    Safety limit for the tool loop
@tool decorator                      LangChain converts function → tool definition
create_react_agent(llm, tools, p)    LangChain builds a ReAct agent
AgentExecutor(agent, tools)          LangChain runs the tool loop
verbose=True                         Print every Thought/Action/Observe step
"""

# ═══════════════════════════════════════════════════════════
# 9. COMMON TOOL USE MISTAKES
# ═══════════════════════════════════════════════════════════
"""
MISTAKE 1: Tool result not stringified
  tool_results.append({"content": result})      ← might be dict
  FIX: tool_results.append({"content": str(result)})

MISTAKE 2: Missing tool_use_id
  {"type": "tool_result", "content": result}    ← missing id field!
  FIX: {"type": "tool_result", "tool_use_id": block.id, "content": result}

MISTAKE 3: Infinite loop (no max iterations)
  Add: max_iterations = 10; break if exceeded

MISTAKE 4: Vague tool description
  LLM calls wrong tool or calls none
  FIX: Rewrite description with when to use + when not to use

MISTAKE 5: Tool crashes silently
  Wrap tool execution in try/except, return error string (not raise)
"""

print("Tool use cheatsheet loaded!")
print("Key: stop_reason='tool_use' → execute → return result → loop.")
