"""
CHEATSHEET L03 — Direct Tool Use
==================================
Keep this open while reading tool-calling code.

SECTION 1: TOOL SCHEMA ANATOMY
SECTION 2: INPUT SCHEMA TYPES
SECTION 3: RESPONSE PARSING
SECTION 4: TOOL RESULT FORMAT
SECTION 5: TOOL_CHOICE OPTIONS
SECTION 6: 3-SECOND RECOGNITION
"""

# ============================================================
# SECTION 1: TOOL SCHEMA ANATOMY
# ============================================================

my_tool = {
    "name": "tool_name",                      # ← identity
    "description": "What it does and WHEN to use it",   # ← LLM decision logic
    "input_schema": {
        "type": "object",                     # ← always "object"
        "properties": {
            "required_param": {
                "type": "string",
                "description": "What this is"
            },
            "optional_param": {
                "type": "integer",
                "description": "Optional setting",
                "default": 5                  # ← hint for optional
            },
            "constrained_param": {
                "type": "string",
                "enum": ["option_a", "option_b"]   # ← restrict values
            }
        },
        "required": ["required_param"]        # ← only these are mandatory
    }
}

# ============================================================
# SECTION 2: INPUT SCHEMA TYPES
# ============================================================

# "type": "string"   → any text
# "type": "integer"  → whole number
# "type": "number"   → float/decimal
# "type": "boolean"  → True / False
# "type": "array", "items": {"type": "string"}  → list of strings
# "type": "object"   → nested dict

# ============================================================
# SECTION 3: RESPONSE PARSING
# ============================================================

# After client.messages.create(tools=[...], messages=[...]):
for block in response.content:
    if block.type == "tool_use":     # ← filter: only tool calls
        name  = block.name           # ← which tool
        args  = block.input          # ← arguments dict
        call_id = block.id           # ← unique id (keep it!)

# ============================================================
# SECTION 4: TOOL RESULT FORMAT
# ============================================================

# Result must include the matching tool_use_id:
tool_result = {
    "type": "tool_result",
    "tool_use_id": block.id,         # ← MUST match block.id exactly
    "content": str(your_result)      # ← always convert to string
}

# Feed results back as a user message:
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user",      "content": [tool_result]})

# ============================================================
# SECTION 5: TOOL_CHOICE OPTIONS
# ============================================================

# Default: LLM decides
#   (no tool_choice param)

# Force a tool call (any tool):  — 400 on claude-opus-5-5 / claude-sonnet-5-5 / claude-fable-5-1
#   tool_choice = {"type": "any"}   (on those models: "auto" + prompt instruction + "strict": True on the tool)

# Force a specific tool:
#   tool_choice = {"type": "tool", "name": "my_tool_name"}

# ============================================================
# SECTION 6: 3-SECOND RECOGNITION
# ============================================================

# Look for these 4 things to spot tool use code:
#
# 1. SCHEMA   → dict with "name", "description", "input_schema"
# 2. REGISTER → tools=[...] in client.messages.create()
# 3. DETECT   → block.type == "tool_use"
# 4. RETURN   → "type": "tool_result", "tool_use_id": block.id
#
# Spot all 4 → you found direct tool use.

# ============================================================
# SECTION 7: PARALLEL TOOL CALLS
# ============================================================

# Claude can request MULTIPLE tools in one response.
# All blocks with type == "tool_use" must be executed.

tool_results = []
for block in response.content:
    if block.type == "tool_use":
        result = dispatch(block.name, block.input)   # run each
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": str(result)
        })

# Return ALL results in a single user message (not one per tool):
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user",      "content": tool_results})  # ← list of all

# INSIGHT: If Claude calls search("Paris") AND search("Berlin") in parallel,
# execute both, collect both results, return both in one message.
# Returning them separately breaks the conversation.


# ============================================================
# SECTION 8: ERROR TOOL RESULT — Tell Claude a tool failed
# ============================================================

# If your tool crashes or returns bad data, don't silently pass an empty string.
# Use is_error=True to tell Claude what went wrong — it will adjust its strategy.

# Tool succeeded:
success_result = {
    "type": "tool_result",
    "tool_use_id": block.id,
    "content": "The population of Tokyo is 13.96 million."
}

# Tool failed:
error_result = {
    "type": "tool_result",
    "tool_use_id": block.id,
    "is_error": True,                         # ← flag the failure
    "content": "Search failed: rate limit exceeded. Try again in 60 seconds."
}

# INSIGHT: With is_error=True, Claude will typically:
# 1. Try a different approach or rephrase the query
# 2. Use its own knowledge instead
# 3. Tell the user why it couldn't complete the task
# Without it: Claude silently uses an empty result and hallucinates.


"""
MINIMAL COMPLETE EXAMPLE:

tools = [{
    "name": "search_web",
    "description": "Search the web.",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"]
    }
}]

response = client.messages.create(
    model="claude-opus-4-6", max_tokens=1024,
    tools=tools, messages=messages
)

results = []
for block in response.content:
    if block.type == "tool_use":
        result = web_search(block.input["query"])
        results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})

messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user",      "content": results})
"""
