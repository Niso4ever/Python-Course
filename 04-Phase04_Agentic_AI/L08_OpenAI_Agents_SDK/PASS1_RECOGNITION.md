# Lesson 24 — Pass 1: RECOGNITION
## Learn to READ OpenAI Agents SDK Code

**Goal:** When you see OpenAI Agents SDK code, instantly recognize its structure and map it back to the patterns you already know from L02–L07.

> **Key insight:** The OpenAI Agents SDK is the lightest agentic framework available. It wraps the same THINK → ACT → OBSERVE loop you already know — but expresses it in 5–10 lines instead of 30. After this lesson, you'll read both.

---

## The Same Loop, Different Syntax

Before reading examples, map the SDK to what you already know:

```
ANTHROPIC (L02–L06)                    OPENAI AGENTS SDK (L08)
══════════════════════════════════════════════════════════════
import anthropic                   →   from agents import Agent, Runner
client.messages.create(tools=...)  →   Runner.run_sync(agent, message)
stop_reason == "end_turn"          →   handled inside Runner automatically
messages.append(...)               →   handled inside Runner automatically
def my_tool(...) + schema dict     →   @function_tool def my_tool(...)
run_specialist(task)               →   agent.handoffs = [other_agent]
```

**The loop still exists — Runner runs it for you.**

---

## Example 1: The Simplest Agent (Hello World)

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
)

result = Runner.run_sync(agent, "What is RAG in AI?")
print(result.final_output)
```

**READ:**
- `Agent(name, instructions)` — the agent definition (replaces system prompt + model config)
- `Runner.run_sync(agent, message)` — runs the full loop synchronously
- `result.final_output` — the agent's final text answer
- No `while True:`, no `messages.append()`, no `stop_reason` — Runner handles all of it

---

## Example 2: Agent with a Tool

```python
from agents import Agent, Runner, function_tool

@function_tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for a given topic."""
    knowledge = {
        "rag": "RAG combines retrieval with LLMs to ground responses in documents.",
        "mcp": "MCP is the 2024 standard for connecting AI models to tools.",
    }
    return knowledge.get(query.lower(), f"No result for: {query}")

agent = Agent(
    name="Researcher",
    instructions="You are a research assistant. Use the knowledge base tool to answer questions.",
    tools=[search_knowledge_base],
)

result = Runner.run_sync(agent, "Explain RAG")
print(result.final_output)
```

**READ:**
- `@function_tool` decorator — converts a Python function into an agent tool (replaces the JSON schema dict)
- The docstring becomes the tool description (what the LLM sees)
- Type hints (`query: str`) define the schema automatically
- `tools=[search_knowledge_base]` — list of decorated functions (same as `tools=[schema_dict]` in Anthropic)

---

## Example 3: Recognizing @function_tool vs. Anthropic Schema

```python
# ANTHROPIC (L03 style) — manual schema dict:
TOOLS = [{
    "name": "search_knowledge_base",
    "description": "Search a knowledge base for information on a topic.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The topic to look up."}
        },
        "required": ["query"]
    }
}]

# OPENAI AGENTS SDK — same thing, 4 lines:
@function_tool
def search_knowledge_base(query: str) -> str:
    """Search a knowledge base for information on a topic."""
    ...
```

**READ:** Both express exactly the same information. The SDK generates the schema from the decorator + type hints + docstring. Less code, same semantics.

---

## Example 4: Agent Handoffs (Multi-Agent)

```python
from agents import Agent, Runner

# Specialist agents
researcher = Agent(
    name="Researcher",
    instructions="You research topics thoroughly using available tools.",
    tools=[search_web],
)

writer = Agent(
    name="Writer",
    instructions="You write clear, engaging content from research provided to you.",
)

# Orchestrator with handoffs
orchestrator = Agent(
    name="Orchestrator",
    instructions="""You manage a content pipeline.
    First hand off to Researcher to gather information.
    Then hand off to Writer to produce the final content.""",
    handoffs=[researcher, writer],
)

result = Runner.run_sync(orchestrator, "Write an article about agentic AI in 2026")
print(result.final_output)
```

**READ:**
- `handoffs=[researcher, writer]` — replaces the `run_specialist()` calls in L05
- The orchestrator decides WHEN to hand off and TO WHOM — same orchestrator logic, SDK handles the routing
- Each agent has its own `instructions` (system prompt) and optional `tools`

---

## Example 5: Guardrails (Input Validation)

```python
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def check_topic(ctx, agent, input) -> GuardrailFunctionOutput:
    """Block off-topic questions."""
    blocked_keywords = ["competitor", "lawsuit", "salary"]
    if any(word in input.lower() for word in blocked_keywords):
        return GuardrailFunctionOutput(
            output_info="Blocked sensitive topic",
            tripwire_triggered=True,
        )
    return GuardrailFunctionOutput(tripwire_triggered=False)

agent = Agent(
    name="Safe Assistant",
    instructions="You are a product assistant.",
    input_guardrails=[check_topic],
)
```

**READ:**
- `@input_guardrail` — decorator for input validation (replaces `if not validate_query(input): return error` from L07)
- `tripwire_triggered=True` — stops the agent from running if guardrail fires
- This maps directly to GUARDRAIL 1 (input validation) from the L07 design framework

---

## Example 6: Async Agent (Parallel Runs)

```python
import asyncio
from agents import Agent, Runner

agent = Agent(
    name="Analyst",
    instructions="You analyze business topics concisely.",
)

async def run_parallel_analyses():
    tasks = [
        Runner.run(agent, "Analyze the energy sector outlook"),
        Runner.run(agent, "Analyze the healthcare sector outlook"),
        Runner.run(agent, "Analyze the fintech sector outlook"),
    ]
    results = await asyncio.gather(*tasks)
    for i, result in enumerate(results):
        print(f"Analysis {i+1}: {result.final_output}\n")

asyncio.run(run_parallel_analyses())
```

**READ:**
- `Runner.run(agent, message)` — async version (no `_sync` suffix)
- `asyncio.gather(*tasks)` — runs all three agents in parallel (same as L05 parallel pattern)
- `Runner.run_sync(...)` = synchronous (blocks until done)
- `Runner.run(...)` = async (use with `await`)

---

## Example 7: Reading the Result Object

```python
result = Runner.run_sync(agent, "What is MCP?")

# What's inside result:
print(result.final_output)          # The agent's text answer (string)
print(result.messages)              # Full message history (list of dicts)
print(result.last_agent)            # Which agent produced the final answer
print(result.new_messages)          # Only messages added in this run
```

**READ — result fields:**

| Field | What it contains |
|:------|:----------------|
| `result.final_output` | The agent's final text response |
| `result.messages` | Complete conversation (all turns) |
| `result.last_agent` | The agent that produced the final answer |
| `result.new_messages` | Only messages from this run (for session memory) |

---

## Example 8: SDK vs. Raw Anthropic — Side by Side

```python
# ══════════════════════════════════════════════════════════
# RAW ANTHROPIC (L02-L06 style) — you write the loop
# ══════════════════════════════════════════════════════════
import anthropic

client = anthropic.Anthropic()
messages = [{"role": "user", "content": "Research agentic AI trends"}]

while True:
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=4096,
        tools=TOOLS,
        messages=messages
    )
    if response.stop_reason == "end_turn":
        print(response.content[0].text)
        break
    messages.append({"role": "assistant", "content": response.content})
    tool_results = execute_tools(response.content)
    messages.append({"role": "user", "content": tool_results})


# ══════════════════════════════════════════════════════════
# OPENAI AGENTS SDK — SDK runs the loop for you
# ══════════════════════════════════════════════════════════
from agents import Agent, Runner

agent = Agent(
    name="Researcher",
    instructions="Research agentic AI trends thoroughly.",
    tools=[search_tool],
)

result = Runner.run_sync(agent, "Research agentic AI trends")
print(result.final_output)
```

**READ:** Same outcome. The SDK collapses the 20-line loop into 6 lines. What it HIDES:
- The `while True` / stop_reason logic
- The `messages.append()` accumulation
- The tool dispatcher

**What it EXPOSES:** Agent config, tools, handoffs. That's it.

---

## Recognition Reference

| What you see | What it means |
|:-------------|:-------------|
| `Agent(name, instructions)` | Agent definition + system prompt |
| `Agent(tools=[...])` | Agent with tool access |
| `Agent(handoffs=[...])` | Orchestrator with specialist routing |
| `@function_tool` | Python function auto-converted to tool schema |
| `Runner.run_sync(agent, msg)` | Run the agent loop synchronously |
| `Runner.run(agent, msg)` | Run the agent loop asynchronously |
| `result.final_output` | The agent's final answer |
| `@input_guardrail` | Input validation before agent runs |
| `@output_guardrail` | Output validation after agent runs |
| `agent.model = "gpt-4o"` | Override default model |

---

## You've Completed Pass 1!

You can now:
✓ **Recognize** an OpenAI Agents SDK agent at a glance
✓ **Map** `@function_tool` to the Anthropic schema dict
✓ **See** that `Runner.run_sync()` is the while loop you wrote in L02
✓ **Read** handoffs as the multi-agent orchestration pattern from L05
✓ **Spot** guardrail decorators vs. inline validation

**Next:** Pass C — visual maps of the SDK's structure
