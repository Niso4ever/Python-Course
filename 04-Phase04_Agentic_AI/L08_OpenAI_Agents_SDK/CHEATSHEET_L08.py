"""
CHEATSHEET L08 — OpenAI Agents SDK
====================================
Keep this open when reading or directing AI to build
agents with the OpenAI Agents SDK.

SECTION 1: CORE OBJECTS
SECTION 2: @function_tool — HOW TO WRITE TOOLS
SECTION 3: RUNNER — HOW TO RUN AGENTS
SECTION 4: MULTI-AGENT HANDOFFS
SECTION 5: GUARDRAILS
SECTION 6: TRANSLATION TABLE (Anthropic ↔ OpenAI SDK)
"""

# ============================================================
# SECTION 1: CORE OBJECTS
# ============================================================

from agents import Agent, Runner, function_tool

# AGENT — the definition
agent = Agent(
    name="Researcher",                    # who this agent is
    instructions="You are a...",          # system prompt (role + task + constraints)
    model="gpt-4o",                       # optional — default is no longer gpt-4o (SDK docs, 2026-10-28: gpt-5.6-luna)
    tools=[],                             # list of @function_tool functions
    handoffs=[],                          # list of specialist agents
    input_guardrails=[],                  # run BEFORE agent starts
    output_guardrails=[],                 # run AFTER agent finishes
)

# RUNNER — runs the loop
result = Runner.run_sync(agent, "question")        # synchronous
# result = await Runner.run(agent, "question")     # async version

# RESULT — what comes back
result.final_output      # str: the agent's answer
result.messages          # list: full conversation history
result.last_agent        # Agent: who produced the final answer
result.new_messages      # list: only messages added this run


# ============================================================
# SECTION 2: @function_tool — HOW TO WRITE TOOLS
# ============================================================

# BASIC TOOL — required parameter
@function_tool
def search_web(query: str) -> str:
    """Search the web for current information on a topic.
    Use this when the user asks about recent events or news."""
    return f"Results for: {query}"   # replace with real logic

# TOOL WITH OPTIONAL PARAMETER
@function_tool
def get_weather(city: str, unit: str = "celsius") -> str:
    """Get current weather for a city. Unit can be 'celsius' or 'fahrenheit'."""
    return f"Weather in {city}: 22°{unit[0].upper()}"

# TOOL WITH MULTIPLE REQUIRED PARAMS
@function_tool
def calculate_roi(revenue: float, cost: float) -> str:
    """Calculate return on investment. Use when given revenue and cost figures."""
    roi = ((revenue - cost) / cost) * 100
    return f"ROI: {roi:.1f}%"

# RULES FOR TOOLS:
#   ✓ Use type hints — they become the JSON schema
#   ✓ Docstring = what the LLM reads to decide when to call this tool
#   ✓ Always return str (or something str()-able)
#   ✓ Add "Do NOT use when X" in docstring if needed
#   ✓ Keep to 3-6 tools per agent (same rule as L07)


# ============================================================
# SECTION 3: RUNNER — HOW TO RUN AGENTS
# ============================================================

import asyncio

# SYNCHRONOUS (simple, blocking):
result = Runner.run_sync(agent, "What is MCP?")
print(result.final_output)

# ASYNC (non-blocking, needed for parallel):
async def run_once():
    result = await Runner.run(agent, "What is MCP?")
    return result.final_output

output = asyncio.run(run_once())

# PARALLEL (multiple agents at same time):
async def run_parallel(tasks):
    results = await asyncio.gather(*[Runner.run(agent, t) for t in tasks])
    return [r.final_output for r in results]

outputs = asyncio.run(run_parallel(["task 1", "task 2", "task 3"]))


# ============================================================
# SECTION 4: MULTI-AGENT HANDOFFS
# ============================================================

# Specialist agents (focused, with their own tools):
researcher = Agent(
    name="Researcher",
    instructions="Research topics thoroughly. Cite all sources.",
    tools=[search_web],
)

writer = Agent(
    name="Writer",
    instructions="Write clear, engaging content from research provided.",
)

# Orchestrator routes to specialists:
orchestrator = Agent(
    name="ContentPipeline",
    instructions="""Manage the content pipeline:
    1. Hand off to Researcher to gather information.
    2. Hand off to Writer to produce final content.
    Return the finished article.""",
    handoffs=[researcher, writer],
)

result = Runner.run_sync(orchestrator, "Write about agentic AI in 2026")
print(result.final_output)
print(f"Last agent: {result.last_agent.name}")   # "Writer"

# HANDOFF RULES:
#   ✓ Orchestrator's instructions must describe WHEN to hand off to WHOM
#   ✓ Specialists should have focused instructions (narrow role)
#   ✓ result.last_agent tells you which specialist produced the final answer


# ============================================================
# SECTION 5: GUARDRAILS
# ============================================================

from agents import input_guardrail, output_guardrail, GuardrailFunctionOutput

# INPUT GUARDRAIL — runs before agent starts:
@input_guardrail
async def block_sensitive(ctx, agent, input) -> GuardrailFunctionOutput:
    """Block sensitive or off-topic input before the agent runs."""
    blocked = ["lawsuit", "salary", "confidential"]
    if any(word in input.lower() for word in blocked):
        return GuardrailFunctionOutput(
            output_info="Sensitive topic detected",
            tripwire_triggered=True,       # ← BLOCKS the agent
        )
    return GuardrailFunctionOutput(tripwire_triggered=False)  # ← ALLOWS the agent

# OUTPUT GUARDRAIL — runs after agent finishes:
@output_guardrail
async def check_quality(ctx, agent, output) -> GuardrailFunctionOutput:
    """Ensure the answer is not empty or too short."""
    if len(output.final_output) < 50:
        return GuardrailFunctionOutput(
            output_info="Answer too short",
            tripwire_triggered=True,
        )
    return GuardrailFunctionOutput(tripwire_triggered=False)

# Attach to agent:
safe_agent = Agent(
    name="SafeBot",
    instructions="You are a product assistant.",
    input_guardrails=[block_sensitive],
    output_guardrails=[check_quality],
)

# Handle tripwire exceptions:
async def run_safe(question):
    try:
        result = await Runner.run(safe_agent, question)
        return result.final_output
    except Exception as e:
        return f"Blocked: {e}"


# ============================================================
# SECTION 6: TRANSLATION TABLE (Anthropic ↔ OpenAI Agents SDK)
# ============================================================

# PURPOSE                  ANTHROPIC (L02-L06)              OPENAI AGENTS SDK
# ─────────────────────────────────────────────────────────────────────────────
# System prompt       →    messages=[{"role":"system",...}]  Agent(instructions=...)
# Define tool         →    {"name":..., "input_schema":...}  @function_tool
# Run loop            →    while True: + stop_reason         Runner.run_sync(...)
# Multi-agent         →    result = run_specialist(task)     Agent(handoffs=[...])
# Input validation    →    if not validate(input): return    @input_guardrail
# Output validation   →    if not quality_gate(out): retry   @output_guardrail
# Get answer          →    response.content[0].text          result.final_output
# Async               →    AsyncAnthropic + asyncio.gather   Runner.run + gather
# Model config        →    model="claude-opus-5-5"           model="gpt-4o"

# THE RULE: If you can read L02–L06 code, you can read OpenAI Agents SDK code.
#           The patterns are the same. Only the syntax changes.
