# Lesson 18 — Pass 1: RECOGNITION
## Learn to SEE the Agent Loop

**Goal:** By the end of this pass, you'll spot the agent loop in any codebase — raw API, framework wrapper, or production system — without writing a single line.

> **2026 Note:** This loop runs inside CrewAI, LangGraph, AutoGen, and OpenAI Agents SDK. Those frameworks hide it with decorators and class magic. Here you see it naked. Once you recognize it here, you can read any of them.

---

## The Three Shapes of the Agent Loop

### Shape 1: The Loop Itself
```python
while True:
    ...
```
or
```python
while not done:
    ...
```
**Recognize:** Unconditional or flag-controlled loop. The agent keeps going until something tells it to stop.

---

### Shape 2: The Decision Point
```python
if response.stop_reason == "end_turn":
    return response.content[0].text   # ← AGENT IS DONE

if response.stop_reason == "tool_use":
    ...                                # ← AGENT WANTS A TOOL
```
**Recognize:** Two exit paths. `"end_turn"` = agent has an answer. `"tool_use"` = agent needs to act first.

---

### Shape 3: The Message Accumulation
```python
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user",      "content": tool_results})
```
**Recognize:** The conversation list grows every iteration. Agent sees its own history.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: The Minimal Agent Loop

```python
import anthropic

client = anthropic.Anthropic()

def run_agent(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    while True:
        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

        # Tool use: add response + results, loop again
        messages.append({"role": "assistant", "content": response.content})
        tool_results = execute_tools(response.content)
        messages.append({"role": "user", "content": tool_results})

# Example call:
answer = run_agent("What is the population of Tokyo?")
print(answer)
# → Agent called search_web("Tokyo population") → got result → composed answer
```

**RECOGNIZE THIS:**
- `while True:` ← the loop
- `stop_reason == "end_turn"` ← the exit
- Two `messages.append(...)` ← conversation grows
- Loop restarts after tool results are added

**What it does:** "Ask LLM → if it needs tools, execute them and loop. If done, return the answer."

---

### Example 2: The Decision Inside the Loop

```python
def run_agent(messages: list) -> str:
    done = False

    while not done:
        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            done = True                          # ← sets the flag, exits next check
        elif response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            results = handle_tool_calls(response.content)
            messages.append({"role": "user", "content": results})

    return response.content[0].text

# Example call:
messages = [{"role": "user", "content": "Summarize today's AI news."}]
answer = run_agent(messages)
print(answer)
# → Agent searched → read articles → synthesized summary → returned
```

**RECOGNIZE THIS:**
- `done = False` + `while not done:` ← flag-controlled loop (same pattern as `while True`)
- `done = True` inside the `if` ← clean exit
- `elif stop_reason == "tool_use"` ← accumulate and continue

**What it does:** "Same loop — uses a flag instead of `return` inside the loop body."

---

### Example 3: The Tool Dispatcher

```python
def execute_tools(content_blocks: list) -> list:
    tool_results = []

    for block in content_blocks:
        if block.type == "tool_use":                # ← only process tool requests
            result = dispatch(block.name, block.input)  # ← call the right function
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,            # ← must match the tool_use id
                "content": str(result)
            })

    return tool_results

# Dispatcher: maps tool names to Python functions
def dispatch(tool_name: str, tool_input: dict) -> str:
    tool_map = {
        "search_web":    search_web,
        "read_file":     read_file,
        "run_python":    run_python,
    }
    fn = tool_map.get(tool_name)
    return fn(**tool_input) if fn else f"Unknown tool: {tool_name}"

# Example call:
results = execute_tools(response.content)
# → finds all tool_use blocks → dispatches each → returns list of tool_results
```

**RECOGNIZE THIS:**
- `for block in content_blocks:` ← loop through response
- `block.type == "tool_use"` ← filter to tool requests only
- `block.id` ← the id that must be echoed back in the result
- `tool_map = {...}` ← name → function lookup dictionary

**What it does:** "Receive agent's tool requests. Find the right function. Execute. Return results."

---

### Example 4: Max Iterations Safety Guard

```python
def run_agent_safe(question: str, max_iterations: int = 10) -> str:
    messages = [{"role": "user", "content": question}]
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        print(f"Iteration {iteration}/{max_iterations}")

        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

        messages.append({"role": "assistant", "content": response.content})
        results = execute_tools(response.content)
        messages.append({"role": "user", "content": results})

    return "Max iterations reached. Partial answer: " + response.content[0].text

# Example call:
answer = run_agent_safe("Plan a 5-step research report on RAG.", max_iterations=8)
print(answer)
# → 5 tool calls max → guaranteed to stop
```

**RECOGNIZE THIS:**
- `iteration < max_iterations` ← the safety cap
- `iteration += 1` ← counter increments every loop
- Fallback return at the end ← never crashes if agent loops forever

**What it does:** "Same loop — but capped. Agents can get stuck. This prevents infinite loops."

---

### Example 5: The OpenAI Equivalent (for Recognition)

```python
# OpenAI uses different field names — same pattern
from openai import OpenAI
openai = OpenAI()

def run_openai_agent(messages: list) -> str:
    while True:
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            tools=tools                              # ← same concept
        )

        finish_reason = response.choices[0].finish_reason  # ← "stop" or "tool_calls"

        if finish_reason == "stop":                  # ← Anthropic calls this "end_turn"
            return response.choices[0].message.content

        if finish_reason == "tool_calls":            # ← Anthropic calls this "tool_use"
            message = response.choices[0].message
            messages.append(message)
            results = handle_tool_calls(message.tool_calls)
            messages.extend(results)

# Example call:
messages = [{"role": "user", "content": "What is 2 + 2?"}]
answer = run_openai_agent(messages)
print(answer)  # "4"
```

**RECOGNIZE THIS:**
- `finish_reason` ← OpenAI's name for `stop_reason`
- `"stop"` ← OpenAI's name for `"end_turn"`
- `"tool_calls"` ← OpenAI's name for `"tool_use"`
- Loop shape is **identical** — only field names differ

**What it does:** "Same loop. Different provider. Different names. Same logic."

---

### Example 6: The Loop with Logging

```python
def run_agent_verbose(question: str) -> str:
    messages = [{"role": "user", "content": question}]
    step = 0

    while True:
        step += 1
        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        print(f"\n--- Step {step} | stop_reason: {response.stop_reason} ---")

        if response.stop_reason == "end_turn":
            print(f"Agent finished in {step} steps.")
            return response.content[0].text

        # Log which tools were called
        for block in response.content:
            if block.type == "tool_use":
                print(f"  Tool called: {block.name}({block.input})")

        messages.append({"role": "assistant", "content": response.content})
        results = execute_tools(response.content)
        messages.append({"role": "user", "content": results})

# Example call:
answer = run_agent_verbose("Research the top 3 AI models released in 2026.")
# Output:
# --- Step 1 | stop_reason: tool_use ---
#   Tool called: search_web({"query": "top AI models 2026"})
# --- Step 2 | stop_reason: tool_use ---
#   Tool called: search_web({"query": "Claude 4 vs GPT-5 comparison 2026"})
# --- Step 3 | stop_reason: end_turn ---
# Agent finished in 3 steps.
```

**RECOGNIZE THIS:**
- `step += 1` ← counts iterations for debugging
- `print(f"  Tool called: {block.name}({block.input})")` ← tracing tool calls
- Same loop — logging is purely additive, doesn't change behavior

**What it does:** "Same loop with observability. Shows you what the agent is doing step by step."

---

### Example 7: The Loop as a Class Method

```python
class ResearchAgent:
    def __init__(self, model: str = "claude-opus-5-5"):
        self.client = anthropic.Anthropic()
        self.model = model
        self.tools = [search_tool, summarize_tool]

    def run(self, question: str, max_steps: int = 15) -> str:
        messages = [{"role": "user", "content": question}]

        for _ in range(max_steps):                  # ← for loop = same as while + counter
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                tools=self.tools,
                messages=messages
            )

            if response.stop_reason == "end_turn":
                return response.content[0].text

            messages.append({"role": "assistant", "content": response.content})
            results = self.execute_tools(response.content)
            messages.append({"role": "user", "content": results})

        return "Max steps reached."

    def execute_tools(self, blocks):
        ...  # dispatcher

# Example call:
agent = ResearchAgent()
report = agent.run("Summarize recent breakthroughs in quantum computing.")
print(report)
# → 4-step tool loop → returns summary
```

**RECOGNIZE THIS:**
- `for _ in range(max_steps):` ← `for` loop doing same job as `while + counter`
- `self.client`, `self.model`, `self.tools` ← config stored in the object
- `self.execute_tools(...)` ← dispatcher is a method, not a standalone function

**What it does:** "Same loop — wrapped in a class. Every agent framework does this (hides the loop in a class)."

---

### Example 8: The Async Loop (2026 Production Style)

```python
import anthropic
import asyncio

client = anthropic.AsyncAnthropic()          # ← async client

async def run_agent_async(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    while True:
        response = await client.messages.create(  # ← await keyword
            model="claude-opus-5-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

        messages.append({"role": "assistant", "content": response.content})
        results = await execute_tools_async(response.content)  # ← tools also async
        messages.append({"role": "user", "content": results})

# Example call:
async def main():
    answer = await run_agent_async("What time is it in Tokyo right now?")
    print(answer)

asyncio.run(main())
# → Agent called get_time(timezone="Asia/Tokyo") → returned formatted time
```

**RECOGNIZE THIS:**
- `AsyncAnthropic()` ← async version of the client
- `await client.messages.create(...)` ← same call, just awaited
- Everything else is **identical** to the sync version
- `asyncio.run(main())` ← how you start an async program

**What it does:** "Same loop — async version for production systems handling many requests at once."

---

## Agent Loop Anatomy Reference

| Part | What it looks like | Role |
|:-----|:------------------|:-----|
| Loop start | `while True:` or `while not done:` | Keeps agent running |
| LLM call | `client.messages.create(...)` | Agent thinks |
| Exit check | `if stop_reason == "end_turn":` | Agent is done |
| Tool check | `if stop_reason == "tool_use":` | Agent needs to act |
| Accumulate | `messages.append(...)` | Agent remembers |
| Dispatch | `tool_map[name](**input)` | Execute the tool |
| Safety | `iteration < max_iterations` | Prevent infinite loop |

---

## Framework Translation Table

When you read framework code, map it back to this:

| Framework | Their name | Raw API equivalent |
|:----------|:-----------|:-------------------|
| CrewAI | `crew.kickoff()` | `run_agent(question)` |
| LangGraph | `graph.invoke(state)` | The while loop |
| OpenAI Agents SDK | `Runner.run(agent, input)` | `run_agent(question)` |
| AutoGen | `agent.initiate_chat(...)` | `run_agent(question)` |
| All of the above | `"finish_reason": "stop"` | `stop_reason == "end_turn"` |

---

## You've Completed Pass 1!

You can now:
✓ **Spot** the agent loop in any codebase
✓ **Identify** the two exit paths (end_turn vs tool_use)
✓ **Recognize** message accumulation
✓ **Read** the tool dispatcher pattern
✓ **Translate** between Anthropic and OpenAI loop syntax
✓ **Understand** why every framework is just this loop in a costume

**Next:**
- **Pass C (Visual):** See the loop as a flowchart — burn the shape in
- **Pass 3 (Templates):** Copy and adapt your own agent loops
