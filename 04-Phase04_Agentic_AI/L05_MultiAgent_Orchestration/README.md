# Lesson 21: Multi-Agent Orchestration
## One Orchestrator, Many Specialists — No Framework Required

> **2026 Note:** CrewAI and LangGraph introduced multi-agent systems by wrapping the pattern in decorators and graph nodes. By 2026, most teams run multi-agent systems using pure API calls — an orchestrator agent decides what to do, calls specialist agents as functions. This lesson teaches that raw pattern.

## Learning Materials
1. **PASS1_RECOGNITION.md** — Learn to read orchestrator/specialist patterns (START HERE)
2. **PASS_C_VISUAL.md** — See the routing and handoff flow
3. **PASS3_TEMPLATES.md** — Copy-paste orchestration patterns

## Templates
4. **CHEATSHEET_L05.py** — Quick reference (KEEP OPEN while reading multi-agent code)
5. **template_orchestrator.py** — Runnable demo: 3 specialists + 1 orchestrator

## The One Shape to Recognize

```python
# Orchestrator routes to specialists
def orchestrate(user_request: str) -> str:
    intent = classify(user_request)          # ← decide who handles it

    if intent == "research":
        return research_agent(user_request)  # ← specialist 1
    elif intent == "write":
        return writer_agent(user_request)    # ← specialist 2
    else:
        return fallback_agent(user_request)  # ← fallback

# Each specialist is just run_agent() with different tools + system prompt
research_agent = lambda q: run_agent(q, tools=research_tools, system=RESEARCH_PROMPT)
writer_agent   = lambda q: run_agent(q, tools=writing_tools,  system=WRITER_PROMPT)
```

**3-second recognition:** See `classify/route` → `specialist_agent(task)` → result returned up → you found a multi-agent system.

## Learning Path
**Step 1:** Read `PASS1_RECOGNITION.md` (30 min)
**Step 2:** Study `PASS_C_VISUAL.md` (15 min)
**Step 3:** Browse `PASS3_TEMPLATES.md` (10 min)
**Step 4:** Run `template_orchestrator.py` to watch routing in action
