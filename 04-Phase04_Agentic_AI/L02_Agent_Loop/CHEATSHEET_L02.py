"""
CHEATSHEET L02 — The Agent Loop
================================
Keep this open while reading agent code.
RECOGNIZE shapes, don't memorize syntax.

SECTION 1: THE LOOP SHAPES
SECTION 2: THE DECISION POINT
SECTION 3: MESSAGE ACCUMULATION
SECTION 4: TOOL DISPATCHER
SECTION 5: FRAMEWORK TRANSLATION
SECTION 6: 3-SECOND RECOGNITION RULE
"""

# ============================================================
# SECTION 1: THE LOOP SHAPES (all equivalent)
# ============================================================

# Shape A: while True (simplest)
while True:
    pass   # ← LLM call + decision inside

# Shape B: flag-controlled
done = False
while not done:
    pass   # ← set done = True when "end_turn"

# Shape C: capped with counter (safest)
for step in range(15):
    pass   # ← return inside when "end_turn", fallback after loop

# ============================================================
# SECTION 2: THE DECISION POINT (Anthropic vs OpenAI)
# ============================================================

# Anthropic SDK:
# response.stop_reason == "end_turn"    ← done, return answer
# response.stop_reason == "tool_use"    ← needs tools, keep looping

# OpenAI SDK:
# response.choices[0].finish_reason == "stop"        ← done (same as "end_turn")
# response.choices[0].finish_reason == "tool_calls"  ← tools needed (same as "tool_use")

# ============================================================
# SECTION 3: MESSAGE ACCUMULATION
# ============================================================

# PATTERN: every tool call iteration appends 2 messages
messages = [{"role": "user", "content": "..."}]   # start: 1 message

# After each tool call:
messages.append({"role": "assistant", "content": response.content})   # agent's request
messages.append({"role": "user",      "content": tool_results})        # tool answer
# messages now has 3 items. Next tool call → 5. Next → 7. Then final answer → 8.

# ============================================================
# SECTION 4: TOOL DISPATCHER
# ============================================================

def execute_tools(content_blocks):
    results = []
    for block in content_blocks:
        if block.type == "tool_use":              # ← filter: only tool requests
            result = dispatch(block.name, block.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,          # ← MUST match block.id
                "content": str(result)
            })
    return results

def dispatch(tool_name, tool_input):
    tool_map = {
        "search_web": search_web,                 # ← add your tools here
        "read_file":  read_file,
    }
    fn = tool_map.get(tool_name)
    return fn(**tool_input) if fn else f"Unknown: {tool_name}"

# ============================================================
# SECTION 5: FRAMEWORK TRANSLATION
# ============================================================

# CrewAI:
#   crew.kickoff()                → run_agent(question)

# LangGraph:
#   graph.invoke({"input": q})   → run_agent(q)

# OpenAI Agents SDK:
#   Runner.run(agent, input)     → run_agent(question)

# AutoGen:
#   agent.initiate_chat(...)     → run_agent(question)

# ============================================================
# SECTION 6: THE 3-SECOND RECOGNITION RULE
# ============================================================

# When you see agent code, scan for:
#
# 1. LOOP    → "while" or "for _ in range(...)"
# 2. DECIDE  → "stop_reason" or "finish_reason"
# 3. GROW    → "messages.append(...)"
#
# If you see all three → you found an agent loop.
# Everything else is config or decoration.
"""
COMPLETE MINIMAL AGENT (reference):

import anthropic
client = anthropic.Anthropic()

def run_agent(question, tools):
    messages = [{"role": "user", "content": question}]
    while True:                                              # 1. LOOP
        response = client.messages.create(
            model="claude-opus-5-5", max_tokens=4096,
            tools=tools, messages=messages
        )
        if response.stop_reason == "end_turn":              # 2. DECIDE
            return response.content[0].text
        messages.append({"role": "assistant",               # 3. GROW
                         "content": response.content})
        results = execute_tools(response.content)
        messages.append({"role": "user", "content": results})
"""
