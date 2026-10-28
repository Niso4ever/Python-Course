"""
CHEATSHEET L07 — Agentic System Design
========================================
Keep this open when reviewing AI-generated agent code
OR when directing AI to build an agentic system.

SECTION 1: DO I NEED AN AGENT?
SECTION 2: HOW MANY AGENTS?
SECTION 3: TOOL SELECTION
SECTION 4: GUARDRAIL PLACEMENT
SECTION 5: MEMORY STRATEGY
SECTION 6: QUICK DESIGN RULES
"""

# ============================================================
# SECTION 1: DO I NEED AN AGENT?
# ============================================================

# USE AN AGENT when:
#   - Task needs real-time or external information (needs tools)
#   - Task requires multi-step reasoning (each step depends on last)
#   - Task requires decisions that change based on runtime conditions
#   - Task is complex enough that LLM can't do it in one call

# DO NOT USE AN AGENT when:
#   - Task is pure Python logic (format, calculate, transform)
#   - Model already knows the answer (definition, common knowledge)
#   - Task is a single structured extraction (use messages.parse(output_format=...), no loop)
#   - Task is too simple for a reasoning loop

# ============================================================
# SECTION 2: HOW MANY AGENTS?
# ============================================================

# ONE agent when:
#   - All steps need the same tools
#   - All steps share the same persona/context
#   - Steps are too short to justify separate agents

# MULTIPLE agents when:
#   - Different steps need genuinely different tools
#   - Quality of step N depends entirely on step N-1 completing first
#   - Different steps have different quality standards

# Rule: Start with one agent. Add agents only when you observe failures
#       that specialization would actually fix.

# ============================================================
# SECTION 3: TOOL SELECTION
# ============================================================

# For each candidate tool, ask:
#   1. Can the agent complete the task WITHOUT this? → YES: remove it
#   2. Is it clear when to use this vs. other tools? → NO: rewrite description
#   3. Could the agent call this at the wrong time? → YES: add "Do NOT use when..."

# TARGET: 3-6 tools per agent
# < 3: agent probably can't complete the task
# 3-6: sweet spot — clear selection, full capability
# > 7: agent gets confused — redesign

# ============================================================
# SECTION 4: GUARDRAIL PLACEMENT
# ============================================================

# THREE required guardrail points in production:

# 1. INPUT GUARDRAIL (before the agent runs)
if not validate_query(user_input):
    return {"error": "Invalid input"}

# 2. LOOP CAP (inside the agent)
for step in range(15):          # ← max 15 iterations
    ...                         # ← agent body
return "Max iterations reached" # ← safe fallback

# 3. OUTPUT GATE (after the agent returns)
gate = quality_gate(question, answer)
if not gate.passes:
    if gate.action == "retry":     return regenerate(question)
    elif gate.action == "escalate": return to_human_review(question)

# ============================================================
# SECTION 5: MEMORY STRATEGY
# ============================================================

# STATELESS (one-shot, no history):
messages = [{"role": "user", "content": question}]

# SESSION (multi-turn, remembers this conversation):
messages = conversation_history + [{"role": "user", "content": question}]
# After response: history.append(answer)

# PERSISTENT (cross-session, stored in DB):
context = db.load(user_id)
messages = [{"role": "system", "content": context}] + [{"role": "user", "content": q}]
# After response: db.save(user_id, new_context)

# TRIM when history gets long:
# history = history[-20:]  ← keep only last 20 messages

# ============================================================
# SECTION 5b: AGENT vs ORCHESTRATION — Pick the Right Pattern
# ============================================================

# AGENT (reasoning loop): LLM decides what to do next at each step
#   Use when: steps are UNKNOWN upfront, depend on runtime conditions
#   Signal:   "I don't know yet if I'll need to search once or three times"

response = client.messages.create(tools=tools, messages=messages)
while response.stop_reason == "tool_use":   # ← LLM keeps deciding
    ...

# ORCHESTRATION (fixed pipeline): You decide the steps, just execute them
#   Use when: steps are KNOWN upfront, always in the same order
#   Signal:   "I always do: fetch → clean → summarize — in that order"

raw      = search(query)          # ← you decide step 1
cleaned  = clean(raw)             # ← you decide step 2
summary  = summarize(cleaned)     # ← you decide step 3

# INSIGHT: Most "agents" in production are actually orchestration.
# Using an LLM agent loop for a fixed 3-step process wastes tokens
# and introduces non-determinism. If you know the steps, just do them.


# ============================================================
# SECTION 5c: TOOL RESULT VALIDATION — Gate bad data before the LLM sees it
# ============================================================

# BAD — feed raw tool output straight back; LLM makes up facts if empty
result = search_tool(query)
messages.append({"role": "user", "content": [{"type": "tool_result",
    "tool_use_id": block.id, "content": str(result)}]})

# GOOD — validate before feeding back
def validate_tool_result(result: str, tool_name: str) -> tuple[str, bool]:
    """Return (validated_content, is_error)."""
    if not result or result.strip() == "[]" or result.strip() == "{}":
        return f"{tool_name} returned no results. Try a different query.", True
    if len(result) > 10_000:
        return result[:10_000] + "... [truncated]", False  # prevent token overflow
    return result, False

content, is_error = validate_tool_result(raw_result, block.name)
tool_result = {"type": "tool_result", "tool_use_id": block.id,
               "content": content, "is_error": is_error}

# INSIGHT: Two common silent failures:
#   1. Empty tool result → LLM hallucinates an answer
#   2. Huge tool result  → context fills up, agent can't finish


# ============================================================
# SECTION 5d: TOKEN GUARDRAILS — Protect the context window
# ============================================================

# Add max_tokens to every agent call — prevents truncation mid-answer
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,               # ← always set; never leave unset
    tools=tools,
    messages=messages
)

# Check if response was truncated:
if response.stop_reason == "max_tokens":
    # Agent didn't finish — handle gracefully
    return {"status": "truncated", "partial": response.content[0].text}

# Context window budget — trim BEFORE it overflows (not after)
# Rough token estimate: 1 token ≈ 4 characters
def estimate_tokens(messages: list[dict]) -> int:
    return sum(len(str(m)) for m in messages) // 4

MAX_CONTEXT = 150_000   # claude-sonnet-5-5 limit

if estimate_tokens(messages) > MAX_CONTEXT * 0.7:   # at 70% capacity
    # Keep: system prompt + last 10 turns + all recent tool results
    messages = messages[:1] + messages[-20:]   # ← trim the middle


# ============================================================
# SECTION 6: QUICK DESIGN RULES
# ============================================================

# DO:
#   ✓ Loop cap (max_iterations)
#   ✓ Input validation before agent runs
#   ✓ Output quality gate before returning to user
#   ✓ System prompt with: role + task + constraints + output format
#   ✓ 3-6 tools per agent max
#   ✓ Tool descriptions: "Use when X, do NOT use when Y"
#   ✓ Demo mode in all templates (runs without API key)
#   ✓ Start simple — one agent first

# DON'T:
#   ✗ while True without a limit
#   ✗ "Be helpful" as system prompt
#   ✗ 10+ tools in one agent
#   ✗ Agent for formatting/simple transforms
#   ✗ 5 agents for something 1 could do
#   ✗ No validation on user input
#   ✗ No quality check on agent output

# THE ARCHITECT'S 4 QUESTIONS:
#   1. Does this NEED an agent? (or is orchestration simpler?)
#   2. Is the tool set MINIMAL? (3-6 tools, all necessary)
#   3. Where can it FAIL? (tool crash, empty result, truncation)
#   4. What happens when it fails? (is_error=True, fallback, escalate)
