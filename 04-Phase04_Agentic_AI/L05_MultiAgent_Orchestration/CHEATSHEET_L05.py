"""
CHEATSHEET L05 — Multi-Agent Orchestration
============================================
Keep this open while reading multi-agent code.

SECTION 1: PATTERN QUICK REFERENCE
SECTION 2: SPECIALIST = run_agent + config
SECTION 3: ROUTING PATTERNS
SECTION 4: FRAMEWORK TRANSLATION
SECTION 5: 3-SECOND RECOGNITION
"""

# ============================================================
# SECTION 1: PATTERN QUICK REFERENCE
# ============================================================

# ROUTER:       classify → if/elif → specialist()
# PIPELINE:     A(input) → B(A_output) → C(B_output)
# PARALLEL:     asyncio.gather(A, B, C)
# SWARM:        for sub_topic in discovered: specialist(sub_topic)
# AGENT-AS-TOOL: run_agent(tools=[agent_schema1, agent_schema2])

# ============================================================
# SECTION 2: SPECIALIST = run_agent + config
# ============================================================

# Every specialist is the SAME loop with different configuration:
def any_specialist(task: str, system_prompt: str, tool_list: list) -> str:
    return run_agent(                    # ← L02 loop
        question=task,
        tools=tool_list,                 # ← domain tools
        system=system_prompt             # ← persona/role
    )

# Shorthand:
research_agent = lambda task: run_agent(task, tools=RESEARCH_TOOLS, system=RESEARCH_PROMPT)
writer_agent   = lambda task: run_agent(task, tools=WRITING_TOOLS,  system=WRITER_PROMPT)
analyst_agent  = lambda task: run_agent(task, tools=ANALYST_TOOLS,  system=ANALYST_PROMPT)

# ============================================================
# SECTION 3: ROUTING PATTERNS
# ============================================================

# Pattern A: if/elif routing
def route_simple(request, intent):
    if intent == "research": return research_agent(request)
    elif intent == "write":  return writer_agent(request)
    else:                    return fallback_agent(request)

# Pattern B: dict routing (cleaner)
AGENTS = {
    "research": research_agent,
    "write":    writer_agent,
    "analyse":  analyst_agent,
}
def route_dict(request, intent):
    fn = AGENTS.get(intent, fallback_agent)
    return fn(request)

# ============================================================
# SECTION 4: FRAMEWORK TRANSLATION
# ============================================================

# CrewAI → Direct API:
# Agent(role="X", tools=[...])    → run_agent(system="You are X", tools=[...])
# Task(context=[prev_task])       → agent(f"Context: {prev_result}\n{task}")
# crew.kickoff()                  → orchestrate(user_request)

# LangGraph → Direct API:
# @node("research")               → def research_agent(task): return run_agent(...)
# graph.add_edge(A, B)            → B_out = B_agent(A_agent(input))
# graph.invoke(state)             → orchestrate(user_input)

# ============================================================
# SECTION 5: 3-SECOND RECOGNITION
# ============================================================

# When you see multi-agent code, look for:
#
# 1. CLASSIFY  → LLM or if/elif routes to a specialist
# 2. DELEGATE  → specialist_agent(task) or system.run(name, task)
# 3. HANDOFF   → result of one agent = input of next
#
# See all 3 → multi-agent orchestration confirmed.
"""
MINIMAL COMPLETE EXAMPLE:

research_agent = lambda q: run_agent(q, tools=[search_tool], system="You are a researcher.")
writer_agent   = lambda q: run_agent(q, tools=[],            system="You are a writer.")

def orchestrate(request):
    research = research_agent(request)    # ← specialist 1
    article  = writer_agent(research)     # ← specialist 2 (handoff)
    return article

result = orchestrate("Explain MCP")
print(result)   # polished article about MCP
"""
