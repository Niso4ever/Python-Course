# Phase 4 — Agentic AI, Raw API (Ph4-L02–L08, 6 templates)

Tier 1 of the three-tier landscape: you hand-write the loop. These prompts are
heavier on **Mode 5 (Integration)** because an agent is components wired
together — and every template runs in `DEMO_MODE` with zero API calls.

---

## 41. `template_agent_loop.py` — Ph4-L02 The Agent Loop
**Level 4 (Test Cases) · Mode 2 (Specification)** — the engine everything else sits on.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Raw `import anthropic`. while-True loop driven by stop_reason. DEMO simulates
             tool calls locally. Accumulate messages across iterations.
REQUEST: The full agent loop — call model → dispatch tool_use → append result → repeat
         until end_turn.
VALIDATION:
  - stop_reason=="tool_use" runs the dispatcher; "end_turn" exits.
  - messages grow each turn (model sees prior steps).
  - a max-iterations cap prevents infinite loops.
```
#### 💻 PRODUCES (essence)
```python
while True:
    resp = client.messages.create(messages=messages, tools=tools)
    if resp.stop_reason != "tool_use": break
    messages.append({"role": "user", "content": dispatch(resp)})
```

---

## 42. `template_tool_caller.py` — Ph4-L03 Direct Tool Use
**Level 3 (Contract) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Define tool schemas, register them, parse tool_use blocks. DEMO runs tools locally.
REQUEST: Register 2–3 tools with the API and parse which one the model picked + its args.
VALIDATION: Each tool_use block maps to exactly one registered function; unknown name handled.
```
#### 💻 PRODUCES (essence)
```python
for block in resp.content:
    if block.type == "tool_use":
        result = REGISTRY[block.name](**block.input)
```

---

## 43. `template_structured_extractor.py` — Ph4-L04 Structured Output
**Level 3 (Contract) · Mode 2** — native structured outputs, not prompt-begging.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Define a Pydantic model and pass it to client.messages.parse(output_format=...).
             No forced tool_choice: it returns 400 on Opus 5.5 / Sonnet 5.5 / Fable 5.1
             (define-tools docs, retrieved 2026-10-28). DEMO returns a canned object.
REQUEST: Extract a typed Person{name, age, role} from free text, guaranteed-valid.
VALIDATION: response.parsed_output is a Person instance; no manual JSON parsing.
```
#### 💻 PRODUCES (essence)
```python
class Person(BaseModel):
    name: str = Field(description="Full name"); age: int; role: str
resp = client.messages.parse(model="claude-opus-5-5", max_tokens=1024,
                             messages=msgs, output_format=Person)
person = resp.parsed_output        # already a validated Person
```

---

## 44. `template_orchestrator.py` — Ph4-L05 Multi-Agent Orchestration
**Mode 5 (Integration)**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: 3 specialist agents (researcher, writer, analyst), already built. A router
             picks one via structured output. DEMO simulates all of them.
REQUEST: An orchestrator that routes a task to the right specialist, then runs a
         research → write sequential pipeline.
VALIDATION: Router's choice is a typed enum; pipeline passes researcher output into writer.
```
#### 💻 PRODUCES (essence)
```python
choice = router.route(task)               # structured → "researcher"
findings = researcher(task)
article = writer(task, context=findings)  # output of 1 = input of 2
```

---

## 45. `template_mcp_client.py` — Ph4-L06 MCP Tool Standard
**Level 2 (Behavior) · Mode 1 (Exploration)** — learning a new protocol.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Show MCP server SHAPE for recognition, then a client. DEMO simulates the
             server locally — no real server needed.
REQUEST: An MCP client that discovers a server's tools and calls one of them.
VALIDATION: discover() lists tool names + schemas; call(name, args) returns a result dict.
```
#### 💻 PRODUCES (essence)
```python
tools = await session.list_tools()             # discover
result = await session.call_tool("search", {"query": "..."})  # invoke
```

---

## 46. `template_openai_agent.py` — Ph4-L08 OpenAI Agents SDK
**Level 2 (Behavior) · Mode 5 (Integration)** — same patterns, different vendor.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: OpenAI Agents SDK. @function_tool decorators. asyncio for parallel runs.
             DEMO simulates agent + tool calls.
REQUEST: A single agent with tools, a multi-agent handoff (orchestrator → specialist),
         and parallel agent runs with asyncio.gather.
VALIDATION: Handoff transfers control cleanly; parallel runs return in any order, all complete.
```
#### 💻 PRODUCES (essence)
```python
@function_tool
def search(query: str) -> str: ...
agent = Agent(name="Assistant", tools=[search], handoffs=[specialist])
results = await asyncio.gather(*(Runner.run(agent, q) for q in queries))
```
