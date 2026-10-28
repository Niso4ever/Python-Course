# Lesson 18: The Agent Loop
## The Pattern Behind Every AI Framework

> **2026 Note:** Every agentic framework you've heard of — CrewAI, LangGraph, AutoGen, OpenAI Agents SDK — is a `while` loop with a decision inside it. This lesson teaches that loop using raw Anthropic SDK. When frameworks change (and they will), this pattern doesn't.

## Learning Materials
1. **PASS1_RECOGNITION.md** — Learn to see the loop in any code (START HERE)
2. **PASS_C_VISUAL.md** — See the loop as a flowchart
3. **PASS3_TEMPLATES.md** — Copy-paste agent loop patterns

## Templates
4. **CHEATSHEET_L02.py** — Quick reference (KEEP OPEN while reading agent code)
5. **template_agent_loop.py** — Runnable demo: agent solving a multi-step problem

## The One Shape to Recognize

```python
while True:                                    # ← the loop
    response = client.messages.create(...)     # ← THINK
    if response.stop_reason == "end_turn":     # ← DONE?
        return response.content[0].text        # ← exit
    # else: tool_use                           # ← ACT
    messages.append(tool_results)             # ← OBSERVE → loop again
```

**3-second recognition:** See `while` + `stop_reason` + `messages.append` → you found an agent loop.

## Learning Path
**Step 1:** Read `PASS1_RECOGNITION.md` (30 min)
**Step 2:** Study `PASS_C_VISUAL.md` (15 min)
**Step 3:** Browse `PASS3_TEMPLATES.md` (10 min)
**Step 4:** Run `template_agent_loop.py` to watch the loop execute live
