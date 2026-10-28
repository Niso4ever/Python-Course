# Lesson: Async Patterns for Agents
## Run Multiple Agents at the Same Time — Without Breaking Anything

> **2026 Note:** Every production multi-agent system runs agents concurrently. The `continual-learning-bench` you reviewed runs baseline instances in parallel. Claude itself can ask for several tool calls in a single response, and your code is expected to run them, often at the same time. Without async literacy, you can't read or direct these systems.

## Why This Lesson Exists

You already know:
- The agent loop (Ph4-L02)
- Multi-agent orchestration (Ph4-L05)
- SDK streaming (L03)

**What's missing:** All those systems run agents one at a time. In production, you run 3 agents simultaneously and merge their results. That requires `async/await` — and the patterns are simple once you see them.

## Learning Materials
1. **PASS1_RECOGNITION.md** — Learn to spot async patterns in real agent code (START HERE)
2. **PASS_C_VISUAL.md** — Sequential vs concurrent execution diagrams
3. **PASS3_TEMPLATES.md** — 5 copy-paste async patterns for agents

## Templates
4. **CHEATSHEET_L01.py** — Quick reference (KEEP OPEN while reading async agent code)
5. **template_parallel_agents.py** — Runnable demo: 3 agents running concurrently via `gather`

## The One Shape to Recognize

```python
# Sequential — slow, one at a time
result1 = await agent_research(query)    # waits 3 sec
result2 = await agent_write(query)       # waits 3 sec
result3 = await agent_review(query)      # waits 3 sec
# Total: 9 seconds

# Concurrent — fast, all at once
result1, result2, result3 = await asyncio.gather(
    agent_research(query),               # ─┐
    agent_write(query),                  # ─┤ all run at same time
    agent_review(query),                 # ─┘
)
# Total: 3 seconds (longest single agent)
```

**3-second recognition:** See `asyncio.gather(` → multiple coroutines inside → you found parallel agent execution.

## Learning Path
**Step 1:** Read `PASS1_RECOGNITION.md` (25 min)
**Step 2:** Study `PASS_C_VISUAL.md` (10 min)
**Step 3:** Browse `PASS3_TEMPLATES.md` (15 min)
**Step 4:** Run `template_parallel_agents.py` to watch concurrent agents in action
