# Phase 5 — Anthropic Agent SDK (Ph5-L01–L06, 6 templates)

Tiers 2 and 3 of the landscape. The whole point of the SDK is that the loop you
hand-wrote in Phase 4 disappears — so these vibe prompts get *shorter*. You stop
specifying the engine and start specifying the **intent + tools**. That shift is
the lesson.

---

## 47. `template_first_sdk_agent.py` — Ph5-L01 From Loop to SDK
**Level 2 (Behavior) · Mode 2 (Specification)**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: from claude_agent_sdk import query. NO hand-written loop. @dataclass config.
             DEMO_MODE = True runs without a key.
REQUEST: The simplest complete SDK agent — give it a system prompt + a task, let query()
         own the loop, tool execution, and retries.
VALIDATION: No while-loop in my code; one query() call returns the final answer.
```
#### 💻 PRODUCES (essence)
```python
async for msg in query(prompt="Summarize RAG in 2 lines",
                       options=ClaudeAgentOptions(system_prompt=SYSTEM)):
    print(msg)        # SDK ran the whole loop for you
```
> Compare to Phase 4 #41: the entire `while True` block is gone. That's Tier 2.

---

## 48. `template_sdk_tools.py` — Ph5-L02 SDK Tools
**Level 3 (Contract) · Mode 2** — tool *descriptions* are the contract now.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: SDK tool registration. Pydantic for tool I/O. Descriptions must be precise
             enough that the model picks the right tool unaided.
REQUEST: An agent with 3 tools — calculator, text analyzer, knowledge search.
VALIDATION: Each tool's description states exactly WHEN to use it; model selects correctly.
```
#### 💻 PRODUCES (essence)
```python
@tool("calculator", "Do exact arithmetic. Use for any math, never guess numbers.")
async def calculator(args: dict) -> dict:
    return {"result": eval_expr(args["expression"])}
```

---

## 49. `template_streaming_agent.py` — Ph5-L03 Streaming
**Level 2 (Behavior) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: client.messages.stream(). DEMO_MODE fakes streaming with time.sleep per chunk.
REQUEST: An agent that prints its answer token-by-token as it generates (live typing).
VALIDATION: Output appears incrementally, not all-at-once; demo needs no API key.
```
#### 💻 PRODUCES (essence)
```python
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)   # live tokens
```

---

## 50. `template_session_memory.py` — Ph5-L04 Session Memory
**Level 2 (Behavior) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Read session_id from the ResultMessage of turn 1; pass it back as resume= on
             later turns. DEMO simulates session state in a dict.
REQUEST: Multi-turn memory where turn 2 remembers turn 1 — without me re-sending history.
VALIDATION: Asking "what did I just ask?" recalls the prior turn; no resume = clean slate.
```
#### 💻 PRODUCES (essence)
```python
async for m in query(prompt="My name is Niso"):          # turn 1: new session
    if isinstance(m, ResultMessage): sid = m.session_id
opts = ClaudeAgentOptions(resume=sid)                     # resume=, not session_id=
async for m in query(prompt="What's my name?", options=opts): ...   # → "Niso"
```
> Compare to Phase 1A #5: there you re-sent the whole list yourself. The SDK does it.

---

## 51. `template_subagent_pipeline.py` — Ph5-L05 Subagent Pipeline
**Mode 5 (Integration)**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Two SDK agents. Output of the researcher becomes input to the synthesizer.
             Pydantic for the hand-off payload.
REQUEST: An orchestrator that delegates research to a specialist subagent, then synthesizes
         its findings into a final answer.
VALIDATION: Researcher runs first; synthesizer only sees its structured output; one entry point.
```
#### 💻 PRODUCES (essence)
```python
findings = await researcher.run(topic)          # subagent 1
report   = await synthesizer.run(findings)      # subagent 2 (input = output of 1)
```

---

## 52. `template_managed_agent.py` — Ph5-L06 Managed Agents
**Level 1 (Features) · Mode 1 (Exploration)** — Tier 3, the highest abstraction.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: client.beta.agents / environments / sessions (public beta since April 2026,
             still beta on 2026-10-28). DEMO mocks the API objects.
             I define intent + tools only — Anthropic's servers run the agent.
REQUEST: The managed-agent pattern: create agent + environment, open a session, send the
         task, stream events until the session goes idle.
VALIDATION: No agent loop and no tool dispatch in my code — just create → send → read events.
```
#### 💻 PRODUCES (essence)
```python
agent = client.beta.agents.create(name="Researcher", model="claude-opus-5-5", system=GOAL,
                                  tools=[{"type": "agent_toolset_20260401"}])
env     = client.beta.environments.create(name="sandbox", config={"type": "cloud", ...})
session = client.beta.sessions.create(agent=agent.id, environment_id=env.id)
with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(session.id, events=[{"type": "user.message", ...}])
    # read "agent.message" events until "session.status_idle"
```
> The arc ends here: Phase 4 you built the car, Phase 5 L01–L05 you drove it,
> L06 you ordered a taxi. **The prompt got shorter as the abstraction got higher.**
