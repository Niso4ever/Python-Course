# Lesson 24 — Pass 3: TEMPLATES
## OpenAI Agents SDK — Copy-Paste Patterns

> These are thinking + code templates. Copy the one that fits your task, fill in the blanks, and run it.

---

## Template 1: Minimal Agent (No Tools)
**Use when:** You want a focused LLM with a specific persona and no tool access.

```python
from agents import Agent, Runner

agent = Agent(
    name="[AgentName]",
    instructions="You are a [role]. Your job is to [task]. Always [constraint].",
    model="gpt-4o",   # optional — default is no longer gpt-4o (SDK docs, 2026-10-28: gpt-5.6-luna)
)

result = Runner.run_sync(agent, "[user question or task]")
print(result.final_output)
```

**Example call:**
```python
agent = Agent(
    name="Summarizer",
    instructions="You are a document summarizer. Condense text to 3 bullet points.",
)
result = Runner.run_sync(agent, "The history of AI spans from 1950...")
print(result.final_output)
# • Alan Turing proposed the Turing Test in 1950.
# • Deep learning emerged in the 2010s with neural networks.
# • Agentic AI systems arrived in 2024–2026.
```

---

## Template 2: Agent with One Tool
**Use when:** Agent needs to call one external function to answer questions.

```python
from agents import Agent, Runner, function_tool

@function_tool
def [tool_name]([param]: [type]) -> str:
    """[What this tool does. When to use it. What it returns.]"""
    # ... your logic here ...
    return str(result)

agent = Agent(
    name="[AgentName]",
    instructions="Use [tool_name] when you need [specific situation].",
    tools=[[tool_name]],
)

result = Runner.run_sync(agent, "[user question]")
print(result.final_output)
```

**Example call:**
```python
@function_tool
def get_price(ticker: str) -> str:
    """Get the current stock price for a ticker symbol like AAPL or MSFT."""
    prices = {"AAPL": "$189.42", "MSFT": "$415.30", "NVDA": "$875.60"}
    return prices.get(ticker.upper(), f"Unknown ticker: {ticker}")

agent = Agent(
    name="StockBot",
    instructions="Answer stock price questions using the get_price tool.",
    tools=[get_price],
)
result = Runner.run_sync(agent, "What is Apple's stock price?")
print(result.final_output)   # "Apple's current stock price is $189.42."
```

---

## Template 3: Agent with Multiple Tools
**Use when:** Agent needs 2–5 tools covering different capabilities.

```python
from agents import Agent, Runner, function_tool

@function_tool
def [tool_1]([params]) -> str:
    """[When to use tool 1. What it does.]"""
    ...

@function_tool
def [tool_2]([params]) -> str:
    """[When to use tool 2. What it does.]"""
    ...

@function_tool
def [tool_3]([params]) -> str:
    """[When to use tool 3. What it does.]"""
    ...

agent = Agent(
    name="[AgentName]",
    instructions="""You are a [role].
    Use [tool_1] when [condition 1].
    Use [tool_2] when [condition 2].
    Use [tool_3] when [condition 3].
    Never fabricate data — always use tools.""",
    tools=[[tool_1], [tool_2], [tool_3]],
)

result = Runner.run_sync(agent, "[task]")
print(result.final_output)
```

**Example call:**
```python
@function_tool
def search_news(topic: str) -> str:
    """Search recent news. Use for current events from the last 30 days."""
    return f"[News about {topic}]: AI investments hit $500B in Q1 2026."

@function_tool
def calculate(expression: str) -> str:
    """Evaluate a math expression. Use when the user needs a calculation."""
    return str(eval(expression))

@function_tool
def format_report(title: str, content: str) -> str:
    """Format a final report. Use LAST, after gathering all information."""
    return f"# {title}\n\n{content}"

agent = Agent(
    name="AnalystBot",
    instructions="You are a business analyst. Research → Calculate → Format.",
    tools=[search_news, calculate, format_report],
)
result = Runner.run_sync(agent, "Summarize AI investment trends this quarter")
print(result.final_output)
```

---

## Template 4: Multi-Agent with Handoffs
**Use when:** Different parts of the task need different expertise or tool sets.

```python
from agents import Agent, Runner, function_tool

# --- SPECIALIST AGENTS ---
[specialist_1] = Agent(
    name="[SpecialistName1]",
    instructions="You are a [role 1]. Focus on [task 1].",
    tools=[[tool_for_specialist_1]],
)

[specialist_2] = Agent(
    name="[SpecialistName2]",
    instructions="You are a [role 2]. Focus on [task 2].",
    tools=[[tool_for_specialist_2]],
)

# --- ORCHESTRATOR ---
orchestrator = Agent(
    name="[OrchestratorName]",
    instructions="""You manage a [pipeline name].
    Step 1: Hand off to [specialist_1] to [task 1].
    Step 2: Hand off to [specialist_2] to [task 2].
    Return the final result.""",
    handoffs=[[specialist_1], [specialist_2]],
)

result = Runner.run_sync(orchestrator, "[user goal]")
print(result.final_output)
print(f"Completed by: {result.last_agent.name}")
```

**Example call:**
```python
researcher = Agent(
    name="Researcher",
    instructions="Research the topic thoroughly using search tools.",
    tools=[search_web],
)

writer = Agent(
    name="Writer",
    instructions="Write a clear, engaging article from the research provided.",
)

orchestrator = Agent(
    name="ContentPipeline",
    instructions="First hand off to Researcher, then to Writer. Return final article.",
    handoffs=[researcher, writer],
)

result = Runner.run_sync(orchestrator, "Write an article about agentic AI in 2026")
print(result.final_output)
print(f"Last agent: {result.last_agent.name}")   # "Writer"
```

---

## Template 5: Agent with Input Guardrail
**Use when:** You need to validate or filter user input before the agent runs.

```python
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput
import asyncio

@input_guardrail
async def [guardrail_name](ctx, agent, input) -> GuardrailFunctionOutput:
    """[What this guardrail checks for.]"""
    # Check condition
    if [condition_that_should_block]:
        return GuardrailFunctionOutput(
            output_info="[Reason for blocking]",
            tripwire_triggered=True,
        )
    return GuardrailFunctionOutput(tripwire_triggered=False)

agent = Agent(
    name="[AgentName]",
    instructions="[System prompt]",
    input_guardrails=[[guardrail_name]],
)

async def safe_run(user_input: str):
    try:
        result = await Runner.run(agent, user_input)
        return result.final_output
    except Exception as e:
        return f"Input blocked: {e}"

print(asyncio.run(safe_run("[user message]")))
```

**Example call:**
```python
@input_guardrail
async def block_sensitive_topics(ctx, agent, input) -> GuardrailFunctionOutput:
    """Block questions about internal salary data or legal disputes."""
    blocked = ["salary", "lawsuit", "confidential", "internal"]
    if any(word in input.lower() for word in blocked):
        return GuardrailFunctionOutput(
            output_info="Sensitive topic blocked",
            tripwire_triggered=True,
        )
    return GuardrailFunctionOutput(tripwire_triggered=False)

agent = Agent(
    name="ProductBot",
    instructions="You answer product questions for customers.",
    input_guardrails=[block_sensitive_topics],
)

async def safe_run(q):
    try:
        result = await Runner.run(agent, q)
        return result.final_output
    except Exception as e:
        return "I can't help with that topic."

print(asyncio.run(safe_run("What's your CEO salary?")))   # "I can't help with that topic."
print(asyncio.run(safe_run("How do I reset my password?")))  # normal answer
```

---

## Template 6: Parallel Agent Runs
**Use when:** You need the same (or different) agents to run multiple tasks simultaneously.

```python
import asyncio
from agents import Agent, Runner, function_tool

agent = Agent(
    name="[AgentName]",
    instructions="[System prompt]",
    tools=[[tool]],
)

async def run_parallel(tasks: list[str]) -> list[str]:
    """Run multiple agent calls in parallel."""
    runs = [Runner.run(agent, task) for task in tasks]
    results = await asyncio.gather(*runs)
    return [r.final_output for r in results]

tasks = [
    "[task 1]",
    "[task 2]",
    "[task 3]",
]

outputs = asyncio.run(run_parallel(tasks))
for i, output in enumerate(outputs, 1):
    print(f"Task {i}: {output}\n")
```

**Example call:**
```python
analyst = Agent(
    name="SectorAnalyst",
    instructions="You give concise 2-sentence sector outlooks based on current trends.",
)

async def analyze_sectors(sectors: list[str]) -> list[str]:
    runs = [Runner.run(analyst, f"Give a 2026 outlook for the {s} sector") for s in sectors]
    results = await asyncio.gather(*runs)
    return [r.final_output for r in results]

sectors = ["energy", "healthcare", "fintech"]
outputs = asyncio.run(analyze_sectors(sectors))

for sector, outlook in zip(sectors, outputs):
    print(f"{sector.upper()}: {outlook}\n")
# ENERGY: The energy sector is transitioning rapidly...
# HEALTHCARE: AI-driven diagnostics are reshaping...
# FINTECH: Embedded finance and agentic payments...
```

---

## Quick Reference: SDK Parameter Cheatsheet

```python
Agent(
    name        = "string",           # required — agent's name
    instructions= "string",           # required — system prompt
    model       = "gpt-4o",           # optional — default (2026-10-28): gpt-5.6-luna
    tools       = [fn1, fn2],         # optional — @function_tool list
    handoffs    = [agent2, agent3],   # optional — agents for routing
    input_guardrails  = [guard1],     # optional — validate input
    output_guardrails = [guard2],     # optional — validate output
)

Runner.run_sync(agent, "message")     # synchronous, returns RunResult
await Runner.run(agent, "message")    # async, returns RunResult

result.final_output    # str — the agent's answer
result.messages        # list — full conversation
result.last_agent      # Agent — who answered
result.new_messages    # list — messages from this run only
```
