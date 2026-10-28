# Phase 5: Anthropic Agent SDK
## From Raw Loop to Managed Agents

> **The 2026 shift:** You learned the engine in Phase 4. Now you learn to drive.
> Phase 4 showed you *how* an agent works. This course shows you *how to build one cleanly*.

---

## The Three-Tier Landscape (2026)

```
┌──────────────────────────────────────────────────────────────────────┐
│  TIER 1 — Raw API   import anthropic                                 │
│  client.messages.create()  →  you write the loop  →  you dispatch    │
│  Phase 4 teaches this. You should read Ph4-L02–L06 first.               │
├──────────────────────────────────────────────────────────────────────┤
│  TIER 2 — Agent SDK   from claude_agent_sdk import query             │
│  SDK handles: loop + tool execution + context + retries              │
│  You provide: tools, system prompt, task. SDK does the rest.         │
│  ← THIS COURSE covers L01–L05                                        │
├──────────────────────────────────────────────────────────────────────┤
│  TIER 3 — Managed Agents   client.beta.agents.create()              │
│  Anthropic's servers run the agent. You define intent + tools.       │
│  Public beta since April 8, 2026; still beta on 2026-10-28.          │
│  ← THIS COURSE introduces in L06                                     │
└──────────────────────────────────────────────────────────────────────┘
```

**The architect's progression:**
- Tier 1 = you built the car from parts
- Tier 2 = you drive a car someone else assembled
- Tier 3 = you order a taxi — describe destination, they handle navigation

---

## Prerequisites

- Phase 4 L02 — The Agent Loop (mandatory — SDK is built on this)
- Phase 3, L01–L02 — Type Hints + Pydantic (tool schemas rely on these)

---

## How to Run Any Template

```bash
# All templates work without an API key in DEMO_MODE
python L01_From_Loop_to_SDK/template_first_sdk_agent.py
python L02_SDK_Tools/template_sdk_tools.py
python L03_Streaming_Agent/template_streaming_agent.py
python L04_Session_Memory/template_session_memory.py
python L05_Subagent_Pipeline/template_subagent_pipeline.py
python L06_Managed_Agents/template_managed_agent.py

# For real API calls: set DEMO_MODE = False and add your key
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Lessons

| # | Lesson | The Shift | Template |
|---|--------|-----------|----------|
| L01 | From Loop to SDK | `while True` → `query()` | `template_first_sdk_agent.py` |
| L02 | SDK Tools | Schema dicts → `@tool` + in-process MCP server | `template_sdk_tools.py` |
| L03 | Streaming Agent | Full response → live token stream | `template_streaming_agent.py` |
| L04 | Session Memory | Stateless calls → `resume=session_id` continuity | `template_session_memory.py` |
| L05 | Subagent Pipeline | One agent → orchestrator + specialist | `template_subagent_pipeline.py` |
| L06 | Managed Agents | Your loop → Anthropic's servers | `template_managed_agent.py` |

---

## What's Deferred (Level Up Phase)

- PASS1_RECOGNITION.md + PASS3_TEMPLATES.md per lesson
- Extended / adaptive thinking (note: `budget_tokens` is rejected on current models; they use `thinking={"type": "adaptive"}` plus `effort`)
- Memory stores (`client.beta.memory_stores`)
- Async parallel agents
- MCP integration (covered in Phase 4 L06)
