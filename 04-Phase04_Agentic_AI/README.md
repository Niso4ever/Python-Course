# Phase 4: Agentic AI
## Direct API Patterns for 2026 and Beyond

> **The 2026 Reality:** Frameworks like CrewAI, LangGraph and AutoGen keep changing their APIs. CrewAI went to 1.0 in October 2025 (pypi.org/project/crewai, retrieved 2026-10-28) and LangChain is on 1.x, so most 2024-era framework code no longer runs as written. What stays the same is the pattern underneath them all. This phase teaches THAT pattern, using the Anthropic SDK directly.

---

## The Shift That Made Frameworks Obsolete

```
2023:  You use LangChain to chain LLM calls              (framework controls everything)
2024:  You use CrewAI / LangGraph to orchestrate agents  (framework controls routing)
2025:  Anthropic + OpenAI expose agent loops at API level (provider does the heavy lifting)
2026+: You talk directly to the API                      (THIS is what you learn here)
```

**Every framework is just a while loop with extra steps.**
Once you see the raw loop, every framework becomes readable.

---

## What You Will Recognize After This Phase

When you see ANY agentic code — CrewAI, LangGraph, OpenAI Agents SDK, raw Anthropic — you will instantly identify:

| Pattern | What to look for |
|:--------|:----------------|
| The agent loop | `while True:` / `while not done:` |
| The decision point | `stop_reason == "end_turn"` vs `"tool_use"` |
| Tool registration | `tools=[{name, description, input_schema}]` |
| Tool dispatch | `if block.type == "tool_use": execute(block.name, block.input)` |
| Conversation growth | `messages.append(...)` every iteration |
| Structured output | `BaseModel` + `messages.parse(output_format=...)` (Anthropic) / `response_format` (OpenAI) |
| Orchestrator handoff | `result = specialist_agent(task)` |
| MCP discovery | `server.list_tools()` → `server.call_tool(name, args)` |

---

## Lessons

| # | Lesson | Core Pattern | Template |
|:--|:-------|:------------|:---------|
| L01 | Introduction to Agentic AI | What it is, use cases, vocabulary | (intro, no template) |
| L02 | The Agent Loop | `while not done: call → decide → act` | `template_agent_loop.py` |
| L03 | Direct Tool Use | `tools=[schema]` → `tool_calls` → dispatch | `template_tool_caller.py` |
| L04 | Structured Output | Pydantic → typed LLM responses | `template_structured_extractor.py` |
| L05 | Multi-Agent Orchestration | Orchestrator → specialists via direct API | `template_orchestrator.py` |
| L06 | MCP — The 2026 Tool Standard | Universal tool discovery and connection | `template_mcp_client.py` |
| L07 | Agentic System Design | When agents, how many, what tools | (architecture, no template) |
| L08 | OpenAI Agents SDK | `Agent + @function_tool + Runner` | `template_openai_agent.py` |

---

## How to Use This Phase

Same three-pass method as Phase 1:

1. **PASS1_RECOGNITION** — Read 8 real code blocks. Don't write. Just see the shape.
2. **PASS_C_VISUAL** — Flowcharts and diagrams. Burn the pattern into memory.
3. **PASS3_TEMPLATES** — Copy, modify, call. Your direct-API agentic toolkit.

**One rule:** `import anthropic` only. No `from crewai import`, no `from langgraph import`.
When frameworks come back in style, you'll read them instantly because you know what's underneath.

---

## The Three Things an Agent Actually Does

```
1. THINK    → Ask the LLM what to do next
2. ACT      → Execute a tool (or not)
3. OBSERVE  → Feed the result back and repeat
```

That's it. Every agent system ever built does exactly this — in a loop.
```
User input
    │
    ▼
┌─────────────────────────┐
│         THINK           │ ← client.messages.create(...)
│    (LLM decides)        │
└─────────────────────────┘
         │
    ┌────┴────┐
    │         │
  ACT      DONE
    │         │
    ▼         ▼
 execute   return answer
  tool
    │
    ▼
 OBSERVE
(feed result back)
    │
    └──→ loop again
```

**The loop is the agent. Everything else is configuration.**
