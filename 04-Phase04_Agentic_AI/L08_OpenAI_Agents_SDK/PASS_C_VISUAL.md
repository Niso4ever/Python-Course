# Lesson 24 — Pass C: VISUAL PATTERNS
## OpenAI Agents SDK — Architecture Diagrams

---

## Visual 1: The SDK Object Map

```
OPENAI AGENTS SDK — what you build with

┌──────────────────────────────────────────────────────────┐
│                        AGENT                             │
│                                                          │
│   name          = "Researcher"                           │
│   instructions  = "You are..."  ← system prompt         │
│   model         = "gpt-4o"      ← which LLM             │
│   tools         = [fn1, fn2]    ← @function_tool list   │
│   handoffs      = [agent2]      ← other agents to route │
│   input_guardrails  = [guard1]  ← validation before     │
│   output_guardrails = [guard2]  ← validation after      │
└──────────────────────────────────────────────────────────┘
              │
              │  passed to
              ▼
┌──────────────────────────────────────────────────────────┐
│                       RUNNER                             │
│                                                          │
│   Runner.run_sync(agent, message)  ← synchronous        │
│   await Runner.run(agent, message) ← async              │
│                                                          │
│   Internally runs:                                       │
│     while stop_reason != "end_turn":                     │
│         response = llm.call(...)                         │
│         execute_tools(response)                          │
│         messages.append(...)                             │
└──────────────────────────────────────────────────────────┘
              │
              │  returns
              ▼
┌──────────────────────────────────────────────────────────┐
│                     RunResult                            │
│                                                          │
│   result.final_output   ← the answer (string)           │
│   result.messages       ← full conversation history     │
│   result.last_agent     ← which agent finished          │
│   result.new_messages   ← messages from this run only   │
└──────────────────────────────────────────────────────────┘
```

---

## Visual 2: @function_tool — How It Works

```
WHAT YOU WRITE:                        WHAT THE SDK GENERATES:

@function_tool                    →    {
def get_weather(city: str,             "name": "get_weather",
                unit: str = "C"        "description": "Get current weather...",
               ) -> str:               "parameters": {
    """Get current weather               "type": "object",
       for a given city."""              "properties": {
    ...                                    "city": {"type": "string"},
                                           "unit": {"type": "string",
                                                    "default": "C"}
                                         },
                                         "required": ["city"]
                                       }
                                     }

Python type hint  → JSON schema type
Docstring         → tool description
Default value     → optional parameter
```

**The decorator reads your code and builds the JSON schema for you.**

---

## Visual 3: Runner Flow — Inside the Black Box

```
Runner.run_sync(agent, "What are AI trends?")
           │
           ▼
    Build initial messages:
    [{"role": "user", "content": "What are AI trends?"}]
           │
           ▼
    ┌─────────────────────────────────────┐
    │           AGENT LOOP                │
    │                                     │
    │  Call LLM with:                     │
    │    model = agent.model              │
    │    system = agent.instructions      │
    │    tools = agent.tools (schemas)    │
    │    messages = current history       │
    │                 │                   │
    │         ┌───────┴────────┐          │
    │         │                │          │
    │    tool_use           end_turn      │
    │         │                │          │
    │    execute tool      EXIT LOOP      │
    │    append result          │          │
    │    loop again        return result  │
    │                                     │
    └─────────────────────────────────────┘
           │
           ▼
    RunResult(final_output=..., messages=..., last_agent=...)
```

---

## Visual 4: Single Agent vs. Multi-Agent Handoff

```
SINGLE AGENT:

User → Runner → Agent(tools=[search]) → result


MULTI-AGENT WITH HANDOFFS:

User → Runner → Orchestrator
                     │
              ┌──────┴──────┐
              │             │
         Researcher      Writer
         (search tools)  (format tools)
              │             │
              └──────┬──────┘
                     │
                   result


CODE:
orchestrator = Agent(
    handoffs=[researcher, writer]  ← defines who can receive work
)
# Orchestrator decides WHEN and to WHOM to hand off
# Runner manages the routing automatically
```

---

## Visual 5: Guardrail Placement in the SDK

```
USER INPUT
    │
    ▼
@input_guardrail ← GUARDRAIL 1: check before agent runs
    │
  PASS  │  FAIL
    │         └──→ InputGuardrailTripwireTriggered exception
    ▼
AGENT LOOP (Runner manages loop cap internally)
    │
    ▼
@output_guardrail ← GUARDRAIL 3: check before returning to user
    │
  PASS  │  FAIL
    │         └──→ OutputGuardrailTripwireTriggered exception
    ▼
result.final_output → returned to user


COMPARISON WITH L07 MANUAL GUARDRAILS:

L07 (manual):                   L08 SDK:
─────────────────────────────────────────────────────
if not validate(input):    →    @input_guardrail
    return error
run_agent(max_iter=15)     →    Runner (handles internally)
if not quality_gate(out):  →    @output_guardrail
    return escalate
```

---

## Visual 6: Sync vs. Async — When to Use Each

```
SYNCHRONOUS (Runner.run_sync):
  ┌─────────────────────────────────┐
  │  result = Runner.run_sync(      │
  │      agent, message)            │
  │                                 │
  │  ← blocks until done            │
  │  ← simple to write              │
  │  ← good for scripts, demos      │
  └─────────────────────────────────┘

ASYNCHRONOUS (await Runner.run):
  ┌─────────────────────────────────┐
  │  result = await Runner.run(     │
  │      agent, message)            │
  │                                 │
  │  ← non-blocking                 │
  │  ← required for parallel runs   │
  │  ← good for production, APIs    │
  └─────────────────────────────────┘

PARALLEL (asyncio.gather):
  ┌─────────────────────────────────┐
  │  results = await asyncio.gather(│
  │      Runner.run(agent, task1),  │
  │      Runner.run(agent, task2),  │
  │      Runner.run(agent, task3),  │
  │  )                              │
  │  ← all three run at same time   │
  └─────────────────────────────────┘
```

---

## Visual 7: SDK vs. Anthropic Raw API — Translation Map

```
PURPOSE            ANTHROPIC (L02–L06)                  OPENAI AGENTS SDK (L08)
═══════════════════════════════════════════════════════════════════════════════
Define agent       system="You are..."                  Agent(instructions="...")
                   + model="claude-opus-5-5"            + model="gpt-4o"  (optional)

Define tool        {"name": ..., "description": ...,    @function_tool
                    "input_schema": {...}}               def tool_name(...): ...

Run loop           while True: + stop_reason check      Runner.run_sync(agent, msg)

Add tools          tools=[schema_dict]                  Agent(tools=[decorated_fn])

Multi-agent        run_specialist(task)                 Agent(handoffs=[other_agent])

Input guard        if not validate(input): return err   @input_guardrail

Output guard       if not quality_gate(out): retry      @output_guardrail

Async              asyncio.gather(+ AsyncAnthropic)     asyncio.gather(+ Runner.run)

Get answer         response.content[0].text             result.final_output

Get history        messages (you maintain it)           result.messages (SDK maintains)
```

---

## Visual 8: The Complexity Scale — SDK Position

```
COMPLEXITY ↑

Single LLM call                         [simplest]
    ↓
Single LLM call + structured output
    ↓
One agent + one tool
    ↓
One agent + multiple tools              ← SDK covers all of this easily
    ↓                                      with Agent + @function_tool
Sequential pipeline (2-3 agents)        ← SDK handoffs handle this
    ↓
Router + specialists                    ← SDK handoffs handle this too
    ↓
Parallel agents                         ← asyncio.gather + Runner.run
    ↓
Swarm (dynamic spawning)               ← still doable with SDK
    ↓
Agent-as-tool (nested agents)          [most complex — raw API better here]

RULE: Start with the SDK for simple to medium complexity.
      Switch to raw Anthropic/OpenAI API when you need full control.
```

---

## You've Completed Pass C!

You can now:
✓ **Map** the SDK objects (Agent, Runner, RunResult) at a glance
✓ **See** that `@function_tool` is the schema dict you wrote in L03
✓ **Trace** the Runner's internal loop without seeing the code
✓ **Compare** SDK guardrails to the three-guardrail pattern from L07
✓ **Choose** sync vs. async vs. parallel based on your use case
✓ **Position** the SDK on the complexity scale — where to use it vs. raw API

**Next:** Pass 3 — Templates you can copy and modify for real projects
